#!/bin/bash 
#SBATCH -p serial 	 	 # Send this job to the serial partition 
#SBATCH -n 4 # number of cores 
#SBATCH --mem=32000                 # 32 GB 
#SBATCH -t 0-15:00                  # wall time (D-HH:MM) 
#SBATCH -o slurm.%j.out             # STDOUT (%j = JobId) 
#SBATCH -e slurm.%j.err             # STDERR (%j = JobId) 
#SBATCH --mail-type=END,FAIL        # notifications for job done & fail 
#SBATCH --mail-user=sliu104@asu.edu # send-to address 
module load gcc/4.9.2 
datatype=NBA
cardinality=23338
d=7
qn=1000
# ------------------------------------------------------------------------------ 
#     Ground-Truth 
# ------------------------------------------------------------------------------ 
dPath=./raw_data/NBA/${datatype}_${d}_${cardinality}.txt 
tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth 
qPath=./query/query_${datatype}.txt 
oFolder=./result/result_${datatype}_${d}D_${cardinality} 
  ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip sleep 2
