#include <cstdlib>
#include <cstdio>
#include <stdio.h>
#include <cassert>
#include <cstring>
#include <array>
#include <set>
#include <vector>
#include <iostream>

using namespace std;

void printArray(float **arr, int m, int n)
{
    int i, j;
    for(i=0; i < m; i++){
        for(j=0; j < n; j++)
        printf("%f ", arr[i][j]);
        
        printf("\n");
    }
}

void printSet(set<int> my_set)
{
    cout<<"test print set start..."<<endl;
    set<int>::iterator it = my_set.begin();
    while(it != my_set.end())
    {
        cout<<*it<<endl;
        it++;
    }
    cout<<"test print set done"<<endl;
}

int load_data(int cardinality, int dim, char* data_file_name, float **data)
{
    
    FILE *fp = fopen(data_file_name, "r");
    if (!fp)
    {
        printf("Could not open %s\n", data_file_name);
        return 1;
    }
    
    int num_dim = -1;
    int num_element = -1;
    fscanf(fp, "%d", &num_dim);
    fscanf(fp, "\n");
    fscanf(fp, "%d", &num_element);
    fscanf(fp, "\n");
    
    assert(num_dim == dim);
    assert(num_element == cardinality);
    
    cout<< num_dim << " " <<num_element<< endl;
    
    int projected_dim = 2;
    int i   = 0;
    while (!feof(fp) && i < cardinality)
    {
        for (int j = 0; j < projected_dim; ++j)
        {
            fscanf(fp, "%f", &data[i][j]);
        }
        fscanf(fp, "\n");
        ++i;
    }
    printf("reading data: line -- %d, total number of input: %d \n", i, cardinality);
    assert(feof(fp) && i == cardinality);
    fclose(fp);
    
    return 0;
}

bool IsADominateB(float* pointA, float* pointB, int dim)
{
    int n_better = 0;
    for(int i = 0; i < dim; i++)
    {
        if(pointA[i] < pointB[i])
        {
            return false;
        }
        n_better += (pointA[i] > pointB[i]);
    }
    
    if(n_better > 0)
        return true;
    return false;
}

/*void count_diffs(float* pointA, float* pointB, int &n_better, int &n_worse, int dim)
{
    for(int i = 0; i < dim; i++)
    {
        n_better += pointA[i] > pointB[i];
        n_worse += pointA[i] < pointB[i];
    }
}*/

void count_diffs(float* pointA, float* pointB, int* n_better, int* n_worse, int dim)
{
    for(int i = 0; i < dim; i++)
    {
        *n_better += pointA[i] > pointB[i];
        *n_worse += pointA[i] < pointB[i];
    }
}


int persist_on_disk(char* output_path, int dim, set<int> index_set, float** data)
{
    cout<<"output path: " << output_path <<endl;
    FILE *fp = fopen(output_path, "w");
    if (!fp)
    {
        printf("Could not create %s\n", output_path);
        return 1;
    }
    
    fprintf(fp, "%d", dim);
    fprintf(fp, "\n");
    fprintf(fp, "%d", index_set.size());
    fprintf(fp, "\n");
    set<int>::iterator it = index_set.begin();
    while(it != index_set.end())
    {
        for(int i = 0; i < dim; i++)
        {
            fprintf(fp, "%f ", data[*it][i]);
        }
        fprintf(fp, "%d ", *it);
        fprintf(fp, "\n");
        it++;
    }
    fclose(fp);
    return 0;
}

// int find_skyline_bnl(float** input_data, int dim, int cardinality, set<int>* total_index_set, char* output_path, int* skyline_cardinality, int* remain_cardinality, int kth_skyline)
int find_skyline_bnl(float** input_data, int dim, int &cardinality, set<int>& total_index_set, set<int>& skyline_index_set)
{
    int projected_dim = 2;
    cout<<"in function find_skyline_bnl"<<endl;
    // set<int> skyline_index_set;
    set<int>::iterator it = total_index_set.begin();
    skyline_index_set.insert(*it);
    
    int outer_loop = 0;
    it++;
    while (it != total_index_set.end())
    {
        set<int> to_drop;
        bool is_dominated = false;
        
        set<int>::iterator itt = skyline_index_set.begin();
        
        int inner_loop = 0;
        while(itt != skyline_index_set.end())
        {
            int n_better = 0;
            int n_worse = 0;
            // check if input data domniates skyline data
            count_diffs(input_data[*it], input_data[*itt], &n_better, &n_worse, projected_dim);
            //count_diffs(input_data[*it], input_data[*itt], n_better, n_worse, projected_dim);
            
            // Case 1: pointA is dominated by pointB, discard pointA
            if (n_worse > 0  && n_better == 0)
            {
                // cout<<"better: " << n_better<<", worse: "<<n_worse<<", skyline_index: "<<*itt<<", data_index: "<<*it<<endl;
                is_dominated = true;
                break;
            }
            
            // Case 3: if this point dominates any point in the list,, insert this point and the dominated point in the list is discarded
            if (n_better > 0 && n_worse == 0)
            {
                to_drop.insert(*itt);
                //cout<<"Point index to be dropped..."<<*itt<<", better: "<<n_better<<", worse: "<<n_worse<<", skyline_index: "<<*it<<", data_index: "<<*itt<<endl;
            }
            itt++;
        }
        
        
        if(is_dominated)
        {
            it++;
            continue;
        }
        set<int> temp;
        // update skyline list
        set_difference(skyline_index_set.begin(), skyline_index_set.end(), to_drop.begin(), to_drop.end(), inserter(temp, temp.end()));
        skyline_index_set = temp;
        temp.clear();
        // if a point can survive to this step, it means it is a skyline point
        // cout<<"adding skyline point index: "<<*it<<endl;
        skyline_index_set.insert(*it);
        it++;
    }
    // udpate total_index_set
    cardinality = total_index_set.size() - skyline_index_set.size();
    
    set<int> temp;
    set_difference(total_index_set.begin(), total_index_set.end(), skyline_index_set.begin(), skyline_index_set.end(), inserter(temp, temp.end()));
    // free spaces
    total_index_set = temp;
    
    cout<<"done w find_skyline_bnl : " << total_index_set.size()<<endl;
    return 0;
}

