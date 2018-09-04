% pre-process
clc;
clear;

% topk of interest
k = 50;
% find highest data/query combination score
% data_file_name = 'NBA_2017_2018.csv';
% data = csvread(data_file_name);

data_file_name = 'NBA_data_for_matlab';
data = importdata(data_file_name);
data_size = size(data, 2);
data_dimension = size(data, 1);

query_1 = 'NBA_query_1_for_matlab';
query_2 = 'NBA_query_2_for_matlab';
query_3 = 'NBA_query_3_for_matlab';
q_1 = importdata(query_1);
q_2 = importdata(query_2);
q_3 = importdata(query_3);

[results_1] = compute_Top_K(data, q_1, k);
[results_2] = compute_Top_K(data, q_2, k);
[results_3] = compute_Top_K(data, q_3, k);

% save result
save_query_1 = ['result_1.csv'];
save_query_2 = ['result_2.csv'];
save_query_3 = ['result_3.csv'];
csvwrite(save_query_1, results_1);
csvwrite(save_query_2, results_2);
csvwrite(save_query_3, results_3);

[results_1_w] = compute_Top_K_weight(data, q_1, k);
[results_2_w] = compute_Top_K_weight(data, q_2, k);
[results_3_w] = compute_Top_K_weight(data, q_3, k);

% save result with weight option
save_query_w_1 = ['result_w_1.csv'];
save_query_w_2 = ['result_w_2.csv'];
save_query_w_3 = ['result_w_3.csv'];
csvwrite(save_query_w_1, results_1_w);
csvwrite(save_query_w_2, results_2_w);
csvwrite(save_query_w_3, results_3_w);

fprintf('All Done.\n');