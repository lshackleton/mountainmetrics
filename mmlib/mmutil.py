#!/usr/bin/env python
__author__ = "Bill Ferrell"

"""Util functions. 
"""

import logging


def SnowfallGraphMaker(data):
  """ This function takes in all the snow data, processes it and returns an img 
      url.
  """
  head = """<img src="http://chart.apis.google.com/chart?chs=400x200&amp;chdlp=b&amp;chf=bg,s,ffffff|c,s,ffffff&amp;chxt=x,y&amp;"""
  x_axis = """"""
  y_axis = """"""
  spacer = """&amp;cht=lc&amp;chd=t:"""
  daily_snowfall_8_9k = """|"""
  daily_snowfall_7_8k = """&amp;"""
  closer = """chdl=7,000+-+8,000+ft|8,000+-+9,000+ft&amp;chco=0000ff,009900&amp;chls=2,1,0|2,3,3" />"""

  complete = (head + x_axis + y_axis + spacer + daily_snowfall_8_9k + 
              daily_snowfall_7_8k + closer)

  return complete
