import sys

# generate data and copy to remote machine
remote_machine_ip = "129.114.108.208"
file_name = './run_bin_partition_bash.sh'
f = open(file_name, 'w')
f.write("#!/bin/bash \n")
# first generate bin partition bash fle
f.write("python ./Norm_Analysis_Run_Bin_Partition_Bash.py \n")
# ship data to cloud machine
f.write("remote_machine_ip=" + str(remote_machine_ip) + "\n")
f.write("ssh cc@${remote_machine_ip} \n")
f.write("scp -r /Users/sicongliu/Desktop/Chameleon/ cc@${remote_machine_ip}")

f.write("scp -r /Users/sicongliu/Desktop/Chameleon/StreamingTopK/Python_Analysis/*.py cc@${remote_machine_ip}:/home/cc/Chameleon/StreamingTopK/Python_Analysis/")
f.close()

copy_mathematica = "copy_math_file.sh"
f = open(copy_mathematica, 'w')
f.write("#!/bin/bash \n")
f.write("scp cc@${remote_machine_ip}:/home/cc/Chameleon/StreamingTopK/H2_ALSH/parameters/*.txt /Users/sicongliu/Desktop/Chameleon/StreamingTopK/H2_ALSH/parameters/ ")
f.close()
