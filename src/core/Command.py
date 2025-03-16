import subprocess


class Command:
    def __init__(self, command: str):
        self.command = command
        self._process:subprocess.Popen = None

    def run(self):
        self._terminate()
        self._process = subprocess.Popen(
            self.command,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            shell=True,
            text=True,
        )
        try:
            for line in self._process.stdout:
                print(line,end="")
            
            for line in self._process.stderr:
                print(line,end="")
        except KeyboardInterrupt as e:
            self._terminate()
        

    def _terminate(self):
        if self._process:
            self._process.terminate()
            try:
                self._process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self._process.kill()
                self._process.wait()
