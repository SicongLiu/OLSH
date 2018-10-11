% pre-process
clc;
clear;

excel_file = ["Checkpoint_Result_Oct_10"];

k_ranges_anti = {'E6:E15', 'E21:E30', 'E37:E46', 'E51:E60', 'E68:E77'};
l_ranges_opt_anti = {'F6:F15', 'F21:F30', 'F37:F46', 'F51:F60', 'F68:F77'};
l_ranges_uni_anti = {'G6:G15', 'G21:G30', 'G37:G46', 'G51:G60', 'G68:G77'};

k_ranges_corr = {'U6:U15', 'U21:U30', 'U37:U46', 'U51:U60', 'U68:U77'};
l_ranges_opt_corr = {'V6:V15', 'V21:V30', 'V37:V46', 'V51:V60', 'V68:V77'};
l_ranges_uni_corr = {'W6:W15', 'W21:W30', 'W37:W46', 'W51:W60', 'W68:W77'};

k_ranges_random = {'AJ6:AJ15', 'AJ21:AJ30', 'AJ37:AJ46', 'AJ51:AJ60', 'AJ68:AJ77'};
l_ranges_opt_random = {'AK6:AK15', 'AK21:AK30', 'AK37:AK46', 'AK51:AK60', 'AK68:AK77'};
l_ranges_uni_random = {'AL6:AL15', 'AL21:AL30', 'AL37:AL46', 'AL51:AL60', 'AL68:AL77'};

top_ks = [10, 25];
budgets = {'500k', '1M'};
dimensions = [5, 7];

% types = {'opt', 'log', 'log_plus', 'log_plus_plus', 'uni'};
types = 5;
save_file_path = ['./H2_ALSH/parameters/'];
for m = 1 : size(types, 2)
    save_file_dir = [save_file_path, 'Space_Cost_', num2str(m), '/'];
    if(exist(save_file_dir, 'dir')==0)
        mkdir(save_file_dir);
    end
    
    for i = 1 : size(top_ks, 2)
        topk = top_ks(i);
        for j  = 1 : size(budgets, 2)
            budget = budgets{j};
            for k = 1 : size(dimensions, 2)
                dimension = dimensions(k);
                sheetname = ['Budget_', dimension, 'D_top', num2str(topk), '_budget_', budget];
            end
        end
    end
    
    
end


K = [];
L = [];

fprintf('All Done.\n');