import subprocess


class Command:
    def __init__(self, command: str):
        self.command = command
        self._process = None

    def run(self):
        self._terminate()
        self._process = subprocess.Popen(
            self.command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        for line in self._process.stdout:
            print(line,end="")
        
        for error in self._process.stderr:
            print(error,end="")

    
    def _terminate(self):
        if self._process:
            self._process.terminate()
            self._process.wait()