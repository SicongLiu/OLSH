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


def colnum_string(n):
    string = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        string = chr(65 + remainder) + string
    return string


def col2num(col):
    num = 0
    for c in col:
        if c in string.ascii_letters:
            num = num * 26 + (ord(c.upper()) - ord('A')) + 1
    return num


# J, AA AQ
def compute_data_list_start_end(data_type_index_, data_list, column_dist_):
    start_items_ = separate_string(data_list[0])
    start_letter_ = start_items_[0]
    start_num_ = start_items_[1]

    end_items_ = separate_string(data_list[1])
    end_letter_ = end_items_[0]
    end_num_ = end_items_[1]

    start_letter_integer_ = int(col2num(start_letter_))
    start_letter_integer_ = start_letter_integer_ + column_dist_ * data_type_index_
    start_letter_ = colnum_string(start_letter_integer_)
    data_list_start = start_letter_ + start_num_
    data_list_end = start_letter_ + end_num_

    return data_list_start, data_list_end


# both letter and integer row index change
def compute_ranges_start_end(column_shift, row_shift, ranges, row_dist_, column_dist_):
    range_start, range_end = compute_data_list_start_end(column_shift, ranges, column_dist_)
    range_column = separate_string(range_start)[0]
    range_row_start = separate_string(range_start)[1] # 6
    range_row_end = separate_string(range_end)[1] # 45
    row_span_ = int(range_row_end) - int(range_row_start)

    target_row_start = int(range_row_end) * row_shift + row_dist_ # 51
    target_row_end = target_row_start + row_span_
    k_ranges_temp_start = range_column + str(target_row_start)
    k_ranges_temp_end = range_column + str(target_row_end)

    return k_ranges_temp_start, k_ranges_temp_end


data_list_40 = ['J6',  'J15', 'J21', 'J30', 'J37', 'J46', 'J51', 'J60', 'J68', 'J77']
k_ranges_40 = ['E6',  'E15', 'E21', 'E30', 'E37', 'E46', 'E51', 'E60', 'E68', 'E77']
l_ranges_opt_40 = ['F6', 'F15', 'F21', 'F30', 'F37', 'F46', 'F51', 'F60', 'F68', 'F77']
l_ranges_max_40 = ['G6', 'G15', 'G21', 'G30', 'G37', 'G46', 'G51', 'G60', 'G68', 'G77']
l_ranges_uni_40 = ['H6', 'H15', 'H21', 'H30', 'H37', 'H46', 'H51', 'H60', 'H68', 'H77']
hash_used_opt_cells_40 = ['I16', 'I31', 'I47', 'I61', 'I78']
hash_used_uni_cells_40 = ['O16', 'O31', 'O47', 'O61', 'O78']


data_list_60 = ['J6',  'J15', 'J21', 'J30', 'J37', 'J46', 'J51', 'J60', 'J68', 'J77']
k_ranges_60 = ['E6',  'E15', 'E21', 'E30', 'E37', 'E46', 'E51', 'E60', 'E68', 'E77']
l_ranges_opt_60 = ['F6', 'F15', 'F21', 'F30', 'F37', 'F46', 'F51', 'F60', 'F68', 'F77']
l_ranges_max_60 = ['G6', 'G15', 'G21', 'G30', 'G37', 'G46', 'G51', 'G60', 'G68', 'G77']
l_ranges_uni_60 = ['H6', 'H15', 'H21', 'H30', 'H37', 'H46', 'H51', 'H60', 'H68', 'H77']
hash_used_opt_cells_60 = ['I16', 'I31', 'I47', 'I61', 'I78']
hash_used_uni_cells_60 = ['O16', 'O31', 'O47', 'O61', 'O78']


