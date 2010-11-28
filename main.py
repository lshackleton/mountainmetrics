#!/usr/bin/env python
"""
Mountain Metrics

We use the webapp.py WSGI framework to handle CGI requests, using the
wsgiref module to wrap the webapp.py WSGI application in a CGI-compatible
container. See webapp.py for documentation on RequestHandlers and the URL
mapping at the bottom of this module.

We use Django templates, which are described at
http://www.djangoproject.com/documentation/templates/. We define a custom
Django template filter library in templatefilters.py for use in dilbertindex
templates.
"""

__author__ = '(Bill Ferrell)'

import cgi
import datetime
import htmlentitydefs
import math
import os
import re
import sgmllib
import sys
import time
import urllib
import logging
import wsgiref.handlers
import traceback

from google.appengine.api import datastore
from google.appengine.api import datastore_types
from google.appengine.api import datastore_errors
from google.appengine.api import users
from google.appengine.api import memcache
from google.appengine.api import mail
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

from google.appengine.ext import db
from django.core.paginator import ObjectPaginator, InvalidPage

# Importing the mmlib for testing
from mmlib.scrapers.expected_snowfall import expected_snowfall_parser
from mmlib import mmutil

# Datastore models.
import models


## Set logging level.
logging.getLogger().setLevel(logging.INFO)

# Add our custom Django template filters to the built in filters
template.register_template_library('templatefilters')

# Set to true to see stack traces and template debugging information
_DEBUG = False


class BaseRequestHandler(webapp.RequestHandler):
  """The common class for all mountainmetrics requests"""

  def handle_exception(self, exception, debug_mode):
    exception_name = sys.exc_info()[0].__name__
    exception_details = str(sys.exc_info()[1])
    exception_traceback = ''.join(traceback.format_exception(*sys.exc_info()))
    logging.error(exception_traceback)
    exception_expiration = 60*60*3 # seconds 
    mail_admin = "wferrell@gmail.com" # must be an admin 
    sitename = "mountainmetrics"
    throttle_name = 'exception-'+exception_name
    throttle = memcache.get(throttle_name)
    if throttle is None:
        memcache.add(throttle_name, 1, exception_expiration)
        subject = '[%s] exception [%s: %s]' % (sitename, exception_name,
                                               exception_details)
        mail.send_mail_to_admins(sender=mail_admin,
                                 subject=subject,
                                 body=exception_traceback)

    values = {}
    template_name = 'error.html'
    if users.is_current_user_admin():
        values['traceback'] = exception_traceback
    directory = os.path.dirname(os.environ['PATH_TRANSLATED'])
    path = os.path.join(directory, os.path.join('templates', template_name))
    self.response.out.write(template.render(path, values, debug=_DEBUG))

  def generate(self, template_name, template_values={}):
    """Generates the given template values into the given template.

    Args:
        template_name: the name of the template file (e.g., 'index.html')
        template_values: a dictionary of values to expand into the template
    """

    # Populate the values common to all templates
    values = {
      'debug': self.request.get('deb'),
      'user': users.GetCurrentUser(),

    }

    values.update(template_values)
    directory = os.path.dirname(os.environ['PATH_TRANSLATED'])
    path = os.path.join(directory, os.path.join('templates', template_name))
    self.response.out.write(template.render(path, values, debug=_DEBUG))


#
# Start Webpage Handlers
#

