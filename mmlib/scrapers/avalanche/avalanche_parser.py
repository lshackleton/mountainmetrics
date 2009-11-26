#!/usr/bin/env python
__author__ = "Bill Ferrell"

"""Parses the DOT i80 live status page. 

i80 Status Page: http://www.dot.ca.gov/hq/roadinfo/i80

This class parses the page and returns an object that allows you to get various status bits. 
"""

import re

import models
from mmlib.scrapers.scraper import Scraper

class AvalancheConditionsParser(Scraper):
  def __init__(self):
    url = 'http://www.sierraavalanchecenter.org/advisory.php'
    Scraper.__init__(self, url=url, geography='Tahoe', 
                     valueType='RoadConditions')
    self.scrape()
    self.parse()

  def parse(self):
    block2 = self.soup.find('a', href=re.compile('^http://www.avalanche.org/~uac/encyclopedia/moderate_danger.htm'))
    print block2

    block = self.soup.find('div', id='today')
    intro = block.find('p')


    new_avalanche_data = models.TodaysAvalancheReport()
    new_avalanche_data.avalanche_report_paragraph = str(intro)
    #new_avalanche_data.avalanche_danger_rating = 
    #new_avalanche_data.avalanche_danger_image_url =
    new_avalanche_data.put()
