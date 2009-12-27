#!/usr/bin/env python
__author__ = "Bill Ferrell"

"""Util functions. 
"""

import datetime
import logging

import models
from google.appengine.ext import db
from google.appengine.api import memcache


def SnowfallGraphMaker(data):
  """ This function takes in all the snow data, processes it and returns an img 
      url.
  """
  head = """<img src="http://chart.apis.google.com/chart?chs=400x200&amp;chdlp=b&amp;chf=bg,s,ffffff|c,s,ffffff&amp;chxt=x,y&amp;"""
  x_axis = """"""
  y_axis = """"""
  spacer = """&amp;cht=lc&amp;chd=t:"""
  daily_snowfall_8_9k = """|"""
  daily_snowfall_7_8k = """&amp;"""
  closer = """chdl=7,000+-+8,000+ft|8,000+-+9,000+ft&amp;chco=0000ff,009900&amp;chls=2,1,0|2,3,3" />"""

  complete = (head + x_axis + y_axis + spacer + daily_snowfall_8_9k + 
              daily_snowfall_7_8k + closer)

  return complete


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
