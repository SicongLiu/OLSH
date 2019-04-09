#include "headers.h"

int MAX_DIMENSION = 0;

// -----------------------------------------------------------------------------
int ground_truth(                    // find the ground truth results
		int   n,                            // number of data points
		int   qn,                            // number of query points
		int   d,                            // dimension of space
		const float **data,                    // data set
		const float **query,                // query set
		const char  *truth_set)                // address of truth set
{
	timeval start_time, end_time;

	// -------------------------------------------------------------------------
	//  find ground truth results (using linear scan method)
	// -------------------------------------------------------------------------
	gettimeofday(&start_time, NULL);
	FILE *fp = fopen(truth_set, "w");
	if (!fp)
	{
		printf("Could not create %s.\n", truth_set);
		return 1;
	}

	MaxK_List *list = new MaxK_List(MAXK);
	fprintf(fp, "%d %d\n", qn, MAXK);
	for (int i = 0; i < qn; ++i)
	{
		list->reset();
		for (int j = 0; j < n; ++j)
		{
			float ip = calc_inner_product(d, data[j], query[i]);
			list->insert(ip, j + 1);
		}

		for (int j = 0; j < MAXK; ++j)
		{
			fprintf(fp, "%d %f ", list->ith_id(j), list->ith_key(j));
		}
		fprintf(fp, "\n");
	}
	fclose(fp);

	gettimeofday(&end_time, NULL);
	float truth_time = end_time.tv_sec - start_time.tv_sec +
			(end_time.tv_usec - start_time.tv_usec) / 1000000.0f;
	printf("Ground Truth: %f Seconds\n\n", truth_time);

	// -------------------------------------------------------------------------
	//  release space
	// -------------------------------------------------------------------------
	delete list; list = NULL;

	return 0;
}


// -----------------------------------------------------------------------------
// NOTE: TA_algorithm, the way we organize the column and row structure index
// -----------------------------------------------------------------------------
set<int> comp_current_seen(vector<vector<int>> sorted_sim_index, int dim, int round)
{
	set<int> current_seen;
	for(int i = 0; i < dim; i++)
	{
		current_seen.insert(sorted_sim_index.at(i).at(round));
	}

	return current_seen;
}



// -----------------------------------------------------------------------------
// NOTE: TA_algorithm, the way we organize the column and row structure index
// -----------------------------------------------------------------------------
float vector_sum(
		vector<vector<float>> sim_matrix,
		int dim,
		int round)
{
	float sum = 0;
	for(int i = 0; i < dim; i++)
	{
		sum += sim_matrix.at(i).at(round);
	}
	return sum;
}

// -----------------------------------------------------------------------------
// NOTE: TA_algorithm, the way we organize the column and row structure index
// -----------------------------------------------------------------------------
int sorted_indexes(
		int   dim_index,                          	// dimension index of sim_matrix
		vector<vector<float>> &sim_matrix,			// reference pass sim_matrix in for update purpose
		vector<vector<int>> &sorted_sim_index)  		// sorted index vector structure
{
	vector<float> vec_interest = sim_matrix.at(dim_index);
	vector<int> idx(vec_interest.size());
	iota(idx.begin(), idx.end(), 0);

	sort(idx.begin(), idx.end(), [&vec_interest](int i1, int i2) {return vec_interest[i1] > vec_interest[i2]; });

	vector<float> v1;

	// update sim_matrix[dim_index]
	for(int i = 0; i < idx.size(); i++)
	{
		v1.push_back(vec_interest[idx[i]]);
	}
	sorted_sim_index.push_back(idx);
	sim_matrix[dim_index] = vec_interest;

	vector<float>().swap(vec_interest);
	return 0;
}


