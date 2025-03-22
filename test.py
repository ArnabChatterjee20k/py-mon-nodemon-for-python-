# from src.core.Inotify import *
# from src.WatcherPath import WatcherPath
# from src.Watcher import Watcher
# import subprocess


# # fd = inotify_init()

# # wd = inotify_add_watch(fd,b".",InotifyEvent.IN_ALL_EVENTS)

# # import os
# # while True:
# #     data = os.read(fd,EVENT_BUFFER_SIZE)
# #     for event in InotifyEvent.parse_event(data):
# #         print(event)

# path1 = WatcherPath("/home/arnab/Desktop/system-implementations/py-mon/example/")

# j = 0
# # for i in p.get_all_files():
# #     if j == 8:
# #         break
# #     print(i)
# #     j+=1
from src.core.Inotify import InotifyEvent

RELOAD_EVENTS = (
    InotifyEvent.IN_MODIFY
    | InotifyEvent.IN_CLOSE_WRITE
    | InotifyEvent.IN_MOVED_TO
    | InotifyEvent.IN_CREATE
)
# watcher = Watcher().add(path1).on(RELOAD_EVENTS)
# # with watcher as data:
# #     for event in data:
# #         print(event)

# # print(path1.get_dirs())
# from src.core.Command import Command
# command = Command("python3 example/test.py")
# for data in watcher.read_events():
#     if data:
#         command.run()


from src.core.WatcherPath import WatcherPath

core_path = WatcherPath(
    "/home/arnab/Desktop/system-implementations/py-mon/src/core", ignore=[]
)
test_path = WatcherPath(
    "/home/arnab/Desktop/system-implementations/py-mon/example", ignore=[]
)
from src.core.Command import Command
from src.core.Watcher import Watcher

watcher = Watcher().add_path(core_path, test_path).add_event(RELOAD_EVENTS)
command = Command("python3 example/hellow.py")
print(watcher._wd_path_map)
from src.core.Buffer import Buffer

buffer = Buffer()
watcher.publish_to(buffer)
try:
    with watcher as watch_events:
        for file_path, event in watch_events:
            if file_path:
                # may produce duplicate events
                # Debouncing at the consuemr level
                command.run()
except Exception as e:
    print(e)
    print("exception")



