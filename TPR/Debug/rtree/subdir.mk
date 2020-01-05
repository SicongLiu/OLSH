################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
CPP_SRCS += \
../rtree/entry.cpp \
../rtree/rtnode.cpp \
../rtree/rtree.cpp 

OBJS += \
./rtree/entry.o \
./rtree/rtnode.o \
./rtree/rtree.o 

CPP_DEPS += \
./rtree/entry.d \
./rtree/rtnode.d \
./rtree/rtree.d 


# Each subdirectory must supply rules for building sources it contributes
rtree/%.o: ../rtree/%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: Cygwin C++ Compiler'
	g++ -O0 -g3 -Wall -c -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


