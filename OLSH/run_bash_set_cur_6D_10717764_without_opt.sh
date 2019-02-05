#!/bin/bash 
datatype=HOUSE
cardinality=10717764
d=6
qn=1000
c0=2
pot=0
temporalResult=./temp_result_6D_top25_log_10717764/run_test_${datatype}_${d}_${cardinality}_opt
overallResult=./temp_result_6D_top25_log_10717764/overall_run_test_${datatype}_${d}_${cardinality}_opt
sim_angle=./temp_result_6D_top25_log_10717764/sim_angle_${datatype}_${d}_${cardinality}_opt
S=0.75
num_layer=6
top_k=25
# ------------------------------------------------------------------------------ 
#     Ground-Truth 
# ------------------------------------------------------------------------------ 
dPath=./raw_data/${datatype}/${datatype}_${d}_${cardinality}.txt 
tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth 
qPath=./query/query_${datatype}.txt 
oFolder=./result/result_${datatype}_${d}D_${cardinality} 
 # ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip 
 # sleep 1 

 
 
# ------------------------------------------------------------------------------ 
#     Layer-Performance 
# ------------------------------------------------------------------------------ 
n0=2005
K0=11
L0=36
dPath0=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_0
oFolder0=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_opt/result_${d}D0_${K0}_${L0}
temp_hash0=./temp_result_6D_top25_log_10717764/hash_proj_${datatype}_opt_0
./alsh -alg 10 -n ${n0} -qn ${qn} -d ${d} -K ${K0} -L ${L0} -LI 1 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath0} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder0}.simple_LSH -hr ${temp_hash0} -pot ${pot} 

n1=4363
K1=13
L1=5
dPath1=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_1
oFolder1=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_opt/result_${d}D1_${K1}_${L1}
temp_hash1=./temp_result_6D_top25_log_10717764/hash_proj_${datatype}_opt_1
./alsh -alg 10 -n ${n1} -qn ${qn} -d ${d} -K ${K1} -L ${L1} -LI 2 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath1} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder1}.simple_LSH -hr ${temp_hash1} -pot ${pot} 

n2=6607
K2=13
L2=4
dPath2=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_2
oFolder2=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_opt/result_${d}D2_${K2}_${L2}
temp_hash2=./temp_result_6D_top25_log_10717764/hash_proj_${datatype}_opt_2
./alsh -alg 10 -n ${n2} -qn ${qn} -d ${d} -K ${K2} -L ${L2} -LI 3 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath2} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder2}.simple_LSH -hr ${temp_hash2} -pot ${pot} 

n3=8840
K3=14
L3=3
dPath3=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_3
oFolder3=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_opt/result_${d}D3_${K3}_${L3}
temp_hash3=./temp_result_6D_top25_log_10717764/hash_proj_${datatype}_opt_3
./alsh -alg 10 -n ${n3} -qn ${qn} -d ${d} -K ${K3} -L ${L3} -LI 4 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath3} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder3}.simple_LSH -hr ${temp_hash3} -pot ${pot} 

n4=10929
K4=14
L4=2
dPath4=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_4
oFolder4=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_opt/result_${d}D4_${K4}_${L4}
temp_hash4=./temp_result_6D_top25_log_10717764/hash_proj_${datatype}_opt_4
./alsh -alg 10 -n ${n4} -qn ${qn} -d ${d} -K ${K4} -L ${L4} -LI 5 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath4} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder4}.simple_LSH -hr ${temp_hash4} -pot ${pot} 

n5=13072
K5=14
L5=1
dPath5=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_5
oFolder5=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_opt/result_${d}D5_${K5}_${L5}
temp_hash5=./temp_result_6D_top25_log_10717764/hash_proj_${datatype}_opt_5
./alsh -alg 10 -n ${n5} -qn ${qn} -d ${d} -K ${K5} -L ${L5} -LI 6 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath5} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder5}.simple_LSH -hr ${temp_hash5} -pot ${pot} 

# ------------------------------------------------------------------------------ 
#     Overall-Performance 
# ------------------------------------------------------------------------------ 
./alsh -alg 12 -d ${d} -qn ${qn} -L1 ${num_layer} -tk ${top_k} -it ${temporalResult} -ts ${tsPath}.mip -of ${overallResult} 
 
 
sleep 2 
datatype=HOUSE
cardinality=10717764
d=6
qn=1000
c0=2
pot=0
temporalResult=./temp_result_6D_top25_log_10717764/run_test_${datatype}_${d}_${cardinality}_max
overallResult=./temp_result_6D_top25_log_10717764/overall_run_test_${datatype}_${d}_${cardinality}_max
sim_angle=./temp_result_6D_top25_log_10717764/sim_angle_${datatype}_${d}_${cardinality}_max
S=0.75
num_layer=6
top_k=25
# ------------------------------------------------------------------------------ 
#     Ground-Truth 
# ------------------------------------------------------------------------------ 
dPath=./raw_data/${datatype}/${datatype}_${d}_${cardinality}.txt 
tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth 
qPath=./query/query_${datatype}.txt 
oFolder=./result/result_${datatype}_${d}D_${cardinality} 
# ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip 

 
 
# ------------------------------------------------------------------------------ 
#     Layer-Performance 
# ------------------------------------------------------------------------------ 
n0=2005
K0=11
L0=15
dPath0=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_0
oFolder0=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_max/result_${d}D0_${K0}_${L0}
temp_hash0=./temp_result_6D_top25_log_10717764/hash_proj_${datatype}_max_0
./alsh -alg 10 -n ${n0} -qn ${qn} -d ${d} -K ${K0} -L ${L0} -LI 1 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath0} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder0}.simple_LSH -hr ${temp_hash0} -pot ${pot} 

n1=4363
K1=13
L1=7
dPath1=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_1
oFolder1=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_max/result_${d}D1_${K1}_${L1}
temp_hash1=./temp_result_6D_top25_log_10717764/hash_proj_${datatype}_max_1
./alsh -alg 10 -n ${n1} -qn ${qn} -d ${d} -K ${K1} -L ${L1} -LI 2 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath1} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder1}.simple_LSH -hr ${temp_hash1} -pot ${pot} 

n2=6607
K2=13
L2=5
dPath2=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_2
oFolder2=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_max/result_${d}D2_${K2}_${L2}
temp_hash2=./temp_result_6D_top25_log_10717764/hash_proj_${datatype}_max_2
./alsh -alg 10 -n ${n2} -qn ${qn} -d ${d} -K ${K2} -L ${L2} -LI 3 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath2} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder2}.simple_LSH -hr ${temp_hash2} -pot ${pot} 

n3=8840
K3=14
L3=3
dPath3=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_3
oFolder3=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_max/result_${d}D3_${K3}_${L3}
temp_hash3=./temp_result_6D_top25_log_10717764/hash_proj_${datatype}_max_3
./alsh -alg 10 -n ${n3} -qn ${qn} -d ${d} -K ${K3} -L ${L3} -LI 4 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath3} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder3}.simple_LSH -hr ${temp_hash3} -pot ${pot} 

n4=10929
K4=14
L4=3
dPath4=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_4
oFolder4=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_max/result_${d}D4_${K4}_${L4}
temp_hash4=./temp_result_6D_top25_log_10717764/hash_proj_${datatype}_max_4
./alsh -alg 10 -n ${n4} -qn ${qn} -d ${d} -K ${K4} -L ${L4} -LI 5 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath4} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder4}.simple_LSH -hr ${temp_hash4} -pot ${pot} 

n5=13072
K5=14
L5=2
dPath5=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_5
oFolder5=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_max/result_${d}D5_${K5}_${L5}
temp_hash5=./temp_result_6D_top25_log_10717764/hash_proj_${datatype}_max_5
./alsh -alg 10 -n ${n5} -qn ${qn} -d ${d} -K ${K5} -L ${L5} -LI 6 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath5} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder5}.simple_LSH -hr ${temp_hash5} -pot ${pot} 

