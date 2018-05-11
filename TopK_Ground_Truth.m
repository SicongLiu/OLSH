% pre-process
clc;
clear;

% topk of interest
k = 10;
% find highest data/query combination score
data_file_name = 'NBA_2017_2018.csv';
data = csvread(data_file_name);
row_size = size(data, 1);
dimension = size(data, 2);

% query gives different weight to different dimensions
query_file_name = 'NBA_query_2017_2018';
query = csvread(query_file_name);
query_size = size(query, 1);
score = zeros(row_size, 1);
for i = 1 : query_size
    cur_query = query(i, :);
    for j = 1 : row_size
        score(j) = dot(data(j, :), cur_query);
    end
    sorted_score = sort(score, 'descend');
    for j = 1 : k
       printf('%d-th score : %f .\n', j, sorted_score(j)); 
    end
end
fprintf('All Done.\n');