
#include "motor_property.h"

motor_property::motor_property(){}

motor_property::motor_property(Motor_type type){
    switch(type){
        case m3508:
            //m3508 p19
            //MAX MRPM: 8500rpm
            //MAX current: 20.0A
            //Number of poles: 14
            //Gear ratio: 3591/187
            setAllparam(8500.0f, 20.0f, 14, (float)(3591.0f/187.0f));
            break;
        
        default:
            break;
    }
}

void motor_property::setAllparam(float rpm, float current, int polesNumber, float ratio){
    setMaxRPM(rpm);
    setMaxCurrent(current);
    setPolesNumber(polesNumber);
    setGearRatio(ratio);
}

motor_property::motor_property(float rpm, float current, int polesNumber, float ratio){
    setAllparam(rpm, current, polesNumber, ratio);
}

void motor_property::setMaxRPM(float rpm){
    maxRPM = rpm;
}

void motor_property::setMaxCurrent(float current){
    maxCurrent = current;
}

void motor_property::setPolesNumber(int number){
    polesNumber = number;
}

void motor_property::setGearRatio(float ratio){
    gear_ratio = ratio;
}

float motor_property::getMaxRPM(){
    return maxRPM;
}

float motor_property::getMaxCurrent(){
    return maxCurrent;
}

int motor_property::getPolesNumber(){
    return polesNumber;
}

float motor_property::getGearRatio(){
    return gear_ratio;
}