// -----------------------------------------------------------------------------
// NOTE: TA_algorithm, the way we organize the column and row structure index
// -----------------------------------------------------------------------------
int compute_TA(                    		  	// find top-k mip using linear_scan
		int   d,                            	// number of space
		int   n,                            	// dimension of data points
		int 	  top_k,
		MaxK_List* seen_sim,
		const float **data,                	// data set
		const float *query)         			// output folder
{
	bool flag = false;
	float current_best = 0;
	int round = 0;

	set<int> TA_seen;

	// compute similarity matrix
	vector<vector<float>> sim_matrix;
	vector<vector<int>> sorted_sim_index;
	for(int i = 0; i < d; i++)
	{
		vector<float> column_sim;
		float query_pt = query[i];
		for(int j = 0; j < n; j++)
		{
			float data_pt = data[j][i];
			float sim_comb = query_pt * data_pt;
			column_sim.push_back(sim_comb);
		}
		sim_matrix.push_back(column_sim);
	}

	// sort sim_matrix, along each dimension
	for(int i = 0; i < d; i++)
	{
		sorted_indexes(i, sim_matrix, sorted_sim_index);
	}

	while(flag == false)
	{
		current_best = vector_sum(sim_matrix, d, round);
		set<int> current_seen = comp_current_seen(sorted_sim_index, d, round);
		set<int> newly_added;

		set_difference(current_seen.begin(), current_seen.end(), TA_seen.begin(), TA_seen.end(), inserter(newly_added, newly_added.end()));
		vector<int> newly_added_vector(newly_added.begin(), newly_added.end());

		for(vector<int>::iterator it = newly_added_vector.begin(); it != newly_added_vector.end(); ++it)
		{
			int obj_index = *it;
			int current_sim = 0;

			for(int j = 0; j < d; j++)
			{
				vector<int> temp_index = sorted_sim_index.at(j);
				vector<float> temp_sim = sim_matrix.at(j);
				int pos = find(temp_index.begin(), temp_index.end(), obj_index) - temp_index.begin();
				current_sim += temp_sim.at(pos);

				// for each window, update seen object_id
			}

			seen_sim->insert(current_sim, obj_index);
			TA_seen.insert(newly_added.begin(), newly_added.end());

			int cur_k = min(top_k, seen_sim->size());
			float current_worst = seen_sim->ith_key(seen_sim->size() - 1);

			if(current_worst < current_best && cur_k == top_k)
			{
				flag = true;
				cout<< "Total run: " << round << endl;
			}
			round++;
		}
	}


	// delete sim_matrix
	return 0;
}


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
		const char  *output_folder)         	// output folder
{
	timeval start_time, end_time;

	// -------------------------------------------------------------------------
	//  read the ground truth file
	// -------------------------------------------------------------------------
	gettimeofday(&start_time, NULL);

	Result **R = new Result*[qn];
	for (int i = 0; i < qn; ++i) R[i] = new Result[MAXK];
	if (read_ground_truth(qn, truth_set, R) == 1) {
		printf("Reading Truth Set Error!\n");
		return 1;
	}

	gettimeofday(&end_time, NULL);
	float read_file_time = end_time.tv_sec - start_time.tv_sec +
			(end_time.tv_usec - start_time.tv_usec) / 1000000.0f;
	printf("Read Ground Truth: %f Seconds\n\n", read_file_time);

	// -------------------------------------------------------------------------
	//  c-AMIP search via linear scan
	// -------------------------------------------------------------------------
	char output_set[200];
	sprintf(output_set, "%slinear.out", output_folder);

	FILE *fp = fopen(output_set, "a+");
	if (!fp) {
		printf("Could not create %s\n", output_set);
		return 1;
	}

	int max_round = 4;
	vector<int> kMIPs;
	if(top_k == 25)
	{
		// top-25
		kMIPs.push_back(1);
		kMIPs.push_back(2);
		kMIPs.push_back(5);
		kMIPs.push_back(10);
		kMIPs.push_back(25);
		// int kMIPs[] = { 1, 2, 5, 10, 25};
		max_round = 5;
	}

	else if(top_k == 10)
	{
		kMIPs.push_back(1);
		kMIPs.push_back(2);
		kMIPs.push_back(5);
		kMIPs.push_back(10);
		// int kMIPs[] = { 1, 2, 5, 10};
		max_round = 4;
	}
	else
	{
		// top-50
		kMIPs.push_back(1);
		kMIPs.push_back(2);
		kMIPs.push_back(5);
		kMIPs.push_back(10);
		kMIPs.push_back(25);
		kMIPs.push_back(50);
		// int kMIPs[] = { 1, 2, 5, 10, 25, 50};
		max_round = 6;
	}

	float runtime = -1.0f;
	float overall_ratio = -1.0f;
	float recall = -1.0f;

	printf("Top-k MIP of Linear Scan:\n");
	printf("  Top-k\t\tRatio\t\tTime (ms)\tRecall\n");
	for (int num = 0; num < max_round; num++) {
		gettimeofday(&start_time, NULL);
		// top_k = kMIPs[num];

		top_k = kMIPs[num] - layer_index + 1;

		MaxK_List* list = new MaxK_List(top_k);

		overall_ratio = 0.0f;
		recall = 0.0f;
		for (int i = 0; i < qn; ++i)
		{
			list->reset();

			// compute TA_TopK here, return as list
			compute_TA(d, n, top_k, list, data, query[i]);

			/*for (int j = 0; j < n; ++j)
			{
				float ip = calc_inner_product(d, data[j], query[i]);
				list->insert(ip, j + 1);
			}*/
			recall += calc_recall(top_k, (const Result *) R[i], list);

			float ratio = 0.0f;
			for (int j = 0; j < top_k; ++j)
			{
				ratio += R[i][j].key_ / list->ith_key(j);
			}
			overall_ratio += ratio / top_k;
		}
		delete list; list = NULL;
		gettimeofday(&end_time, NULL);
		runtime = end_time.tv_sec - start_time.tv_sec + (end_time.tv_usec -
				start_time.tv_usec) / 1000000.0f;

		overall_ratio = overall_ratio / qn;
		recall        = recall / qn;
		runtime       = (runtime * 1000.0f) / qn;

		printf("  %3d\t\t%.4f\t\t%.4f\t\t%.2f%%\n", top_k, overall_ratio,
				runtime, recall);
		fprintf(fp, "%d\t%f\t%f\t%f\n", top_k, overall_ratio, runtime, recall);
	}
	printf("\n");
	fprintf(fp, "\n");
	fclose(fp);

	// -------------------------------------------------------------------------
	//  release space
	// -------------------------------------------------------------------------
	delete[] R; R = NULL;

	return 0;
}



