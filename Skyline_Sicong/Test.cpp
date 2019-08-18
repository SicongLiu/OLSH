#include <cstdlib>
#include <cstdio>
#include <stdio.h>
#include <cassert>
#include <cstring>
#include <array>
#include <set>
#include <vector>
#include <iostream>

using namespace std;

int main(int nargs, char **args)
{
    set<int> setA;
    for(int i = 0; i < 10; i++)
    {
        setA.insert(i);
    }
    
    set<int> setB;
    for(int i=0; i < 5; i++)
    {
        setB.insert(i);
    }
    set<int> temp;
    set_difference(setA.begin(), setA.end(), setB.begin(), setB.end(), inserter(temp, temp.end()));
    
    setA = temp;
    temp.clear();
    set<int>::iterator it = setA.begin();
    
    while(it != setA.end())
    {
        cout<<*it<<endl;
        it++;
    }
    
    return 0;
}


