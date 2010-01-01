#!/usr/bin/env python
"""
Mountain Metrics Cron and Tasks functionality. 

Used to grab data, process it and store it!
"""

__author__ = 'Bill Ferrell'

import logging
import datetime
import wsgiref.handlers

from google.appengine.api.labs import taskqueue
from google.appengine.api import memcache
from google.appengine.ext import webapp
from google.appengine.ext import db

#Import the BaseRequestHandler so we have error handling!
from main import BaseRequestHandler

#The data models.
import models
from models import DOTi80RoadConditions, YesterdayWeather

#For handling the time objects
import rfc822  

#The library for fetching the data from noaa.
from mmlib.pywapi import get_weather_from_noaa

#The library for deleting old data from the datastore
from mmlib import delete_functions

#The library for processing weather data already stored on site
from mmlib.stored_weather_fetcher import FetchAndStoreExistingWeatherData
from mmlib.stored_weather_fetcher import YesterdayWeatherFetchAndStore
from mmlib.stored_weather_fetcher import CreateSnowFallGraph

#The libraries for scraping data
from mmlib.scrapers.i80 import i80_parser
from mmlib.scrapers.avalanche import avalanche_parser
from mmlib.scrapers.alpinemeadows import alpinemeadows_parser
from mmlib.scrapers.squaw import squaw_parser
from mmlib.scrapers.kirkwood import kirkwood_parser
from mmlib.scrapers.expected_snowfall import expected_snowfall_parser
from mmlib.scrapers.sierra_avy_center import sierra_avy_center_parser
from mmlib.scrapers import yahoo_weather_fetcher

## Set logging level.
logging.getLogger().setLevel(logging.INFO)

today = datetime.date.today()
oneday = datetime.timedelta(days=1)
tomorrow = today + oneday
midnight = datetime.datetime.combine(tomorrow, datetime.time(0, 50, 1))
one = datetime.datetime.combine(tomorrow, datetime.time(1, 50, 1))
two = datetime.datetime.combine(tomorrow, datetime.time(2, 50, 1))
three = datetime.datetime.combine(tomorrow, datetime.time(3, 50, 1))
four = datetime.datetime.combine(tomorrow, datetime.time(4, 50, 1))
five = datetime.datetime.combine(tomorrow, datetime.time(5, 50, 1))
six = datetime.datetime.combine(tomorrow, datetime.time(6, 50, 1))
seven = datetime.datetime.combine(tomorrow, datetime.time(7, 50, 1))
eight = datetime.datetime.combine(tomorrow, datetime.time(8, 50, 1))
nine = datetime.datetime.combine(tomorrow, datetime.time(9, 50, 1))
ten = datetime.datetime.combine(tomorrow, datetime.time(10, 50, 1))
eleven = datetime.datetime.combine(tomorrow, datetime.time(11, 50, 1))
twelve = datetime.datetime.combine(tomorrow, datetime.time(12, 50, 1))
thirteen = datetime.datetime.combine(tomorrow, datetime.time(13, 50, 1))
fourteen = datetime.datetime.combine(tomorrow, datetime.time(14, 50, 1))
fifteen = datetime.datetime.combine(tomorrow, datetime.time(15, 50, 1))
sixteen = datetime.datetime.combine(tomorrow, datetime.time(16, 50, 1))
seventeen = datetime.datetime.combine(tomorrow, datetime.time(17, 50, 1))
eightteen = datetime.datetime.combine(tomorrow, datetime.time(18, 50, 1))
nineteen = datetime.datetime.combine(tomorrow, datetime.time(19, 50, 1))
twenty = datetime.datetime.combine(tomorrow, datetime.time(20, 50, 1))
twentyone = datetime.datetime.combine(tomorrow, datetime.time(21, 50, 1))
twentytwo = datetime.datetime.combine(tomorrow, datetime.time(22, 50, 1))
twentythree = datetime.datetime.combine(tomorrow, datetime.time(23, 50, 1))

