import ujson
from httptools import parse_url
from cgi import parse_header
from urllib.parse import parse_qs


class RequestDict(dict):
    ## url args 解析 默认返回list

    def __init__(self, *args, **kwargs):
        self.super = super()
        self.super.__init__(*args, **kwargs)

    def get(self, name, default=None):
        """
        all you get is string
        :param name: key
        :param default: if not get
        :return: args
        """
        values = self.super.get(name)
        return values[0] if values else default

    def get_list(self, name):
        """
        get origin list value
        :param name: 
        :return: 
        """
        return self.super.get(name, None)


class Request:

    def __init__(self, body=None, header=None, method=None, version=None, url_data=None):
        self.body = body
        self.header = header
        self.url = parse_url(url_data)
        self.method = str(method,encoding="utf-8")
        self.version = version
        self.raw_rul = url_data

        self.parsed_form = None
        self.parsed_args = None
        self.parsed_json = None

    @property
    def form(self):
        if self.method == "POST":
            content_type, parameters = parse_header(self.header.get('Content-Type'))
            if content_type == "application/x-www-form-urlencoded":
                self.parsed_form = RequestDict(parse_qs(self.body))
        else:
            self.parsed_form = dict()
        return self.parsed_form

    @property
    def args(self):
        if self.url.query is None:
            return dict()
        self.parsed_args = RequestDict(parse_qs(self.url.query.decode('utf-8')))
        return self.parsed_args

    @property
    def json(self):
        if not self.parsed_json:
            try:
                self.parsed_json = ujson.load(self.body)
            except:
                pass
        return self.parsed_json

    @property
    def cookie(self):
        raw_cookie = self.header.get('Cookie', None)
        if raw_cookie is None:
            return dict()
        cookie_jar = dict()
        cookies = str(raw_cookie).split(";")
        for cookie in cookies:
            c = cookie.split('=')
            key = c[0].strip(' ')
            value = c[1].strip(' ')
            cookie_jar.update({key:value})

        return cookie_jar
