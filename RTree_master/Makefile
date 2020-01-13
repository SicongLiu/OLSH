.PHONY: all build test clean

CXXFLAGS=-Wall -Wextra -Wpedantic -std=c++11

all: build

build: out out/MyTest

out:
	mkdir -p out

max_list.o: max_list.h max_list.cc

gendef.o: gendef.h gendef.cc
#
#myentry.o: myentry.h myentry.cc

out/MyTest: MyTest.cpp RTree.h 
	$(CXX) -o $@ ${CXXFLAGS} $<


test: build
	./out/MyTest
#	./out/TestBadData baddata.txt
#	./out/MemoryTest

clean:
	rm -rf out
	
	
	
#
#.cc.o:
#	$(CC) $(CCOPTS) $<
#
#all: rtree
#
#rtree.o: rtree.cc rtree.h blk_file.h direntry.h direntry.cc gendef.h gendef.cc linlist.h linlist.cc rtdatanode.h rtdatanode.cc rtdirnode.h rtdirnode.cc rtnode.h rtnode.cc 
#
#blk_file.o: blk_file.cc blk_file.h
#
#main.o: main.cc rtree.h
#
#rtree: rtree.o blk_file.o main.o
#	$(LINK) -o rtree main.o rtree.o blk_file.o $(LINKOPTS)
#
#clean:
#	rm *o rtree core
