
// Test.cpp
//
// This is a direct port of the C version of the RTree test program.
//

#include <iostream>
#include <algorithm>
#include <vector>
#include <sys/time.h>

#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <cstring>
#include <unistd.h>
#include <ios>
//#include <iostream>
#include <fstream>
//#include <string>


#include "max_list.h"
#include "RTree.h"
#include "gendef.h"



using namespace std;

typedef float ValueType;


struct TempRect
{
	int dim;
	float* min;
	float* max;
	TempRect(int dim_, float* data)
	{
		dim = dim_;
		// min = (float*) malloc (dim);
		// max = (float*) malloc (dim);
		min = new float[dim];
		max = new float[dim];
		for(int i= 0; i < dim; i++)
		{
			min[i] = data[i];
			max[i] = data[i];
		}
	}
	~TempRect()
	{
		//		free (min);
		//		free (max);
		delete[] min;
		delete[] max;
		min = NULL;
		max = NULL;
	}
};


struct Rect
{
	Rect()  {}

	Rect(int a_minX, int a_minY, int a_maxX, int a_maxY)
	{
		min[0] = a_minX;
		min[1] = a_minY;

		max[0] = a_maxX;
		max[1] = a_maxY;
	}


	int min[2];
	int max[2];
};

struct Rect rects[] =
{
		Rect(0, 0, 2, 2), // xmin, ymin, xmax, ymax (for 2 dimensional RTree)
		Rect(5, 5, 7, 7),
		Rect(8, 5, 9, 6),
		Rect(7, 1, 9, 2),
};

void checkpoint(int   k,	const Result *R, vector<float> myvector)
{
	int i = k - 1;
	int last = k - 1;
	cout<<"vector size: "<<myvector.size()<<", comparing ground truth: " << R[last].key_;
	for(int i = myvector.size() - 1; i >=0 ; i--)
	{
		cout<<", value: "<<myvector.at(i);
	}
	cout<<endl;
}

float calc_recall(					// calc recall (percentage)
		int   k,							// top-k value
		const Result *R,					// ground truth results
		vector<float> myvector)					// results returned by algorithms
{
	int i = k - 1;
	int last = k - 1;
	while (i >= 0 && R[last].key_ - myvector.at(i) > FLOATZERO) {
		i--;
	}
	return (i + 1) * 100.0f / k;
}


int nrects = sizeof(rects) / sizeof(rects[0]);



bool MySearchCallback(ValueType id)
{
	cout << "Hit data rect " << id << "\n";
	return true; // keep going
}


int read_ground_truth(				// read ground truth results from disk
		int qn,								// number of query objects
		const char *fname,					// address of truth set
		Result **R,
		int MAXK)							// ground truth results (return)
{
	FILE *fp = fopen(fname, "r");
	if (!fp)
	{
		printf("Could not open %s\n", fname);
		return 1;
	}

	int tmp1 = -1;
	int tmp2 = -1;
	fscanf(fp, "%d %d\n", &tmp1, &tmp2);
	assert(tmp1 == qn && tmp2 == MAXK);
	for (int i = 0; i < qn; ++i)
	{
		for (int j = 0; j < MAXK; ++j)
		{
			fscanf(fp, "%d %f ", &R[i][j].id_, &R[i][j].key_);
		}
		fscanf(fp, "\n");
	}
	fclose(fp);

	return 0;
}



int read_data(	const char *fname, float **data, int d, int n)
{
	FILE *fp = fopen(fname, "r");
	if (!fp)
	{
		printf("Could not open %s\n", fname);
		return 1;
	}

	int num_dim = -1;
	int num_element = -1;
	fscanf(fp, "%d\n", &num_dim);
	fscanf(fp, "%d\n", &num_element);

	assert(num_dim == d);
	assert(num_element == n);

	int i   = 0;
	while (!feof(fp) && i < n)
	{
		for (int j = 0; j < d; ++j)
		{
			fscanf(fp, " %f", &data[i][j]);
		}
		fscanf(fp, "\n");

		++i;
	}
	assert(feof(fp) && i == n);
	fclose(fp);

	return 0;
}


