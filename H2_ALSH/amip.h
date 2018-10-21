#ifndef __AMIP_H
#define __AMIP_H

// -----------------------------------------------------------------------------
//  interface of this package
// -----------------------------------------------------------------------------
int ground_truth(					// find the ground truth results
	int   n,							// number of data points
	int   qn,							// number of query points
	int   d,							// dimension of space
	const float **data,					// data set
	const float **query,				// query set
	const char  *truth_set);			// address of truth set

// -----------------------------------------------------------------------------
int h2_alsh(						// c-AMIP search via h2_alsh
	int   n,							// number of data points
	int   qn,							// number of query points
	int   d,							// dimension of space
	float nn_ratio,						// approximation ratio for ANN search
	float mip_ratio,					// approximation ratio for AMIP search
	const float **data,					// data set
	const float **query,				// query set
	const char  *truth_set,				// address of truth set
	const char  *output_folder);		// output folder

// -----------------------------------------------------------------------------
int l2_alsh(						// c-AMIP search via l2_alsh
	int   n,							// number of data points
	int   qn,							// number of query points
	int   d,							// dimension of space
	int   m,							// param of l2_alsh
	float U,							// param of l2_alsh
	float nn_ratio,						// approximation ratio for ANN search
	const float **data,					// data set
	const float **query,				// query set
	const char  *truth_set,				// address of truth set
	const char  *output_folder);		// output folder

// -----------------------------------------------------------------------------
int l2_alsh2(						// c-AMIP search via l2_alsh2
	int   n,							// number of data points
	int   qn,							// number of query points
	int   d,							// dimension of space
	int   m,							// param of l2_alsh2
	float U,							// param of l2_alsh2
	float nn_ratio,						// approximation ratio for ANN search
	const float **data,					// data set
	const float **query,				// query set
	const char  *truth_set,				// address of truth set
	const char  *output_folder);		// output folder

// -----------------------------------------------------------------------------
int xbox(							// c-AMIP search via xbox
	int   n,							// number of data points
	int   qn,							// number of query points
	int   d,							// dimension of space
	float nn_ratio,						// approximation ratio for ANN search
	const float **data,					// data set
	const float **query,				// query set
	const char  *truth_set,				// address of truth set
	const char  *output_folder);		// output folder

// -----------------------------------------------------------------------------
int sign_alsh(						// c-AMIP search via sign_alsh
	int   n,							// number of data points
	int   qn,							// number of query points
	int   d,							// dimension of space
	int   K,							// number of hash tables
	int   m,							// param of sign_alsh
	float U,							// param of sign_alsh
	float nn_ratio,						// approximation ratio for ANN search
	const float **data,					// data set
	const float **query,				// query set
	const char  *truth_set,				// address of truth set
	const char  *output_folder);		// output folder

// -----------------------------------------------------------------------------
int simple_lsh(						// c-AMIP search via simple_lsh
	int   n,							// number of data points
	int   qn,							// number of query points
	int   d,							// dimension of space
	int   K,							// number of hash tables
	int   L,							// number of hash layers
	float S,							// similarity threshold
	float nn_ratio,						// approximation ratio for ANN search
	const float **data,					// data set
	const float **query,				// query set
	const char  *truth_set,				// address of truth set
	const char  *output_folder);		// output folder

// -----------------------------------------------------------------------------
int linear_scan(					// find top-k mip using linear_scan
	int   n,							// number of data points
	int   qn,							// number of query points
	int   d,							// dimension of space
	const float **data,					// data set
	const float **query,				// query set
	const char  *truth_set,				// address of truth set
	const char  *output_folder);		// output folder

// -----------------------------------------------------------------------------
int h2_alsh_precision_recall(		// precision recall curve of h2_alsh
	int   n,							// number of data points
	int   qn,							// number of query points
	int   d,							// dimension of space
	float nn_ratio,						// approximation ratio for ANN search
	float mip_ratio,					// approximation ratio for AMIP search
	const float **data,					// data set
	const float **query,				// query set
	const char  *truth_set,				// address of truth set
	const char  *output_folder);		// output folder

