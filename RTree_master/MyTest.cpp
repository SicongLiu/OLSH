//
// Test.cpp
//
// This is a direct port of the C version of the RTree test program.
//

#include <iostream>
#include <algorithm>
#include <vector>
#include <sys/time.h>
#include "max_list.h"
#include "RTree.h"
#include "gendef.h"

using namespace std;

typedef float ValueType;

struct TempRect
{
	int dim;
	float* min;
	float* max;
	TempRect(int dim_, float* data)
	{
		dim = dim_;
		min = (float*) malloc (dim);
		max = (float*) malloc (dim);
		for(int i= 0; i < dim; i++)
		{
			min[i] = data[i];
			max[i] = data[i];
		}
	}
};


struct Rect
{
	Rect()  {}

	Rect(int a_minX, int a_minY, int a_maxX, int a_maxY)
	{
		min[0] = a_minX;
		min[1] = a_minY;

		max[0] = a_maxX;
		max[1] = a_maxY;
	}


	int min[2];
	int max[2];
};

struct Rect rects[] =
{
		Rect(0, 0, 2, 2), // xmin, ymin, xmax, ymax (for 2 dimensional RTree)
		Rect(5, 5, 7, 7),
		Rect(8, 5, 9, 6),
		Rect(7, 1, 9, 2),
};

void checkpoint(int   k,	const Result *R, vector<float> myvector)
{
	int i = k - 1;
	int last = k - 1;
	cout<<"vector size: "<<myvector.size()<<", comparing ground truth: " << R[last].key_;
	for(int i = myvector.size() - 1; i >=0 ; i--)
	{
		cout<<", value: "<<myvector.at(i);
	}
	cout<<endl;
}

float calc_recall(					// calc recall (percentage)
	int   k,							// top-k value
	const Result *R,					// ground truth results
	vector<float> myvector)					// results returned by algorithms
{
	int i = k - 1;
	int last = k - 1;
	while (i >= 0 && R[last].key_ - myvector.at(i) > FLOATZERO) {
		i--;
	}
	return (i + 1) * 100.0f / k;
}


int nrects = sizeof(rects) / sizeof(rects[0]);



bool MySearchCallback(ValueType id)
{
	cout << "Hit data rect " << id << "\n";
	return true; // keep going
}


int read_ground_truth(				// read ground truth results from disk
		int qn,								// number of query objects
		const char *fname,					// address of truth set
		Result **R,
		int MAXK)							// ground truth results (return)
{
	FILE *fp = fopen(fname, "r");
	if (!fp)
	{
		printf("Could not open %s\n", fname);
		return 1;
	}

	int tmp1 = -1;
	int tmp2 = -1;
	fscanf(fp, "%d %d\n", &tmp1, &tmp2);
	assert(tmp1 == qn && tmp2 == MAXK);
	for (int i = 0; i < qn; ++i)
	{
		for (int j = 0; j < MAXK; ++j)
		{
			fscanf(fp, "%d %f ", &R[i][j].id_, &R[i][j].key_);
		}
		fscanf(fp, "\n");
	}
	fclose(fp);

	return 0;
}



int read_data(	const char *fname, float **data, int d, int n)
{
	FILE *fp = fopen(fname, "r");
	if (!fp)
	{
		printf("Could not open %s\n", fname);
		return 1;
	}

	int num_dim = -1;
	int num_element = -1;
	fscanf(fp, "%d\n", &num_dim);
	fscanf(fp, "%d\n", &num_element);

	assert(num_dim == d);
	assert(num_element == n);

	int i   = 0;
	while (!feof(fp) && i < n)
	{
		for (int j = 0; j < d; ++j)
		{
			fscanf(fp, " %f", &data[i][j]);
		}
		fscanf(fp, "\n");

		++i;
	}
	assert(feof(fp) && i == n);
	fclose(fp);

	return 0;
}


TempRect pack_data(float* data, int dim)
{
	return TempRect(dim, data);
}

int main()
{
	int qn = 1000;
	const int MAXK = 50;
	char truth_set[100] = "../H2_ALSH/result/result_correlated_4D_200000.mip";
	int top_k = 25;
	int dimension = 4;
	int cardinality = 200000;
	char filepath[100] = "../H2_ALSH/raw_data/Synthetic/correlated_4_200000.txt";
	char querypath[100] = "../H2_ALSH/query/query_4D.txt";
	typedef RTree<ValueType, float, 4, float> MyTree;
	timeval start_time, end_time;


	Result **R = new Result*[qn];
	for (int i = 0; i < qn; ++i) R[i] = new Result[MAXK];
	if (read_ground_truth(qn, truth_set, R, MAXK) != 0)
	{
		printf("Reading Truth Set Error!\n");
		return 1;
	}

	float** data = new float*[cardinality];
	for (int i = 0; i < cardinality; ++i)
	{
		data[i] = new float[dimension];
	}
	if (read_data(filepath, data, dimension, cardinality) != 0)
	{
		printf("Reading dataset error!\n");
		return 1;
	}

	float** query = new float*[qn];
	for (int i = 0; i < qn; ++i)
	{
		query[i] = new float[dimension];
	}
	if (read_data(querypath, query, dimension, qn) != 0)
	{
		printf("Reading dataset error!\n");
		return 1;
	}


	MyTree tree;
	int i, nhits;

	gettimeofday(&start_time, NULL);
	for(i = 0; i < cardinality; i++)
	{
		// pack data into rtree node
		TempRect myrect = pack_data(data[i], dimension);
		tree.Insert(myrect.min, myrect.max, i); // Note, all values including zero are fine in this version

	}
	gettimeofday(&end_time, NULL);

	float building_tree = end_time.tv_sec - start_time.tv_sec + (end_time.tv_usec -
				start_time.tv_usec) / 1000000.0f;


	cout<<"Tree building time: "<<building_tree<<", total card: "<< cardinality<<", data insertion done"<<endl;
	vector<float> myvector;
	float recall = 0.0f;


	gettimeofday(&start_time, NULL);
	for(int i = 0; i < qn; i++)
	{
		// printf("query index: %d...\n", i);
		float* cur_query = query[i];
		myvector.clear();

		tree.BRS(top_k, myvector, cur_query);

		sort(myvector.begin(), myvector.end(), less<float>());

		// checkpoint(top_k, (const Result *) R[i], myvector);
		recall += calc_recall(top_k, (const Result *) R[i], myvector);
	}
	recall        = recall / qn;
	gettimeofday(&end_time, NULL);
	float runtime = end_time.tv_sec - start_time.tv_sec + (end_time.tv_usec -
			start_time.tv_usec) / 1000000.0f;
	runtime       = (runtime * 1000.0f) / qn;

	printf("  %3d\t\t%.4f\t\t%.2f\n", top_k, runtime, recall);


	return 0;
}

