from pydoc import locate
from enum import Enum
from .response_codes import ResponseCodes
from .list_route import ListRoute

BACK_SLASH ='/'
PREFIX_PARAMETER = ':'
EMPTY_STR = ''
POINT_STR = '.'
START_PARAM = '('
END_PARAM = ')'
PARTING = ','


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

    def remove_backslash(self, str):
        array_str = list(str);
        if array_str[0] == BACK_SLASH:
            array_str.pop(0)

        if array_str[len(array_str)-1] == BACK_SLASH:
            array_str.pop()

        return EMPTY_STR.join(array_str)

    def math_route(self, blocks_uri, blocks_route):

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

    def get_args_list_of_route(self, blocks_route, blocks_uri):

        params = {}
        for i in range(len(blocks_route)):
            if blocks_route[i].find(PREFIX_PARAMETER) == 0:
                key = blocks_route[i].replace(PREFIX_PARAMETER, EMPTY_STR).strip()
                params[key] = blocks_uri[i].strip()

        return params

    def get_method_unless_params(self, method_name):
        pos_start_param = method_name.find(START_PARAM)
        if pos_start_param >= 0:
            return method_name[0:pos_start_param].strip()

        return method_name[0:len(method_name)]

    def get_params(self, method_name):
        params = []

        pos_start_param = method_name.find(START_PARAM)
        pos_end_param = method_name.find(END_PARAM)
        if pos_start_param == -1:
            return params

        if pos_end_param == -1:
            raise Exception('expected )')

        params = method_name[pos_start_param+1:pos_end_param].split(PARTING)

        return params

    def get_endpoint(self, endpoint, route_type):
        blocks_uri = self.remove_backslash(endpoint).split(BACK_SLASH)
        list_routes = list_route.routes[route_type.value]

        data_route = None
        for item in list_routes:
            blocks_route = self.remove_backslash(item).split(BACK_SLASH)

            math = self.math_route(blocks_uri, blocks_route)
            if not(math):
                continue

            full_method = list_routes[item].split(POINT_STR)
            method = full_method.pop()

            args = self.get_args_list_of_route(blocks_route, blocks_uri)
            params = self.get_params(method)

            data_route = {}
            data_route['route']  = item
            data_route['method'] = self.get_method_unless_params(method)
            data_route['class'] = POINT_STR.join(full_method)
            data_route['params'] = params
            data_route['args'] = args

        self.__http_server.code_response = ResponseCodes.OK
        return data_route

    def call_method(self, data_route):
        controller = locate(data_route['class'])
        try:
            method = getattr(controller(),data_route['method'])
        except AttributeError:
            self.__http_server.code_response = ResponseCodes.INTERNAL_SERVER_ERROR
            raise  Exception(f"Error:{data_route['class']} has not implemented route {data_route['method']}")
            return EMPTY_STR

        list_params = data_route['params']
        list_args = data_route['args']

        args = []
        for param in list_params:
            param = param.strip()
            try:
                arg = list_args[param]
            except KeyError:
                raise Exception(f'param "{param}" not found for method {data_route["route"]}')

            args.append(arg)

        self.__http_server.code_response = ResponseCodes.OK
        return method(*args)


    def endpoint(self, endpoint, route_type):
        data_route = self.get_endpoint(endpoint, route_type)

        if data_route != None:
            return self.call_method(data_route)
        else:
            self.__http_server.code_response = ResponseCodes.NOT_FOUND
            return EMPTY_STR