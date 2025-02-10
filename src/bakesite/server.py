import functools
import http.server
import logging
import socketserver


logger = logging.getLogger(__name__)


PORT = 8003


def serve(port=PORT):
    Handler = functools.partial(
        http.server.SimpleHTTPRequestHandler, directory="./_site"
    )

    with socketserver.TCPServer(("", port), Handler) as httpd:
        logger.info(f"Serving at port http://localhost:{port}")
        httpd.serve_forever()
