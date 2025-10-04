import functools
import http.server
import socketserver
import threading

import click


DEFAULT_PORT = 8200  # 8 is standard, 200 is the temp for deliciousness


def serve(port=DEFAULT_PORT, watch_callback=None):
    """Start the HTTP server, optionally with a file watcher.

    Args:
        port: Port to serve on
        watch_callback: Optional callback function to run in a separate thread for watching files
    """
    Handler = functools.partial(
        http.server.SimpleHTTPRequestHandler, directory="./_site"
    )

    # Start watcher in a separate thread if provided
    if watch_callback:
        watcher_thread = threading.Thread(target=watch_callback, daemon=True)
        watcher_thread.start()

    with socketserver.TCPServer(("", port), Handler) as httpd:
        click.echo(f"Serving your baked site at http://localhost:{port}")
        httpd.serve_forever()
