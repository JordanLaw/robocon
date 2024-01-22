#include "vesc.h"
#include "can_packet.h"

unsigned char len = 0;
//https://github.com/vedderb/bldc/blob/master/datatypes.h
//Updated on Sep 12, HmT

vesc::vesc(int CAN_ID, CAN* _CAN, int hz, Motor_type type){
  vesc_init(CAN_ID, _CAN, hz, type);
}

void vesc::vesc_init(int CAN_ID, CAN* _CAN, int hz, Motor_type type)
{
  id = CAN_ID;
  CAN0 = _CAN;
  CAN0->frequency(hz);
  Rxmsg.format = CANExtended;

  motor = motor_property(type);
  
  //CAN0->attach(&can_read, CAN::RxIrq);
}

void vesc::buffer_append_int32(uint8_t* buffer, int32_t number, int32_t *index) 
{
  buffer[(*index)++] = number >> 24;
  buffer[(*index)++] = number >> 16;
  buffer[(*index)++] = number >> 8;
  buffer[(*index)++] = number;
}

uint8_t vesc::sendPacket(uint32_t id, uint8_t packet[], int32_t len)
{
  if (CAN0->write(CANMessage(id, (const char*)packet, sizeof(packet),CANData,CANExtended)))
  {   
    wait_us(3);
    return 1;
  }
  else {
    //Serial.println("Error Sending Message...");
    return 0;
  }
}

void vesc::comm_can_set_duty(float duty) {
  if(duty > 1){
    duty = 1;
  }
  else if(duty < -1){
    duty = -1;
  }

  int32_t send_index = 0;
  uint8_t buffer[4];
  buffer_append_int32(buffer, (int32_t)(duty * 100000.0), &send_index);
  sendPacket(id |
            ((uint32_t)CAN_PACKET_SET_DUTY << 8), buffer, send_index);
}

void vesc::comm_can_set_current(float current) {
  if(current > motor.getMaxCurrent()){
    current = motor.getMaxCurrent();
  }
  else if(current < -motor.getMaxCurrent()){
    current = -motor.getMaxCurrent();
  }

  int32_t send_index = 0;
  uint8_t buffer[4];
  buffer_append_int32(buffer, (int32_t)(current * 1000.0), &send_index);
  sendPacket(id |
            ((uint32_t)CAN_PACKET_SET_CURRENT << 8), buffer, send_index);
}

void vesc::comm_can_set_current_brake(float current) {
  if(current > motor.getMaxCurrent()){
    current = motor.getMaxCurrent();
  }
  else if(current < -motor.getMaxCurrent()){
    current = -motor.getMaxCurrent();
  }

  int32_t send_index = 0;
  uint8_t buffer[4];
  buffer_append_int32(buffer, (int32_t)(current * 1000.0), &send_index);
  sendPacket(id |
            ((uint32_t)CAN_PACKET_SET_CURRENT_BRAKE << 8), buffer, send_index);
}

void vesc::comm_can_set_mrpm(float mrpm) {
  if(mrpm > motor.getMaxRPM()){
    mrpm = motor.getMaxRPM();
  }
  else if(mrpm < -motor.getMaxRPM()){
    mrpm = -motor.getMaxRPM();
  }

  //mrpm change to erpm
  float erpm = mrpm * motor.getPolesNumber() / 2.0f;

  int32_t send_index = 0;
  uint8_t buffer[4];
  buffer_append_int32(buffer, (int32_t)erpm, &send_index);   //send erpm
  sendPacket(id | ((uint32_t)CAN_PACKET_SET_RPM << 8), buffer, send_index);
}

void vesc::comm_can_set_pos(float pos) {

  if(pos > 360.0f){
    pos = 360.0f;
  }

  if(pos < 0){
    pos = 0.0f;
  }
  
  int32_t send_index = 0;
  uint8_t buffer[4];
  buffer_append_int32(buffer, (int32_t)(pos * 1000000.0), &send_index);
  sendPacket(id |
            ((uint32_t)CAN_PACKET_SET_POS << 8), buffer, send_index);
}

void vesc::comm_can_set_tach(int32_t tach, float maxRPM, float kp, float ki, float kd){
  float rpm = 0.0f;

  if(abs(maxRPM) > motor.getMaxRPM()){
    if(maxRPM >= 0.0f){
      rpm = motor.getMaxRPM();
    }
    else{
      rpm = -motor.getMaxRPM();
    }
  }

  ////////////////////////////////////////////////////////////////////////
  /////////////TBC////////////////////////////
  //////////////////////////////////////////////////////

}

void vesc::comm_can_set_handbrake(float current) {
  if(current > motor.getMaxCurrent()){
    current = motor.getMaxCurrent();
  }
  else if(current < -motor.getMaxCurrent()){
    current = -motor.getMaxCurrent();
  }

  int32_t send_index = 0;
  uint8_t buffer[4];
  buffer_append_int32(buffer, (int32_t)(current * 1e3), &send_index);
  comm_can_transmit_eid_replace(id |
          ((uint32_t)CAN_PACKET_SET_CURRENT_HANDBRAKE << 8), buffer, send_index, true);
}

void vesc::comm_can_transmit_eid_replace(uint32_t id, const uint8_t *data, uint8_t len, bool replace) {
  if (len > 8) {
      len = 8;
  }
}

