#!/usr/bin/env python
__author__ = "Bill Ferrell"

"""Parses the Sierra avalanche center status page for general weather data. 

Page found here: http://www.sierraavalanchecenter.org/advisory

This class parses the page and returns an object that allows you to get various status bits. 
"""

import re
import logging

import models
from mmlib.scrapers.scraper import Scraper

class SierraAvyCenterParser(Scraper):
  def __init__(self):
    url = 'http://www.sierraavalanchecenter.org/advisory'
    Scraper.__init__(self, url=url, geography='Tahoe', 
                     valueType='AvalancheConditions')
    self.scrape()
#    expected_snowfall = self.parseSnowFallData()

    published_time = self.parsePublishedTime()
    current_obs = self.parseCurrentObservations()

    new_obs_data = models.SierraAvyCenterCurrentObservations()
    new_obs_data.published_time = str(published_time[0])
    new_obs_data.temp_0600_8700ft = str(current_obs[0])
    new_obs_data.max_temp_24_hours = str(current_obs[1])
    new_obs_data.avg_wind_direction_24_hours = str(current_obs[2])
    new_obs_data.avg_wind_speed_24_hours = str(current_obs[3])
    new_obs_data.max_wind_gust_24_hours = str(current_obs[4])
    new_obs_data.new_snow_8200ft_24_hours = str(current_obs[5])
    new_obs_data.total_snow_depth_8200ft = str(current_obs[6])

    new_obs_data.put()


  def parsePublishedTime(self):
    block = self.soup.find('td', attrs={'class':"views-field views-field-field-pubtime-php-value"})
    time = block.findNext('strong').contents
    return time


  def parseSnowFallData(self):
    dat = []
    block = self.soup.findAll(attrs={'class':
      "views-field-field-2-day-wx-forecast-value"})

    for tag in block:
      tr_sections = tag.findAllNext('tr')
      raw_data = tr_sections[6]
      count = 0
      for td in raw_data:
#        print count
        if count in (3, 5, 7):
          dat.append(td.contents[0])
#          print td
        count += 1    
    logging.info('dat = %s' % str(dat))
    return dat

  def parseCurrentObservations(self):
    dat = []
    block = self.soup.find(attrs={'class':
      "views-field-field-weather-obs-value"})

    tds = block.findAllNext('td')
    count = 0
    for td in tds:
      if count in (1, 3, 5, 7, 9, 11, 13):
        dat.append(td.contents[0])
      count += 1    
    logging.info('dat = %s' % str(dat))
    return dat
