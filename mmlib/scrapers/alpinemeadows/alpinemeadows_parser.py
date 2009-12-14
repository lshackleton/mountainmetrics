#!/usr/bin/env python
__author__ = "Bill Ferrell"

"""Parses the Alpine Meadows Snow report page. 

Page found here: http://www.skialpine.com/mountain/snow-report

This class parses the page and returns an object that allows you to get various status bits. 
"""

import re
import logging

import models
from mmlib.scrapers.scraper import Scraper


class AlpineMeadowsSnowReportParser(Scraper):
  def __init__(self):
    url = 'http://www.skialpine.com/mountain/snow-report'
    Scraper.__init__(self, url=url, geography='Tahoe', 
                     valueType='AlpineMeadowsConditions')
    self.scrape()
    time = self.parseTimeLastUpdate()
    temp = self.parseTemp()
    current_condition = self.parseWeatherDescription()
    snow_conditions = self.parseSnowConditions()

    upper_m_snowbase = (snow_conditions[1][:-1])
    lower_m_snowbase = (snow_conditions[2][:-1])

    twentyfour_total_in = (snow_conditions[5][:-1])
    twentyfour_total_in_base = (snow_conditions[4][:-1])
    twentyfour_total_in_top = (snow_conditions[5][:-1])
    
    new_snow_total_inches = (snow_conditions[8][:-1])
    new_snow_total_inches_base = (snow_conditions[7][:-1])
    new_snow_total_inches_top = (snow_conditions[8][:-1])        


    lower_mountain_temp_f =  float(snow_conditions[10][:-7])
    upper_mountain_temp_f = float(snow_conditions[11][:-7])

    new_snow_report = models.AlpineMeadowsSnowReport()

    try:
      if snow_conditions[14]:

        wind = snow_conditions[14]
        wind_base = snow_conditions[13]
        wind_top = snow_conditions[14]
        new_snow_report.wind = wind
        new_snow_report.wind_base = wind_base
        new_snow_report.wind_top = wind_top
        logging.info('Have full wind data.')
      elif snow_conditions[13]:
        wind = snow_conditions[13]
        wind_base = None
        wind_top = None
        new_snow_report.wind = wind
        logging.info('Partial wind data.')
    except:
      pass
      logging.info('No wind data.')

    new_snow_report.time_of_report = str(time)
    new_snow_report.current_temp_f = temp
    new_snow_report.upper_mountain_temp_f = upper_mountain_temp_f
    new_snow_report.lower_mountain_temp_f = lower_mountain_temp_f
    new_snow_report.upper_mountain_snow_base_inches = upper_m_snowbase 
    new_snow_report.lower_mountain_snow_base_inches = lower_m_snowbase
    new_snow_report.current_condition = str(current_condition)
    new_snow_report.new_snow_total_inches = new_snow_total_inches
    new_snow_report.new_snow_total_inches_base = new_snow_total_inches_base
    new_snow_report.new_snow_total_inches_top = new_snow_total_inches_top
    new_snow_report.storm_snow_total_inches = twentyfour_total_in
    new_snow_report.storm_snow_total_inches_base = twentyfour_total_in_base
    new_snow_report.storm_snow_total_inches_top = twentyfour_total_in_top
    new_snow_report.twentyfour_hour_snow_total_inches = twentyfour_total_in
    new_snow_report.is_alpine_meadows = True

    new_snow_report.put()


  def parseTimeLastUpdate(self):
    time = None
    block = self.soup.findAll(attrs={'id':"sr_title"})
    for tag in block:
      if tag.name == 'div':
        time = tag.findNext('h2')
        time = time.contents[0]
        logging.info('time: %s' % str(time))
    if not time:
      time = ''
      logging.info('Failing to find data.')
    return time

  def parseTemp(self):
    temp = None
    block = self.soup.findAll(attrs={'id':"weather_details_current"})
    for tag in block:
      if tag.name == 'div':
        temp = tag.findNext('span')
        temp = temp.contents[0]
        temp = temp[:-6]
        logging.info('temp: %s' % temp)
        temp = float(temp)
        logging.info('converting temp into a float')
    if not temp:
      temp = 99999999
      logging.info('Failing to find data.')
    return temp


  def parseWeatherDescription(self):
    weather = None
    block = self.soup.findAll(attrs={'id':"weather_details_current"})
    for tag in block:
      if tag.name == 'div':
        weather = tag.findNext('div')
        weather = weather.contents[0]
        logging.info('weather: %s' % str(weather))
    if not weather:
      weather = ''
      logging.info('Failing to find data.')
    return weather

  def parseSnowConditions(self):
    dat = []
    block = self.soup.find(attrs={'id':"current_snow_conditions"})
    table = block.findNext('table')
    for row in table.findAll("tr"):
      td = row.findAll("td")
      for t in td:
        dat += map(str, t.contents)
    logging.info('dat: %s' % str(dat))
    
    return dat