one_week_ago = today + datetime.timedelta(days=-7)

twenty_four_hour_schedule = [one, two, three, four, five, six, seven, eight, 
                             nine, ten, eleven, twelve, thirteen, fourteen,
                             fifteen, sixteen, seventeen, eightteen, nineteen,
                             twenty, twentyone, twentytwo, twentythree, midnight
                            ]


class AddWeatherFetcherTask(BaseRequestHandler):
  """Cron calls this class to enqueue more AddWeatherFetcher tasks."""
  def get(self):
    logging.info('Running the AddWeatherFetcherTask.')
    for eta in twenty_four_hour_schedule:
      taskqueue.Task(url='/tasks/process/WeatherFetcher',
                     eta=eta).add(queue_name='WeatherFetcher')


class Addi80ConditionsFetcherTask(BaseRequestHandler):
  """Cron calls this class to enqueue more AddRoadDataFetcher tasks."""
  def get(self):
    logging.info('Running the Addi80ConditionsFetcherTask.')
    taskqueue.Task(url='/tasks/process/i80ConditionsFetcher').add(
                   queue_name='i80ConditionsFetcher')

class AddHourlyTask(BaseRequestHandler):
 """Cron calls this class to add tasks that need to be added hourly."""
 def get(self):
   logging.info('Running the AddHourlyTask.')
   taskqueue.Task(url='/tasks/process/SierraAvyCenterExpectedSnowFetcher').add(
                  queue_name='AvalancheConditionsFetcher')
   taskqueue.Task(url='/tasks/process/SierraAvyCenterCurrentObsFetcher').add(
                  queue_name='AvalancheConditionsFetcher')
   taskqueue.Task(url='/tasks/process/SierraAvyCenterWeatherFetcher').add(
                  queue_name='AvalancheConditionsFetcher')
   taskqueue.Task(url='/tasks/process/SierraAvyCenterTempFetcher').add(
                  queue_name='AvalancheConditionsFetcher')               
   taskqueue.Task(url='/tasks/process/SierraAvyCenterWindFetcher').add(
                  queue_name='AvalancheConditionsFetcher')
   taskqueue.Task(url='/tasks/process/SierraAvyCenterWindSpeedFetcher').add(
                  queue_name='AvalancheConditionsFetcher')
   taskqueue.Task(url='/tasks/process/StoredWeatherProcesser').add(
                  queue_name='General')
   taskqueue.Task(url='/tasks/process/YesterdayWeatherProcesser').add(
                  queue_name='General')
   taskqueue.Task(url='/tasks/process/SnowFallGraphCreater').add(
                  queue_name='General')
   taskqueue.Task(url='/tasks/process/YahooWeatherFetcher').add(
                  queue_name='General')


class AddAvalancheConditionsFetcherTask(BaseRequestHandler):
 """Cron calls this class to enqueue more AvalancheConditionsFetcher tasks."""
 def get(self):
   logging.info('Running the AvalancheConditionsFetcherTask.')
   taskqueue.Task(url='/tasks/process/AvalancheConditionsFetcher').add(
                  queue_name='AvalancheConditionsFetcher')

class AddAlpineMeadowsConditionsFetcherTask(BaseRequestHandler):
  """Cron calls this class to enqueue more AddAlpineMeadowsConditionsFetcher 
     tasks.
  """
  def get(self):
    logging.info('Running the AddAlpineMeadowsConditionsFetcherTask.')
    taskqueue.Task(url='/tasks/process/AlpineMeadowsConditionsFetcher').add(
                   queue_name='ResortReportFetcher')

class AddSquawValleyConditionsFetcherTask(BaseRequestHandler):
  """Cron calls this class to enqueue more AddSquawValleyConditionsFetcher 
     tasks.
  """
  def get(self):
    logging.info('Running the AddSquawValleyConditionsFetcherTask.')
    taskqueue.Task(url='/tasks/process/SquawValleyConditionsFetcher').add(
                   queue_name='ResortReportFetcher')

