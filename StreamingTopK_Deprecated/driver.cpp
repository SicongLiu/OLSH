//
//  driver.cpp
//  StreamingTopK
//
//  Created by Sicong Liu on 10/20/17.
//  Copyright © 2017 Sicong Liu. All rights reserved.
//

#include"TreeIndex.h"
#include"RTree.h"
#include<iostream>
#include<cmath>
#include<fstream>
#include<sstream>
#include<algorithm>
#include<string>
#include<vector>
#include<set>
#include<numeric>      // std::iota
#include<cfloat>
#include<limits>
#include<ctime>
using namespace std;

vector<double> queryNorm(vector<double> queryData, int W)
{
    double norm = 0;
    for (int i = 0; i < W; i++) {
        norm += queryData.at(i) *queryData.at(i);
    }
    for (int i = 0; i < W; i++) {
        queryData.at(i) = queryData.at(i) / sqrt(norm);
    }
    return queryData;
}
vector<double> loadQueryData(string fileName, int index) {
    vector<double> queryData;
    /*Initializing label and database data*/
    int lineCount = 0;
    cout << "Reading from file: " << fileName << endl;
    ifstream infile(fileName);
    string token;
    string line;
    
    while (getline(infile, line)){
        
        
        if (lineCount == (index - 1)) {
            istringstream ss(line);
            int columnCount = 0;
            while (getline(ss, token, ',')) {
                if (columnCount == 0) {// first column and input data is cluster label
                }
                else {
                    queryData.push_back(atof(token.c_str()));
                }
                columnCount++;
            }
        }
        lineCount++;
    }
    cout << "Query data init done. " << endl;
    return queryData;
        
    
}


int main()
{
    double dataPer = 0.1;
    int classNum = 6;
    int dataPerClass = 50;
    int pivot = 0;
    // vector<int> testIndex = { 1, 2, 3, 4, 5, 51, 52, 53, 54, 55, 101, 102, 103, 104, 105, 151, 152, 153, 154, 155, 201, 202, 203, 204, 205, 251, 252, 253, 254, 255 };
    vector<int> testIndex;
    for (int i = 0; i < classNum; i++) {
        int tempIndex = dataPerClass * dataPer;
        for (int j = pivot; j < pivot + tempIndex; j++) {
            testIndex.push_back(j + 1);
        }
        pivot = pivot + dataPerClass;
    }
    
    // Regular TA Algorithm
    int round1 = 0;
    int round2 = 0;
    
    // int W = 10;
    int W = 2;
    // int K = 5;
    
    int K = testIndex.size();
    string fileName = "synthetic_control_Test";
    
    // load query data
    vector<double> queryData1 = loadQueryData(fileName, 41);
    //vector<double> queryData2 = loadQueryData(fileName, 42);
    vector<double> queryData2 = queryData1;
    //queryData2.at(0) = 0.95;
    queryData2.at(1) = 0.9;
    
    // normalize query data:
    //queryData1 = queryNorm(queryData1, W);
    //queryData2 = queryNorm(queryData2, W);
    
    TreeIndex TKS1(fileName, queryData1, W, K, testIndex);
    // TopKStream TKS(fileName, queryData, W, K);
    
    clock_t TABegin = clock();
    TKS1.TAAlgorithm(round1);
    clock_t TAEnd = clock();
    cout << "TA Algorithm Time(ms): " << double(TAEnd - TABegin) / 1000 << endl;
    TKS1.TAoutputTopK();
    
    TKS1.postRank();
    
    // TKS1.outputMatrixTest(TKS1.getDistMatrix());
    
    // for linear scan
    // TKS1.deltaComp();
    // TKS1.twoDimension(queryData1, queryData2);
    
    // for RTree test
    // vector<float> hyperplane = TKS1.deltaCompRTree(queryData1);
    TKS1.deltaCompRTreeHyperPlane(queryData1);
    TKS1.twoDimensionRTreeHyperPlane(queryData1, queryData2);
    
    
    
    TreeIndex TKS2(fileName, queryData2, W, K, testIndex);
    TKS2.TAAlgorithm(round2);
    
    TKS2.TAoutputTopK();
    cout << "TA Algorithm done" << endl;
    // TA Algorithm finished
    
    system("pause");
    return 0;
}

