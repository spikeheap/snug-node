import json
from pprint import pprint

from Sensors.MockTempSensor import MockTempSensor
from Sensors.MockRelaySensor import MockRelaySensor

class Configuration:
  """ A configuration loader for JSON. The configuration is expected to define the node entirely. """
  
  DEFAULT_CONFIG_FILE = "conf/config.json"
  
  configMap = {}
  
  def __init__(self,configFileName=DEFAULT_CONFIG_FILE):
    """ Creates the configuration object and loads the passed file. """
    # FIXME abstract out the JSON loader
    configFile = open(configFileName, 'r')
    self.configMap = json.loads( configFile.read() )
    configFile.close()
      
  def getMasterConfig(self):
    return self.configMap['master']
  
  def getNodeConfig(self):
    return self.configMap['node']
      
  def getSensors(self):
    sensors = []
    for sensor in self.configMap['sensors']:
      sensorType = sensor.get('type')
      sensorName = sensor.get('name')
      sensorLoc = sensor.get('location')
      sensorDesc = sensor.get('notes')
      
      # FIXME make this more sensible
      if(sensorType == "MockRelaySensor"):
        sensors.append( MockRelaySensor(sensorName, sensorDesc, sensorLoc) )
      elif(sensorType == "MockTempSensor"):
        sensors.append( MockTempSensor(sensorName, sensorDesc, sensorLoc) )
      elif(sensorType == "TempSensor"):
        # FIXME add i2c address
        sensors.append( TempSensor(sensorName, sensorDesc, sensorLoc) )
      elif(sensorType == "RelaySensor"):
        # FIXME add pin number
        sensors.append( RelaySensor(sensorName, sensorDesc, sensorLoc) )
          
    return sensors         
  
  def getControllersConfig(self):
    # FIXME - fix up like the Sensors config
    return self.configMap['controllers']
      