class AddKirkwoodConditionsFetcherTask(BaseRequestHandler):
   """Cron calls this class to enqueue more AddKirkwoodConditionsFetcher 
      tasks.
   """
   def get(self):
     logging.info('Running the AddKirkwoodConditionsFetcherTask.')
     taskqueue.Task(url='/tasks/process/KirkwoodConditionsFetcher').add(
                    queue_name='ResortReportFetcher')

class AddExpectedSnowfallFetcherTask(BaseRequestHandler):
   """Cron calls this class to enqueue more AddExpectedSnowfallFetcher 
      tasks.
   """
   def get(self):
     logging.info('Running the AddExpectedSnowfallFetcherTask.')
     taskqueue.Task(url='/tasks/process/ExpectedSnowfallFetcher').add(
                    queue_name='AvalancheConditionsFetcher')


class PullYesterdayDataAndStore(BaseRequestHandler):
  """ This function pulls yesterday's weather data and stores it in the   
      Yesterday table.
  """
  def get(self):
    logging.info('Running the PullYesterdayDataAndStore.')
    process_yesterday.PullAndStoreData()
    logging.info('Completed PullYesterdayDataAndStore.')


class YahooWeatherFetcher(BaseRequestHandler):
  """ This function pulls weather from the Yahoo RSS feed.
  """
  def get(self):
    logging.info('Running the YahooWeatherFetcher.')
    yahoo_weather.PullAndStoreData()
    logging.info('Completed YahooWeatherFetcher.')


class WeatherFetcher(BaseRequestHandler):
  """ Class used to update the Weather data from NOAA."""

  def WeatherFetcherprocess(self):
    logging.info('Running the WeatherFetcher.')

    a = get_weather_from_noaa('KTRK')
    # KTRK is the station id for Tahoe / Truckee
    try:
      time_var = a["observation_time"]
      time_var = rfc822.parsedate_tz(time_var)
    except:
      time_var = datetime.datetime.now()

    new_forecast_data = models.ThreeDayWeatherForecast()
    
    new_forecast_data.noaa_observation_time = time_var
    try:
      new_forecast_data.noaa_observation_location = a["location"]
    except:
      pass
    try:
      new_forecast_data.current_temp_c = float(a["temp_c"])
    except:
      pass
    try:
      new_forecast_data.current_temp_f = float(a["temp_f"])
    except:
      pass
    try:
      new_forecast_data.temperature_string = a["temperature_string"]
    except:
      pass
    try:
      new_forecast_data.wind_string = a["wind_string"]
    except:
      pass
    try:
      new_forecast_data.wind_dir = a["wind_dir"]
    except:
      pass
    try:
      new_forecast_data.wind_mph = float(a["wind_mph"])
    except:
      pass
    try:
      new_forecast_data.dewpoint_string = a["dewpoint_string"]
    except:
      pass
    try:
      new_forecast_data.dewpoint_f = float(a["dewpoint_f"])
    except:
      pass
    try:
      new_forecast_data.dewpoint_c = float(a["dewpoint_c"])
    except:
      pass
    try:
      new_forecast_data.pressure_string = a["pressure_string"]
    except:
      pass
    try:
      new_forecast_data.pressure_mb = float(a["pressure_mb"])
    except:
      pass
    try:
      new_forecast_data.pressure_in = float(a["pressure_in"])
    except:
      pass
    try:
      new_forecast_data.weather = a["weather"]
    except:
      pass
    try:
      new_forecast_data.icon_url_base = a["icon_url_base"]
    except:
      pass
    try:
      new_forecast_data.icon_url_name = a["icon_url_name"]
    except:
      pass
    try:
      new_forecast_data.two_day_history_url = a["two_day_history_url"]
    except:
      pass
    try:
      new_forecast_data.station_id = a["station_id"]
    except:
      pass
    try:
      new_forecast_data.wind_gust_mph = float(a["wind_gust_mph"])
    except:
      pass
    try:
      new_forecast_data.visibility_mi = float(a["visibility_mi"])
    except:
      pass
    try:
      new_forecast_data.relative_humidity = float(a["relative_humidity"])
    except:
      pass


    new_forecast_data.put()
    logging.info('SUCCESS: Running the WeatherFetcher.')
    memcache.flush_all()
    logging.info('memcache.flush_all() run.')    

  def get(self):
    self.WeatherFetcherprocess()

  def post(self):
    self.WeatherFetcherprocess()


