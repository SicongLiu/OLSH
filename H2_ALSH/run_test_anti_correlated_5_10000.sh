#!/bin/bash 
# make 
rm *.o 
datatype=anti_correlated
cardinality=10000
d=5
qn=20
c0=2
temporalResult=../H2_ALSH/qhull_data/Mathematica/run_test_anti_correlated_5_10000
overallResult=../H2_ALSH/qhull_data/Mathematica/overall_run_test_anti_correlated_5_10000.txt
S=0.9
num_layer=10
# ------------------------------------------------------------------------------ 
#     Ground-Truth 
# ------------------------------------------------------------------------------ 
dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt 
tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth 
qPath=./query/query_${d}D.txt 
oFolder=./result/result_${datatype}_${d}D_${cardinality} 
./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip 

 
 
# ------------------------------------------------------------------------------ 
#     Layer-Performance 
# ------------------------------------------------------------------------------ 
n0=878
K0=90
L0=13
dPath0=./qhull_data/Synthetic/${datatype}_${d}_${cardinality}_qhull_layer_0
oFolder0=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}/result_${d}D0_${K0}_${L0}
./alsh -alg 10 -n ${n0} -qn ${qn} -d ${d} -K ${K0} -L ${L0} -S ${S} -c0 ${c0} -ds ${dPath0} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -of ${oFolder0}.simple_LSH 

n1=1296
K1=80
L1=1
dPath1=./qhull_data/Synthetic/${datatype}_${d}_${cardinality}_qhull_layer_1
oFolder1=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}/result_${d}D1_${K1}_${L1}
./alsh -alg 10 -n ${n1} -qn ${qn} -d ${d} -K ${K1} -L ${L1} -S ${S} -c0 ${c0} -ds ${dPath1} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -of ${oFolder1}.simple_LSH 

n2=1416
K2=70
L2=47
dPath2=./qhull_data/Synthetic/${datatype}_${d}_${cardinality}_qhull_layer_2
oFolder2=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}/result_${d}D2_${K2}_${L2}
./alsh -alg 10 -n ${n2} -qn ${qn} -d ${d} -K ${K2} -L ${L2} -S ${S} -c0 ${c0} -ds ${dPath2} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -of ${oFolder2}.simple_LSH 

n3=1389
K3=60
L3=229
dPath3=./qhull_data/Synthetic/${datatype}_${d}_${cardinality}_qhull_layer_3
oFolder3=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}/result_${d}D3_${K3}_${L3}
./alsh -alg 10 -n ${n3} -qn ${qn} -d ${d} -K ${K3} -L ${L3} -S ${S} -c0 ${c0} -ds ${dPath3} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -of ${oFolder3}.simple_LSH 

n4=1282
K4=50
L4=261
dPath4=./qhull_data/Synthetic/${datatype}_${d}_${cardinality}_qhull_layer_4
oFolder4=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}/result_${d}D4_${K4}_${L4}
./alsh -alg 10 -n ${n4} -qn ${qn} -d ${d} -K ${K4} -L ${L4} -S ${S} -c0 ${c0} -ds ${dPath4} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -of ${oFolder4}.simple_LSH 

n5=1092
K5=40
L5=238
dPath5=./qhull_data/Synthetic/${datatype}_${d}_${cardinality}_qhull_layer_5
oFolder5=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}/result_${d}D5_${K5}_${L5}
./alsh -alg 10 -n ${n5} -qn ${qn} -d ${d} -K ${K5} -L ${L5} -S ${S} -c0 ${c0} -ds ${dPath5} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -of ${oFolder5}.simple_LSH 

n6=872
K6=30
L6=140
dPath6=./qhull_data/Synthetic/${datatype}_${d}_${cardinality}_qhull_layer_6
oFolder6=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}/result_${d}D6_${K6}_${L6}
./alsh -alg 10 -n ${n6} -qn ${qn} -d ${d} -K ${K6} -L ${L6} -S ${S} -c0 ${c0} -ds ${dPath6} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -of ${oFolder6}.simple_LSH 

n7=712
K7=20
L7=49
dPath7=./qhull_data/Synthetic/${datatype}_${d}_${cardinality}_qhull_layer_7
oFolder7=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}/result_${d}D7_${K7}_${L7}
./alsh -alg 10 -n ${n7} -qn ${qn} -d ${d} -K ${K7} -L ${L7} -S ${S} -c0 ${c0} -ds ${dPath7} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -of ${oFolder7}.simple_LSH 

n8=473
K8=10
L8=27
dPath8=./qhull_data/Synthetic/${datatype}_${d}_${cardinality}_qhull_layer_8
oFolder8=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}/result_${d}D8_${K8}_${L8}
./alsh -alg 10 -n ${n8} -qn ${qn} -d ${d} -K ${K8} -L ${L8} -S ${S} -c0 ${c0} -ds ${dPath8} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -of ${oFolder8}.simple_LSH 

n9=311
K9=10
L9=9
dPath9=./qhull_data/Synthetic/${datatype}_${d}_${cardinality}_qhull_layer_9
oFolder9=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}/result_${d}D9_${K9}_${L9}
./alsh -alg 10 -n ${n9} -qn ${qn} -d ${d} -K ${K9} -L ${L9} -S ${S} -c0 ${c0} -ds ${dPath9} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -of ${oFolder9}.simple_LSH 

# ------------------------------------------------------------------------------ 
#     Overall-Performance 
# ------------------------------------------------------------------------------ 
./alsh -alg 12 -d ${d} -qn ${qn} -L1 ${num_layer} -it ${temporalResult} -ts ${tsPath}.mip -of ${overallResult} 