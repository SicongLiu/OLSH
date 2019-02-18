import os
import re
from openpyxl import load_workbook


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


def get_file_info(full_file_name_):
    file_info_ = []
    file_name_ = full_file_name_.split('.txt')[0]
    temp_file_info_ = file_name_.split('_')
    dims_ = temp_file_info_[0]
    topks_ = temp_file_info_[2]
    # cards_= temp_file_info_[1]
    cards_ = re.sub('[.]', '', temp_file_info_[1])
    types_= temp_file_info_[3]

    print('dim: ' + str(dims_) + ' cards: ' + str(cards_) + ' topks: ' + str(topks_) + ' types: ' + str(types_))
    file_info_.append(str(dims_) + '_' + str(topks_) + '_' + str(cards_))
    file_info_.append(str(types_))
    return file_info_


def find_sheet(sheet_names_, ending_):
    for sheet_name_ in sheet_names_:
        if re.search(ending_, sheet_name_, re.IGNORECASE):
            return sheet_name_
    return None


def process_line(line_concate_):
    processed_line_ = []
    temp_arr = line_concate_[line_concate_.find("{") + 1:line_concate_.find("}")].split(',')
    for ii in range(len(temp_arr)):
        processed_line_.append(int(temp_arr[ii].strip()))
    return processed_line_


def read_file_lines(full_file_path_, read_lines_):
    f1 = open(full_file_path_, 'r')
    line_count = 0
    bash_count = 0
    file_dict_ = {}
    line_concate_ = ''
    for line in f1.readlines():
        line_count = line_count + 1
        line_concate_ = line_concate_ + line.split('\n')[0].strip()
        if line_count % read_lines_ == 0:
            line_count = 0
            file_dict_[bash_count] = process_line(line_concate_)
            bash_count = bash_count + 1
            # print(line_concate[line_concate.find("{")+1:line_concate.find("}")])
            line_concate_ = ''
    f1.close()
    return file_dict_


data_anti_list_10 = ['J6',  'J15', 'J21', 'J30', 'J37', 'J46', 'J51', 'J60', 'J68', 'J77']
k_ranges_anti_10 = ['E6',  'E15', 'E21', 'E30', 'E37', 'E46', 'E51', 'E60', 'E68', 'E77']
l_ranges_opt_anti_10 = ['F6', 'F15', 'F21', 'F30', 'F37', 'F46', 'F51', 'F60', 'F68', 'F77']
l_ranges_max_anti_10 = ['G6', 'G15', 'G21', 'G30', 'G37', 'G46', 'G51', 'G60', 'G68', 'G77']
l_ranges_uni_anti_10 = ['H6', 'H15', 'H21', 'H30', 'H37', 'H46', 'H51', 'H60', 'H68', 'H77']
hash_used_anti_opt_cells_10 = ['I16', 'I31', 'I47', 'I61', 'I78']
hash_used_anti_uni_cells_10 = ['O16', 'O31', 'O47', 'O61', 'O78']

data_corr_list_10 = ['AA6',  'AA15', 'AA21', 'AA30', 'AA37', 'AA46', 'AA51', 'AA60', 'AA68', 'AA77']
k_ranges_corr_10 = ['V6', 'V15', 'V21', 'V30', 'V37', 'V46', 'V51', 'V60', 'V68', 'V77']
l_ranges_opt_corr_10 = ['W6', 'W15', 'W21', 'W30', 'W37', 'W46', 'W51', 'W60', 'W68', 'W77']
l_ranges_max_corr_10 = ['X6', 'X15', 'X21', 'X30', 'X37', 'X46', 'X51', 'X60', 'X68', 'X77']
l_ranges_uni_corr_10 = ['Y6', 'Y15', 'Y21', 'Y30', 'Y37', 'Y46', 'Y51', 'Y60', 'Y68', 'Y77']
hash_used_corr_opt_cells_10 = ['Z16', 'Z31', 'Z47', 'Z61', 'Z78']
hash_used_corr_uni_cells_10 = ['AF16', 'AF31', 'AF47', 'AF61', 'AF78']


