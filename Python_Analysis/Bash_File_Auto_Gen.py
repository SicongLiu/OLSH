# script to generate .sh file for execution
# bash file includes execution of Ground Truth, LSH Scheme and Overall Performance

import math
import os
from openpyxl import load_workbook

data_type = ["anti_correlated", "correlated", "random"]
budgets = ["500k", "1M"]
dimensions = [5]
top_ks = [10, 25]
types = ["log", "log_minus", "log_plus", "log_plus_plus", "uni"]
card_excel = ['100k', '200k']

k_ranges_anti_10 = ['E6', 'E15', 'E21', 'E30', 'E37', 'E46', 'E51', 'E60', 'E68', 'E77']
l_ranges_opt_anti_10 = ['F6', 'F15', 'F21', 'F30', 'F37', 'F46', 'F51', 'F60', 'F68', 'F77']
l_ranges_uni_anti_10 = ['G6', 'G15', 'G21', 'G30', 'G37', 'G46', 'G51', 'G60', 'G68', 'G77']

k_ranges_corr_10 = ['U6', 'U15', 'U21', 'U30', 'U37', 'U46', 'U51', 'U60', 'U68', 'U77']
l_ranges_opt_corr_10 = ['V6', 'V15', 'V21', 'V30', 'V37', 'V46', 'V51', 'V60', 'V68', 'V77']
l_ranges_uni_corr_10 = ['W6', 'W15', 'W21', 'W30', 'W37', 'W46', 'W51', 'W60', 'W68', 'W77']

k_ranges_random_10 = ['AJ6', 'AJ15', 'AJ21', 'AJ30', 'AJ37', 'AJ46', 'AJ51', 'AJ60', 'AJ68', 'AJ77']
l_ranges_opt_random_10 = ['AK6', 'AK15', 'AK21', 'AK30', 'AK37', 'AK46', 'AK51', 'AK60', 'AK68', 'AK77']
l_ranges_uni_random_10 = ['AL6', 'AL15', 'AL21', 'AL30', 'AL37', 'AL46', 'AL51', 'AL60', 'AL68', 'AL77']

k_ranges_anti_25 = ['E7', 'E31', 'E39', 'E63', 'E70', 'E94', 'E101', 'E125', 'E132', 'E156']
l_ranges_opt_anti_25 = ['F7', 'F31', 'F39', 'F63', 'F70', 'F94', 'F101', 'F125', 'F132', 'F156']
l_ranges_uni_anti_25 = ['G7', 'G31', 'G39', 'G63', 'G70', 'G94', 'G101', 'G125', 'G132', 'G156']

k_ranges_corr_25 = ['U7', 'U31', 'U39', 'U63', 'U70', 'U94', 'U101', 'U125', 'U132', 'U156']
l_ranges_opt_corr_25 = ['V7', 'V31', 'V39', 'V63', 'V70', 'V94', 'V101', 'V125', 'V132', 'V156']
l_ranges_uni_corr_25 = ['W7', 'W31', 'W39', 'W63', 'W70', 'W94', 'W101', 'W125', 'W132', 'W156']

k_ranges_random_25 = ['AJ7', 'AJ31', 'AJ39', 'AJ63', 'AJ70', 'AJ94', 'AJ101', 'AJ125', 'AJ132', 'AJ156']
l_ranges_opt_random_25 = ['AK7', 'AK31', 'AK39', 'AK63', 'AK70', 'AK94', 'AK101', 'AK125', 'AK132', 'AK156']
l_ranges_uni_random_25 = ['AL7', 'AL31', 'AL39', 'AL63', 'AL70', 'AL94', 'AL101', 'AL125', 'AL132', 'AL156']

excel_file = "../Checkpoint_Result_Oct_10.xlsx"
wb = load_workbook(filename=excel_file, data_only=True)

save_file_path = '../H2_ALSH/parameters/'

