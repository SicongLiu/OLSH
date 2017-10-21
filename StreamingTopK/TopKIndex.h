//
//  TopKIndex.h
//  StreamingTopK
//
//  Created by Sicong Liu on 10/20/17.
//  Copyright © 2017 Sicong Liu. All rights reserved.
//

#ifndef TopKIndex_h
#define TopKIndex_h

#include<iostream>
#include<string>
#include<unordered_map>
#include<vector>
#include<set>

class TopKIndex
{
protected:
    std::string fileName;
    int W;                                        // window size
    int curTimeStamp;                            // current time stamp
    int curCount;                                //
    int K;
    double theta;                                // current threshold of Top-K resuls
    double maxDist;                                // current max Dist for the Top-K query results
    
    std::vector<std::vector<double>> backDistMatrix; // once distMatrix is computed, clear "data" in memory
    // distMatrix: sorted distance, column indexed instead of data row indexed
    std::vector<int> label;                        // initialize during inti()
    std::vector<double> queryData;
    std::vector<std::vector<double>> data;
    std::vector<std::vector<double>> distMatrix; // once distMatrix is computed, clear "data" in memory
    // distMatrix: sorted distance, column indexed instead of data row indexed
    std::vector<std::vector<double>> deltaDist; // once distMatrix is computed, clear "data" in memory
    // distMatrix: sorted distance, column indexed instead of data row indexed
    std::vector<double> seenDist;
    std::vector<int> sortedObjIndex;
    std::vector<int> TopKVector;                // maintin the insertion order of TASeen set, destroy after TAAlgorithm
    std::vector<std::set<int>> seen;            // seen objects for each window W step
    // std::vector<double> threshold;
    
    std::vector<std::vector<int>> sortedDistIndex;// keep sorted index for each column
    // std::vector<std::vector<double>> sortedDist;// keep sorted index for each column -- use as distMatrix
    std::vector<double> windowThreshold;
    
    RTree<int, float, 2, float> tree;
public:
    TopKIndex();
    TopKIndex(std::string fileName, std::vector<double> queryData, int W, int K);
    TopKIndex(std::string fileName, std::vector<double> queryData, int W, int K, std::vector<int> index);
    ~TopKIndex();
    
    void init();                                        // load data into memory, initialize data label, init distMatrix, B Tree, TA algorithm, seen, threshold
    void partialInit(std::vector<int> index);            // partial intial for testing only
    void TAAlgorithm(int &round);
    void sort_indexes(int windowIndex);
    void outputVectorTest(std::vector<int> tVector);
    void outputMatrixTest(std::vector<std::vector<double>> tMatrix);
    void TAoutputTopK();
    void euclideanDist(int start);
    void euclideanDist(int queryDataIndex, int dataIndex);
    void dotProduct(int start);
    void deltaComp();
    std::vector<float> deltaCompRTree(std::vector<double> queryData1);
    void deltaCompRTreeHyperPlane(std::vector<double> queryData1);
    void twoDimension(std::vector<double> queryData1, std::vector<double> queryData2);    // now testing for 2D condition
    void twoDimensionRTree(std::vector<double> queryData1, std::vector<double> queryData2, std::vector<float> hyperplane);    // now testing for 2D condition
    void twoDimensionRTreeHyperPlane(std::vector<double> queryData1, std::vector<double> queryData2);    // now testing for 2D condition
    
    // void findHyperPlaneTwoDimension(std::vector<double> q1, std::vector<double> q2); // build hyperplane
    void postRank();
    // void rankAll();    // sort and rank the aggregation of all data, re-order --
    
    std::set<int> compCurrentSeen(std::vector<std::vector<int>> sortedDistIndex, int count, int window);
    std::vector<double> sort_indexes(std::vector<double> v);
    std::vector<int> getLabel();
    std::vector<std::vector<double>> getData();
    std::vector<std::vector<double>> getDistMatrix();
    
    double plain_DTW(std::vector<double> AA, std::vector<double> BB, int r);  // DTW compuation from UCR_suite, no early termination
    double vectorSum(std::vector<double> v);
    double vectorSum(double* v);
    double vectorSum(std::vector<std::vector<double>> distMatrix, int count, int window);
    bool checkMember(int windowIndex, int obj);    // check if an element is seen in the OTHER WINDOWS in data structure "seen"
    bool checkMember(int obj);    // check if an element is seen in the OTHER WINDOWS in data structure "seen"
    bool checkMember(std::set<int> myVector, int myID);
    bool checkMember(std::vector<int> myVector, int myID);
    static bool MySearchCallback(int id, void* arg) {
        std::cout << "Hit data rect " << id << "\n";
        return true; // keep going
    }
};

#endif /* TopKIndex_h */
