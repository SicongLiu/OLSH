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

	/* load data points qhull format*/
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

/* Persist Hashing Scheme to file*/
void Persist_nnStruct(PRNearNeighborStructT* nnStructs, const char* file_name, int nRadii)
{
	printf("Persisting nnStruct to file... \n");
	FILE *pFile = fopen(file_name, "w");
	for(IntT i = 0; i < nRadii; i++)
	{
		fprintf(pFile, "%d \n", nnStructs[i]->dimension);	// dimension of points.
		fprintf(pFile, "%d \n", nnStructs[i]->parameterK);	// parameter K of the algorithm.
		fprintf(pFile, "%d \n", nnStructs[i]->parameterL);	// parameter L of the algorithm.
		fprintf(pFile, "%f \n", nnStructs[i]->parameterW);	// parameter W of the algorithm.
		fprintf(pFile, "%d \n", nnStructs[i]->parameterT);	// parameter T of the algorithm.
		fprintf(pFile, "%f \n", nnStructs[i]->parameterR);	// parameter R of the algorithm.
		fprintf(pFile, "%f \n", nnStructs[i]->parameterR2);	// = parameterR^2
		fprintf(pFile, "%d \n", nnStructs[i]->useUfunctions);	// boolean type
		fprintf(pFile, "%d \n", nnStructs[i]->nHFTuples);
		fprintf(pFile, "%d \n", nnStructs[i]->hfTuplesLength);
		fprintf(pFile, "%d \n", nnStructs[i]->nPoints);

		// fprint points here: PPointT *points;
		for(IntT p = 0; p < nnStructs[i]->nPoints; p++)
		{
			for(IntT d = 0; d < nnStructs[i]->dimension; d++)
			{
				fprintf(pFile, "%f \t", nnStructs[i]->points[p]->coordinates[d]);
			}
			fprintf(pFile, "\n");
			fprintf(pFile, "%d\n", nnStructs[i]->points[p]->index);
			fprintf(pFile, "%f\n", nnStructs[i]->points[p]->sqrLength);
		}

		fprintf(pFile, "%d \n", nnStructs[i]->pointsArraySize);
		fprintf(pFile, "%d \n", nnStructs[i]->reportingResult);	// boolean type

		// output LSH function here: LSHFunctionT **lshFunctions;
		LSHFunctionT** current_lshFunction = nnStructs[i]->lshFunctions;
		Int32T lsh_tables = nnStructs[i]->parameterL;
		Int32T lsh_hash_per_table = nnStructs[i]->parameterK;
		for(int i=0; i<lsh_tables; i++)
		{
			LSHFunctionT* pmy_cur_lshFunction = current_lshFunction[i];
			for(int j=0; j<lsh_hash_per_table; j++)
			{
				LSHFunctionT my_cur_lshFunction = pmy_cur_lshFunction[j];
				int a_size = sizeof(my_cur_lshFunction.a)/sizeof(my_cur_lshFunction.a[0]);
				for(int k=0; k<a_size; k++)
				{
					fprintf(pFile, "%f \t", my_cur_lshFunction.a[k]);
				}
				fprintf(pFile, "\n");
				fprintf(pFile, "%f \n", (my_cur_lshFunction.b));
			}
		}

		// output precomputedHashesOfULSHs: Uns32T **precomputedHashesOfULSHs;
		unsigned int** precomputedHashesOfULSHs = nnStructs[i]->precomputedHashesOfULSHs;
		// Precomputed hashes of each of the <nHFTuples> of <u> functions
		// (to be used by the bucket hashing module)
		// printf("precompute hash size check: %d .\n",  sizeof(*precomputedHashesOfULSHs)/sizeof(**precomputedHashesOfULSHs));
		for(int ii=0; ii<nnStructs[i]->parameterL; ii++)
		{
			for(int jj=0; jj<nnStructs[i]->parameterK; jj++)
			{
				fprintf(pFile, "%d \t", precomputedHashesOfULSHs[ii][jj]);
			}
			fprintf(pFile, "\n");
		}

		// output hashedBuckets: PUHashStructureT *hashedBuckets;
		PUHashStructureT* current_hashedBuckets = nnStructs[i]->hashedBuckets;
		for(int ii=0; ii<nnStructs[i]->parameterL; ii++)
		{
			// fprintf(pFile, "Current iteration index: %d .\n", ii);
			fprintf(pFile, "%d \n", current_hashedBuckets[ii]->typeHT);
			// save hashTableSize
			fprintf(pFile, "%d \n", current_hashedBuckets[ii]->hashTableSize);

			// save nHashedBuckets
			fprintf(pFile, "%d \n", current_hashedBuckets[ii]->nHashedBuckets);

			// save nHashedPoints
			fprintf(pFile, "%d \n", current_hashedBuckets[ii]->nHashedPoints);

			// save the prime number
			fprintf(pFile, "%d \n", current_hashedBuckets[ii]->prime);	// the prime used for the universal hash functions.

			// save IntT hashedDataLength
			fprintf(pFile, "%d \n", current_hashedBuckets[ii]->hashedDataLength);
			/* HybridHashTable Stores the real stuff used for query processing*/
			fprintf(pFile, "Saving hybridHashTable... \n");
			for (int jj = 0; jj < nnStructs[i]->nPoints; jj++)
			{
				PHybridChainEntryT indexHybrid = current_hashedBuckets[ii]->hashTable.hybridHashTable[jj];
				if(indexHybrid != NULL)
				{
					if(indexHybrid->isControlValue == true)
					{
						fprintf(pFile, "%d \n", indexHybrid->realHybridChainEntryT.controlValue1);
					}
					else
					{
						fprintf(pFile, "%d \n", indexHybrid->realHybridChainEntryT.point.isLastBucket);
						fprintf(pFile, "%d \n", indexHybrid->realHybridChainEntryT.point.bucketLength);
						fprintf(pFile, "%d \n", indexHybrid->realHybridChainEntryT.point.isLastPoint);
						fprintf(pFile, "%d \n", indexHybrid->realHybridChainEntryT.point.pointIndex);
					}
				}
			}

			// save Uns32T *mainHashA;
			// int mainHash_size = sizeof((current_hashedBuckets[ii]->mainHashA))/sizeof((current_hashedBuckets[ii]->mainHashA[0]));
			int mainHash_size = current_hashedBuckets[ii]->hashedDataLength;
			for(int jj=0; jj<mainHash_size; jj++)
			{
				fprintf(pFile, "%d \n", current_hashedBuckets[ii]->mainHashA[jj]);
			}

			// save Uns32T *controlHash1;
			// int controlHash_size = sizeof((current_hashedBuckets[ii]->mainHashA))/sizeof((current_hashedBuckets[ii]->controlHash1[0]));
			int controlHash_size = current_hashedBuckets[ii]->hashedDataLength;
			for(int jj=0; jj<controlHash_size; jj++)
			{
				fprintf(pFile, "%d \n", current_hashedBuckets[ii]->controlHash1[jj]);
			}

		}

		// output pointULSHVectors: Uns32T **pointULSHVectors;
		unsigned int** pointULSHVectors = nnStructs[i]->pointULSHVectors;
		for(int ii=0; ii<nnStructs[i]->parameterL; ii++)
		{
			for(int jj=0; jj<nnStructs[i]->parameterK; jj++)
			{
				fprintf(pFile, "%d ", pointULSHVectors[ii][jj]);
			}
			fprintf(pFile, "\n");
		}

		// output reducedPoint: RealT *reducedPoint;
		float* reducedPoint = nnStructs[i]->reducedPoint;
		for(int ii = 0; ii < nnStructs[i]->dimension; ii++)
		{
			fprintf(pFile, "%f\t", reducedPoint[ii]);
		}
		fprintf(pFile, "\n");

		// output markedPoints: BooleanT *markedPoints;
		// output markedPointsIndeces: Int32T *markedPointsIndeces;
		BooleanT* markedPoints = nnStructs[i]->markedPoints;
		Int32T* markedPointsIndeces = nnStructs[i]->markedPointsIndeces;
		int sizeMarkedPoints = nnStructs[i]->sizeMarkedPoints;
		for(int ii=0; ii<sizeMarkedPoints; ii++)
		{
			fprintf(pFile, "%d \t", markedPoints[ii]);
			fprintf(pFile, "%d \n", markedPointsIndeces[ii]);
		}

		fprintf(pFile, "%d \n", nnStructs[i]->sizeMarkedPoints);	// boolean type
	}

	fclose(pFile);
}

