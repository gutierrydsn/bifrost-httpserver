import json

class ListRoute():
    routes = []

    def load_endpoints(self):
        file_route = open('routes','r')

        try:
            self.routes = json.loads(file_route.read())
        except ValueError:
            print("Error: file route invalid formated!")
            raise

        file_route.close()