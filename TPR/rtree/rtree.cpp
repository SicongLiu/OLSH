/*rtree.cpp
  this file implements the RTree class*/
#include <math.h>
#include <stdlib.h>
#include <string.h>
// #include <bits/stdc++.h>
#include <queue>
#include <vector>
#include "rtree.h"
#include "entry.h"
#include "myentry.h"
#include "rtnode.h"
#include "../blockfile/cache.h"
#include "../blockfile/blk_file.h"
#include "../linlist/linlist.h"
#include "../metrics/metrics.h"
#include "../func/gendef.h"
//------------------------------------------------------------
RTree::RTree(char *fname, Cache *c)
//use this constructor to restore a tree from a file
{
	file = new BlockFile(fname, 0);
	cache =c;

	re_data_cands = new LinList();
	deletelist = new LinList();

	char *header = new char [file->get_blocklength()];
	file -> read_header(header);
	read_header(header);
	delete [] header;

	root_ptr = NULL;
	pathhp=new Heap();
	pathhp->init(2, 500);

	emergency=false;

	//qmbrlen[] and qvbr[] are initialized in read_header
}

/*****************************************************************
Use this function to construct a new TPR-tree from a dataset
para:

dsfname: the dataset file
tfname: the tree file
b_len: the block length
c: the cache
T: the tree is optimized in [0, T]
dimension: dimensionality
qmbrlen: the lengths of the target query mbr
qvbr: the vbr of target query
qst: the starting timestamp of the query interval
qed: the ending timestamp of the query interval

Coded by Yufei Tao 25/10/02
 *****************************************************************/

struct MovingObject
{
	bool active;
	float mbr[4];
	float vbr[4];
	float ref;		//reference time
};

RTree::RTree(char *_dsfname, char *_tfname, int _blen, Cache *_c, int _dimension,
		float *_qmbrlen, float *_qvbr, float _qst, float _qed)
