from pydoc import locate
from enum import Enum
from response_codes import ResponseCodes
from list_route import ListRoute

BACK_SLASH ='/'
PREFIX_PARAMETER = ':'

list_route = ListRoute
list_route.load_endpoints(list_route)

class RouteType(Enum):
    GET    = 'GET'
    POST   = 'POST'
    PUT    = 'PUT'
    DELETE = 'DELETE'

class HTTPRoute():
    __http_server = None
    __paramters = []

    def __init__(self, http_server):
        self.__http_server = http_server

    def math_route(self, route, endpoint):
        blocks_uri = endpoint.split(BACK_SLASH)
        blocks_route = route.split(BACK_SLASH)
        qtd_blocks = len(blocks_uri)

        if qtd_blocks != len(blocks_route):
            return False

        math = True
        for index in range(qtd_blocks):
            is_parameter  = blocks_route[index].find(PREFIX_PARAMETER) == 0
            math_resource = blocks_route[index].upper() == blocks_uri[index].upper()

            if not(is_parameter | math_resource):
                math = False
                break

        return math

    def get_endpoint(self, endpoint, route_type):
        list_routes = list_route.routes[route_type.value]
        for item in list_routes:

            if not(self.math_route(item, endpoint)):
                continue

            full_method = list_routes[item].split('.')
            method_name = full_method.pop()
            class_name = '.'.join(full_method)

            controller = locate(class_name)
            try:
                method = getattr(controller(),method_name)
            except AttributeError:
                self.__http_server.code_response = ResponseCodes.INTERNAL_SERVER_ERROR
                print(f'Error:{class_name} has not implemented method {method_name}')
                return

            #params = []

            self.__http_server.code_response = ResponseCodes.OK
            return method()