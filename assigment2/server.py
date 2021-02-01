import http.server
import json
import re
from collections import namedtuple

import url_view

URL_DICT = {
    re.compile('/posts/'): {
        'GET': url_view.get_data,
        'POST': url_view.add_post
    },
    re.compile(r'/posts/(.+)/'): {
        'GET': url_view.get_post,
        'PUT': url_view.update_post,
        'DELETE': url_view.remove_post
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

    def perform_requests(self, method, url=None, args=None):
        try:
            func = find_matches(URL_DICT, self.path)[method]
        except KeyError:
            self.send_headers(404, 'application/json')
            return
        response = func(url=url, args=args)
        self.send_headers(response.response, response.ContentType)
        self.wfile.write(json.dumps(response.data).encode())

    def do_GET(self):
        return self.perform_requests('GET', url=self.path)

    def do_POST(self):
        post_args = json.loads(self.rfile.read(int(self.headers['Content-Length'])).decode('utf-8'))
        return self.perform_requests('POST', url=self.path, args=post_args)

    def do_PUT(self):
        post_args = json.loads(self.rfile.read(int(self.headers['Content-Length'])).decode('utf-8'))
        return self.perform_requests('PUT', url=self.path, args=post_args)

    def do_DELETE(self):
        return self.perform_requests('DELETE', url=self.path)


PORT = 8087
server_address = ('localhost', PORT)
server = http.server.HTTPServer(server_address, MyServerHandler)
server.serve_forever()