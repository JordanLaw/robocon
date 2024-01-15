#include "chassis.h"

chassis ::chassis(motor* fl, motor *fr,motor *bl,motor *br, bool isTypex ){
        this->fl =fl;
        this->fr=fr;
        this->bl =bl;
        this->br =br;
        this->isTypex=isTypex;
}

void chassis::setType(bool isTypex){
    this->isTypex=isTypex;
}

void chassis ::move(int x,int y,int w){
    int8_t frontLeftMotor =y + x + w;
    int8_t backLeftMotor = y-x+w;
    int8_t frontRightMotor= y-x-w;
    int8_t backRightMotor= y+x-w;

    Serial.printf("fl: %d, bl: %d, fr: %d, br: %d\n\r", (int8_t)frontLeftMotor, (int8_t)backLeftMotor, (int8_t)frontRightMotor, (int8_t)backRightMotor);
///////
    if(frontLeftMotor > 0){
        fl->setDirection(false);
        }
        else{
        fl->setDirection(true);
        }  

        fl->setSpeed(abs(frontLeftMotor));
////////
    if(frontRightMotor > 0){
        fr->setDirection(true); 
        }
        else{
        fr->setDirection(false);
        } 

        fr->setSpeed(abs(frontRightMotor));
///////
    if(backLeftMotor > 0){
        bl->setDirection(false); 
        }
        else{
        bl->setDirection(true);
        } 

        bl->setSpeed(abs(backLeftMotor));

////
    if(backRightMotor > 0){
        br->setDirection(true); 
        }
        else{
        br->setDirection(false);
        } 
        br->setSpeed(abs(backRightMotor));

}

  