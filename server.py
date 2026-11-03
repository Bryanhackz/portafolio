"""Servidor WSGI con threading. Sirve la app y los estáticos de frontend/."""

import sys
from socketserver import ThreadingMixIn
from wsgiref.simple_server import WSGIServer, WSGIRequestHandler, make_server

import config
from router import app


class ThreadedWSGIServer(ThreadingMixIn, WSGIServer):
    daemon_threads = True
    allow_reuse_address = True


class QuietHandler(WSGIRequestHandler):
    def log_message(self, fmt, *args):
        sys.stderr.write("[%s] %s\n" % (self.log_date_time_string(), fmt % args))


def main() -> None:
    httpd = make_server(
        config.HOST,
        config.PORT,
        app,
        server_class=ThreadedWSGIServer,
        handler_class=QuietHandler,
    )
    print(f"Servidor escuchando en http://{config.HOST}:{config.PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()


if __name__ == "__main__":
    main()