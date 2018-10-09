# data_type = ["anti_correlated", "correlated", "random"]
data_type = ["correlated", "anti_correlated", "random"]
dimensions = [5]
cardinality = [100000]
query_count = [1000]
topk = 10
hashTables = ["a", "b", "c", "d", "e", "f", "g", "h", "q", "j"]
# KList = [80, 70, 70, 70, 60, 60, 60, 50, 50, 50]
# KList = [70, 65, 60, 55, 50, 45, 40, 35, 30, 25]
KList = [25, 20, 15, 10, 9, 8, 7, 6, 5, 4]

# count, hashTables KList
PARAMETER_FILE_FOLDER = "../H2_ALSH/parameters/"
SCRIPT_OUTPUT_FILE = "../H2_ALSH/parameters/Mathematica_Parameters.txt"
DATA_FOLDER = "../H2_ALSH/qhull_data/Synthetic/"
f = open(SCRIPT_OUTPUT_FILE, 'w')

for i in range(len(data_type)):
    for j in range(len(dimensions)):
        for k in range(len(cardinality)):

            K_Parameter_File = PARAMETER_FILE_FOLDER + "K_" + data_type[i] + "_" + str(dimensions[j]) + \
                               "_" + str(cardinality[k])
            L_Parameter_File = PARAMETER_FILE_FOLDER + "L_" + data_type[i] + "_" + str(dimensions[j]) + \
                               "_" + str(cardinality[k])
            f3 = open(K_Parameter_File, 'w')
            # f4 = open(L_Parameter_File, 'w')
            for m in range(len(KList)):
                f3.write(str(KList[m]) + "\n")
            f3.close()
            f4 = open(L_Parameter_File, 'w')
            f4.close()
            declare_string = data_type[i] + "_" + str(dimensions[j]) + "_" + str(cardinality[k])
            count = []
            f.write("# ------------------------------------------------------------------------------ \n")
            f.write("#     " + declare_string + " \n")
            f.write("# ------------------------------------------------------------------------------ \n")
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

                count.append(float(cur_cardinality)/float(cardinality[k]))
                f1.close()
            f.write("count = List" + str(count) + "\n")
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





