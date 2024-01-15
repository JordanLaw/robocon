#include <motor.h>
#include <Arduino.h>

motor::motor(uint8_t pwm_pin, uint8_t direction_pin){ 
  this->pwm_pin = pwm_pin;
  this->direction_pin = direction_pin;

  pinMode(pwm_pin, OUTPUT);
  pinMode(direction_pin, OUTPUT);
  setSpeed(0);
  setDirection(true);
}
void motor::setReversed (bool isReversed){
this->isReversed = isReversed;
}

int motor::limited(int value, int maximum_value, int minimum_value){ 
  if (value >=maximum_value){
    value=maximum_value;
  }else if(value<=minimum_value){
    value=minimum_value;
  }
  return value;
}

void motor::setSpeed(int pwm){
 this->pwm = pwm;

this->pwm = limited(this->pwm,100,0);

int value =map(this->pwm, 0, 100, 0, 255);


analogWrite(pwm_pin,value);
}
int motor::getSpeed(){
    return pwm;
}

void motor::setDirection(bool isCW){
  this->isCW= isCW;

  if(isReversed){
  this->isCW = !this->isCW;
  }

  if(isCW){
digitalWrite(this->direction_pin, HIGH);
  }
  else{
digitalWrite(this->direction_pin, LOW);
  }
}
bool motor::getDirection(){
    return isCW;
}


void motor :: setPWMPin(int pin){
    this->pwm_pin =pin;
}
void motor :: setCWCCWPin(int pin){
    this->direction_pin=pin;
}

