#!/bin/bash
# make
rm *.o

# ------------------------------------------------------------------------------
#  Parameters 5_D_anti_correlated
# ------------------------------------------------------------------------------
datatype=anti_correlated
cardinality=4000
d=5
qn=1
c0=2.0
S=0.9
n0=4000
K=50
L=865

dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt

oFolder=./result/${datatype}/result_${d}D0_${K}_${L}

qPath=./query/query_${d}D.txt
tsPath=./result/result_${d}D # path for the ground truth
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


./alsh -alg 10 -n ${n0} -qn ${qn} -d ${d} -K ${K} -L ${L} -S ${S} -c0 ${c0} -ds ${dPath} \
    -qs ${qPath} -ts ${tsPath}.mip -of ${oFolder}.simple_LSH
