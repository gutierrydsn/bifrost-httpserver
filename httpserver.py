import http.server
import socketserver
import httproute
from response_codes import ResponseCodes

PORT = 8000

class HTTPServer(http.server.BaseHTTPRequestHandler):

    code_response = ResponseCodes.NOT_FOUND

    def request(instance, route_type):

        route = httproute.HTTPRoute(instance)

        content = route.endpoint(instance.path, route_type)
        if instance.code_response == ResponseCodes.NOT_FOUND:
            content = ''

        instance.send_response(instance.code_response.value)
        instance.send_header('Content-type', 'text/json')
        instance.end_headers()

        body = content.encode('UTF-8', 'replace')
        instance.wfile.write(body)

    def do_GET(self):
        HTTPServer.request(self, httproute.RouteType.GET)

    def do_POST(self):
        HTTPServer.request(self, httproute.RouteType.POST)

    def do_PUT(self):
        HTTPServer.request(self, httproute.RouteType.PUT)

    def do_DELETE(self):
        HTTPServer.request(self, httproute.RouteType.DELETE)

server = HTTPServer

with socketserver.TCPServer(("", PORT), server) as httpd:
    print("serving at port", PORT)

    #httpd.
    httpd.serve_forever()