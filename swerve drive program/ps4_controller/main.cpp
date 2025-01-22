#include "Arduino.h"
#include <PS4Controller.h>
#include "esp_bt_main.h"
#include "esp_bt_device.h"
#include "esp_gap_bt_api.h"
#include "esp_err.h"

#include <mcp2515.h>

unsigned long lastTimeStamp = 0;

MCP2515 mcp2515(5);
struct can_frame canMsg1;
struct can_frame canMsg2;

void notify()
{
  // char messageString[200];
  // sprintf(messageString, "%4d,%4d,%4d,%4d,%3d,%3d,%3d,%3d,%3d,%3d,%3d,%3d,%3d,%3d,%3d,%3d,%3d,%3d,%3d,%3d,%3d,%3d,%3d,%3d",
  // PS4.LStickX(),
  // PS4.LStickY(),
  // PS4.RStickX(),
  // PS4.RStickY(),
  // PS4.Left(),
  // PS4.Down(),
  // PS4.Right(),
  // PS4.Up(),
  // PS4.Square(),
  // PS4.Cross(),
  // PS4.Circle(),
  // PS4.Triangle(),
  // PS4.L1(),
  // PS4.R1(),
  // PS4.L2(),
  // PS4.R2(),  
  // PS4.Share(),
  // PS4.Options(),
  // PS4.PSButton(),
  // PS4.Touchpad(),
  // PS4.Charging(),
  // PS4.Audio(),
  // PS4.Mic(),
  // PS4.Battery());

  //Only needed to print the message properly on serial monitor. Else we dont need it.
  // if (millis() - lastTimeStamp > 50)
  // {
  //   Serial.println(messageString);
  //   lastTimeStamp = millis();
  // }


}

void onConnect()
{
  Serial.println("Connected!.");
}

void onDisConnect()
{
  Serial.println("Disconnected!.");    
}

void setup() 
{
  PS4.begin();  
  uint8_t pairedDeviceBtAddr[20][6];  
  int count = esp_bt_gap_get_bond_device_num();
  esp_bt_gap_get_bond_device_list(&count, pairedDeviceBtAddr);
  for(int i = 0; i < count; i++) 
  {
    esp_bt_gap_remove_bond_device(pairedDeviceBtAddr[i]);
  }

  Serial.begin(115200);
  PS4.attach(notify);
  PS4.attachOnConnect(onConnect);
  PS4.attachOnDisconnect(onDisConnect);

  Serial.println("Ready.");

  mcp2515.reset();
  mcp2515.setBitrate(CAN_1000KBPS, MCP_8MHZ);
  mcp2515.setNormalMode();

  canMsg1.can_id  = 0xBB;
  canMsg1.can_dlc = 8;

  canMsg2.can_id  = 0xCC;
  canMsg2.can_dlc = 8;
}

void loop() 
{
  canMsg1.data[0] = PS4.Left();
  canMsg1.data[1] = PS4.Down();
  canMsg1.data[2] = PS4.Right();
  canMsg1.data[3] = PS4.Up();
  canMsg1.data[4] = PS4.Square();
  canMsg1.data[5] = PS4.Cross();
  canMsg1.data[6] = PS4.Circle();
  canMsg1.data[7] = PS4.Triangle();

  canMsg2.data[0] = PS4.LStickX();
  canMsg2.data[1] = PS4.LStickY();
  canMsg2.data[2] = PS4.RStickX();
  canMsg2.data[3] = PS4.RStickY();
  canMsg2.data[4] = PS4.L1();
  canMsg2.data[5] = PS4.R1();
  canMsg2.data[6] = PS4.L2();
  canMsg2.data[7] = PS4.R2();

  mcp2515.sendMessage(&canMsg1);
  mcp2515.sendMessage(&canMsg2);

  delay(50);
}
