#!/bin/bash
# make
rm *.o

# ------------------------------------------------------------------------------
#  Parameters
# ------------------------------------------------------------------------------
dname=Sift
n=312
d=5
datatype=anti_correlated
cardinality=1000


qn=1
K=50
m=3
U1=0.83
U2=0.85
c0=2.0
c=0.5
dPath=./data/${dname}/${dname}
oFolder=./results/${dname}/
dPath0=./qhull_data/Synthetic/${datatype}_${d}_${cardinality}_qhull_layer_0
oFolder0=./result/result_${d}D0

qPath=./query/query_${d}D.txt
tsPath=./result/result_${d}D # path for the ground truth
# ------------------------------------------------------------------------------
#  Ground-Truth
# ------------------------------------------------------------------------------
# ./alsh -alg 0 -n ${n} -qn ${qn} -d ${d} -ds ${dPath}.ds -qs ${dPath}.q \
#     -ts ${dPath}.mip

# ------------------------------------------------------------------------------
#  Algorithms for c-k-AMIP search
# ------------------------------------------------------------------------------
# ./alsh -alg 1 -n ${n} -qn ${qn} -d ${d} -c0 ${c0} -c ${c} -ds ${dPath}.ds \
#     -qs ${qPath} -ts ${tsPath}.mip -of ${oFolder}

# ------------------------------------------------------------------------------
#  Precision-Recall Curves of Algorithms for c-k-AMIP search
# ------------------------------------------------------------------------------
./alsh -alg 8 -n ${n} -qn ${qn} -d ${d} -c0 ${c0} -c ${c} -ds ${dPath0} \
    -qs ${qPath} -ts ${tsPath}.mip -of ${oFolder}
