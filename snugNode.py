from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response

import datetime

#from TempSensor import TempSensor
from MockTempSensor import MockTempSensor

# FIXME add to environment config rather than hard-coding only
PORT = 51251
ERRORSTATE_KEY = "errorstate"
ERRORMESSAGE_KEY = "errormessage"

sensors = [
    TempSensor(),
    RelaySensor(),
]

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
    #return Response('Result for %(sensor)s is %(result)s' % {"sensor": sensor, "result": result})
    
    

def issue_command(request):
    return Response('Switching %(output)s to %(state)s' % request.matchdict)

if __name__ == '__main__':
    config = Configurator()

    # Read sensor 
    config.add_route('read_sensor','/read/{sensor}')
    config.add_view(read_sensor, route_name='read_sensor', renderer='json')
    
    # Control output 
    config.add_route('issue_command','/switch/{output}/{state}')
    config.add_view(issue_command, route_name='issue_command')
     
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', PORT, app)
    server.serve_forever()
