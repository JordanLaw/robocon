#include "mbed.h"
#include "vesc.h"

#ifndef _MODULE_H
#define _MODULE_H

class module{

    private:
        vesc* direction;
        vesc* rpm;

        float kp;
        float ki;
        float kd;

        float gear_ratio = 1;


    public:
        module(vesc* direction, vesc* rpm);
        void module_set_mrpm(float mrpm);
        void module_set_direction(float pos);
        void module_set_gearratio(float new_gear_ratio);

        float module_get_mrpm();
        float module_get_direction();

        // void setXXX(float para);
        // float getXXX();
};

#endif 