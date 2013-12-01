from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response

from TempSensor import TempSensor


# FIXME add to environment config rather than hard-coding only
PORT = 51251

sensors = [
    TempSensor()
]

def read_sensor(request):
    result = sensors[sensor].read()
    return Response('Result for %(sensor)s is %(result)s' % request.matchdict)
    
def issue_command(request):
    return Response('Switching %(output)s to %(state)s' % request.matchdict)

if __name__ == '__main__':
    config = Configurator()

    # Read sensor 
    config.add_route('read_sensor','/read/{sensor}')
    config.add_view(read_sensor, route_name='read_sensor')
    
    # Control output 
    config.add_route('issue_command','/switch/{output}/{state}')
    config.add_view(issue_command, route_name='issue_command')
     
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', PORT, app)
    server.serve_forever()