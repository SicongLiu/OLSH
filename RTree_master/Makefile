#.PHONY: all build test clean
#
#CXXFLAGS=-Wall -Wextra -Wpedantic -std=c++11
#
#all: build
#
#build: out out/MyTest
#
#out:
#	mkdir -p out
#
#max_list.o: max_list.h max_list.cpp
#
## gendef.o: gendef.h gendef.cc
##
## myentry.o: myentry.h myentry.cc
#
#out/MyTest: MyTest.cpp RTree.h gendef.h 
#	$(CXX) -o $@ ${CXXFLAGS} $<
#
#
#test: build
#	./out/MyTest
#
#clean:
#	rm -rf out
	
	
	
SRCS=max_list.cpp MyTest.cpp
OBJS=${SRCS:.cc=.o}

CXX=g++ -std=c++11
# CPPFLAGS=-w -O3
CPPFLAGS=-g -O0

.PHONY: clean

all: ${OBJS}
	${CXX} ${CPPFLAGS} -o rtree_main ${OBJS}

max_list.o: max_list.h

gendef.o: gendef.h

main.o: MyTest.cpp RTree.h

clean:
	-rm ${OBJS} rtree_main
