import asyncio
import aiohttp
import httptools
import signal
from inspect import isawaitable
from monk.request import Request

class Signal:
    stopped = False

class HttpProtocol(asyncio.Protocol):

    def __init__(self, loop, request_handler, signal=Signal(),
                 connections=None, request_timeout=60, request_max_size=None):
        if connections is None:
            connections = dict()
        self.loop = loop
        self.transport = None
        self.request = None
        self.body = None
        self.parser = None
        self.url = None
        self.headers = None
        self.signal = signal
        self.connections = connections
        self.request_handler = request_handler
        self.request_timeout = request_timeout
        self._total_request_size = 0
        self._timeout_handler = None

    # Connection

    def connection_made(self, transport):
        self.connections[self] = True
        self.transport = transport

    def connection_lost(self, exc):
        del self.connections[self]

    def data_received(self, data):
        if self.parser is None:
            self.headers = []
            self.parser = httptools.HttpRequestParser(self)
        try:
            self.parser.feed_data(data)
        finally:
            pass

    def on_header(self, name, value):
        self.headers.append((name.decode(), value.decode('utf-8')))

    def on_body(self, body):
        self.body = body

    def on_url(self, url):
        self.url = url

    def on_message_complete(self):
        self.request = Request(body=self.body, header=dict(self.headers),
                               method=self.parser.get_method(), version=self.parser.get_http_version(),
                               url_data=self.url)

        self.loop.create_task(self.request_handler(self.request, self.write_response))

    def write_response(self, response):
        data = response.output()
        self.transport.write(data)
        self.transport.close()


def server(request_handler, host, port):
    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)

    server_coroutine = loop.create_server(lambda: HttpProtocol(loop=loop,
                                                               request_handler=request_handler),host=host,port=port)
    print("Start Run at host {} port {} ".format(host,port))
    http_server = loop.run_until_complete(server_coroutine)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    http_server.close()
    loop.run_until_complete(http_server.wait_closed())
    loop.close()


