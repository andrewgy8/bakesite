import functools
import http.server
import socketserver

import click


DEFAULT_PORT = 8200  # 8 is standard, 200 is the temp for deliciousness


def serve(port=DEFAULT_PORT):
    Handler = functools.partial(
        http.server.SimpleHTTPRequestHandler, directory="./_site"
    )

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", port), Handler) as httpd:
        click.echo(f"Serving your baked site at port http://localhost:{port}")
        httpd.serve_forever()
