#include <Arduino.h>
#include "xm_motor.h"

String comdata = "";  //蓝牙字符
void setup() {


  xm_can_start();                         //初始化can设置
  motor_enable(1);                        //使能id 1电机
  motor_pos_zero(1);                      //位置置0
  motor_mode(1, 1);                       //电机运行模式 电机canid 模式值 1位置模式2速度模式 3 电流模式0运控模式
  motor_pow_value(1, 5, 20, 0.2, 0.13);  //uint8_t id , float torque 位置模式速度限制 ,float limit_cur ,float  kp=0.8,float ki=0.13  id 速度 电流限制，kp,kd  速度 0~30rad/s 6.28rad 等于1圈  电流最大23A
  Serial.println("Example: Write to CAN");
}
void loop() {
    
  int speed_value = 200;
  int speed_valueb = map(speed_value, 0, 1023, 0, 30);  //前进模拟量
  float bb = (float)speed_value;
  bb = bb / 163.9423;
  if (bb > 6.2) { bb = 6.2; }
  motor_pos_value(1, 3.14);          //电机位置模式赋值，id，位置角度rad 2派=360度。

  // motor_speed_value(1, 1);

  delay(20);
}