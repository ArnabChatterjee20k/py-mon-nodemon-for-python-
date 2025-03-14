from queue import Queue


class Buffer:
    def __init__(self, size=128):
        # thread safe queue
        self._queue = Queue(size)

    def push(self):
        return

    def pop(self):
        return
