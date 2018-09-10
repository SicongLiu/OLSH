#!/bin/bash
make
rm *.o

# ------------------------------------------------------------------------------
#  Parameters
# ------------------------------------------------------------------------------
n=312
d=5

qn=1
K=4
L=6
c0=2.0
dPath=./qhull_data/Synthetic/anti_correlated_5_1000_qhull_layer_0
qPath=./query/query_5D.txt
oFolder=./result/result_5D

# ------------------------------------------------------------------------------
#  Ground-Truth
# ------------------------------------------------------------------------------
# ./alsh -alg 0 -n ${n} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} \
#    -ts ${oFolder}.mip


# ------------------------------------------------------------------------------
#  Precision-Recall Curves of Algorithms for c-k-AMIP search
# ------------------------------------------------------------------------------
# ./alsh -alg 8 -n ${n} -qn ${qn} -d ${d} -c0 ${c0} -c ${c} -ds ${dPath}.ds \
#     -qs ${dPath}.q -ts ${dPath}.mip -of ${oFolder}

# ./alsh -alg 9 -n ${n} -qn ${qn} -d ${d} -K ${K} -m ${m} -U ${U2} -c0 ${c0} \
#     -ds ${dPath}.ds -qs ${dPath}.q -ts ${dPath}.mip -of ${oFolder}

./alsh -alg 10 -n ${n} -qn ${qn} -d ${d} -K ${K} -L ${L} -c0 ${c0} -ds ${dPath} \
    -qs ${qPath} -ts ${oFolder}.mip -of ${oFolder}.simple_LSH
