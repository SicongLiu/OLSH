/*
 The main entry file containing the main() function. The main()
 function parses the command line parameters and depending on them
 calls the correspondin functions.
 */

#include <stdio.h>
#include <stdlib.h>
#include <sys/times.h>
#include "headers.h"


#define N_SAMPLE_QUERY_POINTS 100

// The value of parameter R (a near neighbor of a point <q> is any
// point <p> from the data set that is the within distance
// <thresholdR>).
//RealT thresholdR = 1.0;

// The succes probability of each point (each near neighbor is
// reported by the algorithm with probability <successProbability>).
RealT successProbability = 0.9;

// Same as <thresholdR>, only an array of R's (for the case when
// multiple R's are specified).
RealT *listOfRadii = NULL;
RealT *listOfPoints = NULL;
IntT nRadii = 0;

RealT *memRatiosForNNStructs = NULL;

char sBuffer[600000];

/*
 Prints the usage of the LSHMain.
 */
void usage(char *programName){
    printf("Usage: %s successProbability radius data_set_file query_points_file max_available_memory [-c|-p params_file]\n", programName);
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
    if(nargs < 6)
    {
        usage(args[0]);
        exit(1);
    }
    
    successProbability = atof(args[1]);
    
    // The data set containing all the points.
    PPointT *dataSetPoints = NULL;
    PPointT *query_data_Points = NULL;
    
    // Number of points in the data set, load from qhull file
    IntT nPoints = 0;
    
    // The dimension of the points, load from qhull file
    IntT pointsDimension = 0;
    
    // Number of query points in the data set.
    IntT nQueries = 0;
    
    // The dimension of the query points, should be equal to dimension of data points
    IntT query_pointsDimension = 0;
    
    ////////////////////////////////////////////////////////////////////////
    // initialize radius
    ////////////////////////////////////////////////////////////////////////
    char* endPtr[1];
    RealT thresholdR = strtod(args[2], endPtr);
    if (thresholdR == 0 || endPtr[1] == args[2])
    {
        // The value for R is not specified, instead there is a file
        // specifying multiple R's.
        thresholdR = 0;
        
        // Read in the file
        FILE *radiiFile = fopen(args[2], "rt");
        FAILIF(radiiFile == NULL);
        
        // first line of the file is the number of radii
        fscanf(radiiFile, "%d\n", &nRadii);
        ASSERT(nRadii > 0);
        
        // allocate radii
        FAILIF(NULL == (listOfRadii = (RealT*)MALLOC(nRadii * sizeof(RealT))));
        FAILIF(NULL == (memRatiosForNNStructs = (RealT*)MALLOC(nRadii * sizeof(RealT))));
        for(IntT i = 0; i < nRadii; i++)
        {
            FSCANF_REAL(radiiFile, &listOfRadii[i]);
            ASSERT(listOfRadii[i] > 0);
            FSCANF_REAL(radiiFile, &memRatiosForNNStructs[i]);
            ASSERT(memRatiosForNNStructs[i] > 0);
        }
    }
    else
    {
        // set default number of radii
        nRadii = 1;
        FAILIF(NULL == (listOfRadii = (RealT*)MALLOC(nRadii * sizeof(RealT))));
        FAILIF(NULL == (memRatiosForNNStructs = (RealT*)MALLOC(nRadii * sizeof(RealT))));
        listOfRadii[0] = thresholdR;
        memRatiosForNNStructs[0] = 1;
    }
    DPRINTF("No. radii: %d\n", nRadii);
    availableTotalMemory = atoll(args[5]);
    
    ////////////////////////////////////////////////////////////////////////
    // load data points qhull format
    ////////////////////////////////////////////////////////////////////////
    // char* filename = "2d_test2_qhull_layer_0";
    char* filename = args[3];
    FILE *pFile = fopen(filename, "rt");
    FAILIF(pFile == NULL);
    fscanf(pFile, "%d\n", &pointsDimension);
    ASSERT(pointsDimension > 0);
    fscanf(pFile, "%d\n", &nPoints);
    ASSERT(nPoints > 0);
    printf("Number of Dimension: %d, number of Points: %d. \n", pointsDimension, nPoints);
    readDataSetFromFile(dataSetPoints, pFile, nPoints, pointsDimension);
    fclose(pFile);
    
    if (nPoints > MAX_N_POINTS)
    {
        printf("Error: the structure supports at most %d points (%d were specified).\n", MAX_N_POINTS, nPoints);
        fprintf(ERROR_OUTPUT, "Error: the structure supports at most %d points (%d were specified).\n", MAX_N_POINTS, nPoints);
        exit(1);
    }
    
    ////////////////////////////////////////////////////////////////////////
    // load or create sample query points first
    Int32T nSampleQueries = N_SAMPLE_QUERY_POINTS;
    PPointT sampleQueries[nSampleQueries];
    Int32T sampleQBoundaryIndeces[nSampleQueries];
    // In this cases, we need to generate a sample query set for
    // computing the optimal parameters in later phase
    ////////////////////////////////////////////////////////////////////////
    
    if ((nargs < 6) || (strcmp("-c", args[6]) == 0))
    {
        // Generate a sample query set.
        FILE *queryFile = fopen(args[4], "rt");
        FAILIF(pFile == NULL);
        fscanf(pFile, "%d\n", &query_pointsDimension);
        ASSERT(pointsDimension > 0);
        fscanf(pFile, "%d\n", &nQueries);
        ASSERT(nQueries > 0);
        
        if (strcmp(args[4], ".") == 0 || queryFile == NULL || nQueries <= 0)
        {
            // Choose several data set points for the sample query points.
            for(IntT i = 0; i < nSampleQueries; i++)
            {
                sampleQueries[i] = dataSetPoints[genRandomInt(0, nPoints - 1)];
            }
        }
        else
        {
            // Choose several actual query points for the sample query points.
            nSampleQueries = MIN(nSampleQueries, nQueries);
            Int32T sampleIndeces[nSampleQueries];
            for(IntT i = 0; i < nSampleQueries; i++)
            {
                sampleIndeces[i] = genRandomInt(0, nQueries - 1);
            }
            qsort(sampleIndeces, nSampleQueries, sizeof(*sampleIndeces), compareInt32T);
            //printIntVector("sampleIndeces: ", nSampleQueries, sampleIndeces);
            Int32T j = 0;
            for(Int32T i = 0; i < nQueries; i++)
            {
                if (i == sampleIndeces[j])
                {
                    sampleQueries[j] = readPoint(queryFile, query_pointsDimension);
                    j++;
                    while (i == sampleIndeces[j])
                    {
                        sampleQueries[j] = sampleQueries[j - 1];
                        j++;
                    }
                }
                else
                {
                    fscanf(queryFile, "%[^\n]", sBuffer);
                    fscanf(queryFile, "\n");
                }
            }
            nSampleQueries = j;
            fclose(queryFile);
        }
        
        // Compute the array sampleQBoundaryIndeces that specifies how to
        // segregate the sample query points according to their distance
        // to NN.
        sortQueryPointsByRadii(pointsDimension,
                               nSampleQueries,
                               sampleQueries,
                               nPoints,
                               dataSetPoints,
                               nRadii,
                               listOfRadii,
                               sampleQBoundaryIndeces);
    }
    
    ////////////////////////////////////////////////////////////////////////
    // learn and/or set optimal parameters
    ////////////////////////////////////////////////////////////////////////
    RNNParametersT *algParameters = NULL;
    PRNearNeighborStructT *nnStructs = NULL;
    
    // Additional command-line parameter is specified.
    if (nargs > 6)
    {
        // learn optimal parameters
        if (strcmp("-c", args[6]) == 0)
        {
            // Only compute the R-NN DS parameters and output them to stdout.
            
            printf("%d\n", nRadii);
            transformMemRatios();
            for(IntT i = 0; i < nRadii; i++)
            {
                // which sample queries to use
                Int32T segregatedQStart = (i == 0) ? 0 : sampleQBoundaryIndeces[i - 1];
                Int32T segregatedQNumber = nSampleQueries - segregatedQStart;
                if (segregatedQNumber == 0)
                {
                    // XXX: not the right answer
                    segregatedQNumber = nSampleQueries;
                    segregatedQStart = 0;
                }
                ASSERT(segregatedQStart < nSampleQueries);
                ASSERT(segregatedQStart >= 0);
                ASSERT(segregatedQStart + segregatedQNumber <= nSampleQueries);
                ASSERT(segregatedQNumber >= 0);
                RNNParametersT optParameters = computeOptimalParameters(listOfRadii[i],
                                                                        successProbability,
                                                                        nPoints,
                                                                        pointsDimension,
                                                                        dataSetPoints,
                                                                        segregatedQNumber,
                                                                        sampleQueries + segregatedQStart,
                                                                        (MemVarT)((availableTotalMemory - totalAllocatedMemory) * memRatiosForNNStructs[i]));
                printRNNParameters(stdout, optParameters);
            }
            exit(0);
        }
        // Read the R-NN DS parameters from the given file and run the
        // queries on the constructed data structure.
        else if (strcmp("-p", args[6]) == 0)
        {
            if (nargs < 7)
            {
                usage(args[0]);
                exit(1);
            }
            FILE *pFile = fopen(args[7], "rt");
            FAILIFWR(pFile == NULL, "Could not open the params file.");
            fscanf(pFile, "%d\n", &nRadii);
            DPRINTF1("Using the following R-NN DS parameters:\n");
            DPRINTF("N radii = %d\n", nRadii);
            FAILIF(NULL == (nnStructs = (PRNearNeighborStructT*)MALLOC(nRadii * sizeof(PRNearNeighborStructT))));
            FAILIF(NULL == (algParameters = (RNNParametersT*)MALLOC(nRadii * sizeof(RNNParametersT))));
            for(IntT i = 0; i < nRadii; i++)
            {
                algParameters[i] = readRNNParameters(pFile);
                printRNNParameters(stderr, algParameters[i]);
                nnStructs[i] = initLSH_WithDataSet(algParameters[i], nPoints, dataSetPoints);
            }
            
            pointsDimension = algParameters[0].dimension;
            FREE(listOfRadii);
            FAILIF(NULL == (listOfRadii = (RealT*)MALLOC(nRadii * sizeof(RealT))));
            for(IntT i = 0; i < nRadii; i++)
            {
                listOfRadii[i] = algParameters[i].parameterR;
            }
        }
        else
        {
            // Wrong option.
            usage(args[0]);
            exit(1);
        }
    }
    else
    {
        FAILIF(NULL == (nnStructs = (PRNearNeighborStructT*)MALLOC(nRadii * sizeof(PRNearNeighborStructT))));
        // Determine the R-NN DS parameters, construct the DS and run the queries.
        transformMemRatios();
        for(IntT i = 0; i < nRadii; i++)
        {
            // XXX: segregate the sample queries...
            nnStructs[i] = initSelfTunedRNearNeighborWithDataSet(listOfRadii[i],
                                                                 successProbability,
                                                                 nPoints,
                                                                 pointsDimension,
                                                                 dataSetPoints,
                                                                 nSampleQueries,
                                                                 sampleQueries,
                                                                 (MemVarT)((availableTotalMemory - totalAllocatedMemory) * memRatiosForNNStructs[i]));
        }
    }
    
    DPRINTF1("X\n");
    
    ////////////////////////////////////////////////////////////////////////
    // do the query
    ////////////////////////////////////////////////////////////////////////
    IntT resultSize = nPoints;
    PPointT *result = (PPointT*)MALLOC(resultSize * sizeof(*result));
    PPointT queryPoint;
    FAILIF(NULL == (queryPoint = (PPointT)MALLOC(sizeof(PointT))));
    FAILIF(NULL == (queryPoint->coordinates = (RealT*)MALLOC(pointsDimension * sizeof(RealT))));
    
    TimeVarT meanQueryTime = 0;
    PPointAndRealTStructT *distToNN = NULL;
    
    
    // load query points qhull format
    char* query_file_name = args[4];
    FILE *queryFile = fopen(query_file_name, "rt");
    FAILIF(queryFile == NULL);
    fscanf(queryFile, "%d\n", &query_pointsDimension);
    fscanf(queryFile, "%d\n", &nQueries);
    printf("Number of Query Dimension: %d, Number of Query Points: %d. \n", query_pointsDimension, nQueries);
    readDataSetFromFile(query_data_Points, queryFile, nQueries, query_pointsDimension);
    fclose(queryFile);
    
    for(IntT i = 0; i < nQueries; i++)
    {
        queryPoint = query_data_Points[i];
        /*RealT sqrLength = 0;
        // read in the query point, query_pointsDimension = pointsDimension
        for(IntT d = 0; d < pointsDimension; d++)
        {
            FSCANF_REAL(queryFile, &(queryPoint->coordinates[d]));
            sqrLength += SQR(queryPoint->coordinates[d]);
        }
        queryPoint->sqrLength = sqrLength;
        //printRealVector("Query: ", pointsDimension, queryPoint->coordinates);
        */
        
        
        // get the near neighbors.
        IntT nNNs = 0;
        for(IntT r = 0; r < nRadii; r++)
        {
            nNNs = getRNearNeighbors(nnStructs[r], queryPoint, result, resultSize);
            printf("Total time for R-NN query at radius %0.6lf (radius no. %d):\t%0.6lf\n", (double)(listOfRadii[r]), r, timeRNNQuery);
            meanQueryTime += timeRNNQuery;
            
            if (nNNs > 0)
            {
                printf("Query point %d: found %d NNs at distance %0.6lf (%dth radius). First %d NNs are:\n", i, nNNs, (double)(listOfRadii[r]), r, MIN(nNNs, MAX_REPORTED_POINTS));
                
                // compute the distances to the found NN, and sort according to the distance
                FAILIF(NULL == (distToNN = (PPointAndRealTStructT*)REALLOC(distToNN, nNNs * sizeof(*distToNN))));
                for(IntT p = 0; p < nNNs; p++)
                {
                    distToNN[p].ppoint = result[p];
                    distToNN[p].real = distance(pointsDimension, queryPoint, result[p]);
                }
                qsort(distToNN, nNNs, sizeof(*distToNN), comparePPointAndRealTStructT);
                
                // Print the points
                for(IntT j = 0; j < MIN(nNNs, MAX_REPORTED_POINTS); j++)
                {
                    ASSERT(distToNN[j].ppoint != NULL);
                    printf("%09d\tDistance:%0.6lf\n", distToNN[j].ppoint->index, distToNN[j].real);
                    CR_ASSERT(distToNN[j].real <= listOfRadii[r]);
                    //DPRINTF("Distance: %lf\n", distance(pointsDimension, queryPoint, result[j]));
                    //printRealVector("NN: ", pointsDimension, result[j]->coordinates);
                }
                break;
            }
        }
        if (nNNs == 0)
        {
            printf("Query point %d: no NNs found.\n", i);
        }
    }
    if (nQueries > 0){
        meanQueryTime = meanQueryTime / nQueries;
        printf("Mean query time: %0.6lf\n", (double)meanQueryTime);
    }
    
    for(IntT i = 0; i < nRadii; i++)
    {
        freePRNearNeighborStruct(nnStructs[i]);
    }
    // XXX: should ideally free the other stuff as well.
    
    
    return 0;
}