class HomePageHandler(BaseRequestHandler):
  """  Generates the start/home page.
  """

  def get(self, garbageinput=None):
    logging.info('Visiting the homepage')

    handler = mmutil.DataPopulator()
    weather = handler.handle(type='weather')
    roads = handler.handle(type='roads')
    avalanche = handler.handle(type='avalanche')
    alpine_meadows_snow_report = handler.handle(type='alpine_meadows_snow_report')
    squaw_valley_snow_report = handler.handle(type='squaw_valley_snow_report')
    kirkwood_snow_report = handler.handle(type='kirkwood_snow_report')
    expected_snowfall = handler.handle(type='expected_snowfall')
    yahoo_weather = handler.handle(type='yahoo_weather')
    current_obs = handler.handle(type='current_obs')
    sierra_weather = handler.handle(type='sierra_weather')
    sierra_temp = handler.handle(type='sierra_temp')
    sierra_wind_direction = handler.handle(type='sierra_wind_direction')
    sierra_wind_speed = handler.handle(type='sierra_wind_speed')
    sierra_expected_snow = handler.handle(type='sierra_expected_snow')
    yesterday_data = handler.handle(type='yesterday_data')
    TemperaturePerDay = handler.handle(type='TemperaturePerDay')
    snow_fall_graph = handler.handle(type='snow_fall_graph')
    #snow_fall_graph = None
  
    avalanche_multi_levels = False  
    if avalanche.multiple_danger_levels:
      avalanche_multi_levels = True

    avalanche_status = None
    avalanche_graph_url = None
    if avalanche.extreme_danger:
      avalanche_graph_url = 'http://chart.apis.google.com/chart?cht=gom&chs=400x200&chd=t:5&chl=Extreme&chdlp=b'
      avalanche_status = 'Extreme'
    elif avalanche.high_danger:
      avalanche_graph_url = 'http://chart.apis.google.com/chart?cht=gom&chs=400x200&chd=t:10&chl=High&chdlp=b'
      avalanche_status = 'High'
    elif avalanche.considerable_danger:
      avalanche_graph_url = 'http://chart.apis.google.com/chart?cht=gom&chs=400x200&chd=t:25&chl=Considerable&chdlp=b'
      avalanche_status = 'Considerable'
    elif avalanche.moderate_danger:
      avalanche_graph_url = 'http://chart.apis.google.com/chart?cht=gom&chs=400x200&chd=t:50&chl=Moderate&chdlp=b'
      avalanche_status = 'Moderate'
    elif avalanche.low_danger:
      avalanche_graph_url = 'http://chart.apis.google.com/chart?cht=gom&chs=400x200&chd=t:90&chl=Low&chdlp=b'
      avalanche_status = 'Low'
    else:
      avalanche_status = 'No data.'


    logging.info('get_stats(): %s' % memcache.get_stats())


    self.generate('home.html', {
      'ThreeDayWeatherForecast': weather,
      'DOTi80RoadConditions': roads,
      'avalanche_multi_levels': avalanche_multi_levels,
      'avalanche_graph_url': avalanche_graph_url,
      'avalanche_paragraph': avalanche.avalanche_report_paragraph,
      'avalanche_status': avalanche_status,
      'AlpineMeadowsSnowReport': alpine_meadows_snow_report,
      'SquawValleySnowReport': squaw_valley_snow_report,
      'KirkwoodSnowReport': kirkwood_snow_report,
      'ExpectedSnowfall': expected_snowfall,
      'yahoo_weather': yahoo_weather,
      'current_obs': current_obs,
      'sierra_weather': sierra_weather,
      'sierra_temp': sierra_temp,
      'sierra_wind_direction': sierra_wind_direction,
      'sierra_wind_speed': sierra_wind_speed,
      'sierra_expected_snow': sierra_expected_snow,
      'yesterday_data': yesterday_data,
      'snow_fall_graph': snow_fall_graph,
      'TemperaturePerDay': TemperaturePerDay,
      'snow_fall_graph': snow_fall_graph,
      'tomorrow': datetime.datetime.today() + datetime.timedelta(1),
    })

class AboutPageHandler(BaseRequestHandler):
  def get(self, garbageinput=None):
    logging.info('Visiting the about page')
    self.generate('about.html', {
      #'title': 'About',
    })