for i in range(top_ks.__len__()):
    top_k = top_ks[i]
    if top_k == 10:
        k_ranges_anti = k_ranges_anti_10
        l_ranges_opt_anti = l_ranges_opt_anti_10
        l_ranges_uni_anti = l_ranges_uni_anti_10

        k_ranges_corr = k_ranges_corr_10
        l_ranges_opt_corr = l_ranges_opt_corr_10
        l_ranges_uni_corr = l_ranges_uni_corr_10

        k_ranges_random = k_ranges_random_10
        l_ranges_opt_random = l_ranges_opt_random_10
        l_ranges_uni_random = l_ranges_uni_random_10
    else:
        k_ranges_anti = k_ranges_anti_25
        l_ranges_opt_anti = l_ranges_opt_anti_25
        l_ranges_uni_anti = l_ranges_uni_anti_25

        k_ranges_corr = k_ranges_corr_25
        l_ranges_opt_corr = l_ranges_opt_corr_25
        l_ranges_uni_corr = l_ranges_uni_corr_25

        k_ranges_random = k_ranges_random_25
        l_ranges_opt_random = l_ranges_opt_random_25
        l_ranges_uni_random = l_ranges_uni_random_25
    for j in range(budgets.__len__()):
        budget = budgets[j]
        for k in range(dimensions.__len__()):
            dimension = dimensions[k]
            sheetname = "Budget_" + str(dimension) + "D_top" + str(top_k) + "_" + str(budget)
            if sheetname in wb.sheetnames:
                ws = wb[sheetname]
                for m in range(types.__len__()):
                    type_name = types[m]
                    start = 2 * m
                    end = 2 * m + 1
                    # read data type anti_correlated
                    k_anti = []
                    for row in ws[k_ranges_anti[start]: k_ranges_anti[end]]:
                        for cell in row:
                            k_anti.append(cell.value)

                    l_anti_opt = []
                    for row in ws[l_ranges_opt_anti[start]: l_ranges_opt_anti[end]]:
                        for cell in row:
                            l_anti_opt.append(cell.value)

                    l_anti_uni = []
                    for row in ws[l_ranges_uni_anti[start]: l_ranges_uni_anti[end]]:
                        for cell in row:
                            l_anti_uni.append(cell.value)

                    # read data type correlated
                    k_corr = []
                    for row in ws[k_ranges_corr[start]: k_ranges_corr[end]]:
                        for cell in row:
                            k_corr.append(cell.value)

                    l_corr_opt = []
                    for row in ws[l_ranges_opt_corr[start]: l_ranges_opt_corr[end]]:
                        for cell in row:
                            l_corr_opt.append(cell.value)

                    l_corr_uni = []
                    for row in ws[l_ranges_uni_corr[start]: l_ranges_uni_corr[end]]:
                        for cell in row:
                            l_corr_uni.append(cell.value)

                    # read data type random
                    k_random = []
                    for row in ws[k_ranges_random[start]: k_ranges_random[end]]:
                        for cell in row:
                            k_random.append(cell.value)

                    l_random_opt = []
                    for row in ws[l_ranges_opt_random[start]: l_ranges_opt_random[end]]:
                        for cell in row:
                            l_random_opt.append(cell.value)

                    l_random_uni = []
                    for row in ws[l_ranges_uni_random[start]: l_ranges_uni_random[end]]:
                        for cell in row:
                            l_random_uni.append(cell.value)
                    # save current K and L parameters to files
                    # anti_opt
                    # anti_uni
                    save_file_dir = save_file_path + str(dimension) + "D_top" + str(top_k) + "_budget_" + str(budget)\
                                    + "_" + type_name + "/"

                    if not os.path.exists(save_file_dir):
                        os.makedirs(save_file_dir)
                    anti_k_name = save_file_dir + "k_anti_correlated"
                    f = open(anti_k_name, 'w')
                    f.write(','.join(map(str, k_anti)))
                    f.close()

                    anti_opt_name = save_file_dir + "l_anti_correlated_opt"
                    f = open(anti_opt_name, 'w')
                    f.write(','.join(map(str, l_anti_opt)))
                    f.close()

                    anti_uni_name = save_file_dir + "l_anti_correlated_uni"
                    f = open(anti_uni_name, 'w')
                    f.write(','.join(map(str, l_anti_uni)))
                    f.close()

                    # corr_opt
                    # corr_uni
                    corr_k_name = save_file_dir + "k_correlated"
                    f = open(corr_k_name, 'w')
                    f.write(','.join(map(str, k_corr)))
                    f.close()

                    corr_opt_name = save_file_dir + "l_correlated_opt"
                    f = open(corr_opt_name, 'w')
                    f.write(','.join(map(str, l_corr_opt)))
                    f.close()

                    corr_uni_name = save_file_dir + "l_correlated_uni"
                    f = open(corr_uni_name, 'w')
                    f.write(','.join(map(str, l_corr_uni)))
                    f.close()
                    # random_opt
                    # random_uni
                    random_k_name = save_file_dir + "k_random"
                    f = open(random_k_name, 'w')
                    f.write(','.join(map(str, k_random)))
                    f.close()

                    random_opt_name = save_file_dir + "l_random_opt"
                    f = open(random_opt_name, 'w')
                    f.write(','.join(map(str, l_random_opt)))
                    f.close()

                    random_uni_name = save_file_dir + "l_random_uni"
                    f = open(random_uni_name, 'w')
                    f.write(','.join(map(str, l_random_uni)))
                    f.close()
