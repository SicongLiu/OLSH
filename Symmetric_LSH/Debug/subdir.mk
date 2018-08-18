################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
CPP_SRCS += \
../BucketHashing.cpp \
../Geometry.cpp \
../GlobalVars.cpp \
../LSHMain.cpp \
../LocalitySensitiveHashing.cpp \
../NearNeighbors.cpp \
../Random.cpp \
../SelfTuning.cpp \
../Util.cpp \
../compareOutputs.cpp \
../convertMNIST.cpp \
../exactNNs.cpp \
../genDS.cpp \
../genPlantedDS.cpp 

OBJS += \
./BucketHashing.o \
./Geometry.o \
./GlobalVars.o \
./LSHMain.o \
./LocalitySensitiveHashing.o \
./NearNeighbors.o \
./Random.o \
./SelfTuning.o \
./Util.o \
./compareOutputs.o \
./convertMNIST.o \
./exactNNs.o \
./genDS.o \
./genPlantedDS.o 

CPP_DEPS += \
./BucketHashing.d \
./Geometry.d \
./GlobalVars.d \
./LSHMain.d \
./LocalitySensitiveHashing.d \
./NearNeighbors.d \
./Random.d \
./SelfTuning.d \
./Util.d \
./compareOutputs.d \
./convertMNIST.d \
./exactNNs.d \
./genDS.d \
./genPlantedDS.d 


# Each subdirectory must supply rules for building sources it contributes
%.o: ../%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	g++ -O0 -g3 -Wall -c -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.d)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


