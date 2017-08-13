import asyncio
from monk.request import Request
from monk.response import Response,TYPE_MAP
from inspect import isawaitable
from monk.router import Router
from monk.server import server
from monk.static import read_file
from monk.config import Config
from monk.log import log
import ujson
import os



class Monk:

    def __init__(self, router=None):
        self.router = router or Router()
        self.config = Config()

    def route(self, url, methods=None):
        def decorator(func):
            self.router.add(url=url, methods=methods, handle=func)
            return func
        return decorator

    async def handle_request(self, request, write_response):
        if self.is_static(request) is True:
            path = self.config.static_path+str(request.url.path, encoding="utf-8")
            path = os.path.abspath(path)
            log.info("Static file read path {} ".format(path))
            context = await read_file(path)
            file_type = str(request.url.path,encoding="utf-8").split('.')[-1]
            resp = Response(body=context, version='1.1',
                            content_type=TYPE_MAP.get(file_type, "text/plain"))
            write_response(resp)

        handle = self.router.get(request=request)
        if handle is None:
            write_response(self.abort_404("Not found method"))
            return

        response = handle(request)

        if isawaitable(response):
            resp = await response

        write_response(resp)

    @staticmethod
    def jsonfy(**kwargs):
        body = ujson.dumps(kwargs)
        resp = Response(body=bytes(body,encoding="utf-8"), version='1.1', content_type="application/json")
        return resp

    @staticmethod
    def html(body):
        resp = Response(bytes(body, encoding="utf-8"), version='1.1', content_type="text/html")
        return resp

    @staticmethod
    def abort_404(body="Not found"):
        resp = Response(body=bytes(body, encoding="utf-8"), version='1.1', status=404)
        return resp

    @staticmethod
    def is_static(request):
        """
        return is request static or not
        :param request: 
        :return: 
        """
        url = str(request.url.path, encoding="utf-8").split('/')[-1]

        if '.' in url:
            return True
        else:
            return False

    def run(self, host="127.0.0.1", port=5000):
        server(host=host, port=port, request_handler=self.handle_request)