class i80ConditionsFetcher(BaseRequestHandler):

  def i80ConditionsFetcherprocess(self):
    logging.info('Running the i80ConditionsFetcher.')
    i80_parser.i80Parser()
    logging.info('SUCCESS: Running the i80ConditionsFetcher.')
    memcache.flush_all()
    logging.info('memcache.flush_all() run.')

  def get(self):
    self.i80ConditionsFetcherprocess()

  def post(self):
    self.i80ConditionsFetcherprocess()    


class AvalancheConditionsFetcher(BaseRequestHandler):
  
  def AvalancheConditionsFetcherProcess(self):
    logging.info('Running the AvalancheConditionsFetcher.')
    avalanche_parser.AvalancheConditionsParser()
    logging.info('SUCCESS: Running the AvalancheConditionsFetcher.')
    memcache.flush_all()
    logging.info('memcache.flush_all() run.')
  
  def get(self):
    self.AvalancheConditionsFetcherProcess()

  def post(self):
    self.AvalancheConditionsFetcherProcess()


class AlpineMeadowsConditionsFetcher(BaseRequestHandler):

  def AlpineMeadowsFetcherProcess(self):
    logging.info('Running the AlpineMeadowsConditionsFetcher.')
    alpinemeadows_parser.AlpineMeadowsSnowReportParser()
    logging.info('SUCCESS: Running the AlpineMeadowsConditionsFetcher.')
    memcache.flush_all()
    logging.info('memcache.flush_all() run.')

  def get(self):
    self.AlpineMeadowsFetcherProcess()

  def post(self):
    self.AlpineMeadowsFetcherProcess()


class SquawValleyConditionsFetcher(BaseRequestHandler):
  
  def SquawValleyFetcherProcess(self):
    logging.info('Running the SquawValleyFetcherProcess.')
    squaw_parser.SquawSnowReportParser()
    logging.info('SUCCESS: Running the SquawValleyFetcherProcess.')
    memcache.flush_all()
    logging.info('memcache.flush_all() run.')

  def get(self):
    self.SquawValleyFetcherProcess()

  def post(self):
    self.SquawValleyFetcherProcess()


class KirkwoodConditionsFetcher(BaseRequestHandler):

  def KirkwoodFetcherProcess(self):
    logging.info('Running the KirkwoodFetcherProcess.')
    kirkwood_parser.KirkwoodSnowReportParser()
    logging.info('SUCCESS: Running the KirkwoodFetcherProcess.')
    memcache.flush_all()
    logging.info('memcache.flush_all() run.')

  def get(self):
    self.KirkwoodFetcherProcess()

  def post(self):
    self.KirkwoodFetcherProcess()


class ExpectedSnowfallFetcher(BaseRequestHandler):

  def ExpectedSnowfallProcess(self):
    logging.info('Running the ExpectedSnowfallProcess.')
    expected_snowfall_parser.ExpectedSnowFallParser()
    logging.info('SUCCESS: Running the ExpectedSnowfallProcess.')
    memcache.flush_all()
    logging.info('memcache.flush_all() run.')

  def get(self):
    self.ExpectedSnowfallProcess()

  def post(self):
    self.ExpectedSnowfallProcess()

