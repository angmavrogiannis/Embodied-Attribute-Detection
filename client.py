#!/usr/bin/env python

import asyncio
import websockets
import base64

async def hello():
    uri = "ws://localhost:8765" # 192.168.1.178 home ip
    async with websockets.connect(uri) as websocket:
        # name = input("Send a picture.")
        with open("panda.jpeg", "rb") as f:
            fcontent = f.read()

        await websocket.send(base64.b64encode(fcontent).decode('utf-8'))
        result = await websocket.recv()
        print(f"<<< Ok, bounding box coords are: {result}")
        with open("bbox.txt", "w") as f:
            f.write(result)

if __name__ == "__main__":
    asyncio.run(hello())