# ------------------------------------------------------------------------------ 
#     Overall-Performance 
# ------------------------------------------------------------------------------ 
./alsh -alg 12 -d ${d} -qn ${qn} -L1 ${num_layer} -tk ${top_k} -it ${temporalResult} -ts ${tsPath}.mip -of ${overallResult} 
 
 
sleep 2 
datatype=HOUSE
cardinality=10717764
d=6
qn=1000
c0=2
pot=0
temporalResult=./temp_result_6D_top25_log_10717764/run_test_${datatype}_${d}_${cardinality}_uni
overallResult=./temp_result_6D_top25_log_10717764/overall_run_test_${datatype}_${d}_${cardinality}_uni
sim_angle=./temp_result_6D_top25_log_10717764/sim_angle_${datatype}_${d}_${cardinality}_uni
S=0.75
num_layer=6
top_k=25
# ------------------------------------------------------------------------------ 
#     Ground-Truth 
# ------------------------------------------------------------------------------ 
dPath=./raw_data/${datatype}/${datatype}_${d}_${cardinality}.txt 
tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth 
qPath=./query/query_${datatype}.txt 
oFolder=./result/result_${datatype}_${d}D_${cardinality} 
# ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip 

 
 
# ------------------------------------------------------------------------------ 
#     Layer-Performance 
# ------------------------------------------------------------------------------ 
n0=2005
K0=11
L0=15
dPath0=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_0
oFolder0=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_uni/result_${d}D0_${K0}_${L0}
temp_hash0=./temp_result_6D_top25_log_10717764/hash_proj_${datatype}_uni_0
./alsh -alg 10 -n ${n0} -qn ${qn} -d ${d} -K ${K0} -L ${L0} -LI 1 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath0} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder0}.simple_LSH -hr ${temp_hash0} -pot ${pot} 

n1=4363
K1=13
L1=7
dPath1=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_1
oFolder1=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_uni/result_${d}D1_${K1}_${L1}
temp_hash1=./temp_result_6D_top25_log_10717764/hash_proj_${datatype}_uni_1
./alsh -alg 10 -n ${n1} -qn ${qn} -d ${d} -K ${K1} -L ${L1} -LI 2 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath1} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder1}.simple_LSH -hr ${temp_hash1} -pot ${pot} 

n2=6607
K2=13
L2=5
dPath2=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_2
oFolder2=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_uni/result_${d}D2_${K2}_${L2}
temp_hash2=./temp_result_6D_top25_log_10717764/hash_proj_${datatype}_uni_2
./alsh -alg 10 -n ${n2} -qn ${qn} -d ${d} -K ${K2} -L ${L2} -LI 3 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath2} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder2}.simple_LSH -hr ${temp_hash2} -pot ${pot} 

n3=8840
K3=14
L3=3
dPath3=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_3
oFolder3=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_uni/result_${d}D3_${K3}_${L3}
temp_hash3=./temp_result_6D_top25_log_10717764/hash_proj_${datatype}_uni_3
./alsh -alg 10 -n ${n3} -qn ${qn} -d ${d} -K ${K3} -L ${L3} -LI 4 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath3} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder3}.simple_LSH -hr ${temp_hash3} -pot ${pot} 

n4=10929
K4=14
L4=3
dPath4=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_4
oFolder4=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_uni/result_${d}D4_${K4}_${L4}
temp_hash4=./temp_result_6D_top25_log_10717764/hash_proj_${datatype}_uni_4
./alsh -alg 10 -n ${n4} -qn ${qn} -d ${d} -K ${K4} -L ${L4} -LI 5 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath4} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder4}.simple_LSH -hr ${temp_hash4} -pot ${pot} 

n5=13072
K5=14
L5=2
dPath5=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_5
oFolder5=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_uni/result_${d}D5_${K5}_${L5}
temp_hash5=./temp_result_6D_top25_log_10717764/hash_proj_${datatype}_uni_5
./alsh -alg 10 -n ${n5} -qn ${qn} -d ${d} -K ${K5} -L ${L5} -LI 6 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath5} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder5}.simple_LSH -hr ${temp_hash5} -pot ${pot} 

# ------------------------------------------------------------------------------ 
#     Overall-Performance 
# ------------------------------------------------------------------------------ 
./alsh -alg 12 -d ${d} -qn ${qn} -L1 ${num_layer} -tk ${top_k} -it ${temporalResult} -ts ${tsPath}.mip -of ${overallResult} 
 
 
sleep 2 
datatype=HOUSE
cardinality=10717764
d=6
qn=1000
c0=2
pot=0
temporalResult=./temp_result_6D_top25_log_minus_10717764/run_test_${datatype}_${d}_${cardinality}_opt
overallResult=./temp_result_6D_top25_log_minus_10717764/overall_run_test_${datatype}_${d}_${cardinality}_opt
sim_angle=./temp_result_6D_top25_log_minus_10717764/sim_angle_${datatype}_${d}_${cardinality}_opt
S=0.75
num_layer=6
top_k=25
# ------------------------------------------------------------------------------ 
#     Ground-Truth 
# ------------------------------------------------------------------------------ 
dPath=./raw_data/${datatype}/${datatype}_${d}_${cardinality}.txt 
tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth 
qPath=./query/query_${datatype}.txt 
oFolder=./result/result_${datatype}_${d}D_${cardinality} 
 # ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip 
 # sleep 1 

 
 
# ------------------------------------------------------------------------------ 
#     Layer-Performance 
# ------------------------------------------------------------------------------ 
n0=2005
K0=8
L0=21
dPath0=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_0
oFolder0=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_opt/result_${d}D0_${K0}_${L0}
temp_hash0=./temp_result_6D_top25_log_minus_10717764/hash_proj_${datatype}_opt_0
./alsh -alg 10 -n ${n0} -qn ${qn} -d ${d} -K ${K0} -L ${L0} -LI 1 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath0} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder0}.simple_LSH -hr ${temp_hash0} -pot ${pot} 

n1=4363
K1=10
L1=12
dPath1=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_1
oFolder1=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_opt/result_${d}D1_${K1}_${L1}
temp_hash1=./temp_result_6D_top25_log_minus_10717764/hash_proj_${datatype}_opt_1
./alsh -alg 10 -n ${n1} -qn ${qn} -d ${d} -K ${K1} -L ${L1} -LI 2 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath1} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder1}.simple_LSH -hr ${temp_hash1} -pot ${pot} 

n2=6607
K2=10
L2=4
dPath2=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_2
oFolder2=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_opt/result_${d}D2_${K2}_${L2}
temp_hash2=./temp_result_6D_top25_log_minus_10717764/hash_proj_${datatype}_opt_2
./alsh -alg 10 -n ${n2} -qn ${qn} -d ${d} -K ${K2} -L ${L2} -LI 3 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath2} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder2}.simple_LSH -hr ${temp_hash2} -pot ${pot} 

n3=8840
K3=11
L3=3
dPath3=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_3
oFolder3=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_opt/result_${d}D3_${K3}_${L3}
temp_hash3=./temp_result_6D_top25_log_minus_10717764/hash_proj_${datatype}_opt_3
./alsh -alg 10 -n ${n3} -qn ${qn} -d ${d} -K ${K3} -L ${L3} -LI 4 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath3} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder3}.simple_LSH -hr ${temp_hash3} -pot ${pot} 

n4=10929
K4=11
L4=2
dPath4=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_4
oFolder4=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_opt/result_${d}D4_${K4}_${L4}
temp_hash4=./temp_result_6D_top25_log_minus_10717764/hash_proj_${datatype}_opt_4
./alsh -alg 10 -n ${n4} -qn ${qn} -d ${d} -K ${K4} -L ${L4} -LI 5 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath4} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder4}.simple_LSH -hr ${temp_hash4} -pot ${pot} 

