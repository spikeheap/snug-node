from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response

import datetime

from TempSensor import TempSensor
from RelaySensor import RelaySensor
from RelayController import RelayController

from MockTempSensor import MockTempSensor

# FIXME add to environment config rather than hard-coding only
PORT = 51251
ERRORSTATE_KEY = "errorstate"
ERRORMESSAGE_KEY = "errormessage"

sensors = [
#  MockTempSensor(),
    TempSensor(),
    RelaySensor(),
]

controllers = [
    RelayController(),
]

def index(request):
  responseHTML = "<h1>Welcome to the snug</h1>\n"
  
  responseHTML += "<h2>Sensors</h2>\n"
  responseHTML += "<ul>"
  for index in range(len(sensors)):
    responseHTML += "<li><a href=\"/read/%(index)s\">Sensor %(index)s</a></li>" % locals()
  responseHTML += "</ul>"
  
  responseHTML += "<h2>Controllers</h2>\n" 
  responseHTML += "<ul>"
  for index in range(len(controllers)):
    controllerName = controllers[index].name
    responseHTML += "<li>Controller %(controllerName)s: " % locals()
    responseHTML += "<a href=\"/switch/%(index)s/0\">OFF</a>" % locals()
    responseHTML += "&nbsp;|&nbsp;"
    responseHTML += "<a href=\"/switch/%(index)s/1\">ON</a>" % locals()
    responseHTML += "</li>"
  responseHTML += "</ul>"
  
  return Response(responseHTML)

def read_sensor(request):
    sensor = request.matchdict['sensor']
    # default empty result
    result = None
    errors = []
    
    try:
      sensor = int(sensor)
      result = sensors[sensor].read()
    except ValueError:
      errors.append({
          ERRORSTATE_KEY   : 2,
          ERRORMESSAGE_KEY : "The specified sensor ID was not formatted correctly. Use a 0-indexed integer and try again."
      })
    except IndexError:
      errors.append({
        ERRORSTATE_KEY    : 1,
        ERRORMESSAGE_KEY  : "The specified sensor does not exist"
      })

    # FIXME add the errors as an array
    return {
        "sensor": sensor,
        "timestamp": datetime.datetime.now().isoformat(' '),
        "result": result,
        "errors": errors,
    }
    
    

def issue_command(request):
    controller = request.matchdict['output']
    newState = request.matchdict['state']

    # default empty result
    result = None
    errors = []

    try:
      controller = int(controller)
      result = controllers[controller].set(newState)
    except ValueError:
      errors.append({
          ERRORSTATE_KEY   : 2,
          ERRORMESSAGE_KEY : "The specified controller ID was not formatted correctly. Use a 0-indexed integer and try again."
      })
    except IndexError:
      errors.append({
        ERRORSTATE_KEY    : 1,
        ERRORMESSAGE_KEY  : "The specified controller does not exist"
      })

    # FIXME ERROR HANDLING
    return result

if __name__ == '__main__':
    config = Configurator()

    # Read sensor 
    config.add_route('read_sensor','/read/{sensor}')
    config.add_view(read_sensor, route_name='read_sensor', renderer='json')
    
    # Read sensor 
    config.add_route('index','/')
    config.add_view(index, route_name='index')
    
    # Control output 
    config.add_route('issue_command','/switch/{output}/{state}')
    config.add_view(issue_command, route_name='issue_command', renderer='json')
     
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', PORT, app)
    server.serve_forever()
