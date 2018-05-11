% pre-process
clc;
clear;

% design dummy query
save_file_name = 'NBA_query';
dimension = 7;
number_of_queries = 2;

small = 10;
large = 50;
% save data for qHull library processing
fid=fopen(save_file_name, 'w');
fprintf(fid, '%d\n', dimension);
fprintf(fid, '%d\n', number_of_queries);

for i = 1 : number_of_queries
    % generate query in random ranges
    r = (large - small).*rand(dimension,1) + small;
    r = r';
    % query data normalization
    norm_2 = norm(r);
    fprintf(fid, '%f %f %f %f %f %f %f\n', r/norm_2);
end
fclose(fid);
fprintf('Normalized Query Generation Done.\n');