TempRect pack_data(float* data, int dim)
{
	return TempRect(dim, data);
}

//
//long output_mem_usage()
//{
//   vm_size_t page_size;
//    mach_port_t mach_port;
//    mach_msg_type_number_t count;
//    vm_statistics64_data_t vm_stats;
//
//    mach_port = mach_host_self();
//    count = sizeof(vm_stats) / sizeof(natural_t);
//    if (KERN_SUCCESS == host_page_size(mach_port, &page_size) &&
//        KERN_SUCCESS == host_statistics64(mach_port, HOST_VM_INFO,
//                                        (host_info64_t)&vm_stats, &count))
//    {
//        long long free_memory = (int64_t)vm_stats.free_count * (int64_t)page_size;
//
//        long long used_memory = ((int64_t)vm_stats.active_count +
//                                 (int64_t)vm_stats.inactive_count +
//                                 (int64_t)vm_stats.wire_count) *  (int64_t)page_size;
//        // printf("free memory: %lld\nused memory: %lld\n", free_memory, used_memory);
//        return used_memory;
//    }
//    return 0;
//}
//
//
////long long output_mem_usage()
////{
////    long pages = sysconf(_SC_PHYS_PAGES);
////    long page_size = sysconf(_SC_PAGE_SIZE);
////    return pages * page_size;
////}


vector<string> explode(const string& str) {
	string next;
	vector<string> result;

	// For each character in the string
	for (string::const_iterator it = str.begin(); it != str.end(); it++) {
		// If we've hit the terminal character
		if (*it == ' ') {
			// If we have some characters accumulated
			if (!next.empty()) {
				// Add them to the result vector
				result.push_back(next);
				next.clear();
			}
		} else {
			// Accumulate the next character into the sequence
			next += *it;
		}
	}
	if (!next.empty())
		result.push_back(next);
	return result;
}

long long output_mem_usage() {
	string cmd = "free | grep Mem";
	string data;
	FILE * stream;
	const int max_buffer = 256;
	char buffer[max_buffer];
	cmd.append(" 2>&1");

	stream = popen(cmd.c_str(), "r");
	if (stream) {
		while (!feof(stream))
			if (fgets(buffer, max_buffer, stream) != NULL) data.append(buffer);
		pclose(stream);
	}

	char token[] = "\t";
	vector<string> ret = explode(data);
	string ss = ret.at(2);
	char cstr[ss.size() + 1];
	strcpy(cstr, ss.c_str());    // or pass &s[0]
	long long ll = atoll(cstr);
	// return ret.at(2);
	return ll;
}
void mem_usage(double& vm_usage, double& resident_set) {
	vm_usage = 0.0;
	resident_set = 0.0;
	ifstream stat_stream("/proc/self/stat",ios_base::in); //get info from proc
	//directory
	//create some variables to get info
	string pid, comm, state, ppid, pgrp, session, tty_nr;
	string tpgid, flags, minflt, cminflt, majflt, cmajflt;
	string utime, stime, cutime, cstime, priority, nice;
	string O, itrealvalue, starttime;
	unsigned long vsize;
	long rss;
	stat_stream >> pid >> comm >> state >> ppid >> pgrp >> session >> tty_nr
	>> tpgid >> flags >> minflt >> cminflt >> majflt >> cmajflt
	>> utime >> stime >> cutime >> cstime >> priority >> nice
	>> O >> itrealvalue >> starttime >> vsize >> rss; // don't care
	// about the rest
	stat_stream.close();
	long page_size_kb = sysconf(_SC_PAGE_SIZE) / 1024; // for x86-64 is configured
	// to use 2MB pages
	vm_usage = vsize / 1024.0;
	resident_set = rss * page_size_kb;
}

