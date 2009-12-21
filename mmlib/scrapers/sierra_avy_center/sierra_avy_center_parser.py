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


class SierraAvyCenterCurrentObsParser(Scraper):
  def __init__(self):
    url = 'http://www.sierraavalanchecenter.org/advisory'
    Scraper.__init__(self, url=url, geography='Tahoe', 
                     valueType='AvalancheConditions')
    self.scrape()

    published_time = self.parsePublishedTime()

    current_obs_query = models.SierraAvyCenterCurrentObservations.all()
    current_obs_query.order('-date_time_added')
    current_obs_data = current_obs_query.get()
    
    if not current_obs_data:
      self.StoreCurrentObsData(published_time=published_time)
    elif current_obs_data.published_time != str(published_time[0]):
      self.StoreCurrentObsData(published_time=published_time)


  def StoreCurrentObsData(self, published_time):
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


class SierraAvyCenterWeatherParser(Scraper):
  def __init__(self):
    url = 'http://www.sierraavalanchecenter.org/advisory'
    Scraper.__init__(self, url=url, geography='Tahoe', 
                     valueType='AvalancheConditions')
    self.scrape()

    published_time = self.parsePublishedTime()

    current_query = models.SierraAvyCenterWeather.all()
    current_query.order('-date_time_added')
    current_data = current_query.get()
    
    if not current_data:
      self.StoreWeatherDataNow(published_time=published_time)
    elif current_data.published_time != str(published_time[0]):
      self.StoreWeatherDataNow(published_time=published_time)
  

  def StoreWeatherDataNow(self, published_time):
    weather_data = self.parseWeatherData()

    new_data = models.SierraAvyCenterWeather()

    new_data.published_time = str(published_time[0])
    new_data.today_7_to_8kft = str(weather_data[0])
    new_data.tonight_7_to_8kft = str(weather_data[1])
    new_data.tomorrow_7_to_8kft = str(weather_data[2])
    new_data.today_8_to_9kft = str(weather_data[3])
    new_data.tonight_8_to_9kft = str(weather_data[4])
    new_data.tomorrow_8_to_9kft = str(weather_data[5])

    new_data.put()


  def parsePublishedTime(self):
    block = self.soup.find('td', attrs={'class':"views-field views-field-field-pubtime-php-value"})
    time = block.findNext('strong').contents
    return time


  def parseWeatherData(self):
    dat = []
    block = self.soup.findAll(attrs={'class':
      "views-field-field-2-day-wx-forecast-value"})

    for tag in block:
      tr_sections = tag.findAllNext('tr')
      low_data = tr_sections[2]
      high_data = tr_sections[9]
      count = 0
      for td in low_data:
#        print count
#        print td
        if count in (3, 5, 7):
          dat.append(td.contents[0])
#          print td
        count += 1
      count = 0
      for td in high_data:
#        print count
#        print td
        if count in (3, 5, 7):
          dat.append(td.contents[0])
#          print td
        count += 1
    logging.info('dat = %s' % str(dat))
    return dat


class SierraAvyCenterTemperatureParser(Scraper):
  def __init__(self):
    url = 'http://www.sierraavalanchecenter.org/advisory'
    Scraper.__init__(self, url=url, geography='Tahoe', 
                     valueType='AvalancheConditions')
    self.scrape()

    published_time = self.parsePublishedTime()

    current_query = models.SierraAvyCenterTemperatures.all()
    current_query.order('-date_time_added')
    current_data = current_query.get()

    if not current_data:
      self.StoreTempDataNow(published_time=published_time)
    elif current_data.published_time != str(published_time[0]):
      self.StoreTempDataNow(published_time=published_time)


  def StoreTempDataNow(self, published_time):
    temp_data = self.parseTempData()

    new_data = models.SierraAvyCenterTemperatures()

    new_data.published_time = str(published_time[0])
    new_data.today_7_to_8kft = str(temp_data[0])
    new_data.tonight_7_to_8kft = str(temp_data[1])
    new_data.tomorrow_7_to_8kft = str(temp_data[2])
    new_data.today_8_to_9kft = str(temp_data[3])
    new_data.tonight_8_to_9kft = str(temp_data[4])
    new_data.tomorrow_8_to_9kft = str(temp_data[5])

    new_data.put()


  def parsePublishedTime(self):
    block = self.soup.find('td', attrs={'class':"views-field views-field-field-pubtime-php-value"})
    time = block.findNext('strong').contents
    return time


  def parseTempData(self):
    dat = []
    block = self.soup.findAll(attrs={'class':
      "views-field-field-2-day-wx-forecast-value"})

    for tag in block:
      tr_sections = tag.findAllNext('tr')
      low_data = tr_sections[3]
      high_data = tr_sections[10]
      count = 0
      for td in low_data:
#        print count
#        print td
        if count in (3, 5, 7):
          dat.append(td.contents[0])
#          print td
        count += 1
      count = 0
      for td in high_data:
#        print count
#        print td
        if count in (3, 5, 7):
          dat.append(td.contents[0])
#          print td
        count += 1
    logging.info('dat = %s' % str(dat))
    return dat


