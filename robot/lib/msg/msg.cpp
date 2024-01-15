#include "msg.h"

void msg::init(HardwareSerial* serial){ 
    nano = serial;
    nano->begin(115200);
}

bool msg::read(){
if(!nano->available()){
     return false;
}

if (nano->read() != start_byte){ 
    return false;
}

    x_speed =(int)nano->read();
    y_speed =(int)nano->read();
    w_speed =(int)nano->read();

    isCloseClip=(int)nano->read();
    lifting_status=(int)nano->read();

    nano->printf("x: %d, y: %d, w: %d", x_speed, y_speed, w_speed);

    return true;

}
int msg ::getX_speed(){
    return x_speed;
}
int msg ::getY_speed(){
    return y_speed;
}
int msg ::getW_speed(){
    return w_speed;
}

bool msg::get_isCloseClip(){
    return  isCloseClip;
}
int msg::getLifting_status(){
    return  lifting_status;
}