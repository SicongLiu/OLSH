################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
CPP_SRCS += \
../metrics/metrics.cpp \
../metrics/rand.cpp 

OBJS += \
./metrics/metrics.o \
./metrics/rand.o 

CPP_DEPS += \
./metrics/metrics.d \
./metrics/rand.d 


# Each subdirectory must supply rules for building sources it contributes
metrics/%.o: ../metrics/%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: Cygwin C++ Compiler'
	g++ -O3 -Wall -c -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


