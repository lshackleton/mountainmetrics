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
from google.appengine.ext import webapp
from google.appengine.api import memcache

#Import the BaseRequestHandler so we have error handling!
from main import BaseRequestHandler

#The data models.
import models

#For handling the time objects
import rfc822  

#The library for actually fetching the data from noaa.
from mmlib.pywapi import get_weather_from_noaa

#The libraries for scraping data
from mmlib.scrapers.i80 import i80_parser
from mmlib.scrapers.avalanche import avalanche_parser
from mmlib.scrapers.alpinemeadows import alpinemeadows_parser


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



def main():
    wsgiref.handlers.CGIHandler().run(webapp.WSGIApplication([
        ('/tasks/process/AddWeatherFetcherTask', AddWeatherFetcherTask),
        ('/tasks/process/Addi80ConditionsFetcherTask',  
          Addi80ConditionsFetcherTask),
        ('/tasks/process/AddAvalancheConditionsFetcherTask',  
          AddAvalancheConditionsFetcherTask),
        ('/tasks/process/AddAlpineMeadowsConditionsFetcherTask',  
          AddAlpineMeadowsConditionsFetcherTask),
        ('/tasks/process/AvalancheConditionsFetcher', 
          AvalancheConditionsFetcher),
        ('/tasks/process/WeatherFetcher', WeatherFetcher),
        ('/tasks/process/i80ConditionsFetcher', i80ConditionsFetcher),
        ('/tasks/process/AlpineMeadowsConditionsFetcher',   
          AlpineMeadowsConditionsFetcher)
        
    ]))

if __name__ == '__main__':
    main()