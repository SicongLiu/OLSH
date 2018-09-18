#include<stdio.h>
#include<stdlib.h>
#include<vector>
#include<algorithm>
#include<iostream>

using namespace std;

// Compares according to the field "real" of the struct.
int sortcol(const void *a, const void *b){
    float *x = (float*)a;
    float *y = (float*)b;
    int my_dimension = sizeof(x)/sizeof(float);
    return (x[my_dimension-1] < y[my_dimension-1]) - (x[my_dimension-1] > y[my_dimension-1]);
}

bool sortcol2( const vector<float>& v1,
             const vector<float>& v2 ) {
    printf("%d \n", v1.size());
    return v1[v1.size()] < v2[v2.size()];
}


int main()
{
    printf("About to begin. \n");
    float input[3][3] = {{3, 1, 5}, {4, 8, 6}, {7, 2, 9}};
    for(int i=0; i<3; i++)
    {
        for(int j=0; j<3; j++)
        {
            printf("%f \t", input[i][j]);
        }
        printf("\n");
    }
    printf("\n");
    printf("\n");
    qsort(input, 3, sizeof(*input), sortcol);
    for(int i=0; i<3; i++)
    {
        for(int j=0; j<3; j++)
        {
            printf("%f \t", input[i][j]);
        }
        printf("\n");
    }
    
    /*vector< vector<float> > input{{3, 1, 5}, {4, 8, 6}, {7, 2, 9}};
    sort(input.begin(), input.end(), sortcol2);
    for (int i=0; i<input.size(); i++)
    {
        //loop till the size of particular
        //row
        for (int j=0; j<input[i].size() ;j++)
        {
            printf("%f \t", input[i][j]);
        }
        printf("\n");
    }
    */
    
    return 0;

    
}