class AvalanchePageHandler(BaseRequestHandler):
  """
  Generates the avalanche page.

  """
  def get(self, garbageinput=None):
    logging.info('Visiting the avalanchepage')

    handler = mmutil.DataPopulator()
    weather = handler.handle(type='weather')
    roads = handler.handle(type='roads')
    avalanche = handler.handle(type='avalanche')
    alpine_meadows_snow_report = handler.handle(type='alpine_meadows_snow_report')
    squaw_valley_snow_report = handler.handle(type='squaw_valley_snow_report')
    kirkwood_snow_report = handler.handle(type='kirkwood_snow_report')
    expected_snowfall = handler.handle(type='expected_snowfall')
    yahoo_weather = handler.handle(type='yahoo_weather')
    current_obs = handler.handle(type='current_obs')
    sierra_weather = handler.handle(type='sierra_weather')
    sierra_temp = handler.handle(type='sierra_temp')
    sierra_wind_direction = handler.handle(type='sierra_wind_direction')
    sierra_wind_speed = handler.handle(type='sierra_wind_speed')
    sierra_expected_snow = handler.handle(type='sierra_expected_snow')
    yesterday_data = handler.handle(type='yesterday_data')
    TemperaturePerDay = handler.handle(type='TemperaturePerDay')
    snow_fall_graph = handler.handle(type='snow_fall_graph')
    #snow_fall_graph = None
  
    avalanche_multi_levels = False  
    if avalanche.multiple_danger_levels:
      avalanche_multi_levels = True

    avalanche_status = None
    avalanche_graph_url = None
    if avalanche.extreme_danger:
      avalanche_graph_url = 'http://chart.apis.google.com/chart?cht=gom&chs=400x200&chd=t:5&chl=Extreme&chdlp=b'
      avalanche_status = 'Extreme'
    elif avalanche.high_danger:
      avalanche_graph_url = 'http://chart.apis.google.com/chart?cht=gom&chs=400x200&chd=t:10&chl=High&chdlp=b'
      avalanche_status = 'High'
    elif avalanche.considerable_danger:
      avalanche_graph_url = 'http://chart.apis.google.com/chart?cht=gom&chs=400x200&chd=t:25&chl=Considerable&chdlp=b'
      avalanche_status = 'Considerable'
    elif avalanche.moderate_danger:
      avalanche_graph_url = 'http://chart.apis.google.com/chart?cht=gom&chs=400x200&chd=t:50&chl=Moderate&chdlp=b'
      avalanche_status = 'Moderate'
    elif avalanche.low_danger:
      avalanche_graph_url = 'http://chart.apis.google.com/chart?cht=gom&chs=400x200&chd=t:90&chl=Low&chdlp=b'
      avalanche_status = 'Low'
    else:
      avalanche_status = 'No data.'


    logging.info('get_stats(): %s' % memcache.get_stats())


    self.generate('avalanche.html', {
      'ThreeDayWeatherForecast': weather,
      'DOTi80RoadConditions': roads,
      'avalanche_multi_levels': avalanche_multi_levels,
      'avalanche_graph_url': avalanche_graph_url,
      'avalanche_paragraph': avalanche.avalanche_report_paragraph,
      'avalanche_status': avalanche_status,
      'AlpineMeadowsSnowReport': alpine_meadows_snow_report,
      'SquawValleySnowReport': squaw_valley_snow_report,
      'KirkwoodSnowReport': kirkwood_snow_report,
      'ExpectedSnowfall': expected_snowfall,
      'yahoo_weather': yahoo_weather,
      'current_obs': current_obs,
      'sierra_weather': sierra_weather,
      'sierra_temp': sierra_temp,
      'sierra_wind_direction': sierra_wind_direction,
      'sierra_wind_speed': sierra_wind_speed,
      'sierra_expected_snow': sierra_expected_snow,
      'yesterday_data': yesterday_data,
      'snow_fall_graph': snow_fall_graph,
      'TemperaturePerDay': TemperaturePerDay,
      'snow_fall_graph': snow_fall_graph,
      'tomorrow': datetime.datetime.today() + datetime.timedelta(1),
    })


