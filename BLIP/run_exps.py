import torch
from PIL import Image
import requests
from lavis.models import load_model_and_preprocess
import time
import argparse
import pickle
import json
from os import listdir

img_url = 'https://storage.googleapis.com/sfr-vision-language-research/LAVIS/assets/merlion.png' 
# print(raw_image.size)  
# display(raw_image.resize((596, 437)))

# setup device to use
device = torch.device("cuda") if torch.cuda.is_available() else "cpu"

model, vis_processors, _ = load_model_and_preprocess(
    name="blip2_t5", model_type="pretrain_flant5xl", is_eval=True, device=device
)
parser = argparse.ArgumentParser(description='Simple Visual Question Answering (VQA)')
# parser.add_argument('-p','--prompt', help='prompt (visual query)', required=True)
# parser.add_argument('-i','--input_image', help='Path of input image (optional)', required=False)
# parser.add_argument('-i','--input_file', help='Input json file', required=True)
# args = parser.parse_args()

# f = open(args.input_file)
# data = json.load(f)
image_dir = "ai2thor_dist"
with open(image_dir + "/" + 'prompts.pickle', 'rb') as prompt_file:
    prompts = pickle.load(prompt_file)
filenames = [f for f in listdir(image_dir) if f.endswith("jpeg")]
answers = []
for filename in filenames:
    path = image_dir + "/" + filename
    raw_image = Image.open(path).convert('RGB')   
    image = vis_processors["eval"](raw_image).unsqueeze(0).to(device)
    start = time.time()
    answer = model.generate({"image": image, "prompt": prompts[filename]})
    answers.append(answer)
    #answer_dict[filename] = answer
    # with open(f"images/heavy_data/vqa_{filename[:-5]}.txt", "w") as f:
    #     f.write(answer[0])
    end = time.time()
    print("Time taken: ", end - start)
with open("blip_appliances_ai2thor_dist.txt", "w") as f:
    for filename, item in zip(filenames, answers):
        f.write(f"{filename}: {item}\n")

#with open('blip_heavy_abs.pkl', 'wb') as f:
#    pickle.dump(answer_dict, f)
