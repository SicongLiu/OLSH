import math

import decimal

# create a new context for this task
ctx = decimal.Context()

# 20 digits should be enough for everyone :D
ctx.prec = 20

def float_to_str(f):
    """
    Convert the given float to a string,
    without resorting to scientific notation
    """
    d1 = ctx.create_decimal(repr(f))
    return format(d1, 'f')


data_type = ["correlated", "anti_correlated", "random"]
# data_type = ["anti_correlated"]
dimensions = [4]
cardinality = [100000]
topk = 25
# hashTables = ["a", "b", "c", "d", "e", "f", "g", "h", "q", "j"]
hashTables = ["a", "b", "c", "d", "e", "f", "g", "h", "q", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

# hashTables = ["aaa", "bbb", "ccc", "ddd", "eee", "fff", "ggg", "hhh", "iii", "jjj", "kkk", "lll", "mmm", "nnn", "ooo", "ppp",
#               "qqq", "rrr", "sss", "ttt", "uuu", "vvv", "www", "xxx", "yyy", "zzz", "aaaa", "bbbb", "cccc", "dddd", "eeee", "ffff",
              # "gggg", "hhhh", "iiii", "jjjj", "kkkk", "llll", "mmmm", "nnnn", "oooo", "pppp", "qqqq","rrrr", "ssss", "tttt", "uuuu", "vvvv", "wwww", "xxxx"]

# count, hashTables KList
PARAMETER_FILE_FOLDER = "../H2_ALSH/parameters/"
SCRIPT_OUTPUT_FILE = "../H2_ALSH/parameters/New_Mathematica_Parameters_"
DATA_FOLDER = "../H2_ALSH/qhull_data/Synthetic/"


for j in range(len(dimensions)):
    for k in range(len(cardinality)):
        save_data_file = SCRIPT_OUTPUT_FILE + "_top_" + str(topk) + "_" + str(dimensions[j]) + "D_" + str(
            cardinality[k]) + ".txt"

        f = open(save_data_file, 'w')
        for i in range(len(data_type)):
            K_Log_List = []
            K_Log_Minus_List = []
            K_Log_Plus_List = []
            K_Log_Plus_Plus_List = []
            K_Log_Uni_List = []

            K_Parameter_File = PARAMETER_FILE_FOLDER + "K_" + data_type[i] + "_" + str(dimensions[j]) + \
                               "_" + str(cardinality[k])
            # L_Parameter_File = PARAMETER_FILE_FOLDER + "L_" + data_type[i] + "_" + str(dimensions[j]) + \
            #                    "_" + str(cardinality[k])

            # f4 = open(L_Parameter_File, 'w')
            # f4.close()
            declare_string = data_type[i] + "_" + str(dimensions[j]) + "_" + str(cardinality[k])
            count = []
            count1 = []
            f.write("# ------------------------------------------------------------------------------ \n")
            f.write("#     " + declare_string + " \n")
            f.write("# ------------------------------------------------------------------------------ \n")
            print("------------------------------------------------")
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

                count.append(float_to_str(float(cur_cardinality)/float(cardinality[k])))
                count1.append(cur_cardinality)
                k_log = math.ceil(math.log(cur_cardinality, 2))
                k_log_minus = k_log - 3
                k_log_plus = k_log + 3
                k_log_plus_plus = k_log + 6

                K_Log_List.append(k_log)
                K_Log_Minus_List.append(k_log_minus)
                K_Log_Plus_List.append(k_log_plus)
                K_Log_Plus_Plus_List.append(k_log_plus_plus)

                f1.close()
            k_log_max = max(K_Log_List)
            for m in range(topk):
                K_Log_Uni_List.append(k_log_max)

            f.write("hashTables = List" + str(hashTables) + "\n")
            f.write("count = List[" + str(', '.join(map(str, count))) + "]\n")
            f.write("count1 = List" + str(count1) + "\n")

            f.write("K_Log_List = List" + str(K_Log_List) + "\n")
            f.write("K_Log_Minus_List = List" + str(K_Log_Minus_List) + "\n")
            f.write("K_Log_Plus_List = List" + str(K_Log_Plus_List) + "\n")
            f.write("K_Log_Plus_Plus_List = List" + str(K_Log_Plus_Plus_List) + "\n")
            f.write("K_Log_Uni_List = List" + str(K_Log_Uni_List) + "\n")


            # opt_str = "NMinimize[{TotalError, totalHashUsed <= totalBudget && TotalError < 1 && a \[Element] " \
            #           "Integers && b \[Element] Integers && c \[Element] Integers && d \[Element] Integers && e " \
            #           "\[Element] Integers && f \[Element] Integers && g \[Element] Integers && h \[Element] Integers " \
            #           "&& i \[Element] Integers && j \[Element] Integers && a >= 1 " \
            #           "&& b >= 1 && c >= 1 && d >= 1 && e >= 1 && f >= 1 && g >= 1 && h >=1 && i >=1 && j >=1}, " \
            #           "{a,b,c,d,e,f,g,h,i,j}]"
            # f.write(opt_str)
            f.write("\n \n \n")
        f.close()





