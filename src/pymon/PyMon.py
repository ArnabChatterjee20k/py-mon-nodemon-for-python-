from .core.Command import Command
from .core.Watcher import Watcher
from .core.WatcherPath import WatcherPath
from .core.Buffer import Buffer
from .Consumer import Consumer
from .core.Inotify import InotifyEvent
import threading
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

# not using IN_CLOSE_WRITE as it is generated even after IN_MODIFY
RELOAD_EVENTS = (
    InotifyEvent.IN_MODIFY | InotifyEvent.IN_MOVED_TO | InotifyEvent.IN_CREATE
)


class PyMon:
    def __init__(self, command: str):
        self._command = Command(command)
        self._buffer = Buffer()
        self._consumer = None
        self._watcher = None
        self.running = False

    def _read_watch_streams(self):
        """
        the watcher read_events is a generator and we need to iterate every time
        so it is an abstraction over the read_events and it will get used by the thread
        """
        current_path = os.getcwd()
        logging.info(f"Starting PyMon in path: {current_path}")
        logging.info(WatcherPath(current_path).get_dirs())
        self._watcher = Watcher()
        self._watcher.add_event(RELOAD_EVENTS).add_path(
            WatcherPath(current_path)
        ).publish_to(self._buffer)
        with self._watcher as watcher:
            for file_path in watcher:
                logging.info(f"Changes at {file_path}")

    def start(self):
        if self.running:
            logging.warning("PyMon is already running!")
            return
        self.running = True
        self._consumer = Consumer(self._buffer, self._command)

        self._watcher_thread = threading.Thread(
            target=self._read_watch_streams, name="WatcherThread"
        )
        self._consumer_thread = threading.Thread(
            target=self._consumer.consume, name="ConsumerThread"
        )

        self._watcher_thread.start()
        self._consumer_thread.start()

        logging.info("PyMon started successfully.")

    def stop(self):
        if not self.running:
            logging.warning("PyMon is not running!")
            return

        logging.info("Stopping PyMon...")
        self.running = False

        # Gracefully stop watcher and consumer
        self._watcher.stop()
        self._consumer.stop()

        self._watcher_thread.join(timeout=2)
        self._consumer_thread.join(timeout=2)

        logging.info("PyMon stopped successfully.")

    def restart(self):
        self.stop()
        self.start()
