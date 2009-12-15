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
    lower_mtn_conditions = self.parseConditions(div_class='snowreport6200')
    upper_mtn_conditions = self.parseConditions(div_class='snowreport8200')
    
    if lower_mtn_conditions[4] == '    &':
      lower_mtn_conditions[4] = None
    if upper_mtn_conditions[4][:-1] == '    &':
      upper_mtn_conditions[4] = '0'
    else:
      upper_mtn_conditions[4] = upper_mtn_conditions[4][:-1]
    
    
    
    new_data = models.SquawValleySnowReport()

    new_data.time_of_report = str(time)
    new_data.current_temp_f = float(lower_mtn_conditions[0])
    new_data.upper_mountain_temp_f = float(upper_mtn_conditions[0])
    new_data.lower_mountain_temp_f = float(lower_mtn_conditions[0])
    new_data.upper_mountain_snow_base_inches = upper_mtn_conditions[3] 
    new_data.lower_mountain_snow_base_inches = lower_mtn_conditions[3]
    new_data.current_condition = str(lower_mtn_conditions[2])
    new_data.current_condition_top = str(upper_mtn_conditions[2])
    new_data.current_condition_base = str(lower_mtn_conditions[2])
    new_data.new_snow_total_inches = lower_mtn_conditions[4]
    new_data.new_snow_total_inches_base = lower_mtn_conditions[4]
    new_data.new_snow_total_inches_top = upper_mtn_conditions[4]
    new_data.storm_snow_total_inches = lower_mtn_conditions[5]
    new_data.storm_snow_total_inches_base = lower_mtn_conditions[5]
    new_data.storm_snow_total_inches_inches_top = (
      upper_mtn_conditions[5][:-2])
    new_data.wind = lower_mtn_conditions[1]
    new_data.wind_base = lower_mtn_conditions[1]
    new_data.wind_top = upper_mtn_conditions[1]
    new_data.is_squaw_valley = True

    new_data.put()

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

  def parseConditions(self, div_class=None):
    dat = []
    block = self.soup.find('div', attrs={'class': div_class})
    count = 0
    for tag in block:
#      print count
#      print tag

      if count == 5:
        raw_data_var = tag.contents[3]
        temp = raw_data_var.findNext('span')
        temp = temp.contents[0]
        temp = temp[:-5]
        logging.info('temp:%s' % str(temp))
        wind = str(raw_data_var)
        wind = wind[82:-6]
#        print wind
        logging.info('wind:%s' % str(wind))
        dat.append(temp)
        dat.append(wind)

      if count == 7:
        current_conditions = tag.find('p', attrs={'class': 'snowreport-item'})
        current_conditions = current_conditions.contents[0]
        current_conditions = current_conditions[4:-2]
        logging.info('current_conditions:%s' % str(current_conditions))        
        dat.append(current_conditions)

      if count == 9:
        raw_data_var = tag
        base_snow = raw_data_var.findAll('span')
        base_snow = base_snow[1]
        base_snow = base_snow.contents[0]
        base_snow = base_snow[:-6]
        logging.info('base_snow:%s' % str(base_snow))

        new_snow = str(raw_data_var)
        new_snow = new_snow[214:-21]
        logging.info('new_snow:%s' % str(new_snow))        
        
        dat.append(base_snow)
        dat.append(new_snow)

      if count == 11:
        storm_total = tag.find('p', attrs={'class': 'snowreport-item'})
        storm_total = storm_total.contents[0]
        storm_total = storm_total[6:-7]
        logging.info('storm_total:%s' % str(storm_total))
        dat.append(storm_total)
      count += 1
#    print dat
    logging.info('dat: %s' % str(dat))
    return dat
