from .Inotify import (
    inotify_init,
    inotify_add_watch,
    inotify_rm_watch,
    InotifyEvent,
    InotifyEventStructure,
    EVENT_BUFFER_SIZE,
)
import os, select
from .WatcherPath import WatcherPath
from .Command import Command
from .Buffer import Buffer


class Watcher:
    def __init__(self):
        self._inotify_fd = inotify_init()
        self._buffer = Buffer()
        self.paths: list[WatcherPath] = []
        self.path_wd_map = {}
        self.event = None

    def __enter__(self):
        self._event_generator = self.read_events()
        return self._event_generator

    def __exit__(self):
        return

    def add(self, *paths: WatcherPath):
        self.paths.extend(paths)
        return self

    def on(self, event: InotifyEvent):
        self.event = event
        for path in self.paths:
            self._add_watch(path)
        return self

    def on_path(self, path, event):
        """Map path to events"""
        pass

    def _add_watch(self, dir: WatcherPath):
        dirs = dir.get_dirs()
        for path in dirs:
            byte_path = str(path).encode()
            wd = inotify_add_watch(self._inotify_fd, byte_path, self.event)
            if wd == -1:
                raise Exception("Not able to add watcher")
            self.path_wd_map[wd] = path

    def read_events(self):
        while True:
            data = os.read(self._inotify_fd, EVENT_BUFFER_SIZE)
            for event in InotifyEvent.parse_event(data):
                # IN_ACCESS_EVENT = event.mask & InotifyEvent.IN_ACCESS or event.len == 0
                # print(f"Raw event: mask={event.mask}, name={event.name}")
                if event.mask & self.event:
                    # print(f"Triggering command, event- {event.mask & self.event}")
                    yield event
                else:
                    print(f"Filtered out event with mask: {event.mask}")

    def _remove_watch(self):
        pass

    def _close_watch(self):
        pass