data_list_80 = ['J6',  'J15', 'J21', 'J30', 'J37', 'J46', 'J51', 'J60', 'J68', 'J77']
k_ranges_80 = ['E6',  'E15', 'E21', 'E30', 'E37', 'E46', 'E51', 'E60', 'E68', 'E77']
l_ranges_opt_80 = ['F6', 'F15', 'F21', 'F30', 'F37', 'F46', 'F51', 'F60', 'F68', 'F77']
l_ranges_max_80 = ['G6', 'G15', 'G21', 'G30', 'G37', 'G46', 'G51', 'G60', 'G68', 'G77']
l_ranges_uni_80 = ['H6', 'H15', 'H21', 'H30', 'H37', 'H46', 'H51', 'H60', 'H68', 'H77']
hash_used_opt_cells_80 = ['I16', 'I31', 'I47', 'I61', 'I78']
hash_used_uni_cells_80 = ['O16', 'O31', 'O47', 'O61', 'O78']

####################################################################################
column_dist = 17
row_dist = 6
text_file_path = '/Users/sicongliu/'
# text_file_path = './'
dimension = 5
excel_file_dir = './'
collision_probility = 0.75
read_lines = -1
# excel_file_name = excel_file_dir + str(dimension) + 'D_075_redundancy_3_all_before.xlsx'
excel_file_name = excel_file_dir + str(dimension) + 'D_all_new.xlsx'

bin_count_cell = 'E1'
k_types = ["log", "log_minus", "log_plus", "log_plus_plus", "uni"]
Data_Types = ['anti_correlated', 'correlated', 'random']

wb1 = load_workbook(filename=excel_file_name)
wss = wb1.get_sheet_names()

for file in os.listdir(text_file_path):
    if file.endswith(".txt"):
        full_file_path = os.path.join(text_file_path, file)
        file_info = get_file_info(file)
        file_endings = file_info[0]
        data_distributed_type = file_info[1]
        sheet_name = find_sheet(wss, file_endings)
        if sheet_name is not None:
            print('sheet name: ' + str(sheet_name) + ' , data type: ' + data_distributed_type)
            # read file data into structure

            opt_l_info = []
            ws1 = wb1.get_sheet_by_name(sheet_name)
            bin_count = ws1[bin_count_cell].value

            if bin_count == 40:
                read_lines = 3
                data_list = data_list_40
                k_ranges_ = k_ranges_40
                l_ranges_opt_ = l_ranges_opt_40
                l_ranges_max_ = l_ranges_max_40
                l_ranges_uni_ = l_ranges_uni_40

                opt_l_info = read_file_lines(full_file_path, read_lines)

            elif bin_count == 60:
                read_lines = 3
                data_list = data_list_60
                k_ranges_ = k_ranges_60
                l_ranges_opt_ = l_ranges_opt_60
                l_ranges_max_ = l_ranges_max_60
                l_ranges_uni_ = l_ranges_uni_60

                opt_l_info = read_file_lines(full_file_path, read_lines)

            else:
                read_lines = 3
                data_list = data_list_80
                k_ranges_ = k_ranges_80
                l_ranges_opt_ = l_ranges_opt_80
                l_ranges_max_ = l_ranges_max_80
                l_ranges_uni_ = l_ranges_uni_80

                opt_l_info = read_file_lines(full_file_path, read_lines)

            l_ranges_opt = []
            # for loop starts here
            for ii in range(Data_Types.__len__()):
                data_distributed_type = Data_Types[ii]
                for kk in range(k_types.__len__()):
                    l_ranges_opt_temp_start, l_ranges_opt_temp_end = compute_ranges_start_end(kk, ii,
                                                                                              l_ranges_opt,
                                                                                              row_dist,
                                                                                              column_dist)

                    for columns in ws1[l_ranges_opt_temp_start: l_ranges_opt_temp_end]:
                        for cell in columns:
                            ws1[cell] = opt_l_info[kk][cell]
                            # l_uni.append(cell.value)
            #
            # # find data type cells
            # if data_distributed_type == 'anti':
            #     l_ranges_opt = l_ranges_opt_anti
            # elif data_distributed_type == 'corr':
            #     l_ranges_opt = l_ranges_opt_corr
            # else:
            #     l_ranges_opt = l_ranges_opt_random
            # for ii in range(opt_l_info.__len__()):
            #     start = ii
            #     print(opt_l_info[ii])
            #     for jj in range(bin_count):
            #         cur_cell_opt = column_row_index(l_ranges_opt[start], jj)
            #         ws1[cur_cell_opt] = opt_l_info[ii][jj]

wb1.save(excel_file_name)

print("All done")