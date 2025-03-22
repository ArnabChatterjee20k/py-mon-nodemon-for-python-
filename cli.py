from src.PyMon import PyMon

if __name__ == "__main__":
    command = "python3 example/test.py"
    pymon = PyMon(command)

    try:
        pymon.start()
    except KeyboardInterrupt:
        pymon.stop()
