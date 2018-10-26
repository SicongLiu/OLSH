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
int h2_alsh(                        // mip search via h2_alsh
            int   n,                            // number of data points
            int   qn,                            // number of query points
            int   d,                            // dimension of space
            float nn_ratio,                        // approximation ratio for nn search
            float mip_ratio,                    // approximation ratio for mip search
            const float **data,                    // data set
            const float **query,                // query set
            const char  *truth_set,                // address of truth set
            const char  *output_folder)            // output folder
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
int l2_alsh(                        // mip search via l2_alsh
            int   n,                            // number of data points
            int   qn,                            // number of query points
            int   d,                            // dimension of space
            int   m,                            // param of l2_alsh
            float U,                            // param of l2_alsh
            float nn_ratio,                        // approximation ratio for nn search
            const float **data,                    // data set
            const float **query,                // query set
            const char  *truth_set,                // address of truth set
            const char  *output_folder)         // output folder
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
int l2_alsh2(                        // mip search via l2_alsh2
             int   n,                            // number of data points
             int   qn,                            // number of query points
             int   d,                            // dimension of space
             int   m,                            // param of l2_alsh2
             float U,                            // param of l2_alsh2
             float nn_ratio,                        // approximation ratio for nn search
             const float **data,                    // data set
             const float **query,                // query set
             const char  *truth_set,                // address of truth set
             const char  *output_folder)         // output folder
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
int xbox(                            // mip search via xbox
         int   n,                            // number of data points
         int   qn,                            // number of query points
         int   d,                            // dimension of space
         float nn_ratio,                        // approximation ratio for nn search
         const float **data,                    // data set
         const float **query,                // query set
         const char  *truth_set,                // address of truth set
         const char  *output_folder)         // output folder
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
int sign_alsh(                        // mip search via sign_alsh
              int   n,                            // number of data points
              int   qn,                            // number of query points
              int   d,                            // dimension of space
              int   K,                            // number of hash tables
              int   m,                            // param of sign_alsh
              float U,                            // param of sign_alsh
              float nn_ratio,                        // approximation ratio for nn search
              const float **data,                    // data set
              const float **query,                // query set
              const char  *truth_set,                // address of truth set
              const char  *output_folder)         // output folder
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
/*int simple_lsh(                        // mip search via simple_lsh
 int   n,                            // number of data points
 int   qn,                            // number of query points
 int   d,                            // dimension of space
 int   K,                            // number of hash tables
 int   L,                            // number of hash layers
 float S,
 float nn_ratio,                        // approximation ratio for nn search
 const float **data,                    // data set
 const float **query,                // query set
 const char  *truth_set,                // address of truth set
 const char  *output_folder)         // output folder
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
 */

// -----------------------------------------------------------------------------
int linear_scan(                    // find top-k mip using linear_scan
                int   n,                            // number of data points
                int   qn,                            // number of query points
                int   d,                            // dimension of space
                const float **data,                    // data set
                const float **query,                // query set
                const char  *truth_set,                // address of truth set
                const char  *output_folder)         // output folder
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
int h2_alsh_precision_recall(        // precision recall curve of h2_alsh
                             int   n,                            // number of data points
                             int   qn,                            // number of query points
                             int   d,                            // dimension of space
                             float nn_ratio,                        // approximation ratio for nn search
                             float mip_ratio,                    // approximation ratio for mip search
                             const float **data,                    // data set
                             const float **query,                // query set
                             const char  *truth_set,                // address of truth set
                             const char  *output_folder)         // output folder
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
        delete[] pre[i];    pre[i] = NULL;
        delete[] recall[i];    recall[i] = NULL;
    }
    delete[] pre;     pre = NULL;
    delete[] recall; recall = NULL;

    return 0;
}

