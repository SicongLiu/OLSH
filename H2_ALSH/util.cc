#include "headers.h"

// -----------------------------------------------------------------------------
int ResultComp(						// compare function for qsort (ascending)
	const void *e1,						// 1st element
	const void *e2)						// 2nd element
{
	int ret = 0;
	Result *item1 = (Result*) e1;
	Result *item2 = (Result*) e2;

	if (item1->key_ < item2->key_) {
		ret = -1;
	} 
	else if (item1->key_ > item2->key_) {
		ret = 1;
	} 
	else {
		if (item1->id_ < item2->id_) ret = -1;
		else if (item1->id_ > item2->id_) ret = 1;
	}
	return ret;
}

// -----------------------------------------------------------------------------
int ResultCompDesc(					// compare function for qsort (descending)
	const void *e1,						// 1st element
	const void *e2)						// 2nd element
{
	int ret = 0;
	Result *item1 = (Result*) e1;
	Result *item2 = (Result*) e2;

	if (item1->key_ < item2->key_) {
		ret = 1;
	} 
	else if (item1->key_ > item2->key_) {
		ret = -1;
	} 
	else {
		if (item1->id_ < item2->id_) ret = -1;
		else if (item1->id_ > item2->id_) ret = 1;
	}
	return ret;
}

// -----------------------------------------------------------------------------
void create_dir(					// create dir if the path exists
	char *path)							// input path
{
	int len = (int) strlen(path);
	for (int i = 0; i < len; ++i) {
		if (path[i] == '/') {
			char ch = path[i + 1];
			path[i + 1] = '\0';
									// check whether the directory exists
			int ret = access(path, F_OK);
			if (ret != 0) {			// create the directory
				ret = mkdir(path, 0755);
				if (ret != 0) {
					printf("Could not create directory %s\n", path);
				}
			}
			path[i + 1] = ch;
		}
	}
}

// -----------------------------------------------------------------------------
int read_data(						// read data/query set from disk
	int   n,							// number of data/query objects
	int   d,			 				// dimensionality
	const char *fname,					// address of data/query set
	float **data)						// data/query objects (return)
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
	// int tmp = -1;
	while (!feof(fp) && i < n)
	{
		// fscanf(fp, "%d", &tmp);
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

// -----------------------------------------------------------------------------
int read_ground_truth(				// read ground truth results from disk
	int qn,								// number of query objects
	const char *fname,					// address of truth set
	Result **R)							// ground truth results (return)
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

// -----------------------------------------------------------------------------
float calc_inner_product(			// calc inner product
	int   dim,							// dimension
	const float *p1,					// 1st point
	const float *p2)					// 2nd point
{
	float ret = 0.0f;
	for (int i = 0; i < dim; ++i) {
		ret += (p1[i] * p2[i]);
	}
	return ret;
}

// -----------------------------------------------------------------------------
float calc_l2_sqr(					// calc L2 square distance
	int   dim,							// dimension
	const float *p1,					// 1st point
	const float *p2)					// 2nd point
{
	float diff = 0.0f;
	float ret  = 0.0f;
	for (int i = 0; i < dim; ++i) {
		diff = p1[i] - p2[i];
		ret += diff * diff;
	}
	return ret;
}

// -----------------------------------------------------------------------------
float calc_l2_dist(					// calc L2 distance
	int   dim,							// dimension
	const float *p1,					// 1st point
	const float *p2)					// 2nd point
{
	return sqrt(calc_l2_sqr(dim, p1, p2));
}

// -----------------------------------------------------------------------------
float calc_l1_dist(					// calc L1 distance
	int   dim,							// dimension
	const float *p1,					// 1st point
	const float *p2)					// 2nd point
{
	float ret = 0.0f;
	for (int i = 0; i < dim; ++i) {
		ret += fabs(p1[i] - p2[i]);
	}
	return ret;
}

// -----------------------------------------------------------------------------
float calc_recall(					// calc recall (percentage)
	int   k,							// top-k value
	const Result *R,					// ground truth results 
	MaxK_List *list)					// results returned by algorithms
{
	int i = k - 1;
	int last = k - 1;
	while (i >= 0 && R[last].key_ - list->ith_key(i) > FLOATZERO) {
		i--;
	}
	// printf("top-k: %d, index:%d, ground_truth: %f, ret: %f", k, i, R[last].key_, list->ith_key(i));
	return (i + 1) * 100.0f / k;
}

// -----------------------------------------------------------------------------
float calc_DCG(						// compute Discounted Cumulative Gain
		vector<double> relevence)
{
	double dcg = 0.0f;
	for(int i=0; i<relevence.size(); i++)
	{
		int rankIndex = i + 1;
		dcg += relevence.at(i)/(1.0f * log2(rankIndex + 1));
	}
	return dcg;

	/*double dcg = 0;
	for(int i=0; i<relevence.size(); i++)
	{
		int rankIndex = i + 1;
		dcg += (pow(2, relevence.at(i)) - 1 )/log2(rankIndex + 1);
	}
	return dcg;*/
}


// -----------------------------------------------------------------------------
float calc_NDCG(						// compute Normalized Discounted Cumulative Gain
	int   k,							// top-k value
	const Result *R,					// ground truth results
	MaxK_List *list)					// results returned by algorithms
{
	vector<double> ground_truth_list;
	vector<double> returned_list;
	for(int i = 0; i < k; i++)
	{
		ground_truth_list.push_back(R[i].key_);
		returned_list.push_back(list->ith_key(i) > 0 ? list->ith_key(i) : 0);
	}

	double ideal_dcg = calc_DCG(ground_truth_list);
	double dcg = calc_DCG(returned_list);

	return dcg/ideal_dcg;
}

// -----------------------------------------------------------------------------
int get_hits(						// get the number of hits between two ID list
	int   k,							// top-k value
	int   t,							// top-t value
	const Result *R,					// ground truth results 
	MaxK_List *list)					// results returned by algorithms
{
	int i = k - 1;
	int last = t - 1;
	while (i >= 0 && R[last].key_ - list->ith_key(i) > FLOATZERO)
	{
		i--;
	}
	return min(t, i + 1);
}

// -----------------------------------------------------------------------------
float calc_norm(						// calc L2 norm of a given point
	int   dim,						// dimension
	const float *p)
{
	float norm = 0.0f;
	float diff = 0.0f;
	for(int i = 0; i < dim; i++)
	{
		diff = p[i] - 0;
		norm += diff * diff;
	}
	return sqrt(norm);
}

// -----------------------------------------------------------------------------
float calc_angle(					// calc angle of two points p1 and p2
	int   dim,						// dimension
	const float *p1,					// 1st point
	const float *p2)					// 2nd point
{
	float inner_sim = calc_inner_product(dim, p1, p2);
	float p1_norm = calc_norm(dim, p1);
	float p2_norm = calc_norm(dim, p2);
	float cos_angle = acos(inner_sim/(p1_norm * p2_norm)) * 180 / PI;
	return cos_angle;
}

float calc_inner_product_scaled(			// calc inner product
	int   dim,							// dimension
	const float *data,					// 1st point
	const float *query,					// 2nd point
	const float M)						// largest norm to be scaled with
{
	float temp_norm = sqrt(calc_inner_product(dim, data, query));
	float scale = temp_norm / M;
	float ret = 0.0f;
	for (int i = 0; i < dim; ++i) {
		ret += (data[i] * query[i] * scale);
	}
	return ret;
}

