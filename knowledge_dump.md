Resource -> https://copyconstruct.medium.com/nonblocking-i-o-99948ad7c957


# I/O and Descriptors Explained

## 1. What is I/O?
**I/O** stands for **Input/Output** — it’s how a program communicates with the outside world.

- **Input** → Reading data (from a file, socket, user input, etc.)
- **Output** → Writing data (to a file, socket, screen, etc.)

### Examples of I/O:
✅ Reading a file → `read()`  
✅ Writing to a file → `write()`  
✅ Receiving data from a network → `recv()`  
✅ Sending data over a network → `send()`  

### Example:
When you run this command:
```sh
cat file.txt
```
- `cat` → Reads from the file (`input`)  
- `cat` → Outputs the file contents to the terminal (`output`)  

---

## 2. What are Descriptors?
When a program opens a file (or any I/O resource), the **kernel** assigns an integer value to represent that resource — this is called a **file descriptor**.

### Example:
```c
int fd = open("file.txt", O_RDONLY);
```
- `fd` is an integer that represents the open file.  
- You can use `fd` to read, write, or close the file.  

### Common File Descriptors (by default):
| Descriptor | Purpose |
|-----------|---------|
| `0`       | Standard input (stdin)  |
| `1`       | Standard output (stdout) |
| `2`       | Standard error (stderr)  |

### Example:
If you open two files:
```c
int fd1 = open("file1.txt", O_RDONLY);
int fd2 = open("file2.txt", O_RDONLY);
```
- `fd1 = 3` → First available descriptor after 0, 1, 2  
- `fd2 = 4` → Next available descriptor  

The kernel internally maintains a table like this:

| FD | Resource Type | Path |
|----|---------------|------|
| 0  | stdin         | /dev/tty |
| 1  | stdout        | /dev/tty |
| 2  | stderr        | /dev/tty |
| 3  | file          | file1.txt |
| 4  | file          | file2.txt |

---

## 3. Problem with Basic I/O
Most I/O operations are **blocking** by default — this means:
- If you call `read(fd, buffer, size)`, and there’s no data available, your program will **stop** and wait for data.
- If the network is slow or the file is large, the program will freeze until the operation completes.

### Example:
```c
char buffer[128];
int bytes_read = read(fd, buffer, sizeof(buffer));
```
- If data is available → `read()` returns immediately with the data.  
- If no data is available → `read()` **blocks** (pauses) until data becomes available.  

---

## 4. Non-Blocking I/O
To avoid blocking, you can set the descriptor to **non-blocking** mode using `fcntl()`:

### Example:
```c
int flags = fcntl(fd, F_GETFL, 0);
fcntl(fd, F_SETFL, flags | O_NONBLOCK);
```
- If data is available → `read()` returns data immediately.  
- If no data is available → `read()` **returns -1** and sets `errno` to `EAGAIN` or `EWOULDBLOCK`.  

### Why Use Non-Blocking I/O?
✅ Program keeps running even if no data is available.  
✅ Makes it possible to handle **multiple I/O streams** at the same time.  

---

## 5. Multiplexing I/O
If you have multiple descriptors (like sockets or files), how do you know which one is ready?  
Instead of constantly checking each descriptor, you can ask the kernel:
> "Let me know which descriptor is ready to read or write."

### There are 3 common ways to do this:
1. **select()** → Basic  
2. **poll()** → More scalable  
3. **epoll()** → High-performance (Linux)  

### (A) select()
- You create a **set of descriptors** and tell the kernel:  
   👉 "Tell me which ones are ready."  
- Works with up to **1024 descriptors**.  
- After each call, you must **rebuild** the set (which makes it slow).  

**Example:**
```c
fd_set readfds;
FD_ZERO(&readfds);
FD_SET(fd1, &readfds);
FD_SET(fd2, &readfds);

int result = select(fd2 + 1, &readfds, NULL, NULL, NULL);

if (result > 0) {
    if (FD_ISSET(fd1, &readfds)) {
        // fd1 is ready
    }
    if (FD_ISSET(fd2, &readfds)) {
        // fd2 is ready
    }
}
```
✅ Simple  
❌ Slow for large sets of descriptors  

