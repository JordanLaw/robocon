#include "pinmap.h"
#include "chassis.h"
#include <Arduino.h>
#include "motor.h"
#include "msg.h"
#include <Wire.h>
#include "clip.h"
#include "Adafruit_TCS34725.h"
#include <Adafruit_SSD1306.h>
#include <SPI.h>

// #define SERVOMIN 0
// #define SERVOMAX 1000

Adafruit_TCS34725 colorSensor(TCS34725_INTEGRATIONTIME_50MS, TCS34725_GAIN_4X);
// Adafruit_SSD1306 display(128, 64, &Wire);

const int colorTolerance = 50;
const int greenMax = 200;
int detectRed = 0;
int red = 0;

// int sda = 18;
// int scl = 19;

// uint8_t servonum = 1;

// int angleToPulse(int ang){
//    int pulse = map(ang,0, 180, SERVOMIN,SERVOMAX);// map angle of 0 to 180 to Servo min and Servo max 
//    Serial.print("Angle: ");Serial.print(ang);
//    Serial.print(" pulse: ");Serial.println(pulse);
//    return pulse;
// }

motor motor1(motor1_pwm, motor1_CWCCW); 
motor motor2(motor2_pwm, motor2_CWCCW);
motor motor3(motor3_pwm, motor3_CWCCW);
motor motor4(motor4_pwm, motor4_CWCCW);

// motor motor5(motor5_pwm, motor5_CWCCW);


// Adafruit_PWMServoDriver servo_driver = Adafruit_PWMServoDriver(0x40); 
// clip superclip(&motor5);

msg nanoMsg;

chassis superCar(&motor1, &motor2, &motor3, &motor4,true);

// void liftstop(){
//     motor5.setSpeed(0);
// }

void initializeColorSensor() {
  if (colorSensor.begin()) {
    Serial.println("Found sensor");
  } 
  else {
    Serial.println("No GY-33 found, check connections");
    
  }
}

// void initializeDisplay() {
//   if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
//     Serial.println(F("SSD1306 allocation failed"));
//     for (;;);
//   }
//   display.display();
//   delay(500); 
//   display.setTextSize(2);
//   display.setTextColor(WHITE);
//   display.setRotation(0);
// }

int readColorAndDisplay() {
  uint16_t r, g, b, clear, colorTemp, lux;
  int detectR = 0;

  colorSensor.getRawData(&r, &g, &b, &clear);
  colorTemp = colorSensor.calculateColorTemperature(r, g, b);
  lux = colorSensor.calculateLux(r, g, b);

  // display.clearDisplay();
  // display.setCursor(0, 0);

  // Serial.print("Color Temp: "); Serial.print(colorTemp, DEC); Serial.print(" K - "); 
  // Serial.print("Lux: "); Serial.print(lux, DEC); Serial.print(" - "); 
  // Serial.print("R: "); Serial.print(red, DEC); Serial.print(" ");
  // Serial.print("G: "); Serial.print(green, DEC); Serial.print(" ");
  // Serial.print("B: "); Serial.print(blue, DEC); Serial.print(" ");
  // Serial.print("C: "); Serial.print(clear, DEC); Serial.print(" ");
  // Serial.println(" ");

  if (r > b && r > 200 && r - b> colorTolerance && g < greenMax && clear < 1100) {
    // Serial.println("Red Ball: " + String(r));
    // display.println("Red Ball: " + String(r));
    detectR = 1;

  } else if (b > r && b > 200 && b - r > colorTolerance && clear < 1100) {
    // Serial.println("Blue Ball: " + String(b));
    // display.println("Blue Ball: " + String(b));
  } else {
    // Serial.println("NONE");
    // display.println("NONE");
    detectR = 0;
  }

//   display.display();
  return detectR;
}

void setup() {
    // Wire.begin();
    // Serial.begin(115200);
    nanoMsg.init(&Serial);
    initializeColorSensor();
    // initializeDisplay();
 }

void loop() {

    if (detectRed == 0){
      detectRed = readColorAndDisplay();
      delay(1500);

      if (detectRed == 1){
        Serial.println("red Ball: " + String(detectRed));
        colorSensor.disable();
      }
      else{
        Serial.println("NONE");

      }
    }

    if (detectRed == 1){
      if (!nanoMsg.read()){
        return;
      }

      superCar.move(nanoMsg.getX_speed(), nanoMsg.getY_speed(), nanoMsg.getW_speed());
    }

    // if (!nanoMsg.read()){
    //     return;
    //   }

    // superCar.move(nanoMsg.getX_speed(), nanoMsg.getY_speed(), nanoMsg.getW_speed());




// if(nanoMsg.get_isCloseClip()){

//     for( int angle =0; angle<181; angle +=5){
//         servo_driver.setPWM(servonum, 0, angleToPulse(angle) );
//         delay(100);
//     }
//     Serial.println("OPEN");
//     }

// else{

//     for( int angle =180; angle>0; angle -=5){
//         servo_driver.setPWM(servonum, 0, angleToPulse(angle) );
//         delay(100);
//     }
//     Serial.println("CLOSE");


//     }

// switch(nanoMsg.getLifting_status()){
// case 0x00:
// if(!digitalRead(upper_switch)){ 
//     superclip.liftUp();
//     Serial.println("UP");
// }
// else{
//     superclip.liftstop();
// }
// break;

// case 0x01:
// if(!digitalRead(bottom_switch)){
//     superclip.liftDown();
//     Serial.println("Down");
// }
// else{
// superclip.liftstop();
// }
// break;

// case 0x02:
// superclip.liftstop();
// break;

// default:
// break;

// }
}