n5=13072
K5=11
L5=1
dPath5=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_5
oFolder5=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_opt/result_${d}D5_${K5}_${L5}
temp_hash5=./temp_result_6D_top25_log_minus_10717764/hash_proj_${datatype}_opt_5
./alsh -alg 10 -n ${n5} -qn ${qn} -d ${d} -K ${K5} -L ${L5} -LI 6 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath5} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder5}.simple_LSH -hr ${temp_hash5} -pot ${pot} 

# ------------------------------------------------------------------------------ 
#     Overall-Performance 
# ------------------------------------------------------------------------------ 
./alsh -alg 12 -d ${d} -qn ${qn} -L1 ${num_layer} -tk ${top_k} -it ${temporalResult} -ts ${tsPath}.mip -of ${overallResult} 
 
 
sleep 2 
datatype=HOUSE
cardinality=10717764
d=6
qn=1000
c0=2
pot=0
temporalResult=./temp_result_6D_top25_log_minus_10717764/run_test_${datatype}_${d}_${cardinality}_max
overallResult=./temp_result_6D_top25_log_minus_10717764/overall_run_test_${datatype}_${d}_${cardinality}_max
sim_angle=./temp_result_6D_top25_log_minus_10717764/sim_angle_${datatype}_${d}_${cardinality}_max
S=0.75
num_layer=6
top_k=25
# ------------------------------------------------------------------------------ 
#     Ground-Truth 
# ------------------------------------------------------------------------------ 
dPath=./raw_data/${datatype}/${datatype}_${d}_${cardinality}.txt 
tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth 
qPath=./query/query_${datatype}.txt 
oFolder=./result/result_${datatype}_${d}D_${cardinality} 
# ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip 

 
 
# ------------------------------------------------------------------------------ 
#     Layer-Performance 
# ------------------------------------------------------------------------------ 
n0=2005
K0=8
L0=15
dPath0=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_0
oFolder0=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_max/result_${d}D0_${K0}_${L0}
temp_hash0=./temp_result_6D_top25_log_minus_10717764/hash_proj_${datatype}_max_0
./alsh -alg 10 -n ${n0} -qn ${qn} -d ${d} -K ${K0} -L ${L0} -LI 1 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath0} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder0}.simple_LSH -hr ${temp_hash0} -pot ${pot} 

n1=4363
K1=10
L1=7
dPath1=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_1
oFolder1=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_max/result_${d}D1_${K1}_${L1}
temp_hash1=./temp_result_6D_top25_log_minus_10717764/hash_proj_${datatype}_max_1
./alsh -alg 10 -n ${n1} -qn ${qn} -d ${d} -K ${K1} -L ${L1} -LI 2 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath1} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder1}.simple_LSH -hr ${temp_hash1} -pot ${pot} 

n2=6607
K2=10
L2=5
dPath2=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_2
oFolder2=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_max/result_${d}D2_${K2}_${L2}
temp_hash2=./temp_result_6D_top25_log_minus_10717764/hash_proj_${datatype}_max_2
./alsh -alg 10 -n ${n2} -qn ${qn} -d ${d} -K ${K2} -L ${L2} -LI 3 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath2} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder2}.simple_LSH -hr ${temp_hash2} -pot ${pot} 

n3=8840
K3=11
L3=3
dPath3=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_3
oFolder3=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_max/result_${d}D3_${K3}_${L3}
temp_hash3=./temp_result_6D_top25_log_minus_10717764/hash_proj_${datatype}_max_3
./alsh -alg 10 -n ${n3} -qn ${qn} -d ${d} -K ${K3} -L ${L3} -LI 4 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath3} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder3}.simple_LSH -hr ${temp_hash3} -pot ${pot} 

n4=10929
K4=11
L4=3
dPath4=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_4
oFolder4=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_max/result_${d}D4_${K4}_${L4}
temp_hash4=./temp_result_6D_top25_log_minus_10717764/hash_proj_${datatype}_max_4
./alsh -alg 10 -n ${n4} -qn ${qn} -d ${d} -K ${K4} -L ${L4} -LI 5 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath4} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder4}.simple_LSH -hr ${temp_hash4} -pot ${pot} 

n5=13072
K5=11
L5=2
dPath5=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_5
oFolder5=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_max/result_${d}D5_${K5}_${L5}
temp_hash5=./temp_result_6D_top25_log_minus_10717764/hash_proj_${datatype}_max_5
./alsh -alg 10 -n ${n5} -qn ${qn} -d ${d} -K ${K5} -L ${L5} -LI 6 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath5} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder5}.simple_LSH -hr ${temp_hash5} -pot ${pot} 

# ------------------------------------------------------------------------------ 
#     Overall-Performance 
# ------------------------------------------------------------------------------ 
./alsh -alg 12 -d ${d} -qn ${qn} -L1 ${num_layer} -tk ${top_k} -it ${temporalResult} -ts ${tsPath}.mip -of ${overallResult} 
 
 
sleep 2 
datatype=HOUSE
cardinality=10717764
d=6
qn=1000
c0=2
pot=0
temporalResult=./temp_result_6D_top25_log_minus_10717764/run_test_${datatype}_${d}_${cardinality}_uni
overallResult=./temp_result_6D_top25_log_minus_10717764/overall_run_test_${datatype}_${d}_${cardinality}_uni
sim_angle=./temp_result_6D_top25_log_minus_10717764/sim_angle_${datatype}_${d}_${cardinality}_uni
S=0.75
num_layer=6
top_k=25
# ------------------------------------------------------------------------------ 
#     Ground-Truth 
# ------------------------------------------------------------------------------ 
dPath=./raw_data/${datatype}/${datatype}_${d}_${cardinality}.txt 
tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth 
qPath=./query/query_${datatype}.txt 
oFolder=./result/result_${datatype}_${d}D_${cardinality} 
# ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip 

 
 
# ------------------------------------------------------------------------------ 
#     Layer-Performance 
# ------------------------------------------------------------------------------ 
n0=2005
K0=8
L0=15
dPath0=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_0
oFolder0=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_uni/result_${d}D0_${K0}_${L0}
temp_hash0=./temp_result_6D_top25_log_minus_10717764/hash_proj_${datatype}_uni_0
./alsh -alg 10 -n ${n0} -qn ${qn} -d ${d} -K ${K0} -L ${L0} -LI 1 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath0} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder0}.simple_LSH -hr ${temp_hash0} -pot ${pot} 

n1=4363
K1=10
L1=7
dPath1=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_1
oFolder1=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_uni/result_${d}D1_${K1}_${L1}
temp_hash1=./temp_result_6D_top25_log_minus_10717764/hash_proj_${datatype}_uni_1
./alsh -alg 10 -n ${n1} -qn ${qn} -d ${d} -K ${K1} -L ${L1} -LI 2 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath1} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder1}.simple_LSH -hr ${temp_hash1} -pot ${pot} 

n2=6607
K2=10
L2=5
dPath2=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_2
oFolder2=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_uni/result_${d}D2_${K2}_${L2}
temp_hash2=./temp_result_6D_top25_log_minus_10717764/hash_proj_${datatype}_uni_2
./alsh -alg 10 -n ${n2} -qn ${qn} -d ${d} -K ${K2} -L ${L2} -LI 3 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath2} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder2}.simple_LSH -hr ${temp_hash2} -pot ${pot} 

n3=8840
K3=11
L3=3
dPath3=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_3
oFolder3=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_uni/result_${d}D3_${K3}_${L3}
temp_hash3=./temp_result_6D_top25_log_minus_10717764/hash_proj_${datatype}_uni_3
./alsh -alg 10 -n ${n3} -qn ${qn} -d ${d} -K ${K3} -L ${L3} -LI 4 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath3} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder3}.simple_LSH -hr ${temp_hash3} -pot ${pot} 