class SierraAvyCenterWindParser(Scraper):
  def __init__(self):
    url = 'http://www.sierraavalanchecenter.org/advisory'
    Scraper.__init__(self, url=url, geography='Tahoe', 
                     valueType='AvalancheConditions')
    self.scrape()

    published_time = self.parsePublishedTime()

    current_query = models.SierraAvyCenterWindDirection.all()
    current_query.order('-date_time_added')
    current_data = current_query.get()

    if not current_data:
      self.StoreWindDataNow(published_time=published_time)
    elif current_data.published_time != str(published_time[0]):
      self.StoreWindDataNow(published_time=published_time)


  def StoreWindDataNow(self, published_time):
    temp_data = self.parseWindData()

    new_data = models.SierraAvyCenterWindDirection()

    new_data.published_time = str(published_time[0])
    new_data.today_7_to_8kft = str(temp_data[0])
    new_data.tonight_7_to_8kft = str(temp_data[1])
    new_data.tomorrow_7_to_8kft = str(temp_data[2])
    new_data.today_8_to_9kft = str(temp_data[3])
    new_data.tonight_8_to_9kft = str(temp_data[4])
    new_data.tomorrow_8_to_9kft = str(temp_data[5])

    new_data.put()


  def parsePublishedTime(self):
    block = self.soup.find('td', attrs={'class':"views-field views-field-field-pubtime-php-value"})
    time = block.findNext('strong').contents
    return time


  def parseWindData(self):
    dat = []
    block = self.soup.findAll(attrs={'class':
      "views-field-field-2-day-wx-forecast-value"})

    for tag in block:
      tr_sections = tag.findAllNext('tr')
      low_data = tr_sections[4]
      high_data = tr_sections[11]
      count = 0
      for td in low_data:
#        print count
#        print td
        if count in (3, 5, 7):
          dat.append(td.contents[0])
#          print td
        count += 1
      count = 0
      for td in high_data:
#        print count
#        print td
        if count in (3, 5, 7):
          dat.append(td.contents[0])
#          print td
        count += 1
    logging.info('dat = %s' % str(dat))
    return dat


class SierraAvyCenterWindSpeedParser(Scraper):
  def __init__(self):
    url = 'http://www.sierraavalanchecenter.org/advisory'
    Scraper.__init__(self, url=url, geography='Tahoe', 
                     valueType='AvalancheConditions')
    self.scrape()

    published_time = self.parsePublishedTime()

    current_query = models.SierraAvyCenterWindSpeed.all()
    current_query.order('-date_time_added')
    current_data = current_query.get()

    if not current_data:
      self.StoreWindSpeedDataNow(published_time=published_time)
    elif current_data.published_time != str(published_time[0]):
      self.StoreWindSpeedDataNow(published_time=published_time)


  def StoreWindSpeedDataNow(self, published_time):
    temp_data = self.parseWindSpeedData()

    new_data = models.SierraAvyCenterWindSpeed()

    new_data.published_time = str(published_time[0])
    new_data.today_7_to_8kft = str(temp_data[0])
    new_data.tonight_7_to_8kft = str(temp_data[1])
    new_data.tomorrow_7_to_8kft = str(temp_data[2])
    new_data.today_8_to_9kft = str(temp_data[3])
    new_data.tonight_8_to_9kft = str(temp_data[4])
    new_data.tomorrow_8_to_9kft = str(temp_data[5])

    new_data.put()


  def parsePublishedTime(self):
    block = self.soup.find('td', attrs={'class':"views-field views-field-field-pubtime-php-value"})
    time = block.findNext('strong').contents
    return time


  def parseWindSpeedData(self):
    dat = []
    block = self.soup.findAll(attrs={'class':
      "views-field-field-2-day-wx-forecast-value"})

    for tag in block:
      tr_sections = tag.findAllNext('tr')
      low_data = tr_sections[5]
      high_data = tr_sections[12]
      count = 0
      for td in low_data:
#        print count
#        print td
        if count in (3, 5, 7):
          dat.append(td.contents[0])
#          print td
        count += 1
      count = 0
      for td in high_data:
#        print count
#        print td
        if count in (3, 5, 7):
          dat.append(td.contents[0])
#          print td
        count += 1
    logging.info('dat = %s' % str(dat))
    return dat


class SierraAvyCenterExpectedSnowParser(Scraper):
  def __init__(self):
    url = 'http://www.sierraavalanchecenter.org/advisory'
    Scraper.__init__(self, url=url, geography='Tahoe', 
                     valueType='AvalancheConditions')
    self.scrape()

    published_time = self.parsePublishedTime()

    current_query = models.SierraAvyCenterExpectedSnowfall.all()
    current_query.order('-date_time_added')
    current_data = current_query.get()

    if not current_data:
      self.StoreExpectedSnowDataNow(published_time=published_time)
    elif current_data.published_time != str(published_time[0]):
      self.StoreExpectedSnowDataNow(published_time=published_time)


  def StoreExpectedSnowDataNow(self, published_time):
    temp_data = self.parseExpectedSnowData()

    new_data = models.SierraAvyCenterExpectedSnowfall()

    new_data.published_time = str(published_time[0])
    new_data.today_7_to_8kft = str(temp_data[0])
    new_data.tonight_7_to_8kft = str(temp_data[1])
    new_data.tomorrow_7_to_8kft = str(temp_data[2])
    new_data.today_8_to_9kft = str(temp_data[3])
    new_data.tonight_8_to_9kft = str(temp_data[4])
    new_data.tomorrow_8_to_9kft = str(temp_data[5])

    new_data.put()


  def parsePublishedTime(self):
    block = self.soup.find('td', attrs={'class':"views-field views-field-field-pubtime-php-value"})
    time = block.findNext('strong').contents
    return time


  def parseExpectedSnowData(self):
    dat = []
    block = self.soup.findAll(attrs={'class':
      "views-field-field-2-day-wx-forecast-value"})

    for tag in block:
      tr_sections = tag.findAllNext('tr')
      low_data = tr_sections[6]
      high_data = tr_sections[13]
      count = 0
      for td in low_data:
#        print count
#        print td
        if count in (3, 5, 7):
          dat.append(td.contents[0])
#          print td
        count += 1
      count = 0
      for td in high_data:
#        print count
#        print td
        if count in (3, 5, 7):
          dat.append(td.contents[0])
#          print td
        count += 1
    logging.info('dat = %s' % str(dat))
    return dat
