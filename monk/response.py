import ujson

STATUS_CODES = {
    200: b'OK',
    400: b'Bad Request',
    401: b'Unauthorized',
    402: b'Payment Required',
    403: b'Forbidden',
    404: b'Not Found',
    405: b'Method Not Allowed',
    500: b'Internal Server Error',
    501: b'Not Implemented',
    502: b'Bad Gateway',
    503: b'Service Unavailable',
    504: b'Gateway Timeout',
}


class Response:

    def __init__(self, body, version, status=200, headers=None, content_type='text/plain',body_bytes=b''):

        self.content_type = content_type

        self.body = body

        self.status = status
        self.headers = headers or dict()
        self.version = version or 1.1

    def output(self, keep_alive):

        resp = list()
        resp.append("HTTP/{} {} {}".format(self.version, self.status, STATUS_CODES.get(self.status, "FAIL")))
        resp.append("Content-Type: {}".format(self.content_type))
        resp.append("Content-Length: {}".format(len(self.body)))
        resp.append("Cache-Control: {}".format("alive" if keep_alive else "close"))
        resp.append("")
        resp.append("{}".format(self.body))

        return "\r\n".join(resp)

