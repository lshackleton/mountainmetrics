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
  visibility_mi = db.FloatProperty()
  relative_humidity = db.FloatProperty()

class DewpointPerDay(db.Model):
  """ Data model to hold the dewpoint for the previous day. Each entry is for
      the previous day given date_time_added value.
  """
  date_time_added = db.DateTimeProperty(auto_now_add=True)
  dewpoint_f_high = db.FloatProperty()
  dewpoint_f_low = db.FloatProperty()
  dewpoint_c_high = db.FloatProperty()
  dewpoint_c_low = db.FloatProperty()


class TemperaturePerDay(db.Model):
  """ Data model to hold the temperature for the previous day. Each entry is for
      the previous day given date_time_added value.
  """
  date_time_added = db.DateTimeProperty(auto_now_add=True)
  current_temp_c_high = db.FloatProperty()
  current_temp_c_low = db.FloatProperty()
  current_temp_f_high = db.FloatProperty()
  current_temp_f_low = db.FloatProperty()


class ResortSnowReportBase(db.Model):
  date_time_added = db.DateTimeProperty(auto_now_add=True)
  time_of_report = db.StringProperty(multiline=True)
  current_temp_f = db.FloatProperty()
  current_temp_c = db.FloatProperty()
  upper_mountain_temp_f = db.FloatProperty()
  upper_mountain_temp_c = db.FloatProperty()
  lower_mountain_temp_f = db.FloatProperty()
  lower_mountain_temp_c = db.FloatProperty()
  upper_mountain_snow_base_inches = db.StringProperty(multiline=True)
  lower_mountain_snow_base_inches = db.StringProperty(multiline=True)
  current_condition = db.StringProperty(multiline=True)
  current_condition_top = db.StringProperty(multiline=True)
  current_condition_base = db.StringProperty(multiline=True)
  new_snow_total_inches = db.StringProperty(multiline=True)
  new_snow_total_inches_base = db.StringProperty(multiline=True)
  new_snow_total_inches_top = db.StringProperty(multiline=True)
  storm_snow_total_inches = db.StringProperty(multiline=True)
  storm_snow_total_inches_base = db.StringProperty(multiline=True)
  storm_snow_total_inches_top = db.StringProperty(multiline=True)
  wind = db.StringProperty(multiline=True)
  wind_base = db.StringProperty(multiline=True)
  wind_top = db.StringProperty(multiline=True)
  

class SquawValleySnowReport(ResortSnowReportBase):
  """AppEngine data model to store Squaw Valley Snow Report."""
  is_squaw_valley = db.BooleanProperty()


class AlpineMeadowsSnowReport(ResortSnowReportBase):
  """AppEngine data model to store Alpine Meadows Snow Report."""
  is_alpine_meadows = db.BooleanProperty()


class KirkwoodSnowReport(ResortSnowReportBase):
  """AppEngine data model to store Kirkwood Snow Report."""
  is_kirkwood = db.BooleanProperty()
  kirkwood_forcast = db.StringProperty(multiline=True)


class YesterdayWeather(db.Model):
  """AppEngine data model to store Yesterday's weather information."""
  date_time_added = db.DateTimeProperty(auto_now_add=True)


class YahooWeatherForecast(db.Model):
  """AppEngine data model to store Yahoo's weather information."""
  date_time_added = db.DateTimeProperty(auto_now_add=True)
  condition_text = db.StringProperty(multiline=True)
  condition_code = db.StringProperty(multiline=True)
  condition_temp = db.StringProperty(multiline=True)
  condition_date = db.StringProperty(multiline=True)
  astronomy_sunrise = db.StringProperty(multiline=True)
  astronomy_sunset = db.StringProperty(multiline=True)
  atmosphere_humidity = db.StringProperty(multiline=True)
  atmosphere_visibility = db.StringProperty(multiline=True)
  atmosphere_pressure = db.StringProperty(multiline=True)
  atmosphere_rising = db.StringProperty(multiline=True)
  wind_chill = db.StringProperty(multiline=True)
  wind_direction = db.StringProperty(multiline=True)
  wind_speed = db.StringProperty(multiline=True)
  units_temperature = db.StringProperty(multiline=True)
  units_distance = db.StringProperty(multiline=True)
  units_pressure = db.StringProperty(multiline=True)
  units_speed = db.StringProperty(multiline=True)
  location_city = db.StringProperty(multiline=True)
  location_region = db.StringProperty(multiline=True)
  location_country = db.StringProperty(multiline=True)
  forecast_one_date = db.StringProperty(multiline=True)
  forecast_one_low = db.StringProperty(multiline=True)
  forecast_one_high = db.StringProperty(multiline=True)
  forecast_one_condition = db.StringProperty(multiline=True)
  forecast_two_date = db.StringProperty(multiline=True)
  forecast_two_low = db.StringProperty(multiline=True)
  forecast_two_high = db.StringProperty(multiline=True)
  forecast_two_condition = db.StringProperty(multiline=True)
  title = db.StringProperty(multiline=True)
  img_tag = db.StringProperty(multiline=True)


class DOTi80RoadConditions(db.Model):
  """AppEngine data model to store DOT Road Conditions. All data in table from DOT website"""
  date_time_added = db.DateTimeProperty(auto_now_add=True)
  road_conditions_details = db.TextProperty()
  stretch_of_road = db.StringProperty()
  chains_required = db.BooleanProperty()
  road_closed = db.BooleanProperty()  


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


class ExpectedSnowfall(db.Model):
  """AppEngine data model to store Expected Snowfall data. The data is from   
     Sierra Avalanche Center
  """
  date_time_added = db.DateTimeProperty(auto_now_add=True)
  today = db.StringProperty(multiline=True)
  tonight = db.StringProperty(multiline=True)
  tomorrow = db.StringProperty(multiline=True)


class YesterdaysWeather(db.Model):
  """ Data model to hold yesterday's weather. 
  """
  date_time_added = db.DateTimeProperty(auto_now_add=True)
  noaa_observation_location = db.StringProperty()
  temp_c_high = db.FloatProperty()
  temp_c_low = db.FloatProperty()
  temp_f_high = db.FloatProperty()
  temp_f_low = db.FloatProperty()
  wind_mph_high = db.FloatProperty()
  wind_mph_low = db.FloatProperty()
  wind_gust_mph_high = db.FloatProperty()
  wind_gust_mph_low = db.FloatProperty()
  station_id = db.StringProperty()
  dewpoint_f_high = db.FloatProperty()
  dewpoint_f_low = db.FloatProperty()
  dewpoint_c_high = db.FloatProperty()
  dewpoint_c_low = db.FloatProperty()
  pressure_mb_high = db.FloatProperty()
  pressure_mb_low = db.FloatProperty()
  pressure_in_high = db.FloatProperty()
  pressure_in_low = db.FloatProperty()
  weather = db.StringProperty()
  icon_url_base = db.StringProperty()
  icon_url_name = db.StringProperty()
  visibility_mi_high = db.FloatProperty()
  visibility_mi_low = db.FloatProperty()
  relative_humidity_high = db.FloatProperty()
  relative_humidity_low = db.FloatProperty()

