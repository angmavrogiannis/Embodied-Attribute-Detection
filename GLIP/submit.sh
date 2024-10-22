#!/bin/bash
#SBATCH -N 1
#SBATCH --ntasks 1
#SBATCH --mem=16G
#SBATCH --qos high
#SBATCH --gres=gpu:1

module add cuda
module add Python3
module add ffmpeg

srun -u python run_exps.py
# srun -u python run_exps.py --input_file="heavy.json"
# srun -u python real_time_detection.py
