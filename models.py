from google.appengine.ext import db


class ThreeDayWeatherForecast(db.Model):
  """AppEngine data model to store 3 day weather forecast module. All data in table from NOAA"""
  date_time_added = db.DateTimeProperty(auto_now_add=True)
  noaa_observation_time = db.DateTimeProperty()
  noaa_observation_location = db.StringProperty()
  current_temp_c = db.FloatProperty()
  current_temp_f = db.FloatProperty()
  temperature_string = db.StringProperty()
  wind_string = db.StringProperty()
  wind_dir = db.StringProperty()
  wind_mph = db.FloatProperty()
  wind_gust_mph = db.FloatProperty()
  station_id = db.StringProperty()
  dewpoint_string = db.StringProperty()
  dewpoint_f = db.FloatProperty()
  dewpoint_c = db.FloatProperty()
  pressure_string = db.StringProperty()
  pressure_mb = db.FloatProperty()
  pressure_in = db.FloatProperty()
  weather = db.StringProperty()
  icon_url_base = db.StringProperty()
  icon_url_name = db.StringProperty()
  two_day_history_url = db.StringProperty()


class SquawValleySnowReport(db.Model):
  """AppEngine data model to store Squaw Valley Snow Report. All data in table from ____"""
  date_time_added = db.DateTimeProperty(auto_now_add=True)
  today_high_temp = db.FloatProperty()
  today_low_temp = db.FloatProperty()
  today_new_snow = db.FloatProperty()
  today_expected_snowfall = db.FloatProperty()
  tomorrow_high_temp = db.FloatProperty()
  tomorrow_low_temp = db.FloatProperty()
  tomorrow_expected_snowfall = db.FloatProperty()
  third_day_high_temp = db.FloatProperty()
  third_day_tomorrow_low_temp = db.FloatProperty()
  third_day_tomorrow_expected_snowfall = db.FloatProperty()


class AlpineMeadowsSnowReport(db.Model):
  """AppEngine data model to store Alpine Meadows Snow Report. All data in table from ____"""
  date_time_added = db.DateTimeProperty(auto_now_add=True)
  today_high_temp = db.FloatProperty()
  today_low_temp = db.FloatProperty()
  today_new_snow = db.FloatProperty()
  today_expected_snowfall = db.FloatProperty()
  tomorrow_high_temp = db.FloatProperty()
  tomorrow_low_temp = db.FloatProperty()
  tomorrow_expected_snowfall = db.FloatProperty()
  third_day_high_temp = db.FloatProperty()
  third_day_tomorrow_low_temp = db.FloatProperty()
  third_day_tomorrow_expected_snowfall = db.FloatProperty()


class KirkwoodSnowReport(db.Model):
  """AppEngine data model to store Kirkwood Snow Report. All data in table from ____"""
  date_time_added = db.DateTimeProperty(auto_now_add=True)
  today_high_temp = db.FloatProperty()
  today_low_temp = db.FloatProperty()
  today_new_snow = db.FloatProperty()
  today_expected_snowfall = db.FloatProperty()
  tomorrow_high_temp = db.FloatProperty()
  tomorrow_low_temp = db.FloatProperty()
  tomorrow_expected_snowfall = db.FloatProperty()
  third_day_high_temp = db.FloatProperty()
  third_day_tomorrow_low_temp = db.FloatProperty()
  third_day_tomorrow_expected_snowfall = db.FloatProperty()


class DOTi80RoadConditions(db.Model):
  """AppEngine data model to store DOT Road Conditions. All data in table from DOT website"""
  date_time_added = db.DateTimeProperty(auto_now_add=True)
  road_conditions_details = db.TextProperty()
  stretch_of_road = db.StringProperty()
  chains_required = db.BooleanProperty()


class TodaysAvalancheReport(db.Model):
  """AppEngine data model to store Todays Avalanche Report. All data in table from Sierra Avalanche Center"""
  date_time_added = db.DateTimeProperty(auto_now_add=True)
  avalanche_report_paragraph = db.TextProperty()
  avalanche_danger_rating = db.StringProperty()
  avalanche_danger_image_url = db.LinkProperty()
  

