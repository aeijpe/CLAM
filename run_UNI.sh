#!/bin/bash
#SBATCH --job-name=get_data            # Job name
#SBATCH --partition=gpu                # Partition name (queue)
#SBATCH --cpus-per-task=4              # Number of CPU cores per task
#SBATCH --gres=tmpspace:10G            # Temporary disk space required
#SBATCH --gres=gpu:1                   # Number of GPUs per node
#SBATCH --time=12:00:00                # Time limit in HH:MM:SS
#SBATCH --mem=100G                     # Total memory per node
#SBATCH --output=jobs/slurm_%j.log      # Total memory per node

# Start interactive bash session
source /hpc/uu_inf_aidsaitfl/miniconda3/bin/activate clam_latest

# Create patches
# python create_patches_fp.py --source blca_dataset/ --save_dir blca_patched/ --res 0.5 --patch_size 256 --preset tcga.csv --seg --patch --stitch 

# # Obtain patch features
# export UNI_CKPT_PATH=checkpoints/UNI/pytorch_model.bin
# CUDA_VISIBLE_DEVICES=0 python extract_features_fp.py --data_h5_dir blca_patched/ --data_slide_dir blca_dataset/ --csv_path blca_patched/process_list_autogen.csv --feat_dir ../data/tcga_blca/wsi/extracted_res0_5_patch256_uni/ --batch_size 256 --target_patch_size 256 --slide_ext .svs --model_name uni_v1