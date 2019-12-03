

# top_k_ = int(str(sys.argv[1]))
# dimension_ = int(str(sys.argv[2]))
# card_ = int(str(sys.argv[3]))
# bin_count_ = int(str(sys.argv[4]))
# query_num_ = int(str(sys.argv[5]))

# for bin num info, we need to manually input one by one


top_ks = [25, 50]
dimensions = [50, 100, 200, 300]
card = [100000, 500000, 1000000, 2000000, 10000000]
# bins = [40, 60, 80]
bin_count_ = 40
query_num_ = 1000

temp_str = "ready for Mathematica copy"
# run the "file_name" on cloud side
file_name = './run_bin_partition_bash.sh'
f1 = open(file_name, 'w')
f1.write("#!/bin/bash \n")

# use apt-get to update python package: python3, numpy, scipy, openpyxl
f1.write('pip install numpy \n')
f1.write('sleep 2 \n')
f1.write('pip install scipy \n')
f1.write('sleep 2 \n')
f1.write('pip install openpyxl \n')
f1.write('sleep 2 \n')


for top_k_ in top_ks:
    for dimension_ in dimensions:
        for card_ in card:
            f1.write(
                'python ./Norm_Analysis_Bin_Partition_Script.py ' + str(top_k_) + ' ' + str(
                    dimension_) + ' ' + str(card_) + ' ' + str(bin_count_) + ' ' + str(query_num_) + ' \n')
f1.write('echo \"' + temp_str + '\" \n')
f1.close()