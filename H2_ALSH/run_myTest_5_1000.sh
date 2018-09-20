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
c0=2.0
S=0.9

n0=312
n1=301
n2=209
n3=115
# n4=53
# n5=10

K0=50
K1=40
K2=40
K3=30
# K4=4

# K0=512
# K1=512
# K2=512
# K3=512

L0=480
L1=600
L2=600
L3=799
# L4=6



dPath0=./qhull_data/Synthetic/${datatype}_${d}_${cardinality}_qhull_layer_0
dPath1=./qhull_data/Synthetic/${datatype}_${d}_${cardinality}_qhull_layer_1
dPath2=./qhull_data/Synthetic/${datatype}_${d}_${cardinality}_qhull_layer_2
dPath3=./qhull_data/Synthetic/${datatype}_${d}_${cardinality}_qhull_layer_3
# dPath4=./qhull_data/Synthetic/${datatype}_${d}_${cardinality}_qhull_layer_4
# dPath5=./qhull_data/Synthetic/anti_correlated_5_1000_qhull_layer_5

oFolder0=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}/result_${d}D0_${K0}_${L0}
oFolder1=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}/result_${d}D1_${K1}_${L1}
oFolder2=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}/result_${d}D2_${K2}_${L2}
oFolder3=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}/result_${d}D3_${K3}_${L3}
# oFolder4=./result/result_${d}D4
# oFolder5=./result/result_5D5

qPath=./query/query_${d}D.txt
tsPath=./result/result_${datatype}_${d}D # path for the ground truth
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


./alsh -alg 10 -n ${n0} -qn ${qn} -d ${d} -K ${K0} -L ${L0} -S ${S} -c0 ${c0} -ds ${dPath0} \
    -qs ${qPath} -ts ${tsPath}.mip -of ${oFolder0}.simple_LSH

./alsh -alg 10 -n ${n1} -qn ${qn} -d ${d} -K ${K1} -L ${L1} -S ${S} -c0 ${c0} -ds ${dPath1} \
    -qs ${qPath} -ts ${tsPath}.mip -of ${oFolder1}.simple_LSH


./alsh -alg 10 -n ${n2} -qn ${qn} -d ${d} -K ${K2} -L ${L2} -S ${S} -c0 ${c0} -ds ${dPath2} \
    -qs ${qPath} -ts ${tsPath}.mip -of ${oFolder2}.simple_LSH


./alsh -alg 10 -n ${n3} -qn ${qn} -d ${d} -K ${K3} -L ${L3} -S ${S} -c0 ${c0} -ds ${dPath3} \
    -qs ${qPath} -ts ${tsPath}.mip -of ${oFolder3}.simple_LSH

# ./alsh -alg 10 -n ${n4} -qn ${qn} -d ${d} -K ${K} -L ${L} -c0 ${c0} -ds ${dPath4} \
#     -qs ${qPath} -ts ${tsPath}.mip -of ${oFolder4}.simple_LSH



# ./alsh -alg 10 -n ${n5} -qn ${qn} -d ${d} -K ${K} -L ${L} -c0 ${c0} -ds ${dPath5} \
#     -qs ${qPath} -ts ${tsPath}.mip -of ${oFolder5}.simple_LSH


-alg 12 -d 5 -qn 25 -L1 ${} -it ../H2_ALSH/qhull_data/run_test_anti_correlated_5_1000 -ts ./result/result_anti_correlated_5D_1000.mip -of ../H2_ALSH/qhull_data/overall_run_test_anti_correlated_5_1000.txt




