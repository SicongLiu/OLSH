import math
import numpy as np
from openpyxl import load_workbook
import random
import re


def separate_string(input_string):
    items = []
    match = re.match(r"([a-z]+)([0-9]+)", input_string, re.I)
    if match:
        items = match.groups()
    return items


def column_row_index(input_string, column_dist):
    items = separate_string(input_string)
    column_index = items[0]
    row_index = int(items[1]) + column_dist
    return column_index + str(row_index)


def compute_weights(data_list_, top_m_):
    data_list_ = np.asarray(data_list_)
    contribution_list = []
    weight_list_ = []
    data_list_cumsum = np.cumsum(data_list_)
    for i in range(top_m_):
        c_h = data_list_[i]
        temp_contribution = 0
        for j in range(i, top_m_):
            denominator = data_list_cumsum[j]
            temp_contribution = 1.0 * temp_contribution + (1.0 * c_h/denominator)
        contribution_list.append(temp_contribution)
    sum_contribution = sum(contribution_list)
    for i in range(top_m_):
        temp_weight = (1.0 * contribution_list[i])/sum_contribution
        weight_list_.append(temp_weight)
    return weight_list_


def post_optimization_opt(collision_probility_, weight_list_, total_error_, data_list_, K_List_, L_List_, hash_used_, hash_budget_):
    smallest = min(data_list_)
    smallest_index = data_list_.index(min(data_list_))

    # total_error = 0.412502654
    total_error_gain = 0
    flag = False
    while hash_used_ + smallest <= hash_budget_:
        # the condition of improvement is to check if the total error rate drops

        # loop through, keep track of hash-relocation and error rate drop
        # find the biggest error gain, while keep hash-resources constraints
        # update hash_used, LList
        delta_error_list = []
        for i in range(len(data_list_)):
            cur_k = K_List_[i]
            cur_l = L_List_[i]
            c_old = math.pow((1 - math.pow(collision_probility_, cur_k)), cur_l)

            # each time increment hash layer by 1
            c_new = math.pow((1 - math.pow(collision_probility_, cur_k)), (cur_l+1))
            delta_error_list.append((c_old - c_new))

        # sort and check each delta_error
        delta_error_list = np.asarray(delta_error_list)
        # sort in descending order
        sorted_index = delta_error_list.argsort()[::-1][:len(delta_error_list)]
        sorted_pivot = 0
        while sorted_pivot < len(sorted_index):
            cur_index = sorted_index[sorted_pivot]

            # each time increment hash layer by 1
            # temp_hash_used = hash_used + (LList[cur_index] + 1) * data_list[cur_index]
            temp_hash_used = hash_used_ + data_list_[cur_index]
            if temp_hash_used < hash_budget_:
                L_List_[cur_index] = L_List_[cur_index] + 1
                hash_used_ = hash_used_ + data_list_[cur_index]
                break
            sorted_pivot = sorted_pivot + 1
    total_error = 0
    total_hash_used = 0
    for i in range(len(L_List_)):
        cur_k = K_List_[i]
        cur_l = L_List_[i]
        total_error = total_error + weight_list_[i] * math.pow((1 - math.pow(collision_probility_, cur_k)), cur_l)
        total_hash_used = total_hash_used + data_list_[i] * cur_l
    # print("Updated total error: " + str(total_error))
    # print("total hash used: " + str(total_hash_used))
    # print("Optimized approach done")
    return L_List_


####################################################################################
# for uniformly distributed approach
# uniformly pick one that fits the current hash budget instead of the one minimizing total error rate
def post_optimization_uni(data_list_, L_List_, hash_used_, hash_budget_):
    flag = False
    smallest = min(data_list_)
    data_list_ = np.asarray(data_list_)
    while hash_used_ + smallest <= hash_budget_:
        # sort in descending order
        sorted_index = data_list_.argsort()[::-1][:len(data_list_)]

        temp_pivot_list = []
        # first find all the allow current hash re-allocation
        for i in range(len(sorted_index)):
            temp_pivot_index = sorted_index[i]
            if hash_used_ + data_list_[temp_pivot_index] <= hash_budget_:
                temp_pivot_list.append(temp_pivot_index)
        # randomly pick one from those
        cur_pivot = random.choice(temp_pivot_list)
        # update L_Uni_List, hash_used
        L_List_[cur_pivot] = L_List_[cur_pivot] + 1
        hash_used_ = hash_used_ + data_list_[cur_pivot]
    return L_List_


