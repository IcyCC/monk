import re
from collections import namedtuple


class Route:
    def __init__(self, methods, url, handle):
        self.methods = methods
        self.url = url
        self.handle = handle


class Router:

    def __init__(self):
        self.routes = dict()

    def add(self, url, methods, handle):
        self.routes[url] = Route(methods=methods, url=url, handle=handle)

    def get(self, request):
        url = str(request.url.path, encoding='utf-8')
        return self.routes.get(url, None)

