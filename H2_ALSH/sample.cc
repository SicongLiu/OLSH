#include <random>
#include <algorithm>
#include <iterator>
#include <iostream>
#include <unordered_set>


// reference: https://stackoverflow.com/questions/28287138/c-randomly-sample-k-numbers-from-range-0n-1-n-k-without-replacement
std::unordered_set<int> pickSet(int N, int k, std::mt19937& gen)
{
    std::unordered_set<int> elems;
    for (int r = N - k; r < N; ++r)
    {
        int v = std::uniform_int_distribution<>(1, r)(gen);

        // there are two cases.
        // v is not in candidates ==> add it
        // v is in candidates ==> well, r is definitely not, because
        // this is the first iteration in the loop that we could've
        // picked something that big.

        if (!elems.insert(v).second)
        {
            elems.insert(r);
        }
    }
    return elems;
}

std::vector<int> pick(int N, int k)
{
    std::random_device rd;
    std::mt19937 gen(rd());

    std::unordered_set<int> elems = pickSet(N, k, gen);

    // ok, now we have a set of k elements. but now
    // it's in a [unknown] deterministic order.
    // so we have to shuffle it:

    std::vector<int> result(elems.begin(), elems.end());
    std::shuffle(result.begin(), result.end(), gen);
    return result;
}

void output_vec(std::vector<int> vec)
{
	for(int t : vec)
	{
		std::cout<< t <<"\t";
	}
	std::cout<<std::endl;
}

int main()
{
	int N = 10, k = 3;
	std::vector<int> ret1 = pick(N, k);
	output_vec(ret1);

	std::vector<int> ret2 = pick(N, k);
	output_vec(ret2);
	return 0;
}