####################################################################################
# types = ["log", "log_minus", "log_plus", "log_plus_plus", "uni"]
# Data_Types = ['anti_correlated', 'correlated', 'random']
types = ["log", "log_minus", "log_plus", "log_plus_plus", "uni"]
Data_Types = ['anti_correlated']
top_m_cell_anti = 'E1'
top_m_cell_corr = 'V1'
top_m_cell_rand = 'AL1'


# need to update budget cell per data type
budget_cell_anti = 'B4'
budget_cell_corr = 'S4'
budget_cell_rand = 'AI4'


cardinality_cell = 'B2'
top_m_cardinality_anti = 0
top_m_cardinality_corr = 0
top_m_cardinality_random = 0

data_anti_list_28 = ['J6', 'J33', 'J42', 'J69', 'J78', 'J105', 'J114', 'J141', 'J150', 'J177']
k_ranges_anti_28 = ['E6', 'E33', 'E42', 'E69', 'E78', 'E105', 'E114', 'E141', 'E150', 'E177']
l_ranges_opt_anti_28 = ['F6', 'F33', 'F42', 'F69', 'F78', 'F105', 'F114', 'F141', 'F150', 'F177']
l_ranges_max_anti_28 = ['G6', 'G33', 'G42', 'G69', 'G78', 'G105', 'G114', 'G141', 'G150', 'G177']
l_ranges_uni_anti_28 = ['H6', 'H33', 'H42', 'H69', 'H78', 'H105', 'H114', 'H141', 'H150', 'H177']
hash_used_anti_opt_cells_28 = ['I34', 'I70', 'I106', 'I142', 'I178']
hash_used_anti_uni_cells_28 = ['O34', 'O70', 'O106', 'O142', 'O178']


data_corr_list_33 = ['AA6', 'AA38', 'AA42', 'AA74', 'AA78', 'AA110', 'AA114', 'AA146', 'AA150', 'AA182']
k_ranges_corr_33 = ['V6', 'V38', 'V42', 'V74', 'V78', 'V110', 'V114', 'V146', 'V150', 'V182']
l_ranges_opt_corr_33 = ['W6', 'W38', 'W42', 'W74', 'W78', 'W110', 'W114', 'W146', 'W150', 'W182']
l_ranges_max_corr_33 = ['X6', 'X38', 'X42', 'X74', 'X78', 'X110', 'X114', 'X146', 'X150', 'X182']
l_ranges_uni_corr_33 = ['Y6', 'Y38', 'Y42', 'Y74', 'Y78', 'Y110', 'Y114', 'Y146', 'Y150', 'Y182']
hash_used_corr_opt_cells_33 = ['Z39', 'Z75', 'Z111', 'Z147', 'Z183']
hash_used_corr_uni_cells_33 = ['AF39', 'AF75', 'AF111', 'AF147', 'AF183']


data_random_list_27 = ['AQ6', 'AQ32', 'AQ42', 'AQ68', 'AQ78', 'AQ104', 'AQ114', 'AQ140', 'AQ150', 'AQ176']
k_ranges_random_27 = ['AL6', 'AL32', 'AL42', 'AL68', 'AL78', 'AL104', 'AL114', 'AL140', 'AL150', 'AL176']
l_ranges_opt_random_27 = ['AM6', 'AM32', 'AM42', 'AM68', 'AM78', 'AM104', 'AM114', 'AM140', 'AM150', 'AM176']
l_ranges_max_random_27 = ['AN6', 'AN32', 'AN42', 'AN68', 'AN78', 'AN104', 'AN114', 'AN140', 'AN150', 'AN176']
l_ranges_uni_random_27 = ['AO6', 'AO32', 'AO42', 'AO68', 'AO78', 'AO104', 'AO114', 'AO140', 'AO150', 'AO176']
hash_used_rand_opt_cells_27 = ['AP33', 'AP69', 'AP105', 'AP141', 'AP177']
hash_used_rand_uni_cells_27 = ['AV33', 'AV69', 'AV105', 'AV141', 'AV177']






