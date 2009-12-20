#!/usr/bin/env python
__author__ = "Bill Ferrell"

"""Parses the Kirkwood Snow report page. 

Page found here: http://www.kirkwood.com/weather/default.aspx

This class parses the page and returns an object that allows you to get various status bits. 
"""

import re
import logging

import models
from mmlib.scrapers.scraper import Scraper


class KirkwoodSnowReportParser(Scraper):
  def __init__(self):
    url = 'http://www.kirkwood.com/weather/default.aspx'
    Scraper.__init__(self, url=url, geography='Tahoe', 
                     valueType='KirkwoodConditions')
    self.scrape()
    snow_conditions = self.parseSnowConditions()
    
    new_snow_report = models.KirkwoodSnowReport()

    new_snow_report.time_of_report = str(snow_conditions[0])
    new_snow_report.current_temp_f = float(snow_conditions[2][:-7])
    new_snow_report.current_condition = str(snow_conditions[1])
    new_snow_report.new_snow_total_inches = str(snow_conditions[6])
    new_snow_report.storm_snow_total_inches = str(  
      snow_conditions[6])
    new_snow_report.wind = str(snow_conditions[3])
    new_snow_report.kirkwood_forcast = str(snow_conditions[4])
    new_snow_report.is_kirkwood = True
    new_snow_report.new_snow_total_inches_base = str(snow_conditions[7])

    new_snow_report.put()


  def parseSnowConditions(self):
    dat = []
    lblDate = self.soup.find('span', attrs={'id':'lblDate'})
    time = lblDate.contents[0]
    lblSkies = self.soup.find('span', attrs={'id':"lblSkies"})
    weather_descrip = lblSkies.contents[0]
    lblTemperature = self.soup.find('span', attrs={'id':'lblTemperature'})
    temp = lblTemperature.contents[0]
    lblWind = self.soup.find('span', attrs={'id':'lblWind'})
    wind = lblWind.contents[0]
    lblForcast = self.soup.find('span', attrs={'id':'lblForcast'})
    kirkwood_forcast = lblForcast.contents[0]
    lbl24Hours = self.soup.find('span', attrs={'id':'lbl24Hours'})
    snow_24_hours = lbl24Hours.contents[0]         
    lblStormTotal = self.soup.find('span', attrs={'id':'lblStormTotal'})
    storm_total = lblStormTotal.contents[0]
    lblBaseDepth = self.soup.find('span', attrs={'id':'lblBaseDepth'})
    mid_mtn_base = lblBaseDepth.contents[0]


    dat = [time, weather_descrip, temp, wind, kirkwood_forcast, snow_24_hours,
           storm_total, mid_mtn_base]
    logging.info('[time, weather_descrip, temp, wind, kirkwood_forcast, snow_24_hours,storm_total, mid_mtn_base]')
    logging.info('dat: %s' % str(dat))

    return dat
