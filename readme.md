### Py-mon
what's your favourite pokemon? Mine is "Greninja".

### TODO
[] inotify event bitmaks
[] inotify event structures
[] parsing event from the structure and event_buffer
 
[] init inotify
[] close inotify
[] add watch
[] add watch to dir => watch every files
[] reading all registered events => queue
[] run the registered command

### Watcher API design plan
```py
class Watcher:
    def __init__(self):
        pass
watcher = Watcher()

class Events:
    CREATE = "create"
    DELETE = "delete"
    MODIFY = "modify"
    MOVE = "move"

class Path:
    pass

class Command:
    pass

observer = watcher.add(Path(),Path()).ignore(Path()).on(Events.CREATE).run(Command)
status_code = observer.observe()
```

### CLI tool plan
```bash
py-mon "python3 app.py"

py-mon "fastapi dev --port 8000"
```

### Resources
* Watchdog python (src/watchdog/observers/inotify_c.py)
* https://gist.github.com/quiver/3609972#file-inotify_test-py-L62
* https://developer.ibm.com/tutorials/l-ubuntu-inotify/