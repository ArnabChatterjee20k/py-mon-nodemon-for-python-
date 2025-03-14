class Command:
    def __init__(self,command:str):
        self.command = command

    def run(self, command: str):
        print(command)