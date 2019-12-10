#ifndef __SIMPLE_LSH_H
#define __SIMPLE_LSH_H

class SRP_LSH;

// -----------------------------------------------------------------------------
//  Simple-LSH is used to solve the problem of c-Approximate Maximum Inner 
//  Product (c-AMIP) search.
//
//  the idea was introduced by Behnam Neyshabur and Nathan Srebro in their 
//  paper "On Symmetric and Asymmetric LSHs for Inner Product Search", In 
//  Proceedings of the 32nd International Conference on International Conference 
//  on Machine Learning (ICML), pages 1926–1934, 2015.
// -----------------------------------------------------------------------------
class Simple_LSH {
public:
	Simple_LSH();					// defaut constructor
	~Simple_LSH();					// destructor

	// -------------------------------------------------------------------------
	void build(						// build index
			int   n,						// number of data
			int   d,						// dimension of data
			int   K,						// number of hash tables
			int   L,						// number of hash layers
			float S,						// similarity threshold
			float ratio,					// approximation ratio
			const float** data,			// data objects
			bool post_opt,
			const char  *temp_hash);

	// -------------------------------------------------------------------------
	int kmip(						// c-k-AMIP search
			int   top_k,					// top-k value
			const float* query,			// input query
			MaxK_List* list,				// top-k mip results
			float& sim_threshold,
			bool is_threshold,
			int& hash_hits);

	// ------------ when n < top_k, all data available will be candidates ------
	int kmip_special(						// c-k-AMIP search
			int& n, 						// # of data
			int d, 						// dimension of data
			const float** data,
			int   top_k,					// top-k value
			const float* query,			// input query
			MaxK_List* list,				// top-k mip results
			float& sim_threshold,
			bool is_threshold,
			int& hash_hits);


	// ------------ when hash layer L = 0 ------
	int kmip_L0(						// c-k-AMIP search
			int& n, 						// # of data
			int d, 						// dimension of data
			const float** data,
			int   top_k,					// top-k value
			const float* query,			// input query
			MaxK_List* list,				// top-k mip results
			float& sim_threshold,
			bool is_threshold,
			int& hash_hits);

	// -------------------------------------------------------------------------
	int kmip_test(						// c-k-AMIP search
			int   top_k,					// top-k value
			const float* query,			// input query
			MaxK_List* list,				// top-k mip results
			float& sim_threshold,
			bool is_threshold,
			int& hash_hits);
protected:
	int   n_pts_;					// number of data points
	int   dim_;						// dimension of data
	int   K_;						// number of hash tables
	int   L_;						// number of hash layers
	float S_;						// similarity threshold
	float appr_ratio_;				// approximation ratio for AMC search
	const float **data_;			// data objects
	
	float M_;						// max norm of data objects
	int   simple_lsh_dim_;			// dimension of simple_lsh data
	float **simple_lsh_data_;		// simple_lsh data
	SRP_LSH *lsh_;					// SRP_LSH

	// -------------------------------------------------------------------------
	int bulkload(bool post_opt, const char  *temp_hash);					// bulkloading

	// -------------------------------------------------------------------------
	void display();					// display parameters

	// -------------------------------------------------------------------------
	void persistHashTable(const char *fname);		// persist HashTables on file
	void loadHashTable(const char *fname);		// persist HashTables on file
};

#endif // __SIMPLE_LSH_H
