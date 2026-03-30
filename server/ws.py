import websockets
import asyncio
import json

from controller import MyController

connected_clients = set()
event_queue = None
main_loop = None

# Function to broadcast events to all connected clients.
def push_events(events):
    if event_queue is not None and main_loop is not None:
        # I am using call_soon_threadsafe to safely put events into the queue from another thread.
        main_loop.call_soon_threadsafe(event_queue.put_nowait, events)


async def broadcast_events():
    while True:
        events = await event_queue.get()
        msg = json.dumps(events, default=str) # Convert events to JSON string.

        if connected_clients:
            # websockets.broadcast is much safer and optimized than asyncio.gather for broadcasting
            websockets.broadcast(connected_clients, msg)


async def handler(ws):
    connected_clients.add(ws) # Add the new client to the set of connected clients.

    try:
        # Get the current snapshot of the constellation.
        first_snapshot = ctrl.get_all_satellites() 
        
        msg = json.dumps({
            "type": "first_snapshot",
            "data": first_snapshot
        }, default=str)

        # Send the initial snapshot to the newly connected client.
        await ws.send(msg)

        # Listen commands from the client.
        async for raw in ws:
            try:
                # Parse the incoming message as JSON.
                received_msg = json.loads(raw)
                
                # Get the type of the message to determine how to process it.
                msg_type = received_msg.get("type")

                # If the message type is "send_command", process the command.
                if msg_type == "send_command":
                    # Get the command, target satellite, and payload from the message.
                    cmd = received_msg.get("cmd")
                    target = received_msg.get("target")
                    payload = received_msg.get("payload", {})
                    
                    # Send the synchronous command to a separate thread to prevent blocking the async event loop.
                    result = await asyncio.to_thread(ctrl.send_command, target, cmd, payload)
                    
                    response_msg = json.dumps({
                        "type": "command_response",
                        "data": result
                    }, default=str)
                    
                    # Send the command response back to the client.
                    await ws.send(response_msg)
                
                else:
                    # Notifying the client about an unknown message type
                    error_msg = json.dumps({
                        "type": "error",
                        "message": f"Unknown message type: {msg_type}"
                    })
                    await ws.send(error_msg)

            except websockets.exceptions.ConnectionClosed:
                # Do not try to send error messages to a closed connection
                break

            except Exception as e:
                error_msg = json.dumps({
                    "type": "error",
                    "message": str(e)
                }, default=str)
                
                await ws.send(error_msg)

    finally:
        # Remove the client from the set of connected clients when it disconnects.
        connected_clients.remove(ws)


async def main():
    global event_queue, main_loop
    
    # Get the current event loop.
    main_loop = asyncio.get_running_loop()
    
    # Initialize the event queue AFTER the loop is running.
    event_queue = asyncio.Queue()

    # Start the event broadcasting task.
    asyncio.create_task(broadcast_events())

    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()  # Run forever


# Create an instance of MyController and set the push_events function as the callback for updates.
ctrl = MyController(
    group="test",
    on_update=push_events
)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        ctrl.reentry()