// -----------------------------------------------------------------------------
int linear_scan(                    		  	// find top-k mip using linear_scan
		int   n,                            	// number of data points
		int   qn,                           	// number of query points
		int   d,                            	// dimension of space
		int   layer_index,
		int   top_k,
		const float **data,                	// data set
		const float **query,                	// query set
		const char  *truth_set,             	// address of truth set
		const char  *output_folder)         	// output folder
{
	timeval start_time, end_time;

	// -------------------------------------------------------------------------
	//  read the ground truth file
	// -------------------------------------------------------------------------
	gettimeofday(&start_time, NULL);

	Result **R = new Result*[qn];
	for (int i = 0; i < qn; ++i) R[i] = new Result[MAXK];
	if (read_ground_truth(qn, truth_set, R) == 1) {
		printf("Reading Truth Set Error!\n");
		return 1;
	}

	gettimeofday(&end_time, NULL);
	float read_file_time = end_time.tv_sec - start_time.tv_sec +
			(end_time.tv_usec - start_time.tv_usec) / 1000000.0f;
	printf("Read Ground Truth: %f Seconds\n\n", read_file_time);

	// -------------------------------------------------------------------------
	//  c-AMIP search via linear scan
	// -------------------------------------------------------------------------
	char output_set[200];
	sprintf(output_set, "%slinear.out", output_folder);

	FILE *fp = fopen(output_set, "a+");
	if (!fp) {
		printf("Could not create %s\n", output_set);
		return 1;
	}

	int max_round = 4;
	vector<int> kMIPs;
	if(top_k == 25)
	{
		// top-25
		kMIPs.push_back(1);
		kMIPs.push_back(2);
		kMIPs.push_back(5);
		kMIPs.push_back(10);
		kMIPs.push_back(25);
		// int kMIPs[] = { 1, 2, 5, 10, 25};
		max_round = 5;
	}

	else if(top_k == 10)
	{
		kMIPs.push_back(1);
		kMIPs.push_back(2);
		kMIPs.push_back(5);
		kMIPs.push_back(10);
		// int kMIPs[] = { 1, 2, 5, 10};
		max_round = 4;
	}
	else
	{
		// top-50
		kMIPs.push_back(1);
		kMIPs.push_back(2);
		kMIPs.push_back(5);
		kMIPs.push_back(10);
		kMIPs.push_back(25);
		kMIPs.push_back(50);
		// int kMIPs[] = { 1, 2, 5, 10, 25, 50};
		max_round = 6;
	}

	float runtime = -1.0f;
	float overall_ratio = -1.0f;
	float recall = -1.0f;

	printf("Top-k MIP of Linear Scan:\n");
	printf("  Top-k\t\tRatio\t\tTime (ms)\tRecall\n");
	for (int num = 0; num < max_round; num++) {
		gettimeofday(&start_time, NULL);
		// top_k = kMIPs[num];

		top_k = kMIPs[num] - layer_index + 1;

		MaxK_List* list = new MaxK_List(top_k);

		overall_ratio = 0.0f;
		recall = 0.0f;
		for (int i = 0; i < qn; ++i)
		{
			list->reset();
			for (int j = 0; j < n; ++j)
			{
				float ip = calc_inner_product(d, data[j], query[i]);
				list->insert(ip, j + 1);
			}
			recall += calc_recall(top_k, (const Result *) R[i], list);

			float ratio = 0.0f;
			for (int j = 0; j < top_k; ++j)
			{
				ratio += R[i][j].key_ / list->ith_key(j);
			}
			overall_ratio += ratio / top_k;
		}
		delete list; list = NULL;
		gettimeofday(&end_time, NULL);
		runtime = end_time.tv_sec - start_time.tv_sec + (end_time.tv_usec -
				start_time.tv_usec) / 1000000.0f;

		overall_ratio = overall_ratio / qn;
		recall        = recall / qn;
		runtime       = (runtime * 1000.0f) / qn;

		printf("  %3d\t\t%.4f\t\t%.4f\t\t%.2f%%\n", top_k, overall_ratio,
				runtime, recall);
		fprintf(fp, "%d\t%f\t%f\t%f\n", top_k, overall_ratio, runtime, recall);
	}
	printf("\n");
	fprintf(fp, "\n");
	fclose(fp);

	// -------------------------------------------------------------------------
	//  release space
	// -------------------------------------------------------------------------
	delete[] R; R = NULL;

	return 0;
}

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
		bool post_opt)         // output folder
{
	timeval start_time, end_time;

	// -------------------------------------------------------------------------
	//  read the ground truth file
	// -------------------------------------------------------------------------
	gettimeofday(&start_time, NULL);

	Result **R = new Result*[qn];
	for (int i = 0; i < qn; ++i) R[i] = new Result[MAXK];
	if (read_ground_truth(qn, truth_set, R) == 1)
	{
		printf("Reading Truth Set Error!\n");
		return 1;
	}

	gettimeofday(&end_time, NULL);
	float read_file_time = end_time.tv_sec - start_time.tv_sec +
			(end_time.tv_usec - start_time.tv_usec) / 1000000.0f;
	printf("Read Ground Truth: %f Seconds\n\n", read_file_time);

	// -------------------------------------------------------------------------
	//  indexing
	// -------------------------------------------------------------------------
	gettimeofday(&start_time, NULL);
	Simple_LSH *lsh = new Simple_LSH();
	lsh->build(n, d, K, L, S, nn_ratio, data, post_opt, temp_hash);

	gettimeofday(&end_time, NULL);
	float indexing_time = end_time.tv_sec - start_time.tv_sec +
			(end_time.tv_usec - start_time.tv_usec) / 1000000.0f;
	printf("Indexing Time: %f Seconds\n\n", indexing_time);

	// -------------------------------------------------------------------------
	//  Precision Recall Curve of Simple_LSH
	// -------------------------------------------------------------------------
	int threshold_conditions = 2;
     bool use_threshold_pruning[] = {true, false};
     string str_array[] = {"with_threshold", "without_threshold"};


	/*int threshold_conditions = 1;
	bool use_threshold_pruning[] = {false};
	string str_array[] = {"without_threshold"};*/

	int max_round = 4;
	vector<int> kMIPs;
	if(top_k == 25)
	{
		// top-25
		kMIPs.push_back(1);
		kMIPs.push_back(2);
		kMIPs.push_back(5);
		kMIPs.push_back(10);
		kMIPs.push_back(25);
		// int kMIPs[] = { 1, 2, 5, 10, 25};
		max_round = 5;
	}

	else if(top_k == 10)
	{
		kMIPs.push_back(1);
		kMIPs.push_back(2);
		kMIPs.push_back(5);
		kMIPs.push_back(10);
		// int kMIPs[] = { 1, 2, 5, 10};
		max_round = 4;
	}
	else
	{
		// top-50
		kMIPs.push_back(1);
		kMIPs.push_back(2);
		kMIPs.push_back(5);
		kMIPs.push_back(10);
		kMIPs.push_back(25);
		kMIPs.push_back(50);
		// int kMIPs[] = { 1, 2, 5, 10, 25, 50};
		max_round = 6;
	}

	for(int ii = 0; ii < threshold_conditions; ii++)
	{
		int top_k = -1;
		vector<float>* temp_sim_angle_vec = new vector<float>[qn];

		bool is_threshold = use_threshold_pruning[ii];
		string is_threshold_file_name = str_array[ii];

		char output_set[200];
		sprintf(output_set, "%ssimple_lsh_recall_%s_%d.out", output_folder, is_threshold_file_name.c_str(), sample_index);

		FILE *fp = fopen(output_set, "a+");
		if (!fp)
		{
			printf("Could not create %s\n", output_set);
			return 1;
		}

		if(layer_index != 1 && is_threshold)
		{
			printf("Using threshold, layer index: %d .\n", layer_index);
			FILE *fp1 = fopen(sim_angle, "r");
			if (!fp1)
			{
				printf("Could not open %s\n", sim_angle);
				return 1;
			}
			for(int i = 0; i < qn; i++)
			{
				for(int j = 0; j < max_round; j++)
				{
					float temp = 0.0f;
					fscanf(fp1, " %f", &temp);
					temp_sim_angle_vec[i].push_back(temp);
				}
				fscanf(fp1, "\n");
			}
			fclose(fp1);
		}
		else
		{
			for(int i = 0; i < qn; i++)
			{
				// no intilaization info from the file
				for(int j = 0; j < max_round; j++)
				{
					temp_sim_angle_vec[i].push_back(90.0f);
				}
			}
		}

		float runtime = -1.0f;
		float recall = -1.0f;
		float candidate_size = -1.0f;

		unordered_map<int, float> my_run_time;
		unordered_map<int, float> average_candidate_size;
		unordered_map<int, float> total_hash_table_hit;

		printf("Top-k c-AMIP of Simple_LSH: \n");
		printf("  Top-k\t\tTime (ms)\tRecall\n");

		for (int num = 0; num < max_round; num++)
		{
			int total_hash_hits = 0;
			gettimeofday(&start_time, NULL);
			float file_processing_time = 0.0f;

			top_k = kMIPs[num] - layer_index + 1;
			// if(top_k < layer_index)
			if(top_k <=0 )
			{
				continue;
			}
			MaxK_List* list = new MaxK_List(top_k);

			recall = 0.0f;
			// candidate_size = 0.0f;
			candidate_size = 0;

			printf("\n");
			for (int i = 0; i < qn; ++i)
			{
				int current_hash_hits = 0;
				list->reset();

				// top-k computation with threshold from previous layers
				candidate_size += lsh->kmip(top_k, query[i], list, temp_sim_angle_vec[i][num], is_threshold, current_hash_hits);
				recall += calc_recall(top_k, (const Result *) R[i], list);
				total_hash_hits += current_hash_hits;


				// persist on file to compute overall performance
				char output_set[200];
				sprintf(output_set, "%s_top_%d_%s_%d.txt", temp_result, top_k + layer_index - 1, is_threshold_file_name.c_str(), sample_index);

				timeval file_start_time, file_end_time;
				gettimeofday(&file_start_time, NULL);
				persist_intermediate_on_file(top_k + layer_index - 1, d, list, data, query[i], output_set);
				gettimeofday(&file_end_time, NULL);

				file_processing_time += file_end_time.tv_sec - file_start_time.tv_sec + (file_end_time.tv_usec -
						file_start_time.tv_usec) / 1000000.0f;
			}
			delete list; list = NULL;

			gettimeofday(&end_time, NULL);
			runtime = end_time.tv_sec - start_time.tv_sec + (end_time.tv_usec -
					start_time.tv_usec) / 1000000.0f;
			runtime = runtime - file_processing_time;
			pair<int, float > dict_time(top_k + layer_index - 1, runtime);
			my_run_time.insert(dict_time);

			candidate_size = candidate_size * 1.0f / qn;
			total_hash_hits = total_hash_hits * 1.0f/ qn;
			pair<int, float > dict_candidate(top_k + layer_index - 1, candidate_size);
			pair<int, float > dict_hash_table_hit(top_k + layer_index - 1, total_hash_hits);
			average_candidate_size.insert(dict_candidate);
			total_hash_table_hit.insert(dict_hash_table_hit);

			recall        = recall / qn;
			runtime       = (runtime * 1000.0f) / qn;

			printf("  %3d\t\t%.4f\t\t%.2f\n", top_k + layer_index - 1, runtime, recall);
			fprintf(fp, "%d\t%f\t%f\n", top_k + layer_index - 1, runtime, recall);
		}

		if(is_threshold)
		{
			// output updated temp_sim_angle back to file
			FILE *fp2 = fopen(sim_angle, "w");
			if (!fp2)
			{
				printf("Could not open %s\n", sim_angle);
				return 1;
			}
			for(int i = 0; i < qn; i++)
			{
				// no intilaization info from the file
				for(int j = 0; j < max_round; j++)
				{
					fprintf(fp2, "%f\t", temp_sim_angle_vec[i][j]);
				}
				fprintf(fp2, "\n");
			}
			fclose(fp2);
		}

		char temp_result_set[200];
		// sprintf(temp_result_set, "%s_top_%d_%s", temp_result, top_k, is_threshold_file_name.c_str());
		sprintf(temp_result_set, "%s_%s_%d", temp_result, is_threshold_file_name.c_str(), sample_index);
		persist_candidate_size(average_candidate_size, total_hash_table_hit, temp_result_set, my_run_time);

		printf("\n");
		fprintf(fp, "\n");
		fclose(fp);

		// clear vector
		for(int jj = 0; jj < qn; jj++)
		{
			vector<float>().swap(temp_sim_angle_vec[jj]);
		}
	}
	// -------------------------------------------------------------------------
	//  release space
	// -------------------------------------------------------------------------
	delete lsh; lsh = NULL;
	delete[] R; R = NULL;
	return 0;
}

