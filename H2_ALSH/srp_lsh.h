#ifndef __SRP_LSH_H
#define __SRP_LSH_H
#include"headers.h"

// -----------------------------------------------------------------------------
//  Sign-Random Projection LSH (SRP_LSH) is used to solve the problem of 
//  c-Approximate Maximum Cosine (c-AMC) search
// 
//  the idea was introduced by Moses S Charikar in his paper "Similarity 
//  estimation techniques from rounding algorithms", In Proceedings of the 
//  thiry-fourth annual ACM symposium on Theory of computing (STOC), pages 
//  380–388, 2002.
// -----------------------------------------------------------------------------
class SRP_LSH {
public:
	SRP_LSH(
		int n,							// cardinality of dataset
		int d,							// dimensionality of dataset
		int K,							// number of hash tables
		int L,							// number of hash layers
		float S,							// similarity threshold
		const float **data,				// data objects
		bool post_opt,
		const char  *temp_hash);

	// -------------------------------------------------------------------------
	~SRP_LSH();							// destructor

	// -------------------------------------------------------------------------
	int kmc(								// c-k-AMC search
			int   top_k,					// top-k value
			const float *query,			// input query
			MaxK_List *list,				// top-k MC results  (return)
			const float *real_query);
	// -------------------------------------------------------------------------
	unordered_set<int> mykmc(			// c-k-AMC search
			int   top_k,					// top-k value
			const float *query,			// input query
			MaxK_List *list,				// top-k MC results  (return)
			const float *real_query,
			float& sim_threshold,
			bool is_threshold,
			int& hash_table_hit);

	// -------------------------------------------------------------------------
	unordered_set<int> mykmc_test(			// c-k-AMC search
			int   top_k,					// top-k value
			const float *query,			// input query
			MaxK_List *list,				// top-k MC results  (return)
			const float *real_query,
			float& sim_threshold,
			bool is_threshold,
			int& hash_table_hit);

	// -------------------------------------------------------------------------
	int get_candidates(string str_key, MaxK_List *list, unordered_set<int>& candidates,  const float *query,
			const float *real_query, float threshold_S, bool is_threshold, float& angle_threshold, int top_k, int hash_layer, int& hash_table_hit);

	// -------------------------------------------------------------------------
	int hammingDist(string str1, string str2, int length);

	// -------------------------------------------------------------------------
	void persistHashTable(const char *fname);		// persist HashTables on file
	void loadHashTable(const char *fname);			// persist HashTables on file
	float* compute_vector_mean(float** data, vector<int> data_ids);
	float get_indexing_time();

protected:
	int   n_pts_;					// cardinality of dataset
	int   dim_;						// dimensionality of dataset
	int   K_;						// number of hash tables
	int   L_;						// number of hash layers
	float S_;						// similarity threshold
	const float **data_;				// data objects

	bool  ***hash_code_;				// hash code of data objects
	float ***proj_;					// random projection vectors
	unordered_map<string, vector<int>>* maps_;
	unordered_map<string, vector<float>>* maps_interval_;

	// -------------------------------------------------------------------------
	void gen_random_vectors();		// generate random projection vectors

	// -------------------------------------------------------------------------
	void persist_random_vectors(const char *fname);		// generate random projection vectors

	// -------------------------------------------------------------------------
	void load_random_vectors(const char *fname, int input_L);		// generate random projection vectors

	// -------------------------------------------------------------------------
	void bulkload();					// bulkloading

	// -------------------------------------------------------------------------
	void get_proj_vector(			// get vector after random projection
		const float *data,			// input data
		bool *hash_code,				// hash code of input data (return)
		int layer);					// layer index of interest

	// -------------------------------------------------------------------------
	unordered_map<string, vector<int>> buildMap(bool **hashcode);
	void post_process_map();		// compute similarity interval for data elements in each hash buckets
	vector<float> compute_vector_mean(vector<int> data_ids);
	float compute_mean_sim(vector<float> query, vector<int> data_ids);
	float compute_max_angle(vector<float> query, vector<int> data_ids);
	float indexing_time_;
};

#endif // __SRP_LSH_H
