import http.server
import socketserver
from .http_route import HTTPRoute, RouteType
from .response_codes import ResponseCodes

PORT = 8000

class HTTPServer(http.server.BaseHTTPRequestHandler):

    code_response = ResponseCodes.NOT_FOUND

    def request(instance, route_type):

        route = HTTPRoute(instance)

        content = route.endpoint(instance.path, route_type)
        if instance.code_response == ResponseCodes.NOT_FOUND:
            content = ''

        instance.send_response(instance.code_response.value)
        instance.send_header('Content-type', 'text/json')
        instance.end_headers()

        body = content.encode('UTF-8', 'replace')
        instance.wfile.write(body)

    def do_GET(self):
        HTTPServer.request(self, RouteType.GET)

    def do_POST(self):
        HTTPServer.request(self, RouteType.POST)

    def do_PUT(self):
        HTTPServer.request(self, RouteType.PUT)

    def do_DELETE(self):
        HTTPServer.request(self, RouteType.DELETE)
	
    def start(self, pPort = None):
        port = pPort or PORT
        with socketserver.TCPServer(("", port), self) as httpd:
            print("serving at port", port)
            
            httpd.serve_forever()
#server = HTTPServer

