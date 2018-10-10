#!/bin/bash 
# make 
rm *.o 
datatype=anti_correlated
cardinality=100000
d=5
qn=1000
c0=2
temporalResult=./temp_result_11/run_test_${datatype}_${d}_${cardinality}
overallResult=./temp_result_11/overall_run_test_${datatype}_${d}_${cardinality}.txt
S=0.9
num_layer=25
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
n0=2153
K0=12
L0=11
dPath0=./qhull_data/Synthetic/${datatype}_${d}_${cardinality}_qhull_layer_0
oFolder0=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}/result_${d}D0_${K0}_${L0}
./alsh -alg 10 -n ${n0} -qn ${qn} -d ${d} -K ${K0} -L ${L0} -LI 1 -S ${S} -c0 ${c0} -ds ${dPath0} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -of ${oFolder0}.simple_LSH 

n1=4106
K1=13
L1=6
dPath1=./qhull_data/Synthetic/${datatype}_${d}_${cardinality}_qhull_layer_1
oFolder1=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}/result_${d}D1_${K1}_${L1}
./alsh -alg 10 -n ${n1} -qn ${qn} -d ${d} -K ${K1} -L ${L1} -LI 2 -S ${S} -c0 ${c0} -ds ${dPath1} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -of ${oFolder1}.simple_LSH 

n2=5277
K2=13
L2=5
dPath2=./qhull_data/Synthetic/${datatype}_${d}_${cardinality}_qhull_layer_2
oFolder2=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}/result_${d}D2_${K2}_${L2}
./alsh -alg 10 -n ${n2} -qn ${qn} -d ${d} -K ${K2} -L ${L2} -LI 3 -S ${S} -c0 ${c0} -ds ${dPath2} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -of ${oFolder2}.simple_LSH 

n3=6168
K3=13
L3=4
dPath3=./qhull_data/Synthetic/${datatype}_${d}_${cardinality}_qhull_layer_3
oFolder3=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}/result_${d}D3_${K3}_${L3}
./alsh -alg 10 -n ${n3} -qn ${qn} -d ${d} -K ${K3} -L ${L3} -LI 4 -S ${S} -c0 ${c0} -ds ${dPath3} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -of ${oFolder3}.simple_LSH 

n4=6618
K4=13
L4=4
dPath4=./qhull_data/Synthetic/${datatype}_${d}_${cardinality}_qhull_layer_4
oFolder4=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}/result_${d}D4_${K4}_${L4}
./alsh -alg 10 -n ${n4} -qn ${qn} -d ${d} -K ${K4} -L ${L4} -LI 5 -S ${S} -c0 ${c0} -ds ${dPath4} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -of ${oFolder4}.simple_LSH 

n5=6769
K5=13
L5=4
dPath5=./qhull_data/Synthetic/${datatype}_${d}_${cardinality}_qhull_layer_5
oFolder5=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}/result_${d}D5_${K5}_${L5}
./alsh -alg 10 -n ${n5} -qn ${qn} -d ${d} -K ${K5} -L ${L5} -LI 6 -S ${S} -c0 ${c0} -ds ${dPath5} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -of ${oFolder5}.simple_LSH 

n6=6666
K6=13
L6=4
dPath6=./qhull_data/Synthetic/${datatype}_${d}_${cardinality}_qhull_layer_6
oFolder6=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}/result_${d}D6_${K6}_${L6}
./alsh -alg 10 -n ${n6} -qn ${qn} -d ${d} -K ${K6} -L ${L6} -LI 7 -S ${S} -c0 ${c0} -ds ${dPath6} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -of ${oFolder6}.simple_LSH 

n7=6647
K7=13
L7=4
dPath7=./qhull_data/Synthetic/${datatype}_${d}_${cardinality}_qhull_layer_7
oFolder7=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}/result_${d}D7_${K7}_${L7}
./alsh -alg 10 -n ${n7} -qn ${qn} -d ${d} -K ${K7} -L ${L7} -LI 8 -S ${S} -c0 ${c0} -ds ${dPath7} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -of ${oFolder7}.simple_LSH 

