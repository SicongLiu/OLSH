% pre-process
clc;
clear;

data_file_name_layer_1 = 'nba_test_qhull_layer_0_for_matlab';
data_file_name_layer_2 = 'nba_test_qhull_layer_1_for_matlab';
data_file_name_layer_3 = 'nba_test_qhull_layer_2_for_matlab';

layers = [1 2 3];
queries = [1 2 3];
for i = 1 : size(queries, 2)
    for j = 1 : size(layers, 2)
        cur_index_file = ['q', num2str(queries(i)), '_layer_index_', num2str(layers(j))];
        cur_data_file = ['nba_test_qhull_layer_', num2str(j-1), '_for_matlab'];
        data_layer = importdata(cur_data_file);
        cur_index = importdata(cur_index_file);
        
        save_data_file = ['query_', num2str(queries(i)), '_layer_', num2str(layers(j)), '.csv'];
        data_to_be_save = [];
        
        for k = 1 : size(cur_index, 1)
            my_index = cur_index(k);
            data_to_be_save = [data_to_be_save; data_layer(my_index, :)];
            
            
        end
        csvwrite(save_data_file, data_to_be_save);
    end
    
end

fprintf('All Done.\n');