void vesc::can_read() {
  //if fail to read, return
  if(!CAN0->read(Rxmsg)){
      return;
  }

  int can_id = Rxmsg.id & 0xFF;
  int cmd = (Rxmsg.id >> 8);

  //Is the msg send to itself?
  if(can_id != id){
    return;
  }

  switch (cmd) {
    case CAN_PACKET_STATUS:
      mrpm = (float)((((uint32_t)Rxmsg.data[0]) << 24 | 
                    ((uint32_t)Rxmsg.data[1]) << 16 |
                    ((uint32_t)Rxmsg.data[2]) << 8 | 
                    ((uint32_t)Rxmsg.data[3]))) / (motor.getPolesNumber() / 2);   //change erpm to mrpm
      //printf("RPM: %ld\n", rpm);

      current = (float)(((uint16_t)Rxmsg.data[4]) << 8 | 
                              ((uint16_t)Rxmsg.data[5])) / 
                              10.0;

      duty_cycle = (float)((((uint16_t)Rxmsg.data[6]) << 8) | 
                            ((uint16_t)Rxmsg.data[7])) / 
                            1000.0;
      break;

    case CAN_PACKET_STATUS_2:
      ah = (float)((((uint32_t)Rxmsg.data[0]) << 24 | 
                    ((uint32_t)Rxmsg.data[1]) << 16 |
                    ((uint32_t)Rxmsg.data[2]) << 8 | 
                    ((uint32_t)Rxmsg.data[3]))) / 
                    10000.0;

      ah_charged = (float)((((uint32_t)Rxmsg.data[4]) << 24 | 
                    ((uint32_t)Rxmsg.data[5]) << 16 |
                    ((uint32_t)Rxmsg.data[6]) << 8 | 
                    ((uint32_t)Rxmsg.data[7]))) / 
                    10000.0;
      break;

    case CAN_PACKET_STATUS_3:
      wh = (float)(((uint32_t)Rxmsg.data[0]) << 24 | 
                    ((uint32_t)Rxmsg.data[1]) << 16 |
                    ((uint32_t)Rxmsg.data[2]) << 8 | 
                    ((uint32_t)Rxmsg.data[3])) / 
                    10000.0;

      wh_charged = (float)(((uint32_t)Rxmsg.data[4]) << 24 | 
                            ((uint32_t)Rxmsg.data[5]) << 16 |
                            ((uint32_t)Rxmsg.data[6]) << 8 | 
                            ((uint32_t)Rxmsg.data[7])) / 
                            10000.0;
      break;

    case CAN_PACKET_STATUS_4:
      fet_temp = (float)(((uint16_t)Rxmsg.data[0]) << 8 | 
                        ((uint16_t)Rxmsg.data[1])) / 
                        10.0f;

      motor_temp = (float)(((uint16_t)Rxmsg.data[2]) << 8 | 
                          ((uint16_t)Rxmsg.data[3])) / 
                          10.0f;

      current_in = (float)(((uint16_t)Rxmsg.data[4]) << 8 | 
                                ((uint16_t)Rxmsg.data[5])) / 
                                10.0f;

      pid_pos = (float)(((uint16_t)Rxmsg.data[6]) << 8 | 
                          ((uint16_t)Rxmsg.data[7])) / 
                          50.0f;

      //printf("POS: %d\n", motor_pos);

      break;

    case CAN_PACKET_STATUS_5:
      tachometer_value = (int32_t)((((uint32_t)Rxmsg.data[0]) << 24 | 
                                    ((uint32_t)Rxmsg.data[1]) << 16 |
                                    ((uint32_t)Rxmsg.data[2]) << 8 | 
                                    ((uint32_t)Rxmsg.data[3])));

      //  pos = tach * 120 / polesNumber
      //  abs_pos = pos / gear_ratio
      abs_pos = (float)((tachometer_value*120.0f/motor.getPolesNumber())/motor.getGearRatio()); 

      input_voltage = (float)(((uint16_t)Rxmsg.data[4]) << 8 | 
                              ((uint16_t)Rxmsg.data[5])) / 
                              10.0f;
      
      //printf("Voltage: %d\n", input_voltage);
      break;

    case CAN_PACKET_STATUS_6:
      adc1 = (float)(((uint16_t)Rxmsg.data[0]) << 8 | 
                      ((uint16_t)Rxmsg.data[1])) /
                      1000.0f;
      
      adc2 = (float)(((uint16_t)Rxmsg.data[2]) << 8 | 
                      ((uint16_t)Rxmsg.data[3])) /
                      1000.0f;

      adc3 = (float)(((uint16_t)Rxmsg.data[4]) << 8 | 
                      ((uint16_t)Rxmsg.data[5])) /
                      1000.0f;

      ppm = (float)(((uint16_t)Rxmsg.data[6]) << 8 | 
                      ((uint16_t)Rxmsg.data[7])) / 
                      1000.0f;

      break;

    default:
      break;
  }
}

float vesc::getDutyCycle(){
  return duty_cycle;
}

float vesc::getCurrent(){
  return current;
}

float vesc::getMRPM(){
  return mrpm;
}

float vesc::getAh(){
  return ah;
}

float vesc::getAh_charged(){
  return ah_charged;
}

float vesc::getWh(){
  return wh;
}

float vesc::getWh_charged(){
  return wh_charged;
}

float vesc::getPID_POS(){
  return pid_pos;
}

float vesc::getCurrent_in(){
  return current_in;
}

float vesc::getMotor_temp(){
  return motor_temp;
}

float vesc::getFet_temp(){
  return fet_temp;
}

int32_t vesc::getTach(){
  return tachometer_value;
}

float vesc::getInputVolt(){
  return input_voltage;
}

float vesc::getADC1(){
  return adc1;
}

float vesc::getADC2(){
  return adc2;
}

float vesc::getADC3(){
  return adc3;
}

float vesc::getPPM(){
  return ppm;
}

float vesc::getABS_pos(){
  return abs_pos;
}

void vesc::stop(){
  comm_can_set_duty(0.0f);
}

void vesc::hold(){
  comm_can_set_mrpm(0.0f);
}