// construct new R-tree from a specified input textfile with rectangles
{
	//init files--------------------------------------------------
	file=new BlockFile(_tfname, _blen);
	cache=_c;
	//init necessary variables------------------------------------
	re_data_cands=new LinList();   //to be destroyed in desctructor
	deletelist=new LinList();	   //to be destroyed in desctructor

	time=0;
	dimension=_dimension;
	root=0;
	root_ptr=NULL;
	root_is_data=true;
	num_of_data=num_of_inodes=num_of_dnodes=0;
	pathhp=new Heap();
	pathhp->init(2, 10000);
	pathhp->used=0;
	maxChoosePathNA=0;
	emergency=false;

	qmbrlen=new float[dimension];
	qvbr=new float[2*dimension];
	memcpy(qmbrlen, _qmbrlen, dimension*sizeof(float));
	memcpy(qvbr, _qvbr, 2*dimension*sizeof(float));
	qst=_qst; qed=_qed;
	//init the first node-----------------------------------------
	root_ptr = new RTNode(this);
	num_of_dnodes++;
	root_ptr -> level = 0;
	root = root_ptr->block;
	root_lvl=0;
	//------------------------------------------------------------

	int maxN=150000;
	MovingObject *data=new MovingObject[maxN];
	for (int i=0; i<maxN; i++)
		data[i].active=false;

	int record_count = 0;
	FILE *fp;
	if((fp = fopen(_dsfname,"r")) == NULL)
	{
		delete this;
		error("Cannot open R-Tree text file", TRUE);
	}
	else
	{
		Entry *tmpe=new Entry(dimension, this);
		while (!feof(fp))
		{
			record_count ++;

			//init the entry--------------------------------------
			float this_time;
			Entry *d = new Entry(dimension, NULL);
			fscanf(fp, "%d", &(d -> son));
			for (int i = 0; i < 2 * dimension; i ++)
				fscanf(fp, " %f", &(d -> bounces[i]));
			for (int i = 0; i < 2*dimension; i ++)
				fscanf(fp, " %f", &(d->velocity[i]));
			fscanf(fp, " %f\n", &this_time);
			if (this_time<time)
				error("\ncannot insert backward in time!\n", true);
			//			else if (time<this_time)
			//				printf("\nprogressing to time %.3f\n", time);
			time=this_time;

			d->level=0;
			//----------------------------------------------------
			if (record_count % 100 == 0)
			{
				for (int i = 0; i < 79; i ++)  //clear a line
					printf("\b");
				printf("inserting record %d at time %.3f", record_count, time);
			}
			if (emergency)
				printf("record_count=%d\n", record_count);
			//----------------------------------------------------
			//if (record_count==14365)
			//printf("testing...\n");
			if (d->son>=maxN)
				error("please increase maxN\n", true);
			if (data[d->son].active)
			{
				tmpe->son=d->son;
				memcpy(tmpe->bounces, data[d->son].mbr, sizeof(float)*4);
				memcpy(tmpe->velocity, data[d->son].vbr, sizeof(float)*4);
				future_mbr(tmpe->bounces, tmpe->velocity, time-data[d->son].ref, dimension);
				delete_entry(tmpe);
			}
			memcpy(data[d->son].mbr, d->bounces, sizeof(float)*4);
			memcpy(data[d->son].vbr, d->velocity, sizeof(float)*4);
			data[d->son].ref=time;
			data[d->son].active=true;

			insert(d);	//d will be deleted in insert()
			//----------------------------------------------------
			/*
if (record_count>=14364)
{
	int checkId=3531;
	Entry *q=new Entry(2, NULL);

//	for (int i=0; i<4; i++)
//	{
//		q->bounces[i]=data[checkId].mbr[i]+data[checkId].vbr[i]*(time-data[checkId].ref);
//		q->velocity[i]=data[checkId].vbr[i];
//	}
//	q->son=checkId;

	q->bounces[0]=q->bounces[2]=-100000;
	q->bounces[1]=q->bounces[3]=200000;
	q->velocity[0]=q->velocity[1]=q->velocity[2]=q->velocity[3]=0;
	int rescnt=0;
	rangeQuery(q, 0, 0, rescnt);
//if (record_count==298)
//printf("testing...\n");
//	bool cret=FindLeaf(q); 
	if (rescnt!=10000)
//	if (!cret)
	{
		printf("record_count=%d\n", record_count);
		printf("retrieved %d objects\n", rescnt);
		error("found a bug here\n", true);
//		error("entry not found\n", true);
	}
}
			 */
		}
		delete tmpe;
	}

	fclose(fp);
	delete [] data;

	printf("\n");
	delete root_ptr;
	root_ptr = NULL;

	printf("maximum # of node accesses in choose path=%d\n", maxChoosePathNA);
}

//------------------------------------------------------------
RTree::~RTree()
{
	char *header = new char[file -> get_blocklength()];
	write_header(header);
	file->set_header(header);
	delete [] header;

	if (root_ptr != NULL)
	{
		delete root_ptr;
		root_ptr = NULL;
	}

	if (cache)
		cache -> flush();

	delete file;

	delete re_data_cands;
	delete deletelist;
	delete pathhp;

	delete []qmbrlen; delete []qvbr;

	printf("This R-Tree contains %d internal, %d data nodes and %d data\n",
			num_of_inodes, num_of_dnodes, num_of_data);
}
//------------------------------------------------------------
void RTree::del_root()
{
	delete root_ptr;
	root_ptr = NULL;
}
//------------------------------------------------------------
bool RTree::FindLeaf(Entry *_q)
{
	past_mbr(_q->bounces, _q->velocity, time, 2);
	load_root();
	bool cret=root_ptr -> FindLeaf(_q);
	printf("\n");
	del_root();
	return cret;
}

/*****************************************************************
Use this function to insert an entry into the TPR-tree
para:
d: the entry to be inserted

Coded by Yufei Tao 21/6/02
 *****************************************************************/

