SOURCES_DIR:=sources
OBJ_DIR:=bin
OUT_DIR:=bin
TEST_DIR:=$(SOURCES_DIR)
MY_VARIABLE := mips
export WTF=test_mips; 

#H_SOURCES:=`find $(SOURCES_DIR) -name "*.h"`
#CPP_SOURCES:=`find $(SOURCES_DIR) -name "*.cpp"`
#TEST_SOURCES:=`find $(TEST_DIR) -name "*.cpp"`
OBJ_SOURCES:=$(SOURCES_DIR)/BucketHashing.cpp \
	     $(SOURCES_DIR)/Geometry.cpp \
	     $(SOURCES_DIR)/LocalitySensitiveHashing.cpp \
	     $(SOURCES_DIR)/Random.cpp \
	     $(SOURCES_DIR)/Util.cpp \
	     $(SOURCES_DIR)/GlobalVars.cpp \
	     $(SOURCES_DIR)/SelfTuning.cpp \
	     $(SOURCES_DIR)/NearNeighbors.cpp

LSH_BUILD:=LSHMain

TEST_BUILDS:=exactNNs \
            genDS \
	    compareOutputs \
	    genPlantedDS

GCC:=g++ -O3
OPTIONS =  -DREAL_FLOAT $$MIPS # -DDEBUG
# -march=athlon -msse -mfpmath=sse
LIBRARIES:=-lm; 
#-ldmalloc

MIPS_OPT_EXTRACTOR = true  #if [ $* == mips ] ; then export MIPS=-DPERFORM_NEYSHABUR_MIPS; else export MIPS=-DNO_MIPS; fi; echo $$MIPS
export MIPS=-DPERFORM_NEYSHABUR_MIPS 

CC = $$MYCOMPILER $(OPTIONS)
CXX = $$MYCOMPILER $(OPTIONS) 

binaries_%:
	$(MIPS_OPT_EXTRACTOR);\
	$(MAKE) c && $(MAKE) ct

c:
	@mkdir -p $(OUT_DIR)
	$(GCC) -o $(OUT_DIR)/$(LSH_BUILD) $(OPTIONS) $(OBJ_SOURCES) $(SOURCES_DIR)/$(LSH_BUILD).cpp $(LIBRARIES)
	chmod g+rwx $(OUT_DIR)/$(LSH_BUILD)

ct:
	@mkdir -p $(OUT_DIR)
	(for i in $(TEST_BUILDS); do \
	 $(GCC) -o $(OUT_DIR)/$$i $(OPTIONS) $(OBJ_SOURCES) $(TEST_DIR)/$${i}.cpp $(LIBRARIES); chmod g+rwx $(OUT_DIR)/$$i; done)
