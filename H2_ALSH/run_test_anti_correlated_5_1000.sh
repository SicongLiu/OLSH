#!/bin/bash 
# make
rm *.o 
datatype=anti_correlated
cardinality=1000
d=5
qn=2
c0=2
temporalResult=../H2_ALSH/qhull_data/run_test_anti_correlated_5_1000
overallResult=../H2_ALSH/qhull_data/overall_run_test_anti_correlated_5_1000.txt
S=0.9
num_layer=4
qPath=./query/query_${d}D.txt 
tsPath=./result/result_${d}D_${cardinality} # path for the ground truth

 
 
n0=312
K0=50
L0=1300
dPath0=./qhull_data/Synthetic/${datatype}_${d}_${cardinality}_qhull_layer_0
oFolder0=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}/result_${d}D0_${K0}_${L0}
./alsh -alg 10 -n ${n0} -qn ${qn} -d ${d} -K ${K0} -L ${L0} -S ${S} -c0 ${c0} -ds ${dPath0} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -of ${oFolder0}.simple_LSH

#n1=301
#K1=40
#L1=281
#dPath1=./qhull_data/Synthetic/${datatype}_${d}_${cardinality}_qhull_layer_1
#oFolder1=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}/result_${d}D1_${K1}_${L1}
#./alsh -alg 10 -n ${n1} -qn ${qn} -d ${d} -K ${K1} -L ${L1} -S ${S} -c0 ${c0} -ds ${dPath1} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -of ${oFolder1}.simple_LSH
#
#n2=209
#K2=40
#L2=387
#dPath2=./qhull_data/Synthetic/${datatype}_${d}_${cardinality}_qhull_layer_2
#oFolder2=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}/result_${d}D2_${K2}_${L2}
#./alsh -alg 10 -n ${n2} -qn ${qn} -d ${d} -K ${K2} -L ${L2} -S ${S} -c0 ${c0} -ds ${dPath2} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -of ${oFolder2}.simple_LSH
#
#n3=115
#K3=30
#L3=138
#dPath3=./qhull_data/Synthetic/${datatype}_${d}_${cardinality}_qhull_layer_3
#oFolder3=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}/result_${d}D3_${K3}_${L3}
#./alsh -alg 10 -n ${n3} -qn ${qn} -d ${d} -K ${K3} -L ${L3} -S ${S} -c0 ${c0} -ds ${dPath3} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -of ${oFolder3}.simple_LSH
#
#./alsh -alg 12 -d ${d} -qn ${qn} -L1 ${num_layer} -it ${temporalResult} -ts ${tsPath}.mip -of ${overallResult}