n4=10929
K4=11
L4=3
dPath4=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_4
oFolder4=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_uni/result_${d}D4_${K4}_${L4}
temp_hash4=./temp_result_6D_top25_log_minus_10717764/hash_proj_${datatype}_uni_4
./alsh -alg 10 -n ${n4} -qn ${qn} -d ${d} -K ${K4} -L ${L4} -LI 5 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath4} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder4}.simple_LSH -hr ${temp_hash4} -pot ${pot} 

n5=13072
K5=11
L5=2
dPath5=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_5
oFolder5=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_uni/result_${d}D5_${K5}_${L5}
temp_hash5=./temp_result_6D_top25_log_minus_10717764/hash_proj_${datatype}_uni_5
./alsh -alg 10 -n ${n5} -qn ${qn} -d ${d} -K ${K5} -L ${L5} -LI 6 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath5} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder5}.simple_LSH -hr ${temp_hash5} -pot ${pot} 

# ------------------------------------------------------------------------------ 
#     Overall-Performance 
# ------------------------------------------------------------------------------ 
./alsh -alg 12 -d ${d} -qn ${qn} -L1 ${num_layer} -tk ${top_k} -it ${temporalResult} -ts ${tsPath}.mip -of ${overallResult} 
 
 
sleep 2 
datatype=HOUSE
cardinality=10717764
d=6
qn=1000
c0=2
pot=0
temporalResult=./temp_result_6D_top25_log_plus_10717764/run_test_${datatype}_${d}_${cardinality}_opt
overallResult=./temp_result_6D_top25_log_plus_10717764/overall_run_test_${datatype}_${d}_${cardinality}_opt
sim_angle=./temp_result_6D_top25_log_plus_10717764/sim_angle_${datatype}_${d}_${cardinality}_opt
S=0.75
num_layer=6
top_k=25
# ------------------------------------------------------------------------------ 
#     Ground-Truth 
# ------------------------------------------------------------------------------ 
dPath=./raw_data/${datatype}/${datatype}_${d}_${cardinality}.txt 
tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth 
qPath=./query/query_${datatype}.txt 
oFolder=./result/result_${datatype}_${d}D_${cardinality} 
 # ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip 
 # sleep 1 

 
 
# ------------------------------------------------------------------------------ 
#     Layer-Performance 
# ------------------------------------------------------------------------------ 
n0=2005
K0=14
L0=36
dPath0=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_0
oFolder0=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_opt/result_${d}D0_${K0}_${L0}
temp_hash0=./temp_result_6D_top25_log_plus_10717764/hash_proj_${datatype}_opt_0
./alsh -alg 10 -n ${n0} -qn ${qn} -d ${d} -K ${K0} -L ${L0} -LI 1 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath0} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder0}.simple_LSH -hr ${temp_hash0} -pot ${pot} 

n1=4363
K1=16
L1=5
dPath1=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_1
oFolder1=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_opt/result_${d}D1_${K1}_${L1}
temp_hash1=./temp_result_6D_top25_log_plus_10717764/hash_proj_${datatype}_opt_1
./alsh -alg 10 -n ${n1} -qn ${qn} -d ${d} -K ${K1} -L ${L1} -LI 2 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath1} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder1}.simple_LSH -hr ${temp_hash1} -pot ${pot} 

n2=6607
K2=16
L2=4
dPath2=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_2
oFolder2=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_opt/result_${d}D2_${K2}_${L2}
temp_hash2=./temp_result_6D_top25_log_plus_10717764/hash_proj_${datatype}_opt_2
./alsh -alg 10 -n ${n2} -qn ${qn} -d ${d} -K ${K2} -L ${L2} -LI 3 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath2} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder2}.simple_LSH -hr ${temp_hash2} -pot ${pot} 

n3=8840
K3=17
L3=3
dPath3=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_3
oFolder3=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_opt/result_${d}D3_${K3}_${L3}
temp_hash3=./temp_result_6D_top25_log_plus_10717764/hash_proj_${datatype}_opt_3
./alsh -alg 10 -n ${n3} -qn ${qn} -d ${d} -K ${K3} -L ${L3} -LI 4 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath3} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder3}.simple_LSH -hr ${temp_hash3} -pot ${pot} 

n4=10929
K4=17
L4=2
dPath4=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_4
oFolder4=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_opt/result_${d}D4_${K4}_${L4}
temp_hash4=./temp_result_6D_top25_log_plus_10717764/hash_proj_${datatype}_opt_4
./alsh -alg 10 -n ${n4} -qn ${qn} -d ${d} -K ${K4} -L ${L4} -LI 5 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath4} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder4}.simple_LSH -hr ${temp_hash4} -pot ${pot} 

n5=13072
K5=17
L5=1
dPath5=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_5
oFolder5=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_opt/result_${d}D5_${K5}_${L5}
temp_hash5=./temp_result_6D_top25_log_plus_10717764/hash_proj_${datatype}_opt_5
./alsh -alg 10 -n ${n5} -qn ${qn} -d ${d} -K ${K5} -L ${L5} -LI 6 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath5} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder5}.simple_LSH -hr ${temp_hash5} -pot ${pot} 

# ------------------------------------------------------------------------------ 
#     Overall-Performance 
# ------------------------------------------------------------------------------ 
./alsh -alg 12 -d ${d} -qn ${qn} -L1 ${num_layer} -tk ${top_k} -it ${temporalResult} -ts ${tsPath}.mip -of ${overallResult} 
 
 
sleep 2 
datatype=HOUSE
cardinality=10717764
d=6
qn=1000
c0=2
pot=0
temporalResult=./temp_result_6D_top25_log_plus_10717764/run_test_${datatype}_${d}_${cardinality}_max
overallResult=./temp_result_6D_top25_log_plus_10717764/overall_run_test_${datatype}_${d}_${cardinality}_max
sim_angle=./temp_result_6D_top25_log_plus_10717764/sim_angle_${datatype}_${d}_${cardinality}_max
S=0.75
num_layer=6
top_k=25
# ------------------------------------------------------------------------------ 
#     Ground-Truth 
# ------------------------------------------------------------------------------ 
dPath=./raw_data/${datatype}/${datatype}_${d}_${cardinality}.txt 
tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth 
qPath=./query/query_${datatype}.txt 
oFolder=./result/result_${datatype}_${d}D_${cardinality} 
# ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip 

 
 
# ------------------------------------------------------------------------------ 
#     Layer-Performance 
# ------------------------------------------------------------------------------ 
n0=2005
K0=14
L0=15
dPath0=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_0
oFolder0=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_max/result_${d}D0_${K0}_${L0}
temp_hash0=./temp_result_6D_top25_log_plus_10717764/hash_proj_${datatype}_max_0
./alsh -alg 10 -n ${n0} -qn ${qn} -d ${d} -K ${K0} -L ${L0} -LI 1 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath0} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder0}.simple_LSH -hr ${temp_hash0} -pot ${pot} 

n1=4363
K1=16
L1=7
dPath1=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_1
oFolder1=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_max/result_${d}D1_${K1}_${L1}
temp_hash1=./temp_result_6D_top25_log_plus_10717764/hash_proj_${datatype}_max_1
./alsh -alg 10 -n ${n1} -qn ${qn} -d ${d} -K ${K1} -L ${L1} -LI 2 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath1} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder1}.simple_LSH -hr ${temp_hash1} -pot ${pot} 

n2=6607
K2=16
L2=5
dPath2=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_2
oFolder2=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_max/result_${d}D2_${K2}_${L2}
temp_hash2=./temp_result_6D_top25_log_plus_10717764/hash_proj_${datatype}_max_2
./alsh -alg 10 -n ${n2} -qn ${qn} -d ${d} -K ${K2} -L ${L2} -LI 3 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath2} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder2}.simple_LSH -hr ${temp_hash2} -pot ${pot} 

