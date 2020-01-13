//
// Test.cpp
//
// This is a direct port of the C version of the RTree test program.
//

#include <iostream>
#include <sys/time.h>
#include "myentry.h"
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

int nrects = sizeof(rects) / sizeof(rects[0]);

//Rect search_rect(6, 4, 10, 6); // search will find above rects that this one overlaps


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






int read_data(char *filename, float** data, int dimension, int card)
{
	int record_count = 0;
	FILE *fp;
	if((fp = fopen(filename,"r")) == NULL)
	{
		printf("Cannot open R-Tree text file .\n");
		return 1;
	}
	else
	{

		// load data
		int num_dim = -1;
		int num_element = -1;
		fscanf(fp, "%d\n", &num_dim);
		fscanf(fp, "%d\n", &num_element);
		assert(num_dim == dimension);
		assert(num_element == card);

		while (!feof(fp))
		{

			float* temp_data = new float[num_dim];
			for (int ii = 0; ii < num_dim; ++ii)
			{
				fscanf(fp, " %f", &temp_data[ii]);
			}
			fscanf(fp, "\n");
			record_count ++;
		}
		assert(feof(fp));
		fclose(fp);
	}
	cout<<"total data count: "<<record_count<<endl;
	return 0;
}

TempRect pack_data(float* data, int dim)
{
	return TempRect(dim, data);
	// return TempRect;
}

int main()
{
	int qn = 1000;
	const int MAXK = 50;
	char truth_set[100] = "/Users/sicongliu/Desktop/StreamingTopK/H2_ALSH/result/result_anti_correlated_2D_10.mip";
	Result **R = new Result*[qn];
	for (int i = 0; i < qn; ++i) R[i] = new Result[MAXK];
	if (read_ground_truth(qn, truth_set, R, MAXK) != 0)
	{
		printf("Reading Truth Set Error!\n");
		return 1;
	}


	int top_k = 5;
	int dimension = 2;
	int cardinality = 10;
	// char filepath[100] = "../StreamingTopK/H2_ALSH/raw_data/Synthetic/anti_correlated_4_100000.txt";
	char filepath[100] = "/Users/sicongliu/Desktop/StreamingTopK/H2_ALSH/raw_data/Synthetic/anti_correlated_2_10.txt";
	char querypath[100] = "/Users/sicongliu/Desktop/StreamingTopK/H2_ALSH/query/query_2D.txt";
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

	typedef RTree<ValueType, float, 2, float> MyTree;
	MyTree tree;
	int i, nhits;
	cout << "nrects = " << nrects << "\n";





	MaxK_List* list = new MaxK_List(top_k);
	float recall = 0.0f;
	timeval start_time, end_time;
	gettimeofday(&start_time, NULL);
	for(int i = 0; i < qn; i++)
	{
		printf("query index: %d...\n", i);
		float* cur_query = query[i];
		list->reset();

		// should start from the root?
		// tree.BRS(top_k, list, cur_query);
		Node * tt = tree.m_root;
		recall += calc_recall(top_k, (const Result *) R[i], list);
	}
	recall        = recall / qn;
	gettimeofday(&end_time, NULL);
	float runtime = end_time.tv_sec - start_time.tv_sec + (end_time.tv_usec -
			start_time.tv_usec) / 1000000.0f;
	runtime       = (runtime * 1000.0f) / qn;

	printf("  %3d\t\t%.4f\t\t%.2f\n", top_k, runtime, recall);

















//	for(i=0; i<nrects; i++)
//	{
//		tree.Insert(rects[i].min, rects[i].max, i); // Note, all values including zero are fine in this version
//	}

	for(i = 0; i < cardinality; i++)
	{
		// pack data into rtree node
		TempRect myrect = pack_data(data[i], dimension);
		tree.Insert(myrect.min, myrect.max, i); // Note, all values including zero are fine in this version

	}

	float search_data[] = {6.0f, 4.0f, 10.0f, 6.0f};
	TempRect search_rect(4, search_data); // search will find above rects that this one overlaps
	nhits = tree.MySearch(search_rect.min, search_rect.max, MySearchCallback);

	cout << "Search resulted in " << nhits << " hits\n";

	// Iterator test
	int itIndex = 0;
	MyTree::Iterator it;
	for( tree.GetFirst(it);
			!tree.IsNull(it);
			tree.GetNext(it) )
	{
		int value = tree.GetAt(it);

//		int boundsMin[2] = {0,0};
//		int boundsMax[2] = {0,0};
		float boundsMin[2] = {0.0f,0.0f};
		float boundsMax[2] = {0.0f,0.0f};
		it.GetBounds(boundsMin, boundsMax);
		cout << "it[" << itIndex++ << "] " << value << " = (" << boundsMin[0] << "," << boundsMin[1] << "," << boundsMax[0] << "," << boundsMax[1] << ")\n";
	}

	// Iterator test, alternate syntax
	itIndex = 0;
	tree.GetFirst(it);
	while( !it.IsNull() )
	{
		int value = *it;
		++it;
		cout << "it[" << itIndex++ << "] " << value << "\n";
	}

	// test copy constructor
	MyTree copy = tree;

	// Iterator test
	itIndex = 0;
	for (copy.GetFirst(it);
			!copy.IsNull(it);
			copy.GetNext(it) )
	{
		int value = copy.GetAt(it);

		//		int boundsMin[2] = {0,0};
		//		int boundsMax[2] = {0,0};
		float boundsMin[2] = {0.0f,0.0f};
		float boundsMax[2] = {0.0f,0.0f};
		it.GetBounds(boundsMin, boundsMax);
		cout << "it[" << itIndex++ << "] " << value << " = (" << boundsMin[0] << "," << boundsMin[1] << "," << boundsMax[0] << "," << boundsMax[1] << ")\n";
	}

	// Iterator test, alternate syntax
	itIndex = 0;
	copy.GetFirst(it);
	while( !it.IsNull() )
	{
		int value = *it;
		++it;
		cout << "it[" << itIndex++ << "] " << value << "\n";
	}

	return 0;

	// Output:
	//
	// nrects = 4
	// Hit data rect 1
	// Hit data rect 2
	// Search resulted in 2 hits
	// it[0] 0 = (0,0,2,2)
	// it[1] 1 = (5,5,7,7)
	// it[2] 2 = (8,5,9,6)
	// it[3] 3 = (7,1,9,2)
	// it[0] 0
	// it[1] 1
	// it[2] 2
	// it[3] 3
	// it[0] 0 = (0,0,2,2)
	// it[1] 1 = (5,5,7,7)
	// it[2] 2 = (8,5,9,6)
	// it[3] 3 = (7,1,9,2)
	// it[0] 0
	// it[1] 1
	// it[2] 2
	// it[3] 3
}

