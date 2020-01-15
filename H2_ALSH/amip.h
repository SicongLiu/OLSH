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
	int 	  layer_index,
	int   top_k,
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
	int   qn,						// number of query points
	int   d,							// dimension of space
	int   K,							// number of hash tables
	int   L,							// number of hash layers
	int   layer_index, 				// current onion layer index
	int 	  top_k,						// number of elements want to retrieve
	float S,							// similarity threshold
	float nn_ratio,					// approximation ratio for ANN search
	const float **data,				// data set
	const float **query,				// query set
	const char  *truth_set,			// address of truth set
	const char  *temp_result,		// address to store temporary output from different onion layers
	const char  *sim_angle,			// address to store sim-angle from different layers
	const char  *output_folder,		// output folder
	const char  *temp_hash,
	bool post_opt);

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
	const float **data,					// original data set
	const float *query,					// original query
	const char  *output_folder);		// output folder

// -----------------------------------------------------------------------------
int persist_candidate_size(								// persist average number of candidate on file, regarding to a specific topk
		unordered_map<int, float> candidate_map,     	// average value of candidate size
		unordered_map<int, float> hash_table_hit_map,	// average hash table hit counts
		const char  *output_folder,						// output folder
		unordered_map<int, float> my_run_time);			// run time of different top-k

// -----------------------------------------------------------------------------
int overall_performance(				// output the overall performance of indexing
	int   d,							// dimension of space
	int   qn, 							// number of queries
	int   layers,						// number of onion layers
	int   top_k, 						// number of elements to retrieve
	const char  *temp_output_folder,	// temporal output folder
	const char  *ground_truth_folder,	// ground truth folder
	const char  *output_folder);		// output folder


// -----------------------------------------------------------------------------
// NOTE: TA_algorithm, the way we organize the column and row structure index
// -----------------------------------------------------------------------------
set<int> comp_current_seen(vector<vector<int>> sorted_sim_index, int dim, int round);

// -----------------------------------------------------------------------------
// NOTE: TA_algorithm, the way we organize the column and row structure index
// -----------------------------------------------------------------------------
float vector_sum(
		vector<vector<float>> sim_matrix,
		int dim,
		int round);

// -----------------------------------------------------------------------------
// NOTE: TA_algorithm, the way we organize the column and row structure index
// -----------------------------------------------------------------------------
int sorted_indexes(
		int   dim_index,                          	// dimension index of sim_matrix
		vector<vector<float>> &sim_matrix,			// reference pass sim_matrix in for update purpose
		vector<vector<int>> &sorted_sim_index);  		// sorted index vector structure

// -----------------------------------------------------------------------------
// NOTE: TA_algorithm, the way we organize the column and row structure index
// -----------------------------------------------------------------------------
int compute_TA(                    		  	// find top-k mip using linear_scan
		int   d,                            	// number of space
		int   n,                            	// dimension of data points
		int 	  top_k,
		MaxK_List* seen_sim,
		const float **data,                	// data set
		const float *query);         			// output folder

set<int> comp_current_seen_list(vector<vector<int>> sorted_prod_idx, vector<vector<float>> sorted_prod, int dim, int round, float& current_best);

int compute_TA_list(                    		  	// find top-k mip using linear_scan
		int   d,                            	// number of space
		int   n,                            	// dimension of data points
		int 	  top_k,
		MaxK_List* ret,
		const float **data,                	// data set
		const float *query);

int compute_TA_list_set_k(                    		  	// find top-k mip using linear_scan
		int   d,                            	// number of space
		int   n,                            	// dimension of data points
		int 	  top_k,
		MaxK_List* ret,
		const float **data,                	// data set
		const float *query,
		int& total_run,
		int& total_data_access);

// -----------------------------------------------------------------------------
// NOTE: TA_algorithm, the way we organize the column and row structure index
// -----------------------------------------------------------------------------
int TA_Topk(                    		  		// find top-k mip using linear_scan
		int   n,                            	// number of data points
		int   qn,                           	// number of query points
		int   d,                            	// dimension of space
		int   layer_index,
		int   top_k,
		const float **data,                	// data set
		const float **query,                	// query set
		const char  *truth_set,             	// address of truth set
		const char  *output_folder);         	// output folder

// -----------------------------------------------------------------------------
int TA_TopK_all(					// find top-k mip using linear_scan
	int   n,							// number of data points
	int   qn,							// number of query points
	int   d,							// dimension of space
	const float **data,					// data set
	const float **query,				// query set
	const char  *truth_set,				// address of truth set
	const char  *output_folder); 		// output folder

// -----------------------------------------------------------------------------
int linear_scan_layer(    // precision recall curve of linear scan across different onion layer
		int   n,                            // number of data points
		int   qn,                            // number of query points
		int   d,                            // dimension of space
		int       layer_index,                 // the index of current onion layer
		int   top_k, 						// top 25 or top 50?
		const float **data,                    // data set
		const float **query,                // query set
		const char  *truth_set,                // address of truth set
		const char  *temp_result,            // address to store temporary output from different onion layers
		const char  *output_folder);

// -----------------------------------------------------------------------------
int linear_scan_all(					// find top-k mip using linear_scan
	int   n,							// number of data points
	int   qn,							// number of query points
	int   d,							// dimension of space
	const float **data,					// data set
	const float **query,				// query set
	const char  *truth_set,				// address of truth set
	const char  *output_folder); 		// output folder

int my_sort_col(const void *a, const void *b);

#endif // __AMIP_H
