#include "headers.h"

// -----------------------------------------------------------------------------
SRP_LSH::SRP_LSH(					// constructor
	int n,								// cardinality of dataset
	int d,								// dimensionality of dataset
	int K,								// number of hash tables
	int L,								// number of hash layers
	float S,							// similarity threshold
	const float **data)					// data objects
{
	// -------------------------------------------------------------------------
	//  init parameters
	// -------------------------------------------------------------------------
	n_pts_ = n;
	dim_   = d;
	K_     = K;
	L_     = L;
	S_	   = S;
	data_  = data;

	// -------------------------------------------------------------------------
	//  build hash tables (bulkloading)
	// -------------------------------------------------------------------------
	gen_random_vectors();
	bulkload();
}

// -----------------------------------------------------------------------------
SRP_LSH::~SRP_LSH()					// destructor
{
	for(int l=0; l< L_; l++)
	{
		if (proj_[l] != NULL) {
			for (int i = 0; i < K_; ++i)
			{
				delete[] proj_[l][i];
				proj_[l][i] = NULL;
			}
			delete[] proj_[l];
			proj_[l] = NULL;
		}

		if (hash_code_[l] != NULL)
		{
			for (int i = 0; i < n_pts_; ++i)
			{
				delete[] hash_code_[l][i];
				hash_code_[l][i] = NULL;
			}
			delete[] hash_code_[l];
			hash_code_[l] = NULL;
		}
	}

}

// -----------------------------------------------------------------------------
void SRP_LSH::gen_random_vectors()	// generate random projection vectors
{
	proj_ = new float**[L_];
	for(int l=0; l < L_; l++)
	{
		proj_[l] = new float*[K_];
		for (int i = 0; i < K_; ++i)
		{
			proj_[l][i] = new float[dim_];
			for (int j = 0; j < dim_; ++j)
			{
				proj_[l][i][j] = gaussian(0.0f, 1.0f);
			}
		}
	}

}

// -----------------------------------------------------------------------------
void SRP_LSH::bulkload()			// bulkloading
{
	hash_code_ = new bool**[L_];
	for(int l=0; l< L_; l++)
	{
		hash_code_[l] = new bool*[n_pts_];
		for (int i = 0; i < n_pts_; ++i)
		{
			hash_code_[l][i] = new bool[K_];
			get_proj_vector(data_[i], hash_code_[l][i], l);
		}
	}

}

// -----------------------------------------------------------------------------
void SRP_LSH::get_proj_vector(		// get vector after random projection
	const float *data,					// input data 
	bool *hash_code,				// hash code of input data (return)
	int layer)						// layer index of interest
{
	for (int i = 0; i < K_; ++i)
	{
		float sum = calc_inner_product(dim_, proj_[layer][i], data);

		if (sum >= 0) hash_code[i] = true;
		else hash_code[i] = false;
	}
}

// -----------------------------------------------------------------------------
int SRP_LSH::kmc(					// c-k-AMC search
	int   top_k,						// top-k value
	const float *query,					// input query
	MaxK_List *list,					// top-k MC results (return)
	const float *real_query
	)
{
	bool **mc_query = new bool*[L_];
	for(int l = 0; l < L_; l++)
	{
		mc_query[l] = new bool[K_];
		get_proj_vector(query, mc_query[l], l);
	}

	/* Modified by Sicong*/
	// for each point, pick the best matched case and insert into candidate list
	// candidate list:
	// 		key: matched value -- Hamming Similarity of Hash Code
	// 		value: data object ID
	for (int i = 0; i < n_pts_; ++i)
	{
		int best_match = 0;
		int matched_dim = 0;
		for(int l = 0; l < L_; l++)
		{
			int current_match = 0;
			for (int j = 0; j < K_; ++j)
			{
				if (hash_code_[l][i][j] == mc_query[l][j])
				{
					++current_match;
				}
			}
			if(current_match > best_match)
				best_match = current_match;
		}
		// enforce matching similarity associated with optimization function
		if(calc_inner_product(dim_, data_[i], real_query) >=S_)
		{
			list->insert(best_match, i);
		}
	}

	// -------------------------------------------------------------------------
	//  release space
	// -------------------------------------------------------------------------
	delete[] mc_query;
	mc_query = NULL;

	return 0;
}


// -----------------------------------------------------------------------------
void SRP_LSH::persistHashTable(const char *fname)			// persist HashTables on file
{
	FILE *fp = fopen(fname, "w");
	if (!fp)
	{
		printf("Could not create %s\n", fname);
		return;
	}
	for(int l=0; l< L_; l++)
	{
		for(int k = 0; k < K_; k++)
		{
			for(int p=0; p < n_pts_; p++)
			{
				fprintf(fp, "%d", hash_code_[l][k][p]);
			}
			fprintf(fp, "\t");
		}
		fprintf(fp, "\n");
	}
}

// -----------------------------------------------------------------------------
void SRP_LSH::loadHashTable(const char *fname)			// load HashTables on file
{
	FILE *fp = fopen(fname, "r");
	if (!fp)
	{
		printf("Could not create %s\n", fname);
		return;
	}
	for(int l=0; l< L_; l++)
	{
		for(int k = 0; k < K_; k++)
		{
			for(int p=0; p < n_pts_; p++)
			{
				// fprintf(fp, "%d", hash_code_[l][k][p]);
				// load using fscanf
			}
			fscanf(fp, "\t");
		}
		fscanf(fp, "\n");
	}
}