n8=6390
K8=13
L8=4
dPath8=./qhull_data/Synthetic/${datatype}_${d}_${cardinality}_qhull_layer_8
oFolder8=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}/result_${d}D8_${K8}_${L8}
./alsh -alg 10 -n ${n8} -qn ${qn} -d ${d} -K ${K8} -L ${L8} -LI 9 -S ${S} -c0 ${c0} -ds ${dPath8} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -of ${oFolder8}.simple_LSH 

n9=6097
K9=13
L9=4
dPath9=./qhull_data/Synthetic/${datatype}_${d}_${cardinality}_qhull_layer_9
oFolder9=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}/result_${d}D9_${K9}_${L9}
./alsh -alg 10 -n ${n9} -qn ${qn} -d ${d} -K ${K9} -L ${L9} -LI 10 -S ${S} -c0 ${c0} -ds ${dPath9} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -of ${oFolder9}.simple_LSH 

n10=5764
K10=13
L10=4
dPath10=./qhull_data/Synthetic/${datatype}_${d}_${cardinality}_qhull_layer_10
oFolder10=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}/result_${d}D10_${K10}_${L10}
./alsh -alg 10 -n ${n10} -qn ${qn} -d ${d} -K ${K10} -L ${L10} -LI 11 -S ${S} -c0 ${c0} -ds ${dPath10} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -of ${oFolder10}.simple_LSH 

n11=5352
K11=13
L11=5
dPath11=./qhull_data/Synthetic/${datatype}_${d}_${cardinality}_qhull_layer_11
oFolder11=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}/result_${d}D11_${K11}_${L11}
./alsh -alg 10 -n ${n11} -qn ${qn} -d ${d} -K ${K11} -L ${L11} -LI 12 -S ${S} -c0 ${c0} -ds ${dPath11} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -of ${oFolder11}.simple_LSH 

n12=4884
K12=13
L12=5
dPath12=./qhull_data/Synthetic/${datatype}_${d}_${cardinality}_qhull_layer_12
oFolder12=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}/result_${d}D12_${K12}_${L12}
./alsh -alg 10 -n ${n12} -qn ${qn} -d ${d} -K ${K12} -L ${L12} -LI 13 -S ${S} -c0 ${c0} -ds ${dPath12} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -of ${oFolder12}.simple_LSH 

n13=4408
K13=13
L13=6
dPath13=./qhull_data/Synthetic/${datatype}_${d}_${cardinality}_qhull_layer_13
oFolder13=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}/result_${d}D13_${K13}_${L13}
./alsh -alg 10 -n ${n13} -qn ${qn} -d ${d} -K ${K13} -L ${L13} -LI 14 -S ${S} -c0 ${c0} -ds ${dPath13} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -of ${oFolder13}.simple_LSH 

n14=4036
K14=12
L14=6
dPath14=./qhull_data/Synthetic/${datatype}_${d}_${cardinality}_qhull_layer_14
oFolder14=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}/result_${d}D14_${K14}_${L14}
./alsh -alg 10 -n ${n14} -qn ${qn} -d ${d} -K ${K14} -L ${L14} -LI 15 -S ${S} -c0 ${c0} -ds ${dPath14} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -of ${oFolder14}.simple_LSH 

n15=3517
K15=12
L15=7
dPath15=./qhull_data/Synthetic/${datatype}_${d}_${cardinality}_qhull_layer_15
oFolder15=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}/result_${d}D15_${K15}_${L15}
./alsh -alg 10 -n ${n15} -qn ${qn} -d ${d} -K ${K15} -L ${L15} -LI 16 -S ${S} -c0 ${c0} -ds ${dPath15} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -of ${oFolder15}.simple_LSH 

n16=3128
K16=12
L16=8
dPath16=./qhull_data/Synthetic/${datatype}_${d}_${cardinality}_qhull_layer_16
oFolder16=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}/result_${d}D16_${K16}_${L16}
./alsh -alg 10 -n ${n16} -qn ${qn} -d ${d} -K ${K16} -L ${L16} -LI 17 -S ${S} -c0 ${c0} -ds ${dPath16} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -of ${oFolder16}.simple_LSH 