data_random_list_10 = ['AQ6',  'AQ15', 'AQ21', 'AQ30', 'AQ37', 'AQ46', 'AQ51', 'AQ60', 'AQ68', 'AQ77']
k_ranges_random_10 = ['AL6', 'AL15', 'AL21', 'AL30', 'AL37', 'AL46', 'AL51', 'AL60', 'AL68', 'AL77']
l_ranges_opt_random_10 = ['AM6', 'AM15', 'AM21', 'AM30', 'AM37', 'AM46', 'AM51', 'AM60', 'AM68', 'AM77']
l_ranges_max_random_10 = ['AN6', 'AN15', 'AN21', 'AN30', 'AN37', 'AN46', 'AN51', 'AN60', 'AN68', 'AN77']
l_ranges_uni_random_10 = ['AO6', 'AO15', 'AO21', 'AO30', 'AO37', 'AO46', 'AO51', 'AO60', 'AO68', 'AO77']
hash_used_rand_opt_cells_10 = ['AP6', 'AP31', 'AP47', 'AP61', 'AP78']
hash_used_rand_uni_cells_10 = ['AV16', 'AV31', 'AV47', 'AV61', 'AV78']

data_anti_list_25 = ['J6', 'J30', 'J38', 'J62', 'J69', 'J93', 'J100', 'J124', 'J131', 'J155']
k_ranges_anti_25 = ['E6', 'E30', 'E38', 'E62', 'E69', 'E93', 'E100', 'E124', 'E131', 'E155']
l_ranges_opt_anti_25 = ['F6', 'F30', 'F38', 'F62', 'F69', 'F93', 'F100', 'F124', 'F131', 'F155']
l_ranges_max_anti_25 = ['G6', 'G30', 'G38', 'G62', 'G69', 'G93', 'G100', 'G124', 'G131', 'G155']
l_ranges_uni_anti_25 = ['H6', 'H30', 'H38', 'H62', 'H69', 'H93', 'H100', 'H124', 'H131', 'H155']
hash_used_anti_opt_cells_25 = ['I31', 'I63', 'I94', 'I125', 'I156']
hash_used_anti_uni_cells_25 = ['O31', 'O63', 'O94', 'O125', 'O156']

data_corr_list_25 = ['AA6', 'AA30', 'AA38', 'AA62', 'AA69', 'AA93', 'AA100', 'AA124', 'AA131', 'AA155']
k_ranges_corr_25 = ['V6', 'V30', 'V38', 'V62', 'V69', 'V93', 'V100', 'V124', 'V131', 'V155']
l_ranges_opt_corr_25 = ['W6', 'W30', 'W38', 'W62', 'W69', 'W93', 'W100', 'W124', 'W131', 'W155']
l_ranges_max_corr_25 = ['X6', 'X30', 'X38', 'X62', 'X69', 'X93', 'X100', 'X124', 'X131', 'X155']
l_ranges_uni_corr_25 = ['Y6', 'Y30', 'Y38', 'Y62', 'Y69', 'Y93', 'Y100', 'Y124', 'Y131', 'Y155']
hash_used_corr_opt_cells_25 = ['Z31', 'Z63', 'Z94', 'Z125', 'Z156']
hash_used_corr_uni_cells_25 = ['AF31', 'AF63', 'AF94', 'AF125', 'AF156']


data_random_list_25 = ['AQ6', 'AQ30', 'AQ38', 'AQ62', 'AQ69', 'AQ93', 'AQ100', 'AQ124', 'AQ131', 'AQ155']
k_ranges_random_25 = ['AL6', 'AL30', 'AL38', 'AL62', 'AL69', 'AL93', 'AL100', 'AL124', 'AL131', 'AL155']
l_ranges_opt_random_25 = ['AM6', 'AM30', 'AM38', 'AM62', 'AM69', 'AM93', 'AM100', 'AM124', 'AM131', 'AM155']
l_ranges_max_random_25 = ['AN6', 'AN30', 'AN38', 'AN62', 'AN69', 'AN93', 'AN100', 'AN124', 'AN131', 'AN155']
l_ranges_uni_random_25 = ['AO6', 'AO30', 'AO38', 'AO62', 'AO69', 'AO93', 'AO100', 'AO124', 'AO131', 'AO155']
hash_used_rand_opt_cells_25 = ['AP31', 'AP63', 'AP94', 'AP125', 'AP156']
hash_used_rand_uni_cells_25 = ['AV31', 'AV63', 'AV94', 'AV125', 'AV156']