n3=8840
K3=17
L3=3
dPath3=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_3
oFolder3=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_max/result_${d}D3_${K3}_${L3}
temp_hash3=./temp_result_6D_top25_log_plus_10717764/hash_proj_${datatype}_max_3
./alsh -alg 10 -n ${n3} -qn ${qn} -d ${d} -K ${K3} -L ${L3} -LI 4 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath3} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder3}.simple_LSH -hr ${temp_hash3} -pot ${pot} 

n4=10929
K4=17
L4=3
dPath4=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_4
oFolder4=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_max/result_${d}D4_${K4}_${L4}
temp_hash4=./temp_result_6D_top25_log_plus_10717764/hash_proj_${datatype}_max_4
./alsh -alg 10 -n ${n4} -qn ${qn} -d ${d} -K ${K4} -L ${L4} -LI 5 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath4} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder4}.simple_LSH -hr ${temp_hash4} -pot ${pot} 

n5=13072
K5=17
L5=2
dPath5=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_5
oFolder5=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_max/result_${d}D5_${K5}_${L5}
temp_hash5=./temp_result_6D_top25_log_plus_10717764/hash_proj_${datatype}_max_5
./alsh -alg 10 -n ${n5} -qn ${qn} -d ${d} -K ${K5} -L ${L5} -LI 6 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath5} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder5}.simple_LSH -hr ${temp_hash5} -pot ${pot} 

# ------------------------------------------------------------------------------ 
#     Overall-Performance 
# ------------------------------------------------------------------------------ 
./alsh -alg 12 -d ${d} -qn ${qn} -L1 ${num_layer} -tk ${top_k} -it ${temporalResult} -ts ${tsPath}.mip -of ${overallResult} 
 
 
sleep 2 
datatype=HOUSE
cardinality=10717764
d=6
qn=1000
c0=2
pot=0
temporalResult=./temp_result_6D_top25_log_plus_10717764/run_test_${datatype}_${d}_${cardinality}_uni
overallResult=./temp_result_6D_top25_log_plus_10717764/overall_run_test_${datatype}_${d}_${cardinality}_uni
sim_angle=./temp_result_6D_top25_log_plus_10717764/sim_angle_${datatype}_${d}_${cardinality}_uni
S=0.75
num_layer=6
top_k=25
# ------------------------------------------------------------------------------ 
#     Ground-Truth 
# ------------------------------------------------------------------------------ 
dPath=./raw_data/${datatype}/${datatype}_${d}_${cardinality}.txt 
tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth 
qPath=./query/query_${datatype}.txt 
oFolder=./result/result_${datatype}_${d}D_${cardinality} 
# ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip 

 
 
# ------------------------------------------------------------------------------ 
#     Layer-Performance 
# ------------------------------------------------------------------------------ 
n0=2005
K0=14
L0=15
dPath0=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_0
oFolder0=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_uni/result_${d}D0_${K0}_${L0}
temp_hash0=./temp_result_6D_top25_log_plus_10717764/hash_proj_${datatype}_uni_0
./alsh -alg 10 -n ${n0} -qn ${qn} -d ${d} -K ${K0} -L ${L0} -LI 1 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath0} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder0}.simple_LSH -hr ${temp_hash0} -pot ${pot} 

n1=4363
K1=16
L1=7
dPath1=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_1
oFolder1=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_uni/result_${d}D1_${K1}_${L1}
temp_hash1=./temp_result_6D_top25_log_plus_10717764/hash_proj_${datatype}_uni_1
./alsh -alg 10 -n ${n1} -qn ${qn} -d ${d} -K ${K1} -L ${L1} -LI 2 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath1} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder1}.simple_LSH -hr ${temp_hash1} -pot ${pot} 

n2=6607
K2=16
L2=5
dPath2=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_2
oFolder2=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_uni/result_${d}D2_${K2}_${L2}
temp_hash2=./temp_result_6D_top25_log_plus_10717764/hash_proj_${datatype}_uni_2
./alsh -alg 10 -n ${n2} -qn ${qn} -d ${d} -K ${K2} -L ${L2} -LI 3 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath2} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder2}.simple_LSH -hr ${temp_hash2} -pot ${pot} 

n3=8840
K3=17
L3=3
dPath3=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_3
oFolder3=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_uni/result_${d}D3_${K3}_${L3}
temp_hash3=./temp_result_6D_top25_log_plus_10717764/hash_proj_${datatype}_uni_3
./alsh -alg 10 -n ${n3} -qn ${qn} -d ${d} -K ${K3} -L ${L3} -LI 4 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath3} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder3}.simple_LSH -hr ${temp_hash3} -pot ${pot} 

n4=10929
K4=17
L4=3
dPath4=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_4
oFolder4=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_uni/result_${d}D4_${K4}_${L4}
temp_hash4=./temp_result_6D_top25_log_plus_10717764/hash_proj_${datatype}_uni_4
./alsh -alg 10 -n ${n4} -qn ${qn} -d ${d} -K ${K4} -L ${L4} -LI 5 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath4} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder4}.simple_LSH -hr ${temp_hash4} -pot ${pot} 

n5=13072
K5=17
L5=2
dPath5=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_5
oFolder5=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_uni/result_${d}D5_${K5}_${L5}
temp_hash5=./temp_result_6D_top25_log_plus_10717764/hash_proj_${datatype}_uni_5
./alsh -alg 10 -n ${n5} -qn ${qn} -d ${d} -K ${K5} -L ${L5} -LI 6 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath5} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder5}.simple_LSH -hr ${temp_hash5} -pot ${pot} 

# ------------------------------------------------------------------------------ 
#     Overall-Performance 
# ------------------------------------------------------------------------------ 
./alsh -alg 12 -d ${d} -qn ${qn} -L1 ${num_layer} -tk ${top_k} -it ${temporalResult} -ts ${tsPath}.mip -of ${overallResult} 
 
 
sleep 2 
datatype=HOUSE
cardinality=10717764
d=6
qn=1000
c0=2
pot=0
temporalResult=./temp_result_6D_top25_log_plus_plus_10717764/run_test_${datatype}_${d}_${cardinality}_opt
overallResult=./temp_result_6D_top25_log_plus_plus_10717764/overall_run_test_${datatype}_${d}_${cardinality}_opt
sim_angle=./temp_result_6D_top25_log_plus_plus_10717764/sim_angle_${datatype}_${d}_${cardinality}_opt
S=0.75
num_layer=6
top_k=25
# ------------------------------------------------------------------------------ 
#     Ground-Truth 
# ------------------------------------------------------------------------------ 
dPath=./raw_data/${datatype}/${datatype}_${d}_${cardinality}.txt 
tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth 
qPath=./query/query_${datatype}.txt 
oFolder=./result/result_${datatype}_${d}D_${cardinality} 
 # ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip 
 # sleep 1 

 
 
# ------------------------------------------------------------------------------ 
#     Layer-Performance 
# ------------------------------------------------------------------------------ 
n0=2005
K0=17
L0=36
dPath0=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_0
oFolder0=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_opt/result_${d}D0_${K0}_${L0}
temp_hash0=./temp_result_6D_top25_log_plus_plus_10717764/hash_proj_${datatype}_opt_0
./alsh -alg 10 -n ${n0} -qn ${qn} -d ${d} -K ${K0} -L ${L0} -LI 1 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath0} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder0}.simple_LSH -hr ${temp_hash0} -pot ${pot} 

n1=4363
K1=19
L1=5
dPath1=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_1
oFolder1=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_opt/result_${d}D1_${K1}_${L1}
temp_hash1=./temp_result_6D_top25_log_plus_plus_10717764/hash_proj_${datatype}_opt_1
./alsh -alg 10 -n ${n1} -qn ${qn} -d ${d} -K ${K1} -L ${L1} -LI 2 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath1} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder1}.simple_LSH -hr ${temp_hash1} -pot ${pot} 

