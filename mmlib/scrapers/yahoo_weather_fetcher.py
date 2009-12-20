#!/usr/bin/env python
__author__ = "Bill Ferrell"

"""Grabs weather data from the Yahoo weather service.
"""

import re
import logging

from google.appengine.api import urlfetch 

from third_party.BeautifulSoup import BeautifulSoup
from xml.dom import minidom 

import models


#WOEIDs
## WOEID is used to tell Yahoo the location for which you want data.
tahoe_city_woeid = 2503603
## Full url: http://weather.yahooapis.com/forecastrss?w=2503603

WEATHER_URL = 'http://weather.yahooapis.com/forecastrss?w=%s' 
WEATHER_NS = 'http://xml.weather.yahoo.com/ns/rss/1.0' 

def run():
  """Function to call to execute fetching data."""
  print 'Content-Type: text/plain' 
  print ''
  print weather_for_woeid(tahoe_city_woeid)

def parse(url): 
   result = urlfetch.fetch(url) 
   if result.status_code == 200: 
     return minidom.parseString(result.content) 

def weather_for_woeid(WOEID): 
    url = WEATHER_URL % WOEID
    dom = parse(url) 
    forecasts = [] 
    for node in dom.getElementsByTagNameNS(WEATHER_NS, 'forecast'): 
      forecasts.append({ 
          'date': node.getAttribute('date'), 
          'low': node.getAttribute('low'), 
          'high': node.getAttribute('high'), 
          'condition': node.getAttribute('text') 
      })
    location = []
    for node in dom.getElementsByTagNameNS(WEATHER_NS, 'location'): 
      location.append({ 
          'city': node.getAttribute('city'), 
          'region': node.getAttribute('region'), 
          'country': node.getAttribute('country') 
      })
    units = []
    for node in dom.getElementsByTagNameNS(WEATHER_NS, 'units'): 
      units.append({ 
          'temperature': node.getAttribute('temperature'), 
          'distance': node.getAttribute('distance'), 
          'pressure': node.getAttribute('pressure'),
          'speed': node.getAttribute('speed')
      })
    wind = []
    for node in dom.getElementsByTagNameNS(WEATHER_NS, 'wind'): 
      wind.append({ 
          'chill': node.getAttribute('chill'), 
          'direction': node.getAttribute('direction'), 
          'speed': node.getAttribute('speed')
      })    
    atmosphere = []
    for node in dom.getElementsByTagNameNS(WEATHER_NS, 'atmosphere'): 
      atmosphere.append({ 
          'humidity': node.getAttribute('humidity'), 
          'visibility': node.getAttribute('visibility'), 
          'pressure': node.getAttribute('pressure'),
          'rising': node.getAttribute('rising')
      })
    astronomy = []
    for node in dom.getElementsByTagNameNS(WEATHER_NS, 'astronomy'): 
      astronomy.append({ 
          'sunrise': node.getAttribute('sunrise'), 
          'sunset': node.getAttribute('sunset')
      })
    condition = []
    for node in dom.getElementsByTagNameNS(WEATHER_NS, 'condition'): 
      condition.append({ 
          'text': node.getAttribute('text'), 
          'code': node.getAttribute('code'),
          'temp': node.getAttribute('temp'),
          'date': node.getAttribute('date')
      })

    title = dom.getElementsByTagName('title')[0].firstChild.data

    description_2 = dom.getElementsByTagName('description')[1].firstChild
    weather_img = description_2.wholeText

    soup = BeautifulSoup(''.join(weather_img))
    logging.info('soup: %s' % str(soup))
    img_tag = soup.find('img')
    img_tag = str(img_tag)[10:-4]
    logging.info('img_tag: %s' % str(img_tag))

    StoreYahooData(forecast_one=forecasts[0], forecast_two=forecasts[1],
                   location=location[0], units=units[0], wind=wind[0], 
                   atmosphere=atmosphere[0], astronomy=astronomy[0], 
                   condition=condition[0], title=title, img_tag=img_tag)

    return { 
      'forecast_one': forecasts[0],
      'forecast_two': forecasts[1],
      'location': location,
      'units': units,
      'wind': wind,
      'atmosphere': atmosphere,
      'astronomy': astronomy,
      'condition': condition,
      'title': title,
      'img_tag': img_tag      
    }

def StoreYahooData(forecast_one, forecast_two, location, units, wind,   
                   atmosphere, astronomy, condition, title, img_tag):
  
  new_data = models.YahooWeatherForecast()

  logging.info('dir condition: %s' % str(dir(condition)))

  new_data.condition_text = condition['text']
  new_data.condition_code = condition['code']
  new_data.condition_temp = condition['temp']
  new_data.condition_date = condition['date']
  new_data.astronomy_sunrise = astronomy['sunrise']
  new_data.astronomy_sunset = astronomy['sunset']
  new_data.atmosphere_humidity = atmosphere['humidity']
  new_data.atmosphere_visibility = atmosphere['visibility']
  new_data.atmosphere_pressure = atmosphere['pressure']
  new_data.atmosphere_rising = atmosphere['rising']
  new_data.wind_chill = wind['chill']
  new_data.wind_direction = wind['direction']
  new_data.wind_speed = wind['speed']
  new_data.units_temperature = units['temperature']
  new_data.units_distance = units['distance']
  new_data.units_pressure = units['pressure']
  new_data.units_speed = units['speed']
  new_data.location_city = location['city']
  new_data.location_region = location['region']
  new_data.location_country = location['country']
  new_data.forecast_one_date = forecast_one['date']
  new_data.forecast_one_low = forecast_one['low']
  new_data.forecast_one_high = forecast_one['high']
  new_data.forecast_one_condition = forecast_one['condition']
  new_data.forecast_two_date = forecast_two['date']
  new_data.forecast_two_low = forecast_two['low']
  new_data.forecast_two_high = forecast_two['high']
  new_data.forecast_two_condition = forecast_two['condition']
  new_data.title = title
  new_data.img_tag = img_tag
  
  new_data.put()
  

