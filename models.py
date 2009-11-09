from google.appengine.ext import db
from google.appengine.ext.db import polymodel


class Trainees(db.Model):
  """AppEngine data model to store users and list of associated groups."""
  creation_time = db.DateTimeProperty(auto_now_add=True)
  user = db.UserProperty(required=True)
  update_time = db.DateTimeProperty(auto_now=True)


class LogEntry(db.Model):
  """Stores all training input by user."""
  date_day = db.IntegerProperty()
  date_month = db.IntegerProperty()
  date_sel2 = db.TextProperty()
  activity = db.TextProperty()
  miles = db.FloatProperty()
  minutes = db.FloatProperty()
  notes = db.TextProperty()
  trainee = db.ReferenceProperty(Trainees)
  creation_time = db.DateTimeProperty(auto_now_add=True)
