from .Inotify import (
    InotifyEvent,
    InotifyEventData,
    inotify_add_watch,
    inotify_init,
    inotify_rm_watch,
    EVENT_BUFFER_SIZE,
)
from .WatcherPath import WatcherPath
from .Buffer import Buffer
import os
import errno


class Watcher:
    def __init__(self):
        self.paths: list[WatcherPath] = []
        self.buffer = None
        self._inoitfy_fd = inotify_init()
        self._wd_path_map = {}
        self.watch_event = InotifyEvent.IN_ALL_EVENTS
        self.running = True

    def __enter__(self):
        event_gen = self.read_events()
        return event_gen

    def __exit__(self, *args):
        if self._wd_path_map:
            self._remove_watch()

    def add_path(self, *paths: WatcherPath):
        self.paths.extend(paths)
        self._add_watch()
        return self

    def add_event(self, *events: InotifyEvent):
        self._add_event(events)
        return self

    def publish_to(self, buffer: Buffer):
        self.buffer = buffer
        # self._add_event(events)
        return self

    def read_events(self):
        # TODO: make it epoll instead of read
        while self.running:
            try:
                events_stream = os.read(self._inoitfy_fd, EVENT_BUFFER_SIZE)
                for wd, mask, cookie, length, name in InotifyEvent.parse_event(
                    events_stream
                ):
                    if (self.watch_event & mask) and length and name:
                        path = self._wd_path_map[wd]
                        path += "" if path.endswith("/") else "/"
                        event_file_source = path + name.decode()
                        if self.buffer:
                            print("pushing")
                            self.buffer.push((event_file_source, mask))
                        yield event_file_source, mask
            except KeyboardInterrupt:
                print("Closing....")
                self._remove_watch()
                self.stop()
                break

    def _add_watch(self):
        self._wd_path_map.clear()
        for path in self.paths:
            for dir_path in path.get_dirs():
                wd = inotify_add_watch(
                    self._inoitfy_fd, dir_path.encode(), self.watch_event
                )
                if wd == -1:
                    raise Exception("Failed adding watcher to the path ", dir_path)
                self._wd_path_map[wd] = dir_path

    def _add_event(self, events: list[InotifyEvent]):
        mask = events[0]
        for event in events[1:]:
            mask |= event
        self.watch_event = mask

    def stop(self):
        self.running = False

    def _remove_watch(self):
        for wd in list(self._wd_path_map):
            status = inotify_rm_watch(self._inoitfy_fd, wd)
            if status == -1:
                raise OSError(
                    errno.errorcode[os.errno],
                    f"Failed to remove watcher on {self._wd_path_map[wd]}",
                )
        self._wd_path_map.clear()
        os.close(self._inoitfy_fd)
