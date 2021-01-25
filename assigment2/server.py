import http.server
import json
import re
from collections import namedtuple

from url_view import UrlView

URL_DICT = {
    re.compile('/posts/'): {
        'GET': UrlView.do_GET_json,
        'POST': UrlView.do_POST
    },
    re.compile(r'/posts/(.+)/'): {
        'GET': UrlView.do_GET,
        'PUT': UrlView.do_PUT,
        'DELETE': UrlView.do_DELETE
    }
}


def find_matches(d, item):
    for k in d.keys():
        if re.fullmatch(k, item):
            return d[k]


ResponseStatus = namedtuple("ResponseStatus",
                            ["response", "ContentType", "data"])


class MyServerHandler(http.server.BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def send_headers(self, response_status, response_content):
        self.send_response(response_status)
        self.send_header("Content-type", response_content)
        self.end_headers()

    def perform_requests(self, method, url=None, vars=None):
        try:
            func = find_matches(URL_DICT, self.path)[method]
        except KeyError:
            self.send_headers(404, 'application/json')
            return
        response = func(url=url, vars=vars)
        self.send_headers(response.response, response.ContentType)
        self.wfile.write(json.dumps(response.data).encode())

    def do_GET(self):
        return self.perform_requests('GET', url=self.path)

    def do_POST(self):
        post_vars = json.loads(self.rfile.read(int(self.headers['Content-Length'])).decode('utf-8'))
        return self.perform_requests('POST', url=self.path, vars=post_vars)

    def do_PUT(self):
        post_vars = json.loads(self.rfile.read(int(self.headers['Content-Length'])).decode('utf-8'))
        return self.perform_requests('PUT', url=self.path, vars=post_vars)

    def do_DELETE(self):
        return self.perform_requests('DELETE', url=self.path)


PORT = 8087
server_address = ('localhost', PORT)
server = http.server.HTTPServer(server_address, MyServerHandler)
server.serve_forever()
