% pre-process
clc;
clear;

% same-attribute data as ICDE paper
file_name = 'NBA_2017_2018.csv';
save_file_name = 'NBA_2017_2018';

% minutes played (MP), total points (PTS), field goals attempted (FGA),
% free throws attempted (FTA), total rebounds (TRB), total assists (AST).
% total personal fouls (PF)
attribute_index = [5, 27, 7, 17, 21, 22, 26];
data = csvread(file_name);
data = data(:, attribute_index);
row_size = size(data, 1);
column_size = size(data, 2);

fid=fopen(save_file_name, 'w');
fprintf(fid, '%d\n', column_size);
fprintf(fid, '%d\n', row_size);
for i = 1 : row_size
    % fprintf(fid, [ header1 ' ' header2 '\n']);
    fprintf(fid, '%f %f %f %f %f %f %f\n', data(i, :));
end
fclose(fid);
% save data for qHull library processing
fprintf('All Done.\n');