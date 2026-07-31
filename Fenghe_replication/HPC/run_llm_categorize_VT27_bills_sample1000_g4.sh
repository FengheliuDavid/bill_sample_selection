#!/bin/bash
#SBATCH --job-name=bill_VT27_s5k_g4
#SBATCH --array=1-5%5
#SBATCH --partition=gpunormal
#SBATCH --gres=gpu:a100:1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --time=24:00:00
#SBATCH --output=llm_bill_VT27_category_outputs_sample5000_06_29_g4/logs/task_%j_%a.out
#SBATCH --error=llm_bill_VT27_category_outputs_sample5000_06_29_g4/logs/task_%j_%a.err

WORKDIR=/gpfs/home/fl488/process_bill_text
mkdir -p $WORKDIR/llm_bill_VT27_category_outputs_sample5000_06_29_g4/logs
cd $WORKDIR

module purge
module load anaconda3
module load cuda/toolkit/12.9.0

source /apps/spack/apps-2025/linux-rhel9-x86_64_v3/none-none/anaconda3/2023.09-0-k3at/etc/profile.d/conda.sh
conda activate llama_cuda_g4

export LD_LIBRARY_PATH="/apps/spack/apps-2025/linux-rhel9-x86_64_v3/none-none/cuda/12.9.0-xsr6/lib64:$LD_LIBRARY_PATH"

echo "Starting task ${SLURM_ARRAY_TASK_ID} of ${SLURM_ARRAY_TASK_COUNT} on $(hostname)"
python 8_llm_categorize_VT27_bills_sample1000_g4.py
echo "Task ${SLURM_ARRAY_TASK_ID} complete"
