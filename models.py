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


class ResortSnowReportBase(db.Model):
  date_time_added = db.DateTimeProperty(auto_now_add=True)
  time_of_report = db.StringProperty(multiline=True)
  current_temp_f = db.FloatProperty()
  current_temp_c = db.FloatProperty()
  upper_mountain_temp_f = db.FloatProperty()
  upper_mountain_temp_c = db.FloatProperty()
  lower_mountain_temp_f = db.FloatProperty()
  lower_mountain_temp_c = db.FloatProperty()
  upper_mountain_snow_base_cm = db.FloatProperty()
  upper_mountain_snow_base_inches = db.FloatProperty()
  lower_mountain_snow_base_cm = db.FloatProperty()
  lower_mountain_snow_base_inches = db.FloatProperty()
  current_condition = db.StringProperty(multiline=True)
  current_condition_top = db.StringProperty(multiline=True)
  current_condition_base = db.StringProperty(multiline=True)
  new_snow_total_inches = db.FloatProperty()
  new_snow_total_inches_base = db.FloatProperty()
  new_snow_total_inches_top = db.FloatProperty()
  new_snow_total_cm = db.FloatProperty()
  new_snow_total_cm_base = db.FloatProperty()
  new_snow_total_cm_top = db.FloatProperty()
  twentyfour_hour_snow_total_inches = db.FloatProperty()
  twentyfour_hour_snow_total_inches_base = db.FloatProperty()
  twentyfour_hour_snow_total_inches_top = db.FloatProperty()
  twentyfour_hour_snow_total_cm = db.FloatProperty() 
  twentyfour_hour_snow_total_cm_base = db.FloatProperty() 
  twentyfour_hour_snow_total_cm_top = db.FloatProperty() 
  wind = db.StringProperty(multiline=True)
  wind_base = db.StringProperty(multiline=True)
  wind_top = db.StringProperty(multiline=True)
  

class SquawValleySnowReport(ResortSnowReportBase):
  """AppEngine data model to store Squaw Valley Snow Report."""
  is_squaw_valley = db.BooleanProperty()
  squaw_lower_mountain_snow_base_inches = db.StringProperty(multiline=True)
  squaw_upper_mountain_snow_base_inches = db.StringProperty(multiline=True)

class AlpineMeadowsSnowReport(ResortSnowReportBase):
  """AppEngine data model to store Alpine Meadows Snow Report."""
  is_alpine_meadows = db.BooleanProperty()

class KirkwoodSnowReport(ResortSnowReportBase):
  """AppEngine data model to store Kirkwood Snow Report."""
  is_kirkwood = db.BooleanProperty()
  kirkwood_forcast = db.StringProperty(multiline=True)
  kirkwood_mid_mountain_snow_base = db.StringProperty(multiline=True)
  kirkwood_24_hour_snow_total_inches = db.StringProperty(multiline=True)
  kirkwood_new_snow_total_inches = db.StringProperty(multiline=True)


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
  low_danger = db.BooleanProperty()
  moderate_danger = db.BooleanProperty()
  considerable_danger = db.BooleanProperty()
  high_danger = db.BooleanProperty()
  extreme_danger = db.BooleanProperty()
  multiple_danger_levels = db.BooleanProperty()  


class SevenDayWeatherForecast(db.Model):
  """AppEngine data model to hold the seven day forecast."""
  date_time_added = db.DateTimeProperty(auto_now_add=True)
  time_of_report = db.StringProperty(multiline=True)
  #TODO: Fill this out when we have a forecast provider.
