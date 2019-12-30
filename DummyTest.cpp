#include<stdio.h>
#include<stdlib.h>
#include<limits>
#include<vector>
#include<algorithm>
#include<iostream>
#include <unordered_set>

using namespace std;

// Compares according to the field "real" of the struct.
int sortcol(const void *a, const void *b){
    float *x = (float*)a;
    float *y = (float*)b;
    int my_dimension = 6;
    printf("oops: %f \n", x[my_dimension-1]);
    return x[my_dimension-1] < y[my_dimension-1] ;
}

bool sortcol2( const vector<float>& v1,
             const vector<float>& v2 ) {
    printf("%d \n", v1.size());
    return v1[v1.size()] < v2[v2.size()];
}

int compare ( const void *pa, const void *pb ) {
    const int *a = *(const int **)pa;
    const int *b = *(const int **)pb;
    return (a[5] < b[5]) - (a[5] > b[5]);
}

int main()
{

    // cout<<DBL_EPSILON<<endl;
    // double temp =  std::numeric_limits<double>::epsilon();
    // cout << temp <<endl;
   
//    unordered_set<int> candidates;
//    int range = 3;
//    for(int i = 0; i < range; i++)
//    {
//        candidates.insert(i);
//    }
//
//    for(auto it : candidates)
//    {
//        int id = (int)it;
//        cout<<id<<endl;
//    }
    string temp_folder = "./query_test/random_";
    const char* temp_folder_char = temp_folder.c_str();
    
    char command_str_char[200];
    sprintf(command_str_char, "rm %s*", temp_folder_char);

    cout << "command line to be executed... " << command_str_char << endl;
    system(command_str_char);
    
    return 0;

    
}