wb.close()
print("Done .\n")


cardinality = [100000, 200000]
query_count = 1000
ratio = 2
sim_threshold = 0.9

parameter_path = '../H2_ALSH/parameters/'
parameter_type = ["opt", "uni"]
BASE_FOLDER = "../H2_ALSH/qhull_data/Synthetic/"
BASH_FILE_BASE_FOLDER = "../H2_ALSH/"

total_bash_file = BASH_FILE_BASE_FOLDER + "run_bash_set_cur.sh"
f10 = open(total_bash_file, 'w')
f10.write("#!/bin/bash \n")

for i in range(top_ks.__len__()):
    top_k = top_ks[i]
    for j in range(budgets.__len__()):
        budget = budgets[j]
        for k in range(dimensions.__len__()):
            dimension = dimensions[k]
            for m in range(types.__len__()):
                type_name = types[m]
                parameter_dir = parameter_path + str(dimension) + "D_top" + str(top_k) + "_budget_" + str(budget)\
                                    + "_" + type_name + "/"
                if not os.path.exists(parameter_dir):
                    continue
                else:
                    BASH_FILE_FOLDER = BASH_FILE_BASE_FOLDER + "bash_set_" + str(dimension) + "D_top" + str(top_k) + \
                                       "_budget_" + str(budget) + "_" + type_name + "/"
                    TEMPORAL_RESULT = "../H2_ALSH/temp_result_" + str(dimension) + "D_top" + str(top_k) + "_budget_" + \
                                      str(budget) + "_" + type_name + "/"
                    TEMPORAL_RESULT_FOR_BASH = "./temp_result_" + str(dimension) + "D_top" + str(top_k) + "_budget_" + \
                                               str(budget) + "_" + type_name + "/"

                    if not os.path.exists(BASH_FILE_FOLDER):
                        os.makedirs(BASH_FILE_FOLDER)

                    if not os.path.exists(TEMPORAL_RESULT):
                        os.makedirs(TEMPORAL_RESULT)

                    cur_bash_set_dir = "bash_set_" + str(dimension) + "D_top" + str(top_k) + \
                                       "_budget_" + str(budget) + "_" + type_name + "/"
                    for ii in range(len(data_type)):
                        K_List = []
                        L_Opt_List = []
                        L_Uni_List = []
                        qhull_data_count = []
                        bash_file_opt = BASH_FILE_FOLDER + "run_test_" + str(data_type[ii]) + "_" + str(dimensions[k]) \
                                        + "_" + str(cardinality) + "_opt.sh"

                        bash_file_uni = BASH_FILE_FOLDER + "run_test_" + str(data_type[ii]) + "_" + str(dimensions[k]) \
                                        + "_" + str(cardinality) + "_uni.sh"

                        f10.write('sh ./' + cur_bash_set_dir + "run_test_" + str(data_type[ii]) + "_" + str(dimensions[k]) + "_" + str(cardinality) + "_opt.sh \n")
                        f10.write('sh ./' + cur_bash_set_dir + "run_test_" + str(data_type[ii]) + "_" + str(dimensions[k]) + "_" + str(cardinality) + "_uni.sh \n")
                        paramK_path = parameter_dir + "k_" + data_type[ii] #str(cardinality[k])
                        f1 = open(paramK_path, 'r')
                        K_lines = f1.readlines()
                        for k_index in range(top_k):
                            K_List.append(int(K_lines[0].split(',')[k_index]))
                        f1.close()

                        paramL_opt_path = parameter_dir + "l_" + data_type[ii] + "_opt" # str(cardinality[k])
                        f2 = open(paramL_opt_path, 'r')
                        L_lines = f2.readlines()
                        for l_index in range(0, top_k):
                            L_Opt_List.append(int(math.floor(float(L_lines[0].split(',')[l_index]))))
                        f2.close()
                        print("L opt: " + str(L_Opt_List))

                        paramL_uni_path = parameter_dir + "l_" + data_type[ii] + "_uni"  # str(cardinality[k])
                        f2 = open(paramL_uni_path, 'r')
                        L_lines = f2.readlines()
                        for l_index in range(0, top_k):
                            L_Uni_List.append(int(math.floor(float(L_lines[0].split(',')[l_index]))))
                        f2.close()
                        print("L uni: " + str(L_Uni_List))

                        for mm in range(len(K_List)):
                            qhull_file = BASE_FOLDER + data_type[ii] + "_" + str(dimensions[k]) + "_" + str(cardinality)\
                                         + "_" + "qhull_layer_" + str(mm)
                            f = open(qhull_file, 'r')
                            lines = f.readlines()
                            second_line = lines[1]
                            cur_data_count = int(second_line.split('\n')[0])
                            qhull_data_count.append(cur_data_count)
                            f.close()

                        # opt cumsum_hashsize
                        obj_cumsum = []
                        hashsize_cumsum = []
                        obj_hashsize_file = BASH_FILE_FOLDER + "cumsum_hashsize_obj_opt_" + data_type[ii] + "_" + str(
                            dimensions[k]) +  "_" + str(cardinality) + ".txt"
                        f4 = open(obj_hashsize_file, 'w')
                        for mm in range(len(L_Opt_List)):
                            if obj_cumsum.__len__() == 0:
                                obj_cumsum.append(qhull_data_count[mm])
                                hashsize_cumsum.append(qhull_data_count[mm] * L_Opt_List[mm])
                            else:
                                obj_cumsum.append(obj_cumsum[obj_cumsum.__len__() - 1] + qhull_data_count[mm])
                                hashsize_cumsum.append(
                                    hashsize_cumsum[hashsize_cumsum.__len__() - 1] + qhull_data_count[mm] * L_Opt_List[mm])
                        f4.write(','.join(map(repr, obj_cumsum)))
                        f4.write("\n")
                        f4.write(','.join(map(repr, hashsize_cumsum)))
                        f4.close()

                        # uni cumsum hashsize
                        obj_cumsum = []
                        hashsize_cumsum = []
                        obj_hashsize_file = BASH_FILE_FOLDER + "cumsum_hashsize_obj_uni_" + data_type[ii] + "_" + str(
                            dimensions[k]) + "_" + str(cardinality) + ".txt"
                        f4 = open(obj_hashsize_file, 'w')
                        for mm in range(len(L_Uni_List)):
                            if obj_cumsum.__len__() == 0:
                                obj_cumsum.append(qhull_data_count[mm])
                                hashsize_cumsum.append(qhull_data_count[mm] * L_Uni_List[mm])
                            else:
                                obj_cumsum.append(obj_cumsum[obj_cumsum.__len__() - 1] + qhull_data_count[mm])
                                hashsize_cumsum.append(
                                    hashsize_cumsum[hashsize_cumsum.__len__() - 1] + qhull_data_count[mm] * L_Uni_List[mm])
                        f4.write(','.join(map(repr, obj_cumsum)))
                        f4.write("\n")
                        f4.write(','.join(map(repr, hashsize_cumsum)))
                        f4.close()

                        # write to .sh file at save path, opt
                        f3 = open(bash_file_opt, 'w')
                        f3.write("#!/bin/bash \n")
                        f3.write("# make \n")
                        f3.write("rm *.o \n")
                        cur_data_type = data_type[ii]
                        cur_cardinality = cardinality
                        cur_dimension = dimensions[k]
                        f3.write("datatype=" + cur_data_type + "\n")
                        f3.write("cardinality=" + str(cur_cardinality) + "\n")
                        f3.write("d=" + str(cur_dimension) + "\n")
                        f3.write("qn=" + str(query_count) + "\n")
                        f3.write("c0=" + str(ratio) + "\n")

                        temporalResult = TEMPORAL_RESULT_FOR_BASH + "run_test_${datatype}_${d}_${cardinality}_opt"
                        overallResult = TEMPORAL_RESULT_FOR_BASH + "overall_run_test_${datatype}_${d}_${cardinality}_opt.txt"
                        f3.write("temporalResult=" + temporalResult + "\n")
                        f3.write("overallResult=" + overallResult + "\n")
                        f3.write("S=" + str(sim_threshold) + "\n")
                        f3.write("num_layer=" + str(len(K_List)) + "\n")
                        f3.write("# ------------------------------------------------------------------------------ \n")
                        f3.write("#     Ground-Truth \n")
                        f3.write("# ------------------------------------------------------------------------------ \n")
                        f3.write("dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt \n")
                        f3.write(
                            "tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth \n")
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
                            f3.write("L" + str(kk) + "=" + str(L_Opt_List[kk]) + "\n")

                            f3.write("dPath" + str(kk) + "=./qhull_data/Synthetic/${datatype}_${d}_"
                                                         "${cardinality}_qhull_layer_" + str(kk) + "\n")

                            f3.write("oFolder" + str(kk) + "=./result/${datatype}/Dimension_${d}_Cardinality_"
                                                           "${cardinality}_opt/result_${d}D" + str(kk) + "_${K" + str(kk)
                                     + "}_${L" + str(kk) + "}" + "\n")

                            f3.write("./alsh -alg 10 -n ${n" + str(kk) + "} -qn ${qn} -d ${d} -K ${K" + str(kk) +
                                     "} -L ${L" + str(kk) + "} -LI " + str(
                                kk + 1) + " -S ${S} -c0 ${c0} -ds ${dPath" + str(kk)
                                     + "} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -of ${oFolder" + str(
                                kk) + "}.simple_LSH \n")

                            f3.write("\n")
                        # append overall accuracy computation here
                        f3.write("# ------------------------------------------------------------------------------ \n")
                        f3.write("#     Overall-Performance \n")
                        f3.write("# ------------------------------------------------------------------------------ \n")
                        f3.write("./alsh -alg 12 -d ${d} -qn ${qn} -L1 ${num_layer} -it ${temporalResult} -ts "
                                 "${tsPath}.mip -of ${overallResult} \n")
                        f3.close()

                        # write to .sh file at save path, uni
                        f3 = open(bash_file_uni, 'w')
                        f3.write("#!/bin/bash \n")
                        f3.write("# make \n")
                        f3.write("rm *.o \n")
                        cur_data_type = data_type[ii]
                        cur_cardinality = cardinality
                        cur_dimension = dimensions[k]
                        f3.write("datatype=" + cur_data_type + "\n")
                        f3.write("cardinality=" + str(cur_cardinality) + "\n")
                        f3.write("d=" + str(cur_dimension) + "\n")
                        f3.write("qn=" + str(query_count) + "\n")
                        f3.write("c0=" + str(ratio) + "\n")

                        temporalResult = TEMPORAL_RESULT_FOR_BASH + "run_test_${datatype}_${d}_${cardinality}_uni"
                        overallResult = TEMPORAL_RESULT_FOR_BASH + "overall_run_test_${datatype}_${d}_${cardinality}_uni.txt"
                        f3.write("temporalResult=" + temporalResult + "\n")
                        f3.write("overallResult=" + overallResult + "\n")
                        f3.write("S=" + str(sim_threshold) + "\n")
                        f3.write("num_layer=" + str(len(K_List)) + "\n")
                        f3.write("# ------------------------------------------------------------------------------ \n")
                        f3.write("#     Ground-Truth \n")
                        f3.write("# ------------------------------------------------------------------------------ \n")
                        f3.write("dPath=./raw_data/Synthetic/${datatype}_${d}_${cardinality}.txt \n")
                        f3.write(
                            "tsPath=./result/result_${datatype}_${d}D_${cardinality} # path for the ground truth \n")
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
                            f3.write("L" + str(kk) + "=" + str(L_Uni_List[kk]) + "\n")

                            f3.write("dPath" + str(kk) + "=./qhull_data/Synthetic/${datatype}_${d}_"
                                                         "${cardinality}_qhull_layer_" + str(kk) + "\n")

                            f3.write("oFolder" + str(kk) + "=./result/${datatype}/Dimension_${d}_Cardinality_"
                                                           "${cardinality}_uni/result_${d}D" + str(kk) + "_${K" + str(kk)
                                     + "}_${L" + str(kk) + "}" + "\n")

                            f3.write("./alsh -alg 10 -n ${n" + str(kk) + "} -qn ${qn} -d ${d} -K ${K" + str(kk) +
                                     "} -L ${L" + str(kk) + "} -LI " + str(
                                kk + 1) + " -S ${S} -c0 ${c0} -ds ${dPath" + str(kk)
                                     + "} -qs ${qPath} -ts ${tsPath}.mip -it ${temporalResult} -of ${oFolder" + str(
                                kk) + "}.simple_LSH \n")

                            f3.write("\n")
                        # append overall accuracy computation here
                        f3.write("# ------------------------------------------------------------------------------ \n")
                        f3.write("#     Overall-Performance \n")
                        f3.write("# ------------------------------------------------------------------------------ \n")
                        f3.write("./alsh -alg 12 -d ${d} -qn ${qn} -L1 ${num_layer} -it ${temporalResult} -ts "
                                 "${tsPath}.mip -of ${overallResult} \n")
                        f3.close()
f10.close()
print("Done .\n")