#!/usr/bin/env python
__author__ = "Bill Ferrell"

"""Parses the Sierra avalanche center status page. 

Page found here: http://www.sierraavalanchecenter.org/advisory

This class parses the page and returns an object that allows you to get various status bits. 
"""

import re
import logging

import models
from mmlib.scrapers.scraper import Scraper

class AvalancheConditionsParser(Scraper):
  def __init__(self):
    url = 'http://www.sierraavalanchecenter.org/advisory'
    Scraper.__init__(self, url=url, geography='Tahoe', 
                     valueType='AvalancheConditions')
    self.scrape()
    intro_paragraph = self.parseIntroText()
    low = self.parseDanger(find_value=
      'http://www.avalanche.org/~uac/encyclopedia/low_avalanche_hazard.htm')
    if not low:
      low = self.parseDanger(find_value=
        'http://www.avalanche.org/%7Euac/encyclopedia/low_avalanche_hazard.htm')
    moderate = self.parseDanger(find_value=
      'http://www.avalanche.org/~uac/encyclopedia/moderate_danger.htm')
    if not moderate:
      moderate = self.parseDanger(find_value=
        'http://www.avalanche.org/%7Euac/encyclopedia/moderate_danger.htm')
    considerable = self.parseDanger(find_value=
      'http://www.avalanche.org/~uac/encyclopedia/considerable_danger.htm')
    if not considerable:
       considerable = self.parseDanger(find_value=
        'http://www.avalanche.org/%7Euac/encyclopedia/considerable_danger.htm')
    high = self.parseDanger(find_value=
      'http://www.avalanche.org/~uac/encyclopedia/high_danger.htm')
    if not high:
      high = self.parseDanger(find_value=
        'http://www.avalanche.org/%7Euac/encyclopedia/high_danger.htm')
    extreme = self.parseDanger(find_value=
      'http://www.avalanche.org/~uac/encyclopedia/extreme_danger.htm')
    if not extreme:
      extreme = self.parseDanger(find_value=
        'http://www.avalanche.org/%7Euac/encyclopedia/extreme_danger.htm')

    conditions = [low, moderate, considerable, high, extreme]
    condition_counter = 0
    for condition in conditions:
#      print condition
      if condition:
        condition_counter += 1

    if condition_counter > 1:
      multiple_danger_levels = True
    else:
      multiple_danger_levels = False

    new_avalanche_data = models.TodaysAvalancheReport()

    new_avalanche_data.avalanche_report_paragraph = str(intro_paragraph)
    new_avalanche_data.low_danger = low
    new_avalanche_data.moderate_danger = moderate
    new_avalanche_data.considerable_danger = considerable
    new_avalanche_data.high_danger = high
    new_avalanche_data.extreme_danger = extreme
    new_avalanche_data.multiple_danger_levels = multiple_danger_levels

    new_avalanche_data.put()


  def parseDanger(self, find_value):
    logging.info('starting parseDanger')
    logging.info('findvalue = %s' % find_value)
    block = self.soup.find(attrs={'href': find_value})
# Code for troubleshooting.
#    block = self.soup.findAll(True)
#    for tag in block:
#      print tag.name
#      print tag.attrs

    if block:
      logging.info('Found danger')
#      print 'DANGER'
      return True
    logging.info('Found nothing')
    return False


  def parseIntroText(self):
    intro = None
    block = self.soup.findAll(attrs={'class':"views-field views-field-field-discussion-php-value"})
    for tag in block:
      if tag.name == 'td':
        intro = tag.findNext('p')
        intro = intro.contents[0]
    if not intro:
      intro = 'None'
    
    logging.info('intro = %s' % str(intro))
    return str(intro)
