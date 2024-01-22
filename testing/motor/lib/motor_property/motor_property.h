#ifndef _MOTOR_PROPERTY_H
#define _MOTOR_PROPERTY_H

#include "mbed.h"   

typedef enum{
    m3508               = 1,
} Motor_type;

class motor_property{
    private:
        float maxRPM;
        float maxCurrent;
        int polesNumber;
        float gear_ratio; 

        void setAllparam(float rpm, float current, int polesNumber, float ratio);

    public:
        motor_property();
        motor_property(Motor_type type);
        motor_property(float rpm, float current, int polesNumber, float ratio);    

        void setMaxRPM(float rpm);
        void setMaxCurrent(float current);
        void setPolesNumber(int number);
        void setGearRatio(float ratio);

        float getMaxRPM();
        float getMaxCurrent();
        int getPolesNumber();
        float getGearRatio();
};

#endif