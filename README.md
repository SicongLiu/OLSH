# OLSH: Onion LSH

Version: 1.0.0

Release date: 01-02-2019


Introduction
--------

This implementation is written in C++, which provides an angular LSH framework 
using Onion layer technique based on Simple LSH[1].


DataSet
--------

* NBA: https://www.basketball-reference.com

* HOUSE: https://www.ipums.org

* Synthetic Data Generator: We modified the original implementation from original github folder: https://github.com/sofiabravo103/builder, and the revised version of synthetic data generator is listed in this github repository as Synthetic_Data_Gen.cpp


CodeBase
--------

We adopted the implemention of Simple LSH from paper[2] of 2018 SIGKDD, with github link: https://github.com/HuangQiang/H2_ALSH

Authors
--------

* **Sicong Liu**

  Arizona State University,
  
  Tempe, USA 
  
  s.liu@asu.edu
  
* **Silvestro R. Poccia**

  University of Turin,
  
  Turin, Italy
  
  poccia@di.unito.it


Relevant Papers
--------

The paper for the package of OLSH has been submitted in VLDB 2019 which is 
displayed as follows:

* **Sicong Liu, Silvestro R. Poccia, K. Selçuk Candan, Maria Luisa Sapino. 
OLSH: Onion-LSH with Layer-Aware Resource Allocation for Approximate Top-K Query Processing. VLDB 2019**


References
--------

[1] Neyshabur, Behnam, and Nathan Srebro. "On symmetric and asymmetric LSHs for inner product search." arXiv preprint arXiv:1410.5518 (2014).

[2] Qiang Huang, Guihong Ma, Jianlin Feng, Qiong Fang, and Anthony K. H. Tung. Accurate and Fast Asymmetric Locality-Sensitive Hashing Scheme for Maximum Inner Product Search. SIGKDD, pages 1561-1570, 2018.

