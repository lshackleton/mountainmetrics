#!/usr/bin/env python
__author__ = "Bill Ferrell"

"""Functions for deleting data from the datastore. 
"""

import logging
from google.appengine.ext import db
import datetime

today = datetime.date.today()
one_week_ago = today + datetime.timedelta(days=-7)

def Deletei80RoadData():
  
  logging.info('Running the Deletei80DataOneWeekAtATime.')
  q = db.GqlQuery("SELECT __key__ FROM DOTi80RoadConditions WHERE "
                  " date_time_added < :1", one_week_ago)
  results = q.fetch(50)
  db.delete(results)
  

def DeleteYesterdaysWeatherData():

  logging.info('Running the DeleteYesterdayDataOneWeekAtATime.')
  q = db.GqlQuery("SELECT __key__ FROM YesterdayWeather WHERE "
                  " date_time_added < :1", one_week_ago)
  results = q.fetch(50)
  db.delete(results)