#include "kinematics.h"
#include <math.h>

kinematics::kinematics(int length, int width, int speed){
    this->chassis_L = length;
    this->chassis_W = width;
    this->limit_speed = speed;

}

void kinematics::move_cal(float f, float s, float r){
    R = sqrt(pow(chassis_L, 2) + pow(chassis_W, 2));

    FWD = f;                                                            // (forward/reverse command, -1 to +1)     (y-axis: go up or down)
    STR = s;                                                            // (strafe right command, -1 to +1)          (x-axis: go right or left)
    RCW = r;                                                            // (rotate clockwise command, -1 to +1)    (rotate)

    A = STR - RCW * (chassis_L/R);
    B = STR + RCW * (chassis_L/R);
    C = FWD - RCW * (chassis_W/R);
    D = FWD + RCW * (chassis_W/R);

    WS1 = sqrt(pow(B,2) + pow(C,2));                             // front-right speed
    WS2 = sqrt(pow(B,2) + pow(D,2));                             // front-left speed
    WS3 = sqrt(pow(A,2) + pow(D,2));                             // back-left speed
    WS4 = sqrt(pow(A,2) + pow(C,2));                             // back-right speed

    max_speed = max({WS1, WS2, WS3, WS4});

    if (max_speed > 1){
        WS1 = WS1 / max_speed;
        WS2 = WS2 / max_speed;
        WS3 = WS3 / max_speed;
        WS4 = WS4 / max_speed;
    }

    if (C == 0 and B == 0){
        WA1 = 0;
    }
    else{
        WA1 = round(atan2(B, C) * 180 / M_PI);
    }


    if (D == 0 and B == 0){
        WA2 = 0;
    }
    else{
        WA2 = round(atan2(B, D) * 180 / M_PI);
    }
        

    if (A == 0 and D == 0){
        WA3 = 0;
    } 
    else{
        WA3 = round(atan2(A, D) * 180 / M_PI);
    }
        

    if (A == 0 and C == 0){
        WA4 = 0;
    }
    else{
        WA4 = round(atan2(A, C) * 180 / M_PI);
    }

    WS1 = round(WS1 * limit_speed);
    WS2 = round(WS2 * limit_speed);
    WS3 = round(WS3 * limit_speed);
    WS4 = round(WS4 * limit_speed);

    if (WA1 < 0){
        WA1 = 360 + WA1;
    }
            
    if (WA2 < 0){
        WA2 = 360 + WA2;
    }

    if (WA3 < 0){
        WA3 = 360 + WA3;
    }
            
    if (WA4 < 0){
        WA4 = 360 + WA4;
    }

    if (r > 0 and s == 0 and f == 0){
        WA1 = 360 - 45;
        WA2 = 45;
        WA3 = 360 - 45;
        WA4 = 45;
        
        WS1 = -WS1;
        WS4 = -WS4;
    }


    if (r < 0 and s == 0 and f == 0){
        WA1 = 360 - 45;
        WA2 = 45;
        WA3 = 360 - 45;
        WA4 = 45;
        
        WS2 = -WS2;
        WS3 = WS3;
    }

    short_path(last_angle1, WA1, WS1);
    WA1 = short_path_val[0];
    WS1 = short_path_val[1];
    last_angle1 = WA1;
    
    short_path(last_angle2, WA2, WS2);
    WA2 = short_path_val[0];
    WS2 = short_path_val[1];
    last_angle2 = WA2;
    
    short_path(last_angle3, WA3, WS3);
    WA3 = short_path_val[0];
    WS3 = short_path_val[1];
    last_angle3 = WA3;
    
    short_path(last_angle4, WA4, WS4);
    WA4 = short_path_val[0];
    WS4 = short_path_val[1];
    last_angle4 = WA4;

    // printf("WS: %d %d %d %d WA: %d %d %d %d\n", (int)(WS1), (int)(WS2), (int)(WS3), (int)(WS4), (int)(WA1), (int)(WA2), (int)(WA3), (int)(WA4));
        
}

void kinematics::short_path(float last, float target, float speed){
    
    float inverse_angle = target + 180;
        
    if (inverse_angle > 360){
        inverse_angle -= 360;
    }
    else if(inverse_angle == 360){
        inverse_angle = 0;
    }
        
    float delta = abs(last - target);
    float inverse_delta = abs(last - inverse_angle);
    
    if (delta > 180){
        delta = 360 - delta;
    }
        
    if (inverse_delta > 180){
        inverse_delta = 360 - inverse_delta;
    }
        
        
    if (delta > inverse_delta){
        short_path_val[0] = inverse_angle;
        short_path_val[1] = -speed;
        // return short_path_val;
    }
        
    else{
        short_path_val[0] = target;
        short_path_val[1] = speed;
        // return short_path_val;
    }
        
}

void kinematics::mecanum_wheel_move(float x, float y, float w){
    denominator = abs(y) + abs(x) + abs(w);

    if (denominator < 1){
        denominator = 1;
    }

    frontLeftPower = 0;
    backLeftPower = 0;
    frontRightPower = 0;
    backRightPower = 0;

    if (denominator == 0){
        frontLeftPower = (y + x + w) * maxRPM;
        backLeftPower = (y - x + w) * maxRPM;
        frontRightPower = (y - x - w) * maxRPM;
        backRightPower = (y + x - w) * maxRPM;
    } 
    else{
        frontLeftPower = (y + x + w) / denominator * maxRPM;
        backLeftPower = (y - x + w) / denominator * maxRPM;
        frontRightPower = (y - x - w) / denominator * maxRPM;
        backRightPower = (y + x - w) / denominator * maxRPM;
    }
}