import cgi
import json
import re
from wsgiref.simple_server import make_server

from jinja2 import Environment, FileSystemLoader


class Snow:
    def __init__(self, template_folder='templates'):
        self.url_map = []
        self.env = Environment(loader=FileSystemLoader(template_folder))

    def route(self, rule, method='GET', template=None):
        def decorator(view):
            self.url_map.append((rule, method, view, template))
            return view

        return decorator

    def render_template(self, template_name, **context):
        template = self.env.get_template(template_name)
        return template.render(**context).encode('utf-8')

    def __call__(self, environ, start_response):
        body = b'Content not found'
        status = '404 Not Found'
        content_type = 'text/html'
        path = environ['PATH_INFO']
        request_method = environ['REQUEST_METHOD']

        for rule, method, view, template in self.url_map:
            if match := re.match(rule, path):
                if method != request_method:
                    continue
                view_args = match.groupdict()

                if method == 'POST':
                    view_args['form'] = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ, keep_blank_values=1)

                view_result = view(**view_args)

                if isinstance(view_result, tuple):
                    view_result, status, content_type = view_result
                else:
                    status = '200 OK'

                if template:
                    body = self.render_template(template, **view_result)
                elif isinstance(view_result, dict) and content_type == 'application/json':
                    body = json.dumps(view_result).encode('utf-8')
                else:
                    body = str(view_result).encode('utf-8')

        headers = [('Content-type', content_type)]
        start_response(status, headers)
        return [body]

    def run(self, host='0.0.0.0', port=8000):
        server = make_server(host, port, self)
        server.serve_forever()
