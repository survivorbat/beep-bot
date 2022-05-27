import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        self.send_response(200)
        return


def start_health():
    server = HTTPServer(('0.0.0.0', int(os.environ.get('PORT') or '8000')), Handler)
    threading.Thread(target=server.serve_forever).start()
