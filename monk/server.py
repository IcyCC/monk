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
                 connections={}, request_timeout=60, request_max_size=None):
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
        loop = asyncio.get_event_loop()
        loop.stop()

    def data_received(self, data):
        if self.parser is None:
            self.headers = []
            self.parser = httptools.HttpRequestParser(self)
        try:
            self.parser.feed_data(data)
        finally:
            pass

    def on_header(self, name, value):
        self.headers.append((name.decode(), value.decode('uft-8')))

    def on_body(self, body):
        self.body = body

    def on_url(self, url):
        self.url = url

    def on_message_complete(self):
        self.request = Request(body=self.body, header=dict(self.headers),
                               method=self.parser.get_method(), version=self.parser.get_http_version(),
                               url_data=self.url)

        self.loop.create_tast(self.request_handler(self.request_handler,self.we))




