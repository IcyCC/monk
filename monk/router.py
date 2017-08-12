import re
from collections import namedtuple
from monk.log import log


class Route:
    def __init__(self, url, handle, methods=None):
        if methods is None:
            methods = ['GET','POST','DELETE','CONNECT']
        self.methods = methods
        self.url = url
        self.handle = handle


class Router:

    def __init__(self):
        self.routes = dict()

    def add(self, url, methods, handle):
        self.routes[url] = Route(methods=methods, url=url, handle=handle)

    def get(self, request):
        try:
            url = str(request.url.path, encoding='utf-8')
            route = self.routes.get(url, None)
            if request.method not in route.methods:
                log.error("NOT support method {} ".format(request.method))
                return None
        finally:
            return route.handle

