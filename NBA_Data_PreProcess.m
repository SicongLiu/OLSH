% pre-process
clc;
clear;

% same-attribute data as ICDE paper

% minutes played (MP), total points (PTS), field goals attempted (FGA),
% free throws attempted (FTA), total rebounds (TRB), total assists (AST).
% total personal fouls (PF)
nba_data = [];
number_of_record = 0;

attribute_index = [27, 7];
% attribute_index = [5, 27, 7];
% attribute_index = [5, 27, 7, 17, 21, 22, 26];
% nba_data_file_season = [2018, 2017, 2016, 2015, 2014, 2013, 2012];
nba_data_file_season = [2018];
for k = 1 : size(nba_data_file_season, 2)
    nba_data_file_name = ['NBA_', num2str(nba_data_file_season(k) - 1), '_', num2str(nba_data_file_season(k)), '.csv'];
    % save_file_name = ['NBA_', num2str(nba_data_file_season(k) - 1), '_', num2str(nba_data_file_season(k))];
    cur_nba_data = csvread(nba_data_file_name);
    cur_nba_data = cur_nba_data(:, attribute_index);
    row_size = size(cur_nba_data, 1);
    column_size = size(cur_nba_data, 2);
    
    number_of_record = number_of_record + row_size;
    % merge data
    nba_data = [nba_data; cur_nba_data];
    %     % save data for qHull library processing
    %     fid=fopen(save_file_name, 'w');
    %     fprintf(fid, '%d\n', column_size);
    %     fprintf(fid, '%d\n', row_size);
    %     for i = 1 : row_size
    %         % data normalization
    %         norm_2 = norm(data(i, :));
    %         fprintf(fid, '%f %f %f %f %f %f %f\n', data(i, :)/norm_2);
    %     end
    %     fclose(fid);
end

% save data for qHull library processing
save_file_name = ['NBA_data'];
dimension = size(attribute_index, 2);
fid=fopen(save_file_name, 'w');
fprintf(fid, '%d\n', dimension);
fprintf(fid, '%d\n', number_of_record);
for i = 1 : number_of_record
    % data normalization
    norm_2 = norm(nba_data(i, :));
    if(norm_2 == 0 || size(find(nba_data(i, :) == 0), 2) > 0 )
        continue;
    else
        % fprintf(fid, '%f %f %f %f %f %f %f\n', nba_data(i, :)./norm_2);
        % fprintf(fid, '%f %f %f\n', nba_data(i, :)./norm_2);
        fprintf(fid, '%f %f\n', nba_data(i, :)./norm_2);
    end
end
fclose(fid);


fprintf('All Done.\n');