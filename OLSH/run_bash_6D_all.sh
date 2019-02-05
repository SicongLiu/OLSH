#!/bin/bash 
sh ../H2_ALSH/run_bash_set_cur_6D_10717764_without_opt.sh
echo "aggregating for non-opt round 0" 
python ../Python_Analysis/LSH_Post_Process_HOUSE.py without_opt 0 
sleep 3
python ../Python_Analysis/Clean_Sim_Overall_run_test_HOUSE.py
sleep 5
sh ../H2_ALSH/run_bash_set_cur_6D_10717764_with_opt.sh
echo "aggregating for opt round 0" 
python ../Python_Analysis/LSH_Post_Process_HOUSE.py with_opt 0 
sleep 3
python ../Python_Analysis/Clean_All_HOUSE.py
sleep 5
sh ../H2_ALSH/run_bash_set_cur_6D_10717764_without_opt.sh
echo "aggregating for non-opt round 1" 
python ../Python_Analysis/LSH_Post_Process_HOUSE.py without_opt 1 
sleep 3
python ../Python_Analysis/Clean_Sim_Overall_run_test_HOUSE.py
sleep 5
sh ../H2_ALSH/run_bash_set_cur_6D_10717764_with_opt.sh
echo "aggregating for opt round 1" 
python ../Python_Analysis/LSH_Post_Process_HOUSE.py with_opt 1 
sleep 3
python ../Python_Analysis/Clean_All_HOUSE.py
sleep 5
sh ../H2_ALSH/run_bash_set_cur_6D_10717764_without_opt.sh
echo "aggregating for non-opt round 2" 
python ../Python_Analysis/LSH_Post_Process_HOUSE.py without_opt 2 
sleep 3
python ../Python_Analysis/Clean_Sim_Overall_run_test_HOUSE.py
sleep 5
sh ../H2_ALSH/run_bash_set_cur_6D_10717764_with_opt.sh
echo "aggregating for opt round 2" 
python ../Python_Analysis/LSH_Post_Process_HOUSE.py with_opt 2 
sleep 3
python ../Python_Analysis/Clean_All_HOUSE.py
sleep 5
sh ../H2_ALSH/run_bash_set_cur_6D_10717764_without_opt.sh
echo "aggregating for non-opt round 3" 
python ../Python_Analysis/LSH_Post_Process_HOUSE.py without_opt 3 
sleep 3
python ../Python_Analysis/Clean_Sim_Overall_run_test_HOUSE.py
sleep 5
sh ../H2_ALSH/run_bash_set_cur_6D_10717764_with_opt.sh
echo "aggregating for opt round 3" 
python ../Python_Analysis/LSH_Post_Process_HOUSE.py with_opt 3 
sleep 3
python ../Python_Analysis/Clean_All_HOUSE.py
sleep 5
sh ../H2_ALSH/run_bash_set_cur_6D_10717764_without_opt.sh
echo "aggregating for non-opt round 4" 
python ../Python_Analysis/LSH_Post_Process_HOUSE.py without_opt 4 
sleep 3
python ../Python_Analysis/Clean_Sim_Overall_run_test_HOUSE.py
sleep 5
sh ../H2_ALSH/run_bash_set_cur_6D_10717764_with_opt.sh
echo "aggregating for opt round 4" 
python ../Python_Analysis/LSH_Post_Process_HOUSE.py with_opt 4 
sleep 3
python ../Python_Analysis/Clean_All_HOUSE.py
sleep 5
