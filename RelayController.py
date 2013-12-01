import datetime
import wiringpi2 as wiringpi 
import sys

class RelayController:
  """ A simple sensor class for the Ciseco Slice of Pi relay (http://shop.ciseco.co.uk/slice-of-relay/) """
  
  
  name = "Relay Control: Slice of Relay: A"
  on  = 1
  off = 0
  OUTPUT_MODE = 1 
  relayA = 24
  relayB = 25

  wiringpi.wiringPiSetupGpio()

  # FIXME this should be a metaprogrammed setup - many sensor instances for a single slice of pi
  def set(self,newState):
    
    # FIXME need to catch error
    print "Switching relay " + relayA + " to " + ` int(stateArg)`

    if int(stateArg) == 1:
    	relayValue = 1
    else:
    	relayValue = 0 
    
    OUTPUT = 1
    wiringpi.pinMode(relayA,self.OUTPUT_MODE)
    
    initialState = wiringpi.digitalRead(relayA)
    wiringpi.digitalWrite(relayA,newState)
    currentState = wiringpi.digitalRead(relayA)
    
    result = None
    if(initialState == currentState):
    	result = "Target state was already set. No action taken"
    else:
    	result = "Switched"
    
    errors = None
    
    return {
        "controller": self.name,
        "timestamp": datetime.datetime.now().isoformat(' '),
        "result": result,
        "errors": errors,
    }
