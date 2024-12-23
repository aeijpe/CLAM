#!/bin/bash
#SBATCH --job-name=get_data            # Job name
#SBATCH --cpus-per-task=4              # Number of CPU cores per task
#SBATCH --gres=tmpspace:10G            # Temporary disk space required
#SBATCH --time=12:00:00                # Time limit in HH:MM:SS
#SBATCH --mem=100G                     # Total memory per node
#SBATCH --output=jobs/slurm_%j.log      # Total memory per node

# Start interactive bash session
source /hpc/uu_inf_aidsaitfl/miniconda3/bin/activate clam_latest

# Download data
python download_TCGA_data.py --dataset kirc --file_path ../data/tcga_kirc/splits/TCGA_KIRC_overall_survival_k=0