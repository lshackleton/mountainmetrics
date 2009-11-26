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
    intro_paragraph = self.parseBlockText()
###### PROBLEM CODE BELOW #######
    condition = self.parseCondition()
    if condition == 1:
      avalanche_danger_rating = 1
      avalanche_danger_image_url = 1  
    elif condition == 2:
      avalanche_danger_rating = 1
      avalanche_danger_image_url = 1      
    elif condition == 3:
      pass
    else:
      pass 
    
    
    
    new_avalanche_data = models.TodaysAvalancheReport()
    new_avalanche_data.avalanche_report_paragraph = str(intro_paragraph)
    #new_avalanche_data.avalanche_danger_rating = 
    #new_avalanche_data.avalanche_danger_image_url =
    new_avalanche_data.put()
    

  def parseCondition(self):
    block2 = self.soup.find('a', href=re.compile('^http://www.avalanche.org/~uac/encyclopedia/moderate_danger.htm'))
    print block2
    return 

#Have BS -- find in the large mess the BIG section -- from which we pull based on URL to understand what the condition is.  

#Then match based on the tag

#Then yse the block again -- but this time find something else.

  def parseBlockText(self):
    block = self.soup.find('div', id='today')
    intro = block.find('p')
    return str(intro)


