from .core.Buffer import Buffer
from .core.Command import Command
class Consumer:
    def __init__(self,buffer:Buffer,command:Command):
        self.buffer = buffer
        self.running = False
        self.command = command
    def consume(self):
        self.running = True
        while self.running:
            try:
                if not self.buffer.is_empty():
                    data = self.buffer.pop()
                    print(data)
                    self.command.run()
            except KeyboardInterrupt:
                print("closing")
                break

    def stop(self):
        self.running = False