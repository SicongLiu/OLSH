//***************************************************
//This is implementation of TPR-tree (cost model based)
//Coded by Yufei Tao 
//June 2002
//***************************************************

#include <math.h>
#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include "./rtree/rtree.h"
#include "./rtree/rtnode.h"
#include "./rtree/entry.h"
#include "./blockfile/blk_file.h"
#include "./blockfile/cache.h"
#include "./linlist/linlist.h"
#include "./metrics/metrics.h"
#include "./metrics/rand.h"

void buildtree(char *_trfname, char *_dsfname, float *_qmbrlen, float *_qvbr,
			   float _qst, float _qed, int _dsize)
{
	printf("really build tree?");
	char c=getchar();
	if (c!='y')
		return;
	remove(_trfname);
	RTree *rt = new RTree(_dsfname, _trfname, _dsize, NULL, 2, _qmbrlen, _qvbr, _qst, _qed);
//	rt->adjust_vmbr();
	delete rt;
};

/*****************************************************************
use traverse_node and traverse_tree to check the integrity of the
tree
coded by Yufei Tao 26/09/02
*****************************************************************/

int data_cnt=0;
int leaf_cnt=0;
int non_leaf_cnt=0;
int chk_lvl=0;
float xlen, ylen, ulen, vlen;
float avg_CX_ara=0;
float T=0;

///*
void traverse_node(RTNode *_rtn)
{
	if (_rtn->level==chk_lvl)
	{
		data_cnt+=_rtn->num_entries;
		leaf_cnt++;
		//these lines print the swept area of the node's CX-------
//		float *mbr=_rtn->get_mbr();
//		float *vbr=_rtn->get_vmbr();
//		float this_ara=Metrics::area(mbr, vbr, 0, T, 2);
//		avg_CX_ara+=this_ara;
//		xlen+=mbr[1]-mbr[0]; ylen+=mbr[3]-mbr[2];
//		ulen+=vbr[1]-vbr[0]; vlen+=vbr[3]-vbr[2];
//		printf("node id=%d, area=%f\n", _rtn->block, this_ara);
//		printf("len1=%.2f, len2=%.2f, vlen1=%.2f, vlen2=%.2f\n", 
//			mbr[1]-mbr[0], mbr[3]-mbr[2], vbr[1]-vbr[0], vbr[3]-vbr[2]);
//		delete []vbr;
//		delete []mbr;
		//--------------------------------------------------------
		return;
	}
	else
	{
		non_leaf_cnt++;
		for (int i=0; i<_rtn->num_entries; i++)
		{
			RTNode *succ=_rtn->entries[i].get_son();

			float *mbr=succ->get_mbr();
			float *vmbr=succ->get_vmbr();
			for (int j=0; j<4; j++)
			{
				if (fabs(mbr[j]-_rtn->entries[i].bounces[j])>0.001)
					printf("caught a bug\n");
				if (fabs(vmbr[j]-_rtn->entries[i].velocity[j])>0.001)
					printf("caught a bug\n");
			}
			delete []mbr;
			delete []vmbr;

			traverse_node(succ);
			_rtn->entries[i].del_son();
		}
	}
}

void traverse_tree(char *_trfname)
{
	data_cnt=0; leaf_cnt=0;
	non_leaf_cnt=0; avg_CX_ara=0;
	RTree *rt=new RTree(_trfname, NULL);
	rt->load_root();
	printf("the capacity=%d\n", rt->root_ptr->capacity-2);
	traverse_node(rt->root_ptr);
	rt->del_root();
	printf("dsize=%d\n", rt->file->blocklength);
//	printf("T=%f\n", rt->T);
	delete rt;
	printf("total number of leaf entries=%d\n", data_cnt);
	printf("total leaf=%d\n", leaf_cnt);
	printf("total non-leaf=%d\n", non_leaf_cnt);
//	printf("average CX area=%f\n", avg_CX_ara/leaf_cnt);
//	printf("xlen=%.3f, ylen=%.3f\n", xlen/leaf_cnt, ylen/leaf_cnt);
//	printf("ulen=%.3f, vlen=%.3f\n", ulen/leaf_cnt, vlen/leaf_cnt);
}
//*/

