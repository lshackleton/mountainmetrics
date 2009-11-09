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
import random

from google.appengine.api import datastore
from google.appengine.api import datastore_types
from google.appengine.api import datastore_errors
from google.appengine.api import users
from google.appengine.api import memcache
from google.appengine.api import mail
from google.appengine.ext import webapp
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import login_required
from google.appengine.ext import search
from google.appengine.ext import bulkload
from google.appengine.ext import db
from django.core.paginator import ObjectPaginator, InvalidPage


# Datastore models.
import models


# GLOBAL CONSTANTS
RESULTS_PER_PAGE = 50


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
    exception_expiration = 600 # seconds 
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
      'login_url': users.CreateLoginURL(self.request.uri),
      'logout_url': users.CreateLogoutURL(self.request.uri),

    }

    values.update(template_values)
    directory = os.path.dirname(os.environ['PATH_TRANSLATED'])
    path = os.path.join(directory, os.path.join('templates', template_name))
    self.response.out.write(template.render(path, values, debug=_DEBUG))


#
# Start Action Handlers
#


class InputNewEntry(BaseRequestHandler):
  """ Inputs new data into the data model.
  """
  def post(self):
    user = users.get_current_user()
    if user:
      logging.info('User ==  %s' % str(user))
      logging.info('Fetching user')
      trainee = models.Trainees.gql("WHERE user = :1", user).get()
      logging.info('trainee = %s ' % trainee)
      if not trainee:
        trainee = models.Trainees(user=user)
        trainee.put()
        logging.info('Created user: %s.' % str(user))        
      logging.info('Inputting Data')
      date_day = int(cgi.escape(self.request.get('date_day')))
      date_month = int(cgi.escape(self.request.get('date_month')))
      date_sel2 = cgi.escape(self.request.get('date_sel2'))
      activity = cgi.escape(self.request.get('activity'))
      miles = float(cgi.escape(self.request.get('miles')))
      minutes = float(cgi.escape(self.request.get('minutes')))
      notes = cgi.escape(self.request.get('notes'))

      new_entry = models.LogEntry(trainee=trainee,
                                  date_day=date_day,
                                  date_month=date_month,
                                  date_sel2=date_sel2,
                                  activity=activity,
                                  miles=miles,
                                  minutes=minutes,
                                  notes=notes
                                 )
      new_entry.put()
      self.redirect('/enter')
    else:
      self.redirect(users.create_login_url('/enter'))


#
# End Action Handlers
#

#
# Start Helper Functions
#

def Paging(page=None):
  """ Classes handles page variables in case of erronious page input.
  """
  if not page:
    page = 0
    logging.info('Page variable is None? page: %s ' % page)
  try:
    page = int(page)
  except ValueError:
    logging.error('ERROR: Page value is not an int. Page = %s' % page)
    page = 0

  logging.info('Results page number: %s.' % page)
  return page

#
# End Helper Functions
#

#
# Start Webpage Handlers
#

class MainPage(BaseRequestHandler):
  """ Generates the all Logs page.
  """
  def get(self):
    logging.info('Visiting the homepage')

    self.generate('base.html', {
      'title': 'Train - Home',
    })

class ShowResults(BaseRequestHandler):
  """ Generates the results page.
  """
  def get(self):
    logging.info('Visiting the all entries results.html page')
    user = users.get_current_user()
    if user:
      logging.info('User ==  %s' % str(user))
   
      logging.info('Page variable: %s' % self.request.get('page'))
      resultspage = Paging(page=self.request.get('page'))

      query = models.LogEntry.all()
      query.filter('trainee =', user)
      query.order('-creation_time')

      paginator = ObjectPaginator(query, RESULTS_PER_PAGE)
      logging.info('Paginator.pages: %s.' % paginator.pages)
      if resultspage >= paginator.pages:
        logging.info('resultspage: %s. paginator.pages %s' %
                     (resultspage, paginator.pages))
        resultspage = paginator.pages - 1

      self.generate('results.html', {
        'entries': paginator.get_page(resultspage),
        'resultspages' : range(0, paginator.pages),
        'resultspage' : resultspage,
        'nickname': user.nickname,
      })
    else:
      self.redirect(users.create_login_url('/results'))


class EnterLogPage(BaseRequestHandler):
  """ Displays page allowing users to submit entries.
  """
  def get(self):
    logging.info('Visiting the myframps.html page')
    user = users.get_current_user()
    logging.info('User ==  %s' % str(user))
    if user:
      logging.info('Visiting the enter page')
      self.generate('enter.html', {
      })
    else:
      self.redirect(users.create_login_url('/enter'))

class HomePageHandler(BaseRequestHandler):
  """  Generates the start/home page.
  """

  def get(self, garbageinput=None):
    logging.info('Visiting the homepage')

    self.generate('home.html', {
    })

#
# End Webpage Handlers
#



#
# Start URL Map
#

# Map URLs to our RequestHandler classes above
_TRAINAUCTION_URLS = [
# after each URL map we list the html template that is displayed
   ('/enter', EnterLogPage), #enter.html
   ('/results', ShowResults), #results.html
   ('/home', HomePageHandler), #home.html
   ('/.*$', MainPage), #base.html
]


#
# End URL Map
#


def main():
  application = webapp.WSGIApplication(_TRAINAUCTION_URLS, debug=_DEBUG)
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