data_anti_list_34 = ['J6', 'J39', 'J53', 'J86', 'J100', 'J133', 'J147', 'J180', 'J194', 'J227']
k_ranges_anti_34 = ['E6', 'E39', 'E53', 'E86', 'E100', 'E133', 'E147', 'E180', 'E194', 'E227']
l_ranges_opt_anti_34 = ['F6', 'F39', 'F53', 'F86', 'F100', 'F133', 'F147', 'F180', 'F194', 'F227']
l_ranges_max_anti_34 = ['G6', 'G39', 'G53', 'G86', 'G100', 'G133', 'G147', 'G180', 'G194', 'G227']
l_ranges_uni_anti_34 = ['H6', 'H39', 'H53', 'H86', 'H100', 'H133', 'H147', 'H180', 'H194', 'H227']
hash_used_anti_opt_cells_34 = ['I40', 'I87', 'I134', 'I181', 'I228']
hash_used_anti_uni_cells_34 = ['O40', 'O87', 'O134', 'O181', 'O228']


data_corr_list_40 = ['AA6', 'AA45', 'AA53', 'AA92', 'AA100', 'AA139', 'AA147', 'AA186', 'AA194', 'AA233']
k_ranges_corr_40 = ['V6', 'V45', 'V53', 'V92', 'V100', 'V139', 'V147', 'V186', 'V194', 'V233']
l_ranges_opt_corr_40 = ['W6', 'W45', 'W53', 'W92', 'W100', 'W139', 'W147', 'W186', 'W194', 'W233']
l_ranges_max_corr_40 = ['X6', 'X45', 'X53', 'X92', 'X100', 'X139', 'X147', 'X186', 'X194', 'X233']
l_ranges_uni_corr_40 = ['Y6', 'Y45', 'Y53', 'Y92', 'Y100', 'Y139', 'Y147', 'Y186', 'Y194', 'Y233']
hash_used_corr_opt_cells_40 = ['Z46', 'Z93', 'Z140', 'Z187', 'Z234']
hash_used_corr_uni_cells_40 = ['AF46', 'AF93', 'AF140', 'AF187', 'AF234']


data_random_list_32 = ['AQ6', 'AQ37', 'AQ53', 'AQ84', 'AQ91', 'AQ122', 'AQ129', 'AQ160', 'AQ167', 'AQ198']
k_ranges_random_32 = ['AL6', 'AL37', 'AL53', 'AL84', 'AL91', 'AL122', 'AL129', 'AL160', 'AL167', 'AL198']
l_ranges_opt_random_32 = ['AM6', 'AM37', 'AM53', 'AM84', 'AM91', 'AM122', 'AM129', 'AM160', 'AM167', 'AM198']
l_ranges_max_random_32 = ['AN6', 'AN37', 'AN53', 'AN84', 'AN91', 'AN122', 'AN129', 'AN160', 'AN167', 'AN198']
l_ranges_uni_random_32 = ['AO6', 'AO37', 'AO53', 'AO84', 'AO91', 'AO122', 'AO129', 'AO160', 'AO167', 'AO198']
hash_used_rand_opt_cells_32 = ['AP38', 'AP85', 'AP123', 'AP161', 'AP199']
hash_used_rand_uni_cells_32 = ['AV38', 'AV85', 'AV123', 'AV161', 'AV199']





data_anti_list_38 = ['J6', 'J43', 'J51', 'J88', 'J96', 'J133', 'J141', 'J178', 'J186', 'J223']
k_ranges_anti_38 = ['E6', 'E43', 'E51', 'E88', 'E96', 'E133', 'E141', 'E178', 'E186', 'E223']
l_ranges_opt_anti_38 = ['F6', 'F43', 'F51', 'F88', 'F96', 'F133', 'F141', 'F178', 'F186', 'F223']
l_ranges_max_anti_38 = ['G6', 'G43', 'G51', 'G88', 'G96', 'G133', 'G141', 'G178', 'G186', 'G223']
l_ranges_uni_anti_38 = ['H6', 'H43', 'H51', 'H88', 'H96', 'H133', 'H141', 'H178', 'H186', 'H223']
hash_used_anti_opt_cells_38 = ['I44', 'I89', 'I134', 'I179', 'I224']
hash_used_anti_uni_cells_38 = ['O44', 'O89', 'O134', 'O179', 'O224']


