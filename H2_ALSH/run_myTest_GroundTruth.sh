#!/bin/bash
# make
rm *.o

# ------------------------------------------------------------------------------
#  Parameters 5_D_anti_correlated
# ------------------------------------------------------------------------------
datatype=anti_correlated
cardinality=1000
d=5
qn=25

dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt

oFolder=./result/result_${datatype}_${d}D_${cardinality}


qPath=./query/query_${d}D.txt
tsPath=./result/result_${d}D # path for the ground truth
# ------------------------------------------------------------------------------
#  Ground-Truth
# ------------------------------------------------------------------------------
 ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} \
    -ts ${oFolder}.mip
