#!/usr/bin/env python

import asyncio
import websockets
from PIL import Image
import base64
import time
import io
import cv2
import os

async def hello(websocket):
    start = time.time()
    prompt = await websocket.recv()
    image = await websocket.recv()
    print("Prompt and image received..")

    decoded_img = base64.b64decode(image)
    f = io.BytesIO(decoded_img)
    img_file = Image.open(f)
    img_filename = "input.jpg"
    img_file.save(img_filename)
    os.system("head -n -1 submit.sh > temp.txt ; mv temp.txt submit.sh")
    bash_command = f"echo 'srun -u python demo.py --input_image=\"{img_filename}\" --prompt=\"{prompt.rstrip()}\"' >> submit.sh"
    os.system(bash_command)
    os.system("sbatch submit.sh")
    while not os.path.exists("bbox.txt"):
        time.sleep(0.1)
    print("Output file created.")
    end = time.time()
    print(f"Elapsed time: {end - start}")

    with open("bbox.txt", "r") as f:
        lines = [int(line.rstrip()) for line in f]
    await websocket.send(str(lines))
    print("Done!")

async def main():
    async with websockets.serve(hello, "localhost", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