data_corr_list_45 = ['AA6', 'AA50', 'AA58', 'AA102', 'AA110', 'AA154', 'AA162', 'AA206', 'AA214', 'AA258']
k_ranges_corr_45 = ['V6', 'V50', 'V58', 'V102', 'V110', 'V154', 'V162', 'V206', 'V214', 'V258']
l_ranges_opt_corr_45 = ['W6', 'W50', 'W58', 'W102', 'W110', 'W154', 'W162', 'W206', 'W214', 'W258']
l_ranges_max_corr_45 = ['X6', 'X50', 'X58', 'X102', 'X110', 'X154', 'X162', 'X206', 'X214', 'X258']
l_ranges_uni_corr_45 = ['Y6', 'Y50', 'Y58', 'Y102', 'Y110', 'Y154', 'Y162', 'Y206', 'Y214', 'Y258']
hash_used_corr_opt_cells_45 = ['Z51', 'Z103', 'Z155', 'Z207', 'Z259']
hash_used_corr_uni_cells_45 = ['AF51', 'AF103', 'AF155', 'AF207', 'AF259']


data_random_list_37 = ['AQ6', 'AQ42', 'AQ50', 'AQ86', 'AQ94', 'AQ130', 'AQ138', 'AQ174', 'AQ182', 'AQ218']
k_ranges_random_37 = ['AL6', 'AL42', 'AL50', 'AL86', 'AL94', 'AL130', 'AL138', 'AL174', 'AL182', 'AL218']
l_ranges_opt_random_37 = ['AM6', 'AM42', 'AM50', 'AM86', 'AM94', 'AM130', 'AM138', 'AM174', 'AM182', 'AM218']
l_ranges_max_random_37 = ['AN6', 'AN42', 'AN50', 'AN86', 'AN94', 'AN130', 'AN138', 'AN174', 'AN182', 'AN218']
l_ranges_uni_random_37 = ['AO6', 'AO42', 'AO50', 'AO86', 'AO94', 'AO130', 'AO138', 'AO174', 'AO182', 'AO218']
hash_used_rand_opt_cells_37 = ['AP43', 'AP87', 'AP131', 'AP175', 'AP219']
hash_used_rand_uni_cells_37 = ['AV43', 'AV87', 'AV131', 'AV175', 'AV219']




data_anti_list_41 = ['J6', 'J46', 'J54', 'J94', 'J102', 'J142', 'J150', 'J190', 'J198', 'J238']
k_ranges_anti_41 = ['E6', 'E46', 'E54', 'E94', 'E102', 'E142', 'E150', 'E190', 'E198', 'E238']
l_ranges_opt_anti_41 = ['F6', 'F46', 'F54', 'F94', 'F102', 'F142', 'F150', 'F190', 'F198', 'F238']
l_ranges_max_anti_41 = ['G6', 'G46', 'G54', 'G94', 'G102', 'G142', 'G150', 'G190', 'G198', 'G238']
l_ranges_uni_anti_41 = ['H6', 'H46', 'H54', 'H94', 'H102', 'H142', 'H150', 'H190', 'H198', 'H238']
hash_used_anti_opt_cells_41 = ['I47', 'I95', 'I142', 'I191', 'I239']
hash_used_anti_uni_cells_41 = ['O47', 'O95', 'O142', 'O191', 'O239']


data_corr_list_49 = ['AA6', 'AA54', 'AA62', 'AA110', 'AA118', 'AA166', 'AA174', 'AA222', 'AA230', 'AA278']
k_ranges_corr_49 = ['V6', 'V54', 'V62', 'V110', 'V118', 'V166', 'V174', 'V222', 'V230', 'V278']
l_ranges_opt_corr_49 = ['W6', 'W54', 'W62', 'W110', 'W118', 'W166', 'W174', 'W222', 'W230', 'W278']
l_ranges_max_corr_49 = ['X6', 'X54', 'X62', 'X110', 'X118', 'X166', 'X174', 'X222', 'X230', 'X278']
l_ranges_uni_corr_49 = ['Y6', 'Y54', 'Y62', 'Y110', 'Y118', 'Y166', 'Y174', 'Y222', 'Y230', 'Y278']
hash_used_corr_opt_cells_49 = ['Z55', 'Z111', 'Z167', 'Z223', 'Z279']
hash_used_corr_uni_cells_49 = ['AF55', 'AF111', 'AF167', 'AF223', 'AF279']