class SierraAvyCenterExpectedSnowFetcher(BaseRequestHandler):

  def SierraAvyCenterExpectedSnowProcess(self):
    logging.info('Running the SierraAvyCenterExpectedSnowProcess.')
    sierra_avy_center_parser.SierraAvyCenterExpectedSnowParser()
    logging.info('SUCCESS: Running the SierraAvyCenterExpectedSnowProcess.')
    memcache.flush_all()
    logging.info('memcache.flush_all() run.')

  def get(self):
    self.SierraAvyCenterExpectedSnowProcess()

  def post(self):
    self.SierraAvyCenterExpectedSnowProcess()


class SierraAvyCenterCurrentObsFetcher(BaseRequestHandler):

  def SierraAvyCenterCurrentObsProcess(self):
    logging.info('Running the SierraAvyCenterCurrentObsProcess.')
    sierra_avy_center_parser.SierraAvyCenterCurrentObsParser()
    logging.info('SUCCESS: Running the SierraAvyCenterCurrentObsProcess.')
    memcache.flush_all()
    logging.info('memcache.flush_all() run.')

  def get(self):
    self.SierraAvyCenterCurrentObsProcess()

  def post(self):
    self.SierraAvyCenterCurrentObsProcess()


class SierraAvyCenterWeatherFetcher(BaseRequestHandler):

  def SierraAvyCenterWeatherProcess(self):
    logging.info('Running the SierraAvyCenterWeatherProcess.')
    sierra_avy_center_parser.SierraAvyCenterWeatherParser()
    logging.info('SUCCESS: Running the SierraAvyCenterWeatherProcess.')
    memcache.flush_all()
    logging.info('memcache.flush_all() run.')

  def get(self):
    self.SierraAvyCenterWeatherProcess()

  def post(self):
    self.SierraAvyCenterWeatherProcess()


class SierraAvyCenterTempFetcher(BaseRequestHandler):

  def SierraAvyCenterTempProcess(self):
    logging.info('Running the SierraAvyCenterTempProcess.')
    sierra_avy_center_parser.SierraAvyCenterTemperatureParser()
    logging.info('SUCCESS: Running the SierraAvyCenterTempProcess.')
    memcache.flush_all()
    logging.info('memcache.flush_all() run.')

  def get(self):
    self.SierraAvyCenterTempProcess()

  def post(self):
    self.SierraAvyCenterTempProcess()


class SierraAvyCenterWindFetcher(BaseRequestHandler):

  def SierraAvyCenterWindProcess(self):
    logging.info('Running the SierraAvyCenterWindProcess.')
    sierra_avy_center_parser.SierraAvyCenterWindParser()
    logging.info('SUCCESS: Running the SierraAvyCenterWindProcess.')
    memcache.flush_all()
    logging.info('memcache.flush_all() run.')

  def get(self):
    self.SierraAvyCenterWindProcess()

  def post(self):
    self.SierraAvyCenterWindProcess()


class SierraAvyCenterWindSpeedFetcher(BaseRequestHandler):

  def SierraAvyCenterWindSpeedProcess(self):
    logging.info('Running the SierraAvyCenterWindSpeedFetcher.')
    sierra_avy_center_parser.SierraAvyCenterWindSpeedParser()
    logging.info('SUCCESS: Running the SierraAvyCenterWindSpeedFetcher.')
    memcache.flush_all()
    logging.info('memcache.flush_all() run.')

  def get(self):
    self.SierraAvyCenterWindSpeedProcess()

  def post(self):
    self.SierraAvyCenterWindSpeedProcess()


class StoredWeatherProcesser(BaseRequestHandler):

  def StoredWeatherFetcher(self):
    logging.info('Running the StoredWeatherFetcher.')
    FetchAndStoreExistingWeatherData()
    logging.info('SUCCESS: Running the StoredWeatherFetcher.')
    memcache.flush_all()
    logging.info('memcache.flush_all() run.')

  def get(self):
    self.StoredWeatherFetcher()

  def post(self):
    self.StoredWeatherFetcher()


