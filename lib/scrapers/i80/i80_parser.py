#!/usr/bin/env python
__author__ = "Bill Ferrell"

"""Parses the DOT i80 live status page. 

i80 Status Page: http://www.dot.ca.gov/hq/roadinfo/i80

This class parses the page and returns an object that allows you to get various status bits. 
"""

from lib.scrapers.scraper import Scraper

class i80Parser(Scraper):
  def __init__(self):
    url = 'http://www.tfl.gov.uk/tfl/livetravelnews/realtime/tube/default.html'
    Scraper.__init__(self, url=url, network='underground', geography='UK-LON', 
                     valueType='line')
    self.scrape()
    self.parse()

  def parse(self):
    self.status = {}
    block = self.soup.find('dl', id='lines')
    lines = block.findAll('dt')
    status = block.findAll('dd')
    ziplist = [lines, status]
    for x in zip(*ziplist):
      line = x[0]['class']
      self.status[line] = {}
      
      if "Good service" == x[1].string:
        self.status[line]['status'] = 'goodservice'
        self.status[line]['description'] = ''
      elif "Minor delays" == x[1].find('h3').string:
        self.status[line]['status'] = 'minordelays'
        self.status[line]['description'] = x[1].find('p').string
      elif "Severe delays" == x[1].find('h3').string:
        self.status[line]['status'] = 'severedelays'
        self.status[line]['description'] = x[1].find('p').string
      elif "Part suspended" == x[1].find('h3').string:
        self.status[line]['status'] = 'partsuspended'
        self.status[line]['description'] = x[1].find('p').string
      elif "Suspended" == x[1].find('h3').string:
        self.status[line]['status'] = "suspended"
        self.status[line]['description'] = x[1].find('p').string
      elif "Part closure" == x[1].find('h3').string:
        self.status[line]['status'] = "partclosure"
        self.status[line]['description'] = x[1].find('p').string
      elif "Planned closure" == x[1].find('h3').string:
        self.status[line]['status'] = "plannedclosure"
        self.status[line]['description'] = x[1].find('p').string
  

  def getStatusValues(self):
    statusValues = []
    if self.status is not None:
      for line in self.status.keys():
        status = self.status[line]['status']
        description = str(self.status[line]['description'])
        statusValues.append(self.makeStatusValue(name=line, status=status, 
                            description=description))
    return statusValues
    