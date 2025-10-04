import logging
import time
from pathlib import Path

import click
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

logger = logging.getLogger(__name__)


class ContentChangeHandler(FileSystemEventHandler):
    """Handle file system events for content changes."""

    def __init__(self, rebuild_callback):
        self.rebuild_callback = rebuild_callback
        self.last_rebuild = 0
        self.debounce_seconds = 1  # Avoid rebuilding too frequently

    def on_any_event(self, event):
        # Ignore directory events and hidden files
        if event.is_directory or Path(event.src_path).name.startswith("."):
            return

        # Only rebuild for relevant file types
        if not any(
            event.src_path.endswith(ext)
            for ext in [".md", ".yaml", ".yml", ".html", ".css", ".js"]
        ):
            return

        # Debounce: only rebuild if enough time has passed
        current_time = time.time()
        if current_time - self.last_rebuild < self.debounce_seconds:
            return

        self.last_rebuild = current_time
        click.echo(f"\nDetected change in {event.src_path}")
        click.echo("Rebuilding site...")
        self.rebuild_callback()
        click.echo("✓ Rebuild complete\n")


def watch(rebuild_callback, paths_to_watch=None):
    """Watch specified paths for changes and trigger rebuild callback."""
    if paths_to_watch is None:
        paths_to_watch = ["content", "bakesite.yaml", "bakesite.yml"]

    event_handler = ContentChangeHandler(rebuild_callback)
    observer = Observer()

    # Watch each path that exists
    for path in paths_to_watch:
        if Path(path).exists():
            observer.schedule(event_handler, path, recursive=True)
            click.echo(f"Watching {path} for changes...")

    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        click.echo("\nStopped watching for changes.")
    observer.join()