void RTree::insert(Entry* d)
{
	if (d->level==0)
		num_of_data++;

	re_level = new bool[root_lvl + 1];
	for (int i = 0; i <= root_lvl; i++)
		re_level[i] = FALSE;

	//insert d into re_data_cands as the first entry to insert----
	//make a copy of d because it should be erased later
	Linkable *new_link;
	new_link=d->gen_Linkable();
	new_link->level=d->level;
	re_data_cands->insert(new_link);
	delete d;  //we follow the convention that the entry will be deleted when insertion finishes
	//------------------------------------------------------------

	R_OVERFLOW split_root;
	RTNode *sn; //the point to the new node (if created)
	while (re_data_cands->get_num()>0)
	{
		Linkable *d_cand;
		d_cand = re_data_cands -> get_first();
		if (d_cand != NULL)
		{
			//copy the first entry from re_data_cands-------------
			Entry *dc=new Entry(dimension, NULL); //the entry to be inserted
			dc->set_from_Linkable(d_cand);
			re_data_cands -> erase();
			//then insert it--------------------------------------
			float min_pen=choose_path(dc); 
			//if (dc->son % 1 == 0)
			{
				//printf("checking path...");
				//check_path(dc, min_pen);
				//printf("pased\n");
			}
			load_root();
			split_root = root_ptr -> insert(dc, &sn);
			//----------------------------------------------------
		}
		else
			error("RTree::insert--inconsistent list re_data_cands", true);

		if (split_root == SPLIT)
			// insert will lead to a new root with two sons (i.e. root and sn)
		{
			RTNode *nroot_ptr = new RTNode(this);
			nroot_ptr -> level = root_ptr -> level + 1;
			root_lvl++;
			num_of_inodes++;
			int nroot = nroot_ptr -> block; //this is the block id of the new root

			//now create the first entry of the new root----------
			Entry *de = new Entry(dimension, this);
			float *nmbr = root_ptr -> get_mbr();
			float *vbr = root_ptr -> get_vmbr();
			//			adjust_mbr(nmbr, vbr, time, dimension);
			memcpy(de->bounces, nmbr, 2*dimension*sizeof(float));
			memcpy(de -> velocity, vbr, 2 * dimension * sizeof(float));
			if (emergency)
			{
				future_mbr(nmbr, vbr, time, 2);
			}
			delete [] nmbr; delete [] vbr;

			de->son = root_ptr->block;
			de->son_ptr = NULL;
			nroot_ptr -> enter(de);
			delete root_ptr;
			//then the second entry-------------------------------
			de = new Entry(dimension, this);
			nmbr = sn -> get_mbr();
			if (emergency)
			{
				printf("****************\n");
				printf("%f %f %f %f\n", nmbr[0], nmbr[1], nmbr[2], nmbr[3]);
				printf("****************\n");
			}
			vbr=sn->get_vmbr();
			//			adjust_mbr(nmbr, vbr, time, dimension);
			if (emergency)
			{
				float *nmbr=sn->get_mbr();
				printf("****************\n");
				printf("level=%d, block=%d\n", sn->level, sn->block);
				printf("%f %f %f %f\n", nmbr[0], nmbr[1], nmbr[2], nmbr[3]);
				printf("****************\n");
				delete []nmbr;

			}
			memcpy(de -> bounces, nmbr, 2*dimension*sizeof(float));
			memcpy(de -> velocity, vbr, 2 * dimension * sizeof(float));
			if (emergency)
			{
				future_mbr(nmbr, vbr, time, 2);
			}
			delete [] nmbr; delete []vbr;

			de -> son = sn -> block;
			de -> son_ptr = NULL;
			nroot_ptr->enter(de);
			delete sn;
			//----------------------------------------------------
			root=nroot;
			root_ptr=nroot_ptr;
			root_is_data = FALSE;
		}
		if (emergency)
		{
			for (int i=0;i<root_ptr->num_entries;i++)
			{
				float nmbr[4];
				memcpy(nmbr, root_ptr->entries[i].bounces, 4*sizeof(float));
				future_mbr(nmbr, root_ptr->entries[i].velocity, time, 2);
			}
		}
		delete root_ptr; root_ptr=NULL;
	}

	delete [] re_level;
	delete root_ptr;
	root_ptr = NULL;
}