// -----------------------------------------------------------------------------
int sign_alsh_precision_recall(        // precision recall curve of sign_alsh
                               int   n,                            // number of data points
                               int   qn,                            // number of query points
                               int   d,                            // dimension of space
                               int   K,                            // number of hash tables
                               int   m,                            // param of sign_alsh
                               float U,                            // param of sign_alsh
                               float nn_ratio,                        // approximation ratio for nn search
                               const float **data,                    // data set
                               const float **query,                // query set
                               const char  *truth_set,                // address of truth set
                               const char  *output_folder)         // output folder
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
        delete[] pre[i];    pre[i] = NULL;
        delete[] recall[i];    recall[i] = NULL;
    }
    delete[] pre;    pre = NULL;
    delete[] recall;    recall = NULL;

    return 0;
}

/*
 // -----------------------------------------------------------------------------
 int simple_lsh_precision_recall(    // precision recall curve of simple_lsh
 int   n,                            // number of data points
 int   qn,                            // number of query points
 int   d,                            // dimension of space
 int   K,                            // number of hash functions
 int   L,                            // number of hash tables
 float  S,                            // number of hash tables
 float nn_ratio,                        // approximation ratio for nn search
 const float **data,                    // data set
 const float **query,                // query set
 const char  *truth_set,                // address of truth set
 const char  *temp_result,            // address to store temporary output from different onion layers
 const char  *output_folder)         // output folder
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

 float candidate_size = 0.0f;
 for (int i = 0; i < qn; ++i)
 {
 list->reset();
 candidate_size +=lsh->kmip(top_k, query[i], list);

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
 delete[] pre[i];    pre[i] = NULL;
 delete[] recall[i];    recall[i] = NULL;
 }
 delete[] pre;     pre = NULL;
 delete[] recall; recall = NULL;

 return 0;
 }
 */