### (B) poll()
- Works like `select()` but uses an **array** instead of a fixed set.  
- You pass an array of `struct pollfd` to the kernel.  
- Still scans linearly, so it’s not very efficient for large descriptor sets.  

**Example:**
```c
struct pollfd fds[2];
fds[0].fd = fd1;
fds[0].events = POLLIN;
fds[1].fd = fd2;
fds[1].events = POLLIN;

int result = poll(fds, 2, -1);

if (result > 0) {
    if (fds[0].revents & POLLIN) {
        // fd1 is ready
    }
    if (fds[1].revents & POLLIN) {
        // fd2 is ready
    }
}
```
✅ No descriptor limit  
❌ Linear scanning = Slow for large descriptor sets  

### (C) epoll()
- Only available on **Linux**.  
- You tell the kernel once which descriptors you want to watch.  
- The kernel maintains the state — you don’t need to rebuild sets!  

**Example:**
```c
int epfd = epoll_create1(0);

struct epoll_event event;
event.events = EPOLLIN;
event.data.fd = fd;
epoll_ctl(epfd, EPOLL_CTL_ADD, fd, &event);

struct epoll_event events[10];
int num_events = epoll_wait(epfd, events, 10, -1);

for (int i = 0; i < num_events; i++) {
    if (events[i].events & EPOLLIN) {
        // fd is ready
    }
}
```
✅ Fast, scales well  
✅ Efficient event-based model  
❌ Linux-only  

---

## 6. Edge-Triggered vs Level-Triggered
- **Level-triggered** → Keeps notifying you if the descriptor is ready.  
- **Edge-triggered** → Notifies you **only once** when the descriptor becomes ready.  

### Example:
- Level-triggered → You keep getting notifications if data is available.  
- Edge-triggered → You get notified only when data first becomes available.  

👉 `epoll` and `kqueue` support **both modes**.  
👉 Level-triggered = Safer, easier to handle.  
👉 Edge-triggered = High-performance, but you need to handle data immediately.  

---

### Non blocking vs Multiplexing IO
| **Aspect** | **Non-Blocking I/O** | **Multiplexing I/O** |
|-----------|----------------------|---------------------|
| **Focus** | Behavior of individual I/O operation | Handling multiple descriptors simultaneously |
| **Purpose** | Prevent process from blocking on a single descriptor | Efficiently monitor multiple descriptors for readiness |
| **Example** | `fcntl(fd, F_SETFL, O_NONBLOCK)` | `epoll()`, `select()`, `poll()` |
| **How It Works** | `read()` or `write()` returns immediately if no data is available | Kernel tells you which descriptor is ready for I/O |
| **Problem** | If data isn’t available, you need to retry manually → Inefficient for many descriptors | If descriptor isn’t set to `O_NONBLOCK`, `read()` or `write()` can still block |
| **Efficiency** | Wastes CPU cycles if repeatedly polling | Efficient handling of large sets of descriptors |
| **Best Use Case** | When handling a **single** descriptor | When handling **many** descriptors at once |
| **Combination** | Works best with multiplexing for high-performance I/O | Requires `O_NONBLOCK` for truly non-blocking I/O |

✅ Why Use Both Together?
👉 O_NONBLOCK → Ensures read() or write() won’t block.
👉 epoll → Efficiently monitors multiple descriptors and tells you when they’re ready.

## ✅ Summary
✅ I/O streams = Input/Output sources (files, sockets, etc.)  
✅ Descriptor = Integer handle to reference an open I/O stream  
✅ Blocking = Process pauses until I/O is ready  
✅ Non-blocking = I/O returns immediately  
✅ Multiplexing = Handling multiple descriptors at once
✅ `select()` → Simple, slow  
✅ `poll()` → More flexible, still slow for large sets  
✅ `epoll()` → Fast and scalable (preferred for high-performance apps)  