//------------------------------------------------------------

void RTree::load_root()
{
	if (root_ptr == NULL)
		root_ptr = new RTNode(this, root);
	if (emergency)
	{
		if (root_ptr->level != root_lvl)
			error("root level doesn't match!\n", true);
		printf("root is at block %d at level %d containing %d entries\n",
				root_ptr->block, root_ptr->level, root_ptr->num_entries);
	}
}
//------------------------------------------------------------
void RTree::rangeQuery(Entry *_q, float _st, float _ed, int& _rsltcnt)
//void RTree::rangeQuery(Entry *_q, float _st, float _ed, SortedLinList *res)
{
	_st+=time; _ed+=time;
	past_mbr(_q->bounces, _q->velocity, _st, 2);
	load_root();
	//  root_ptr -> rangeQuery(_q, _st, _ed, res);
	root_ptr -> rangeQuery(_q, _st, _ed, _rsltcnt);
	delete root_ptr;
	root_ptr = NULL;
}
//------------------------------------------------------------
void RTree::read_header(char *buffer)
{
	int i;

	memcpy(&dimension, buffer, sizeof(dimension));
	i = sizeof(dimension);

	memcpy(&num_of_data, &buffer[i], sizeof(num_of_data));
	i += sizeof(num_of_data);

	memcpy(&num_of_dnodes, &buffer[i], sizeof(num_of_dnodes));
	i += sizeof(num_of_dnodes);

	memcpy(&num_of_inodes, &buffer[i], sizeof(num_of_inodes));
	i += sizeof(num_of_inodes);

	memcpy(&root_is_data, &buffer[i], sizeof(root_is_data));
	i += sizeof(root_is_data);

	memcpy(&root, &buffer[i], sizeof(root));
	i += sizeof(root);

	//	memcpy(&T, &buffer[i], sizeof(T));
	//	i += sizeof(T);

	qmbrlen=new float[dimension];
	qvbr=new float[2*dimension];

	memcpy(qmbrlen, &buffer[i], dimension*sizeof(float));
	i+=dimension*sizeof(float);

	memcpy(qvbr, &buffer[i], 2*dimension*sizeof(float));
	i+=2*dimension*sizeof(float);

	memcpy(&qst, &buffer[i], sizeof(qst));
	i+=sizeof(qst);

	memcpy(&qed, &buffer[i], sizeof(qed));
	i+=sizeof(qed);

	memcpy(&time, &buffer[i], sizeof(float));
	i+=sizeof(time);
}
//------------------------------------------------------------
void RTree::write_header(char *buffer)
{
	int i;

	memcpy(buffer, &dimension, sizeof(dimension));
	i = sizeof(dimension);

	memcpy(&buffer[i], &num_of_data, sizeof(num_of_data));
	i += sizeof(num_of_data);

	memcpy(&buffer[i], &num_of_dnodes, sizeof(num_of_dnodes));
	i += sizeof(num_of_dnodes);

	memcpy(&buffer[i], &num_of_inodes, sizeof(num_of_inodes));
	i += sizeof(num_of_inodes);

	memcpy(&buffer[i], &root_is_data, sizeof(root_is_data));
	i += sizeof(root_is_data);

	memcpy(&buffer[i], &root, sizeof(root));
	i += sizeof(root);

	//	memcpy(&buffer[i], &T, sizeof(T));
	//	i += sizeof(T);

	memcpy(&buffer[i], qmbrlen, dimension*sizeof(float));
	i+=dimension*sizeof(float);

	memcpy(&buffer[i], qvbr, 2*dimension*sizeof(float));
	i+=2*dimension*sizeof(float);

	memcpy(&buffer[i], &qst, sizeof(qst));
	i+=sizeof(qst);

	memcpy(&buffer[i], &qed, sizeof(qed));
	i+=sizeof(qed);

	memcpy(&buffer[i], &time, sizeof(float));
	i+=sizeof(time);
}

