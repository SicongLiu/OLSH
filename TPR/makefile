############### Linux ########################
##CC       = g++
##CCOPTS   = -c -I/usr/include/X11R5 -I/usr/X11R6/include -I/usr/include/Motif1.2 -g -DLINUX
##LINK     = g++
###
##LINKOPTS = -static -L/usr/lib/Motif1.2 -L/usr/lib/X11R5 -lm 
##############################################
#
#
#
############### HP-UX ########################
#CC       = g++
#CCOPTS   = -c -O -I/usr/include/X11R5 -I/usr/X11R6/include -I/usr/include/Motif1.2 -g -DHPUX
#LINK     = g++
#
#LINKOPTS = -L/usr/lib/Motif1.2 -L/usr/lib/X11R5 -lm -lXm -lXt -lX11 -lXext -lXhp11
##############################################
#
#.cc.o:
#	$(CC) $(CCOPTS) $<
#
#all: rtree
#
#rtree.o: ./rtree/rtree.cc ./rtree/rtree.h blk_file.h 
#
#blk_file.o: blk_file.cc blk_file.h
#
#main.o: main.cc ./rtree/rtree.h
#
#rtree: rtree.o entry.o main.o
#	$(LINK) -o rtree main.o rtree.o blk_file.o $(LINKOPTS)
#
#clean:
#	rm *o rtree core

SRCS=./blockfile/blk_file.cpp ./blockfile/cache.cpp ./func/functions.cpp ./heap/heap.cpp ./linlist/linlist.cpp ./metrics/metrics.cpp ./metrics/rand.cpp ./rtree/entry.cpp \
        ./blockfile/max_list.cpp ./rtree/myentry.cpp ./rtree/rtnode.cpp ./rtree/rtree.cpp main.cpp
OBJS=${SRCS:.cc=.o}

CXX=g++ #-std=c++11
# CPPFLAGS=-w -O3
CPPFLAGS=-g -O0

.PHONY: clean

all: ${OBJS}
		${CXX} ${CPPFLAGS} -o rtree_main ${OBJS}

blockfile.o: ./blockfile/blk_file.h ./blockfile/cache.h

function.o: ./func/gendef.h

heap.o: ./heap/heap.h

linlist.o: ./linlist/linlist.h

metrics.o: ./metrics/metrics.h ./metrics/rand.h

rtree.o: ./rtree/entry.h ./rtree/rtnode.h ./rtree/rtree.h ./rtree/myentry.h ./blockfile/max_list.h

main.o: 

clean:
		-rm ${OBJS} rtree_main