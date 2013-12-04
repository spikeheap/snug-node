from random import randrange

from Sensor import Sensor

class MockRelaySensor(Sensor):
  """ A dummy temperature sensor for testing purposes"""
  
  def read(self):
    min = 10
    max = 20
    return randrange(min, max)