// -----------------------------------------------------------------------------
int norm_distribution(                // analyse norm distribution of data
		int   n,                            // number of data points
		int   d,                            // dimension of space
		const float **data,                    // data set
		const char  *output_folder)         // output folder
{
	timeval start_time, end_time;

	// -------------------------------------------------------------------------
	//  calc norm for all data objects
	// -------------------------------------------------------------------------
	gettimeofday(&start_time, NULL);
	vector<float> norm(n, 0.0f);
	float max_norm = MINREAL;

	for (int i = 0; i < n; ++i) {
		norm[i] = sqrt(calc_inner_product(d, data[i], data[i]));
		if (norm[i] > max_norm) max_norm = norm[i];
	}

	// -------------------------------------------------------------------------
	//  get the percentage of frequency of norm
	// -------------------------------------------------------------------------
	int m = 25;
	float interval = max_norm / m;
	printf("m = %d, max_norm = %f, interval = %f\n", m, max_norm, interval);

	vector<int> freq(m, 0);
	for (int i = 0; i < n; ++i) {
		int id = (int) ceil(norm[i] / interval) - 1;
		if (id < 0) id = 0;
		if (id >= m) id = m - 1;
		freq[id]++;
	}

	// -------------------------------------------------------------------------
	//  write norm distribution
	// -------------------------------------------------------------------------
	char output_set[200];
	sprintf(output_set, "%snorm_distribution.out", output_folder);

	FILE *fp = fopen(output_set, "w");
	if (!fp) {
		printf("Could not create %s\n", output_set);
		return 1;
	}

	float num = 0.5f / m;
	float step = 1.0f / m;
	for (int i = 0; i < m; ++i) {
		fprintf(fp, "%.1f\t%f\n", (num + step * i) * 100.0, freq[i] * 100.0 / n);
	}
	fprintf(fp, "\n");
	fclose(fp);

	gettimeofday(&end_time, NULL);
	float runtime = end_time.tv_sec - start_time.tv_sec + (end_time.tv_usec -
			start_time.tv_usec) / 1000000.0f;
	printf("Norm distribution: %.6f Seconds\n\n", runtime);

	return 0;
}

