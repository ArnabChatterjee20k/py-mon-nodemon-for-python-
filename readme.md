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

### About inotify and related system calls
* inotify_init() for creating instance of inotify. Returns a file descriptor or -1(in case of failure)

* inotify_add_watch() for adding a watcher to a pathname and an event to monitor. Event are bitmask and multiple events can be combined by pipe operator or bitwise and.
Returns an unique identifier for the watch.
-1 in case of failure

* inotify_rm_watch() removes a watch. Takes the unique identifier

* read(fd) – Block and wait for events.

* close(fd) – Cleanup resources when done.

### What makes the thing synchronous?
Synchronous read() is blocking.
When you call read() on an inotify file descriptor, the process stops and waits until an event happens.
* While waiting:
    * The process can't handle other tasks.
    * The CPU is idle or underutilized.
    * The app can become unresponsive.

### Making the whole flow event driven and async using epoll(event poll)