// ./Skyline /Users/sicongliu/Desktop/StreamingTopK/H2_ALSH/raw_data/Synthetic/ anti_correlated_4_100 4 100 2 /Users/sicongliu/Desktop/StreamingTopK/H2_ALSH/qhull_data/Synthetic_test

// ./Skyline /Users/sicongliu/Desktop/StreamingTopK/H2_ALSH/raw_data/Synthetic/ anti_correlated_4_100 4 100 2 /Users/sicongliu/Desktop/StreamingTopK/H2_ALSH/qhull_data/Synthetic_test

// ./Skyline /home/cc/Chameleon/StreamingTopK/H2_ALSH/raw_data/Synthetic/ random_6_100000 2 100000 3 /home/cc/Chameleon/StreamingTopK/H2_ALSH/qhull_data/Synthetic_test/


// ./Skyline /Users/sicongliu/Desktop/StreamingTopK/H2_ALSH/raw_data/Synthetic/ random_17_100000 17 100000 2 /Users/sicongliu/Desktop/StreamingTopK/H2_ALSH/qhull_data/Synthetic_test


int main(int nargs, char **args)
{
    int data_folder_index       = 1;
    int input_file_index        = 2;
    int dim_index               = 3;
    int card_index              = 4;
    int k_index                 = 5;
    int output_folder_index     = 6;
    
    char data_folder_name[200];                   // address of input data folder
    char input_file_name[200];                    // actual file name, for convinience of output files
    int dim = -1;
    int cardinality = -1;
    int k = -1;
    char output_folder_name[200];               // address of data set
    
    float **input_data = NULL;
    // float **remain_data = NULL;
    // float **skyline_data = NULL;
    
    strncpy(data_folder_name, args[data_folder_index], sizeof(data_folder_name));
    strncpy(input_file_name, args[input_file_index], sizeof(input_file_name));
    dim = atoi(args[dim_index]);
    cardinality = atoi(args[card_index]);
    k = atoi(args[k_index]);
    strncpy(output_folder_name, args[output_folder_index], sizeof(output_folder_name));
    
    // int nCount[25] = {0, 1, 2, 3, 4};
    // int total_count = 25;
    
    // int nCount[2] = {6, 33};
    // int total_count = 2;

    char data_file_name[200];   // absolute path for input data file
    sprintf(data_file_name, "%s%s.txt", data_folder_name, input_file_name);
    printf("data_folder_index   = %s \n", data_file_name);
    printf("dim                 = %d \n", dim);
    printf("cardinality         = %d \n", cardinality);
    printf("k                   = %d \n", k);
    printf("output folder name  = %s \n", output_folder_name);
    
    input_data = new float*[cardinality];
    for (int i = 0; i < cardinality; ++i)
    {
        input_data[i] = new float[dim];
    }
    
    if (load_data(cardinality, dim, data_file_name, input_data) == 1)
    {
        printf("Reading dataset error!\n");
        return 1;
    }
    
    // save_data_file
    // top-k layer
    int* array = (int *) malloc(cardinality * sizeof(int));
    for(int i = 0; i < cardinality; i++)
    {
        array[i] = i;
    }
    set<int> index_set (array, array + cardinality);
    
    
    for(int i = 0; i < k; i++)
    {
        // save_data_file
        char output_set[200];
        sprintf(output_set, "%s%s_qhull_layer_%d", output_folder_name, input_file_name, i);
        set<int> skyline_index_set;
        int ret_skyline = find_skyline_bnl(input_data, dim, cardinality, index_set, skyline_index_set);
        
        cout<<"oop s... done w find_skyline_bnl : " << index_set.size()<<endl;
        /*set<int>::iterator it = index_set.begin();
        
        while(it != index_set.end())
        {
            cout<<*it<<endl;
            it++;
        }*/
        
        
        int projected_dim = 2;
        int ret_persiste = persist_on_disk(output_set, projected_dim, skyline_index_set, input_data);
        if(ret_skyline == 1 || ret_persiste == 1)
        {
            cout<< "Something is wrong...  Program terminated"<<endl;
            return 1;
        }
    }
     
    
    return 0;
}