// -----------------------------------------------------------------------------
int persist_intermediate_on_file(        		// persist intermediate result per query per onion layer on file, for aggregation
		int   topk,                         	// topk results of interest
		int   d,                            	// dimension of space
		MaxK_List* list,                    	// list that contains the topk result per query per onion layer
		const float **data,                    	// original data set
		const float *query,						// original query
		const char  *output_folder)            	// output folder
{
	FILE *fp = fopen(output_folder, "a+");
	if (!fp)
	{
		printf("Could not create %s\n", output_folder);
		return 1;
	}

	// persist the dot product in between query and original data

	for(int i = 0; i < list->size(); i++)
	{
		int current_data_idx = list->ith_id(i) - 1;
		if(current_data_idx < 0 )
		{
			for(int j = 0; j < d; j++)
			{
				fprintf(fp, "%f\t", -1.0f);

			}
			fprintf(fp, "%f\n", -100.0f);    // flush the similarity value to file
		}
		else
		{
			float temp_value = list->ith_key(i);
			for(int j = 0; j < d; j++)
			{
				fprintf(fp, "%f\t", data[current_data_idx][j]);
			}
			// value is based on scaled similarity, need to update to
			// the ones in between original data and real query

			// fprintf(fp, "%f\n", list->ith_key(i));    // flush the similarity value to file
			float temp_sim_original = calc_inner_product(d, data[current_data_idx], query);
			fprintf(fp, "%f\n", temp_sim_original);    // flush the similarity value to file

		}
	}
	fclose(fp);

	return 0;
}

