#!/bin/bash
#SBATCH --job-name=get_data            # Job name
#SBATCH --partition=gpu                # Partition name (queue)
#SBATCH --cpus-per-task=4              # Number of CPU cores per task
#SBATCH --gres=tmpspace:10G            # Temporary disk space required
#SBATCH --gres=gpu:1                   # Number of GPUs per node
#SBATCH --time=05:00:00                # Time limit in HH:MM:SS
#SBATCH --mem=100G                     # Total memory per node
#SBATCH --output=jobs/slurm_%j.log      # Total memory per node



# Start interactive bash session
source /hpc/uu_inf_aidsaitfl/miniconda3/bin/activate
conda activate clam_latest

export TMPDIR=/hpc/uu_inf_aidsaitfl/
# Create patches
# python download_TCGA_data.py
python create_patches_fp.py --source brca_dataset/ --save_dir brca_patched/ --res 0.5 --patch_size 256 --preset tcga.csv --seg --patch --stitch 
# 
# export UNI_CKPT_PATH=checkpoints/UNI/pytorch_model.bin
# # Adjust batch size, depending on GPU req! 
# # Adjust target_path_size to 224?? --> is this solid or not?
# CUDA_VISIBLE_DEVICES=0 python extract_features_fp.py --data_h5_dir brca_patched/ --data_slide_dir brca_dataset/ --csv_path brca_patched/process_list_autogen.csv --feat_dir ../MMP/src/data_wsi/tcga_brca/extracted_res0_5_patch256_uni/ --batch_size 256 --target_patch_size 256 --slide_ext .svs --model_name uni_v1