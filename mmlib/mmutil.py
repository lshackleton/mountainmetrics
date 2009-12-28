#!/usr/bin/env python
__author__ = "Bill Ferrell"

"""Util functions. 
"""

import datetime
import logging

import models
from google.appengine.ext import db
from google.appengine.api import memcache


class DataPopulator(object):

  def handle_weather(self, *args, **kwargs):
    return models.ThreeDayWeatherForecast.all()

  def handle_roads(self, *args, **kwargs):
    return models.DOTi80RoadConditions.all()

  def handle_avalanche(self, *args, **kwargs):
    return models.TodaysAvalancheReport.all()

  def handle_alpine_meadows_snow_report(self, *args, **kwargs):
    return models.AlpineMeadowsSnowReport.all()

  def handle_squaw_valley_snow_report(self, *args, **kwargs):
    return models.SquawValleySnowReport.all()

  def handle_kirkwood_snow_report(self, *args, **kwargs):
    return models.KirkwoodSnowReport.all()

  def handle_expected_snowfall(self, *args, **kwargs):
    return models.ExpectedSnowfall.all()

  def handle_yahoo_weather(self, *args, **kwargs):
    return models.YahooWeatherForecast.all()

  def handle_current_obs(self, *args, **kwargs):
    return models.SierraAvyCenterCurrentObservations.all()

  def handle_sierra_weather(self, *args, **kwargs):
    return models.SierraAvyCenterWeather.all()

  def handle_sierra_temp(self, *args, **kwargs):
    return models.SierraAvyCenterTemperatures.all()

  def handle_sierra_wind_direction(self, *args, **kwargs):
    return models.SierraAvyCenterWindDirection.all()

  def handle_sierra_wind_speed(self, *args, **kwargs):
    return models.SierraAvyCenterWindSpeed.all()

  def handle_sierra_expected_snow(self, *args, **kwargs):
    return models.SierraAvyCenterExpectedSnowfall.all()

  def handle_yesterday_data(self, *args, **kwargs):
    return models.YesterdaysWeather.all()

  def handle_TemperaturePerDay(self, *args, **kwargs):
    return models.TemperaturePerDay.all()

  def handle_snow_fall_graph(self, *args, **kwargs):
    return models.SnowFallGraph.all()


  def handle(self, type, *args, **kwargs):
    data = memcache.get("%s" % type)
    if data is None:
      func = getattr(self, 'handle_%s' % type, None)
      if func is None:
        raise Exception("No handler for type %r" % type)
      raw_data = func(*args, **kwargs)
      raw_data.order('-date_time_added')
      data = raw_data.get()
      if data:
        if data.date_time_added:
          data.date_time_added = (data.date_time_added - 
                                  datetime.timedelta(hours=8))
      memcache.set("%s" % type, data, time=3600)
    
    return data