// -----------------------------------------------------------------------------
int persist_candidate_size(                				// persist average number of candidate on file, regarding to a specific topk
		unordered_map<int, float> candidate_map,     	// average value of candidate size
		unordered_map<int, float> hash_table_hit_map,	// average hash table hit counts
		const char  *output_folder,            			// output folder
		unordered_map<int, float> my_run_time)   		// run time of different top-k
{
	int run_time_index = 0;
	for ( auto it = candidate_map.begin(), itt = hash_table_hit_map.begin(); it != candidate_map.end() && itt != hash_table_hit_map.end(); ++it, ++itt)
	{
		int top_k_key = (int)it->first;
		float element_count = (float)it->second;
		float run_time =  my_run_time[(int)it->first];

		int hash_hit_key = (int)itt->first;
		float hash_hit_count = (float)itt->second;

		char output_set[200];
		sprintf(output_set, "%s_top_%d_candidate_size.txt", output_folder, top_k_key);
		FILE *fp = fopen(output_set, "a+");
		if (!fp)
		{
			printf("Could not create %s\n", output_set);
			return 1;
		}
		// fprintf(fp, "%f, %f\n", element_count, run_time);
		fprintf(fp, "%f, %f, ", element_count, run_time);
		fprintf(fp, "%f \n", hash_hit_count);

		fclose(fp);
	}
	return 0;
}

// -----------------------------------------------------------------------------
int persist_sample_results(int max_top_k, MaxK_List* list, FILE *fp)
{
	assert(fp != NULL && list->size() == max_top_k);

	// persist current sample top-k results on file
	for(int i = 0; i < list->size(); i++)
	{
		int current_data_idx = list->ith_id(i) - 1;
		current_data_idx = current_data_idx < 0 ? -1 : current_data_idx;
		float temp_value = current_data_idx < 0 ? -1.0f : list->ith_key(i);
		fprintf(fp, "%d %f ", current_data_idx, temp_value);
	}
	fprintf(fp, "\n");
	return 0;
}

