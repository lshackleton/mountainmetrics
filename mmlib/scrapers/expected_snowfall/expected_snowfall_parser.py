#!/usr/bin/env python
__author__ = "Bill Ferrell"

"""Parses the Sierra avalanche center status page for expected snowfall. 

Page found here: http://www.sierraavalanchecenter.org/advisory

This class parses the page and returns an object that allows you to get various status bits. 
"""

import re
import logging

import models
from mmlib.scrapers.scraper import Scraper

class ExpectedSnowFallParser(Scraper):
  def __init__(self):
    url = 'http://www.sierraavalanchecenter.org/advisory'
    Scraper.__init__(self, url=url, geography='Tahoe', 
                     valueType='AvalancheConditions')
    self.scrape()
    expected_snowfall = self.parseSnowFallData()

    published_time = self.parsePublishedTime()

    new_data = models.ExpectedSnowfall()

    new_data.today = str(expected_snowfall[0])
    new_data.tonight = str(expected_snowfall[1])
    new_data.tomorrow = str(expected_snowfall[2])
    new_data.published_time = str(published_time)

    new_data.put()


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

