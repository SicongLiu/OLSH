function [result] = compute_Top_K(data, query, k)
    temp_data = data;
    data_size = size(temp_data, 1);
    data_dimension = size(temp_data, 2);
    distance = zeros(data_size, 1);
    for i = 1 : data_size
        data_vector = temp_data(i, :);
        distance(i) = sqrt(sum((data_vector - query) .^ 2));
    end
    [value, index] = sort(distance);
    temp_data = temp_data(index, :);
    
    result = [index(1:k) temp_data(1:k, :) value(1:k)];
end