/*****************************************************************
This function will detect whether two moving regions will intersect
during [st,ed].  If yes, an array containing the intersection interval
will be returned.  

para:
e1: the first moving region
e2: the 2nd one
st: the starting time of the query interval
ed: the ending time

Coded by Yufei Tao 23/06/02
 *****************************************************************/

float *RTree::moving_sect(Entry *_e1, Entry *_e2, float _st, float _ed)
{
	//we first copy the two input entries-------------------------
	Entry *e1=new Entry(dimension, NULL);
	Entry *e2=new Entry(dimension, NULL);
	*e1=*_e1; *e2=*_e2; 
	//set e1.mbr and e2.mbr at time st ---------------------------
	//note the current time is 0
	for (int i=0; i<2*dimension; i++)
	{
		e1->bounces[i]+=e1->velocity[i]*_st;
		e2->bounces[i]+=e2->velocity[i]*_st;
	}
	//init another 2 entries and set their mbrs at ed ------------
	Entry *ee1=new Entry(dimension, NULL);
	Entry *ee2=new Entry(dimension, NULL);
	*ee1=*_e1; *ee2=*_e2; 
	for (int i=0; i<2*dimension; i++)
	{
		ee1->bounces[i]+=ee1->velocity[i]*_ed;
		ee2->bounces[i]+=ee2->velocity[i]*_ed;
	}

	float *finalintv=new float[2]; //the final intersection interval
	float curintv[2]; //the intersection interval along the dimension being considered

	for (int i=0;i<dimension;i++)
	{
		if (e1->bounces[2*i]>e2->bounces[2*i+1] && ee1->bounces[2*i]>ee2->bounces[2*i+1])
		{
			delete [] finalintv;
			delete e1; delete e2; 
			delete ee1; delete ee2;
			return NULL;
		}
		if (e1->bounces[2*i+1]<e2->bounces[2*i] && ee1->bounces[2*i+1]<ee2->bounces[2*i])
		{
			delete [] finalintv; 
			delete e1; delete e2; 
			delete ee1; delete ee2;
			return NULL;
		}

		float A,B,C,D;
		A=e2->bounces[2*i+1]-e1->bounces[2*i];
		B=e1->velocity[2*i]-e2->velocity[2*i+1];
		C=e2->bounces[2*i]-e1->bounces[2*i+1];
		D=e1->velocity[2*i+1]-e2->velocity[2*i];

		if (e1->bounces[2*i]>e2->bounces[2*i+1])
		{
			curintv[0]=_st+A/B;
		}
		else if (e1->bounces[2*i+1]<e2->bounces[2*i])
		{
			curintv[0]=_st+C/D;
		}
		else
			curintv[0]=_st;
		//if (curintv[0]<_st)
		//printf("testing...caught an error in querying\n");

		if (ee1->bounces[2*i]>ee2->bounces[2*i+1])
		{
			curintv[1]=_st+A/B;
		}
		else if (ee1->bounces[2*i+1]<ee2->bounces[2*i])
		{
			curintv[1]=_st+C/D;
		}
		else
			curintv[1]=_ed;
		//if (curintv[1]>_ed)
		//printf("testing...caught an error in querying\n");

		if (i==0)
		{
			finalintv[0]=curintv[0];
			finalintv[1]=curintv[1];
		}
		else
		{
			if (curintv[0]>finalintv[1] || curintv[1]<finalintv[0])
			{
				delete []finalintv; 
				delete e1; delete e2; 
				delete ee1; delete ee2;
				return NULL;
			}

			if (finalintv[0]<curintv[0])
				finalintv[0]=curintv[0];
			if (finalintv[1]>curintv[1])
				finalintv[1]=curintv[1];
		}
	}

	delete e1; delete e2; 
	delete ee1; delete ee2;
	return finalintv;
}

