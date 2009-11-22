#!/usr/bin/env python
#
# Copyright 2008 Allen Hutchison (allen@hutchison.org)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# $URL: http://severedelays.googlecode.com/svn/trunk/appengine/lib/validators.py $
__version__ = "$Rev: 69 $"
__author__ = "Allen Hutchison (allen@hutchison.org)"

class Validators():
  """A set of validators to be shared by all data classes.

  These validators should be used by any class that deals with the data in the 
  datastore. They will ensure consistency between the classes dealing with this
  data. To use a validator set "validator=Validators.validLine" for example in
  your data model. See StatusValue in lib.status_values.py for an example.
  """
  # All allowable lines in our current datastore should be defined here.
  validLines = ['jubilee',
                'bakerloo',
                'central',
                'metropolitan',
                'district',
                'piccadilly',
                'hammersmithandcity',
                'victoria',
                'circle',
                'northern',
                'waterlooandcity',
                'dlr',
                'overground']
  
  # This dictionary contains all of the possible status values for a given
  # line and it's real language translation.
  validStatusValues = {'goodservice': 'Good Service',
                       'minordelays': 'Minor Delays',
                       'severedelays': 'Severe Delays',
                       'partsuspended': 'Part Suspended',
                       'suspended': 'Suspended',
                       'partclosure': 'Part Closure',
                       'plannedclosure': 'Planned Closure',
                       'information' : 'Information'}
  
  # This list contains all of the valid geograpies in our current app.
  validGeos = ['UK-LON']
  
  #This list contains all of the valid networks in our current app.
  validNetworks = ['underground', 'overground']
  
  # This list contains all of our valid value types in our current app. Line
  # should be used for anything that moves, stations for anything that it 
  # arrives at.
  validValueTypes = ['line', 'station']
  
  @staticmethod
  def getStatus(status):
    """Get the storage value for the current human readable status or get the
    current human readable status for the current storage value."""
    for x in Validators.validStatusValues:
      if (x == status):
        return Validators.validStatusValues[x]
      if (Validators.validStatusValues[x] == status):
        return x
  
  @staticmethod
  def validate(item, validList):
    """Validate an item in the given list.
    
    Raises: ValidatorError if the item isn't found.
    """
    if item not in validList:
      raise ValidatorError("%s is not in list %s" % (item, validList))
    else:
      return
  
  @staticmethod
  def validLine(line):
    Validators.validate(line, Validators.validLines)
  
  @staticmethod
  def validStatus(status):
    Validators.validate(status, Validators.validStatusValues.keys())
  
  @staticmethod
  def validGeo(geo):
    Validators.validate(geo, Validators.validGeos)
  
  @staticmethod
  def validNetwork(network):
    Validators.validate(network, Validators.validNetworks)
  
  @staticmethod
  def validValueType(valueType):
    Validators.validate(valueType, Validators.validValueTypes)
    
class ValidatorError(Exception):
  """Exception raised if one of the validators failes."""
  def __init__(self, message):
    self.message = message
  def __str__(self):
    return repr(self.message)
  