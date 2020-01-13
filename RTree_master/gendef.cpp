#include <string.h>

#include "max_list.h"
#include "gendef.h"

float calc_recall(					// calc recall (percentage)
	int   k,							// top-k value
	const Result *R,					// ground truth results
	MaxK_List *list)					// results returned by algorithms
{
	int i = k - 1;
	int last = k - 1;
	while (i >= 0 && R[last].key_ - list->ith_key(i) > FLOATZERO) {
		i--;
	}
	// printf("top-k: %d, index:%d, ground_truth: %f, ret: %f", k, i, R[last].key_, list->ith_key(i));
	return (i + 1) * 100.0f / k;
}

