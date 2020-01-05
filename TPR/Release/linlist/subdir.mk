################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
CPP_SRCS += \
../linlist/linlist.cpp 

OBJS += \
./linlist/linlist.o 

CPP_DEPS += \
./linlist/linlist.d 


# Each subdirectory must supply rules for building sources it contributes
linlist/%.o: ../linlist/%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: Cygwin C++ Compiler'
	g++ -O3 -Wall -c -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