data_anti_list_50 = ['J6', 'J55', 'J63', 'J112', 'J120', 'J169', 'J177', 'J226', 'J234', 'J283']
k_ranges_anti_50 = ['E6', 'E55', 'E63', 'E112', 'E120', 'E169', 'E177', 'E226', 'E234', 'E283']
l_ranges_opt_anti_50 = ['F6', 'F55', 'F63', 'F112', 'F120', 'F169', 'F177', 'F226', 'F234', 'F283']
l_ranges_max_anti_50 = ['G6', 'G55', 'G63', 'G112', 'G120', 'G169', 'G177', 'G226', 'G234', 'G283']
l_ranges_uni_anti_50 = ['H6', 'H55', 'H63', 'H112', 'H120', 'H169', 'H177', 'H226', 'H234', 'H283']
hash_used_anti_opt_cells_50 = ['I56', 'I113', 'I170', 'I227', 'I284']
hash_used_anti_uni_cells_50 = ['O56', 'O113', 'O170', 'O227', 'O284']


data_corr_list_50 = ['AA6', 'AA55', 'AA63', 'AA112', 'AA120', 'AA169', 'AA177', 'AA226', 'AA234', 'AA283']
k_ranges_corr_50 = ['V6', 'V55', 'V63', 'V112', 'V120', 'V169', 'V177', 'V226', 'V234', 'V283']
l_ranges_opt_corr_50 = ['W6', 'W55', 'W63', 'W112', 'W120', 'W169', 'W177', 'W226', 'W234', 'W283']
l_ranges_max_corr_50 = ['X6', 'X55', 'X63', 'X112', 'X120', 'X169', 'X177', 'X226', 'X234', 'X283']
l_ranges_uni_corr_50 = ['Y6', 'Y55', 'Y63', 'Y112', 'Y120', 'Y169', 'Y177', 'Y226', 'Y234', 'Y283']
hash_used_corr_opt_cells_50 = ['Z56', 'Z113', 'Z170', 'Z227', 'Z284']
hash_used_corr_uni_cells_50 = ['AF56', 'AF113', 'AF170', 'AF227', 'AF284']


data_random_list_50 = ['AQ6', 'AQ55', 'AQ63', 'AQ112', 'AQ120', 'AQ169', 'AQ177', 'AQ226', 'AQ234', 'AQ283']
k_ranges_random_50 = ['AL6', 'AL55', 'AL63', 'AL112', 'AL120', 'AL169', 'AL177', 'AL226', 'AL234', 'AL283']
l_ranges_opt_random_50 = ['AM6', 'AM55', 'AM63', 'AM112', 'AM120', 'AM169', 'AM177', 'AM226', 'AM234', 'AM283']
l_ranges_max_random_50 = ['AN6', 'AN55', 'AN63', 'AN112', 'AN120', 'AN169', 'AN177', 'AN226', 'AN234', 'AN283']
l_ranges_uni_random_50 = ['AO6', 'AO55', 'AO63', 'AO112', 'AO120', 'AO169', 'AO177', 'AO226', 'AO234', 'AO283']
hash_used_rand_opt_cells_50 = ['AP56', 'AP113', 'AP170', 'AP227', 'AP284']
hash_used_rand_uni_cells_50 = ['AV56', 'AV113', 'AV170', 'AV227', 'AV284']


####################################################################################
text_file_path = '/Users/sicongliu/'
# text_file_path = './'
dimension = 4
excel_file_dir = './'
collision_probility = 0.75
read_lines = -1
# excel_file_name = excel_file_dir + str(dimension) + 'D_075_redundancy_3_all_before.xlsx'
excel_file_name = excel_file_dir + str(dimension) + 'D_all_new.xlsx'

top_m_cell = 'E1'
k_types = ["log", "log_minus", "log_plus", "log_plus_plus", "uni"]
Data_Types = ['anti_correlated', 'correlated', 'random']

