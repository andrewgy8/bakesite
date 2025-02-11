import functools
import http.server
import logging
import socketserver

import click


logger = logging.getLogger(__name__)


DEFAULT_PORT = 8003


def serve(port=DEFAULT_PORT):
    Handler = functools.partial(
        http.server.SimpleHTTPRequestHandler, directory="./_site"
    )

    with socketserver.TCPServer(("", port), Handler) as httpd:
        click.echo(f"Serving your baked site at port http://localhost:{port}")
        httpd.serve_forever()
