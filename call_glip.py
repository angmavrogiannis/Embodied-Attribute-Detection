cd /fs/nexus-scratch/angelosm/GLIP
source /fs/nexus-scratch/angelosm/miniconda3/bin/activate glip
submit.sh
squeue | grep 'angelosm' | awk '{ print $1 }'