/*****************************************************************
this function finds the leaf node that leads to minimum area increase
para:
newe: the entry to be inserted. its mbr must be at the current time
the return value indicates the minimum penalty
Coded by Yufei Tao 30/09/02
 *****************************************************************/

float RTree::choose_path(Entry *_newe)
{
	if (emergency)
		printf("the level of the new entry is %d, id=%d\n", _newe->level, _newe->son);

	if (_newe->level==root_lvl)
	{
		path[_newe->level]=root;
		return 0;
	}

	float minpen=MAXREAL, minara=MAXREAL;
	pathhp->used=0;
	HeapEntry *hpe=new HeapEntry();
	hpe->son1=root;
	hpe->key=0;
	hpe->path[root_lvl]=root;
	pathhp->insert(hpe);
	int ndacs=0;

	Entry *e=new Entry(dimension, NULL);
	while (pathhp->used>0 && pathhp->cont[0].key<minpen)
	{
		pathhp->remove(hpe);
		RTNode *succ=new RTNode(this, hpe->son1);
		ndacs++;
		if (succ->level==_newe->level+1)
		{
			for (int i=0; i<succ->num_entries; i++)
			{
				if (emergency)
				{
					printf("choosepath at level %d block %d entry %d\n", succ->level, succ->block, i);
				}
				//				float this_ara=Metrics::area(succ->entries[i].bounces, succ->entries[i].velocity,
				//					qmbrlen, qvbr, time+qst, time+qed, dimension);
				*e=succ->entries[i];
				future_mbr(e->bounces, e->velocity, time, dimension);
				float this_ara=Metrics::area(e->bounces, e->velocity, qmbrlen, 
						qvbr, qst, qed, dimension);
				e->enlarge(e, _newe);
				float ara=Metrics::area(e->bounces, e->velocity, qmbrlen, qvbr, qst, qed, dimension);

				if (ara<this_ara && this_ara-ara>10)
				{
					future_mbr(succ->entries[i].bounces, succ->entries[i].velocity, time, dimension);
					printf("\nbefore: %.3f, %.3f, %.3f, %.3f %.3f %.3f %.3f %.3f\n", succ->entries[i].bounces[0],
							succ->entries[i].bounces[1], succ->entries[i].bounces[2], succ->entries[i].bounces[3],
							succ->entries[i].velocity[0], succ->entries[i].velocity[1], succ->entries[i].velocity[2],
							succ->entries[i].velocity[3]);
					printf("\nafter: %.3f, %.3f, %.3f, %.3f %.3f %.3f %.3f %.3f\n", e->bounces[0],
							e->bounces[1], e->bounces[2], e->bounces[3], e->velocity[0],
							e->velocity[1], e->velocity[2], e->velocity[3]);
					printf("enlarged mbr actually smaller, difference: %.3f\n", ara-this_ara);
					error("", true);
				}

				float pen=ara-this_ara+hpe->key;
				if (pen<minpen || (pen==minpen && this_ara<minara))
				{
					path[succ->level-1]=succ->entries[i].son;
					for (int j=succ->level; j<root_lvl; j++)
					{
						path[j]=hpe->path[j];
					}
					minpen=pen; minara=this_ara;
				}
			}
		}
		else
		{
			for (int i=0; i<succ->num_entries; i++)
			{
				//				float this_ara=Metrics::area(succ->entries[i].bounces, succ->entries[i].velocity,
				//					qmbrlen, qvbr, time+qst, time+qed, dimension);
				*e=succ->entries[i];
				future_mbr(e->bounces, e->velocity, time, dimension);
				float this_ara=Metrics::area(e->bounces, e->velocity, qmbrlen, 
						qvbr, qst, qed, dimension);
				e->enlarge(e, _newe);
				float ara=Metrics::area(e->bounces, e->velocity, qmbrlen, qvbr, qst, qed, dimension);

				if (ara<this_ara && this_ara-ara>10)
				{
					future_mbr(succ->entries[i].bounces, succ->entries[i].velocity, time, dimension);
					printf("\nbefore: %.3f, %.3f, %.3f, %.3f %.3f %.3f %.3f %.3f\n", succ->entries[i].bounces[0],
							succ->entries[i].bounces[1], succ->entries[i].bounces[2], succ->entries[i].bounces[3],
							succ->entries[i].velocity[0], succ->entries[i].velocity[1], succ->entries[i].velocity[2],
							succ->entries[i].velocity[3]);
					printf("\nafter: %.3f, %.3f, %.3f, %.3f %.3f %.3f %.3f %.3f\n", e->bounces[0],
							e->bounces[1], e->bounces[2], e->bounces[3], e->velocity[0],
							e->velocity[1], e->velocity[2], e->velocity[3]);
					printf("enlarged mbr actually smaller, difference: %.3f\n", ara-this_ara);
					error("", true);
				}
				float pen=ara-this_ara+hpe->key;
				if (pen<minpen)
				{
					HeapEntry *newhpe=new HeapEntry();
					newhpe->path[succ->level-1]=succ->entries[i].son;
					for (int j=succ->level; j<root_lvl; j++)
					{
						newhpe->path[j]=hpe->path[j];
					}
					newhpe->son1=succ->entries[i].son;
					newhpe->key=pen;
					pathhp->insert(newhpe);
					delete newhpe;
				}
			}
		}
		delete succ;
	}
	delete e;
	delete hpe;

	if (maxChoosePathNA<ndacs)
		maxChoosePathNA=ndacs;
	//printing summary of this choose path ---------------------------
	//if (_newe->son % 1000 == 0)
	//{
	//printf("visited %d nodes (max %d)\n", ndacs, maxChoosePathNA);
	//printf("the minimum penalty is %.3f\n", minpen);
	//}
	//----------------------------------------------------------------
	return minpen;
}

