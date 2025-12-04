import asyncio
import websockets
import json

async def test_ws():
    uri = "ws://localhost:8765/ws"
    print(f"Connecting to {uri}...")
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected!")
            # Send a ping
            await websocket.send(json.dumps({"type": "ping"}))
            print("Sent ping")
            
            response = await websocket.recv()
            print(f"Received: {response}")
            
            print("Waiting for 5 seconds to check stability...")
            await asyncio.sleep(5)
            print("Connection still open.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_ws())
