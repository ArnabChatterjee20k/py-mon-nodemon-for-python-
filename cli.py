from src.PyMon import PyMon

if __name__ == "__main__":
    command = "python3 example/webserver/server.py"
    pymon = PyMon(command)

    try:
        pymon.start()
    except KeyboardInterrupt:
        pymon.stop()