//===========random functions=====================================
/*float uniform(float _min, float _max)
{
	int int_r = rand();
	long base = RAND_MAX-1;
	float f_r  = ((float) int_r) / base;
	return (_max - _min) * f_r + _min;
}

float new_uniform(int _d_num)
{
	float base=1;
	float sum=0; 
	for (int i=0; i<_d_num; i++)
	{
		int digit=uniform(0, 10);
		if (digit==10) digit=9;
		sum+=base*digit;
		base*=10;
	}
	return sum;
}

float new_uniform(float _min, float _max)
{
	float ran_base=9999999;
	float ran=new_uniform(7);
	return ran/ran_base*(_max-_min)+_min;
}*/
//================================================================

int main(int argc, char* argv[])
{
	printf("*********************************************\n");
	printf("    TPR*-tree 1.1 (deletions)\n");
	printf("*********************************************\n");
	printf("\n\n");

	int dsize=1024;

	char trfname[100]="./trees/up3-2-test";
	//-test.tpr";
//	char trfname[100]="./trees/rs1-2.tpr";
	float qmbrlen[2]={100, 100};
	float qvbr[4]={-10, 10, -10, 10};
	float qst=0, qed=50;

///*
	buildtree(trfname, "../../ds/up3-time4.txt", qmbrlen, qvbr, qst, qed, dsize);
//	buildtree(trfname, "../../ds/rs1.txt", qmbrlen, qvbr, qst, qed, dsize);
//	traverse_tree(trfname); return;
//*/

///*
//	char trfname[100]="./trees/up3-1.tpr";
//	char trfname[100]="./trees/up3-2.tpr";
//	float qmbrlen[2]={100, 100};
//	float qvbr[4]={-10, 10, -10, 10};
//	float qst=0, qed=100;

	Cache *c=new Cache(0, dsize);
	RTree *rt=new RTree(trfname, c);
	printf("queries are performed as of time %.3f\n", rt->time);
	Entry *q=new Entry(2, NULL);

	int ita_cnt=50; 
	int total_rescnt=0;
	for (int i=0; i<ita_cnt; i++)
	{
		q->bounces[0]=new_uniform(1000, 9000-qmbrlen[0]);
		q->bounces[1]=q->bounces[0]+qmbrlen[0];
		q->bounces[2]=new_uniform(1000, 9000-qmbrlen[1]);
		q->bounces[3]=q->bounces[2]+qmbrlen[1];
//		q->bounces[0]=0;
//		q->bounces[1]=10000;
//		q->bounces[2]=0;
//		q->bounces[3]=10000;
	
		q->velocity[0]=qvbr[0]; q->velocity[1]=qvbr[1];
		q->velocity[2]=qvbr[2]; q->velocity[3]=qvbr[3];

//		q->velocity[0]=-100; q->velocity[1]=100;
//		q->velocity[2]=-100; q->velocity[3]=100;

		int rescnt=0;

		int this_cost=c->page_faults;
		rt->rangeQuery(q, qst, qed, rescnt);
		this_cost=c->page_faults-this_cost;
		total_rescnt+=rescnt;
		printf("%d: cost=%d\n", i+1, this_cost);

//		printf("retrieved %d entries\n", rescnt);
//		fprintf(fp, "%d %f %f %f %f %f %f %f %f %f %f %f\n", i, q->bounces[0], q->bounces[1], q->bounces[2],
//			q->bounces[3], q->velocity[0], q->velocity[1], q->velocity[2],q->velocity[3], (float)qst, 
//			(float)qed, (float)rescnt);
	}
//	fclose(fp);
	printf("avg # of entries retrieved=%f\n", total_rescnt/(float)ita_cnt);
	printf("avg node accesses=%f\n", c->page_faults/(float)ita_cnt);
	delete q;
	delete rt;
	delete c;
//*/
}