PRNearNeighborStructT* Load_nnStruct(const char* file_name)
{
	printf("Loading nnStruct to RAM... \n");
	FILE *pFile = fopen(file_name, "rt");
	RNNParametersT *algParameters = NULL;
	PRNearNeighborStructT *nnStructs = NULL;

	FAILIF(NULL == (nnStructs = (PRNearNeighborStructT*)MALLOC(nRadii * sizeof(PRNearNeighborStructT))));
	FAILIF(NULL == (algParameters = (RNNParametersT*)MALLOC(nRadii * sizeof(RNNParametersT))));
	for(int i=0; i<nRadii; i++)
	{
		FAILIF(NULL == (nnStructs[i] = (PRNearNeighborStructT)MALLOC(sizeof(RNearNeighborStructT))));
		fscanf(pFile, "%d\n", &nnStructs[i]->dimension);
		fscanf(pFile, "%d\n", &nnStructs[i]->parameterK);	// parameter K of the algorithm.
		fscanf(pFile, "%d\n", &nnStructs[i]->parameterL);	// parameter L of the algorithm.
		fscanf(pFile, "%f\n", &nnStructs[i]->parameterW);	// parameter W of the algorithm.
		fscanf(pFile, "%d\n", &nnStructs[i]->parameterT);	// parameter T of the algorithm.
		fscanf(pFile, "%f\n", &nnStructs[i]->parameterR);	// parameter R of the algorithm.
		fscanf(pFile, "%f\n", &nnStructs[i]->parameterR2);	// = parameterR^2
		fscanf(pFile, "%d\n", &nnStructs[i]->useUfunctions);	// boolean type
		fscanf(pFile, "%d\n", &nnStructs[i]->nHFTuples);
		fscanf(pFile, "%d\n", &nnStructs[i]->hfTuplesLength);
		fscanf(pFile, "%d\n", &nnStructs[i]->nPoints);
		fscanf(pFile, "%d\n", &nnStructs[i]->sizeMarkedPoints);	// boolean type

		FAILIF(NULL == (nnStructs[i]->points = (PPointT*)MALLOC(nnStructs[i]->pointsArraySize * sizeof(PPointT))));
		// Read PPointT *points;
		for(IntT p = 0; p < nnStructs[i]->nPoints; p++)
		{
			char* line = NULL;
			fscanf(pFile, "%s\n", line);
			float f_number = 0;
			int cur_offset, d_index = 0;
			while( 1 == sscanf(line, "%f\t[^\n]", f_number, &cur_offset) )
			{
				nnStructs[i]->points[p]->coordinates[d_index] = f_number;
				d_index++;
			}
			fscanf(pFile, "%f\n", &nnStructs[i]->points[p]->index);
			fscanf(pFile, "%f\n", &nnStructs[i]->points[p]->sqrLength);
		}

		fscanf(pFile, "%d\n", &nnStructs[i]->pointsArraySize);
		fscanf(pFile, "%d\n", &nnStructs[i]->reportingResult);	// boolean type

		// output LSH function here: LSHFunctionT **lshFunctions;
		LSHFunctionT **lshFunctions;
		// allocate memory for the functions
		FAILIF(NULL == (lshFunctions = (LSHFunctionT**)MALLOC(nnStructs[i]->nHFTuples * sizeof(LSHFunctionT*))));
		for(IntT ii = 0; ii < nnStructs[i]->nHFTuples; ii++)
		{
			FAILIF(NULL == (lshFunctions[ii] = (LSHFunctionT*)MALLOC(nnStructs[i]->hfTuplesLength * sizeof(LSHFunctionT))));
			for(IntT jj = 0; jj < nnStructs[i]->hfTuplesLength; jj++)
			{
				FAILIF(NULL == (lshFunctions[ii][jj].a = (RealT*)MALLOC(nnStructs[i]->dimension * sizeof(RealT))));
			}
		}

		for(IntT ii = 0; ii < nnStructs[i]->nHFTuples; ii++)
		{
			for(IntT jj = 0; jj < nnStructs[i]->hfTuplesLength; jj++)
			{
				char* line = NULL;
				fscanf(pFile, "%s\n", line);
				float f_number = 0;
				int cur_offset, d_index = 0;
				while( 1 == sscanf(line, "%f\t[^\n]", f_number, &cur_offset) )
				{
					lshFunctions[ii][jj].a[d_index] = f_number;
					d_index++;
				}
				fscanf(pFile, "%f\n", lshFunctions[ii][jj].b);
			}
		}
		nnStructs[i]->lshFunctions = lshFunctions;


		// read precomputedHashesOfULSHs: Uns32T **precomputedHashesOfULSHs;
		FAILIF(NULL == (nnStructs[i]->precomputedHashesOfULSHs = (Uns32T**)MALLOC(nnStructs[i]->nHFTuples * sizeof(Uns32T*))));
		for(IntT ii = 0; ii < nnStructs[i]->nHFTuples; ii++)
		{
			FAILIF(NULL == (nnStructs[i]->precomputedHashesOfULSHs[ii] = (Uns32T*)MALLOC(N_PRECOMPUTED_HASHES_NEEDED * sizeof(Uns32T))));
		}

		for(IntT ii = 0; ii < nnStructs[i]->nHFTuples; ii++)
		{
			char* line = NULL;
			fscanf(pFile, "%s\n", line);
			float f_number = 0;
			int cur_offset, d_index = 0;
			while( 1 == sscanf(line, "%f\t[^\n]", f_number, &cur_offset) )
			{
				nnStructs[i]->precomputedHashesOfULSHs[ii][d_index] = f_number;
				d_index++;
			}
		}
		// read hashedBuckets: PUHashStructureT *hashedBuckets;
		FAILIF(NULL == (nnStructs[i]->hashedBuckets = (PUHashStructureT*)MALLOC(nnStructs[i]->parameterL * sizeof(PUHashStructureT))));

		for(int ii=0; ii<nnStructs[i]->parameterL; ii++)
		{
			fscanf(pFile, "%d\n", &nnStructs[i]->hashedBuckets[ii]->typeHT);
			fscanf(pFile, "%d \n", &nnStructs[i]->hashedBuckets[ii]->hashTableSize);
			// read nHashedBuckets
			fscanf(pFile, "%d \n", &nnStructs[i]->hashedBuckets[ii]->nHashedBuckets);

			// read nHashedPoints
			fscanf(pFile, "%d \n", &nnStructs[i]->hashedBuckets[ii]->nHashedPoints);

			// read the prime number
			fscanf(pFile, "%d \n", &nnStructs[i]->hashedBuckets[ii]->prime);	// the prime used for the universal hash functions.

			// read IntT hashedDataLength
			fscanf(pFile, "%d \n", &nnStructs[i]->hashedBuckets[ii]->hashedDataLength);

			FAILIF(NULL == (nnStructs[i]->hashedBuckets[ii]->hashTable.hybridHashTable = (PHybridChainEntryT*)MALLOC(nnStructs[i]->hashedBuckets[ii]->hashTableSize * sizeof(PHybridChainEntryT))));

			int count = 0;
			fscanf(pFile, "%d \n", &count);
			/*
			for(int jj = 0; jj < count; jj++)
			{
				int temp_index = -1;
				fscanf(pFile, "%d \n", &temp_index);
				fscanf(pFile, "%d \n", &nnStructs[i]->hashedBuckets[ii]->hashTable.hybridHashTable[temp_index]->controlValue1);
				int isLastBucket = 0;
				fscanf(pFile, "%d \n", &isLastBucket);
				nnStructs[i]->hashedBuckets[ii]->hashTable.hybridHashTable[temp_index]->point.isLastBucket = isLastBucket;

				int bucketLength = 0;
				fscanf(pFile, "%d \n", &bucketLength);
				nnStructs[i]->hashedBuckets[ii]->hashTable.hybridHashTable[temp_index]->point.bucketLength = bucketLength;

				int isLastPoint = 0;
				fscanf(pFile, "%d \n", &isLastPoint);
				nnStructs[i]->hashedBuckets[ii]->hashTable.hybridHashTable[temp_index]->point.isLastPoint = isLastPoint;

				int pointIndex = 0;
				fscanf(pFile, "%d \n", &pointIndex);
				nnStructs[i]->hashedBuckets[ii]->hashTable.hybridHashTable[temp_index]->point.pointIndex = pointIndex;
			}
			*/
			// read Uns32T *mainHashA;
			FAILIF(NULL == (nnStructs[i]->hashedBuckets[ii]->controlHash1 = (Uns32T*)MALLOC(nnStructs[i]->hashedBuckets[ii]->hashedDataLength * sizeof(Uns32T))));
			for(int jj=0; jj<nnStructs[i]->hashedBuckets[ii]->hashedDataLength; jj++)
			{
				fscanf(pFile, "%d\n", nnStructs[i]->hashedBuckets[ii]->mainHashA[jj]);
			}

			// read Uns32T *controlHash1;
			FAILIF(NULL == (nnStructs[i]->hashedBuckets[ii]->controlHash1 = (Uns32T*)MALLOC(nnStructs[i]->hashedBuckets[ii]->hashedDataLength * sizeof(Uns32T))));
			for(int jj=0; jj<nnStructs[i]->hashedBuckets[ii]->hashedDataLength; jj++)
			{
				fscanf(pFile, "%d\n", &nnStructs[i]->hashedBuckets[ii]->controlHash1[jj]);
			}
		}
		// read pointULSHVectors: Uns32T **pointULSHVectors;
		FAILIF(NULL == (nnStructs[i]->pointULSHVectors = (Uns32T**)MALLOC(nnStructs[i]->nHFTuples * sizeof(Uns32T*))));
		for(IntT i = 0; i < nnStructs[i]->nHFTuples; i++)
		{
			FAILIF(NULL == (nnStructs[i]->pointULSHVectors[i] = (Uns32T*)MALLOC(nnStructs[i]->hfTuplesLength * sizeof(Uns32T))));
		}

		for(int ii=0; ii<nnStructs[i]->parameterL; ii++)
		{
			char* ULSH_line = NULL;
			fscanf(pFile, "%s\n", &ULSH_line);
			int ULSH_value = 0;
			int cur_offset, d_index = 0;
			while( 1 == sscanf(ULSH_line, "%f\t[^\n]", ULSH_value, &cur_offset) )
			{
				nnStructs[i]->pointULSHVectors[ii][d_index] = ULSH_value;
				d_index++;
			}
		}
		// read reducedPoint: RealT *reducedPoint;
		// init the vector <reducedPoint>
		FAILIF(NULL == (nnStructs[i]->reducedPoint = (RealT*)MALLOC(nnStructs[i]->dimension * sizeof(RealT))));

		char* reduced_point_line = NULL;
		fscanf(pFile, "%s\n", &reduced_point_line);
		float point_number = 0;
		int cur_offset, d_index = 0;
		while( 1 == sscanf(reduced_point_line, "%f\t[^\n]", point_number, &cur_offset) )
		{
			nnStructs[i]->reducedPoint[d_index] = point_number;
			d_index++;
		}

		// read markedPoints: BooleanT *markedPoints;
		// read markedPointsIndeces: Int32T *markedPointsIndeces;
		// init the vector <nearPoints>
		FAILIF(NULL == (nnStructs[i]->markedPoints = (BooleanT*)MALLOC(nnStructs[i]->sizeMarkedPoints * sizeof(BooleanT))));


		for(IntT ii = 0; ii < nnStructs[i]->sizeMarkedPoints; ii++)
		{
			fscanf(pFile, "%d\n", &nnStructs[i]->markedPoints[ii]);
		}

		// init the vector <nearPointsIndeces>
		FAILIF(NULL == (nnStructs[i]->markedPointsIndeces = (Int32T*)MALLOC(nnStructs[i]->sizeMarkedPoints * sizeof(Int32T))));
		for(int ii=0; ii<nnStructs[i]->sizeMarkedPoints; ii++)
		{
			fscanf(pFile, "%d\n", &nnStructs[i]->markedPointsIndeces[ii]);
		}
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
	int nRadii = 1;

	// read nnRadii from parameter file
	FILE *parameterFile = fopen(args[7], "rt");
	FAILIFWR(parameterFile == NULL, "Could not open the params file.");
	fscanf(parameterFile, "%d\n", &nRadii);

	const char* nnStructs_file_name = "nn_Structs_file.txt";
	Persist_nnStruct(nnStructs, nnStructs_file_name, nRadii);

	/* Load nnStruct from file*/
	// nnStructs = Load_nnStruct(nnStructs_file_name);

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


	/* Load nnStruct*/
	// PRNearNeighborStructT* nnStructs =  Load_nnStruct(nnStructs_file_name);


	/* Do the query*/
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
