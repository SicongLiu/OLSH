CC=gcc
CXX=g++
RM=rm -f
CPPFLAGS=-g $(shell python-config --cflags) -I/usr/local/Cellar/numpy/1.13.3/lib/python3.6/site-packages/numpy/core/include
# INC=-I/usr/local/Cellar/numpy/1.13.3/lib/python3.6/site-packages/numpy/core/include
# INC=-I/usr/local/Cellar/numpy/1.14.0/lib/python3.6/site-packages/numpy/core/include

LDFLAGS=-g $(shell python-config --ldflags)
LDLIBS=$(shell python-config --libs)

SRCS=Skyline.cpp
OBJS=$(subst .cc,.o,$(SRCS))

Skyline: Skyline.o
	# $(CXX) $(CPPFLAGS) -o Skyline Skyline.cpp
	$(CXX) $(CPPFLAGS) -o Skyline Skyline.o $(LDFLAGS) pymodule.c