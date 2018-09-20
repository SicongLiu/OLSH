#include "headers.h"

int MAX_DIMENSION = 0;

// -----------------------------------------------------------------------------
int ground_truth(					// find the ground truth results
	int   n,							// number of data points
	int   qn,							// number of query points
	int   d,							// dimension of space
	const float **data,					// data set
	const float **query,				// query set
	const char  *truth_set)				// address of truth set
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
int h2_alsh(						// mip search via h2_alsh
	int   n,							// number of data points
	int   qn,							// number of query points
	int   d,							// dimension of space
	float nn_ratio,						// approximation ratio for nn search
	float mip_ratio,					// approximation ratio for mip search
	const float **data,					// data set
	const float **query,				// query set
	const char  *truth_set,				// address of truth set
	const char  *output_folder)			// output folder
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
	//  indexing
	// -------------------------------------------------------------------------
	gettimeofday(&start_time, NULL);
	H2_ALSH *lsh = new H2_ALSH();
	lsh->build(n, d, nn_ratio, mip_ratio, data);

	gettimeofday(&end_time, NULL);
	float indexing_time = end_time.tv_sec - start_time.tv_sec + 
		(end_time.tv_usec - start_time.tv_usec) / 1000000.0f;
	printf("Indexing Time: %f Seconds\n\n", indexing_time);

	// -------------------------------------------------------------------------
	//  c-AMIP search via H2_ALSH
	// -------------------------------------------------------------------------	
	char output_set[200];
	sprintf(output_set, "%sh2_alsh.out", output_folder);

	FILE *fp = fopen(output_set, "a+");
	if (!fp) {
		printf("Could not create %s\n", output_set);
		return 1;
	}

	int kMIPs[] = { 1, 2, 5, 10 };
	int max_round = 4;
	int top_k = -1;

	float runtime = -1.0f;
	float overall_ratio = -1.0f;
	float recall = -1.0f;

	printf("Top-k c-AMIP of H2_ALSH: \n");
	printf("  Top-k\t\tRatio\t\tTime (ms)\tRecall\n");
	for (int num = 0; num < max_round; num++) {
		gettimeofday(&start_time, NULL);
		top_k = kMIPs[num];
		MaxK_List* list = new MaxK_List(top_k);

		overall_ratio = 0.0f;
		recall = 0.0f;
		for (int i = 0; i < qn; ++i) {
			list->reset();
			lsh->kmip(top_k, query[i], list);
			recall += calc_recall(top_k, (const Result *) R[i], list);
			
			float ratio = 0.0f;
			for (int j = 0; j < top_k; ++j) {
				ratio += list->ith_key(j) / R[i][j].key_;
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
	delete lsh; lsh = NULL;
	delete[] R; R = NULL;

	return 0;
}

// -----------------------------------------------------------------------------
int l2_alsh(						// mip search via l2_alsh
	int   n,							// number of data points
	int   qn,							// number of query points
	int   d,							// dimension of space
	int   m,							// param of l2_alsh
	float U,							// param of l2_alsh
	float nn_ratio,						// approximation ratio for nn search
	const float **data,					// data set
	const float **query,				// query set
	const char  *truth_set,				// address of truth set
	const char  *output_folder) 		// output folder
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
	//  indexing
	// -------------------------------------------------------------------------
	gettimeofday(&start_time, NULL);
	L2_ALSH *lsh = new L2_ALSH();
	lsh->build(n, d, m, U, nn_ratio, data);

	gettimeofday(&end_time, NULL);
	float indexing_time = end_time.tv_sec - start_time.tv_sec + 
		(end_time.tv_usec - start_time.tv_usec) / 1000000.0f;
	printf("Indexing Time: %f Seconds\n\n", indexing_time);

	// -------------------------------------------------------------------------
	//  c-AMIP search via L2_ALSH
	// -------------------------------------------------------------------------	
	char output_set[200];
	sprintf(output_set, "%sl2_alsh.out", output_folder);

	FILE *fp = fopen(output_set, "a+");
	if (!fp) {
		printf("Could not create %s\n", output_set);
		return 1;
	}

	int kMIPs[] = { 1, 2, 5, 10 };
	int max_round = 4;
	int top_k = -1;

	float runtime = -1.0f;
	float overall_ratio = -1.0f;
	float recall = -1.0f;

	printf("Top-k c-AMIP of L2_ALSH: \n");
	printf("  Top-k\t\tRatio\t\tTime (ms)\tRecall\n");
	for (int num = 0; num < max_round; num++) {
		gettimeofday(&start_time, NULL);
		top_k = kMIPs[num];
		MaxK_List* list = new MaxK_List(top_k);

		overall_ratio = 0.0f;
		recall = 0.0f;
		for (int i = 0; i < qn; ++i) {
			list->reset();
			lsh->kmip(top_k, query[i], list);
			recall += calc_recall(top_k, (const Result *) R[i], list);
			
			float ratio = 0.0f;
			for (int j = 0; j < top_k; ++j) {
				ratio += list->ith_key(j) / R[i][j].key_;
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
	delete lsh; lsh = NULL;
	delete[] R; R = NULL;

	return 0;
}

// -----------------------------------------------------------------------------
int l2_alsh2(						// mip search via l2_alsh2
	int   n,							// number of data points
	int   qn,							// number of query points
	int   d,							// dimension of space
	int   m,							// param of l2_alsh2
	float U,							// param of l2_alsh2
	float nn_ratio,						// approximation ratio for nn search
	const float **data,					// data set
	const float **query,				// query set
	const char  *truth_set,				// address of truth set
	const char  *output_folder) 		// output folder
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
	//  indexing
	// -------------------------------------------------------------------------
	gettimeofday(&start_time, NULL);
	L2_ALSH2 *lsh = new L2_ALSH2();
	lsh->build(n, qn, d, m, U, nn_ratio, data, query);

	gettimeofday(&end_time, NULL);
	float indexing_time = end_time.tv_sec - start_time.tv_sec + 
		(end_time.tv_usec - start_time.tv_usec) / 1000000.0f;
	printf("Indexing Time: %f Seconds\n\n", indexing_time);

	// -------------------------------------------------------------------------
	//  c-AMIP search via L2_ALSH2
	// -------------------------------------------------------------------------	
	char output_set[200];
	sprintf(output_set, "%sl2_alsh2.out", output_folder);

	FILE *fp = fopen(output_set, "a+");
	if (!fp) {
		printf("Could not create %s\n", output_set);
		return 1;
	}

	int kMIPs[] = { 1, 2, 5, 10 };
	int max_round = 4;
	int top_k = -1;

	float runtime = -1.0f;
	float overall_ratio = -1.0f;
	float recall = -1.0f;

	printf("Top-k c-AMIP of L2_ALSH2: \n");
	printf("  Top-k\t\tRatio\t\tTime (ms)\tRecall\n");
	for (int num = 0; num < max_round; num++) {
		gettimeofday(&start_time, NULL);
		top_k = kMIPs[num];
		MaxK_List* list = new MaxK_List(top_k);

		overall_ratio = 0.0f;
		recall = 0.0f;
		for (int i = 0; i < qn; ++i) {
			list->reset();
			lsh->kmip(top_k, query[i], list);
			recall += calc_recall(top_k, (const Result *) R[i], list);
			
			float ratio = 0.0f;
			for (int j = 0; j < top_k; ++j) {
				ratio += list->ith_key(j) / R[i][j].key_;
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
	delete lsh; lsh = NULL;
	delete[] R; R = NULL;

	return 0;
}

// -----------------------------------------------------------------------------
int xbox(							// mip search via xbox
	int   n,							// number of data points
	int   qn,							// number of query points
	int   d,							// dimension of space
	float nn_ratio,						// approximation ratio for nn search
	const float **data,					// data set
	const float **query,				// query set
	const char  *truth_set,				// address of truth set
	const char  *output_folder) 		// output folder
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
	//  indexing
	// -------------------------------------------------------------------------
	gettimeofday(&start_time, NULL);
	XBox *lsh = new XBox();
	lsh->build(n, d, nn_ratio, data);

	gettimeofday(&end_time, NULL);
	float indexing_time = end_time.tv_sec - start_time.tv_sec + 
		(end_time.tv_usec - start_time.tv_usec) / 1000000.0f;
	printf("Indexing Time: %f Seconds\n\n", indexing_time);

	// -------------------------------------------------------------------------
	//  c-AMIP search via XBox
	// -------------------------------------------------------------------------
	char output_set[200];
	int kMIPs[] = { 1, 2, 5, 10 };
	int max_round = 4;
	int top_k = -1;

	float runtime = -1.0f;
	float overall_ratio = -1.0f;
	float recall = -1.0f;

	sprintf(output_set, "%sxbox.out", output_folder);
	FILE *fp = fopen(output_set, "a+");
	if (!fp) {
		printf("Could not create %s\n", output_set);
		return 1;
	}

	printf("Top-k c-AMIP of XBox: \n");
	printf("  Top-k\t\tRatio\t\tTime (ms)\tRecall\n");
	for (int num = 0; num < max_round; num++) {
		gettimeofday(&start_time, NULL);
		top_k = kMIPs[num];
		MaxK_List* list = new MaxK_List(top_k);

		overall_ratio = 0.0f;
		recall = 0.0f;
		for (int i = 0; i < qn; ++i) {
			list->reset();
			lsh->kmip(top_k, false, query[i], list);
			recall += calc_recall(top_k, (const Result *) R[i], list);
			
			float ratio = 0.0f;
			for (int j = 0; j < top_k; ++j) {
				ratio += list->ith_key(j) / R[i][j].key_;
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
	//  c-AMIP search via H2-ALSH-
	// -------------------------------------------------------------------------	
	sprintf(output_set, "%sh2_alsh_minus.out", output_folder);
	fp = fopen(output_set, "a+");
	if (!fp) {
		printf("Could not create %s\n", output_set);
		return 1;
	}

	printf("Top-k c-AMIP of H2-ALSH-: \n");
	printf("  Top-k\t\tRatio\t\tTime (ms)\tRecall\n");
	for (int num = 0; num < max_round; num++) {
		gettimeofday(&start_time, NULL);
		top_k = kMIPs[num];
		MaxK_List* list = new MaxK_List(top_k);

		overall_ratio = 0.0f;
		recall = 0.0f;
		for (int i = 0; i < qn; ++i) {
			list->reset();
			lsh->kmip(top_k, true, query[i], list);
			recall += calc_recall(top_k, (const Result *) R[i], list);
			
			float ratio = 0.0f;
			for (int j = 0; j < top_k; ++j) {
				ratio += list->ith_key(j) / R[i][j].key_;
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
	delete lsh; lsh = NULL;
	delete[] R; R = NULL;

	return 0;
}

// -----------------------------------------------------------------------------
int sign_alsh(						// mip search via sign_alsh
	int   n,							// number of data points
	int   qn,							// number of query points
	int   d,							// dimension of space
	int   K,							// number of hash tables
	int   m,							// param of sign_alsh
	float U,							// param of sign_alsh
	float nn_ratio,						// approximation ratio for nn search
	const float **data,					// data set
	const float **query,				// query set
	const char  *truth_set,				// address of truth set
	const char  *output_folder) 		// output folder
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
	//  indexing
	// -------------------------------------------------------------------------
	gettimeofday(&start_time, NULL);
	Sign_ALSH *lsh = new Sign_ALSH();
	lsh->build(n, d, K, m, U, nn_ratio, data);

	gettimeofday(&end_time, NULL);
	float indexing_time = end_time.tv_sec - start_time.tv_sec + 
		(end_time.tv_usec - start_time.tv_usec) / 1000000.0f;
	printf("Indexing Time: %f Seconds\n\n", indexing_time);

	// -------------------------------------------------------------------------
	//  c-AMIP search via Sign_ALSH
	// -------------------------------------------------------------------------	
	char output_set[200];
	sprintf(output_set, "%ssign_alsh.out", output_folder);

	FILE *fp = fopen(output_set, "a+");
	if (!fp) {
		printf("Could not create %s\n", output_set);
		return 1;
	}

	int kMIPs[] = { 1, 2, 5, 10 };
	int max_round = 4;
	int top_k = -1;

	float runtime = -1.0f;
	float overall_ratio = -1.0f;
	float recall = -1.0f;

	printf("Top-k c-AMIP of Sign_ALSH: \n");
	printf("  Top-k\t\tRatio\t\tTime (ms)\tRecall\n");
	for (int num = 0; num < max_round; num++) {
		gettimeofday(&start_time, NULL);
		top_k = kMIPs[num];
		MaxK_List* list = new MaxK_List(top_k);

		overall_ratio = 0.0f;
		recall = 0.0f;
		for (int i = 0; i < qn; ++i) {
			list->reset();
			lsh->kmip(top_k, query[i], list);
			recall += calc_recall(top_k, (const Result *) R[i], list);
			
			float ratio = 0.0f;
			for (int j = 0; j < top_k; ++j) {
				ratio += list->ith_key(j) / R[i][j].key_;
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
	delete lsh; lsh = NULL;
	delete[] R; R = NULL;

	return 0;
}

// -----------------------------------------------------------------------------
int simple_lsh(						// mip search via simple_lsh
	int   n,							// number of data points
	int   qn,							// number of query points
	int   d,							// dimension of space
	int   K,							// number of hash tables
	int   L,							// number of hash layers
	float S,
	float nn_ratio,						// approximation ratio for nn search
	const float **data,					// data set
	const float **query,				// query set
	const char  *truth_set,				// address of truth set
	const char  *output_folder) 		// output folder
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
	lsh->build(n, d, K, L, S, nn_ratio, data);

	gettimeofday(&end_time, NULL);
	float indexing_time = end_time.tv_sec - start_time.tv_sec + 
		(end_time.tv_usec - start_time.tv_usec) / 1000000.0f;
	printf("Indexing Time: %f Seconds\n\n", indexing_time);

	// -------------------------------------------------------------------------
	//  c-AMIP search via Simple_LSH
	// -------------------------------------------------------------------------	
	char output_set[200];
	sprintf(output_set, "%ssimple_lsh.out", output_folder);

	FILE *fp = fopen(output_set, "a+");
	if (!fp)
	{
		printf("Could not create %s\n", output_set);
		return 1;
	}

	// Top-K result of interest
	int kMIPs[] = { 1, 2, 5, 10 };

	// max_round : size of kMIPs array
	int max_round = 4;
	int top_k = -1;

	float runtime = -1.0f;
	float overall_ratio = -1.0f;
	float recall = -1.0f;

	printf("Top-k c-AMIP of Simple_LSH: \n");
	printf("  Top-k\t\tRatio\t\tTime (ms)\tRecall\n");
	for (int num = 0; num < max_round; num++)
	{
		gettimeofday(&start_time, NULL);
		top_k = kMIPs[num];
		MaxK_List* list = new MaxK_List(top_k);

		overall_ratio = 0.0f;
		recall = 0.0f;
		for (int i = 0; i < qn; ++i)
		{
			list->reset();
			lsh->kmip(top_k, query[i], list);
			recall += calc_recall(top_k, (const Result *) R[i], list);
			
			float ratio = 0.0f;
			for (int j = 0; j < top_k; ++j)
			{
				ratio += list->ith_key(j) / R[i][j].key_;
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
	delete lsh; lsh = NULL;
	delete[] R; R = NULL;

	return 0;
}

// -----------------------------------------------------------------------------
int linear_scan(					// find top-k mip using linear_scan
	int   n,							// number of data points
	int   qn,							// number of query points
	int   d,							// dimension of space
	const float **data,					// data set
	const float **query,				// query set
	const char  *truth_set,				// address of truth set
	const char  *output_folder) 		// output folder
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

	int kMIPs[] = { 1, 2, 5, 10 };
	int max_round = 4;
	int top_k = -1;

	float runtime = -1.0f;
	float overall_ratio = -1.0f;
	float recall = -1.0f;

	printf("Top-k MIP of Linear Scan:\n");
	printf("  Top-k\t\tRatio\t\tTime (ms)\tRecall\n");
	for (int num = 0; num < max_round; num++) {
		gettimeofday(&start_time, NULL);
		top_k = kMIPs[num];
		MaxK_List* list = new MaxK_List(top_k);

		overall_ratio = 0.0f;
		recall = 0.0f;
		for (int i = 0; i < qn; ++i) {
			list->reset();
			for (int j = 0; j < n; ++j) {
				float ip = calc_inner_product(d, data[j], query[i]);
				list->insert(ip, j + 1);
			}
			recall += calc_recall(top_k, (const Result *) R[i], list);

			float ratio = 0.0f;
			for (int j = 0; j < top_k; ++j) {
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
int h2_alsh_precision_recall(		// precision recall curve of h2_alsh
	int   n,							// number of data points
	int   qn,							// number of query points
	int   d,							// dimension of space
	float nn_ratio,						// approximation ratio for nn search
	float mip_ratio,					// approximation ratio for mip search
	const float **data,					// data set
	const float **query,				// query set
	const char  *truth_set,				// address of truth set
	const char  *output_folder) 		// output folder
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
	//  indexing
	// -------------------------------------------------------------------------
	gettimeofday(&start_time, NULL);
	H2_ALSH *lsh = new H2_ALSH();
	lsh->build(n, d, nn_ratio, mip_ratio, data);

	gettimeofday(&end_time, NULL);
	float indexing_time = end_time.tv_sec - start_time.tv_sec + 
		(end_time.tv_usec - start_time.tv_usec) / 1000000.0f;
	printf("Indexing Time: %f Seconds\n\n", indexing_time);

	// -------------------------------------------------------------------------
	//  Precision Recall Curve of H2_ALSH
	// -------------------------------------------------------------------------	
	char output_set[200];
	sprintf(output_set, "%sh2_alsh_precision_recall.out", output_folder);

	FILE *fp = fopen(output_set, "a+");
	if (!fp) {
		printf("Could not create %s\n", output_set);
		return 1;
	}

	int tMIPs[] = { 1, 2, 5, 10 };
	int kMIPs[] = { 1, 2, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 200, 500, 1000 };
	int maxT_round = 4;
	int maxK_round = 16;

	float **pre    = new float*[maxT_round];
	float **recall = new float*[maxT_round];
	
	for (int t_round = 0; t_round < maxT_round; ++t_round) {
		pre[t_round]    = new float[maxK_round];
		recall[t_round] = new float[maxK_round];

		for (int k_round = 0; k_round < maxK_round; ++k_round) {
			pre[t_round][k_round]    = 0;
			recall[t_round][k_round] = 0;
		}
	}

	printf("Top-t c-AMIP of H2_ALSH: \n");
	for (int k_round = 0; k_round < maxK_round; ++k_round) {
		int top_k = kMIPs[k_round];
		MaxK_List* list = new MaxK_List(top_k);

		for (int i = 0; i < qn; ++i) {
			list->reset();
			lsh->kmip(top_k, query[i], list);

			for (int t_round = 0; t_round < maxT_round; ++t_round) {
				int top_t = tMIPs[t_round];
				int hits = get_hits(top_k, top_t, R[i], list);

				pre[t_round][k_round]    += hits / (float) top_k;
				recall[t_round][k_round] += hits / (float) top_t;
			}
		}
		delete list; list = NULL;
	}

	for (int t_round = 0; t_round < maxT_round; ++t_round) {
		int top_t = tMIPs[t_round];
		printf("Top-%d\t\tRecall\t\tPrecision\n", top_t);
		fprintf(fp, "Top-%d\tRecall\t\tPrecision\n", top_t);
		
		for (int k_round = 0; k_round < maxK_round; ++k_round) {
			int top_k = kMIPs[k_round];
			pre[t_round][k_round]    = pre[t_round][k_round]    * 100.0f / qn;
			recall[t_round][k_round] = recall[t_round][k_round] * 100.0f / qn;

			printf("%4d\t\t%.2f\t\t%.2f\n", top_k,
				recall[t_round][k_round], pre[t_round][k_round]);
			fprintf(fp, "%d\t%f\t%f\n", top_k,
				recall[t_round][k_round], pre[t_round][k_round]);
		}
		printf("\n");
		fprintf(fp, "\n");
	}
	printf("\n");
	fprintf(fp, "\n");
	fclose(fp);

	// -------------------------------------------------------------------------
	//  release space
	// -------------------------------------------------------------------------
	delete lsh; lsh = NULL;
	delete[] R; R = NULL;
	for (int i = 0; i < maxT_round; ++i) {
		delete[] pre[i];	pre[i] = NULL;
		delete[] recall[i];	recall[i] = NULL;
	}
	delete[] pre;	 pre = NULL;
	delete[] recall; recall = NULL;

	return 0;
}

// -----------------------------------------------------------------------------
int sign_alsh_precision_recall(		// precision recall curve of sign_alsh
	int   n,							// number of data points
	int   qn,							// number of query points
	int   d,							// dimension of space
	int   K,							// number of hash tables
	int   m,							// param of sign_alsh
	float U,							// param of sign_alsh
	float nn_ratio,						// approximation ratio for nn search
	const float **data,					// data set
	const float **query,				// query set
	const char  *truth_set,				// address of truth set
	const char  *output_folder) 		// output folder
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
	//  indexing
	// -------------------------------------------------------------------------
	gettimeofday(&start_time, NULL);
	Sign_ALSH *lsh = new Sign_ALSH();
	lsh->build(n, d, K, m, U, nn_ratio, data);

	gettimeofday(&end_time, NULL);
	float indexing_time = end_time.tv_sec - start_time.tv_sec + 
		(end_time.tv_usec - start_time.tv_usec) / 1000000.0f;
	printf("Indexing Time: %f Seconds\n\n", indexing_time);

	// -------------------------------------------------------------------------
	//  Precision Recall Curve of Sign-ALSH
	// -------------------------------------------------------------------------	
	char output_set[200];
	sprintf(output_set, "%ssign_alsh_precision_recall.out", output_folder);

	FILE *fp = fopen(output_set, "a+");
	if (!fp) {
		printf("Could not create %s\n", output_set);
		return 1;
	}

	int tMIPs[] = { 1, 2, 5, 10 };
	int kMIPs[] = { 1, 2, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 200, 500, 1000 };
	int maxT_round = 4;
	int maxK_round = 16;

	float **pre    = new float*[maxT_round];
	float **recall = new float*[maxT_round];
	
	for (int t_round = 0; t_round < maxT_round; ++t_round) {
		pre[t_round]    = new float[maxK_round];
		recall[t_round] = new float[maxK_round];

		for (int k_round = 0; k_round < maxK_round; ++k_round) {
			pre[t_round][k_round]    = 0;
			recall[t_round][k_round] = 0;
		}
	}

	printf("Top-t c-AMIP of Sign_ALSH: \n");
	for (int k_round = 0; k_round < maxK_round; ++k_round) {
		int top_k = kMIPs[k_round];
		MaxK_List* list = new MaxK_List(top_k);

		for (int i = 0; i < qn; ++i) {
			list->reset();
			lsh->kmip(top_k, query[i], list);

			for (int t_round = 0; t_round < maxT_round; ++t_round) {
				int top_t = tMIPs[t_round];
				int hits = get_hits(top_k, top_t, R[i], list);

				pre[t_round][k_round]    += hits / (float) top_k;
				recall[t_round][k_round] += hits / (float) top_t;
			}
		}
		delete list; list = NULL;
	}

	for (int t_round = 0; t_round < maxT_round; ++t_round) {
		int top_t = tMIPs[t_round];
		printf("Top-%d\t\tRecall\t\tPrecision\n", top_t);
		fprintf(fp, "Top-%d\tRecall\t\tPrecision\n", top_t);
		
		for (int k_round = 0; k_round < maxK_round; ++k_round) {
			int top_k = kMIPs[k_round];
			pre[t_round][k_round]    = pre[t_round][k_round]    * 100.0f / qn;
			recall[t_round][k_round] = recall[t_round][k_round] * 100.0f / qn;

			printf("%4d\t\t%.2f\t\t%.2f\n", top_k,
				recall[t_round][k_round], pre[t_round][k_round]);
			fprintf(fp, "%d\t%f\t%f\n", top_k,
				recall[t_round][k_round], pre[t_round][k_round]);
		}
		printf("\n");
		fprintf(fp, "\n");
	}
	printf("\n");
	fprintf(fp, "\n");
	fclose(fp);

	// -------------------------------------------------------------------------
	//  release space
	// -------------------------------------------------------------------------
	delete lsh; lsh = NULL;
	delete[] R; R = NULL;

	for (int i = 0; i < maxT_round; ++i) {
		delete[] pre[i];	pre[i] = NULL;
		delete[] recall[i];	recall[i] = NULL;
	}
	delete[] pre;	pre = NULL;
	delete[] recall;	recall = NULL;
	
	return 0;
}

// -----------------------------------------------------------------------------
int simple_lsh_precision_recall(	// precision recall curve of simple_lsh
	int   n,							// number of data points
	int   qn,							// number of query points
	int   d,							// dimension of space
	int   K,							// number of hash functions
	int   L,							// number of hash tables
	float  S,							// number of hash tables
	float nn_ratio,						// approximation ratio for nn search
	const float **data,					// data set
	const float **query,				// query set
	const char  *truth_set,				// address of truth set
	const char  *temp_result,			// address to store temporary output from different onion layers
	const char  *output_folder) 		// output folder
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
	lsh->build(n, d, K, L, S, nn_ratio, data);

	gettimeofday(&end_time, NULL);
	float indexing_time = end_time.tv_sec - start_time.tv_sec + 
		(end_time.tv_usec - start_time.tv_usec) / 1000000.0f;
	printf("Indexing Time: %f Seconds\n\n", indexing_time);

	// -------------------------------------------------------------------------
	//  Precision Recall Curve of Simple_LSH
	// -------------------------------------------------------------------------	
	char output_set[200];
	sprintf(output_set, "%ssimple_lsh_precision_recall.out", output_folder);

	FILE *fp = fopen(output_set, "a+");
	if (!fp)
	{
		printf("Could not create %s\n", output_set);
		return 1;
	}

	int tMIPs[] = { 1, 2, 5, 10 };
	//int kMIPs[] = { 1, 2, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 200, 500, 1000 };
	int kMIPs[] = { 1, 2, 5, 10, 20};
	int maxT_round = 4;
	int maxK_round = 5;

	float **pre    = new float*[maxT_round];
	float **recall = new float*[maxT_round];
	
	for (int t_round = 0; t_round < maxT_round; ++t_round)
	{
		pre[t_round]    = new float[maxK_round];
		recall[t_round] = new float[maxK_round];

		for (int k_round = 0; k_round < maxK_round; ++k_round)
		{
			pre[t_round][k_round]    = 0;
			recall[t_round][k_round] = 0;
		}
	}

	printf("Top-t c-AMIP of Simple_LSH: \n");
	for (int k_round = 0; k_round < maxK_round; ++k_round)
	{
		int top_k = kMIPs[k_round];
		MaxK_List* list = new MaxK_List(top_k);
		for (int i = 0; i < qn; ++i)
		{
			list->reset();
			lsh->kmip(top_k, query[i], list);

			// persist on file to compute overall performance
			char output_set[200];
			sprintf(output_set, "%s_top_%d.txt", temp_result, top_k);

			persist_intermediate_on_file(top_k, d, list, data, output_set);
			for (int t_round = 0; t_round < maxT_round; ++t_round)
			{
				int top_t = tMIPs[t_round];
				int hits = get_hits(top_k, top_t, R[i], list);

				pre[t_round][k_round]    += hits / (float) top_k;
				recall[t_round][k_round] += hits / (float) top_t;
			}
		}
		delete list;
		list = NULL;
	}

	for (int t_round = 0; t_round < maxT_round; ++t_round)
	{
		int top_t = tMIPs[t_round];
		printf("Top-%d\t\tRecall\t\tPrecision\n", top_t);
		fprintf(fp, "Top-%d\tRecall\t\tPrecision\n", top_t);
		
		for (int k_round = 0; k_round < maxK_round; ++k_round)
		{
			int top_k = kMIPs[k_round];
			pre[t_round][k_round]    = pre[t_round][k_round]    * 100.0f / qn;
			recall[t_round][k_round] = recall[t_round][k_round] * 100.0f / qn;

			printf("%4d\t\t%.2f\t\t%.2f\n", top_k,
				recall[t_round][k_round], pre[t_round][k_round]);
			fprintf(fp, "%d\t%f\t%f\n", top_k,
				recall[t_round][k_round], pre[t_round][k_round]);
		}
		printf("\n");
		fprintf(fp, "\n");
	}
	printf("\n");
	fprintf(fp, "\n");
	fclose(fp);

	// -------------------------------------------------------------------------
	//  release space
	// -------------------------------------------------------------------------
	delete lsh; lsh = NULL;
	delete[] R; R = NULL;
	for (int i = 0; i < maxT_round; ++i) {
		delete[] pre[i];	pre[i] = NULL;
		delete[] recall[i];	recall[i] = NULL;
	}
	delete[] pre;	 pre = NULL;
	delete[] recall; recall = NULL;

	return 0;
}

// -----------------------------------------------------------------------------
int norm_distribution(				// analyse norm distribution of data
	int   n,							// number of data points
	int   d,							// dimension of space
	const float **data,					// data set
	const char  *output_folder) 		// output folder
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
int persist_intermediate_on_file(		// persist intermediate result per query per onion layer on file, for aggregation
	int   topk, 						// topk results of interest
	int   d,							// dimension of space
	MaxK_List* list,					// list that contains the topk result per query per onion layer
	const float **data,					// data set
	const char  *output_folder)			// output folder
{
	FILE *fp = fopen(output_folder, "a+");
	if (!fp)
	{
		printf("Could not create %s\n", output_folder);
		return 1;
	}

	for(int i = 0; i < list->size(); i++)
	{
		int current_data_idx = list->ith_id(i) - 1;
		if(current_data_idx < 0 )
		{
			for(int j = 0; j < d; j++)
			{
				fprintf(fp, "%f\t", -1.0f);

			}
			fprintf(fp, "%f\n", -100.0f);	// flush the similarity value to file
		}
		else
		{
			float temp_value = list->ith_key(i);
			for(int j = 0; j < d; j++)
			{
				fprintf(fp, "%f\t", data[current_data_idx][j]);
			}
			fprintf(fp, "%f\n", list->ith_key(i));	// flush the similarity value to file
		}
	}
	fclose(fp);

	return 0;
}


/*
// -----------------------------------------------------------------------------
int overall_performance(				// output the overall performance of indexing
		int   d,							// dimension of space
		int   qn, 							// number of queries
		int   layers,						// number of onion layers
		const char  *temp_output_folder,	// temporal output
		const char  *ground_truth_folder,	// ground truth folder
		const char  *output_folder)			// output folder
{
	MAX_DIMENSION = d;
	int tMIPs[] = { 1, 2, 5, 10 };
	int kMIPs[] = { 1, 2, 5, 10, 20};
	int maxT_round = 4;
	int maxK_round = 5;

	// -------------------------------------------------------------------------
	//  read all candidates per query per onion layer and sort
	// -------------------------------------------------------------------------
	// float** temp_result = new float*[kMIPs[maxK_round - 1]*layers*qn];
	float*** temp_result = new float**[qn];
	for(int i = 0; i < qn; i++)
	{
		temp_result[i] = new float*[kMIPs[maxK_round - 1]*layers];
		for(int j=0; j<kMIPs[maxK_round - 1]*layers; j++)
		{
			temp_result[i][j] = new float[d+1];
		}
	}

	FILE *fp1 = fopen(temp_output_folder, "r");
	if (!fp1)
	{
		printf("Could not open %s\n", temp_output_folder);
		return 1;
	}

	// temp_result dimension: d+1, last dimension is the similarity score
	int line_count   = 0;
	int cur_q_line_count = 0;
	int q_index = 0;
	int layer_index = 0;
	while (!feof(fp1) && line_count < kMIPs[maxK_round - 1]*layers*qn)
	{
		if(line_count%(kMIPs[maxK_round - 1]) == 0 && line_count > 0)
		{
			q_index = (++q_index)%qn;
			cur_q_line_count = 0;
			if(line_count%(kMIPs[maxK_round - 1]*qn) == 0)
			{
				++layer_index;
			}
		}
		for (int j = 0; j < d + 1; ++j)
		{
			fscanf(fp1, " %f", &temp_result[q_index][cur_q_line_count + layer_index * kMIPs[maxK_round - 1]][j]);
		}
		fscanf(fp1, "\n");

		++line_count;
		++cur_q_line_count;

	}
	assert(feof(fp1) && line_count == kMIPs[maxK_round - 1]*layers*qn);
	fclose(fp1);

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

	// sort based on the last dimension of temp_result as the output of topk from each layer
	for(int i = 0; i < qn; i++)
	{
		qsort(temp_result[i], kMIPs[maxK_round - 1]*layers, sizeof(*temp_result[i]), my_sort_col);
		for(int j=0; j<20; j++)
		{
			for(int k=0; k < d + 1; k++)
			{
				printf("%f ", temp_result[i][j][k]);
			}
			printf("\n");
		}
	}

	printf("Output path %s \n. ", output_folder);
	FILE *fp2 = fopen(output_folder, "a+");
	if (!fp2)
	{
		printf("Could not open %s\n", output_folder);
		return 1;
	}

	// -------------------------------------------------------------------------
	//  compute precision and recall per query
	// -------------------------------------------------------------------------
	float **pre    = new float*[maxT_round];
	float **recall = new float*[maxT_round];

	for (int t_round = 0; t_round < maxT_round; ++t_round)
	{
		pre[t_round]    = new float[maxK_round];
		recall[t_round] = new float[maxK_round];

		for (int k_round = 0; k_round < maxK_round; ++k_round)
		{
			pre[t_round][k_round]    = 0;
			recall[t_round][k_round] = 0;
		}
	}

	printf("Top-t c-AMIP of Simple_LSH (overall): \n");
	for (int k_round = 0; k_round < maxK_round; ++k_round)
	{
		int top_k = kMIPs[k_round];
		MaxK_List* list = new MaxK_List(top_k);
		for (int i = 0; i < qn; ++i)
		{
			list->reset();

			// initialize list
			for(int j = 0; j < top_k; j++)
			{
				// key: j, value: temp_result[i][j][d];
				list->insert(temp_result[i][j][d], j + 1);
			}

			for (int t_round = 0; t_round < maxT_round; ++t_round)
			{
				int top_t = tMIPs[t_round];
				int hits = get_hits(top_k, top_t, R[i], list);

				pre[t_round][k_round]    += hits / (float) top_k;
				recall[t_round][k_round] += hits / (float) top_t;
			}
		}
		delete list;
		list = NULL;
	}

	for (int t_round = 0; t_round < maxT_round; ++t_round)
	{
		int top_t = tMIPs[t_round];
		printf("Top-%d\t\tRecall\t\tPrecision\n", top_t);
		fprintf(fp2, "Top-%d\tRecall\t\tPrecision\n", top_t);

		for (int k_round = 0; k_round < maxK_round; ++k_round)
		{
			int top_k = kMIPs[k_round];
			pre[t_round][k_round]    = pre[t_round][k_round]    * 100.0f / qn;
			recall[t_round][k_round] = recall[t_round][k_round] * 100.0f / qn;

			printf("%4d\t\t%.2f\t\t%.2f\n", top_k,
					recall[t_round][k_round], pre[t_round][k_round]);
			fprintf(fp2, "%d\t%f\t%f\n", top_k,
					recall[t_round][k_round], pre[t_round][k_round]);
		}
		printf("\n");
		fprintf(fp2, "\n");
	}
	printf("\n");
	fprintf(fp2, "\n");
	fclose(fp2);


	/////////////////////////////////////////////
	// -------------------------------------------------------------------------
	//  free memory space
	// -------------------------------------------------------------------------
	for(int i = 0; i < qn; i++)
	{
		for(int j = 0; j < kMIPs[maxK_round - 1]*layers; j++)
		{
			delete[] temp_result[i][j];
			temp_result[i][j] = NULL;
		}
		delete[] temp_result[i];
		temp_result[i] = NULL;
	}
	delete[] temp_result;
	temp_result = NULL;

	delete[] R; R = NULL;
	for (int i = 0; i < maxT_round; ++i) {
		delete[] pre[i];	pre[i] = NULL;
		delete[] recall[i];	recall[i] = NULL;
	}
	delete[] pre;	 pre = NULL;
	delete[] recall; recall = NULL;

	return 0;
}
*/

// -------------------------------------------------------------------------
//  read all candidates per top_k, per query per onion layer
// -------------------------------------------------------------------------
int overall_performance(				// output the overall performance of indexing
		int   d,							// dimension of space
		int   qn, 							// number of queries
		int   layers,						// number of onion layers
		const char  *temp_output_folder,	// temporal output
		const char  *ground_truth_folder,	// ground truth folder
		const char  *output_folder)			// output folder
{
	MAX_DIMENSION = d;
	int tMIPs[] = { 1, 2, 5, 10 };
	int kMIPs[] = { 1, 2, 5, 10, 20};
	int maxT_round = 4;
	int maxK_round = 5;

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

	// -------------------------------------------------------------------------
	//  compute precision and recall per query
	// -------------------------------------------------------------------------
	float **pre    = new float*[maxT_round];
	float **recall = new float*[maxT_round];

	for (int t_round = 0; t_round < maxT_round; ++t_round)
	{
		pre[t_round]    = new float[maxK_round];
		recall[t_round] = new float[maxK_round];

		for (int k_round = 0; k_round < maxK_round; ++k_round)
		{
			pre[t_round][k_round]    = 0;
			recall[t_round][k_round] = 0;
		}
	}

	printf("Top-t c-AMIP of Simple_LSH (overall): \n");

	for (int k_round = 0; k_round < maxK_round; ++k_round)
	{
		int top_k = kMIPs[k_round];
		char output_set[200];
		sprintf(output_set, "%s_top_%d.txt", temp_output_folder, top_k);

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
		float*** temp_result = new float**[qn];
		for(int i = 0; i < qn; i++)
		{
			temp_result[i] = new float*[top_k * layers];
			for(int j=0; j< top_k * layers; j++)
			{
				temp_result[i][j] = new float[d+1];
			}
		}

		int q_index = 0;
		int layer_index = 0;
		int cur_q_line_count = 0;
		int line_count = 0;
		while (!feof(fp1) && line_count < top_k * layers * qn)
		{
			if(line_count%top_k == 0 && line_count > 0)
			{
				q_index = (++q_index)%qn;
				cur_q_line_count = 0;
				if(line_count%(top_k * qn) == 0)
				{
					++layer_index;
				}
			}
			for (int j = 0; j < d + 1; ++j)
			{
				fscanf(fp1, " %f", &temp_result[q_index][cur_q_line_count + layer_index * top_k][j]);
			}
			fscanf(fp1, "\n");
			++line_count;
			++cur_q_line_count;

		}
		printf("top_k: %d, layers: %d, qn: %d, line_count: %d .\n", top_k, layers, qn, line_count);
		assert(feof(fp1) && line_count == top_k * layers * qn);

		MaxK_List* list = new MaxK_List(top_k);
		for (int i = 0; i < qn; ++i)
		{
			list->reset();
			for(int j = 0; j < top_k * layers; j++)
			{
				list->insert(temp_result[i][j][d], j + 1);
			}

			for (int t_round = 0; t_round < maxT_round; ++t_round)
			{
				int top_t = tMIPs[t_round];
				int hits = get_hits(top_k, top_t, R[i], list);

				pre[t_round][k_round]    += hits / (float) top_k;
				recall[t_round][k_round] += hits / (float) top_t;
			}
		}
		delete list;
		list = NULL;
		fclose(fp1);

		// -------------------------------------------------------------------------
		//  free memory space
		// -------------------------------------------------------------------------
		for(int i = 0; i < qn; i++)
		{
			for(int j = 0; j < top_k * layers; j++)
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

	printf("Output path %s \n ", output_folder);
	FILE *fp2 = fopen(output_folder, "a+");
	if (!fp2)
	{
		printf("Could not open %s\n", output_folder);
		return 1;
	}
	for (int t_round = 0; t_round < maxT_round; ++t_round)
	{
		int top_t = tMIPs[t_round];
		printf("Top-%d\t\tRecall\t\tPrecision\n", top_t);
		fprintf(fp2, "Top-%d\tRecall\t\tPrecision\n", top_t);

		for (int k_round = 0; k_round < maxK_round; ++k_round)
		{
			int top_k = kMIPs[k_round];
			pre[t_round][k_round]    = pre[t_round][k_round]    * 100.0f / qn;
			recall[t_round][k_round] = recall[t_round][k_round] * 100.0f / qn;

			printf("%4d\t\t%.2f\t\t%.2f\n", top_k,
					recall[t_round][k_round], pre[t_round][k_round]);
			fprintf(fp2, "%d\t%f\t%f\n", top_k,
					recall[t_round][k_round], pre[t_round][k_round]);
		}
		printf("\n");
		fprintf(fp2, "\n");
	}
	printf("\n");
	fprintf(fp2, "\n");
	fclose(fp2);

	delete[] R; R = NULL;
	for (int i = 0; i < maxT_round; ++i) {
		delete[] pre[i];	pre[i] = NULL;
		delete[] recall[i];	recall[i] = NULL;
	}
	delete[] pre;	 pre = NULL;
	delete[] recall; recall = NULL;

	return 0;
}

// -----------------------------------------------------------------------------
int my_sort_col(const void *pa, const void *pb )
{
	const int *a = *(const int **)pa;
	const int *b = *(const int **)pb;
	return (a[MAX_DIMENSION] < b[MAX_DIMENSION]) - (a[MAX_DIMENSION] > b[MAX_DIMENSION]);
}