n2=6607
K2=19
L2=4
dPath2=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_2
oFolder2=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_opt/result_${d}D2_${K2}_${L2}
temp_hash2=./temp_result_6D_top25_log_plus_plus_10717764/hash_proj_${datatype}_opt_2
./alsh -alg 10 -n ${n2} -qn ${qn} -d ${d} -K ${K2} -L ${L2} -LI 3 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath2} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder2}.simple_LSH -hr ${temp_hash2} -pot ${pot} 

n3=8840
K3=20
L3=3
dPath3=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_3
oFolder3=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_opt/result_${d}D3_${K3}_${L3}
temp_hash3=./temp_result_6D_top25_log_plus_plus_10717764/hash_proj_${datatype}_opt_3
./alsh -alg 10 -n ${n3} -qn ${qn} -d ${d} -K ${K3} -L ${L3} -LI 4 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath3} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder3}.simple_LSH -hr ${temp_hash3} -pot ${pot} 

n4=10929
K4=20
L4=2
dPath4=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_4
oFolder4=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_opt/result_${d}D4_${K4}_${L4}
temp_hash4=./temp_result_6D_top25_log_plus_plus_10717764/hash_proj_${datatype}_opt_4
./alsh -alg 10 -n ${n4} -qn ${qn} -d ${d} -K ${K4} -L ${L4} -LI 5 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath4} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder4}.simple_LSH -hr ${temp_hash4} -pot ${pot} 

n5=13072
K5=20
L5=1
dPath5=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_5
oFolder5=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_opt/result_${d}D5_${K5}_${L5}
temp_hash5=./temp_result_6D_top25_log_plus_plus_10717764/hash_proj_${datatype}_opt_5
./alsh -alg 10 -n ${n5} -qn ${qn} -d ${d} -K ${K5} -L ${L5} -LI 6 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath5} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder5}.simple_LSH -hr ${temp_hash5} -pot ${pot} 

# ------------------------------------------------------------------------------ 
#     Overall-Performance 
# ------------------------------------------------------------------------------ 
./alsh -alg 12 -d ${d} -qn ${qn} -L1 ${num_layer} -tk ${top_k} -it ${temporalResult} -ts ${tsPath}.mip -of ${overallResult} 
 
 
sleep 2 
datatype=HOUSE
cardinality=10717764
d=6
qn=1000
c0=2
pot=0
temporalResult=./temp_result_6D_top25_log_plus_plus_10717764/run_test_${datatype}_${d}_${cardinality}_max
overallResult=./temp_result_6D_top25_log_plus_plus_10717764/overall_run_test_${datatype}_${d}_${cardinality}_max
sim_angle=./temp_result_6D_top25_log_plus_plus_10717764/sim_angle_${datatype}_${d}_${cardinality}_max
S=0.75
num_layer=6
top_k=25
# ------------------------------------------------------------------------------ 
#     Ground-Truth 
# ------------------------------------------------------------------------------ 
dPath=./raw_data/${datatype}/${datatype}_${d}_${cardinality}.txt 
tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth 
qPath=./query/query_${datatype}.txt 
oFolder=./result/result_${datatype}_${d}D_${cardinality} 
# ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip 

 
 
# ------------------------------------------------------------------------------ 
#     Layer-Performance 
# ------------------------------------------------------------------------------ 
n0=2005
K0=17
L0=15
dPath0=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_0
oFolder0=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_max/result_${d}D0_${K0}_${L0}
temp_hash0=./temp_result_6D_top25_log_plus_plus_10717764/hash_proj_${datatype}_max_0
./alsh -alg 10 -n ${n0} -qn ${qn} -d ${d} -K ${K0} -L ${L0} -LI 1 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath0} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder0}.simple_LSH -hr ${temp_hash0} -pot ${pot} 

n1=4363
K1=19
L1=7
dPath1=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_1
oFolder1=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_max/result_${d}D1_${K1}_${L1}
temp_hash1=./temp_result_6D_top25_log_plus_plus_10717764/hash_proj_${datatype}_max_1
./alsh -alg 10 -n ${n1} -qn ${qn} -d ${d} -K ${K1} -L ${L1} -LI 2 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath1} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder1}.simple_LSH -hr ${temp_hash1} -pot ${pot} 

n2=6607
K2=19
L2=5
dPath2=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_2
oFolder2=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_max/result_${d}D2_${K2}_${L2}
temp_hash2=./temp_result_6D_top25_log_plus_plus_10717764/hash_proj_${datatype}_max_2
./alsh -alg 10 -n ${n2} -qn ${qn} -d ${d} -K ${K2} -L ${L2} -LI 3 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath2} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder2}.simple_LSH -hr ${temp_hash2} -pot ${pot} 

n3=8840
K3=20
L3=3
dPath3=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_3
oFolder3=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_max/result_${d}D3_${K3}_${L3}
temp_hash3=./temp_result_6D_top25_log_plus_plus_10717764/hash_proj_${datatype}_max_3
./alsh -alg 10 -n ${n3} -qn ${qn} -d ${d} -K ${K3} -L ${L3} -LI 4 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath3} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder3}.simple_LSH -hr ${temp_hash3} -pot ${pot} 

n4=10929
K4=20
L4=3
dPath4=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_4
oFolder4=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_max/result_${d}D4_${K4}_${L4}
temp_hash4=./temp_result_6D_top25_log_plus_plus_10717764/hash_proj_${datatype}_max_4
./alsh -alg 10 -n ${n4} -qn ${qn} -d ${d} -K ${K4} -L ${L4} -LI 5 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath4} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder4}.simple_LSH -hr ${temp_hash4} -pot ${pot} 

n5=13072
K5=20
L5=2
dPath5=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_5
oFolder5=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_max/result_${d}D5_${K5}_${L5}
temp_hash5=./temp_result_6D_top25_log_plus_plus_10717764/hash_proj_${datatype}_max_5
./alsh -alg 10 -n ${n5} -qn ${qn} -d ${d} -K ${K5} -L ${L5} -LI 6 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath5} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder5}.simple_LSH -hr ${temp_hash5} -pot ${pot} 

# ------------------------------------------------------------------------------ 
#     Overall-Performance 
# ------------------------------------------------------------------------------ 
./alsh -alg 12 -d ${d} -qn ${qn} -L1 ${num_layer} -tk ${top_k} -it ${temporalResult} -ts ${tsPath}.mip -of ${overallResult} 
 
 
sleep 2 
datatype=HOUSE
cardinality=10717764
d=6
qn=1000
c0=2
pot=0
temporalResult=./temp_result_6D_top25_log_plus_plus_10717764/run_test_${datatype}_${d}_${cardinality}_uni
overallResult=./temp_result_6D_top25_log_plus_plus_10717764/overall_run_test_${datatype}_${d}_${cardinality}_uni
sim_angle=./temp_result_6D_top25_log_plus_plus_10717764/sim_angle_${datatype}_${d}_${cardinality}_uni
S=0.75
num_layer=6
top_k=25
# ------------------------------------------------------------------------------ 
#     Ground-Truth 
# ------------------------------------------------------------------------------ 
dPath=./raw_data/${datatype}/${datatype}_${d}_${cardinality}.txt 
tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth 
qPath=./query/query_${datatype}.txt 
oFolder=./result/result_${datatype}_${d}D_${cardinality} 
# ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip 

 
 
