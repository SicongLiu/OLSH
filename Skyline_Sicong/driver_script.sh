#!/bin/bash 

echo "running for 6"
./Skyline /Users/sicongliu/Desktop/StreamingTopK/H2_ALSH/raw_data/Synthetic/ random_6_100000 6 100000 25 /Users/sicongliu/Desktop/StreamingTopK/H2_ALSH/qhull_data/Synthetic_test/
sleep 3

echo "running for 33"
./Skyline /Users/sicongliu/Desktop/StreamingTopK/H2_ALSH/raw_data/Synthetic/ random_33_100000 33 100000 25 /Users/sicongliu/Desktop/StreamingTopK/H2_ALSH/qhull_data/Synthetic_test/