data_random_list_40 = ['AQ6', 'AQ45', 'AQ53', 'AQ92', 'AQ100', 'AQ139', 'AQ147', 'AQ186', 'AQ194', 'AQ233']
k_ranges_random_40 = ['AL6', 'AL45', 'AL53', 'AL92', 'AL100', 'AL139', 'AL147', 'AL186', 'AL194', 'AL233']
l_ranges_opt_random_40 = ['AM6', 'AM45', 'AM53', 'AM92', 'AM100', 'AM139', 'AM147', 'AM186', 'AM194', 'AM233']
l_ranges_max_random_40 = ['AN6', 'AN45', 'AN53', 'AN92', 'AN100', 'AN139', 'AN147', 'AN186', 'AN194', 'AN233']
l_ranges_uni_random_40 = ['AO6', 'AO45', 'AO53', 'AO92', 'AO100', 'AO139', 'AO147', 'AO186', 'AO194', 'AO233']
hash_used_rand_opt_cells_40 = ['AP46', 'AP93', 'AP140', 'AP187', 'AP234']
hash_used_rand_uni_cells_40 = ['AV46', 'AV93', 'AV140', 'AV187', 'AV234']


collision_probility = 0.9
total_error = 0
# K_log_list_start_cell = ['E6', 'V6', 'AL6']
# K_log_minus_list_start_cell = ['']
# K_log_plus_list_start_cell = []
# K_log_plus_plus_list_start_cell = []
# K_log_uni_list_start_cell = []

####################################################################################

# dimensions = [2, 3, 4, 5, 6, 7]
dimensions = [4]
excel_file_dir = './'

