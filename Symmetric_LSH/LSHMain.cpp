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
PPointT* readDataSetFromFile(PPointT *dataSetPoints, FILE *fileHandle, int num_of_points, int num_of_dimensions)
{
	FAILIF(NULL == (dataSetPoints = (PPointT*)MALLOC(num_of_points * sizeof(PPointT))));
	for(IntT i = 0; i < num_of_points; i++)
	{
		dataSetPoints[i] = readPoint(fileHandle, num_of_dimensions);
		dataSetPoints[i]->index = i;
	}
	return dataSetPoints;
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

/** flushing nnStructs to file
    return: 0 -- success
            1 -- failure
 */
/*int save_nnStructs_To_File(PRNearNeighborStructT nnStructs, int nRadii, const char* file_name)
{
    printf("Flushing nnStructs to file... \n");
    int flag = 0;
    FILE *nnStruct_File = fopen(file_name, "w");
    fprintf(nnStruct_File, "%s \n", "Flushing nnStructs to file..." );
    for(int nns = 0; nns < nRadii; nns++)
    {
        fprintf(nnStruct_File, "%s \n", nnStructs[nns] );
    }
    fclose(nnStruct_File);
    return flag;
}*/


/** flushing hashtable (defined in BucketHashing) to file
        return: 0 -- success
                1 -- failure
 */
int save_hashTable_To_File(PRNearNeighborStructT nnStructs, int nRadii, const char* file_name)
{
	printf("Flushing HashTable (using BucketHashing) to file... \n");
	int flag = 0;
	FILE *hashTable_File = fopen(file_name, "w");
	PUHashStructureT* current_hashedBuckets = nnStructs->hashedBuckets;
	fprintf(hashTable_File, "%s \n", "Flushing HashTable to file..." );
	unsigned long hashedBuckets_size = sizeof(nnStructs->hashedBuckets)/sizeof(nnStructs->hashedBuckets[0]);
	for(int i=0; i<hashedBuckets_size; i++)
	{
		HybridChainEntryT *hybridChainsStorage = current_hashedBuckets[i]->hybridChainsStorage;
		PHybridChainEntryT *hybridHashTable = current_hashedBuckets[i]->hashTable.hybridHashTable;
		printf("control value from pointer : %d .\n", (*hybridHashTable)->controlValue1);
		printf("control value from struct : %d .\n", hybridChainsStorage->controlValue1);

		printf("size1 : %d, size2 : %d, number of table: %d . \n", sizeof(hybridHashTable), sizeof(PHybridChainEntryT), sizeof(hybridHashTable)/sizeof(PHybridChainEntryT));
		printf("size1 : %d, size2 : %d, number of complex structure: %d .\n", sizeof(hybridChainsStorage), sizeof(HybridChainEntryT), sizeof(hybridChainsStorage)/sizeof(HybridChainEntryT));
	}

	fclose(hashTable_File);


	return flag;
}

/** flushing nnStructs to file, structure defined in BucketHashing.h
        return: 0 -- success
                1 -- failure
 */
int save_nnStructs_hashedBuckets_To_File(PRNearNeighborStructT nnStructs, int nRadii, const char* file_name)
{
	printf("Flushing hashedBuckets to file... \n");
	int flag = 0;
	PUHashStructureT* current_hashedBuckets = nnStructs->hashedBuckets;
	FILE *hashedBuckets_File = fopen(file_name, "w");
	fprintf(hashedBuckets_File, "%s \n", "Flushing hashedBuckets to file..." );
	fprintf(hashedBuckets_File, "%s \n", "Union bucketPoints not flushed..." );
	unsigned long hashedBuckets_size = sizeof(nnStructs->hashedBuckets)/sizeof(nnStructs->hashedBuckets[0]);
	for(int i=0; i<nnStructs->parameterL; i++)
	{
		fprintf(hashedBuckets_File, "Current iteration index: %d .\n", i);
		fprintf(hashedBuckets_File, "typeHT: %d \n", current_hashedBuckets[i]->typeHT);
		fprintf(hashedBuckets_File, "Prime Number Used: %d \n", current_hashedBuckets[i]->prime);
		fprintf(hashedBuckets_File, "hashTableSize: %d \n", current_hashedBuckets[i]->hashTableSize);
		fprintf(hashedBuckets_File, "nHashedBuckets: %d \n", current_hashedBuckets[i]->nHashedBuckets);
		fprintf(hashedBuckets_File, "nHashedPoints: %d \n", current_hashedBuckets[i]->nHashedPoints);

		/////////////////////////////////////////////////////////////////////////////
		if(current_hashedBuckets[i]->bucketPoints.pointsList == NULL)
		{
			printf("******************** \n");
			printf("bucketPoints.pointsList is null .\n");
			printf("******************** \n");
		}
		if(current_hashedBuckets[i]->bucketPoints.pointsArray == NULL)
		{
			printf("******************** \n");
			printf("bucketPoints.pointsArray is null .\n");
			printf("******************** \n");
		}

		/////////////////////////////////////////////////////////////////////////////
		if(current_hashedBuckets[i]->hashTable.llHashTable == NULL)
		{
			printf("******************** \n");
			printf("hashTable.llHashTable is null .\n");
			printf("******************** \n");
		}
		if(current_hashedBuckets[i]->hashTable.packedHashTable == NULL)
		{
			printf("******************** \n");
			printf("hashTable.packedHashTable is null .\n");
			printf("******************** \n");
		}
		if(current_hashedBuckets[i]->hashTable.linkHashTable == NULL)
		{
			printf("******************** \n");
			printf("hashTable.linkHashTable is null .\n");
			printf("******************** \n");
		}
		if(current_hashedBuckets[i]->hashTable.hybridHashTable == NULL)
		{
			printf("******************** \n");
			printf("hashTable.hybridHashTable is null .\n");
			printf("******************** \n");
		}

		/////////////////////////////////////////////////////////////////////////////
		if(current_hashedBuckets[i]->hybridChainsStorage == NULL)
		{
			printf("******************** \n");
			printf("hybridChainsStorage is null .\n");
			printf("******************** \n");
		}
		// The sizes of each of the chains of the hashtable (used only when
		// typeHT=HT_PACKED or HT_STATISTICS.
		if(current_hashedBuckets[i]->chainSizes == NULL)
		{
			printf("typeHT indicates this is a linked-list .\n");
			fprintf(hashedBuckets_File, " \n typeHT indicates this is a linked-list .\n");
			/////////////////////////////////////////////////////////////////////////////
			// To-Do:
			// output the hashed LinkedList to file
			/////////////////////////////////////////////////////////////////////////////
		}
		else
		{
			fprintf(hashedBuckets_File, "******************** \n");
			fprintf(hashedBuckets_File, "Chain size (the sizes of each of the chains of the hashtable): %lu \n", sizeof((current_hashedBuckets[i]->chainSizes))/sizeof((current_hashedBuckets[i]->chainSizes[0])));
			for(int j=0; j<1; j++)
			{
				fprintf(hashedBuckets_File, "chain index: %d, value: %d .\n", j, current_hashedBuckets[i]->chainSizes[j]);
			}
		}

		fprintf(hashedBuckets_File, "******************** \n");
		fprintf(hashedBuckets_File, "Number of main hash functions: %lu \n", sizeof((current_hashedBuckets[i]->mainHashA))/sizeof((current_hashedBuckets[i]->mainHashA[0])));
		int mainHash_size = sizeof((current_hashedBuckets[i]->mainHashA))/sizeof((current_hashedBuckets[i]->mainHashA[0]));
		for(int j=0; j<mainHash_size; j++)
		{
			fprintf(hashedBuckets_File, "mainHash index: %d, value: %d .\n", j, current_hashedBuckets[i]->mainHashA[j]);
		}

		fprintf(hashedBuckets_File, "******************** \n");
		fprintf(hashedBuckets_File, "Number of control hash functions: %lu \n", sizeof((current_hashedBuckets[i]->controlHash1))/sizeof((current_hashedBuckets[i]->controlHash1[0])));
		int controlHash_size = sizeof((current_hashedBuckets[i]->mainHashA))/sizeof((current_hashedBuckets[i]->controlHash1[0]));
		for(int j=0; j<controlHash_size; j++)
		{
			fprintf(hashedBuckets_File, "mainHash index: %d, value: %d .\n", j, current_hashedBuckets[i]->controlHash1[j]);
		}

		fprintf(hashedBuckets_File, "Hash data length: %d \n", current_hashedBuckets[i]->hashedDataLength);


		fprintf(hashedBuckets_File, "\n \n \n");
	}

	fclose(hashedBuckets_File);
	return flag;
}

/** flushing nnStructs to file, structure/LSHFunctionT defined in LocalitySensitiveHashing.h
    return: 0 -- success
            1 -- failure
 */
int save_nnStructs_LSHFunction_To_File(PRNearNeighborStructT nnStructs, int nRadii, const char* file_name)
{
	printf("Flushing LSHFunction to file... \n");
	int flag = 0;
	LSHFunctionT** current_lshFunction = nnStructs->lshFunctions;
	FILE *LSHFunction_File = fopen(file_name, "w");
	fprintf(LSHFunction_File, "%s \n", "Flushing LSHFunction to file..." );
	// unsigned long lsh_length = sizeof(current_lshFunction);
	Int32T lsh_tables = nnStructs->parameterL;
	Int32T lsh_hash_per_table = nnStructs->parameterK;
	for(int i=0; i<lsh_tables; i++)
	{
		LSHFunctionT* pmy_cur_lshFunction = current_lshFunction[i];
		for(int j=0; j<lsh_hash_per_table; j++)
		{
			LSHFunctionT my_cur_lshFunction = pmy_cur_lshFunction[j];
			int a_size = sizeof(my_cur_lshFunction.a)/sizeof(my_cur_lshFunction.a[0]);
			fprintf(LSHFunction_File, "%s ", "a : ");
			for(int k=0; k<a_size; k++)
			{
				fprintf(LSHFunction_File, "%f \t", my_cur_lshFunction.a[k]);
			}
			fprintf(LSHFunction_File, "%s ", "b : ");
			fprintf(LSHFunction_File, "%f \n", (my_cur_lshFunction.b));
		}
		fprintf(LSHFunction_File, "\n******************************\n \n");
	}
	fclose(LSHFunction_File);
	return flag;
}

/** flushing precomputedHashesOfULSHs to file, structure defined in LocalitySensitiveHashing.h
    return: 0 -- success
            1 -- failure
 */
int save_nnStructs_precomputedHashes_To_File(PRNearNeighborStructT nnStructs, int nRadii, const char* file_name)
{
	printf("Flushing precomputedHashes to file... \n");
	int flag = 0;
	unsigned int** precomputedHashesOfULSHs = nnStructs->precomputedHashesOfULSHs;
	FILE *precomputedHashesOfULSHs_File = fopen(file_name, "w");
	fprintf(precomputedHashesOfULSHs_File, "%s \n", "Flushing precomputedHashes to file..." );
	// Precomputed hashes of each of the <nHFTuples> of <u> functions
	// (to be used by the bucket hashing module)

	Int32T lsh_tables = nnStructs->parameterL;
	Int32T lsh_functions_per_table = nnStructs->parameterK;
	printf("precompute hash size check: %d .\n",  sizeof(*precomputedHashesOfULSHs)/sizeof(**precomputedHashesOfULSHs));
	for(int i=0; i<lsh_tables; i++)
	{
		for(int j=0; j<lsh_functions_per_table; j++)
		{
			fprintf(precomputedHashesOfULSHs_File, "%d ", precomputedHashesOfULSHs[i][j]);
		}
		fprintf(precomputedHashesOfULSHs_File, "\n******************************\n \n");
	}
	fclose(precomputedHashesOfULSHs_File);
	return flag;
}

/** flushing pointULSHVectors to file, structure defined in LocalitySensitiveHashing.h
        return: 0 -- success
                1 -- failure
 */
int save_nnStructs_pointULSHVectors_To_File(PRNearNeighborStructT nnStructs, int nRadii, const char* file_name)
{
	printf("Flushing pointULSHVectors to file... \n");
	int flag = 0;
	unsigned int** pointULSHVectors = nnStructs->pointULSHVectors;
	FILE *pointULSHVectors_File = fopen(file_name, "w");
	fprintf(pointULSHVectors_File, "%s \n", "Flushing pointULSHVectors to file..." );
	Int32T lsh_tables = nnStructs->parameterL;
	Int32T lsh_functions_per_table = nnStructs->parameterK;


	for(int i=0; i<lsh_tables; i++)
	{
		for(int j=0; j<lsh_functions_per_table; j++)
		{
			fprintf(pointULSHVectors_File, "%d ", pointULSHVectors[i][j]);
		}
		fprintf(pointULSHVectors_File, "\n******************************\n \n");
	}
	fclose(pointULSHVectors_File);
	return flag;
}

/** flushing reductedPoints to file, structure defined in LocalitySensitiveHashing.h
        return: 0 -- success
                1 -- failure
 */
int save_nnStructs_reducedPoint_To_File(PRNearNeighborStructT nnStructs, int nRadii, const char* file_name)
{
	printf("Flushing reducedPoint to file... \n");
	int flag = 0;
	float* reducedPoint = nnStructs->reducedPoint;
	FILE *reducedPoint_File = fopen(file_name, "w");
	fprintf(reducedPoint_File, "%s \n", "Flushing reducedPoint to file..." );
	unsigned long row = sizeof(reducedPoint)/sizeof(reducedPoint[0]);
	// fprintf(precomputedHashesOfULSHs_File, "%s \n", "a \t b " );
	for(int i=0; i<row; i++)
	{
		fprintf(reducedPoint_File, "%f \n", reducedPoint[i]);
	}

	fclose(reducedPoint_File);
	return flag;
}

/** flushing MarkedPoints and MarkedPointsIndices to file, structure defined in LocalitySensitiveHashing.h
        return: 0 -- success
                1 -- failure
 */
int save_nnStructs_MarkedPoints_To_File(PRNearNeighborStructT nnStructs, int nRadii, const char* file_name)
{
	printf("Flushing MarkedPoints/MarkedPointsIndices to file... \n");
	int flag = 0;
	BooleanT* markedPoints = nnStructs->markedPoints;
	Int32T* markedPointsIndeces = nnStructs->markedPointsIndeces;
	int sizeMarkedPoints = nnStructs->sizeMarkedPoints;
	FILE *MarkedPoints_File = fopen(file_name, "w");
	fprintf(MarkedPoints_File, "%s \n", "Flushing MarkedPoints/MarkedPointsIndices to file..." );
	fprintf(MarkedPoints_File, "%s \t", "markedPoints" );
	fprintf(MarkedPoints_File, "%s \n", "markedPointsIndeces" );
	for(int i=0; i<sizeMarkedPoints; i++)
	{
		fprintf(MarkedPoints_File, "%d \t", markedPoints[i]);
		fprintf(MarkedPoints_File, "%d \n", markedPointsIndeces[i]);
	}

	fclose(MarkedPoints_File);
	return flag;
}


/** flushing optimal parameters (can ge accessed through nnStructs) to file
    return: 0 -- success
            1 -- failure
 */
int save_nnStructs_parameters_To_File(PRNearNeighborStructT nnStructs, int nRadii, const char* file_name)
{
	printf("Flushing optimal parameters to file... \n");
	int flag = 0;
	FILE *parameter_File = fopen(file_name, "w");
	fprintf(parameter_File, "%s \n", "Flushing nnStructs to file..." );
	fprintf(parameter_File, "dimension of points: %d \n", nnStructs->dimension);
	fprintf(parameter_File, "parameter K of the algorithm: %d \n", nnStructs->parameterK);
	fprintf(parameter_File, "parameter L of the algorithm: %d \n", nnStructs->parameterL);
	fprintf(parameter_File, "parameter W of the algorithm: %f \n", nnStructs->parameterW);
	fprintf(parameter_File, "parameter T of the algorithm: %d \n", nnStructs->parameterT);
	fprintf(parameter_File, "parameter R of the algorithm: %f \n", nnStructs->parameterR);
	fprintf(parameter_File, "parameter R^2 of the algorithm: %f \n", nnStructs->parameterR2);

	fprintf(parameter_File, "\n \n \n");
	fprintf(parameter_File, "UseUfunctions (Whether to use <u> hash functions instead of usual <g>)? (boolean): %d \n", nnStructs->useUfunctions);
	fprintf(parameter_File, "Number of tuples of hash functions used (nHFTuples): %d \n", nnStructs->nHFTuples);
	fprintf(parameter_File, "How many LSH functions each of the tuple has (hfTuplesLength): %d \n", nnStructs->hfTuplesLength);
	fprintf(parameter_File, "Number of points (nPoints): %d \n", nnStructs->nPoints);
	fprintf(parameter_File, "The size of the array <points>: %d \n", nnStructs->pointsArraySize);
	fprintf(parameter_File, "Reporting Results (boolean): %d \n", nnStructs->reportingResult);
	fprintf(parameter_File, "The size of <markedPoints> and of <markedPointsIndeces>: %d \n", nnStructs->sizeMarkedPoints);

	fprintf(parameter_File, "\n \n \n");
	/*unsigned long lsh_row = sizeof(nnStructs->lshFunctions);
    // unsigned long lsh_row = sizeof(nnStructs->lshFunctions)/sizeof(nnStructs->lshFunctions[0]);
    unsigned long lsh_column = sizeof(nnStructs->lshFunctions[0])/sizeof(nnStructs->lshFunctions[0][0]);
    fprintf(parameter_File, "The size of lshFunctions (row): %lu \n", lsh_row);
    fprintf(parameter_File, "The size of lshFunctions (column): %lu \n", lsh_column);

    fprintf(parameter_File, "\n \n \n");
    unsigned long ULSH_length= sizeof(nnStructs->precomputedHashesOfULSHs)/sizeof(nnStructs->precomputedHashesOfULSHs[0]);
    fprintf(parameter_File, "The length of precomputedHashesOfULSHs (array of array): %lu \n", ULSH_length);

    fprintf(parameter_File, "\n \n \n");
    fprintf(parameter_File, "The length of hashedBuckets (array of array): %lu \n", sizeof(nnStructs->hashedBuckets)/sizeof(nnStructs->hashedBuckets[0]));

    fprintf(parameter_File, "\n \n \n");
    unsigned long ULSHvector_length = sizeof(nnStructs->pointULSHVectors)/sizeof(nnStructs->pointULSHVectors[0]);
    fprintf(parameter_File, "The length of pointULSHVectors (array of array) :  %lu \n", ULSHvector_length);*/

	fclose(parameter_File);
	return flag;
}

PRNearNeighborStructT* Process_Input_Data(PPointT **dataSetPoints, int nargs, char **args)
{
	printf("****************************************************************** .\n");
	printf("Total number of arguments: %d .\n", nargs);
	for(int nnp = 0; nnp < nargs; nnp++)
	{
		printf("Argument - %d, %s \n", nnp, args[nnp]);
	}
	printf("****************************************************************** .\n");
	successProbability = atof(args[1]);

	// Number of points in the data set, load from qhull file
	IntT nPoints = 0;

	// The dimension of the points, load from qhull file
	IntT pointsDimension = 0;

	char* endPtr[1];
	RealT thresholdR = strtod(args[2], endPtr);
	if (thresholdR == 0 || endPtr[1] == args[2])
	{
		printf("There is a file specifying multiple R's .\n");
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
		printf("Setting default number of radii .\n");
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
	char* filename = args[3];
	FILE *dataFile = fopen(filename, "rt");
	FAILIF(dataFile == NULL);
	fscanf(dataFile, "%d\n", &pointsDimension);
	ASSERT(pointsDimension > 0);
	fscanf(dataFile, "%d\n", &nPoints);
	ASSERT(nPoints > 0);
	printf("Number of Dimension: %d, number of Points: %d. \n", pointsDimension, nPoints);
	*dataSetPoints = readDataSetFromFile(*dataSetPoints, dataFile, nPoints, pointsDimension);

	fclose(dataFile);
	printf("Reading data done... \n");


	if (nPoints > MAX_N_POINTS)
	{
		printf("Error: the structure supports at most %d points (%d were specified).\n", MAX_N_POINTS, nPoints);
		fprintf(ERROR_OUTPUT, "Error: the structure supports at most %d points (%d were specified).\n", MAX_N_POINTS, nPoints);
		exit(1);
	}

	RNNParametersT *algParameters = NULL;
	PRNearNeighborStructT *nnStructs = NULL;

	printf("Loading parameters from input file. \n");

	FILE *parameterFile = fopen(args[7], "rt");
	FAILIFWR(parameterFile == NULL, "Could not open the params file.");
	fscanf(parameterFile, "%d\n", &nRadii);
	DPRINTF1("Using the following R-NN DS parameters:\n");
	DPRINTF("N radii = %d\n", nRadii);
	FAILIF(NULL == (nnStructs = (PRNearNeighborStructT*)MALLOC(nRadii * sizeof(PRNearNeighborStructT))));
	FAILIF(NULL == (algParameters = (RNNParametersT*)MALLOC(nRadii * sizeof(RNNParametersT))));
	for(IntT i = 0; i < nRadii; i++)
	{
		algParameters[i] = readRNNParameters(parameterFile);
		printRNNParameters(stderr, algParameters[i]);
		nnStructs[i] = initLSH_WithDataSet(algParameters[i], nPoints, *dataSetPoints);
	}

	pointsDimension = algParameters[0].dimension;
	FREE(listOfRadii);
	FAILIF(NULL == (listOfRadii = (RealT*)MALLOC(nRadii * sizeof(RealT))));
	for(IntT i = 0; i < nRadii; i++)
	{
		listOfRadii[i] = algParameters[i].parameterR;
	}

	return nnStructs;
}

/*
 The main entry to LSH package. Depending on the command line
 parameters, the function computes the R-NN data structure optimal
 parameters and/or construct the R-NN data structure and runs the
 queries on the data structure.
 */
int main(int nargs, char **args)
{
	/* Load data points*/
	PPointT *dataSetPoints;
	PRNearNeighborStructT* nnStructs =  Process_Input_Data(&dataSetPoints, nargs, args);

	/* Persist nnStruct to file*/


	/* Load queries from file*/
	PPointT *query_data_Points = NULL;
	// Number of query points in the data set.
	IntT nQueries = 0;

	// The dimension of the query points, equal to dimension of data points
	IntT query_pointsDimension = 0;
	IntT resultSize = 6; // could be of user's interest

	// load query points qhull format
	char* query_file_name = args[4];
	FILE *queryFile = fopen(query_file_name, "rt");
	FAILIF(queryFile == NULL);
	fscanf(queryFile, "%d\n", &query_pointsDimension);
	fscanf(queryFile, "%d\n", &nQueries);
	query_data_Points = readDataSetFromFile(query_data_Points, queryFile, nQueries, query_pointsDimension);
	printf("Number of Query Dimension: %d, Number of Query Points: %d. \n", query_pointsDimension, nQueries);
	fclose(queryFile);

	PPointT *result = (PPointT*)MALLOC(resultSize * sizeof(*result));
	PPointT queryPoint;
	FAILIF(NULL == (queryPoint = (PPointT)MALLOC(sizeof(PointT))));
	FAILIF(NULL == (queryPoint->coordinates = (RealT*)MALLOC(query_pointsDimension * sizeof(RealT))));


	////////////////////////////////////////////////////////////////////////
	// do the query
	////////////////////////////////////////////////////////////////////////

	TimeVarT meanQueryTime = 0;
	PPointAndRealTStructT *distToNN = NULL;

	const char* results_file_name = "TopK_Results.txt";
	FILE *results_file = fopen(results_file_name, "w");
	for(IntT i = 0; i < nQueries; i++)
	{
		fprintf(results_file, "Query Index: %d. \n", i);
		queryPoint = query_data_Points[i];

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

					// Use Euclidean distance to compute distance between query and retrieved data points
					distToNN[p].real = distance(query_pointsDimension, queryPoint, result[p]);
					/**
					 * comment from Sicong:
					 * combine query with data point using dot product then re-rank them
					 * my_combined_score -- defined in Geometry.cpp
					 * */
					// distToNN[p].real = my_combined_score(pointsDimension, queryPoint, result[p]);
				}
				// sort in ascending order due to Euclidean distance
				qsort(distToNN, nNNs, sizeof(*distToNN), comparePPointAndRealTStructT);
				/**Changed by Sicong
				 * Using dot product
				 * my_comparePPointAndRealTStructT/comparePPointAndREALTStruct -- defined in Geometry.cpp
				 * */
				// sort in descending order because of dot product
				// qsort(distToNN, nNNs, sizeof(*distToNN), my_comparePPointAndRealTStructT);

				for(IntT j = 0; j < MIN(nNNs, MAX_REPORTED_POINTS); j++)
				{
					ASSERT(distToNN[j].ppoint != NULL);
					printf("%09d\tDistance:%0.6lf\n", distToNN[j].ppoint->index, distToNN[j].real);

					fprintf(results_file, "%09d\tDistance:%0.6lf\t", distToNN[j].ppoint->index, distToNN[j].real);

					for(IntT input_data_dimension = 0; input_data_dimension < query_pointsDimension; input_data_dimension++)
					{
						fprintf(results_file, "%0.6lf\t", dataSetPoints[distToNN[j].ppoint->index]->coordinates[input_data_dimension]);
					}
					fprintf(results_file, "\n");
					/**
					 * Comment out CR_ASSERT function by Sicong
					 * Radius does not make sense in MIPS
					 * */
					// CR_ASSERT(distToNN[j].real <= listOfRadii[r]);
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
		fprintf(results_file, "******************************************** \n");
	}
	fclose(results_file);
	if (nQueries > 0)
	{
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