class YesterdayWeatherProcesser(BaseRequestHandler):
  
  def YesterdayWeatherProcess(self):
    logging.info('Running the YesterdayWeatherProcess.')
    YesterdayWeatherFetchAndStore()
    logging.info('SUCCESS: Running the YesterdayWeatherProcess.')
    memcache.flush_all()
    logging.info('memcache.flush_all() run.')

  def get(self):
    self.YesterdayWeatherProcess()

  def post(self):
    self.YesterdayWeatherProcess()


class YahooWeatherFetcher(BaseRequestHandler):
  
  def YahooFetcherProcess(self):
    logging.info('Running the YahooFetcherProcess.')
    yahoo_weather_fetcher.run()
    logging.info('SUCCESS: Running the YahooFetcherProcess.')
    memcache.flush_all()
    logging.info('memcache.flush_all() run.')
    
  def get(self):
    self.YahooFetcherProcess()

  def post(self):
    self.YahooFetcherProcess()


class SnowFallGraphCreater(BaseRequestHandler):

  def SnowFallGraphCreaterProcess(self):
    logging.info('Running the SnowFallGraphCreaterProcess.')
    CreateSnowFallGraph()
    logging.info('SUCCESS: Running the SnowFallGraphCreaterProcess.')
    memcache.flush_all()
    logging.info('memcache.flush_all() run.')

  def get(self):
    self.SnowFallGraphCreaterProcess()

  def post(self):
    self.SnowFallGraphCreaterProcess()



class BulkDeleter(BaseRequestHandler):
  
  def BulkDeleteProcess(self):
    logging.info('Running the BulkDeleteProcess.')
    delete_functions.Deletei80RoadData()
    delete_functions.DeleteYesterdaysWeatherData()
    logging.info('SUCCESS: Running the BulkDeleteProcess.')

  def get(self):
    self.BulkDeleteProcess()

  def post(self):
    self.BulkDeleteProcess()


class AllFetcher(BaseRequestHandler):

  def AllFetcherProcess(self):
    logging.info('Running the AllFetcherProcess.')

    kirkwood = KirkwoodConditionsFetcher()
    kirkwood.KirkwoodFetcherProcess()
    squaw = SquawValleyConditionsFetcher()
    squaw.SquawValleyFetcherProcess()
    alpine = AlpineMeadowsConditionsFetcher()
    alpine.AlpineMeadowsFetcherProcess()
    avalanche = AvalancheConditionsFetcher()
    avalanche.AvalancheConditionsFetcherProcess()
    i80 = i80ConditionsFetcher()
    i80.i80ConditionsFetcherprocess()
    weather = WeatherFetcher()
    weather.WeatherFetcherprocess()
    expected_snowfall = ExpectedSnowfallFetcher()
    expected_snowfall.ExpectedSnowfallProcess()
    yahoo_weather = YahooWeatherFetcher()
    yahoo_weather.YahooFetcherProcess()
    current_observations = SierraAvyCenterCurrentObsFetcher()
    current_observations.SierraAvyCenterCurrentObsProcess()
    sierra_avy_center_expected_snow = SierraAvyCenterExpectedSnowFetcher()
    sierra_avy_center_expected_snow.SierraAvyCenterExpectedSnowProcess()
    sierra_avy_center_weather = SierraAvyCenterWeatherFetcher()
    sierra_avy_center_weather.SierraAvyCenterWeatherProcess()
    sierra_avy_center_temp = SierraAvyCenterTempFetcher()
    sierra_avy_center_temp.SierraAvyCenterTempProcess()
    sierra_avy_center_wind = SierraAvyCenterWindFetcher()
    sierra_avy_center_wind.SierraAvyCenterWindProcess()
    sierra_avy_center_wind_speed = SierraAvyCenterWindSpeedFetcher()
    sierra_avy_center_wind_speed.SierraAvyCenterWindSpeedProcess()

    stored_weather = StoredWeatherProcesser()
    stored_weather.StoredWeatherFetcher()
    yesterdaysweather = YesterdayWeatherProcesser()
    yesterdaysweather.YesterdayWeatherProcess()


    logging.info('SUCCESS: Running the AllFetcherProcess.')
    memcache.flush_all()
    logging.info('memcache.flush_all() run.')

  def get(self):
    self.AllFetcherProcess()


