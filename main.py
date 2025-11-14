import re
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import os

class CustomRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path

        routes = [
            (r'^/$', self.handle_index),
            (r'^/(\d+)$', self.handle_blog_post),
            (r'^/static/(.*)$', self.handle_static_files),
            (r'^/blogs/(.*)$', self.handle_static_files),
        ]

        for pattern, handler_func in routes:
            match = re.match(pattern, path)
            if match:
                return handler_func(path, parsed_url)

        return super().do_GET()

    def handle_index(self, path=None, parsed_url=None):
        self.path = '/index.html'
        return super().do_GET()

    def handle_blog_post(self, path, parsed_url):
        target_page_file = '/pages.html'

        if os.path.exists(self.translate_path(target_page_file)):
            self.path = target_page_file
            return super().do_GET()
        else:
            self.send_error(404, "Файл страниц публикаций не найден")

    def send_error(self, code: int, message: str = None):
        self.send_response(code)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        if message:
            self.wfile.write(f"<html><body><h1>{code} {message}</h1></body></html>".encode('utf-8'))

    def handle_static_files(self, path, parsed_url):
        self.path = '/' + path.lstrip('/')
        return super().do_GET()

def start_server(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Сервер ЗабГУКОНТАКТ запущен на http://localhost:{port}/')
    httpd.serve_forever()

if __name__ == "__main__":
    start_server(HTTPServer, CustomRequestHandler)