// -----------------------------------------------------------------------------
int sign_alsh_precision_recall(		// precision recall curve of sign_alsh
	int   n,							// number of data points
	int   qn,							// number of query points
	int   d,							// dimension of space
	int   K,							// number of hash tables
	int   m,							// param of sign_alsh
	float U,							// param of sign_alsh
	float nn_ratio,						// approximation ratio for ANN search
	const float **data,					// data set
	const float **query,				// query set
	const char  *truth_set,				// address of truth set
	const char  *output_folder);		// output folder

// -----------------------------------------------------------------------------
int simple_lsh_precision_recall(	// precision recall curve of simple_lsh
	int   n,							// number of data points
	int   qn,							// number of query points
	int   d,							// dimension of space
	int   K,							// number of hash tables
	int   L,							// number of hash layers
	float S,							// similarity threshold
	float nn_ratio,						// approximation ratio for ANN search
	const float **data,					// data set
	const float **query,				// query set
	const char  *truth_set,				// address of truth set
	const char  *temp_result,			// address to store temporary output from different onion layers
	const char  *output_folder);		// output folder

/*
// -----------------------------------------------------------------------------
int simple_lsh_recall(	// precision recall curve of simple_lsh
	int   n,							// number of data points
	int   qn,							// number of query points
	int   d,							// dimension of space
	int   K,							// number of hash tables
	int   L,							// number of hash layers
	int   layer_index, 				// current onion layer index
	float S,							// similarity threshold
	float nn_ratio,						// approximation ratio for ANN search
	const float **data,					// data set
	const float **query,				// query set
	const char  *truth_set,				// address of truth set
	const char  *temp_result,			// address to store temporary output from different onion layers
	const char  *output_folder);		// output folder
*/

// -----------------------------------------------------------------------------
int simple_lsh_recall(	// precision recall curve of simple_lsh
	int   n,							// number of data points
	int   qn,							// number of query points
	int   d,							// dimension of space
	int   K,							// number of hash tables
	int   L,							// number of hash layers
	int   layer_index, 				// current onion layer index
	float S,							// similarity threshold
	float nn_ratio,						// approximation ratio for ANN search
	const float **data,					// data set
	const float **query,				// query set
	const char  *truth_set,				// address of truth set
	const char  *temp_result,			// address to store temporary output from different onion layers
	const char  *sim_angle,			// address to store sim-angle from different layers
	const char  *output_folder);		// output folder

// -----------------------------------------------------------------------------
int norm_distribution(				// analyse norm distribution of data
	int   n,							// number of data points
	int   d,							// dimension of space
	const float **data,					// data set
	const char  *output_folder);		// output folder

// -----------------------------------------------------------------------------
int persist_intermediate_on_file(		// persist intermediate result per query per onion layer on file, for aggregation
	int   topk, 						// topk results of interest
	int   d,							// dimension of space
	MaxK_List* list,					// list that contains the topk result per query per onion layer
	const float **data,					// data set
	const char  *output_folder);		// output folder

// -----------------------------------------------------------------------------
int persist_candidate_size(				// persist average number of candidate on file, regarding to a specific topk
		unordered_map<int, float> mymap, 	// average value of candidate size
		const char  *output_folder,			// output folder
		unordered_map<int, float> my_run_time);			// run time of different top-k

// -----------------------------------------------------------------------------
int overall_performance(				// output the overall performance of indexing
	int   d,							// dimension of space
	int   qn, 							// number of queries
	int   layers,						// number of onion layers
	const char  *temp_output_folder,	// temporal output folder
	const char  *ground_truth_folder,	// ground truth folder
	const char  *output_folder);		// output folder

int my_sort_col(const void *a, const void *b);

#endif // __AMIP_H
