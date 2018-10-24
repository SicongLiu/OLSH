1. NBA Data is from http://www.basketballreference.com, it has been tested and used in "The Hybrid-Layer Index: A Synergic Approach to Answering Top-K Queries in Arbitrary Subspaces".

2. Originally it has 30 column fields:

1 - Rank
2 - Name
3 - Position
4 - Age
5 - Team
6 - G
7 - GS
8 - MP
9 - FG
10 - FGA
11 - FG%
12 - 3P
13 - 3PA
14 - 3P%
15 - 2P
16 - 2PA
17 - 2P%
18 - eFG% 
19 - FT
20 - FTA
21 - FT%
22 - ORB
23 - DRB
24 - TRB
25 - AST
26 - STL
27 - BLK
28 - TOV
29 - PF
30 - PTS

3. Files can be downloaded from the website season by season, will need to be pre-processed to be used in our scenario

Points, rebounds, assistants, steal, block, turn-over, personal fouls (PF), FGA (field goal attempt), FTA(free throw attempt)


https://www.basketball-reference.com/leagues/NBA_2018_totals.html

Need to select hide partial rows -> to delete duplicate, only showing the total stats for a player


For House data, we the instruction is here: 

https://www.wellesley.edu/sites/default/files/assets/departments/libraryandtechnology/files/ris/how_to_download_ipums_data_and_open_it_in_stata.pdf

And here:

https://usa.ipums.org/usa/extract_instructions.shtml


https://usa.ipums.org/usa/data.shtml




========================================================================================================================



Hi man about the dataset, I think you got the info about dimentions in the paper  where you found the datasets:

- http://kdd.ics.uci.edu/: this is a collection of dataset for all the knowledge data discovery tasks.
http://kdd.ics.uci.edu/summary.data.alphabetical.html I cannot find Color do you  mean COREL?
Corel Image Features
by application area it fiigure as good for indexing http://kdd.ics.uci.edu/summary.data.application.html

This dataset contains image features extracted from a Corel image collection. Four sets of features are available based on the color histogram, color histogram layout, color moments, and co-occurence texture. 
http://kdd.ics.uci.edu/databases/CorelFeatures/CorelFeatures.data.html

I think this dataset  can be useful for us  just   point me the paper that uses it in such a way that we can know what pre-processing have to be done.


******************************
- https://www.ipums.org/ please point me the paper  that uses  the dataset. This are survay data  there should be a sort of pre-processing to  do  some sort of mapping also the groundtruth. 

from the paper  Maximum Rank Query from 2015 VLDB: HOUSE (from ipums.org) contains 315,265 records; each holds six values that represent an American family’s spendings in gas, electricity, water, heating, insurance, and property tax 

IPUMS provides census and survey data from around the world integrated across time and space. IPUMS integration and documentation makes it easy to study change, conduct comparative research, merge information across data types, and analyze individuals within family and community context. Data and services available free of charge. 

https://usa.ipums.org/usa-action/variables/group?id=h-econ
select household and then the  economic characteristic  that are relevant.

We can get this data but then  what is the groundtruth???


**********************************
Movieleng  can be good I need to register to go on for it.