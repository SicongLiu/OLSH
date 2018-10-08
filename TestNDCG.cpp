//
//  TestNDCG.cpp
//  StreamingTopK
//
//  Created by Sicong Liu on 11/21/17.
//  Copyright © 2017 Sicong Liu. All rights reserved.
//
// Test implementation of DCG and NDCG
// reference: https://en.wikipedia.org/wiki/Discounted_cumulative_gain

#include <stdio.h>
#include <cmath>
#include <iostream>
#include <vector>

double DCG(std::vector<double> relevence)
{
    double dcg = 0;
    for(int i=0; i<relevence.size(); i++)
    {
        int rankIndex = i + 1;
        dcg += relevence.at(i)/std::log2(rankIndex + 1);
    }
    return dcg;
}

double NDCG(std::vector<double> relevence)
{
    double dcg = DCG(relevence);
    std::sort(relevence.begin(), relevence.end(), std::greater<double>());
    double tempNDCG = DCG(relevence);
    return dcg/tempNDCG;
}

double alterDCG(std::vector<double> relevence)
{
    double dcg = 0;
    for(int i=0; i<relevence.size(); i++)
    {
        int rankIndex = i + 1;
        dcg += (std::pow(2, relevence.at(i)) - 1 )/std::log2(rankIndex + 1);
    }
    return dcg;
}

double alterNDCG(std::vector<double> relevence)
{
    double alterdcg = alterDCG(relevence);
    std::sort(relevence.begin(), relevence.end(), std::greater<double>());
    double alterTempNDCG = alterDCG(relevence);
    
    std::cout<<alterdcg << " "<<alterTempNDCG<<std::endl;
    return alterdcg/alterTempNDCG;
}

int main()
{
    static const double arr[] = {3,2,3,0,1,2};
    std::vector<double> relevence (arr, arr + sizeof(arr) / sizeof(arr[0]) );
    std::vector<double> relevence1 (arr, arr + sizeof(arr) / sizeof(arr[0]) );
    
    // print to check
    for(int i=0; i<relevence.size(); i++)
    {
        std::cout<<relevence[i]<<" ";
    }
    std::cout<<std::endl;
    
    double alterdcg = alterDCG(relevence);
    double alterndcg = alterNDCG(relevence);
    std::cout<<"Alter DCG Value: " << alterdcg << std::endl;
    std::cout<<"Alter NDCG Value: " << alterndcg <<std::endl;
    
    double dcg = DCG(relevence1);
    double ndcg = NDCG(relevence1);
    std::cout<<"DCG Value: " << dcg << std::endl;
    std::cout<<"NDCG Value: " << ndcg <<std::endl;
    return 0;
}