int main()
{

	double vm1, rss1;
	mem_usage(vm1, rss1);
	// cout << "Virtual Memory: " << vm << "\nResident set size: " << rss << endl;





	int qn = 1000;
	const int MAXK = 50;
	char truth_set[100] = "../H2_ALSH/result/result_anti_correlated_5D_200000.mip";
	int top_k = 25;
	int dimension = 5;
	const int gloabl_dim = 5;
	int cardinality = 200000;
	char filepath[100] = "../H2_ALSH/raw_data/Synthetic/anti_correlated_5_200000.txt";
	char querypath[100] = "../H2_ALSH/query/query_5D.txt";

	typedef RTree<ValueType, float, gloabl_dim, float> MyTree;


	cout<<"data path: "<<filepath<<endl;
	Result **R = new Result*[qn];
	for (int i = 0; i < qn; ++i) R[i] = new Result[MAXK];
	if (read_ground_truth(qn, truth_set, R, MAXK) != 0)
	{
		printf("Reading Truth Set Error!\n");
		return 1;
	}

	float** data = new float*[cardinality];
	for (int i = 0; i < cardinality; ++i) data[i] = new float[dimension];
	if (read_data(filepath, data, dimension, cardinality) != 0)
	{
		printf("Reading dataset error!\n");
		return 1;
	}

	float** query = new float*[qn];
	for (int i = 0; i < qn; ++i) query[i] = new float[dimension];
	if (read_data(querypath, query, dimension, qn) != 0)
	{
		printf("Reading dataset error!\n");
		return 1;
	}


	MyTree tree;
	int i, nhits;

	timeval start_time, end_time;
	long long indexing_mem_start = output_mem_usage();

	gettimeofday(&start_time, NULL);
	for(i = 0; i < cardinality; i++)
	{
		// pack data into rtree node
		TempRect myrect = pack_data(data[i], dimension);
		tree.Insert(myrect.min, myrect.max, i); // Note, all values including zero are fine in this version
	}

	gettimeofday(&end_time, NULL);
	long long indexing_mem_end = output_mem_usage();

	cout<<"indexing start: "<<indexing_mem_start<<", indexing end: "<<indexing_mem_end<<endl;
	cout<<"indexing cost: "<<(long long)((long long)indexing_mem_end - (long long)indexing_mem_start) << endl;


	float building_tree = end_time.tv_sec - start_time.tv_sec + (end_time.tv_usec -
			start_time.tv_usec) / 1000000.0f;

	cout<<"Tree building time: "<<building_tree<<", total card: "<< cardinality<<", data insertion done"<<endl;

	double vm2, rss2;
	mem_usage(vm2, rss2);
	cout << "Virtual Memory: " << (vm2 - vm1) << "\nResident set size: " << (rss2- rss1) << endl;


	vector<float> myvector;
	float recall = 0.0f;
	int data_accessed = 0;

	long long query_mem_start = output_mem_usage();
	qn = 18;
	gettimeofday(&start_time, NULL);
	for(int i = 0; i < qn; i++)
	{
		// printf("query index: %d...\n", i);
		float* cur_query = query[i];
		if(myvector.size() != 0)
			myvector.clear();

		tree.BRS(top_k, myvector, cur_query, data_accessed);

		sort(myvector.begin(), myvector.end(), less<float>());

		// checkpoint(top_k, (const Result *) R[i], myvector);
		recall += calc_recall(top_k, (const Result *) R[i], myvector);
	}


	recall        = recall / qn;
	gettimeofday(&end_time, NULL);

	float runtime = end_time.tv_sec - start_time.tv_sec + (end_time.tv_usec -
			start_time.tv_usec) / 1000000.0f;
	runtime       = (runtime * 1000.0f) / qn;
	float average_data_accessed = ((float) data_accessed)/(float)qn;

	long long query_mem_end = output_mem_usage();
	cout<<"average query cost: "<<(float)(query_mem_end - query_mem_start)/(float)qn<<endl;


	cout<<"TopK: "<<top_k << ", runtime: "<<runtime<<", average data accessed: "<< average_data_accessed<<", recall: "<<recall<<endl;
	printf("  %3d\t\t%.4f\t\t%.2f\n", top_k, runtime, recall);


	return 0;
}

