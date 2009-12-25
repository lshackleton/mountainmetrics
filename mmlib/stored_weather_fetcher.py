#!/usr/bin/env python
__author__ = "Bill Ferrell"

"""Parses the AppEngine NOAA weather data stores interesting parts (highs and lows) in specific additional data models. 
"""

import logging
import datetime

from google.appengine.ext import db

import models

age_threshold = datetime.datetime.now() - datetime.timedelta(days=1)

def FetchAndStoreExistingWeatherData():
  """ Fetch Data from app engine and then process and store it in a new model.
  """
  weather_data = FetchPastWeatherData()
  CalculateAndPutData(weather=weather_data)
  logging.info('Success fetching old weather data and storing.')


def YesterdayWeatherFetchAndStore():
  """ Fetch all weather data, process and store it in a new model.
  """
  weather_data = FetchPastWeatherData()
  
  snow_obs = models.SierraAvyCenterCurrentObservations.all()
  snow_obs.filter('date_time_added >', age_threshold)
  snow_data = snow_obs.get()
  snow = snow_data.total_snow_depth_8200ft
  YesterdaysWeatherCalculator(weather=weather_data, snow=snow)
  logging.info('Success fetching ALL old weather data and storing.')


def FetchPastWeatherData(): 
   """Fetch weather from the data we have stored from NOAA.
      Return the weather for the past day. It can then be iterated through.
   """
   # The age threshold requires that this report be run at one hour after 
   # midnight for the region being considered.

   weather = models.ThreeDayWeatherForecast.all()
   weather.filter('date_time_added >', age_threshold)
   
   # TODO: Comment the logging line below out.
   logging.info('weather.count: %s' % str(weather.count()))

   weather_data = weather.fetch(limit=1000)
   return weather_data
   


def CalculateAndPutData(weather):
   """ Given the Weather data for the past day, this routine processes and stores the high and low temp and dew point values."""

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
  

def YesterdaysWeatherCalculator(weather, snow):
    """ Given the Weather data for the past day, process the input and develop 
        values to represent Yesterday's weather.
    """
    initial = weather[0]
  
    noaa_observation_location = initial.noaa_observation_location
    station_id = initial.station_id
    icon_url_base = initial.icon_url_base
    icon_url_name = initial.icon_url_name
    weather_for_db = initial.weather

    dewpoint_f_high = initial.dewpoint_f
    dewpoint_f_low = initial.dewpoint_f
    dewpoint_c_low = initial.dewpoint_c
    dewpoint_c_high = initial.dewpoint_c
    temp_c_high = initial.current_temp_c
    temp_c_low = initial.current_temp_c
    temp_f_high = initial.current_temp_f
    temp_f_low = initial.current_temp_f
    wind_mph_high = initial.wind_mph
    wind_mph_low = initial.wind_mph
    wind_gust_mph_high = initial.wind_gust_mph
    wind_gust_mph_low = initial.wind_gust_mph
    dewpoint_f_high = initial.dewpoint_f
    dewpoint_f_low = initial.dewpoint_f
    dewpoint_c_high = initial.dewpoint_c
    dewpoint_c_low = initial.dewpoint_c
    pressure_mb_high = initial.pressure_mb
    pressure_mb_low = initial.pressure_mb
    pressure_in_high = initial.pressure_in
    pressure_in_low = initial.pressure_in
    visibility_mi_high = initial.visibility_mi
    visibility_mi_low = initial.visibility_mi
    relative_humidity_high = initial.relative_humidity
    relative_humidity_low = initial.relative_humidity

    for datapoint in weather:
      if datapoint.dewpoint_f > dewpoint_f_high:
        dewpoint_f_high = datapoint.dewpoint_f
      if datapoint.dewpoint_f < dewpoint_f_low:
        dewpoint_f_low = datapoint.dewpoint_f
      if datapoint.dewpoint_c > dewpoint_c_high:
        dewpoint_c_high = datapoint.dewpoint_c
      if datapoint.dewpoint_c < dewpoint_c_low:
        dewpoint_c_low = datapoint.dewpoint_c
      if datapoint.current_temp_c > temp_c_high:
        temp_c_high = datapoint.current_temp_c
      if datapoint.current_temp_c < temp_c_low:
        temp_c_low = datapoint.current_temp_c
      if datapoint.current_temp_f > temp_f_high:
        temp_f_high = datapoint.current_temp_f
      if datapoint.current_temp_f < temp_f_low:
        temp_f_low = datapoint.current_temp_f
      if datapoint.wind_mph > wind_mph_high:
        wind_mph_high = datapoint.wind_mph
      if datapoint.wind_mph < wind_mph_low:
        wind_mph_low = datapoint.wind_mph
      if datapoint.wind_gust_mph > wind_gust_mph_high:
        wind_gust_mph_high = datapoint.wind_mph
      if datapoint.wind_gust_mph < wind_gust_mph_low:
        wind_gust_mph_low = datapoint.wind_mph
      if datapoint.pressure_mb > pressure_mb_high:
        pressure_mb_high = datapoint.pressure_mb
      if datapoint.pressure_mb < pressure_mb_low:
        pressure_mb_low = datapoint.pressure_mb
      if datapoint.pressure_in > pressure_in_high:
        pressure_in_high = datapoint.pressure_in
      if datapoint.pressure_in < pressure_in_low:
        pressure_in_low = datapoint.pressure_in
      if datapoint.visibility_mi > visibility_mi_high:
        visibility_mi_high = datapoint.visibility_mi
      if datapoint.visibility_mi < visibility_mi_low:
        visibility_mi_low = datapoint.visibility_mi
      if datapoint.relative_humidity > relative_humidity_high:
        relative_humidity_high = datapoint.relative_humidity
      if datapoint.relative_humidity < relative_humidity_low:
        relative_humidity_low = datapoint.relative_humidity

    

    new = models.YesterdaysWeather()

    new.noaa_observation_location = noaa_observation_location
    new.station_id = station_id
    new.icon_url_base = icon_url_base
    new.icon_url_name = icon_url_name
    new.temp_c_high = temp_c_high
    new.temp_c_low = temp_c_low
    new.temp_f_high = temp_f_high
    new.temp_f_low = temp_f_low
    new.wind_mph_high = wind_mph_high
    new.wind_mph_low = wind_mph_low
    new.wind_gust_mph_high = wind_gust_mph_high
    new.wind_gust_mph_low = wind_gust_mph_low
    new.dewpoint_f_high = dewpoint_f_high
    new.dewpoint_f_low = dewpoint_f_low
    new.dewpoint_c_high = dewpoint_c_high
    new.dewpoint_c_low = dewpoint_c_low
    new.pressure_mb_high = pressure_mb_high
    new.pressure_mb_low = pressure_mb_low
    new.pressure_in_high = pressure_in_high
    new.pressure_in_low = pressure_in_low
    new.weather = weather_for_db
    new.visibility_mi_high = visibility_mi_high
    new.visibility_mi_low = visibility_mi_low
    new.relative_humidity_high = relative_humidity_high
    new.relative_humidity_low = relative_humidity_low
    new.new_snow_8200ft_24_hours = snow

    new.put()
