import functools
import http.server
import logging
import socketserver


logger = logging.getLogger(__name__)


PORT = 8003


def serve():
    Handler = functools.partial(
        http.server.SimpleHTTPRequestHandler, directory="./_site"
    )

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        logger.info(f"Serving at port http://localhost:{PORT}")
        httpd.serve_forever()
