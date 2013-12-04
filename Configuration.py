import json
from pprint import pprint

class Configuration:
    """ A configuration loader for JSON. The configuration is expected to define the node entirely. """
    
    DEFAULT_CONFIG_FILE = "conf/config.json"
    
    configMap = {}
    
    def __init__(self,configFileName=DEFAULT_CONFIG_FILE):
        """ Creates the configuration object and loads the passed file. """
        configFile = open(configFileName, 'r')
        self.configMap = json.loads( configFile.read() )
        configFile.close()
        
    def getMasterConfig(self):
        return self.configMap['master']
    
    def getNodeConfig(self):
        return self.configMap['node']
        
    def getSensorsConfig(self):
        return self.configMap['sensors']
    
    def getControllersConfig(self):
        return self.configMap['controllers']
        
