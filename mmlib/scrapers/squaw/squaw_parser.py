#!/usr/bin/env python
__author__ = "Bill Ferrell"

"""Parses the Squaw Valley Snow report page. 

Page found here: http://www.squaw.com/winter/mtnreport.html

This class parses the page and returns an object that allows you to get various status bits. 
"""

import re
import logging

import models
from mmlib.scrapers.scraper import Scraper


class SquawSnowReportParser(Scraper):
  def __init__(self):
    url = 'http://www.squaw.com/winter/mtnreport.html'
    Scraper.__init__(self, url=url, geography='Tahoe', 
                     valueType='SquawConditions')
    self.scrape()
    time = self.parseTimeLastUpdate()
    snow_conditions = self.parseSnowConditions()

    temp = float(snow_conditions[10][36:-12])
    lower_mountain_temp_f = float(snow_conditions[1][36:-12])
    upper_mountain_temp_f = float(snow_conditions[10][36:-12])

    current_condition = snow_conditions[12][4:]
    current_condition_top = snow_conditions[12][4:]
    current_condition_base = snow_conditions[3][4:]

    upper_m_snowbase = snow_conditions[14][36:-13]
    lower_m_snowbase = snow_conditions[5][36:-13]

    # Squaw does not provide the following data
    #twentyfour_total_in = 
    #twentyfour_total_in_base = 
    #twentyfour_total_in_top = 
    
    #new_snow_total_inches = 
    #new_snow_total_inches_base = 
    #new_snow_total_inches_top =        

    wind = snow_conditions[11][4:-4]
    wind_base = snow_conditions[2][4:-4]
    wind_top = snow_conditions[11][4:-4]
    
    new_snow_report = models.SquawValleySnowReport()

    new_snow_report.time_of_report = str(time)
    new_snow_report.current_temp_f = temp
    new_snow_report.upper_mountain_temp_f = upper_mountain_temp_f
    new_snow_report.lower_mountain_temp_f = lower_mountain_temp_f
    new_snow_report.squaw_upper_mountain_snow_base_inches = upper_m_snowbase 
    new_snow_report.squaw_lower_mountain_snow_base_inches = lower_m_snowbase
    new_snow_report.current_condition = str(current_condition)
    new_snow_report.current_condition_top = str(current_condition_top)
    new_snow_report.current_condition_base = str(current_condition_base)
# Commented out because Squaw does not provide this data
#    new_snow_report.new_snow_total_inches = new_snow_total_inches
#    new_snow_report.new_snow_total_inches_base = new_snow_total_inches_base
#    new_snow_report.new_snow_total_inches_top = new_snow_total_inches_top
#    new_snow_report.twentyfour_hour_snow_total_inches = twentyfour_total_in
#    new_snow_report.twentyfour_hour_snow_total_inches_base = twentyfour_total_in_base
#    new_snow_report.twentyfour_hour_snow_total_inches_top = twentyfour_total_in_top
#    new_snow_report.twentyfour_hour_snow_total_inches = twentyfour_total_in

    new_snow_report.wind = wind
    new_snow_report.wind_base = wind_base
    new_snow_report.wind_top = wind_top
    new_snow_report.is_squaw_valley = True

    new_snow_report.put()


  def parseTimeLastUpdate(self):
    time = None
    block = self.soup.find(attrs={'id':"snow-report"})
    span = block.findNext('span')
    time = span.contents[0]
    logging.info('time: %s' % str(time))
    if not time:
      time = ''
      logging.info('Failing to find data.')
    return time

  def parseSnowConditions(self):
    dat = []
    block = self.soup.findAll('p', attrs={'class': 'snowreport-item'})
    for tag in block:
#      print tag.attrs
#      print tag.contents
      dat += map(str, tag.contents)
#    print dat [1]
    logging.info('dat: %s' % str(dat))
    return dat