# ------------------------------------------------------------------------------ 
#     Layer-Performance 
# ------------------------------------------------------------------------------ 
n0=2005
K0=17
L0=15
dPath0=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_0
oFolder0=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_uni/result_${d}D0_${K0}_${L0}
temp_hash0=./temp_result_6D_top25_log_plus_plus_10717764/hash_proj_${datatype}_uni_0
./alsh -alg 10 -n ${n0} -qn ${qn} -d ${d} -K ${K0} -L ${L0} -LI 1 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath0} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder0}.simple_LSH -hr ${temp_hash0} -pot ${pot} 

n1=4363
K1=19
L1=7
dPath1=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_1
oFolder1=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_uni/result_${d}D1_${K1}_${L1}
temp_hash1=./temp_result_6D_top25_log_plus_plus_10717764/hash_proj_${datatype}_uni_1
./alsh -alg 10 -n ${n1} -qn ${qn} -d ${d} -K ${K1} -L ${L1} -LI 2 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath1} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder1}.simple_LSH -hr ${temp_hash1} -pot ${pot} 

n2=6607
K2=19
L2=5
dPath2=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_2
oFolder2=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_uni/result_${d}D2_${K2}_${L2}
temp_hash2=./temp_result_6D_top25_log_plus_plus_10717764/hash_proj_${datatype}_uni_2
./alsh -alg 10 -n ${n2} -qn ${qn} -d ${d} -K ${K2} -L ${L2} -LI 3 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath2} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder2}.simple_LSH -hr ${temp_hash2} -pot ${pot} 

n3=8840
K3=20
L3=3
dPath3=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_3
oFolder3=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_uni/result_${d}D3_${K3}_${L3}
temp_hash3=./temp_result_6D_top25_log_plus_plus_10717764/hash_proj_${datatype}_uni_3
./alsh -alg 10 -n ${n3} -qn ${qn} -d ${d} -K ${K3} -L ${L3} -LI 4 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath3} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder3}.simple_LSH -hr ${temp_hash3} -pot ${pot} 

n4=10929
K4=20
L4=3
dPath4=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_4
oFolder4=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_uni/result_${d}D4_${K4}_${L4}
temp_hash4=./temp_result_6D_top25_log_plus_plus_10717764/hash_proj_${datatype}_uni_4
./alsh -alg 10 -n ${n4} -qn ${qn} -d ${d} -K ${K4} -L ${L4} -LI 5 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath4} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder4}.simple_LSH -hr ${temp_hash4} -pot ${pot} 

n5=13072
K5=20
L5=2
dPath5=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_5
oFolder5=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_uni/result_${d}D5_${K5}_${L5}
temp_hash5=./temp_result_6D_top25_log_plus_plus_10717764/hash_proj_${datatype}_uni_5
./alsh -alg 10 -n ${n5} -qn ${qn} -d ${d} -K ${K5} -L ${L5} -LI 6 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath5} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder5}.simple_LSH -hr ${temp_hash5} -pot ${pot} 

# ------------------------------------------------------------------------------ 
#     Overall-Performance 
# ------------------------------------------------------------------------------ 
./alsh -alg 12 -d ${d} -qn ${qn} -L1 ${num_layer} -tk ${top_k} -it ${temporalResult} -ts ${tsPath}.mip -of ${overallResult} 
 
 
sleep 2 
datatype=HOUSE
cardinality=10717764
d=6
qn=1000
c0=2
pot=0
temporalResult=./temp_result_6D_top25_uni_10717764/run_test_${datatype}_${d}_${cardinality}_opt
overallResult=./temp_result_6D_top25_uni_10717764/overall_run_test_${datatype}_${d}_${cardinality}_opt
sim_angle=./temp_result_6D_top25_uni_10717764/sim_angle_${datatype}_${d}_${cardinality}_opt
S=0.75
num_layer=6
top_k=25
# ------------------------------------------------------------------------------ 
#     Ground-Truth 
# ------------------------------------------------------------------------------ 
dPath=./raw_data/${datatype}/${datatype}_${d}_${cardinality}.txt 
tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth 
qPath=./query/query_${datatype}.txt 
oFolder=./result/result_${datatype}_${d}D_${cardinality} 
 # ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip 
 # sleep 1 

 
 
# ------------------------------------------------------------------------------ 
#     Layer-Performance 
# ------------------------------------------------------------------------------ 
n0=2005
K0=14
L0=36
dPath0=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_0
oFolder0=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_opt/result_${d}D0_${K0}_${L0}
temp_hash0=./temp_result_6D_top25_uni_10717764/hash_proj_${datatype}_opt_0
./alsh -alg 10 -n ${n0} -qn ${qn} -d ${d} -K ${K0} -L ${L0} -LI 1 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath0} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder0}.simple_LSH -hr ${temp_hash0} -pot ${pot} 

n1=4363
K1=14
L1=5
dPath1=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_1
oFolder1=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_opt/result_${d}D1_${K1}_${L1}
temp_hash1=./temp_result_6D_top25_uni_10717764/hash_proj_${datatype}_opt_1
./alsh -alg 10 -n ${n1} -qn ${qn} -d ${d} -K ${K1} -L ${L1} -LI 2 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath1} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder1}.simple_LSH -hr ${temp_hash1} -pot ${pot} 

n2=6607
K2=14
L2=4
dPath2=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_2
oFolder2=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_opt/result_${d}D2_${K2}_${L2}
temp_hash2=./temp_result_6D_top25_uni_10717764/hash_proj_${datatype}_opt_2
./alsh -alg 10 -n ${n2} -qn ${qn} -d ${d} -K ${K2} -L ${L2} -LI 3 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath2} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder2}.simple_LSH -hr ${temp_hash2} -pot ${pot} 

n3=8840
K3=14
L3=3
dPath3=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_3
oFolder3=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_opt/result_${d}D3_${K3}_${L3}
temp_hash3=./temp_result_6D_top25_uni_10717764/hash_proj_${datatype}_opt_3
./alsh -alg 10 -n ${n3} -qn ${qn} -d ${d} -K ${K3} -L ${L3} -LI 4 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath3} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder3}.simple_LSH -hr ${temp_hash3} -pot ${pot} 

n4=10929
K4=14
L4=2
dPath4=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_4
oFolder4=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_opt/result_${d}D4_${K4}_${L4}
temp_hash4=./temp_result_6D_top25_uni_10717764/hash_proj_${datatype}_opt_4
./alsh -alg 10 -n ${n4} -qn ${qn} -d ${d} -K ${K4} -L ${L4} -LI 5 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath4} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder4}.simple_LSH -hr ${temp_hash4} -pot ${pot} 

n5=13072
K5=14
L5=1
dPath5=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_5
oFolder5=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_opt/result_${d}D5_${K5}_${L5}
temp_hash5=./temp_result_6D_top25_uni_10717764/hash_proj_${datatype}_opt_5
./alsh -alg 10 -n ${n5} -qn ${qn} -d ${d} -K ${K5} -L ${L5} -LI 6 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath5} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder5}.simple_LSH -hr ${temp_hash5} -pot ${pot} 

# ------------------------------------------------------------------------------ 
#     Overall-Performance 
# ------------------------------------------------------------------------------ 
./alsh -alg 12 -d ${d} -qn ${qn} -L1 ${num_layer} -tk ${top_k} -it ${temporalResult} -ts ${tsPath}.mip -of ${overallResult} 
 
 
sleep 2 
datatype=HOUSE
cardinality=10717764
d=6
qn=1000
c0=2
pot=0
temporalResult=./temp_result_6D_top25_uni_10717764/run_test_${datatype}_${d}_${cardinality}_max
overallResult=./temp_result_6D_top25_uni_10717764/overall_run_test_${datatype}_${d}_${cardinality}_max
sim_angle=./temp_result_6D_top25_uni_10717764/sim_angle_${datatype}_${d}_${cardinality}_max
S=0.75
num_layer=6
top_k=25
# ------------------------------------------------------------------------------ 
#     Ground-Truth 
# ------------------------------------------------------------------------------ 
dPath=./raw_data/${datatype}/${datatype}_${d}_${cardinality}.txt 
tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth 
qPath=./query/query_${datatype}.txt 
oFolder=./result/result_${datatype}_${d}D_${cardinality} 
# ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip 

 
 
