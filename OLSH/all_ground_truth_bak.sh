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
datatype=anti_correlated
cardinality=500000
d=2
qn=1000
# ------------------------------------------------------------------------------ 
#     Ground-Truth 
# ------------------------------------------------------------------------------ 
dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt 
tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth 
qPath=./query/query_${d}D.txt 
oFolder=./result/result_${datatype}_${d}D_${cardinality} 
  ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip sleep 2
datatype=correlated
cardinality=500000
d=2
qn=1000
## ------------------------------------------------------------------------------
##     Ground-Truth
## ------------------------------------------------------------------------------
#dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt
#tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth
#qPath=./query/query_${d}D.txt
#oFolder=./result/result_${datatype}_${d}D_${cardinality}
#  ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip sleep 2
#datatype=random
#cardinality=500000
#d=2
#qn=1000
## ------------------------------------------------------------------------------
##     Ground-Truth
## ------------------------------------------------------------------------------
#dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt
#tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth
#qPath=./query/query_${d}D.txt
#oFolder=./result/result_${datatype}_${d}D_${cardinality}
#  ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip sleep 2
#datatype=anti_correlated
#cardinality=1000000
#d=2
#qn=1000
## ------------------------------------------------------------------------------
##     Ground-Truth
## ------------------------------------------------------------------------------
#dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt
#tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth
#qPath=./query/query_${d}D.txt
#oFolder=./result/result_${datatype}_${d}D_${cardinality}
#  ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip sleep 2
#datatype=correlated
#cardinality=1000000
#d=2
#qn=1000
## ------------------------------------------------------------------------------
##     Ground-Truth
## ------------------------------------------------------------------------------
#dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt
#tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth
#qPath=./query/query_${d}D.txt
#oFolder=./result/result_${datatype}_${d}D_${cardinality}
#  ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip sleep 2
#datatype=random
#cardinality=1000000
#d=2
#qn=1000
## ------------------------------------------------------------------------------
##     Ground-Truth
## ------------------------------------------------------------------------------
#dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt
#tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth
#qPath=./query/query_${d}D.txt
#oFolder=./result/result_${datatype}_${d}D_${cardinality}
#  ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip sleep 2
#datatype=anti_correlated
#cardinality=1500000
#d=2
#qn=1000
## ------------------------------------------------------------------------------
##     Ground-Truth
## ------------------------------------------------------------------------------
#dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt
#tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth
#qPath=./query/query_${d}D.txt
#oFolder=./result/result_${datatype}_${d}D_${cardinality}
#  ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip sleep 2
#datatype=correlated
#cardinality=1500000
#d=2
#qn=1000
## ------------------------------------------------------------------------------
##     Ground-Truth
## ------------------------------------------------------------------------------
#dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt
#tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth
#qPath=./query/query_${d}D.txt
#oFolder=./result/result_${datatype}_${d}D_${cardinality}
#  ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip sleep 2
#datatype=random
#cardinality=1500000
#d=2
#qn=1000
## ------------------------------------------------------------------------------
##     Ground-Truth
## ------------------------------------------------------------------------------
#dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt
#tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth
#qPath=./query/query_${d}D.txt
#oFolder=./result/result_${datatype}_${d}D_${cardinality}
#  ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip sleep 2
#datatype=anti_correlated
#cardinality=2000000
#d=2
#qn=1000
## ------------------------------------------------------------------------------
##     Ground-Truth
## ------------------------------------------------------------------------------
#dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt
#tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth
#qPath=./query/query_${d}D.txt
#oFolder=./result/result_${datatype}_${d}D_${cardinality}
#  ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip sleep 2
#datatype=correlated
#cardinality=2000000
#d=2
#qn=1000
## ------------------------------------------------------------------------------
##     Ground-Truth
## ------------------------------------------------------------------------------
#dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt
#tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth
#qPath=./query/query_${d}D.txt
#oFolder=./result/result_${datatype}_${d}D_${cardinality}
#  ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip sleep 2
#datatype=random
#cardinality=2000000
#d=2
#qn=1000
## ------------------------------------------------------------------------------
##     Ground-Truth
## ------------------------------------------------------------------------------
#dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt
#tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth
#qPath=./query/query_${d}D.txt
#oFolder=./result/result_${datatype}_${d}D_${cardinality}
#  ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip sleep 2
#datatype=anti_correlated
#cardinality=500000
#d=3
#qn=1000
## ------------------------------------------------------------------------------
##     Ground-Truth
## ------------------------------------------------------------------------------
#dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt
#tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth
#qPath=./query/query_${d}D.txt
#oFolder=./result/result_${datatype}_${d}D_${cardinality}
#  ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip sleep 2
#datatype=correlated
#cardinality=500000
#d=3
#qn=1000
## ------------------------------------------------------------------------------
##     Ground-Truth
## ------------------------------------------------------------------------------
#dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt
#tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth
#qPath=./query/query_${d}D.txt
#oFolder=./result/result_${datatype}_${d}D_${cardinality}
#  ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip sleep 2
#datatype=random
#cardinality=500000
#d=3
#qn=1000
## ------------------------------------------------------------------------------
##     Ground-Truth
## ------------------------------------------------------------------------------
#dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt
#tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth
#qPath=./query/query_${d}D.txt
#oFolder=./result/result_${datatype}_${d}D_${cardinality}
#  ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip sleep 2
#datatype=anti_correlated
#cardinality=1000000
#d=3
#qn=1000
## ------------------------------------------------------------------------------
##     Ground-Truth
## ------------------------------------------------------------------------------
#dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt
#tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth
#qPath=./query/query_${d}D.txt
#oFolder=./result/result_${datatype}_${d}D_${cardinality}
#  ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip sleep 2
#datatype=correlated
#cardinality=1000000
#d=3
#qn=1000
## ------------------------------------------------------------------------------
##     Ground-Truth
## ------------------------------------------------------------------------------
#dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt
#tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth
#qPath=./query/query_${d}D.txt
#oFolder=./result/result_${datatype}_${d}D_${cardinality}
#  ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip sleep 2
#datatype=random
#cardinality=1000000
#d=3
#qn=1000
## ------------------------------------------------------------------------------
##     Ground-Truth
## ------------------------------------------------------------------------------
#dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt
#tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth
#qPath=./query/query_${d}D.txt
#oFolder=./result/result_${datatype}_${d}D_${cardinality}
#  ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip sleep 2
#datatype=anti_correlated
#cardinality=1500000
#d=3
#qn=1000
## ------------------------------------------------------------------------------
##     Ground-Truth
## ------------------------------------------------------------------------------
#dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt
#tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth
#qPath=./query/query_${d}D.txt
#oFolder=./result/result_${datatype}_${d}D_${cardinality}
#  ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip sleep 2
#datatype=correlated
#cardinality=1500000
#d=3
#qn=1000
## ------------------------------------------------------------------------------
##     Ground-Truth
## ------------------------------------------------------------------------------
#dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt
#tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth
#qPath=./query/query_${d}D.txt
#oFolder=./result/result_${datatype}_${d}D_${cardinality}
#  ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip sleep 2
#datatype=random
#cardinality=1500000
#d=3
#qn=1000
## ------------------------------------------------------------------------------
##     Ground-Truth
## ------------------------------------------------------------------------------
#dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt
#tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth
#qPath=./query/query_${d}D.txt
#oFolder=./result/result_${datatype}_${d}D_${cardinality}
#  ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip sleep 2
#datatype=anti_correlated
#cardinality=2000000
#d=3
#qn=1000
## ------------------------------------------------------------------------------
##     Ground-Truth
## ------------------------------------------------------------------------------
#dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt
#tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth
#qPath=./query/query_${d}D.txt
#oFolder=./result/result_${datatype}_${d}D_${cardinality}
#  ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip sleep 2
#datatype=correlated
#cardinality=2000000
#d=3
#qn=1000
## ------------------------------------------------------------------------------
##     Ground-Truth
## ------------------------------------------------------------------------------
#dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt
#tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth
#qPath=./query/query_${d}D.txt
#oFolder=./result/result_${datatype}_${d}D_${cardinality}
#  ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip sleep 2
#datatype=random
#cardinality=2000000
#d=3
#qn=1000
## ------------------------------------------------------------------------------
##     Ground-Truth
## ------------------------------------------------------------------------------
#dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt
#tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth
#qPath=./query/query_${d}D.txt
#oFolder=./result/result_${datatype}_${d}D_${cardinality}
#  ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip sleep 2
#datatype=anti_correlated
#cardinality=500000
#d=4
#qn=1000
## ------------------------------------------------------------------------------
##     Ground-Truth
## ------------------------------------------------------------------------------
#dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt
#tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth
#qPath=./query/query_${d}D.txt
#oFolder=./result/result_${datatype}_${d}D_${cardinality}
#  ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip sleep 2
#datatype=correlated
#cardinality=500000
#d=4
#qn=1000
## ------------------------------------------------------------------------------
##     Ground-Truth
## ------------------------------------------------------------------------------
#dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt
#tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth
#qPath=./query/query_${d}D.txt
#oFolder=./result/result_${datatype}_${d}D_${cardinality}
#  ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip sleep 2
#datatype=random
#cardinality=500000
#d=4
#qn=1000
## ------------------------------------------------------------------------------
##     Ground-Truth
## ------------------------------------------------------------------------------
#dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt
#tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth
#qPath=./query/query_${d}D.txt
#oFolder=./result/result_${datatype}_${d}D_${cardinality}
#  ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip sleep 2
#datatype=anti_correlated
#cardinality=1000000
#d=4
#qn=1000
## ------------------------------------------------------------------------------
##     Ground-Truth
## ------------------------------------------------------------------------------
#dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt
#tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth
#qPath=./query/query_${d}D.txt
#oFolder=./result/result_${datatype}_${d}D_${cardinality}
#  ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip sleep 2
#datatype=correlated
#cardinality=1000000
#d=4
#qn=1000
## ------------------------------------------------------------------------------
##     Ground-Truth
## ------------------------------------------------------------------------------
#dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt
#tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth
#qPath=./query/query_${d}D.txt
#oFolder=./result/result_${datatype}_${d}D_${cardinality}
#  ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip sleep 2
#datatype=random
#cardinality=1000000
#d=4
#qn=1000
## ------------------------------------------------------------------------------
##     Ground-Truth
## ------------------------------------------------------------------------------
#dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt
#tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth
#qPath=./query/query_${d}D.txt
#oFolder=./result/result_${datatype}_${d}D_${cardinality}
#  ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip sleep 2
#datatype=anti_correlated
#cardinality=1500000
#d=4
#qn=1000
## ------------------------------------------------------------------------------
##     Ground-Truth
## ------------------------------------------------------------------------------
#dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt
#tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth
#qPath=./query/query_${d}D.txt
#oFolder=./result/result_${datatype}_${d}D_${cardinality}
#  ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip sleep 2
#datatype=correlated
#cardinality=1500000
#d=4
#qn=1000
## ------------------------------------------------------------------------------
##     Ground-Truth
## ------------------------------------------------------------------------------
#dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt
#tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth
#qPath=./query/query_${d}D.txt
#oFolder=./result/result_${datatype}_${d}D_${cardinality}
#  ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip sleep 2
#datatype=random
#cardinality=1500000
#d=4
#qn=1000
## ------------------------------------------------------------------------------
##     Ground-Truth
## ------------------------------------------------------------------------------
#dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt
#tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth
#qPath=./query/query_${d}D.txt
#oFolder=./result/result_${datatype}_${d}D_${cardinality}
#  ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip sleep 2
#datatype=anti_correlated
#cardinality=2000000
#d=4
#qn=1000
## ------------------------------------------------------------------------------
##     Ground-Truth
## ------------------------------------------------------------------------------
#dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt
#tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth
#qPath=./query/query_${d}D.txt
#oFolder=./result/result_${datatype}_${d}D_${cardinality}
#  ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip sleep 2
#datatype=correlated
#cardinality=2000000
#d=4
#qn=1000
## ------------------------------------------------------------------------------
##     Ground-Truth
## ------------------------------------------------------------------------------
#dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt
#tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth
#qPath=./query/query_${d}D.txt
#oFolder=./result/result_${datatype}_${d}D_${cardinality}
#  ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip sleep 2
#datatype=random
#cardinality=2000000
#d=4
#qn=1000
## ------------------------------------------------------------------------------
##     Ground-Truth
## ------------------------------------------------------------------------------
#dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt
#tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth
#qPath=./query/query_${d}D.txt
#oFolder=./result/result_${datatype}_${d}D_${cardinality}
#  ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip sleep 2
#datatype=anti_correlated
#cardinality=500000
#d=5
#qn=1000
## ------------------------------------------------------------------------------
##     Ground-Truth
## ------------------------------------------------------------------------------
#dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt
#tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth
#qPath=./query/query_${d}D.txt
#oFolder=./result/result_${datatype}_${d}D_${cardinality}
#  ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip sleep 2
#datatype=correlated
#cardinality=500000
#d=5
#qn=1000
## ------------------------------------------------------------------------------
##     Ground-Truth
## ------------------------------------------------------------------------------
#dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt
#tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth
#qPath=./query/query_${d}D.txt
#oFolder=./result/result_${datatype}_${d}D_${cardinality}
#  ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip sleep 2
#datatype=random
#cardinality=500000
#d=5
#qn=1000
## ------------------------------------------------------------------------------
##     Ground-Truth
## ------------------------------------------------------------------------------
#dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt
#tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth
#qPath=./query/query_${d}D.txt
#oFolder=./result/result_${datatype}_${d}D_${cardinality}
#  ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip sleep 2
#datatype=anti_correlated
#cardinality=1000000
#d=5
#qn=1000
## ------------------------------------------------------------------------------
##     Ground-Truth
## ------------------------------------------------------------------------------
#dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt
#tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth
#qPath=./query/query_${d}D.txt
#oFolder=./result/result_${datatype}_${d}D_${cardinality}
#  ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip sleep 2
#datatype=correlated
#cardinality=1000000
#d=5
#qn=1000
## ------------------------------------------------------------------------------
##     Ground-Truth
## ------------------------------------------------------------------------------
#dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt
#tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth
#qPath=./query/query_${d}D.txt
#oFolder=./result/result_${datatype}_${d}D_${cardinality}
#  ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip sleep 2
#datatype=random
#cardinality=1000000
#d=5
#qn=1000
## ------------------------------------------------------------------------------
##     Ground-Truth
## ------------------------------------------------------------------------------
#dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt
#tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth
#qPath=./query/query_${d}D.txt
#oFolder=./result/result_${datatype}_${d}D_${cardinality}
#  ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip sleep 2
#datatype=anti_correlated
#cardinality=1500000
#d=5
#qn=1000
## ------------------------------------------------------------------------------
##     Ground-Truth
## ------------------------------------------------------------------------------
#dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt
#tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth
#qPath=./query/query_${d}D.txt
#oFolder=./result/result_${datatype}_${d}D_${cardinality}
#  ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip sleep 2
#datatype=correlated
#cardinality=1500000
#d=5
#qn=1000
## ------------------------------------------------------------------------------
##     Ground-Truth
## ------------------------------------------------------------------------------
#dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt
#tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth
#qPath=./query/query_${d}D.txt
#oFolder=./result/result_${datatype}_${d}D_${cardinality}
#  ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip sleep 2
#datatype=random
#cardinality=1500000
#d=5
#qn=1000
## ------------------------------------------------------------------------------
##     Ground-Truth
## ------------------------------------------------------------------------------
#dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt
#tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth
#qPath=./query/query_${d}D.txt
#oFolder=./result/result_${datatype}_${d}D_${cardinality}
#  ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip sleep 2
#datatype=anti_correlated
#cardinality=2000000
#d=5
#qn=1000
## ------------------------------------------------------------------------------
##     Ground-Truth
## ------------------------------------------------------------------------------
#dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt
#tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth
#qPath=./query/query_${d}D.txt
#oFolder=./result/result_${datatype}_${d}D_${cardinality}
#  ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip sleep 2
#datatype=correlated
#cardinality=2000000
#d=5
#qn=1000
## ------------------------------------------------------------------------------
##     Ground-Truth
## ------------------------------------------------------------------------------
#dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt
#tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth
#qPath=./query/query_${d}D.txt
#oFolder=./result/result_${datatype}_${d}D_${cardinality}
#  ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip sleep 2
#datatype=random
#cardinality=2000000
#d=5
#qn=1000
## ------------------------------------------------------------------------------
##     Ground-Truth
## ------------------------------------------------------------------------------
#dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt
#tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth
#qPath=./query/query_${d}D.txt
#oFolder=./result/result_${datatype}_${d}D_${cardinality}
#  ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip sleep 2
#datatype=anti_correlated
#cardinality=500000
#d=6
#qn=1000
## ------------------------------------------------------------------------------
##     Ground-Truth
## ------------------------------------------------------------------------------
#dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt
#tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth
#qPath=./query/query_${d}D.txt
#oFolder=./result/result_${datatype}_${d}D_${cardinality}
#  ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip sleep 2
#datatype=correlated
#cardinality=500000
#d=6
#qn=1000
## ------------------------------------------------------------------------------
##     Ground-Truth
## ------------------------------------------------------------------------------
#dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt
#tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth
#qPath=./query/query_${d}D.txt
#oFolder=./result/result_${datatype}_${d}D_${cardinality}
#  ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip sleep 2
#datatype=random
#cardinality=500000
#d=6
#qn=1000
## ------------------------------------------------------------------------------
##     Ground-Truth
## ------------------------------------------------------------------------------
#dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt
#tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth
#qPath=./query/query_${d}D.txt
#oFolder=./result/result_${datatype}_${d}D_${cardinality}
#  ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip sleep 2
#datatype=anti_correlated
#cardinality=1000000
#d=6
#qn=1000
## ------------------------------------------------------------------------------
##     Ground-Truth
## ------------------------------------------------------------------------------
#dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt
#tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth
#qPath=./query/query_${d}D.txt
#oFolder=./result/result_${datatype}_${d}D_${cardinality}
#  ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip sleep 2
#datatype=correlated
#cardinality=1000000
#d=6
#qn=1000
## ------------------------------------------------------------------------------
##     Ground-Truth
## ------------------------------------------------------------------------------
#dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt
#tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth
#qPath=./query/query_${d}D.txt
#oFolder=./result/result_${datatype}_${d}D_${cardinality}
#  ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip sleep 2
#datatype=random
#cardinality=1000000
#d=6
#qn=1000
## ------------------------------------------------------------------------------
##     Ground-Truth
## ------------------------------------------------------------------------------
#dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt
#tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth
#qPath=./query/query_${d}D.txt
#oFolder=./result/result_${datatype}_${d}D_${cardinality}
#  ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip sleep 2
#datatype=anti_correlated
#cardinality=1500000
#d=6
#qn=1000
## ------------------------------------------------------------------------------
##     Ground-Truth
## ------------------------------------------------------------------------------
#dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt
#tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth
#qPath=./query/query_${d}D.txt
#oFolder=./result/result_${datatype}_${d}D_${cardinality}
#  ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip sleep 2
#datatype=correlated
#cardinality=1500000
#d=6
#qn=1000
## ------------------------------------------------------------------------------
##     Ground-Truth
## ------------------------------------------------------------------------------
#dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt
#tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth
#qPath=./query/query_${d}D.txt
#oFolder=./result/result_${datatype}_${d}D_${cardinality}
#  ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip sleep 2
#datatype=random
#cardinality=1500000
#d=6
#qn=1000
## ------------------------------------------------------------------------------
##     Ground-Truth
## ------------------------------------------------------------------------------
#dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt
#tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth
#qPath=./query/query_${d}D.txt
#oFolder=./result/result_${datatype}_${d}D_${cardinality}
#  ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip sleep 2
#datatype=anti_correlated
#cardinality=2000000
#d=6
#qn=1000
## ------------------------------------------------------------------------------
##     Ground-Truth
## ------------------------------------------------------------------------------
#dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt
#tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth
#qPath=./query/query_${d}D.txt
#oFolder=./result/result_${datatype}_${d}D_${cardinality}
#  ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip sleep 2
#datatype=correlated
#cardinality=2000000
#d=6
#qn=1000
## ------------------------------------------------------------------------------
##     Ground-Truth
## ------------------------------------------------------------------------------
#dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt
#tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth
#qPath=./query/query_${d}D.txt
#oFolder=./result/result_${datatype}_${d}D_${cardinality}
#  ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip sleep 2
#datatype=random
#cardinality=2000000
#d=6
#qn=1000
## ------------------------------------------------------------------------------
##     Ground-Truth
## ------------------------------------------------------------------------------
#dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt
#tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth
#qPath=./query/query_${d}D.txt
#oFolder=./result/result_${datatype}_${d}D_${cardinality}
#  ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip sleep 2
