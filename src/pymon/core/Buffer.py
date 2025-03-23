from queue import Queue


class Buffer:
    def __init__(self):
        self._q = Queue()

    def push(self, item):
        self._q.put(item)

    def pop(self):
        return self._q.get()

    def is_empty(self):
        return self._q.empty()