// -------------------------------------------------------------------------
//  read all candidates per top_k, per query per onion layer
// -------------------------------------------------------------------------
int overall_performance(                        	// output the overall performance of indexing
		int   d,                                	// dimension of space
		int   qn,                             		// number of queries
		int   layers,                        		// max amount of onion layers so far
		int   top_k, 								// top 25 or top 50?
		int   sample_index,							// sample index of current operation
		const char  *temp_output_folder,        	// temporal output
		const char  *ground_truth_folder,    		// ground truth folder
		const char  *output_folder)            		// output folder
{

	// need to pass max_number_layer we have so far as parameters into function
	// instead of top_k * top_k, we use max_layer * top_k
	MAX_DIMENSION = d;

	int threshold_conditions = 2;
	bool use_threshold_pruning[] = {true, false};
	string str_array[] = {"with_threshold", "without_threshold"};


	/*int threshold_conditions = 1;
	bool use_threshold_pruning[] = {false};
	string str_array[] = {"without_threshold"};*/


	int max_round = 4;
	vector<int> kMIPs;
	if(top_k == 25)
	{
		// top-25
		// int kMIPs[] = { 1, 2, 5, 10, 25};
		kMIPs.push_back(1);
		kMIPs.push_back(2);
		kMIPs.push_back(5);
		kMIPs.push_back(10);
		kMIPs.push_back(25);
		max_round = 5;
	}

	else if(top_k == 10)
	{
		// int kMIPs[] = { 1, 2, 5, 10};
		kMIPs.push_back(1);
		kMIPs.push_back(2);
		kMIPs.push_back(5);
		kMIPs.push_back(10);
		max_round = 4;
	}
	else
	{
		// top-50
		// int kMIPs[] = { 1, 2, 5, 10, 25, 50};
		kMIPs.push_back(1);
		kMIPs.push_back(2);
		kMIPs.push_back(5);
		kMIPs.push_back(10);
		kMIPs.push_back(25);
		kMIPs.push_back(50);
		max_round = 6;
	}

	// -------------------------------------------------------------------------
	//  read the ground truth file
	// -------------------------------------------------------------------------
	Result **R = new Result*[qn];
	for (int i = 0; i < qn; ++i)
	{
		R[i] = new Result[MAXK];
	}
	if (read_ground_truth(qn, ground_truth_folder, R) == 1)
	{
		printf("Reading Truth Set Error!\n");
		return 1;
	}

	for(int ii = 0 ; ii < threshold_conditions; ii++)
	{
		bool is_threshold = use_threshold_pruning[ii];
		string is_threshold_file_name = str_array[ii];
		// -------------------------------------------------------------------------
		//  compute precision and recall per query
		// -------------------------------------------------------------------------
		float *recall = new float[max_round];
		float *NDCG = new float[max_round];
		float *avg_topk_ground_truth = new float[max_round];
		float *avg_topk_ret = new float[max_round];
		for (int round = 0; round < max_round; ++round)
		{
			recall[round] = 0;
			NDCG[round] = 0;

			avg_topk_ground_truth[round] = 0.0f;
			avg_topk_ret[round] = 0.0f;
		}

		printf("Top-t c-AMIP of Simple_LSH (overall): \n");
		FILE *query_sample_file_handle = NULL;

		for (int round = 0; round < max_round; ++round)
		{
			int top_k = kMIPs[round];
			int temp_layer = min(top_k, layers);
			/*if(top_k > layers)
			{
				break;
			}*/
			char output_set[200];
			sprintf(output_set, "%s_top_%d_%s.txt", temp_output_folder, top_k, is_threshold_file_name.c_str());

			// load from file
			FILE *fp1 = fopen(output_set, "r");
			if (!fp1)
			{
				printf("Could not open %s\n", output_set);
				return 1;
			}

			/**
			 * Created by Sicong
			 *
			 * The idea essentially is to combine the top-k results of the same
			 * query across different layers, then aggregate different query
			 * results together
			 * */

			int total_num = temp_layer * top_k - temp_layer * (temp_layer - 1)/2;

			float*** temp_result = new float**[qn];
			for(int i = 0; i < qn; i++)
			{
				// temp_result[i] = new float*[temp_layer * top_k];
				// for(int j=0; j< temp_layer * top_k; j++)
				temp_result[i] = new float*[total_num];
				for(int j=0; j< total_num; j++)
				{
					temp_result[i][j] = new float[d+1];
				}
			}

			int q_index = 0;
			int layer_index = 0;	// range [0, layers - 1]
			int cur_q_line_count = 0;
			int line_count = 0;

			int temp_top_k = top_k;
			int cur_counter = temp_top_k * qn;
			int per_query_accumu_index = 0;
			while (!feof(fp1) && line_count < total_num * qn)
			{
				if(cur_q_line_count%temp_top_k == 0 && line_count > 0)
				{
					q_index = (++q_index)%qn;
					cur_q_line_count = 0;
					if(line_count == cur_counter)
					{
						++layer_index;
						per_query_accumu_index += temp_top_k;
						temp_top_k = temp_top_k - 1;
						cur_counter += temp_top_k * qn;
					}
				}
				for (int j = 0; j < d + 1; ++j)
				{
					// fscanf(fp1, " %f", &temp_result[q_index][cur_q_line_count + layer_index * temp_top_k][j]);
					// fscanf(fp1, " %f", &temp_result[q_index][cur_q_line_count + layer_index * (temp_top_k + 1)][j]);
					fscanf(fp1, " %f", &temp_result[q_index][cur_q_line_count + per_query_accumu_index][j]);
				}
				fscanf(fp1, "\n");
				++line_count;
				++cur_q_line_count;

			}

			printf("top_k: %d, max amount of layers: %d, qn: %d, line_count: %d, total num: %d.\n", top_k, layers, qn, line_count, total_num);



			// assert(feof(fp1) && line_count == temp_layer * top_k * qn);
			assert(feof(fp1) && line_count == total_num * qn);

			MaxK_List* list = new MaxK_List(top_k);

			/**
			 * Added by Sicong, April-08-2019
			 * */
			// collect at final round
			// persist top-k candidates from each query, each optimized top_k and each topk, each sample on file
			if(round == max_round)
			{
				char query_sample_file_name[100];
				sprintf(query_sample_file_name, "%s_top_%d_%s_%d.txt", temp_output_folder, top_k, is_threshold_file_name.c_str(), sample_index);
				// create file handle
				query_sample_file_handle = fopen(query_sample_file_name, "a+");
			}



			for (int i = 0; i < qn; ++i)
			{
				list->reset();

				// temp_layer * top_k should be the total number of candidates that
				// top_k, top_k - 1, top_k - 2, top_k - 3 .... top_k - temp_layer + 1
				// for(int j = 0; j < temp_layer * top_k; j++)
				for(int j = 0; j < total_num ; j++)
				{
					list->insert(temp_result[i][j][d], j + 1);
				}

				if(round == max_round - 1 && query_sample_file_handle != NULL)
				{
					persist_sample_results(top_k, list, query_sample_file_handle);
				}

				recall[round] += calc_recall(top_k, (const Result *) R[i], list);
				NDCG[round] += calc_NDCG(top_k, (const Result *) R[i], list);

				avg_topk_ground_truth[round] += R[i][top_k - 1].key_;
				avg_topk_ret[round] += list->ith_key(top_k - 1) > 0 ? list->ith_key(top_k - 1) : 0;
			}

			delete list;
			list = NULL;
			fclose(fp1);
			// -------------------------------------------------------------------------
			//  free memory space
			// -------------------------------------------------------------------------
			for(int i = 0; i < qn; i++)
			{
				for(int j = 0; j < total_num; j++)
				{
					delete[] temp_result[i][j];
					temp_result[i][j] = NULL;
				}
				delete[] temp_result[i];
				temp_result[i] = NULL;
			}
			delete[] temp_result;
			temp_result = NULL;

		}

		// close file handle
		fclose(query_sample_file_handle);

		char output_folder_set[200];
		// sprintf(output_folder_set, "%s_top_%d%s.txt", temp_output_folder, top_k, is_threshold_file_name.c_str());
		sprintf(output_folder_set, "%s_%s_%d.txt", output_folder, is_threshold_file_name.c_str(), sample_index);

		printf("Output path %s \n ", output_folder_set);
		FILE *fp2 = fopen(output_folder_set, "a+");
		if (!fp2)
		{
			printf("Could not open %s\n", output_folder_set);
			return 1;
		}
		printf("Top-k\t\tRecall\tNDCG\tground_truth\treturned_results\n");
		fprintf(fp2, "Top-k\t\tRecall\tNDCG\tground_truth\treturned_results\n");
		for (int round = 0; round < max_round; ++round)
		{
			int top_k = kMIPs[round];
			recall[round] = recall[round] / qn;
			NDCG[round] = NDCG[round] * 1.0f / qn;

			avg_topk_ground_truth[round] = avg_topk_ground_truth[round]/qn;
			avg_topk_ret[round] = avg_topk_ret[round]/qn;

			printf("%4d\t\t%.2f\t%.2f\t%.2f\t%.2f\n", top_k,
					recall[round], NDCG[round], avg_topk_ground_truth[round], avg_topk_ret[round]);
			fprintf(fp2, "%d\t%f\t%f\t%f\t%f\n", top_k,
					recall[round], NDCG[round], avg_topk_ground_truth[round], avg_topk_ret[round]);
			printf("\n");
			fprintf(fp2, "\n");
		}
		printf("\n");
		fprintf(fp2, "\n");
		fclose(fp2);

		delete[] recall; recall = NULL;
		delete[] NDCG; NDCG = NULL;
	}
	delete[] R; R = NULL;
	return 0;
}