/*****************************************************************
this function checks whether the path got from choose_path is indeed
an optimal path. before calling this function, you must make sure
that the path array of the tree has been set
para:
newe: the entry to be inserted
minpen: the minimum penalty
Coded by Yufei Tao 30/09/02
 *****************************************************************/

void RTree::check_path(Entry *_newe, float _minpen)
{
	load_root();	
	//printf("debugging...check_path(R-tree)");
	bool cret=root_ptr->check_path(_newe, 0, _minpen);
	if (!cret)
		error("the path is not confirmed\n", true);
	//printf("fine\n");
	delete root_ptr; root_ptr=NULL;
}

/*****************************************************************
this function deletes an entry from the current tree
para:
olde: the entry to be inserted -- we need its mbr at the current time set
Coded by Yufei Tao 03/11/02
 *****************************************************************/

void RTree::delete_entry(Entry *_olde)
{
	load_root();
	R_DELETE cret=root_ptr->delete_entry(_olde);
	if (cret!=ERASED)
		del_root();
	else
		if (cret==ERASED)
		{
			//printf("before root=%d and root_lvl=%d\n", root, root_lvl);
			if (root_ptr->level>0)
			{
				root=root_ptr->entries[0].son;
				root_lvl=root_ptr->level-1;
			}
			del_root();
			//printf("after root=%d and root_lvl=%d\n", root, root_lvl);
			//printf("deleting root\n");
			//emergency=true;
		}

	if (cret==NOTFOUND)
	{
		printf("could not find entry id=%d\n", _olde->son);
		printf("mbr=[%f, %f][%f, %f]\n", _olde->bounces[0], _olde->bounces[1],
				_olde->bounces[2], _olde->bounces[3]);
		error("entry not found\n", true);
	}

	num_of_data--;

	while (deletelist->get_num()>0)
	{
		Linkable *d_cand;
		d_cand = deletelist -> get_first();
		if (d_cand != NULL)
		{
			Entry *dc=new Entry(dimension, NULL); //the entry to be inserted
			dc->set_from_Linkable(d_cand);
			deletelist -> erase();	
			if (dc->level==0)
				num_of_data--;
			insert(dc);
		}
	}
}


