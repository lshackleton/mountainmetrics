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

# Datastore models.
import models


## Set logging level.
logging.getLogger().setLevel(logging.INFO)

# Add our custom Django template filters to the built in filters
template.register_template_library('templatefilters')

# Set to true to see stack traces and template debugging information
_DEBUG = True


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
    
    weather = memcache.get("weather")
    if weather is None:
      weather_query = models.ThreeDayWeatherForecast.all()
      weather_query.order('-date_time_added')
      weather = weather_query.get()
      memcache.set("weather", weather, time=3600)

    roads = memcache.get("roads")
    if roads is None:
      road_query = models.DOTi80RoadConditions.all()
      road_query.order('-date_time_added')
      roads = road_query.get()
      memcache.set("roads", roads, time=3600)

    avalanche = memcache.get("avalanche")
    if avalanche is None:
      avalanche_query = models.TodaysAvalancheReport.all()
      avalanche_query.order('-date_time_added')
      avalanche = avalanche_query.get()
      memcache.set("avalanche", avalanche, time=3600)
    
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

    alpine_meadows_snow_report = memcache.get("alpine_meadows_snow_report")
    if alpine_meadows_snow_report is None:
      alpine_meadows_snow_report_query = models.AlpineMeadowsSnowReport.all()
      alpine_meadows_snow_report_query.order('-date_time_added')
      alpine_meadows_snow_report = alpine_meadows_snow_report_query.get()
      memcache.set("alpine_meadows_snow_report", alpine_meadows_snow_report,
                   time=3600)

    squaw_valley_snow_report = memcache.get("squaw_valley_snow_report")
    if squaw_valley_snow_report is None:
      squaw_valley_snow_report_query = models.SquawValleySnowReport.all()
      squaw_valley_snow_report_query.order('-date_time_added')
      squaw_valley_snow_report = squaw_valley_snow_report_query.get()
      memcache.set("squaw_valley_snow_report", squaw_valley_snow_report,
                   time=3600)

    kirkwood_snow_report = memcache.get("kirkwood_snow_report")
    if kirkwood_snow_report is None:
      kirkwood_snow_report_query = models.KirkwoodSnowReport.all()
      kirkwood_snow_report_query.order('-date_time_added')
      kirkwood_snow_report = kirkwood_snow_report_query.get()
      memcache.set("kirkwood_snow_report", kirkwood_snow_report,
                   time=3600)

    expected_snowfall = memcache.get("expected_snowfall")
    if expected_snowfall is None:
      expected_snowfall_query = models.ExpectedSnowfall.all()
      expected_snowfall_query.order('-date_time_added')
      expected_snowfall = expected_snowfall_query.get()
      logging.info('expected_snowfall: %s' % str(expected_snowfall))
      memcache.set("expected_snowfall", expected_snowfall,
                   time=3600)


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
      'yesterday': datetime.datetime.today() - datetime.timedelta(1),
      'tomorrow': datetime.datetime.today() + datetime.timedelta(1),
      'dayaftertomorrow': datetime.datetime.today() + datetime.timedelta(2),      
    })


class Bill(BaseRequestHandler):
  def get(self, garbageinput=None):
    logging.info('Visiting the bill page')
    expected_snowfall_parser.ExpectedSnowFallParser()
    logging.info('Success for the bill page')


class AboutPageHandler(BaseRequestHandler):
  def get(self, garbageinput=None):
    logging.info('Visiting the about page')
    self.generate('about.html', {
      #'title': 'About',
    })

class ErrorPageHandler(BaseRequestHandler):
  def get(self, garbageinput=None):
    logging.info('Visiting the about page')
    self.generate('error.html', {
      #'title': 'About',
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
   ('/bill', Bill), #base.html
   ('/error', ErrorPageHandler), #about.html
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