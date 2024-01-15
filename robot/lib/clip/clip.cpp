#include "clip.h"

clip::clip(motor* lifter){
    this->lifter = lifter;
//this->servo_driver = servo_driver;

// this->servo_driver->begin();
// this->servo_driver->setOscillatorFrequency(27000000);
// this->servo_driver->setPWMFreq(50);
}

void clip::set_num_channel(int num){
    num_channel = num;
}

// void clip::openclip(){

// servo_driver->setPWM(num_channel, 0, 10);

// }

// void clip::closeClip(){

// servo_driver->setPWM(num_channel, 0, 10);

// }

void clip::liftUp(){
    lifter->setDirection(false); 
    lifter->setSpeed(30);
}


void clip::liftDown(){
    lifter->setDirection(true); 
    lifter->setSpeed(30);
}

void clip::liftstop(){
    lifter->setSpeed(0);
}