// Added by Sicong
float RTree::get_maxscore(float* p_mbr, float* query)
{
	float score = 0.0f;
	for(int i = 0; i < dimension; i++)
	{
		if(query[i] >= 0)
		{
			score += query[i] * p_mbr[2 * i + 1];
		}
		else
		{
			score += query[i] * p_mbr[2 * i];
		}
	}
	return score;
}


// Added by Sicong
struct Compare
{
    bool operator() (MyEntry const& e1, MyEntry const& e2)
    {
    		if(e1.key <= e2.key)
    			return true;
    		else
    			return false;
    }
};


int RTree::BRS(int top_k, MaxK_List* list, float ** data, float* query)
{
	// initiate the candidate heap H,
	std::priority_queue <MyEntry, std::vector<MyEntry>, Compare> pq;
	int list_size_count = 0;

	// initiate a result set S with size k
	// list size already = size of k

	// load the root of RTree
	load_root();

	for(int i = 0; i < root_ptr->capacity; i++)
	{
		Entry cur_entry = root_ptr->entries[i];
		float temp_max_score = get_maxscore(cur_entry.bounces, query);
		MyEntry* temp_entry = new MyEntry(temp_max_score, cur_entry);
		pq.push(*temp_entry);
	}

	while(list_size_count < top_k)
	{
		// temp_H = de-heap(H)
		MyEntry temp_H = pq.top();
		pq.pop();
		// if temp_H is a leaf, then add it to S (return S if it contains k tuples)
		if(temp_H.e.isLeaf())
		{
			// id is an arbitrary number, here i use node level
			list->insert(temp_H.key, temp_H.e.level);
			list_size_count++;
			if(list_size_count == list->size())
				return 0;
		}
		else // else for every entry e in temp_H.childnode
		{
			Entry temp_entry = temp_H.e;
			RTNode* temp_RT_node = temp_entry.son_ptr;

			for (int j = 0; j < temp_RT_node->capacity; j++)
			{
				// e.maxscore=getmax_score(e.mbr, f)
				float temp_max_score = get_maxscore(temp_RT_node->entries[j].bounces, query);
				MyEntry* temp_entry = new MyEntry(temp_max_score, temp_RT_node->entries[j]);
				// insert(e, e.maxscore) into H
				pq.push(*temp_entry);
			}
		}
	}

	return 0;
}





=======
/*
Algorithm get_maxscore (M=(l1,h1, l2,h2,…, ld,hd), f)
// M is a MBR with extent [li, hi] along the i-th dimension (1≤i≤d), and f the preference function 
1. initiate a point p whose coordinates are not decided yet
2. for i=1 to d // examine each dimension in turn 
3. if f is increasingly monotone on this dimension
4. the i-th coordinate of p is set to hi
5. else the i-th coordinate of p is set to li
6. return f(p)
end get_maxscore
*/

/*
Algorithm BRS (RTree, f, k}
// RTree is the R-tree on the data set, f is the preference function, and k denotes how many points to return 
1. initiate the candidate heap H  // H takes entries in the form (REntry, key) and manages them in descending order of key (REntry is an entry in RTree)
2. initiate a result set S with size k
3. load the root of RTree, and for each entry e in the root
4. e.maxscore=get_maxscore(e.MBR, f) // invoke the algorithm in Figure 4
5. insert (e, e.maxscore) into H
6. while (S contains less than k objects)
7. he=de-heap(H)
8. if he is a leaf entry, then add he to S, and return S if it contains k tuples
9. else for every entry e in he.childnode
10. e.maxscore=get_maxscore(e.MBR, f)
11. insert (e, e.maxscore) into H
12. return S
end BRS
*/
