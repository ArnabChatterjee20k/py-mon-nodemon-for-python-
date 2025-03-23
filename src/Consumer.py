from .core.Buffer import Buffer
from .core.Command import Command
from multiprocessing import Process
import psutil,time


class Consumer:
    def __init__(self, buffer: Buffer, command: Command):
        self.buffer = buffer
        self.running = False
        self.command = command
        self._process: Process = None

    def consume(self):
        self.running = True
        if not self._process or not self._process.is_alive():
            self._restart()
        while self.running:
            try:
                if not self.buffer.is_empty():
                    data = self.buffer.pop()
                    print(data)
                    self._terminate()
                    self._restart()
                time.sleep(0.1)
            except KeyboardInterrupt:
                print("closing")
                self.stop()
                break

    def stop(self):
        self._terminate()
        self.running = False

    def _restart(self):
        self._process = Process(target=self.command.run, daemon=True)
        self._process.start()

    def _terminate(self):
        """recursively close all the childs of the process and no chance of zombie processes"""
        if not self._process or not self._process.is_alive():
            return
        parent = psutil.Process(self._process.pid)
        children = parent.children(recursive=True)

        for child in children:
            child.terminate()

        parent.terminate()
        total_processes = [parent] + children
        processes_killed, processes_still_alived = psutil.wait_procs(
            total_processes, timeout=3
        )
        for process in processes_still_alived:
            process.kill()