class WeatherPageHandler(BaseRequestHandler):
  """
  Generates the weather page.

  """
  def get(self, garbageinput=None):
    logging.info('Visiting the weatherpage')

    handler = mmutil.DataPopulator()
    weather = handler.handle(type='weather')
    roads = handler.handle(type='roads')
    avalanche = handler.handle(type='avalanche')
    alpine_meadows_snow_report = handler.handle(type='alpine_meadows_snow_report')
    squaw_valley_snow_report = handler.handle(type='squaw_valley_snow_report')
    kirkwood_snow_report = handler.handle(type='kirkwood_snow_report')
    expected_snowfall = handler.handle(type='expected_snowfall')
    yahoo_weather = handler.handle(type='yahoo_weather')
    current_obs = handler.handle(type='current_obs')
    sierra_weather = handler.handle(type='sierra_weather')
    sierra_temp = handler.handle(type='sierra_temp')
    sierra_wind_direction = handler.handle(type='sierra_wind_direction')
    sierra_wind_speed = handler.handle(type='sierra_wind_speed')
    sierra_expected_snow = handler.handle(type='sierra_expected_snow')
    yesterday_data = handler.handle(type='yesterday_data')
    TemperaturePerDay = handler.handle(type='TemperaturePerDay')
    snow_fall_graph = handler.handle(type='snow_fall_graph')
    #snow_fall_graph = None
  
    avalanche_multi_levels = False  
    if avalanche.multiple_danger_levels:
      avalanche_multi_levels = True

    avalanche_status = None
    avalanche_graph_url = None
    if avalanche.extreme_danger:
      avalanche_graph_url = 'http://chart.apis.google.com/chart?cht=gom&chs=400x200&chd=t:5&chl=Extreme&chdlp=b'
      avalanche_status = 'Extreme'
    elif avalanche.high_danger:
      avalanche_graph_url = 'http://chart.apis.google.com/chart?cht=gom&chs=400x200&chd=t:10&chl=High&chdlp=b'
      avalanche_status = 'High'
    elif avalanche.considerable_danger:
      avalanche_graph_url = 'http://chart.apis.google.com/chart?cht=gom&chs=400x200&chd=t:25&chl=Considerable&chdlp=b'
      avalanche_status = 'Considerable'
    elif avalanche.moderate_danger:
      avalanche_graph_url = 'http://chart.apis.google.com/chart?cht=gom&chs=400x200&chd=t:50&chl=Moderate&chdlp=b'
      avalanche_status = 'Moderate'
    elif avalanche.low_danger:
      avalanche_graph_url = 'http://chart.apis.google.com/chart?cht=gom&chs=400x200&chd=t:90&chl=Low&chdlp=b'
      avalanche_status = 'Low'
    else:
      avalanche_status = 'No data.'


    logging.info('get_stats(): %s' % memcache.get_stats())


    self.generate('weather.html', {
      'ThreeDayWeatherForecast': weather,
      'DOTi80RoadConditions': roads,
      'avalanche_multi_levels': avalanche_multi_levels,
      'avalanche_graph_url': avalanche_graph_url,
      'avalanche_paragraph': avalanche.avalanche_report_paragraph,
      'avalanche_status': avalanche_status,
      'AlpineMeadowsSnowReport': alpine_meadows_snow_report,
      'SquawValleySnowReport': squaw_valley_snow_report,
      'KirkwoodSnowReport': kirkwood_snow_report,
      'ExpectedSnowfall': expected_snowfall,
      'yahoo_weather': yahoo_weather,
      'current_obs': current_obs,
      'sierra_weather': sierra_weather,
      'sierra_temp': sierra_temp,
      'sierra_wind_direction': sierra_wind_direction,
      'sierra_wind_speed': sierra_wind_speed,
      'sierra_expected_snow': sierra_expected_snow,
      'yesterday_data': yesterday_data,
      'snow_fall_graph': snow_fall_graph,
      'TemperaturePerDay': TemperaturePerDay,
      'snow_fall_graph': snow_fall_graph,
      'tomorrow': datetime.datetime.today() + datetime.timedelta(1),
    })

