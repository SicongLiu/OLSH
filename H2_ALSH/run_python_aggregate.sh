#!/bin/bash


#SBATCH -p serial                   # Send this job to the serial partition
#SBATCH -n 4                        # number of cores
#SBATCH --mem=14000                 # 14 GB
#SBATCH -t 0-15:00                  # wall time (D-HH:MM)
#SBATCH -o slurm.%j.out             # STDOUT (%j = JobId)
#SBATCH -e slurm.%j.err             # STDERR (%j = JobId)
#SBATCH --mail-type=END,FAIL        # notifications for job done & fail
#SBATCH --mail-user=sliu104@asu.edu # send-to address

module load gcc/4.9.2
cd /home/sliu104/LSH_TopK_Saguaro/Python_Analysis/
python LSH_Post_Process.py

