#ifndef COMMUNICATION_FORMAT_H
#define COMMUNICATION_FORMAT_H

#include "mbed.h"

int8_t start_byte = 0x7f;
int8_t zero_byte = 0x9f;

struct robot_msg
{
  int8_t startByte = (int8_t)start_byte;

  uint8_t voltage[4];
  uint8_t rpm[4];
  uint8_t angle[4];
  int8_t setting_num = 0x00;
  int8_t error_Flag = 0x00;
};

struct remote_msg
{
  int8_t startByte = (int8_t)start_byte;
  int8_t x = 0x00;
  int8_t y = 0x00;
  int8_t w = 0x00;
  int8_t operation1 = 0x00; // operation1 Up=0, Down=1, Left=2, Right=3, A=4, B=5, X=6, Y=7,
  int8_t operation2 = 0x00; // operation2 L1=0, L2=1, R1=2, R2=3, LjoystickSW=4, RjoystickSW=5, 
  int8_t operation3 = 0x00; // Estop=0, Reset=1, hold=2

  uint8_t up_flag, down_flag, Left_flag, Right_flag, A_flag, B_flag, X_flag, Y_flag, L1, L2, R1, R2, LjoystickSW, RjoystickSW, ESTOP, Reset_button, Home = 0;
};

#endif