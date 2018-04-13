/*
 *   Copyright (c) 2004-2005 Massachusetts Institute of Technology.
 *   All Rights Reserved.
 *
 *   This program is free software: you can redistribute it and/or modify
 *   it under the terms of the GNU General Public License as published by
 *   the Free Software Foundation, either version 3 of the License, or
 *   (at your option) any later version.
 *
 *   This program is distributed in the hope that it will be useful,
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *   GNU General Public License for more details.
 *
 *   You should have received a copy of the GNU General Public License
 *   along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *   Authors: Alexandr Andoni (andoni@mit.edu), Piotr Indyk (indyk@mit.edu)
 */

/*
 The main entry file containing the main() function. The main()
 function parses the command line parameters and depending on them
 calls the correspondin functions.
 */

#include <stdio.h>
#include <stdlib.h>
#include <sys/times.h>
#include "headers.h"

// The value of parameter R (a near neighbor of a point <q> is any
// point <p> from the data set that is the within distance
// <thresholdR>).
//RealT thresholdR = 1.0;

// The succes probability of each point (each near neighbor is
// reported by the algorithm with probability <successProbability>).
RealT successProbability = 0.9;

// Same as <thresholdR>, only an array of R's (for the case when
// multiple R's are specified).
// RealT *listOfRadii = NULL;
RealT *listOfPoints = NULL;
IntT nRadii = 0;

RealT *memRatiosForNNStructs = NULL;

char sBuffer[600000];

/*
 Prints the usage of the LSHMain.
 */
void usage(char *programName){
    printf("Usage: %s #pts_in_data_set #queries dimension successProbability radius data_set_file query_points_file max_available_memory [-c|-p params_file]\n", programName);
}

inline PPointT readPoint(FILE *fileHandle, int num_of_dimensions)
{
    PPointT p;
    RealT sqrLength = 0;
    FAILIF(NULL == (p = (PPointT)MALLOC(sizeof(PointT))));
    FAILIF(NULL == (p->coordinates = (RealT*)MALLOC(num_of_dimensions * sizeof(RealT))));
    for(IntT d = 0; d < num_of_dimensions; d++)
    {
        FSCANF_REAL(fileHandle, &(p->coordinates[d]));
        sqrLength += SQR(p->coordinates[d]);
    }
    fscanf(fileHandle, "%[^\n]", sBuffer);
    p->index = -1;
    p->sqrLength = sqrLength;
    return p;
}

// Read data from Qhull format
// data line by line, type-real
void readDataSetFromFile(PPointT *dataSetPoints, FILE *fileHandle, int num_of_points, int num_of_dimensions)
{
    FAILIF(NULL == (dataSetPoints = (PPointT*)MALLOC(num_of_points * sizeof(PPointT))));
    for(IntT i = 0; i < num_of_points; i++)
    {
        dataSetPoints[i] = readPoint(fileHandle, num_of_dimensions);
        dataSetPoints[i]->index = i;
    }
}


// Tranforming <memRatiosForNNStructs> from
// <memRatiosForNNStructs[i]=ratio of mem/total mem> to
// <memRatiosForNNStructs[i]=ratio of mem/mem left for structs i,i+1,...>.
void transformMemRatios(){
    RealT sum = 0;
    for(IntT i = nRadii - 1; i >= 0; i--){
        sum += memRatiosForNNStructs[i];
        memRatiosForNNStructs[i] = memRatiosForNNStructs[i] / sum;
        //DPRINTF("%0.6lf\n", memRatiosForNNStructs[i]);
    }
    ASSERT(sum <= 1.000001);
}


int compareInt32T(const void *a, const void *b){
    Int32T *x = (Int32T*)a;
    Int32T *y = (Int32T*)b;
    return (*x > *y) - (*x < *y);
}

/*
 The main entry to LSH package. Depending on the command line
 parameters, the function computes the R-NN data structure optimal
 parameters and/or construct the R-NN data structure and runs the
 queries on the data structure.
 */
int main(int nargs, char **args)
{
    // The data set containing all the points.
    PPointT *dataSetPoints = NULL;
    PPointT *query_data_Points = NULL;
    
    // Number of points in the data set.
    IntT nPoints = 0;
    // The dimension of the points.
    IntT pointsDimension = 0;
    
    // Number of query points in the data set.
    Int32T nSampleQueries = 0;
    // The dimension of the query points, should be equal to dimension of data points
    IntT query_pointsDimension = 0;
    
    // load data points
    char* filename = "2d_test2_qhull_layer_0";
    FILE *pFile = fopen(filename, "rt");
    FAILIF(pFile == NULL);
    fscanf(pFile, "%d\n", &pointsDimension);
    ASSERT(pointsDimension > 0);
    fscanf(pFile, "%d\n", &nPoints);
    ASSERT(nPoints > 0);
    printf("Number of Dimension: %d, number of Points: %d. \n", pointsDimension, nPoints);
    readDataSetFromFile(dataSetPoints, pFile, nPoints, pointsDimension);
    fclose(pFile)
    
    // load query data
    PPointT sampleQueries[nSampleQueries];
    Int32T sampleQBoundaryIndeces[nSampleQueries];
    char* query_file_name = "query_file";
    FILE *queryFile = fopen(query_file_name, "rt");
    FAILIF(pFile == NULL);
    fscanf(pFile, "%d\n", &query_pointsDimension);
    ASSERT(pointsDimension > 0);
    fscanf(pFile, "%d\n", &nSampleQueries);
    ASSERT(nPoints > 0);
    printf("Number of Query Dimension: %d, Number of Query Points: %d. \n", query_pointsDimension, nSampleQueries);
    readDataSetFromFile(query_data_Points, queryFile, nSampleQueries, query_pointsDimension);
    fclose(queryFile);
    
    return 0;
}