# for each excel file
for i in range(len(dimensions)):
    cur_d = dimensions[i]
    # excel_file_name = excel_file_dir + 'Checkpoint_Result_Nov_26_' + str(cur_d) + 'D_test.xlsx'
    excel_file_name = excel_file_dir + str(cur_d) + 'D.xlsx'
    wb = load_workbook(filename=excel_file_name, data_only=True)
    wb1 = load_workbook(filename=excel_file_name)
    wss = wb.get_sheet_names()

    for wwss in wss:
        print(wwss)
        ws = wb.get_sheet_by_name(wwss)
        ws1 = wb1.get_sheet_by_name(wwss)
        top_m_anti = ws[top_m_cell_anti].value
        top_m_corr = ws[top_m_cell_corr].value
        top_m_rand = ws[top_m_cell_rand].value
        # ws = wb.get_sheet_by_name(wss[0])
        # ws1 = wb1.get_sheet_by_name(wss[0])
        # top_m = ws[top_m_cell].value
        # print("Sheet name: " + str(ws) + " top-m : " + str(top_m))
        hash_budget_anti = ws[budget_cell_anti].value
        hash_budget_corr = ws[budget_cell_corr].value
        hash_budget_rand = ws[budget_cell_rand].value
        total_cardinality = ws[cardinality_cell].value
        if top_m_anti == 28:
            top_m_cardinality_anti_cell = 'J16'
            top_m_cardinality_anti = ws[top_m_cardinality_anti_cell].value
            hash_used_anti_opt_cells = hash_used_anti_opt_cells_28
            hash_used_anti_uni_cells = hash_used_anti_uni_cells_28
            data_anti_list = data_anti_list_28
            k_ranges_anti = k_ranges_anti_28
            l_ranges_opt_anti = l_ranges_opt_anti_28
            l_ranges_max_anti = l_ranges_max_anti_28
            l_ranges_uni_anti = l_ranges_uni_anti_28

            top_m_cardinality_corr_cell = 'AA16'
            top_m_cardinality_corr = ws[top_m_cardinality_corr_cell].value
            hash_used_corr_opt_cells = hash_used_corr_opt_cells_33
            hash_used_corr_uni_cells = hash_used_corr_uni_cells_33
            data_corr_list = data_corr_list_33
            k_ranges_corr = k_ranges_corr_33
            l_ranges_opt_corr = l_ranges_opt_corr_33
            l_ranges_max_corr = l_ranges_max_corr_33
            l_ranges_uni_corr = l_ranges_uni_corr_33

            top_m_cardinality_random_cell = 'AQ16'
            top_m_cardinality_random = ws[top_m_cardinality_random_cell].value
            hash_used_rand_opt_cells = hash_used_rand_opt_cells_27
            hash_used_rand_uni_cells = hash_used_rand_uni_cells_27
            data_random_list = data_random_list_27
            k_ranges_random = k_ranges_random_27
            l_ranges_opt_random = l_ranges_opt_random_27
            l_ranges_max_random = l_ranges_max_random_27
            l_ranges_uni_random = l_ranges_uni_random_27
        elif top_m_anti == 34:
            top_m_cardinality_anti_cell = 'J31'
            top_m_cardinality_anti = ws[top_m_cardinality_anti_cell].value
            hash_used_anti_opt_cells = hash_used_anti_opt_cells_34
            hash_used_anti_uni_cells = hash_used_anti_uni_cells_34
            data_anti_list = data_anti_list_34
            k_ranges_anti = k_ranges_anti_34
            l_ranges_opt_anti = l_ranges_opt_anti_34
            l_ranges_max_anti = l_ranges_max_anti_34
            l_ranges_uni_anti = l_ranges_uni_anti_34

            top_m_cardinality_corr_cell = 'AA31'
            top_m_cardinality_corr = ws[top_m_cardinality_corr_cell].value
            hash_used_corr_opt_cells = hash_used_corr_opt_cells_40
            hash_used_corr_uni_cells = hash_used_corr_uni_cells_40
            data_corr_list = data_corr_list_40
            k_ranges_corr = k_ranges_corr_40
            l_ranges_opt_corr = l_ranges_opt_corr_40
            l_ranges_max_corr = l_ranges_max_corr_40
            l_ranges_uni_corr = l_ranges_uni_corr_40

            top_m_cardinality_random_cell = 'AQ31'
            top_m_cardinality_random = ws[top_m_cardinality_random_cell].value
            hash_used_rand_opt_cells = hash_used_rand_opt_cells_32
            hash_used_rand_uni_cells = hash_used_rand_uni_cells_32
            data_random_list = data_random_list_32
            k_ranges_random = k_ranges_random_32
            l_ranges_opt_random = l_ranges_opt_random_32
            l_ranges_max_random = l_ranges_max_random_32
            l_ranges_uni_random = l_ranges_uni_random_32
        elif top_m_anti == 38:
            top_m_cardinality_anti_cell = 'J31'
            top_m_cardinality_anti = ws[top_m_cardinality_anti_cell].value
            hash_used_anti_opt_cells = hash_used_anti_opt_cells_38
            hash_used_anti_uni_cells = hash_used_anti_uni_cells_38
            data_anti_list = data_anti_list_38
            k_ranges_anti = k_ranges_anti_38
            l_ranges_opt_anti = l_ranges_opt_anti_38
            l_ranges_max_anti = l_ranges_max_anti_38
            l_ranges_uni_anti = l_ranges_uni_anti_38

            top_m_cardinality_corr_cell = 'AA31'
            top_m_cardinality_corr = ws[top_m_cardinality_corr_cell].value
            hash_used_corr_opt_cells = hash_used_corr_opt_cells_45
            hash_used_corr_uni_cells = hash_used_corr_uni_cells_45
            data_corr_list = data_corr_list_45
            k_ranges_corr = k_ranges_corr_45
            l_ranges_opt_corr = l_ranges_opt_corr_45
            l_ranges_max_corr = l_ranges_max_corr_45
            l_ranges_uni_corr = l_ranges_uni_corr_45

            top_m_cardinality_random_cell = 'AQ31'
            top_m_cardinality_random = ws[top_m_cardinality_random_cell].value
            hash_used_rand_opt_cells = hash_used_rand_opt_cells_37
            hash_used_rand_uni_cells = hash_used_rand_uni_cells_37
            data_random_list = data_random_list_37
            k_ranges_random = k_ranges_random_37
            l_ranges_opt_random = l_ranges_opt_random_37
            l_ranges_max_random = l_ranges_max_random_37
            l_ranges_uni_random = l_ranges_uni_random_37
        else: # 41
            top_m_cardinality_anti_cell = 'J56'
            top_m_cardinality_anti = ws[top_m_cardinality_anti_cell].value
            hash_used_anti_opt_cells = hash_used_anti_opt_cells_41
            hash_used_anti_uni_cells = hash_used_anti_uni_cells_41
            data_anti_list = data_anti_list_41
            k_ranges_anti = k_ranges_anti_41
            l_ranges_opt_anti = l_ranges_opt_anti_41
            l_ranges_max_anti = l_ranges_max_anti_41
            l_ranges_uni_anti = l_ranges_uni_anti_41

            top_m_cardinality_corr_cell = 'AA56'
            top_m_cardinality_corr = ws[top_m_cardinality_corr_cell].value
            hash_used_corr_opt_cells = hash_used_corr_opt_cells_49
            hash_used_corr_uni_cells = hash_used_corr_uni_cells_49
            data_corr_list = data_corr_list_49
            k_ranges_corr = k_ranges_corr_49
            l_ranges_opt_corr = l_ranges_opt_corr_49
            l_ranges_max_corr = l_ranges_max_corr_49
            l_ranges_uni_corr = l_ranges_uni_corr_49

            top_m_cardinality_random_cell = 'AQ56'
            top_m_cardinality_random = ws[top_m_cardinality_random_cell].value
            hash_used_rand_opt_cells = hash_used_rand_opt_cells_40
            hash_used_rand_uni_cells = hash_used_rand_uni_cells_40
            data_random_list = data_random_list_40
            k_ranges_random = k_ranges_random_40
            l_ranges_opt_random = l_ranges_opt_random_40
            l_ranges_max_random = l_ranges_max_random_40
            l_ranges_uni_random = l_ranges_uni_random_40

        data_anti = []
        data_corr = []
        data_random = []
        # within each excel file, for each data type
        for j in range(len(Data_Types)):
            # read data list
            data_anti_list_start = data_anti_list[0]
            data_anti_list_end = data_anti_list[1]

            data_corr_list_start = data_corr_list[0]
            data_corr_list_end = data_corr_list[1]

            data_random_list_start = data_random_list[0]
            data_random_list_end = data_random_list[1]

            for columns in ws[data_anti_list_start: data_anti_list_end]:
                for cell in columns:
                    data_anti.append(cell.value)

            for columns in ws[data_corr_list_start: data_corr_list_end]:
                for cell in columns:
                    data_corr.append(cell.value)

            for columns in ws[data_random_list_start: data_random_list_end]:
                for cell in columns:
                    data_random.append(cell.value)

            weight_anti = compute_weights(data_anti, len(data_anti))
            weight_corr = compute_weights(data_corr, len(data_corr))
            weight_random = compute_weights(data_random, len(data_random))

            # for each type, log, log_minus, log_plus, etc
            for jj in range(types.__len__()):
                # read k and l
                type_name = types[jj]
                start = 2 * jj
                end = 2 * jj + 1
                k_anti = []
                for columns in ws[k_ranges_anti[start]: k_ranges_anti[end]]:
                    for cell in columns:
                        k_anti.append(cell.value)

                l_anti_opt = []
                for columns in ws[l_ranges_opt_anti[start]: l_ranges_opt_anti[end]]:
                    for cell in columns:
                        l_anti_opt.append(cell.value)

                l_anti_max = []
                for columns in ws[l_ranges_max_anti[start]: l_ranges_max_anti[end]]:
                    for cell in columns:
                        l_anti_max.append(cell.value)

                l_anti_uni = []
                for columns in ws[l_ranges_uni_anti[start]: l_ranges_uni_anti[end]]:
                    for cell in columns:
                        l_anti_uni.append(cell.value)

                # read data type correlated
                k_corr = []
                for columns in ws[k_ranges_corr[start]: k_ranges_corr[end]]:
                    for cell in columns:
                        k_corr.append(cell.value)

                l_corr_opt = []
                for columns in ws[l_ranges_opt_corr[start]: l_ranges_opt_corr[end]]:
                    for cell in columns:
                        l_corr_opt.append(cell.value)

                l_corr_max = []
                for columns in ws[l_ranges_max_corr[start]: l_ranges_max_corr[end]]:
                    for cell in columns:
                        l_corr_max.append(cell.value)

                l_corr_uni = []
                for columns in ws[l_ranges_uni_corr[start]: l_ranges_uni_corr[end]]:
                    for cell in columns:
                        l_corr_uni.append(cell.value)

                # read data type random
                k_random = []
                for columns in ws[k_ranges_random[start]: k_ranges_random[end]]:
                    for cell in columns:
                        k_random.append(cell.value)

                l_random_opt = []
                for columns in ws[l_ranges_opt_random[start]: l_ranges_opt_random[end]]:
                    for cell in columns:
                        l_random_opt.append(cell.value)

                l_random_max = []
                for columns in ws[l_ranges_max_random[start]: l_ranges_max_random[end]]:
                    for cell in columns:
                        l_random_max.append(cell.value)

                l_random_uni = []
                for columns in ws[l_ranges_uni_random[start]: l_ranges_uni_random[end]]:
                    for cell in columns:
                        l_random_uni.append(cell.value)

                hash_used_anti_opt_cell = hash_used_anti_opt_cells[jj]
                hash_used_corr_opt_cell = hash_used_corr_opt_cells[jj]
                hash_used_random_opt_cell = hash_used_rand_opt_cells[jj]

                hash_used_anti_opt = ws[hash_used_anti_opt_cell].value
                hash_used_corr_opt = ws[hash_used_corr_opt_cell].value
                hash_used_random_opt = ws[hash_used_random_opt_cell].value

                # update LList
                l_anti_opt = post_optimization_opt(collision_probility, weight_anti, total_error, data_anti, k_anti, l_anti_opt,
                                               hash_used_anti_opt, hash_budget_anti)
                l_corr_opt = post_optimization_opt(collision_probility, weight_anti, total_error, data_corr, k_corr, l_corr_opt,
                                               hash_used_corr_opt, hash_budget_corr)
                l_random_opt = post_optimization_opt(collision_probility, weight_anti, total_error, data_random, k_anti, l_random_opt,
                                               hash_used_random_opt, hash_budget_rand)

                hash_used_anti_uni_cell = hash_used_anti_uni_cells[jj]
                hash_used_corr_uni_cell = hash_used_corr_uni_cells[jj]
                hash_used_random_uni_cell = hash_used_rand_uni_cells[jj]

                hash_used_anti_uni = ws[hash_used_anti_uni_cell].value
                hash_used_corr_uni = ws[hash_used_corr_uni_cell].value
                hash_used_random_uni = ws[hash_used_random_uni_cell].value

                l_anti_uni = post_optimization_uni(data_anti, l_anti_uni, hash_used_anti_uni, hash_budget_anti)
                l_corr_uni = post_optimization_uni(data_corr, l_corr_uni, hash_used_corr_uni, hash_budget_corr)
                l_random_uni = post_optimization_uni(data_random, l_random_uni, hash_used_random_uni, hash_budget_rand)

                # write udpate LList back to excel file
                for kk in range(len(l_anti_opt)):
                    cur_cell_anti_opt = column_row_index(l_ranges_opt_anti[start], kk)
                    cur_cell_anti_uni = column_row_index(l_ranges_uni_anti[start], kk)
                    ws1[cur_cell_anti_opt] = l_anti_opt[kk]
                    ws1[cur_cell_anti_uni] = l_anti_uni[kk]

                for kk in range(len(l_corr_opt)):
                    cur_cell_corr_opt = column_row_index(l_ranges_opt_corr[start], kk)
                    cur_cell_corr_uni = column_row_index(l_ranges_uni_corr[start], kk)
                    ws1[cur_cell_corr_opt] = l_corr_opt[kk]
                    ws1[cur_cell_corr_uni] = l_corr_uni[kk]

                for kk in range(len(l_random_opt)):
                    cur_cell_random_opt = column_row_index(l_ranges_opt_random[start], kk)
                    cur_cell_random_uni = column_row_index(l_ranges_uni_random[start], kk)
                    ws1[cur_cell_random_uni] = l_random_uni[kk]
                    ws1[cur_cell_random_opt] = l_random_opt[kk]
        wb1.save(excel_file_name)

print("All done")