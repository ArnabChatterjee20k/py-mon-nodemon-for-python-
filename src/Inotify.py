import ctypes, struct, collections
from ctypes import c_int, c_char_p, c_uint32, CFUNCTYPE, CDLL
import ctypes.util
from functools import reduce

InotifyEventData = collections.namedtuple(
    "InotifyEvent", ["wd", "mask", "cookie", "len", "name"]
)


class InotifyEventStructure(ctypes.Structure):
    """
    Total Size = 16bytes + variable size name(padded by kernel to multiple of 4bytes)
    Structure representation of the inotify_event structure
    (used in buffer size calculations)::
        struct inotify_event {
            __s32 wd;            /* watch descriptor -> 4bytes*/
            __u32 mask;          /* watch mask -> 4bytes*/
            __u32 cookie;        /* cookie to synchronize two events -> 4bytes*/
            __u32 len;           /* length (including nulls) of name -> 4bytes*/
            char  name[0];       /* stub for possible name -> variable sized */
        };
    """

    _fields_ = (
        ("wd", c_int),
        ("mask", c_uint32),
        ("cookie", c_uint32),
        ("len", c_uint32),
        ("name", c_char_p),
    )


class InotifyEvent:
    # User-space events
    IN_ACCESS = 0x00000001  # File was accessed.
    IN_MODIFY = 0x00000002  # File was modified.
    IN_ATTRIB = 0x00000004  # Meta-data changed.
    IN_CLOSE_WRITE = 0x00000008  # Writable file was closed.
    IN_CLOSE_NOWRITE = 0x00000010  # Unwritable file closed.
    IN_OPEN = 0x00000020  # File was opened.
    IN_MOVED_FROM = 0x00000040  # File was moved from X.
    IN_MOVED_TO = 0x00000080  # File was moved to Y.
    IN_CREATE = 0x00000100  # Subfile was created.
    IN_DELETE = 0x00000200  # Subfile was deleted.
    IN_DELETE_SELF = 0x00000400  # Self was deleted.
    IN_MOVE_SELF = 0x00000800  # Self was moved.

    # All user-space events.
    IN_ALL_EVENTS = reduce(
        lambda x, y: x | y,
        [
            IN_ACCESS,
            IN_MODIFY,
            IN_ATTRIB,
            IN_CLOSE_WRITE,
            IN_CLOSE_NOWRITE,
            IN_OPEN,
            IN_MOVED_FROM,
            IN_MOVED_TO,
            IN_DELETE,
            IN_CREATE,
            IN_DELETE_SELF,
            IN_MOVE_SELF,
        ],
    )

    @classmethod
    def parse_event(cls, binary_data):
        # since binary data we can't use decode
        # so need to use struct unpacking
        # we need to unpack a c-level event struct which contains int, char,etc
        FORMAT = "iIII"
        i = 0
        min_event_size = 16
        while i + min_event_size <= len(binary_data):
            wd, mask, cookie, length = struct.unpack_from(FORMAT, binary_data, i)
            name_offset = i + min_event_size
            name_end = i + min_event_size + length
            name = binary_data[name_offset:name_end].rstrip(b"\0")
            i += min_event_size + length
            yield InotifyEventData(
                wd=wd, mask=mask, cookie=cookie, name=name, len=length
            )


# in bytes
EVENT_SIZE = ctypes.sizeof(InotifyEventStructure)
EVENT_BUFFER_SIZE = 1024 * (EVENT_SIZE + 16)

# loading default shared library interface(libc)
libc = CDLL(None)
# (return type,*args)
inotify_init = CFUNCTYPE(c_int, use_errno=True)(("inotify_init", libc))
inotify_add_watch = CFUNCTYPE(c_int, c_int, c_char_p, c_uint32, use_errno=True)(
    ("inotify_add_watch", libc)
)
inotify_rm_watch = CFUNCTYPE(c_int, use_errno=True)(("inotify_rm_watch", libc))
