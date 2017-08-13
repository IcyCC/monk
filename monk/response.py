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

TYPE_MAP = {
    'a': 'application/octet-stream',
    'ai': 'application/postscript',
    'aif': 'audio/x-aiff',
    'aifc': 'audio/x-aiff',
    'aiff': 'audio/x-aiff',
    'au': 'audio/basic',
    'avi': 'video/x-msvideo',
    'bat': 'text/plain',
    'bcpio': 'application/x-bcpio',
    'bin': 'application/octet-stream',
    'bmp': 'image/x-ms-bmp',
    'c': 'text/plain',
    # Duplicates :(
    'cdf': 'application/x-cdf',
    'cdf': 'application/x-netcdf',
    'cpio': 'application/x-cpio',
    'csh': 'application/x-csh',
    'css': 'text/css',
    'csv': 'text/csv',
    'dll': 'application/octet-stream',
    'doc': 'application/msword',
    'dot': 'application/msword',
    'dvi': 'application/x-dvi',
    'eml': 'message/rfc822',
    'eps': 'application/postscript',
    'etx': 'text/x-setext',
    'exe': 'application/octet-stream',
    'gif': 'image/gif',
    'gtar': 'application/x-gtar',
    'h': 'text/plain',
    'hdf': 'application/x-hdf',
    'htm': 'text/html',
    'html': 'text/html',
    'ico': 'image/vnd.microsoft.icon',
    'ief': 'image/ief',
    'jpe': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'jpg': 'image/jpeg',
    'js': 'application/javascript',
    'ksh': 'text/plain',
    'latex': 'application/x-latex',
    'm1v': 'video/mpeg',
    'm3u': 'application/vnd.apple.mpegurl',
    'm3u8': 'application/vnd.apple.mpegurl',
    'man': 'application/x-troff-man',
    'me': 'application/x-troff-me',
    'mht': 'message/rfc822',
    'mhtml': 'message/rfc822',
    'mif': 'application/x-mif',
    'mov': 'video/quicktime',
    'movie': 'video/x-sgi-movie',
    'mp2': 'audio/mpeg',
    'mp3': 'audio/mpeg',
    'mp4': 'video/mp4',
    'mpa': 'video/mpeg',
    'mpe': 'video/mpeg',
    'mpeg': 'video/mpeg',
    'mpg': 'video/mpeg',
    'ms': 'application/x-troff-ms',
    'nc': 'application/x-netcdf',
    'nws': 'message/rfc822',
    'o': 'application/octet-stream',
    'obj': 'application/octet-stream',
    'oda': 'application/oda',
    'p12': 'application/x-pkcs12',
    'p7c': 'application/pkcs7-mime',
    'pbm': 'image/x-portable-bitmap',
    'pdf': 'application/pdf',
    'pfx': 'application/x-pkcs12',
    'pgm': 'image/x-portable-graymap',
    'pl': 'text/plain',
    'png': 'image/png',
    'pnm': 'image/x-portable-anymap',
    'pot': 'application/vnd.ms-powerpoint',
    'ppa': 'application/vnd.ms-powerpoint',
    'ppm': 'image/x-portable-pixmap',
    'pps': 'application/vnd.ms-powerpoint',
    'ppt': 'application/vnd.ms-powerpoint',
    'ps': 'application/postscript',
    'pwz': 'application/vnd.ms-powerpoint',
    'py': 'text/x-python',
    'pyc': 'application/x-python-code',
    'pyo': 'application/x-python-code',
    'qt': 'video/quicktime',
    'ra': 'audio/x-pn-realaudio',
    'ram': 'application/x-pn-realaudio',
    'ras': 'image/x-cmu-raster',
    'rdf': 'application/xml',
    'rgb': 'image/x-rgb',
    'roff': 'application/x-troff',
    'rtx': 'text/richtext',
    'sgm': 'text/x-sgml',
    'sgml': 'text/x-sgml',
    'sh': 'application/x-sh',
    'shar': 'application/x-shar',
    'snd': 'audio/basic',
    'so': 'application/octet-stream',
    'src': 'application/x-wais-source',
    'sv4cpio': 'application/x-sv4cpio',
    'sv4crc': 'application/x-sv4crc',
    'svg': 'image/svg+xml',
    'swf': 'application/x-shockwave-flash',
    't': 'application/x-troff',
    'tar': 'application/x-tar',
    'tcl': 'application/x-tcl',
    'tex': 'application/x-tex',
    'texi': 'application/x-texinfo',
    'texinfo': 'application/x-texinfo',
    'tif': 'image/tiff',
    'tiff': 'image/tiff',
    'tr': 'application/x-troff',
    'tsv': 'text/tab-separated-values',
    'txt': 'text/plain',
    'ustar': 'application/x-ustar',
    'vcf': 'text/x-vcard',
    'wav': 'audio/x-wav',
    'webm': 'video/webm',
    'wiz': 'application/msword',
    'wsdl': 'application/xml',
    'xbm': 'image/x-xbitmap',
    'xlb': 'application/vnd.ms-excel',
    # Duplicates :(
    'xls': 'application/excel',
    'xls': 'application/vnd.ms-excel',
    'xml': 'text/xml',
    'xpdl': 'application/xml',
    'xpm': 'image/x-xpixmap',
    'xsl': 'application/xml',
    'xwd': 'image/x-xwindowdump',
    'zip': 'application/zip',
}


class Response:

    def __init__(self, body, version, status=200, headers=None, content_type='text/plain',body_bytes=b''):

        self.content_type = bytes(content_type, encoding="utf-8")

        self.body =body

        self.status = status
        self.headers = headers or dict()
        self.version = bytes(version or '1.1', encoding="utf-8")
        self.cookies = list()

    def output(self, keep_alive=None):

        resp = list()
        resp.append(b"HTTP/%b %d %b" % (self.version, self.status, STATUS_CODES.get(self.status, "FAIL")))
        resp.append(b"Content-Type: %b" % self.content_type)
        resp.append(b"Content-Length: %d" % len(self.body))
        resp.append(b"Cache-Control: %b" % bytes("alive" if keep_alive else "close", encoding="utf-8"))
        for cookie in self.cookies:
            resp.append(b"Set-Cookie:%b" % cookie)
        resp.append(b"")
        resp.append(b"%b" % self.body)

        return b"\r\n".join(resp)

    def add_cookie(self,**kwargs):
        for key, value in kwargs.items():
            self.cookies.append(bytes(" {}={};".format(key, value), encoding="utf-8"))


