# Constellation Web Interface - Proof of Concept (PoC)

This repository is a Proof of Concept (PoC) project developed as part of the Google Summer of Code (GSoC). The goal of this project is to bring the core satellite management features of the Constellation framework's desktop-based MissionControl application to the web.

In this project, a custom controller class was written using the standard Constellation Python API. Live satellite management (real-time status tracking, sending commands, etc.) is successfully achieved through a web interface via WebSockets. There may be some issues within the scope of this PoC. These will be resolved during the development of the main project. While this PoC does not include all the capabilities of MissionControl, it aims to prove that a web-based architecture is viable.

## Screenshots and Usage

### Constellation MissionControl (Reference Application)

The Constellation network uses the **MissionControl** application as the standard way to monitor and manage satellites. In the GIF below, you can see the standard usage of the original desktop application, satellite state management, and the current interface dynamics.

![MissionControl Usage](/images/mission_control_overview.gif)

### Web PoC and MissionControl Synchronization

One of the strongest parts of the web-based solution we developed is its ability to provide real-time, two-way synchronization with the Constellation ecosystem.

In the GIF below, you can see the Web Application of this project and the original MissionControl window running at the same time. A state change triggered from the web interface is instantly seen in the MissionControl app. Similarly, any action taken in MissionControl updates immediately on the web interface without delay. This is strong proof that our architecture works perfectly with the existing network.

One important note here is that values like "Last Message", "Heartbeat", and "Lives" are not updated dynamically. To keep this PoC simple, these values are currently static. During the full project development, all this data will be handled dynamically and in sync. Only the outputs of functions starting with `get_` are printed in the "Last Message" area to show what happens when a command like `get_name` is sent to a satellite. Not all commands from the MissionControl interface are active in the web interface yet. The goal is to build a pop-up identical to the one in MissionControl. In the background, other `get_` functions were added to the list but have been commented out to hide them from the interface for now.

Also, you might notice that when a command like `get_name` is sent to a satellite, the output only appears on the client that sent the command. You can confirm this is not a synchronized action by opening two different MissionControl windows.

![Web and MissionControl Sync](/images/web_ui_and_mission_control.gif)

When you log into the web interface, it automatically lists the satellites in the network, and their statuses can be tracked live. When a new satellite is detected, it is added to the interface. If a satellite is removed, it automatically disappears from the dashboard.
![Dashboard Live](/images/live_satellite_data.gif)

## Custom Controller Class (`MyController`)

The heart of this PoC project is the `MyController` class, which handles all satellite operations. Fetching satellite data, tracking state changes, and sending commands are all done through this class.

If you look at `server/controller.py`, you will see that `MyController` inherits from the `ScriptableController` class found in the Constellation Python API. The inheritance chain is as follows:

![Inheritance](/images/inheritence.png)

The basic structure of the `MyController` class looks like this:

```python
class MyController(ScriptableController):
    def __init__(self, on_update=None, **kwargs):
        # ...

    def _build_snapshot(self):
        # ...

    def _add_satellite(self, service):
        # ...

    def _remove_satellite(self, service):
        # ...

    def _poll_heartbeats(self):
        # ...

    def _dispatch(self, events):
        # ...

    def _emit(self):
        # ...

    def send_command(self, canonical_name, cmd, payload=None):
        # ...

    def get_satellite_details(self, canonical_name):
        # ...

    def get_all_satellites(self):
        # ...
```

Here is a quick summary of what these functions do:

- **`_build_snapshot()`**: Takes a "snapshot" of the current state of the Constellation network. It holds the names, types, current states, and last modified times of the satellites.
  _Example output:_

  ```json
  {
  	"Sputnik.Device1": {
  		"name": "Device1",
  		"type": "Sputnik",
  		"state": "ORBIT",
  		"last_changed": "2026-03-30 22:43:01.997005+00:00"
  	}
  }
  ```

- **`_add_satellite()` & `_remove_satellite()`**: The Constellation framework automatically detects satellites in the network using the CHIRP protocol. Inherited from `BaseController`, these methods trigger automatically when a new satellite joins or leaves the network. In this project, they are overridden to call the `_emit()` function, so the interface gets updated instantly.

- **`_poll_heartbeats()`**: Inherited from the `HeartbeatChecker` class, this method is triggered when a regular 'heartbeat' is received from the satellites. It calls the `_emit()` method every time to ensure the interface stays live.

- **`_emit()`**: This is the most critical method for keeping the interface updated in real-time using WebSockets. It compares the old snapshot with a new one created by `_build_snapshot()`. It finds:
  - Newly added satellites,
  - Satellites that have disconnected (DEAD),
  - Satellites that have changed their state.
    Then, it packages them and sends them to the `_dispatch()` method to be broadcast.

- **`_dispatch(events)`**: Notifies the outside world about the changes. It runs the `on_update` callback provided during class startup, sending the data to the WebSocket server (and then to the web interface).

- **`send_command()`**: The function needed to send a command with parameters to a specific satellite (e.g., `Sputnik.Device1`).

- **`get_satellite_details()` & `get_all_satellites()`**: These functions retrieve data for a specific satellite or all satellites from the latest snapshot.

### WebSocket Server

While `MyController` listens to satellite data in the background and sends it out using `_dispatch()`, the task of sending this data to the web interface instantly and without interruption belongs to the WebSocket server in `server/ws.py`. However, an important architectural problem must be solved here to keep the system stable.

Background operations coming from the Python API run on separate threads. In contrast, our WebSocket server, which needs to efficiently handle fast and multiple connections, runs asynchronously (`asyncio`). If these background threads try to directly and suddenly send data into the running asyncio WebSocket loop, they break thread safety, which will cause the application to crash.

To make these two different architectures work together safely, an asynchronous **queue system** is placed between them. Here is how `ws.py` works:

First, when `MyController` starts, it is told where to send updates:

```python
# The push_events function is called when updates are triggered
ctrl = MyController(
    group="test",
    on_update=push_events
)
```

When a new update comes from `MyController`, this data is not thrown directly to the users. Instead, it is pushed into a queue using the `push_events()` function:

```python
def push_events(events):
    if event_queue is not None and main_loop is not None:
        # Data can't be written directly to the async queue from a different thread.
        # This is why the data is safely placed in the queue using call_soon_threadsafe.
        main_loop.call_soon_threadsafe(event_queue.put_nowait, events)
```

The critical part here is the `call_soon_threadsafe()` method. This acts as a safe bridge that allows the background thread to drop its data into the asynchronous `event_queue` without locking or crashing the system.

Finally, the WebSocket server pulls this ready data from the queue one by one and broadcasts it to the users:

```python
async def broadcast_events():
    while True:
        # Takes the next data when the WebSocket server is ready
        events = await event_queue.get()
        msg = json.dumps(events, default=str)

        # Broadcasts the message to all connected web clients
        if connected_clients:
            websockets.broadcast(connected_clients, msg)
```

In summary, instead of dangerously sending data directly over the network, background operations leave the data in this designated queue using a safe transfer method. The asynchronous WebSocket server then takes the data from the queue when it is its turn and smoothly broadcasts it to the clients.

## AI Usage Policy

AI assistants were utilized in the preparation of this README file and during the development of the front-end.

The design and architecture of the front-end were primarily adapted from my other project, [DAQ Command Center](https://github.com/cysctl/daq-command-center).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
