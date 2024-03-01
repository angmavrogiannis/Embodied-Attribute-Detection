#!/usr/bin/env python

import asyncio
import websockets
import base64
import time
import os

async def hello():
    uri = "ws://localhost:8765" # 192.168.1.178 home ip
    async with websockets.connect(uri) as websocket:
        with open("task_prompt.txt", "r") as f:
            task_prompt = f.read()
        await websocket.send(task_prompt)
        task, prompt = [item for item in task_prompt.split("\n") if item]
        with open("ovd.jpg", "rb") as f:
            fcontent = f.read()

        await websocket.send(base64.b64encode(fcontent).decode('utf-8'))
        print(">>> Query and image sent successfully")
        start = time.time()
        result = await websocket.recv()
        print(">>> Result received {time.time() - start} seconds after the query and image were sent.")

        if task == "ovd":
            print(f"<<< Open-Vocabulary Description: {prompt} \n >>> Bounding box coords are: {result}")
            output_file = "bbox.txt"
        else:
            print(f"<<< Visual query: {prompt} \n >>> Answer: {result}")
            output_file = "vqa.txt"
        with open(output_file, "w") as f:
            f.write(result)

if __name__ == "__main__":
    asyncio.run(hello())