wb1 = load_workbook(filename=excel_file_name)
wss = wb1.get_sheet_names()

for file in os.listdir(text_file_path):
    if file.endswith(".txt"):
        full_file_path = os.path.join(text_file_path, file)
        # print(os.path.join(file_path, file))
        # print(file)
        # file = '3D_1.5M_Top50_anit.txt'
        file_info = get_file_info(file)
        file_endings = file_info[0]
        data_distributed_type = file_info[1]
        sheet_name = find_sheet(wss, file_endings)
        if sheet_name is not None:
            print('sheet namne: ' + str(sheet_name) + ' , data type: ' + data_distributed_type)
            # read file data into structure
            # opt_l_info = read_file_lines(full_file_path, read_lines)

            opt_l_info = []
            ws1 = wb1.get_sheet_by_name(sheet_name)
            top_m = ws1[top_m_cell].value

            if top_m == 10:
                read_lines = 1
                k_ranges_anti = k_ranges_anti_10
                l_ranges_opt_anti = l_ranges_opt_anti_10
                l_ranges_max_anti = l_ranges_max_anti_10
                l_ranges_uni_anti = l_ranges_uni_anti_10

                k_ranges_corr = k_ranges_corr_10
                l_ranges_opt_corr = l_ranges_opt_corr_10
                l_ranges_max_corr = l_ranges_max_corr_10
                l_ranges_uni_corr = l_ranges_uni_corr_10

                k_ranges_random = k_ranges_random_10
                l_ranges_opt_random = l_ranges_opt_random_10
                l_ranges_max_random = l_ranges_max_random_10
                l_ranges_uni_random = l_ranges_uni_random_10
                opt_l_info = read_file_lines(full_file_path, read_lines)

            elif top_m == 25:
                read_lines = 2
                k_ranges_anti = k_ranges_anti_25
                l_ranges_opt_anti = l_ranges_opt_anti_25
                l_ranges_max_anti = l_ranges_max_anti_25
                l_ranges_uni_anti = l_ranges_uni_anti_25

                k_ranges_corr = k_ranges_corr_25
                l_ranges_opt_corr = l_ranges_opt_corr_25
                l_ranges_max_corr = l_ranges_max_corr_25
                l_ranges_uni_corr = l_ranges_uni_corr_25

                k_ranges_random = k_ranges_random_25
                l_ranges_opt_random = l_ranges_opt_random_25
                l_ranges_max_random = l_ranges_max_random_25
                l_ranges_uni_random = l_ranges_uni_random_25
                opt_l_info = read_file_lines(full_file_path, read_lines)

            else:
                read_lines = 3
                k_ranges_anti = k_ranges_anti_50
                l_ranges_opt_anti = l_ranges_opt_anti_50
                l_ranges_max_anti = l_ranges_max_anti_50
                l_ranges_uni_anti = l_ranges_uni_anti_50

                k_ranges_corr = k_ranges_corr_50
                l_ranges_opt_corr = l_ranges_opt_corr_50
                l_ranges_max_corr = l_ranges_max_corr_50
                l_ranges_uni_corr = l_ranges_uni_corr_50

                k_ranges_random = k_ranges_random_50
                l_ranges_opt_random = l_ranges_opt_random_50
                l_ranges_max_random = l_ranges_max_random_50
                l_ranges_uni_random = l_ranges_uni_random_50
                opt_l_info = read_file_lines(full_file_path, read_lines)

            l_ranges_opt = []
            # find data type cells
            if data_distributed_type == 'anti':
                l_ranges_opt = l_ranges_opt_anti
            elif data_distributed_type == 'corr':
                l_ranges_opt = l_ranges_opt_corr
            else:
                l_ranges_opt = l_ranges_opt_random
            # write values to L_Opt list

            for ii in range(opt_l_info.__len__()):
                start = 2 * ii
                print(opt_l_info[ii])
                for jj in range(top_m):
                    cur_cell_opt = column_row_index(l_ranges_opt[start], jj)
                    ws1[cur_cell_opt] = opt_l_info[ii][jj]

wb1.save(excel_file_name)

print("All done")