import websockets
import asyncio
import json

# Set to keep track of connected clients
connected_clients = set()

async def handler(websocket):
    connected_clients.add(websocket)

    try:
        msg_as_json = json.dumps({"message": "Hello, World!"})
        await websocket.send(msg_as_json)

        async for message in websocket:
            print(message)

    finally:
        connected_clients.remove(websocket)

async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("WebSocket server started.")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())