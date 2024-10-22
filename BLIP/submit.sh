#!/bin/bash
#SBATCH -N 1
#SBATCH --ntasks 1
#SBATCH --mem 48GB
#SBATCH --qos high
#SBATCH --gres=gpu:rtxa6000:1

module add cuda
module add Python3
module add ffmpeg

export TRANSFORMERS_CACHE=/fs/nexus-scratch/angelosm/.cache/blip

# srun -u python vqa.py --prompt='is the pot empty?' --input_image='kitchen.jpeg'
srun -u python run_exps.py
