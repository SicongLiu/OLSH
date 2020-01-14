#include <string.h>
#include <stdio.h>
#include "max_list.h"
#include "gendef.h"


// -----------------------------------------------------------------------------
MaxK_List::MaxK_List(                // constructor (given max size)
    int max)                            // max size
{
    num_ = 0;
    k_ = max;
    list_ = new Result[max + 1];
}

// -----------------------------------------------------------------------------
MaxK_List::~MaxK_List()             // destructor
{
    if (list_ != NULL) {
        delete[] list_; list_ = NULL;
    }
}

// -----------------------------------------------------------------------------
bool MaxK_List::isFull()            // is full?
{
    if (num_ >= k_) return true;
    else return false;
}

// -----------------------------------------------------------------------------
float MaxK_List::insert(            // insert item
    float key,                            // key of item
    int id)                                // id of item
{
    int i = 0;

    // for each candidate, check potential insert location
    for (i = num_; i > 0; i--)
    {
    	if (list_[i-1].key_ < key)
    		list_[i] = list_[i - 1];
    	else break;
    }
    list_[i].key_ = key;                // store new item here
    list_[i].id_ = id;
    if (num_ < k_)
    	num_++;            // increase the number of items
    return min_key();
}

void MaxK_List::reset()
{
	num_ = 0;
}

// -------------------------------------------------------------------------
float MaxK_List::max_key(){
	return num_ > 0 ? list_[0].key_ : MINREAL;
}

// -------------------------------------------------------------------------
float MaxK_List::min_key() { return num_ == k_ ? list_[k_-1].key_ : MINREAL; }

// -------------------------------------------------------------------------
float MaxK_List::ith_key(int i) { return i < num_ ? list_[i].key_ : MINREAL; }

// -------------------------------------------------------------------------
int MaxK_List::ith_id(int i) { return i < num_ ? list_[i].id_ : MININT; }




