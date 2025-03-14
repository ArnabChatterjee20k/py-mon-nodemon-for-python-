from src.Inotify import *
from src.WatcherPath import WatcherPath
from src.Watcher import Watcher
import subprocess


# fd = inotify_init()

# wd = inotify_add_watch(fd,b".",InotifyEvent.IN_ALL_EVENTS)

# import os
# while True:
#     data = os.read(fd,EVENT_BUFFER_SIZE)
#     for event in InotifyEvent.parse_event(data):
#         print(event)

path1 = WatcherPath("/home/arnab/Desktop/system-implementations/py-mon/example/")

j = 0
# for i in p.get_all_files():
#     if j == 8:
#         break
#     print(i)
#     j+=1
event = InotifyEvent.IN_CLOSE_WRITE | InotifyEvent.IN_CREATE | InotifyEvent.IN_MODIFY
watcher = Watcher().add(path1).on(event)
with watcher as data:
    for event in data:
        print(event)
