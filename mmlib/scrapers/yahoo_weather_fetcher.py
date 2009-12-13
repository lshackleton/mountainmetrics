#!/usr/bin/env python
__author__ = "Bill Ferrell"

"""Parses the Squaw Valley Snow report page. 

Page found here: http://www.squaw.com/winter/mtnreport.html

This class parses the page and returns an object that allows you to get various status bits. 
"""

import re
import logging

from google.appengine.api import urlfetch 
from xml.dom import minidom 

import models


#WOEIDs
## WOEID is used to tell Yahoo the location for which you want data.
tahoe_city = 2503603

WEATHER_URL = 'http://xml.weather.yahoo.com/forecastrss?p=%s' 
WEATHER_NS = 'http://xml.weather.yahoo.com/ns/rss/1.0' 

def parse(url): 
   result = urlfetch.fetch(url) 
   if result.status_code == 200: 
           return minidom.parseString(result.content) 

def weather_for_zip(zip_code): 
    url = WEATHER_URL % zip_code 
    dom = parse(url) 
    forecasts = [] 
    for node in dom.getElementsByTagNameNS(WEATHER_NS, 'forecast'): 
        forecasts.append({ 
            'date': node.getAttribute('date'), 
            'low': node.getAttribute('low'), 
            'high': node.getAttribute('high'), 
            'condition': node.getAttribute('text') 
        }) 
    return { 
        'forecasts': forecasts, 
        'title': dom.getElementsByTagName('title')[0].firstChild.data 
    }


print 'Content-Type: text/plain' 
print '' 
print weather_for_zip('94089')  

