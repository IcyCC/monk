import asyncio
from monk.request import Request
from monk.response import Response
from inspect import isawaitable
from monk.router import Router
from monk.server import server
import ujson

class Monk:

    def __init__(self, router=None):
        self.router = router or Router()
        self.config = dict()


    def route(self, url, methods=None):
        def decorator(func):
            self.router.add(url=url, methods=methods, handle=func)
            return func
        return decorator

    async def handle_request(self, request, write_response):
        handle = self.router.get(request=request)
        if handle is None:
            return None
        response = handle(request)

        if isawaitable(response):
            resp = await response

        write_response(resp)

    @staticmethod
    def jsonfy(**kwargs):
        body = ujson.dumps(kwargs)
        resp = Response(body=body, version=1.1, content_type="application/json")
        return resp

    @staticmethod
    def html(body):
        resp = Response(body, version=1.1, content_type="text/html")
        return resp

    @staticmethod
    def abort_404():
        resp = Response(body='', version=1.1, status=404)
        return resp

    @staticmethod
    def is_static(request):
        """
        return is request static or not
        :param request: 
        :return: 
        """
        url = str(request.url.path)
        if url.startswith('/static/'):
            return True
        else:
            return False

    def run(self, host="127.0.0.1", port=5000):
        self.router.add("/favicon.ico", handle=favicon, methods=None)
        server(host=host, port=port, request_handler=self.handle_request)

async def favicon(request):
    return Response(body='', version=1.1, status=200)