# ------------------------------------------------------------------------------ 
#     Layer-Performance 
# ------------------------------------------------------------------------------ 
n0=2005
K0=14
L0=15
dPath0=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_0
oFolder0=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_max/result_${d}D0_${K0}_${L0}
temp_hash0=./temp_result_6D_top25_uni_10717764/hash_proj_${datatype}_max_0
./alsh -alg 10 -n ${n0} -qn ${qn} -d ${d} -K ${K0} -L ${L0} -LI 1 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath0} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder0}.simple_LSH -hr ${temp_hash0} -pot ${pot} 

n1=4363
K1=14
L1=7
dPath1=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_1
oFolder1=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_max/result_${d}D1_${K1}_${L1}
temp_hash1=./temp_result_6D_top25_uni_10717764/hash_proj_${datatype}_max_1
./alsh -alg 10 -n ${n1} -qn ${qn} -d ${d} -K ${K1} -L ${L1} -LI 2 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath1} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder1}.simple_LSH -hr ${temp_hash1} -pot ${pot} 

n2=6607
K2=14
L2=5
dPath2=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_2
oFolder2=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_max/result_${d}D2_${K2}_${L2}
temp_hash2=./temp_result_6D_top25_uni_10717764/hash_proj_${datatype}_max_2
./alsh -alg 10 -n ${n2} -qn ${qn} -d ${d} -K ${K2} -L ${L2} -LI 3 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath2} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder2}.simple_LSH -hr ${temp_hash2} -pot ${pot} 

n3=8840
K3=14
L3=3
dPath3=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_3
oFolder3=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_max/result_${d}D3_${K3}_${L3}
temp_hash3=./temp_result_6D_top25_uni_10717764/hash_proj_${datatype}_max_3
./alsh -alg 10 -n ${n3} -qn ${qn} -d ${d} -K ${K3} -L ${L3} -LI 4 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath3} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder3}.simple_LSH -hr ${temp_hash3} -pot ${pot} 

n4=10929
K4=14
L4=3
dPath4=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_4
oFolder4=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_max/result_${d}D4_${K4}_${L4}
temp_hash4=./temp_result_6D_top25_uni_10717764/hash_proj_${datatype}_max_4
./alsh -alg 10 -n ${n4} -qn ${qn} -d ${d} -K ${K4} -L ${L4} -LI 5 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath4} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder4}.simple_LSH -hr ${temp_hash4} -pot ${pot} 

n5=13072
K5=14
L5=2
dPath5=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_5
oFolder5=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_max/result_${d}D5_${K5}_${L5}
temp_hash5=./temp_result_6D_top25_uni_10717764/hash_proj_${datatype}_max_5
./alsh -alg 10 -n ${n5} -qn ${qn} -d ${d} -K ${K5} -L ${L5} -LI 6 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath5} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder5}.simple_LSH -hr ${temp_hash5} -pot ${pot} 

# ------------------------------------------------------------------------------ 
#     Overall-Performance 
# ------------------------------------------------------------------------------ 
./alsh -alg 12 -d ${d} -qn ${qn} -L1 ${num_layer} -tk ${top_k} -it ${temporalResult} -ts ${tsPath}.mip -of ${overallResult} 
 
 
sleep 2 
datatype=HOUSE
cardinality=10717764
d=6
qn=1000
c0=2
pot=0
temporalResult=./temp_result_6D_top25_uni_10717764/run_test_${datatype}_${d}_${cardinality}_uni
overallResult=./temp_result_6D_top25_uni_10717764/overall_run_test_${datatype}_${d}_${cardinality}_uni
sim_angle=./temp_result_6D_top25_uni_10717764/sim_angle_${datatype}_${d}_${cardinality}_uni
S=0.75
num_layer=6
top_k=25
# ------------------------------------------------------------------------------ 
#     Ground-Truth 
# ------------------------------------------------------------------------------ 
dPath=./raw_data/${datatype}/${datatype}_${d}_${cardinality}.txt 
tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth 
qPath=./query/query_${datatype}.txt 
oFolder=./result/result_${datatype}_${d}D_${cardinality} 
# ./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts ${oFolder}.mip 

 
 
# ------------------------------------------------------------------------------ 
#     Layer-Performance 
# ------------------------------------------------------------------------------ 
n0=2005
K0=14
L0=15
dPath0=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_0
oFolder0=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_uni/result_${d}D0_${K0}_${L0}
temp_hash0=./temp_result_6D_top25_uni_10717764/hash_proj_${datatype}_uni_0
./alsh -alg 10 -n ${n0} -qn ${qn} -d ${d} -K ${K0} -L ${L0} -LI 1 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath0} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder0}.simple_LSH -hr ${temp_hash0} -pot ${pot} 

n1=4363
K1=14
L1=7
dPath1=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_1
oFolder1=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_uni/result_${d}D1_${K1}_${L1}
temp_hash1=./temp_result_6D_top25_uni_10717764/hash_proj_${datatype}_uni_1
./alsh -alg 10 -n ${n1} -qn ${qn} -d ${d} -K ${K1} -L ${L1} -LI 2 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath1} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder1}.simple_LSH -hr ${temp_hash1} -pot ${pot} 

n2=6607
K2=14
L2=5
dPath2=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_2
oFolder2=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_uni/result_${d}D2_${K2}_${L2}
temp_hash2=./temp_result_6D_top25_uni_10717764/hash_proj_${datatype}_uni_2
./alsh -alg 10 -n ${n2} -qn ${qn} -d ${d} -K ${K2} -L ${L2} -LI 3 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath2} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder2}.simple_LSH -hr ${temp_hash2} -pot ${pot} 

n3=8840
K3=14
L3=3
dPath3=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_3
oFolder3=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_uni/result_${d}D3_${K3}_${L3}
temp_hash3=./temp_result_6D_top25_uni_10717764/hash_proj_${datatype}_uni_3
./alsh -alg 10 -n ${n3} -qn ${qn} -d ${d} -K ${K3} -L ${L3} -LI 4 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath3} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder3}.simple_LSH -hr ${temp_hash3} -pot ${pot} 

n4=10929
K4=14
L4=3
dPath4=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_4
oFolder4=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_uni/result_${d}D4_${K4}_${L4}
temp_hash4=./temp_result_6D_top25_uni_10717764/hash_proj_${datatype}_uni_4
./alsh -alg 10 -n ${n4} -qn ${qn} -d ${d} -K ${K4} -L ${L4} -LI 5 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath4} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder4}.simple_LSH -hr ${temp_hash4} -pot ${pot} 

n5=13072
K5=14
L5=2
dPath5=./qhull_data/${datatype}/${datatype}_${d}_${cardinality}_qhull_layer_5
oFolder5=./result/${datatype}/Dimension_${d}_Cardinality_${cardinality}_uni/result_${d}D5_${K5}_${L5}
temp_hash5=./temp_result_6D_top25_uni_10717764/hash_proj_${datatype}_uni_5
./alsh -alg 10 -n ${n5} -qn ${qn} -d ${d} -K ${K5} -L ${L5} -LI 6 -tk ${top_k} -S ${S} -c0 ${c0} -ds ${dPath5} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -sa ${sim_angle} -of ${oFolder5}.simple_LSH -hr ${temp_hash5} -pot ${pot} 

# ------------------------------------------------------------------------------ 
#     Overall-Performance 
# ------------------------------------------------------------------------------ 
./alsh -alg 12 -d ${d} -qn ${qn} -L1 ${num_layer} -tk ${top_k} -it ${temporalResult} -ts ${tsPath}.mip -of ${overallResult} 
 
 
sleep 2 
