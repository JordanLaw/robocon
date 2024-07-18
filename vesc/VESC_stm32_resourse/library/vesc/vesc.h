#ifndef _VESC_H
#define _VESC_H

#include "CAN3.h"
#include "mbed.h"
#include "motor_property.h"

class vesc
{
    private:
        int id;
        motor_property motor;

        // CAN_PACKET_STATUS_1
        float duty_cycle = 0.0f;        //unit: %, scale: 1000
        float current = 0.0f;           //unit: A, scale: 10
        float mrpm = 0.0f;              //unit: RPM, scale: 1

        // CAN_PACKET_STATUS_2
        float ah = 0.0f;                //unit: Ah, scale: 10000
        float ah_charged = 0.0f;        //unit: Ah, scale: 10000

        // CAN_PACKET_STATUS_3
        float wh = 0.0f;                //unit: Wh, scale: 10000
        float wh_charged = 0.0f;        //unit: Wh, scale: 10000

        // CAN_PACKET_STATUS_4
        float pid_pos = 0.0f;           //unit: deg, scale: 50
        float current_in = 0.0f;        //unit: A,  scale: 10
        float motor_temp = 0.0f;        //unit: degC, scale: 10
        float fet_temp = 0.0f;          //unit: degC, scale: 10

        // CAN_PACKET_STATUS_5
        int32_t tachometer_value = 0;   //unit: EREV, scale: 6    //tach = pos/360 * 3 * (2 * polePairNumber)
        float input_voltage = 0.0f;     //unit: V, scale: 10

        // CAN_PACKET_STATUS_6
        float adc1 = 0.0f;              //unit: V, scale: 1000
        float adc2 = 0.0f;              //unit: V, scale: 1000
        float adc3 = 0.0f;              //unit: V, scale: 1000
        float ppm = 0.0f;               //unit: %, scale: 1000

        float abs_pos = 0.0f;

        CAN3* CAN0;
        // CAN* CAN0;
        CANMessage Txmsg;
        CANMessage Rxmsg;

        unsigned char rxBuf[8];
        char msgString[128];
        char display_buffer[8];

    public:
        vesc(int CAN_ID, CAN3* _CAN, int hz, Motor_type type);

        //Change to vesc_init to replace constructor    
        void vesc_init(int CAN_ID, CAN3* _CAN, int hz, Motor_type type);

        void stop();
        void hold();

        void can_read();

        void comm_can_transmit_eid_replace(uint32_t id, const uint8_t *data, uint8_t len, bool replace, int interface);
        void buffer_append_int32(uint8_t* buffer, int32_t number, int32_t *index);
        void comm_can_transmit_eid_replace(uint32_t id, const uint8_t *data, uint8_t len, bool replace);
        void sendPacket(uint32_t id, uint8_t packet[], int32_t len);
        
        void comm_can_set_duty(float duty); //-1 (-100%) <= duty <= 1 (100%)
        void comm_can_set_current(float current);
        void comm_can_set_handbrake(float current);
        void comm_can_set_current_brake(float current);
        void comm_can_set_mrpm(float mrpm);
        void comm_can_set_pos(float pos);
        void comm_can_set_tach(int32_t tach, float maxRPM, float kp = 1.0f, float ki = 1.0f, float kd = 0.0f);

        void comm_can_update_pid_pos_offset(float angle_now, bool store);

        float getDutyCycle();
        float getCurrent();
        float getMRPM();
        float getAh();
        float getAh_charged();
        float getWh();
        float getWh_charged();
        float getPID_POS();
        float getCurrent_in();
        float getMotor_temp();
        float getFet_temp();
        int32_t getTach();
        float getInputVolt();
        float getADC1();
        float getADC2();
        float getADC3();
        float getPPM();
        float getABS_pos();

        bool read_pos_status = false;
};

#endif
