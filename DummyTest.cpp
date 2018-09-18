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
    printf("About to begin. \n");
    int count = 2;
    int d = 6;
    float*** input = new float**[count];
    for(int i=0; i < count; i++)
    {
        input[i] = new float*[3];
        for(int j = 0; j< 3; j++)
            input[i][j]  = new float[d];
    }
    const char* temp_output_folder = "test_input.txt";
    FILE *fp1 = fopen(temp_output_folder, "r");
    if (!fp1)
    {
        printf("Could not open %s\n", temp_output_folder);
        return 1;
    }
    
    
    int line_count = 0;
    while (!feof(fp1))
    {
        for (int i = 0; i < d ; ++i)
        {
            float temp = 0;
            fscanf(fp1, " %f", &temp);
            input[0][line_count][i] = temp;
            input[1][line_count][i] = temp;
        }
        fscanf(fp1, "\n");
        ++line_count;
    }
    printf("total line count: %d \n", line_count);
    
    // assert(feof(fp1) && line_count == 3);
    fclose(fp1);
    
    for(int i=0; i<count; i++)
    {
        for(int j=0; j<3; j++)
        {
            for(int k=0; k<d; k++)
            {
                printf("%f \t", input[i][j][k]);
            }
            printf("\n");
        }
    }
    
    printf("**************************** \n");
    
    /*for(int i=0; i<count; i++)
    {
        qsort(input[i], 3, sizeof(*input[i]), sortcol);
    }*/
    qsort(input[0], 3, sizeof(*input[0]), compare);
    for(int i=0; i<count; i++)
    {
        for(int j=0; j<3; j++)
        {
            for(int k=0; k<d; k++)
            {
                printf("%f \t", input[i][j][k]);
            }
            printf("\n");
        }
    }
    
    
    /*
    float input1[3][4] = {{3, 1, 5, 100}, {4, 8, 6, 10}, {7, 2, 9, 1000}};
    float input2[3][4] = {{3, 1, 5, 100}, {4, 8, 6, 10}, {7, 2, 9, 1000}};
    float*** input = new float**[2];
    input[0] = input1;
    input[1] = input2;
    
    for(int i=0; i<count; i++)
    {
    for(int i=0; i<3; i++)
    {
        for(int j=0; j<4; j++)
        {
            printf("%f \t", input[i][j]);
        }
        printf("\n");
    }
    }
    printf("\n");
    printf("\n");
    for(int i=0; i<count; i++){
        qsort(input[i], 3, sizeof(*input[i]), sortcol);
    }
    for(int i=0; i<count; i++)
    {
    for(int i=0; i<3; i++)
    {
        for(int j=0; j<4; j++)
        {
            printf("%f \t", input[i][j]);
        }
        printf("\n");
    }
    }
    printf("%d \n", sizeof(*input));
    printf("%d \n", sizeof(*input[0]));
     */
     
     
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
