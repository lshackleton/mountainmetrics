#!/usr/bin/env python
"""
Mountain Metrics Cron and Tasks functionality. 

Used to grab data, process it and store it!
"""

__author__ = '(Bill Ferrell)'

import logging
import datetime
import wsgiref.handlers

from google.appengine.api.labs import taskqueue
from google.appengine.ext import webapp

#The data models.
import models

#For handling the time objects
import rfc822  

#The library for actually fetching the data from noaa.
from mmlib.pywapi import get_weather_from_noaa

#The library for fetching i80 conditions.
from mmlib.scrapers.i80 import i80_parser


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



class AddWeatherFetcherTask(webapp.RequestHandler):
  """Cron calls this class to enqueue more AddWeatherFetcherTasks tasks."""
  def get(self):
    logging.info('Running the WeatherFetcher.')
    taskqueue.add(queue_name='WeatherFetcher', url='/tasks/process/WeatherFetcher', eta=one)
    taskqueue.add(queue_name='WeatherFetcher', url='/tasks/process/WeatherFetcher', eta=two)
    taskqueue.add(queue_name='WeatherFetcher', url='/tasks/process/WeatherFetcher', eta=three)
    taskqueue.add(queue_name='WeatherFetcher', url='/tasks/process/WeatherFetcher', eta=four)
    taskqueue.add(queue_name='WeatherFetcher', url='/tasks/process/WeatherFetcher', eta=five)
    taskqueue.add(queue_name='WeatherFetcher', url='/tasks/process/WeatherFetcher', eta=six)
    taskqueue.add(queue_name='WeatherFetcher', url='/tasks/process/WeatherFetcher', eta=seven)
    taskqueue.add(queue_name='WeatherFetcher', url='/tasks/process/WeatherFetcher', eta=eight)
    taskqueue.add(queue_name='WeatherFetcher', url='/tasks/process/WeatherFetcher', eta=nine)
    taskqueue.add(queue_name='WeatherFetcher', url='/tasks/process/WeatherFetcher', eta=ten)
    taskqueue.add(queue_name='WeatherFetcher', url='/tasks/process/WeatherFetcher', eta=eleven)
    taskqueue.add(queue_name='WeatherFetcher', url='/tasks/process/WeatherFetcher', eta=twelve)
    taskqueue.add(queue_name='WeatherFetcher', url='/tasks/process/WeatherFetcher', eta=thirteen)
    taskqueue.add(queue_name='WeatherFetcher', url='/tasks/process/WeatherFetcher', eta=fourteen)
    taskqueue.add(queue_name='WeatherFetcher', url='/tasks/process/WeatherFetcher', eta=fifteen)
    taskqueue.add(queue_name='WeatherFetcher', url='/tasks/process/WeatherFetcher', eta=sixteen)
    taskqueue.add(queue_name='WeatherFetcher', url='/tasks/process/WeatherFetcher', eta=seventeen)
    taskqueue.add(queue_name='WeatherFetcher', url='/tasks/process/WeatherFetcher', eta=eightteen)
    taskqueue.add(queue_name='WeatherFetcher', url='/tasks/process/WeatherFetcher', eta=nineteen)
    taskqueue.add(queue_name='WeatherFetcher', url='/tasks/process/WeatherFetcher', eta=twenty)
    taskqueue.add(queue_name='WeatherFetcher', url='/tasks/process/WeatherFetcher', eta=twentyone)
    taskqueue.add(queue_name='WeatherFetcher', url='/tasks/process/WeatherFetcher', eta=twentytwo)
    taskqueue.add(queue_name='WeatherFetcher', url='/tasks/process/WeatherFetcher', eta=twentythree)

class Addi80ConditionsFetcherTask(webapp.RequestHandler):
  """Cron calls this class to enqueue more AddRoadDataFetcherTasks tasks."""
  taskqueue.add(queue_name='i80ConditionsFetcher', url='/tasks/process/i80ConditionsFetcher')




#class AddForecastFetcherTask(webapp.RequestHandler):
  """Cron calls this class to enqueue more AddForecastFetcherTask tasks."""



class WeatherFetcher(webapp.RequestHandler):
  """ Class used to update the Weather data from NOAA."""
  def get(self):
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
    print 'success!'


class i80ConditionsFetcher(BaseRequestHandler):
  def get(self):
    logging.info('Running the WeatherFetcher.')
    i80_parser.i80Parser()



def main():
    wsgiref.handlers.CGIHandler().run(webapp.WSGIApplication([
        ('/tasks/process/AddWeatherFetcherTask', AddWeatherFetcherTask),
        ('/tasks/process/Addi80ConditionsFetcherTask',  
          Addi80ConditionsFetcherTask),        
        ('/tasks/process/WeatherFetcher', WeatherFetcher),
        ('/tasks/process/i80ConditionsFetcher', i80ConditionsFetcher),
    ]))

if __name__ == '__main__':
    main()
