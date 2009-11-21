#!/usr/bin/env python
#
__author__ = ""

from lib.validators import Validators
from google.appengine.ext import db

class StatusValue(db.Model):
  """Model for status values in the Data Store

  This Model defines all of the data going into the datastore on app engine. It
  enforces some normalization on the data as it's stored through the choices
  attributes.
  """
  update = db.DateTimeProperty(auto_now_add=True)
  name = db.StringProperty(required=True,
                           validator=Validators.validLine)
  status = db.StringProperty(required=True,
                             validator=Validators.validStatus)
  description = db.TextProperty()
  geography = db.StringProperty(required=True,
                                validator=Validators.validGeo)
  network = db.StringProperty(required=True,
                              validator=Validators.validNetwork)
  valueType = db.StringProperty(required=True,
                                validator=Validators.validValueType)

  def getStatus(self):
    return Validators.getStatus(self.status)
