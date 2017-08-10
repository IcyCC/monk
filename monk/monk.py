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
        handle = self.router.get(request=request).handle

        response = handle(request)

        if isawaitable(response):
            response = await response

        write_response(response)

    @staticmethod
    async def jsonfy(**kwargs):
        body = ujson.dumps(kwargs)
        resp = Response(body=body,version=1.1, content_type="application/json")
        return resp


    def run(self, host = "127.0.0.1", port=5000):


        server(host=host, port=port,request_handler=self.handle_request)