// -----------------------------------------------------------------------------
int simple_lsh_recall(    // precision recall curve of simple_lsh
                      int   n,                            // number of data points
                      int   qn,                            // number of query points
                      int   d,                            // dimension of space
                      int   K,                            // number of hash functions
                      int   L,                            // number of hash tables
                      int       layer_index,                 // the index of current onion layer
                      float  S,                            // number of hash tables
                      float nn_ratio,                        // approximation ratio for nn search
                      const float **data,                    // data set
                      const float **query,                // query set
                      const char  *truth_set,                // address of truth set
                      const char  *temp_result,            // address to store temporary output from different onion layers
                      const char  *sim_angle,            // address to store sim-angle from different layers
                      const char  *output_folder)         // output folder
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
     int threshold_conditions = 2;
     bool use_threshold_pruning[] = {true, false};
     string str_array[] = {"with_threshold", "without_threshold"};

     /*
    int threshold_conditions = 1;
    bool use_threshold_pruning[] = {false};
    string str_array[] = {"without_threshold"};
	*/

    // top-25
    int kMIPs[] = { 1, 2, 5, 10, 25};
    int max_round = 5;

    // top-50
    // int kMIPs[] = { 1, 2, 5, 10, 25, 50};
    // int max_round = 6;


    for(int ii = 0; ii < threshold_conditions; ii++)
    {
        int top_k = -1;
        vector<float>* temp_sim_angle_vec = new vector<float>[qn];

        bool is_threshold = use_threshold_pruning[ii];
        string is_threshold_file_name = str_array[ii];

        char output_set[200];
        sprintf(output_set, "%ssimple_lsh_recall_%s.out", output_folder, is_threshold_file_name.c_str());

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

        printf("Top-k c-AMIP of Simple_LSH: \n");
        printf("  Top-k\t\tTime (ms)\tRecall\n");

        for (int num = 0; num < max_round; num++)
        {
        		int total_hash_hits = 0;
            gettimeofday(&start_time, NULL);
            float file_processing_time = 0.0f;

            top_k = kMIPs[num];
            if(top_k < layer_index)
            {
                continue;
            }
            MaxK_List* list = new MaxK_List(top_k);

            recall = 0.0f;
            candidate_size = 0.0f;

            for (int i = 0; i < qn; ++i)
            {
            		int current_hash_hits = 0;
                list->reset();

                // top-k computation with threshold from previous layers
                candidate_size += lsh->kmip(top_k, query[i], list, temp_sim_angle_vec[i][num], is_threshold, current_hash_hits);
                recall += calc_recall(top_k, (const Result *) R[i], list);
                total_hash_hits += current_hash_hits;
                // printf("query index: %d, round: %d, using threshold? -- %d, candidate size: %f .\n", i, num, is_threshold, candidate_size);

                // persist on file to compute overall performance
                char output_set[200];
                // sprintf(output_set, "%s_top_%d.txt", temp_result, top_k);
                sprintf(output_set, "%s_top_%d_%s.txt", temp_result, top_k, is_threshold_file_name.c_str());

                timeval file_start_time, file_end_time;
                gettimeofday(&file_start_time, NULL);
                persist_intermediate_on_file(top_k, d, list, data, output_set);
                gettimeofday(&file_end_time, NULL);

                file_processing_time += file_end_time.tv_sec - file_start_time.tv_sec + (file_end_time.tv_usec -
                                                                                         file_start_time.tv_usec) / 1000000.0f;
            }
            delete list; list = NULL;

            gettimeofday(&end_time, NULL);
            runtime = end_time.tv_sec - start_time.tv_sec + (end_time.tv_usec -
                                                             start_time.tv_usec) / 1000000.0f;
            runtime = runtime - file_processing_time;
            pair<int, float > dict_time(top_k, runtime);
            my_run_time.insert(dict_time);

            candidate_size = candidate_size * 1.0f / qn;
            pair<int, float > dict_candidate(top_k, candidate_size);
            average_candidate_size.insert(dict_candidate);
            recall        = recall / qn;
            runtime       = (runtime * 1000.0f) / qn;

            printf("  %3d\t\t%.4f\t\t%.2f\n", top_k, runtime, recall);
            fprintf(fp, "%d\t%f\t%f\n", top_k, runtime, recall);
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
        sprintf(temp_result_set, "%s_%s", temp_result, is_threshold_file_name.c_str());
        persist_candidate_size(average_candidate_size, temp_result_set, my_run_time);

        printf("\n");
        fprintf(fp, "\n");
        fclose(fp);

        // clear vector
        for(int jj = 0; jj < qn; jj++)
        {
            vector<float>().swap(temp_sim_angle_vec[jj]);
        }
        // delete temp_sim_angle_vec; temp_sim_angle_vec = NULL;

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
int persist_intermediate_on_file(        // persist intermediate result per query per onion layer on file, for aggregation
                                 int   topk,                         // topk results of interest
                                 int   d,                            // dimension of space
                                 MaxK_List* list,                    // list that contains the topk result per query per onion layer
                                 const float **data,                    // data set
                                 const char  *output_folder)            // output folder
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
            fprintf(fp, "%f\n", -100.0f);    // flush the similarity value to file
        }
        else
        {
            float temp_value = list->ith_key(i);
            for(int j = 0; j < d; j++)
            {
                fprintf(fp, "%f\t", data[current_data_idx][j]);
            }
            fprintf(fp, "%f\n", list->ith_key(i));    // flush the similarity value to file
        }
    }
    fclose(fp);

    return 0;
}

// -----------------------------------------------------------------------------
int persist_candidate_size(                // persist average number of candidate on file, regarding to a specific topk
                           unordered_map<int, float> mymap,     // average value of candidate size
                           const char  *output_folder,            // output folder
                           unordered_map<int, float> my_run_time)            // run time of different top-k
{
    int run_time_index = 0;
    for ( auto it = mymap.begin(); it != mymap.end(); ++it )
    {
        int top_k_key = (int)it->first;
        float element_count = (float)it->second;
        float run_time =  my_run_time[(int)it->first];
        char output_set[200];
        sprintf(output_set, "%s_top_%d_candidate_size.txt", output_folder, top_k_key);
        FILE *fp = fopen(output_set, "a+");
        if (!fp)
        {
            printf("Could not create %s\n", output_set);
            return 1;
        }
        fprintf(fp, "%f, %f\n", element_count, run_time);

        fclose(fp);
    }
    return 0;
}

