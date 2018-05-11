function [result] = compute_Top_K_weight(data, query, k)
    temp_data = data.*query;
    score = sum(temp_data, 2); % sum each row
    [value, index] = sort(score, 'descend');
    temp_data = temp_data(index, :);
    result = [index(1:k) temp_data(1:k, :) value(1:k)];
end