// -----------------------------------------------------------------------------
int my_sort_col(const void *pa, const void *pb )
{
	const int *a = *(const int **)pa;
	const int *b = *(const int **)pb;
	return (a[MAX_DIMENSION] < b[MAX_DIMENSION]) - (a[MAX_DIMENSION] > b[MAX_DIMENSION]);
}

// -----------------------------------------------------------------------------
/**
 * Added by Sicong, April-08-2019
 * Combine result from each sampled portion
 *
 * And Delete intermediate files afterwards
 * */
int combine_sample_result(int sample_space, int optimized_topk, int qn, const char  *temp_result)
{
	int threshold_conditions = 2;
	bool use_threshold_pruning[] = {true, false};
	string str_array[] = {"with_threshold", "without_threshold"};
	int max_round = 4;
	vector<int> kMIPs;
	if(optimized_topk == 25)
	{
		// top-25
		// int kMIPs[] = { 1, 2, 5, 10, 25};
		kMIPs.push_back(1);
		kMIPs.push_back(2);
		kMIPs.push_back(5);
		kMIPs.push_back(10);
		kMIPs.push_back(25);
		max_round = 5;
	}

	else if(optimized_topk == 10)
	{
		// int kMIPs[] = { 1, 2, 5, 10};
		kMIPs.push_back(1);
		kMIPs.push_back(2);
		kMIPs.push_back(5);
		kMIPs.push_back(10);
		max_round = 4;
	}
	else
	{
		// top-50
		// int kMIPs[] = { 1, 2, 5, 10, 25, 50};
		kMIPs.push_back(1);
		kMIPs.push_back(2);
		kMIPs.push_back(5);
		kMIPs.push_back(10);
		kMIPs.push_back(25);
		kMIPs.push_back(50);
		max_round = 6;
	}
	for (int ii = 0; ii < threshold_conditions; ii++)
	{
		bool is_threshold = use_threshold_pruning[ii];
		string is_threshold_file_name = str_array[ii];

		for (int jj = 0; jj < max_round; jj++)
		{
			int top_k = kMIPs[jj];
			// a vector of maps with size qn
			// key : value = data_index_id : aggrgated_sim_value
			unordered_map<string, vector<int>>* maps_ = new unordered_map<string, vector<int> >[qn];
			for(int i = 0; i < sample_space; i++)
			{
				char output_set[200];
				sprintf(output_set, "%s_top_%d_%s_%d.txt", temp_result, top_k, is_threshold_file_name.c_str(), i);
				// read results and combine (sim_value, data_index_id) and compute recall

				delete[] output_set; output_set = NULL;
			}
		}
	}



}
