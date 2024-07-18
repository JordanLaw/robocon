#include "mbed.h"
#include "CAN3.h"
#include "vesc.h"

#define CAN_MSG_ID_1  0x111
#define CAN_MSG_ID_2  0x222

#define CAN_MSG_DATA_1  ""
#define CAN_MSG_DATA_2  "CAN message 2"

// 1 -> f446re, 0 -> f446ZE
#define BOARD 1

#if BOARD == 1
    SPI spi(PA_7, PA_6, PA_5);
    CAN can2(PA_11, PA_12, 1000000);  //rd, td, hz
    CAN3 can(spi, PA_4);

    DigitalOut home1(PC_12);
    DigitalOut home2(PC_11);

#else
    SPI spi(PA_7, PA_6, PA_5);
    CAN can2(PA_11, PA_12, 1000000);  //rd, td, hz
    CAN3 can(spi, PB_6);

#endif

DigitalIn userbutton(PC_13);

// vesc dir6(6, &can, 1000000, Motor_type::m3508);
// vesc dir10(10, &can, 1000000, Motor_type::m3508);
// vesc dir57(57, &can, 1000000, Motor_type::m3508);
// vesc rpm20(20, &can, 1000000, Motor_type::m3508);
// vesc rpm114(114, &can, 1000000, Motor_type::m3508);
// vesc rpm61(61, &can, 1000000, Motor_type::m3508);

vesc dir122(122, &can, 1000000, Motor_type::m3508);
vesc dir71(71, &can, 1000000, Motor_type::m3508);
vesc dir46(46, &can, 1000000, Motor_type::m3508);
// vesc rpm108(108, &can, 1000000, Motor_type::m3508);

// unsigned char bytes[4];
// unsigned char* bytes_send;

// unsigned char* int_to_byte(int z){

//     bytes[0] = (z >> 24) & 0xFF;
//     bytes[1] = (z >> 16) & 0xFF;
//     bytes[2] = (z >> 8) & 0xFF;
//     bytes[3] = (z) & 0xFF;

//     return bytes;
// }

bool homing1 = false;
bool homing2 = false;
bool home_finished = false;
int offset_pos1;
int offset_pos2;
int count_pos = 0;

int main(){
    // bytes_send = int_to_byte(100);

    can.frequency(CAN_1MBPS_8MHZ);

    // CANMessage msg1(CAN_MSG_ID_1, CAN_MSG_DATA_1, 13);
    // CANMessage msg2(CAN_MSG_ID_2, CAN_MSG_DATA_2, 13);

    // CANMessage message(CAN_MSG_ID_1, bytes_send, 4);
    // CANMessage message2;

    while (1){
        // printf("pos: %d\n", offset_pos);
        
        // if (homing1 == false){
        //     if (!home1.read()){
        //         dir122.comm_can_set_mrpm(500);
            
        //     }

        //     else{
        //         homing1 = true;
        //         dir122.comm_can_set_mrpm(0);
        //     }
        // }

        // if (homing2 == false){
        //     if (!home2.read()){
        //         dir71.comm_can_set_mrpm(500);
            
        //     }

        //     else{
        //         homing2 = true;
        //         dir71.comm_can_set_mrpm(0);
        //     }
        // }

        // if (homing1 == true and homing2 == true){
        //     while (count_pos <= 500){
        //         dir122.read_pos_status = false;
        //         dir71.read_pos_status = false;
        //         offset_pos1 = (int)dir122.getPID_POS();
        //         offset_pos2 = (int)dir71.getPID_POS();
        //         count_pos += 1;
        //         home_finished = true;
        //         }
                        
        // }
        
        // if (home_finished == true){

        //     printf("pos1: %d pos2: %d\n", offset_pos1, offset_pos2);
        //     if (!userbutton){
        //         if ((offset_pos1 + 90) > 360){
        //             dir122.comm_can_set_pos(90 + offset_pos1 - 360);
        //         }
        //         else{
        //             dir122.comm_can_set_pos(90 + offset_pos1);
        //         }

        //         if ((offset_pos2 + 90) > 360){
        //             dir71.comm_can_set_pos(90 + offset_pos2 - 360);
        //         }
        //         else{
        //             dir71.comm_can_set_pos(90 + offset_pos2);
        //         }

                
        //     }   
        //     else{
        //         dir122.comm_can_set_pos(0 + offset_pos1);
        //         dir71.comm_can_set_pos(0 + offset_pos2);
        // // }
            
        //     }
        // }
        
        if (!userbutton){
            dir46.comm_can_set_pos(90);
        }
        else{
            dir46.comm_can_set_pos(0);
        }


        wait_us(10);
        
        // printf("123\n");
        // if(can.read(&message2)){
        //     printf("id: %u\n", message2.id);
        // }

        

    }
}