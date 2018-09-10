#!/bin/bash
# make
rm *.o

# ------------------------------------------------------------------------------
#  Parameters
# ------------------------------------------------------------------------------
d=5
n0=312
n1=301
n2=209
n3=115
n4=53
n5=10

qn=1
K=4
L=6
c0=2.0
dPath0=./qhull_data/Synthetic/anti_correlated_5_1000_qhull_layer_0
dPath1=./qhull_data/Synthetic/anti_correlated_5_1000_qhull_layer_1
dPath2=./qhull_data/Synthetic/anti_correlated_5_1000_qhull_layer_2
dPath3=./qhull_data/Synthetic/anti_correlated_5_1000_qhull_layer_3
dPath4=./qhull_data/Synthetic/anti_correlated_5_1000_qhull_layer_4
dPath5=./qhull_data/Synthetic/anti_correlated_5_1000_qhull_layer_5


oFolder0=./result/result_5D0
oFolder1=./result/result_5D1
oFolder2=./result/result_5D2
oFolder3=./result/result_5D3
oFolder4=./result/result_5D4
oFolder5=./result/result_5D5


qPath=./query/query_5D.txt
tsPath=./result/result_5D
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



./alsh -alg 10 -n ${n0} -qn ${qn} -d ${d} -K ${K} -L ${L} -c0 ${c0} -ds ${dPath0} \
    -qs ${qPath} -ts ${tsPath}.mip -of ${oFolder0}.simple_LSH

./alsh -alg 10 -n ${n1} -qn ${qn} -d ${d} -K ${K} -L ${L} -c0 ${c0} -ds ${dPath1} \
    -qs ${qPath} -ts ${tsPath}.mip -of ${oFolder1}.simple_LSH


./alsh -alg 10 -n ${n2} -qn ${qn} -d ${d} -K ${K} -L ${L} -c0 ${c0} -ds ${dPath2} \
    -qs ${qPath} -ts ${tsPath}.mip -of ${oFolder2}.simple_LSH



./alsh -alg 10 -n ${n3} -qn ${qn} -d ${d} -K ${K} -L ${L} -c0 ${c0} -ds ${dPath3} \
    -qs ${qPath} -ts ${tsPath}.mip -of ${oFolder3}.simple_LSH



./alsh -alg 10 -n ${n4} -qn ${qn} -d ${d} -K ${K} -L ${L} -c0 ${c0} -ds ${dPath4} \
    -qs ${qPath} -ts ${tsPath}.mip -of ${oFolder4}.simple_LSH



./alsh -alg 10 -n ${n5} -qn ${qn} -d ${d} -K ${K} -L ${L} -c0 ${c0} -ds ${dPath5} \
    -qs ${qPath} -ts ${tsPath}.mip -of ${oFolder5}.simple_LSH










