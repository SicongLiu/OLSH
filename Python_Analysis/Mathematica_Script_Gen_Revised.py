# data_type = ["anti_correlated", "correlated", "random"]

# data_type = ["anti_correlated"]
# dimensions = [7]
# cardinality = [200000]
# query_count = [1000]
# topk = 14

# data_type = ["correlated"]
# dimensions = [7]
# cardinality = [200000]
# query_count = [1000]
# topk = 17

# data_type = ["random"]
# dimensions = [7]
# cardinality = [200000]
# query_count = [1000]
# topk = 13
#
# #########
#
# data_type = ["anti_correlated"]
# dimensions = [7]
# cardinality = [1000000]
# query_count = [1000]
# topk = 21
# #
# data_type = ["correlated"]
# dimensions = [7]
# cardinality = [1000000]
# query_count = [1000]
# topk = 26
#
# data_type = ["random"]
# dimensions = [7]
# cardinality = [1000000]
# query_count = [1000]
# topk = 21
#
# ##############
#
# data_type = ["anti_correlated"]
# dimensions = [7]
# cardinality = [1500000]
# query_count = [1000]
# topk = 24
# #
# data_type = ["correlated"]
# dimensions = [7]
# cardinality = [1500000]
# query_count = [1000]
# topk = 29

# data_type = ["random"]
# dimensions = [7]
# cardinality = [1500000]
# query_count = [1000]
# topk = 23
# #
# ###############
#
# data_type = ["anti_correlated"]
# dimensions = [7]
# cardinality = [2000000]
# query_count = [1000]
# topk = 26
#
# data_type = ["correlated"]
# dimensions = [7]
# cardinality = [2000000]
# query_count = [1000]
# topk = 31
#
data_type = ["random"]
dimensions = [4]
cardinality = [2000000]
query_count = [1000]
topk = 16

import math

hashTables = ["a", "b", "c", "d", "e", "f", "g", "h", "q", "j"]
# KList = [80, 70, 70, 70, 60, 60, 60, 50, 50, 50]
# KList = [70, 65, 60, 55, 50, 45, 40, 35, 30, 25]
KList = [25, 20, 15, 10, 9, 8, 7, 6, 5, 4]

# count, hashTables KList
PARAMETER_FILE_FOLDER = "../H2_ALSH/parameters/"

DATA_FOLDER = "../H2_ALSH/qhull_data/Synthetic/"
SCRIPT_OUTPUT_DIR = "../H2_ALSH/parameters/4D_sum/"

for i in range(len(data_type)):
    for j in range(len(dimensions)):
        for k in range(len(cardinality)):
            SCRIPT_OUTPUT_FILE = SCRIPT_OUTPUT_DIR + data_type[i] + "_" + str(dimensions[j]) + \
                               "_" + str(cardinality[k]) + "_" + str(topk) + "_parameters.txt"
            f = open(SCRIPT_OUTPUT_FILE, 'w')
            K_Parameter_File = PARAMETER_FILE_FOLDER + "K_" + data_type[i] + "_" + str(dimensions[j]) + \
                               "_" + str(cardinality[k])
            # L_Parameter_File = PARAMETER_FILE_FOLDER + "L_" + data_type[i] + "_" + str(dimensions[j]) + \
            #                    "_" + str(cardinality[k])
            f3 = open(K_Parameter_File, 'w')
            # f4 = open(L_Parameter_File, 'w')
            for m in range(len(KList)):
                f3.write(str(KList[m]) + "\n")
            f3.close()
            # f4 = open(L_Parameter_File, 'w')
            # f4.close()
            declare_string = data_type[i] + "_" + str(dimensions[j]) + "_" + str(cardinality[k])
            count = []
            count1 = []
            K_Log_List = []
            K_Log_Minus_List = []
            K_Log_Plus_List = []
            K_Log_Plus_Plus_List = []
            f.write("# ------------------------------------------------------------------------------ \n")
            f.write("#     " + declare_string + " \n")
            f.write("# ------------------------------------------------------------------------------ \n")

            cum_card_count = []
            for m in range(topk):
                input_file = DATA_FOLDER + data_type[i] + "_" + str(dimensions[j]) + "_" + str(cardinality[k]) + \
                             "_qhull_layer_" + str(m)
                f1 = open(input_file, 'r')
                lines = f1.readlines()
                first_line = lines[0]
                second_line = lines[1]

                cur_dimension = int(first_line.split('\n')[0])
                cur_cardinality = int(second_line.split('\n')[0])
                if m == 0 :
                    cum_card_count.append(cur_cardinality)
                else:
                    cum_card_count.append(cur_cardinality + cum_card_count[m-1])
                f1.close()

            for m in range(topk):
                input_file = DATA_FOLDER + data_type[i] + "_" + str(dimensions[j]) + "_" + str(cardinality[k]) + \
                             "_qhull_layer_" + str(m)
                f1 = open(input_file, 'r')
                lines = f1.readlines()
                first_line = lines[0]
                second_line = lines[1]

                cur_dimension = int(first_line.split('\n')[0])
                cur_cardinality = int(second_line.split('\n')[0])
                assert cur_dimension == dimensions[j]

                count.append(cur_cardinality)
                # count1.append(float(cur_cardinality)/float(cardinality[k]))
                count1.append(float(cur_cardinality) / float(cum_card_count[m]))

                k_log = math.ceil(math.log(cur_cardinality, 2))
                k_log_minus = k_log - 3
                k_log_plus = k_log + 3
                k_log_plus_plus = k_log + 6

                K_Log_List.append(k_log)
                K_Log_Minus_List.append(k_log_minus)
                K_Log_Plus_List.append(k_log_plus)
                K_Log_Plus_Plus_List.append(k_log_plus_plus)
                f1.close()

            f.write("count = List" + str(count) + "\n")
            f.write("count1 = List" + str(count1) + "\n")
            f.write("KList = List" + str(K_Log_List) + "\n")
            f.write("KList = List" + str(K_Log_Minus_List) + "\n")
            f.write("KList = List" + str(K_Log_Plus_List) + "\n")
            f.write("KList = List" + str(K_Log_Plus_Plus_List) + "\n")
            f.write("hashTables = List[" + ','.join(hashTables) + "] \n")
            # f.write("hashTables = List" + str(hashTables) + "\n")
            f.write("KList = List" + str(KList) + "\n")
            opt_str = "NMinimize[{TotalError, totalHashUsed <= totalBudget && TotalError < 1 && a \[Element] " \
                      "Integers && b \[Element] Integers && c \[Element] Integers && d \[Element] Integers && e " \
                      "\[Element] Integers && f \[Element] Integers && g \[Element] Integers && h \[Element] Integers " \
                      "&& i \[Element] Integers && j \[Element] Integers && a >= 1 " \
                      "&& b >= 1 && c >= 1 && d >= 1 && e >= 1 && f >= 1 && g >= 1 && h >=1 && i >=1 && j >=1}, " \
                      "{a,b,c,d,e,f,g,h,i,j}]"
            f.write("\n \n \n")
            f.close()






