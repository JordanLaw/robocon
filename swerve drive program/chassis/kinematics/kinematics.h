#ifndef _KINEMATICS_H
#define _KINEMATICS_H

#include <mbed.h>

class kinematics{
    private:
        float chassis_L;
        float chassis_W;
        float limit_speed;

        float limit;
        
        float last_angle1;
        float last_angle2;
        float last_angle3;
        float last_angle4;

        float R;
        float FWD;
        float STR;
        float RCW;

        float A;
        float B;
        float C;
        float D;

        float max_speed;

        float short_path_val[2];

        // mecanum wheel control
        float maxRPM = 3500;
        float denominator;

    public:
        float WS1;
        float WS2;
        float WS3;
        float WS4;

        float WA1;
        float WA2;
        float WA3;
        float WA4;

        float frontLeftPower;
        float backLeftPower;
        float frontRightPower;
        float backRightPower;
        
        kinematics(int length, int width, int speed);

        void move_cal(float f, float s, float r);

        void short_path(float last, float target, float speed);

        void mecanum_wheel_move(float x, float y, float w);
};

#endif