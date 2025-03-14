# Inotify generate events

We can process them in two ways
* Using a generator based streming to read all streams of event in real time

* Using a queue to store events temporarily then processing. We can multiple threads to process this

# Why a hybrid approach?
* We are building a file watcher based control handling system.
So what if 50 files got changed in real time?
> We need to active lookup + debouncing + squashing or neglecting same events if required
* My api design -> 
    ```python3
    observer = watcher.add(Path(),Path()).ignore(Path()).on(Events.CREATE).run(Command)
    status_code = observer.observe()
    ```
1. Generator(event streaming) as a Gatekeeper:

The generator will provide a continuous stream of events directly from inotify (low-latency).
It filters or drops irrelevant events — only passes the needed ones to the queue.
Ensures you don't overwhelm the queue with irrelevant noise.

2. Queue as a Buffer:

The queue absorbs bursts and smooths out spikes in event flow.
If events come too fast, they are held in the queue (instead of being lost).
Acts as a buffer between the generator and the processing logic.

3. Worker Thread for Processing:

A worker thread (or pool) can consume events from the queue at a controlled rate.
You can throttle how fast the processing happens based on system load.
Helps to handle bursty traffic while preventing event loss.

4. Subprocess Handling:
Runs the command using subprocess.Popen
Redirects logs to the terminal
Kills the process on restart