class RoadsPageHandler(BaseRequestHandler):
  """
  Generates the roads page.

  """
  def get(self, garbageinput=None):
    logging.info('Visiting the roadspage')

    handler = mmutil.DataPopulator()
    weather = handler.handle(type='weather')
    roads = handler.handle(type='roads')
    avalanche = handler.handle(type='avalanche')
    alpine_meadows_snow_report = handler.handle(type='alpine_meadows_snow_report')
    squaw_valley_snow_report = handler.handle(type='squaw_valley_snow_report')
    kirkwood_snow_report = handler.handle(type='kirkwood_snow_report')
    expected_snowfall = handler.handle(type='expected_snowfall')
    yahoo_weather = handler.handle(type='yahoo_weather')
    current_obs = handler.handle(type='current_obs')
    sierra_weather = handler.handle(type='sierra_weather')
    sierra_temp = handler.handle(type='sierra_temp')
    sierra_wind_direction = handler.handle(type='sierra_wind_direction')
    sierra_wind_speed = handler.handle(type='sierra_wind_speed')
    sierra_expected_snow = handler.handle(type='sierra_expected_snow')
    yesterday_data = handler.handle(type='yesterday_data')
    TemperaturePerDay = handler.handle(type='TemperaturePerDay')
    snow_fall_graph = handler.handle(type='snow_fall_graph')
    #snow_fall_graph = None
  
    avalanche_multi_levels = False  
    if avalanche.multiple_danger_levels:
      avalanche_multi_levels = True

    avalanche_status = None
    avalanche_graph_url = None
    if avalanche.extreme_danger:
      avalanche_graph_url = 'http://chart.apis.google.com/chart?cht=gom&chs=400x200&chd=t:5&chl=Extreme&chdlp=b'
      avalanche_status = 'Extreme'
    elif avalanche.high_danger:
      avalanche_graph_url = 'http://chart.apis.google.com/chart?cht=gom&chs=400x200&chd=t:10&chl=High&chdlp=b'
      avalanche_status = 'High'
    elif avalanche.considerable_danger:
      avalanche_graph_url = 'http://chart.apis.google.com/chart?cht=gom&chs=400x200&chd=t:25&chl=Considerable&chdlp=b'
      avalanche_status = 'Considerable'
    elif avalanche.moderate_danger:
      avalanche_graph_url = 'http://chart.apis.google.com/chart?cht=gom&chs=400x200&chd=t:50&chl=Moderate&chdlp=b'
      avalanche_status = 'Moderate'
    elif avalanche.low_danger:
      avalanche_graph_url = 'http://chart.apis.google.com/chart?cht=gom&chs=400x200&chd=t:90&chl=Low&chdlp=b'
      avalanche_status = 'Low'
    else:
      avalanche_status = 'No data.'


    logging.info('get_stats(): %s' % memcache.get_stats())


    self.generate('roads.html', {
      'ThreeDayWeatherForecast': weather,
      'DOTi80RoadConditions': roads,
      'avalanche_multi_levels': avalanche_multi_levels,
      'avalanche_graph_url': avalanche_graph_url,
      'avalanche_paragraph': avalanche.avalanche_report_paragraph,
      'avalanche_status': avalanche_status,
      'AlpineMeadowsSnowReport': alpine_meadows_snow_report,
      'SquawValleySnowReport': squaw_valley_snow_report,
      'KirkwoodSnowReport': kirkwood_snow_report,
      'ExpectedSnowfall': expected_snowfall,
      'yahoo_weather': yahoo_weather,
      'current_obs': current_obs,
      'sierra_weather': sierra_weather,
      'sierra_temp': sierra_temp,
      'sierra_wind_direction': sierra_wind_direction,
      'sierra_wind_speed': sierra_wind_speed,
      'sierra_expected_snow': sierra_expected_snow,
      'yesterday_data': yesterday_data,
      'snow_fall_graph': snow_fall_graph,
      'TemperaturePerDay': TemperaturePerDay,
      'snow_fall_graph': snow_fall_graph,
      'tomorrow': datetime.datetime.today() + datetime.timedelta(1),
    })


