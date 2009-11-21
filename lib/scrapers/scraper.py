#!/usr/bin/env python
#

__author__ = "Bill Ferrell"

import sys

from lib.status_value import StatusValue
from third_party.BeautifulSoup import BeautifulSoup

from google.appengine.api import urlfetch

class Scraper(object):
  """Base class for transportation web page scrapers."""
  def __init__(self, url=None, geography=None, valueType=None):
    self.url = url
    self.geography = geography
    self.valueType = valueType

  def scrape(self):
    """Download the URL or exit."""
    self.result = urlfetch.fetch(self.url)
    if ((self.result.status_code == 200) and
        (self.result.content_was_truncated == 0)):
      self.soup = BeautifulSoup(self.result.content)
    else:
      logging.critical("Bad Status Code: ", self.result.status_code, self.url)
      sys.exit(1)

  def makeStatusValue(self, name, status, description):
    """Makes a StatusValue object."""
    return StatusValue(name=name, status=status, description=description,
                       geography=self.geography, valueType=self.valueType)

  def parse(self):
    """Should be implemented by the implementing class to parse the#
       data found in the scrape call. No return value.
    """  
    pass

  def getStatusValues(self):
    """Should return a list of StatusValue objects for the current
       scraper. Should be overridden by the implementing class.
    """
    return []