// -------------------------------------------------------------------------
//  read all candidates per top_k, per query per onion layer
// -------------------------------------------------------------------------
int overall_performance(                        // output the overall performance of indexing
                        int   d,                                // dimension of space
                        int   qn,                             // number of queries
                        int   layers,                        // number of onion layers
                        const char  *temp_output_folder,        // temporal output
                        const char  *ground_truth_folder,    // ground truth folder
                        const char  *output_folder)            // output folder
{
    MAX_DIMENSION = d;


     int threshold_conditions = 2;
     bool use_threshold_pruning[] = {true, false};
     string str_array[] = {"with_threshold", "without_threshold"};


    /*int threshold_conditions = 1;
    bool use_threshold_pruning[] = {true};
    string str_array[] = {"_with_threshold"};
    */

    // top-25
    int kMIPs[] = { 1, 2, 5, 10, 25};
    int max_round = 5;

    // top-50
    // int kMIPs[] = { 1, 2, 5, 10, 25, 50};
    // int max_round = 6;

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
        for (int round = 0; round < max_round; ++round)
        {
            recall[round] = 0;
            NDCG[round] = 0;
        }

        printf("Top-t c-AMIP of Simple_LSH (overall): \n");

        for (int round = 0; round < max_round; ++round)
        {
            int top_k = kMIPs[round];
            if(top_k > layers)
            {
                break;
            }
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
            float*** temp_result = new float**[qn];
            for(int i = 0; i < qn; i++)
            {
                temp_result[i] = new float*[top_k * top_k];
                for(int j=0; j< top_k * top_k; j++)
                {
                    temp_result[i][j] = new float[d+1];
                }
            }

            int q_index = 0;
            int layer_index = 0;
            int cur_q_line_count = 0;
            int line_count = 0;
            // while (!feof(fp1) && line_count < top_k * layers * qn)
            while (!feof(fp1) && line_count < top_k * top_k * qn)
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
            // assert(feof(fp1) && line_count == top_k * layers * qn);
            assert(feof(fp1) && line_count == top_k * top_k * qn);

            MaxK_List* list = new MaxK_List(top_k);
            for (int i = 0; i < qn; ++i)
            {
                list->reset();
                for(int j = 0; j < top_k * top_k; j++)
                {
                    list->insert(temp_result[i][j][d], j + 1);
                }

                recall[round] += calc_recall(top_k, (const Result *) R[i], list);
                NDCG[round] += calc_NDCG(top_k, (const Result *) R[i], list);
            }
            delete list;
            list = NULL;
            fclose(fp1);

            // -------------------------------------------------------------------------
            //  free memory space
            // -------------------------------------------------------------------------
            for(int i = 0; i < qn; i++)
            {
                for(int j = 0; j < top_k * top_k; j++)
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

        char output_folder_set[200];
        // sprintf(output_folder_set, "%s_top_%d%s.txt", temp_output_folder, top_k, is_threshold_file_name.c_str());
        sprintf(output_folder_set, "%s_%s.txt", output_folder, is_threshold_file_name.c_str());

        printf("Output path %s \n ", output_folder_set);
        FILE *fp2 = fopen(output_folder_set, "a+");
        if (!fp2)
        {
            printf("Could not open %s\n", output_folder_set);
            return 1;
        }
        printf("Top-k\t\tRecall\tNDCG\n");
        fprintf(fp2, "Top-k\t\tRecall\tNDCG\n");
        for (int round = 0; round < max_round; ++round)
        {
            int top_k = kMIPs[round];
            recall[round] = recall[round] / qn;
            NDCG[round] = NDCG[round] * 1.0f / qn;
            printf("%4d\t\t%.2f\t%.2f\n", top_k,
                   recall[round], NDCG[round]);
            fprintf(fp2, "%d\t%f\t%f\n", top_k,
                    recall[round], NDCG[round]);
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