class ResortsPageHandler(BaseRequestHandler):
  """
  Generates the resorts page.

  """
  def get(self, garbageinput=None):
    logging.info('Visiting the resortspage')

    handler = mmutil.DataPopulator()
    weather = handler.handle(type='weather')
    roads = handler.handle(type='roads')
    avalanche = handler.handle(type='avalanche')
    alpine_meadows_snow_report = handler.handle(type='alpine_meadows_snow_report')
    squaw_valley_snow_report = handler.handle(type='squaw_valley_snow_report')
    kirkwood_snow_report = handler.handle(type='kirkwood_snow_report')
    expected_snowfall = handler.handle(type='expected_snowfall')
    yahoo_weather = handler.handle(type='yahoo_weather')
    current_obs = handler.handle(type='current_obs')
    sierra_weather = handler.handle(type='sierra_weather')
    sierra_temp = handler.handle(type='sierra_temp')
    sierra_wind_direction = handler.handle(type='sierra_wind_direction')
    sierra_wind_speed = handler.handle(type='sierra_wind_speed')
    sierra_expected_snow = handler.handle(type='sierra_expected_snow')
    yesterday_data = handler.handle(type='yesterday_data')
    TemperaturePerDay = handler.handle(type='TemperaturePerDay')
    snow_fall_graph = handler.handle(type='snow_fall_graph')
    #snow_fall_graph = None
  
    avalanche_multi_levels = False  
    if avalanche.multiple_danger_levels:
      avalanche_multi_levels = True

    avalanche_status = None
    avalanche_graph_url = None
    if avalanche.extreme_danger:
      avalanche_graph_url = 'http://chart.apis.google.com/chart?cht=gom&chs=400x200&chd=t:5&chl=Extreme&chdlp=b'
      avalanche_status = 'Extreme'
    elif avalanche.high_danger:
      avalanche_graph_url = 'http://chart.apis.google.com/chart?cht=gom&chs=400x200&chd=t:10&chl=High&chdlp=b'
      avalanche_status = 'High'
    elif avalanche.considerable_danger:
      avalanche_graph_url = 'http://chart.apis.google.com/chart?cht=gom&chs=400x200&chd=t:25&chl=Considerable&chdlp=b'
      avalanche_status = 'Considerable'
    elif avalanche.moderate_danger:
      avalanche_graph_url = 'http://chart.apis.google.com/chart?cht=gom&chs=400x200&chd=t:50&chl=Moderate&chdlp=b'
      avalanche_status = 'Moderate'
    elif avalanche.low_danger:
      avalanche_graph_url = 'http://chart.apis.google.com/chart?cht=gom&chs=400x200&chd=t:90&chl=Low&chdlp=b'
      avalanche_status = 'Low'
    else:
      avalanche_status = 'No data.'


    logging.info('get_stats(): %s' % memcache.get_stats())


    self.generate('resorts.html', {
      'ThreeDayWeatherForecast': weather,
      'DOTi80RoadConditions': roads,
      'avalanche_multi_levels': avalanche_multi_levels,
      'avalanche_graph_url': avalanche_graph_url,
      'avalanche_paragraph': avalanche.avalanche_report_paragraph,
      'avalanche_status': avalanche_status,
      'AlpineMeadowsSnowReport': alpine_meadows_snow_report,
      'SquawValleySnowReport': squaw_valley_snow_report,
      'KirkwoodSnowReport': kirkwood_snow_report,
      'ExpectedSnowfall': expected_snowfall,
      'yahoo_weather': yahoo_weather,
      'current_obs': current_obs,
      'sierra_weather': sierra_weather,
      'sierra_temp': sierra_temp,
      'sierra_wind_direction': sierra_wind_direction,
      'sierra_wind_speed': sierra_wind_speed,
      'sierra_expected_snow': sierra_expected_snow,
      'yesterday_data': yesterday_data,
      'snow_fall_graph': snow_fall_graph,
      'TemperaturePerDay': TemperaturePerDay,
      'snow_fall_graph': snow_fall_graph,
      'tomorrow': datetime.datetime.today() + datetime.timedelta(1),
    })



class ErrorPageHandler(BaseRequestHandler):
  def get(self, garbageinput=None):
    logging.info('Visiting the error page')
    self.generate('error.html', {
      #'title': 'Error',
    })

class GraphsPageHandler(BaseRequestHandler):
  def get(self, garbageinput=None):
    logging.info('Visiting the graphs page')
    past_temp_data = memcache.get("past_temp_data")
    if past_temp_data is None:
      past_temp_data_query = models.YesterdaysWeather.all()
      past_temp_data_query.order('-date_time_added')
      past_temp_data = past_temp_data_query.fetch(limit=30)
      memcache.set("past_temp_data", past_temp_data,
                    time=3600)

    self.generate('graphs.html', {
      #'title': 'Graphs',
      'past_temp_data':past_temp_data,
    })

#
# End Webpage Handlers
#


#
# Start URL Map
#

# Map URLs to our RequestHandler classes above
_MountainMetrics_Urls = [
# after each URL map we list the html template that is displayed
   ('/error', ErrorPageHandler), #error.html
   ('/resorts', ResortsPageHandler), 
   ('/avalanche', AvalanchePageHandler), 
   ('/roads', RoadsPageHandler), 
   ('/weather', WeatherPageHandler), 
   ('/graphs', GraphsPageHandler), #graphs.html
   ('/about', AboutPageHandler), #about.html
   ('/.*$', HomePageHandler), #base.html
]

#
# End URL Map
#


def main():
  application = webapp.WSGIApplication(_MountainMetrics_Urls, debug=_DEBUG)
  run_wsgi_app(application)

if __name__ == '__main__':
  main()