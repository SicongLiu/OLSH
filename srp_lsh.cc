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
	maps_ = new unordered_map<string, vector<int> >[L_];
	maps_interval_ = new unordered_map<string, vector<float>>[L_];
	// -------------------------------------------------------------------------
	//  build hash tables (bulkloading)
	// -------------------------------------------------------------------------
	gen_random_vectors();
	bulkload();
	post_process_map();
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
		// To-Do:
		// need to clear up the maps
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
		// for each layer build map here
		maps_[l] = buildMap(hash_code_[l]);
	}

	// free hashcode space
	/*if (hash_code_[l] != NULL)
	{
		for (int i = 0; i < n_pts_; ++i)
		{
			delete[] hash_code_[l][i];
			hash_code_[l][i] = NULL;
		}
		delete[] hash_code_[l];
		hash_code_[l] = NULL;
	}*/
}

// -----------------------------------------------------------------------------
unordered_map<string, vector<int>> SRP_LSH::buildMap(bool **hashcode)			// build hash map
{
	unordered_map<string, vector<int> > map;
	for(int i=0; i < n_pts_; i++)
	{
		char c[K_];
		for(int j = 0; j < K_; j++)
		{
			c[j] = hashcode[i][j] == true ? '1' : '0';
		}
		string str(c);
		str = str.substr(0, K_);
		if(map.find(str) != map.end())
		{
			map[str].push_back(i);
		}
		else
		{
			vector<int> data_index;
			data_index.push_back(i);
			pair<string, vector<int> > dict(str, data_index);
			map.insert(dict);
		}
		memset(c, 0, K_);
	}
	return map;
}

// -----------------------------------------------------------------------------
vector<float> SRP_LSH::compute_vector_mean(vector<int> data_ids)
{
	// float* vector_mean = new float[dim_];
	vector<float> vector_mean;
	for(int i = 0; i < dim_; i++)
	{
		float cur_dim = 0.0f;
		for(int j = 0; j < data_ids.size(); j++)
		{
			cur_dim += data_[data_ids[j]][i];
		}
		cur_dim = cur_dim / data_ids.size();
		// vector_mean[i] = cur_dim;
		vector_mean.push_back(cur_dim);
	}
	return vector_mean;
}

// -----------------------------------------------------------------------------
float SRP_LSH::compute_mean_sim(vector<float> query, vector<int> data_ids)
{
	float min_sim = MAXREAL;
	for(int i = 0; i < data_ids.size(); i++)
	{
		float temp = calc_inner_product(dim_, &query[0], data_[i]);
		if(temp < min_sim)
		{
			min_sim = temp;
		}
	}
	return min_sim;
}

// -----------------------------------------------------------------------------
float SRP_LSH::compute_max_angle(vector<float> query, vector<int> data_ids)
{
	float max_angle = 0.0f;
	for(int i = 0; i < data_ids.size(); i++)
	{
		float cos_angle = calc_angle(dim_, &query[0], data_[i]);
		if(cos_angle > max_angle)
		{
			max_angle = cos_angle; // max angle -> min cos-sim
		}
	}
	return max_angle;
}

// -----------------------------------------------------------------------------
void SRP_LSH::post_process_map()			// compute similarity interval for data elements in each hash buckets
{
	// for each layer
	for(int l = 0; l < L_; l++)
	{
		unordered_map<string, vector<float> > cur_angle_map;
		unordered_map<string, vector<int> > cur_map = maps_[l];

		// for each hash bucket at each layer
		for (auto const& it : cur_map)
		{
			vector<int> data_ids = it.second;
			vector<float> mean_data_vector = compute_vector_mean(data_ids);
			float max_angle = compute_max_angle(mean_data_vector, data_ids);

			vector<float>::iterator iterator;
			iterator = mean_data_vector.begin();
			mean_data_vector.insert(iterator , max_angle);
			pair<string, vector<float> > dict(it.first, mean_data_vector);
			cur_angle_map.insert(dict);
		}
		maps_interval_[l] = cur_angle_map;
	}
}

// -----------------------------------------------------------------------------
void SRP_LSH::get_proj_vector(		// get vector after random projection
	const float *data,				// input data
	bool *hash_code,					// hash code of input data (return)
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
unordered_set<int> SRP_LSH::mykmc(	// c-k-AMC search
	int   top_k,						// top-k value
	const float *query,				// input query
	MaxK_List *list,					// top-k MC results (return)
	const float *real_query,
	float& angle_threshold,
	bool is_threshold,				// sim_threshold from previous layers
	int& hash_table_hit)
{
	bool **mc_query = new bool*[L_];
	for(int l = 0; l < L_; l++)
	{
		mc_query[l] = new bool[K_];
		get_proj_vector(query, mc_query[l], l);
	}

	// build hash code for mc_query
	unordered_set<int> candidates;

	for(int i = 0; i < L_; i++)
	{
		char c[K_];
		for(int j = 0; j < K_; j++)
		{
			c[j] = mc_query[i][j] ? '1' : '0';
		}
		string str(c);
		str = str.substr(0, K_);

		// search through map to find collision hashcode and retrieve candidates
		if(maps_[i].find(str) != maps_[i].end())
		{
			++hash_table_hit;
			vector<int> temp_map = maps_[i][str];
			if(is_threshold)
			{
				// condition: angle_q_mean <= angle_q_topk + angle_i
				vector<float> cur_angle_vec = maps_interval_[i][str];
				float angle_i = cur_angle_vec[0];
				float angle_q_mean = calc_angle(dim_, real_query, &cur_angle_vec[1]);
				if(angle_threshold + angle_i >= angle_q_mean)
				{
					copy(temp_map.begin(), temp_map.end(),inserter(candidates, candidates.end()));
				}
				else
				{
					// printf("gain size: %lu .\n", temp_map.size());
				}
			}
			else
			{
				copy(temp_map.begin(), temp_map.end(),inserter(candidates, candidates.end()));
			}
		}
		memset(c, 0, K_);
	}
	// -------------------------------------------------------------------------
	//  release space
	// -------------------------------------------------------------------------
	delete[] mc_query;
	mc_query = NULL;

	return candidates;
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

	// Modified by Sicong
	// for each point, pick the best matched case and insert into candidate list
	// candidate list:
	// 		key: matched value -- Hamming Similarity of Hash Code
	// 		value: data object ID
	for (int i = 0; i < n_pts_; ++i)
	{
		int collisions = 0;
		for(int l = 0; l < L_; l++)
		{
			for (int j = 0; j < K_; ++j)
			{
				if (hash_code_[l][i][j] == mc_query[l][j])
				{
					++collisions;
				}
			}
		}
		// enforce matching similarity associated with optimization function
		if(calc_inner_product(dim_, data_[i], real_query) >=S_)
		{
			list->insert(collisions, i);
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


