#ifndef __GENERAL_DEFINITION
#define __GENERAL_DEFINITION

class MaxK_List;

#define FLOATZERO       1e-2

const float MAXREAL       = 3.402823466e+38F;
const float MINREAL       = -MAXREAL;
const int   MAXINT        = 2147483647;
const int   MININT        = -MAXINT;


//#define min(a, b) (((a) < (b))? (a) : (b)  )
//#define max(a, b) (((a) > (b))? (a) : (b)  )

//-----------------------------------------------------------
struct Result {						// structure for furthest neighbor / hash value
	float key_;							// distance / random projection value
	int   id_;							// object id
};

float calc_recall(					// calc recall (percentage)
	int   k,							// top-k value
	const Result *R,					// ground truth results
	MaxK_List *list)	;




#endif
