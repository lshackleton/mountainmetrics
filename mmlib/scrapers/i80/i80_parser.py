#!/usr/bin/env python
__author__ = "Bill Ferrell"

"""Parses the DOT i80 live status page. 

i80 Status Page: http://www.dot.ca.gov/hq/roadinfo/i80

This class parses the page and returns an object that allows you to get various status bits. 
"""

import re
import logging
 
import models
from mmlib.scrapers.scraper import Scraper

class i80Parser(Scraper):
  def __init__(self):
    logging.info('i80Parser running __init__')
    url = 'http://www.dot.ca.gov/hq/roadinfo/i80'
    Scraper.__init__(self, url=url, geography='Tahoe', 
                     valueType='RoadConditions')
    self.scrape()
    self.parse()
    logging.info('i80Parser finishe parse')

  def parse(self):
    logging.info('i80Parser running Parse')
    self.status = {}
    block = self.soup.find('pre')
    
    logging.info('Prepping to put data into database.')    
    new_i80_conditions = models.DOTi80RoadConditions()
    new_i80_conditions.road_conditions_details = str(block)
    new_i80_conditions.put()
    logging.info('Finished adding to the databse.')