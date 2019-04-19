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
int simple_lsh_recall(    // precision recall curve of simple_lsh
		int   n,                            // number of data points
		int   qn,                            // number of query points
		int   d,                            // dimension of space
		int   K,                            // number of hash functions
		int   L,                            // number of hash tables
		int       layer_index,                 // the index of current onion layer
		int   top_k, 						// top 25 or top 50?
		int   sample_index,
		float  S,                            // number of hash tables
		float nn_ratio,                        // approximation ratio for nn search
		const float **data,                    // data set
		const float **query,                // query set
		const char  *truth_set,                // address of truth set
		const char  *temp_result,            // address to store temporary output from different onion layers
		const char  *sim_angle,            // address to store sim-angle from different layers
		const char  *output_folder,
		const char  *temp_hash,
		const char  *data_index_set,
		bool post_opt);         // output folder
// -----------------------------------------------------------------------------
int norm_distribution(				// analyse norm distribution of data
	int   n,							// number of data points
	int   d,							// dimension of space
	const float **data,					// data set
	const char  *output_folder);		// output folder

// -----------------------------------------------------------------------------
int persist_intermediate_on_file(        		// persist intermediate result per query per onion layer on file, for aggregation
		int   topk,                         	// topk results of interest
		int   d,                            	// dimension of space
		MaxK_List* list,                    	// list that contains the topk result per query per onion layer
		const float **data,                    	// original data set
		const float *query,						// original query
		const char  *output_folder,
		const char *data_index_set);            	// output folder

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
	int   sample_index,
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




int my_sort_col(const void *a, const void *b);
int persist_sample_results(int max_top_k, MaxK_List* list, FILE *fp);
// int combine_sample_result(int sample_space, int optimized_topk, int qn, const char  *temp_result, const char *ground_truth_folder, const char *output_folder, const char  *temp_result_str);
int combine_sample_result(int d, int qn, int layers, int optimized_topk, int sample_space, const char  *temp_result, const char *ground_truth_folder, const char *output_folder, const char  *temp_result_str);


int read_sample_index_from_sample(
	const char *fname,
	vector<int> &sample_data_index);
// -----------------------------------------------------------------------------
int read_ground_truth_from_sample(						// read ground truth results from disk
	int qn, 											// # of result-sets (one per query)
	int top_k,											// number of query objects
	const char *fname,									// address of truth set
	unordered_map<int, float>* map_array);

#endif // __AMIP_H
