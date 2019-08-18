// #include "headers.h"
#include <cstdlib>
#include <cstdio>

#include "Python.h"
#include "numpy/arrayobject.h"
// #include "pyxmod.h"
#include "pymodule.h"
#include <stdio.h>

using namespace std;

void parse_data(float ***data, int * m, int * n)
{
    // setenv is important, makes python find
    // modules in working directory
    setenv("PYTHONPATH", ".", 1);
    
    // Initialize interpreter and module
    Py_Initialize();
    // initpyxmod();
    initpymodule();
    
    // Use Cython functions.
    PyArrayObject *arr = getNPArray();
    *m = getShape(arr, 0);
    *n = getShape(arr, 1);
    
    copyData(data, arr);
    
    if (data == NULL){  //really redundant.
        fprintf(stderr, "Data is NULL\n");
        return ;
    }
    
    Py_DECREF(arr);
    Py_Finalize();
}

void printArray(float **arr, int m, int n)
{
    int i, j;
    for(i=0; i < m; i++){
        for(j=0; j < n; j++)
            printf("%f ", arr[i][j]);
        
        printf("\n");
    }
}

// nargs = 3
// data, dimension, cardinality
int main(int nargs, char **args)
{
    int dim_index = 2;
    int card_index = 3;
    int data_index = 1;
    
    int dim = -1;
    int cardinality = -1;
    
    dim = atoi(args[dim_index]);
    cardinality = atoi(args[card_index]);
    
    // float[][] data = new float[cardinality][dim]
    int m, n;
    // parse_data(args[data_index], &m, &n);
    float **data = NULL;
    // parse_data(&data, &m, &n);
    data = args[data_index];
    printArray(data, m, n);
    // printf("dummy: %d, dim: %d, cardinality: %d. \n", dummy, dim, cardinality);
    
    return 0;
}


