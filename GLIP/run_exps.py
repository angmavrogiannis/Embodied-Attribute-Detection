import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import argparse
import requests
from io import BytesIO
from PIL import Image
import numpy as np
pylab.rcParams['figure.figsize'] = 20, 12
from maskrcnn_benchmark.config import cfg
from maskrcnn_benchmark.engine.predictor_glip import GLIPDemo
import json
from os import listdir

def load(filename):
    """
    Given an url of an image, downloads the image and
    returns a PIL image
    """
    # response = requests.get(url)
    # pil_image = Image.open(BytesIO(response.content)).convert("RGB")
    pil_image = Image.open(filename).convert("RGB")
    # convert to BGR format
    image = np.array(pil_image)[:, :, [2, 1, 0]]
    return image

def imshow(img, prompt, savepath):
    plt.imshow(img[:, :, [2, 1, 0]])
    plt.axis("off")
    plt.figtext(0.5, 0.09, prompt, wrap=True, horizontalalignment='center', fontsize=20)
    plt.savefig(savepath)
    plt.close()

# parser = argparse.ArgumentParser(description='Open-vocabulary object detection')
# parser.add_argument('-p','--prompt', help='prompt (open-vocabulary description of object to detect)', required=True)
# parser.add_argument('-i','--input_image', help='Path of input image (optional)', required=False)
# parser.add_argument('-i','--input_file', help='Path of input json file with captions', required=True)
# args = parser.parse_args()

config_file = "configs/pretrain/glip_Swin_L.yaml"
weight_file = "MODEL/glip_large_model.pth"

cfg.local_rank = 0
cfg.num_gpus = 1
cfg.merge_from_file(config_file)
cfg.merge_from_list(["MODEL.WEIGHT", weight_file])
cfg.merge_from_list(["MODEL.DEVICE", "cuda"])

glip_demo = GLIPDemo(
    cfg,
    min_image_size=800,
    confidence_threshold=0.7,
    show_mask_heatmaps=False
)

print('glip_demo')

# f = open(args.input_file)
# data = json.load(f)
filenames = [f for f in listdir("../BLIP/ai2thor_heavy") if f.endswith("jpeg")]
for filename in filenames:
    path = f"../BLIP/ai2thor_heavy/{filename}"
    prompt = "the most lightweight object"
    image = load(path)
    result, prediction = glip_demo.run_on_web_image(image, prompt, 0.5)
    imshow(result, prompt, f'images/glip_abs_weight/detections/glip_{filename}')
    pred = prediction.bbox.squeeze().detach().numpy()
    print(f"filename: {filename}, pred: {pred}")
    imshow(result, prompt, f'ai2thor_heavy/pred_{filename}')
    # np.savetxt(f"images/glip_abs_weight/bboxes/glip_{filename[:-5]}.out", pred, delimiter=",")

#print(f"result: {[round(coord) for coord in list(prediction.bbox.squeeze().detach().numpy())]}")
#with open("bbox.txt", "w") as f:
#    for coord in list(prediction.bbox.squeeze().detach().numpy()):
#        f.write(str(round(coord)) + "\n")
# imshow(result, args.prompt, f'images/glip_{args.input_directory}')
