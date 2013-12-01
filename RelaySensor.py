import wiringpi2 as wiringpi 
import sys

# FIXME sensor classes should return a JSON object containing additional information, such as the sensor ID, timestamp.
# FIXME needs to be made generic so it's just a GPIO pin reader, with a wrapper so people with relays know to use it :)
class RelaySensor:
  """ A simple sensor class for the Ciseco Slice of Pi relay (http://shop.ciseco.co.uk/slice-of-relay/) """
  wiringpi.wiringPiSetupGpio()
  
  OUTPUT_MODE = 1 
  relayA = 24
  relayB = 25
  
  def read(self, relayId):
    if relayId == 'A' or relayId == 'a' or relayId == 0:
    	selectedRelay = relayA
    elif relayId == 'B' or relayId == 'b' or relayId == 1:
    	selectedRelay = relayB
    else:
      # FIXME needs to be less generic
      raise Exception("relayId argument was not valid for this sensor type. Must be one of 'A,a,0' or 'B,b,1'.)
      

  wiringpi.pinMode(selectedRelay,OUTPUT_MODE)
  
  return wiringpi.digitalRead(selectedRelay)
