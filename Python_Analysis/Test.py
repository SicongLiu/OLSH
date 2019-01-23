import sys

def colnum_string(n):
    string = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        string = chr(65 + remainder) + string
    return string


def compute_cell_index(column_index_start_, kk_, row_index_):
    column_index_num = column_index_start_ + kk_
    cs = colnum_string(column_index_num)
    cell_index_ = cs + str(row_index_)
    return cell_index_


row_index_start = [5, 15, 25, 35, 45]
column_index_start = 2
column_counts = 45
row_counts = 6

types = ["log", "log_minus", "log_plus", "log_plus_plus", "uni"]
budgets = ["1M", "10M"]
dimensions = [2]

repeated_run = 10
excel_folders = '../H2_ALSH/'
column_counts = 45
row_index = 5

for ii in range(0, column_counts):
    cell_index = compute_cell_index(column_index_start, ii, 5)
    print(cell_index)




