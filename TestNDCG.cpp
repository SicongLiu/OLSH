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

double NDCG_1(std::vector<double> relevence, std::vector<double> ground_truth)
{
    double dcg = 0;
    double ideal = 0;
    for(int i=0; i<relevence.size(); i++)
    {
        int rankIndex = i + 1;
        dcg += relevence.at(i)/std::log2(rankIndex + 1);
        ideal += ground_truth.at(i)/std::log2(rankIndex + 1);
    }
    return dcg/ideal;
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

double NDCG_2(std::vector<double> relevence, std::vector<double> ground_truth)
{
    double dcg = 0;
    double ideal = 0;
    for(int i=0; i<relevence.size(); i++)
    {
        int rankIndex = i + 1;
        dcg += (std::pow(2, relevence.at(i)) - 1 )/std::log2(rankIndex + 1);
        ideal += (std::pow(2, ground_truth.at(i)) - 1 )/std::log2(rankIndex + 1);
    }
    return dcg/ideal;
}

int main()
{
    /*static const double arr[] = {3,2,3,0,1,2};
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
    std::cout<<"NDCG Value: " << ndcg <<std::endl;*/
    //Ground Truth:  1.696900,  1.694765,  1.671995,  1.665944,  1.658606, query returned:  1.696900,  1.694765,  1.671995,  1.665944,  1.658606,
    // Ground Truth:  0.753326,  0.746245,  0.742675,  0.733187,  0.732304, query returned:  0.000000,  0.000000,  0.000000,  0.000000,  0.000000,
    static const double arr_relevance[] = {0.919739,  0.918154,  0.915374,  0.910382,  0.909635,  0.907417,  0.905106,  0.903858,  0.903201,  0.900712,  0.900379,  0.000000,  0.000000,  0.000000,  0.000000,  0.000000,  0.000000,  0.000000,  0.000000,  0.000000,  0.000000,  0.000000,  0.000000,  0.000000,  0.000000};
    static const double arry_ground_truth[] = {0.919739,  0.918154,  0.915374,  0.910382,  0.909635,  0.907417,  0.905106,  0.903858,  0.903201,  0.900712,  0.900379,  0.899134,  0.897717,  0.896778,  0.896463,  0.894955,  0.894251,  0.893711,  0.893619,  0.892640,  0.892035,  0.891872,  0.891386,  0.890586,  0.889269};
    std::vector<double> relevance;
    std::vector<double> ground_truth;
    int k = 25;
    for(int i = 0; i < k; i ++)
    {
        relevance.push_back(arr_relevance[i]);
        ground_truth.push_back(arry_ground_truth[i]);
    }
    
    std::cout<<"NDCG_1 Value: " << NDCG_1(relevance, ground_truth) << std::endl;
    std::cout<<"NDCG_2 Value: " << NDCG_2(relevance, ground_truth) << std::endl;
    
    
    
    return 0;
}