n17=2707
K17=12
L17=9
dPath17=./qhull_data/Synthetic/${datatype}_${d}_${cardinality}_qhull_layer_17
oFolder17=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}/result_${d}D17_${K17}_${L17}
./alsh -alg 10 -n ${n17} -qn ${qn} -d ${d} -K ${K17} -L ${L17} -LI 18 -S ${S} -c0 ${c0} -ds ${dPath17} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -of ${oFolder17}.simple_LSH 

n18=2243
K18=12
L18=11
dPath18=./qhull_data/Synthetic/${datatype}_${d}_${cardinality}_qhull_layer_18
oFolder18=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}/result_${d}D18_${K18}_${L18}
./alsh -alg 10 -n ${n18} -qn ${qn} -d ${d} -K ${K18} -L ${L18} -LI 19 -S ${S} -c0 ${c0} -ds ${dPath18} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -of ${oFolder18}.simple_LSH 

n19=1880
K19=11
L19=13
dPath19=./qhull_data/Synthetic/${datatype}_${d}_${cardinality}_qhull_layer_19
oFolder19=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}/result_${d}D19_${K19}_${L19}
./alsh -alg 10 -n ${n19} -qn ${qn} -d ${d} -K ${K19} -L ${L19} -LI 20 -S ${S} -c0 ${c0} -ds ${dPath19} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -of ${oFolder19}.simple_LSH 

n20=1492
K20=11
L20=16
dPath20=./qhull_data/Synthetic/${datatype}_${d}_${cardinality}_qhull_layer_20
oFolder20=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}/result_${d}D20_${K20}_${L20}
./alsh -alg 10 -n ${n20} -qn ${qn} -d ${d} -K ${K20} -L ${L20} -LI 21 -S ${S} -c0 ${c0} -ds ${dPath20} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -of ${oFolder20}.simple_LSH 

n21=1210
K21=11
L21=19
dPath21=./qhull_data/Synthetic/${datatype}_${d}_${cardinality}_qhull_layer_21
oFolder21=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}/result_${d}D21_${K21}_${L21}
./alsh -alg 10 -n ${n21} -qn ${qn} -d ${d} -K ${K21} -L ${L21} -LI 22 -S ${S} -c0 ${c0} -ds ${dPath21} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -of ${oFolder21}.simple_LSH 

n22=916
K22=10
L22=25
dPath22=./qhull_data/Synthetic/${datatype}_${d}_${cardinality}_qhull_layer_22
oFolder22=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}/result_${d}D22_${K22}_${L22}
./alsh -alg 10 -n ${n22} -qn ${qn} -d ${d} -K ${K22} -L ${L22} -LI 23 -S ${S} -c0 ${c0} -ds ${dPath22} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -of ${oFolder22}.simple_LSH 

n23=678
K23=10
L23=34
dPath23=./qhull_data/Synthetic/${datatype}_${d}_${cardinality}_qhull_layer_23
oFolder23=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}/result_${d}D23_${K23}_${L23}
./alsh -alg 10 -n ${n23} -qn ${qn} -d ${d} -K ${K23} -L ${L23} -LI 24 -S ${S} -c0 ${c0} -ds ${dPath23} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -of ${oFolder23}.simple_LSH 

n24=432
K24=9
L24=53
dPath24=./qhull_data/Synthetic/${datatype}_${d}_${cardinality}_qhull_layer_24
oFolder24=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}/result_${d}D24_${K24}_${L24}
./alsh -alg 10 -n ${n24} -qn ${qn} -d ${d} -K ${K24} -L ${L24} -LI 25 -S ${S} -c0 ${c0} -ds ${dPath24} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -of ${oFolder24}.simple_LSH 

# ------------------------------------------------------------------------------ 
#     Overall-Performance 
# ------------------------------------------------------------------------------ 
./alsh -alg 12 -d ${d} -qn ${qn} -L1 ${num_layer} -it ${temporalResult} -ts ${tsPath}.mip -of ${overallResult} 
