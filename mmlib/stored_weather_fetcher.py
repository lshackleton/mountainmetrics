#!/usr/bin/env python
__author__ = "Bill Ferrell"

"""Parses the AppEngine NOAA weather data stores interesting parts (highs and lows) in specific additional data models. 
"""

import logging
import datetime

from google.appengine.ext import db

import models

def FetchAndStoreExistingWeatherData():
  """ Fetch Data from app engine and then process and store it in a new model.
  """
  weather_data = FetchPastWeatherData()
  CalculateAndPutData(weather=weather_data)
  logging.info('Success fetching old weather data and storing.')


def FetchPastWeatherData(): 
   """Fetch weather from the data we have stored from NOAA.
      Return the weather for the past day. It can then be iterated through.
   """
   # The age threshold requires that this report be run at one hour after 
   # midnight for the region being considered.
   age_threshold = datetime.datetime.now() - datetime.timedelta(days=1)
   weather = models.ThreeDayWeatherForecast.all()
   weather.filter('date_time_added >', age_threshold)
   
   # TODO: Comment the logging line below out.
   logging.info('weather.count: %s' % str(weather.count()))

   weather_data = weather.fetch(limit=1000)
   return weather_data
   


def CalculateAndPutData(weather):
   """ """
   
   initial = weather[0]
   
   dewpoint_f_high = initial.dewpoint_f
   dewpoint_f_low = initial.dewpoint_f
   dewpoint_c_low = initial.dewpoint_c
   dewpoint_c_high = initial.dewpoint_c
   current_temp_c_high = initial.current_temp_c
   current_temp_c_low = initial.current_temp_c
   current_temp_f_high = initial.current_temp_f
   current_temp_f_low = initial.current_temp_f
   
   for datapoint in weather:
     if datapoint.dewpoint_f > dewpoint_f_high:
       dewpoint_f_high = datapoint.dewpoint_f
     if datapoint.dewpoint_f < dewpoint_f_low:
       dewpoint_f_low = datapoint.dewpoint_f
     if datapoint.dewpoint_c > dewpoint_c_high:
       dewpoint_c_high = datapoint.dewpoint_c
     if datapoint.dewpoint_c < dewpoint_c_low:
       dewpoint_c_low = datapoint.dewpoint_c
     if datapoint.current_temp_c > current_temp_c_high:
       current_temp_c_high = datapoint.current_temp_c
     if datapoint.current_temp_c < current_temp_c_low:
       current_temp_c_low = datapoint.current_temp_c
     if datapoint.current_temp_f > current_temp_f_high:
       current_temp_f_high = datapoint.current_temp_f
     if datapoint.current_temp_f < current_temp_f_low:
       current_temp_f_low = datapoint.current_temp_f

   new_dew = models.DewpointPerDay()

   new_dew.dewpoint_f_high = dewpoint_f_high
   new_dew.dewpoint_f_low = dewpoint_f_low
   new_dew.dewpoint_c_low = dewpoint_c_low
   new_dew.dewpoint_c_high = dewpoint_c_high

   new_dew.put()

   new_temp = models.TemperaturePerDay()

   new_temp.current_temp_c_high = current_temp_c_high
   new_temp.current_temp_c_low = current_temp_c_low
   new_temp.current_temp_f_high = current_temp_f_high
   new_temp.current_temp_f_low = current_temp_f_low

   new_temp.put()