def main():
    wsgiref.handlers.CGIHandler().run(webapp.WSGIApplication([
        ('/tasks/process/AddWeatherFetcherTask', AddWeatherFetcherTask),
        ('/tasks/process/Addi80ConditionsFetcherTask',  
          Addi80ConditionsFetcherTask),
        ('/tasks/process/AddAvalancheConditionsFetcherTask',  
          AddAvalancheConditionsFetcherTask),
        ('/tasks/process/AddAlpineMeadowsConditionsFetcherTask',  
          AddAlpineMeadowsConditionsFetcherTask),
        ('/tasks/process/AddSquawValleyConditionsFetcherTask',  
          AddSquawValleyConditionsFetcherTask),
        ('/tasks/process/AddKirkwoodConditionsFetcherTask',  
          AddKirkwoodConditionsFetcherTask),
        ('/tasks/process/AddExpectedSnowfallFetcherTask',  
          AddExpectedSnowfallFetcherTask),
        ('/tasks/process/AddHourlyTask', AddHourlyTask),
# The section above are URLs that the cron job calls -- to queue up fetchers.
# The section below are URLs for actually fetching data.
        ('/tasks/process/AvalancheConditionsFetcher', 
          AvalancheConditionsFetcher),
        ('/tasks/process/WeatherFetcher', WeatherFetcher),
        ('/tasks/process/i80ConditionsFetcher', i80ConditionsFetcher),
        ('/tasks/process/AlpineMeadowsConditionsFetcher',   
          AlpineMeadowsConditionsFetcher),
        ('/tasks/process/SquawValleyConditionsFetcher',   
          SquawValleyConditionsFetcher),
        ('/tasks/process/KirkwoodConditionsFetcher',   
          KirkwoodConditionsFetcher),      
        ('/tasks/process/ExpectedSnowfallFetcher',   
          ExpectedSnowfallFetcher),
        ('/tasks/process/SierraAvyCenterExpectedSnowFetcher',   
          SierraAvyCenterExpectedSnowFetcher),
        ('/tasks/process/SierraAvyCenterCurrentObsFetcher',   
          SierraAvyCenterCurrentObsFetcher),
        ('/tasks/process/SierraAvyCenterWeatherFetcher',   
          SierraAvyCenterWeatherFetcher),
        ('/tasks/process/SierraAvyCenterTempFetcher',   
          SierraAvyCenterTempFetcher),
        ('/tasks/process/SierraAvyCenterWindFetcher',   
          SierraAvyCenterWindFetcher),
        ('/tasks/process/SierraAvyCenterWindSpeedFetcher',   
          SierraAvyCenterWindSpeedFetcher),
        ('/tasks/process/StoredWeatherProcesser',   
          StoredWeatherProcesser),
        ('/tasks/process/SnowFallGraphCreater',   
          SnowFallGraphCreater),
        ('/tasks/process/YesterdayWeatherProcesser',   
          YesterdayWeatherProcesser),
        ('/tasks/process/YahooWeatherFetcher',   
          YahooWeatherFetcher),
# This section contains processes that delete data
        ('/tasks/process/BulkDeleter',   
          BulkDeleter),
# This is intended to only be used by Bill and Lane
        ('/tasks/process/allfetcher',   
          AllFetcher),
    ]))

if __name__ == '__main__':
    main()