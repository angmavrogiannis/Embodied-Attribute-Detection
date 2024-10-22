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
    task_prompt = await websocket.recv()
    image = await websocket.recv()
    print("Task type, prompt, and image received..")

    task, prompt = [item for item in task_prompt.split("\n") if item]
    with open("prompt.txt", "w") as f:
        f.write(prompt)

    decoded_img = base64.b64decode(image)
    f = io.BytesIO(decoded_img)
    img = Image.open(f)
    if task == "ovd":
        img_filename = "ovd.jpg"
        output_file = "bbox.txt"
    else:
        img_filename = "vqa.jpg"
        output_file = "vqa.txt"
    img.save(img_filename)
    # os.system("head -n -1 submit.sh > temp.txt ; mv temp.txt submit.sh")
    # bash_command = f"echo 'srun -u python demo.py --input_image=\"{img_filename}\" --prompt=\"{prompt.rstrip()}\"' >> submit.sh"
    # os.system(bash_command)
    # os.system("sbatch submit.sh")
    while not os.path.exists(output_file):
        time.sleep(0.1)
    print(">>> Output file created.")
    end = time.time()
    print(f">>> Elapsed time: {end - start}")
    
    with open(output_file, "r") as f:
        if task == "ovd":
            output = str([int(line.rstrip()) for line in f])
        else:
            output = f.read().rstrip()

    await websocket.send(output)
    os.system(f"rm -rf {output_file}")
    print("Done!")

async def main():
    async with websockets.serve(hello, "localhost", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
