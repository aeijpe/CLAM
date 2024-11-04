#!/bin/bash
#SBATCH --job-name=get_data            # Job name
#SBATCH --cpus-per-task=8              # Number of CPU cores per task
#SBATCH --gres=tmpspace:10G            # Temporary disk space required
#SBATCH --time=40:00:00                # Time limit in HH:MM:SS
#SBATCH --output=jobs/slurm_%j.log      # Total memory per node


# Start interactive bash session
source /hpc/uu_inf_aidsaitfl/miniconda3/bin/activate
conda activate clam_latest

export TMPDIR=/hpc/uu_inf_aidsaitfl/
# Create patches
python download_TCGA_data.py