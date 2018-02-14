import http.server
import socketserver
import httproute
from response_codes import ResponseCodes

PORT = 8000

class HTTPServer(http.server.BaseHTTPRequestHandler):

    code_response = ResponseCodes.NOT_FOUND

    def do_GET(self):
        route = httproute.HTTPRoute(self)

        content = route.endpoint(self.path, httproute.RouteType.GET)

        if self.code_response == ResponseCodes.NOT_FOUND:
            content = ''

        self.send_response(self.code_response.value)
        self.send_header('Content-type', 'text/json')
        self.end_headers()

        body = content.encode('UTF-8', 'replace')

        self.wfile.write(body)

server = HTTPServer

with socketserver.TCPServer(("", PORT), server) as httpd:
    print("serving at port", PORT)

    #httpd.
    httpd.serve_forever()