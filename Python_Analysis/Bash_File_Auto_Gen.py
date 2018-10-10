# script to generate .sh file for execution
# bash file includes execution of Ground Truth, LSH Scheme and Overall Performance

import math
import os

# data_type = ["random", "correlated", "anti_correlated"]
data_type = ["random", "correlated", "anti_correlated"]
# data_type = ["correlated"]
dimensions = [5]
cardinality = [100000]
query_count = 1000

topk = 25
ratio = 2
sim_threshold = 0.9

# bash_set_indices = [6, 7, 8, 9, 10]
bash_set_indices = [11, 12, 13, 14, 15]
for jjj in range(bash_set_indices.__len__()):
    bash_set_index = bash_set_indices[jjj]
    PARAMETER_BASE_FOLDER = "../H2_ALSH/parameters/Space_Cost_Uni_" + str(bash_set_index) + "/"

    BASE_FOLDER = "../H2_ALSH/qhull_data/Synthetic/"
    BASH_FILE_BASE_FOLDER = "../H2_ALSH/"
    BASH_FILE_FOLDER = BASH_FILE_BASE_FOLDER + "bash_set_" + str(bash_set_index) + "/"
    TEMPORAL_RESULT = "../H2_ALSH/temp_result_" + str(bash_set_index) + "/"
    TEMPORAL_RESULT_FOR_BASH = "./temp_result_" + str(bash_set_index) + "/"

    if not os.path.exists(BASH_FILE_FOLDER):
        os.makedirs(BASH_FILE_FOLDER)

    if not os.path.exists(TEMPORAL_RESULT):
        os.makedirs(TEMPORAL_RESULT)

    # read qhull data to get qhull layer element count
    for i in range(len(data_type)):
        for j in range(len(dimensions)):
            for k in range(len(cardinality)):
                K_List = []
                L_List = []
                qhull_data_count = []

                bash_file = BASH_FILE_FOLDER + "run_test_" + str(data_type[i]) + "_" + str(dimensions[j]) + "_" + \
                            str(cardinality[k]) + ".sh"

                # read parameters K and L
                # path for param-K
                paramK_path = PARAMETER_BASE_FOLDER + "K_" + data_type[i] + "_" + str(dimensions[j]) + "_" + str(cardinality[k])
                f1 = open(paramK_path, 'r')
                K_lines = f1.readlines()
                # for k_index in range(topk):
                #     K_List.append(int(K_lines[0].split('\r')[k_index]))
                # f1.close()
                for k_index in range(0, len(K_lines)):
                    K_List.append(int(K_lines[k_index].split('\n')[0]))
                f1.close()

                # path for param-L
                paramL_path = PARAMETER_BASE_FOLDER + "L_" + data_type[i] + "_" + str(dimensions[j]) + "_" + str(cardinality[k])


                f2 = open(paramL_path, 'r')
                L_lines = f2.readlines()
                # for l_index in range(0, topk):
                #     L_List.append(int(math.floor(float(L_lines[0].split('\r')[l_index]))))
                # f2.close()

                for l_index in range(0, len(L_lines)):
                    L_List.append(int(math.floor(float(L_lines[l_index].split('\n')[0]))))
                f2.close()
                print(L_List)

                for m in range(len(K_List)):
                    qhull_file = BASE_FOLDER + data_type[i] + "_" + str(dimensions[j]) + "_" + str(cardinality[k]) + \
                                 "_" + "qhull_layer_" + str(m)
                    f = open(qhull_file, 'r')
                    lines = f.readlines()
                    second_line = lines[1]
                    cur_data_count = int(second_line.split('\n')[0])
                    qhull_data_count.append(cur_data_count)
                    f.close()

                obj_cumsum = []
                hashsize_cumsum = []
                obj_hashsize_file = BASH_FILE_FOLDER + "cumsum_hashsize_obj_" + data_type[i] + "_" + str(dimensions[j]) + \
                    "_" + str(cardinality[k]) + ".txt"
                f4 = open(obj_hashsize_file, 'w')
                for m in range(len(L_List)):
                    if obj_cumsum.__len__() == 0:
                        obj_cumsum.append(qhull_data_count[m])
                        hashsize_cumsum.append(qhull_data_count[m] * L_List[m])
                    else:
                        obj_cumsum.append(obj_cumsum[obj_cumsum.__len__() - 1] + qhull_data_count[m])
                        hashsize_cumsum.append(hashsize_cumsum[hashsize_cumsum.__len__() - 1] + qhull_data_count[m] * L_List[m])
                f4.write(','.join(map(repr, obj_cumsum)))
                f4.write("\n")
                f4.write(','.join(map(repr, hashsize_cumsum)))
                f4.close()
                # write to .sh file at save path
                f3 = open(bash_file, 'w')
                f3.write("#!/bin/bash \n")
                f3.write("# make \n")
                f3.write("rm *.o \n")
                cur_data_type = data_type[i]
                cur_cardinality = cardinality[k]
                cur_dimension = dimensions[j]
                f3.write("datatype=" + cur_data_type + "\n")
                f3.write("cardinality=" + str(cur_cardinality) + "\n")
                f3.write("d=" + str(cur_dimension) + "\n")
                f3.write("qn=" + str(query_count) + "\n")
                f3.write("c0=" + str(ratio) + "\n")
                # temporalResult = TEMPORAL_RESULT + "run_test_" + str(data_type[i]) + "_" + str(dimensions[j]) + "_" + \
                #     str(cardinality[k])
                # overallResult = TEMPORAL_RESULT + "overall_run_test_" + str(data_type[i]) + "_" + str(dimensions[j]) + "_" + \
                #     str(cardinality[k]) + ".txt"

                temporalResult = TEMPORAL_RESULT_FOR_BASH + "run_test_${datatype}_${d}_${cardinality}"
                overallResult = TEMPORAL_RESULT_FOR_BASH + "overall_run_test_${datatype}_${d}_${cardinality}.txt"
                f3.write("temporalResult=" + temporalResult + "\n")
                f3.write("overallResult=" + overallResult + "\n")
                f3.write("S=" + str(sim_threshold) + "\n")
                f3.write("num_layer=" + str(len(K_List)) + "\n")
                f3.write("# ------------------------------------------------------------------------------ \n")
                f3.write("#     Ground-Truth \n")
                f3.write("# ------------------------------------------------------------------------------ \n")
                f3.write("dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt \n")
                f3.write("tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth \n")
                f3.write("qPath=./query/query_${d}D.txt \n")
                f3.write("oFolder=./result/result_${datatype}_${d}D_${cardinality} \n")
                f3.write("./alsh -alg 0 -n ${cardinality} -qn ${qn} -d ${d} -ds ${dPath} -qs ${qPath} -ts "
                         "${oFolder}.mip \n")
                f3.write("\n \n \n")
                f3.write("# ------------------------------------------------------------------------------ \n")
                f3.write("#     Layer-Performance \n")
                f3.write("# ------------------------------------------------------------------------------ \n")
                for kk in range(len(K_List)):
                    f3.write("n" + str(kk) + "=" + str(qhull_data_count[kk]) + "\n")
                    f3.write("K" + str(kk) + "=" + str(K_List[kk]) + "\n")
                    f3.write("L" + str(kk) + "=" + str(L_List[kk]) + "\n")

                    f3.write("dPath" + str(kk) + "=./qhull_data/Synthetic/${datatype}_${d}_"
                                                 "${cardinality}_qhull_layer_"+str(kk) + "\n")

                    f3.write("oFolder" + str(kk) + "=./result/${datatype}/Dimension_${d}_Cardinality_"
                                                   "${cardinality}/result_${d}D" + str(kk) + "_${K" + str(kk)
                             + "}_${L"+str(kk) + "}" + "\n")

                    f3.write("./alsh -alg 10 -n ${n" + str(kk) + "} -qn ${qn} -d ${d} -K ${K" + str(kk) +
                             "} -L ${L" + str(kk) + "} -LI " + str(kk+1) + " -S ${S} -c0 ${c0} -ds ${dPath" + str(kk)
                             + "} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -of ${oFolder" + str(kk) + "}.simple_LSH \n")

                    f3.write("\n")
                # append overall accuracy computation here
                f3.write("# ------------------------------------------------------------------------------ \n")
                f3.write("#     Overall-Performance \n")
                f3.write("# ------------------------------------------------------------------------------ \n")
                f3.write("./alsh -alg 12 -d ${d} -qn ${qn} -L1 ${num_layer} -it ${temporalResult} -ts "
                         "${tsPath}.mip -of ${overallResult} \n")
                f3.close()
