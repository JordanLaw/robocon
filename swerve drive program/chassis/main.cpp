#include "mbed.h"
#include "CAN3.h"
#include "vesc.h"
#include "abi_encoder.h"
#include "odometry.h"
#include "rmd_can.h"
#include "math.h"
#include "kinematics.h"
#include "xm_motor.h"

#define CAN_MSG_ID_1  0x111
#define CAN_MSG_ID_2  0x222

#define CAN_MSG_DATA_1  ""
#define CAN_MSG_DATA_2  "CAN message 2"

DigitalIn userbutton(PC_13);

BufferedSerial pc (USBTX, USBRX, 256000);

// vesc dir6(6, &can, 1000000, Motor_type::m3508);
// vesc dir10(10, &can, 1000000, Motor_type::m3508);
// vesc dir57(57, &can, 1000000, Motor_type::m3508);
// vesc rpm20(20, &can, 1000000, Motor_type::m3508);
// vesc rpm114(114, &can, 1000000, Motor_type::m3508);
// vesc rpm61(61, &can, 1000000, Motor_type::m3508);

// vesc dir46(46, &can, 1000000, Motor_type::m3508);
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
kinematics robot1(47, 45, 4000);

bool homingFR = false;
bool homingFL = false;
bool homingBL = false;
bool homingBR = false;

int16_t WA1;
int16_t WA2;
int16_t WA3;
int16_t WA4;

int16_t WS1;
int16_t WS2;
int16_t WS3;
int16_t WS4;

bool home_finished = false;
int offset_posFR;
int offset_posFL;
int offset_posBL;
int offset_posBR;
int count_pos = 0;
int value_plus = 0;

int max_rpm = 1000;

bool WA_message_receive = false;
bool WS1_message_receive = false;
bool WS2_message_receive = false;
bool WS3_message_receive = false;
bool WS4_message_receive = false;

int posR;
int posL;

struct {
    int ps4_Left;
    int ps4_Down;
    int ps4_Right;
    int ps4_Up;
    int ps4_Square;
    int ps4_Cross;
    int ps4_Circle;
    int ps4_Triangle;

    int8_t PS4LStickX;
    int8_t PS4LStickY;
    int8_t PS4RStickX;
    int8_t PS4RStickY;

} myController;

// 1 -> complete swereve drive chassis program with home function 
// 2 -> odometry program
// 3 -> mecamun wheel chassis program with rmd motor
// 4 -> Test program of receiving PS4 controller data
// 5 -> cybergear motor test program
// 6 -> Test program of swerve drive chassis without home function
// 7 -> testing 100 times turning swerve drive from 0 to 90 and return to 0 again
// 8 -> tesing MCP2515 readMessage function
// 9 -> testing MCP2515 writeMessage function

#define BOARD 6

#if BOARD == 1
    SPI spi(PA_7, PA_6, PA_5);
    CAN can2(PA_11, PA_12, 1000000);  //rd, td, hz
    CAN3 can(spi, PA_4);

    vesc dir122(122, &can, 1000000, Motor_type::m3508);
    vesc dir71(71, &can, 1000000, Motor_type::m3508);
    vesc dir126(126, &can, 1000000, Motor_type::m3508);
    vesc dir47(47, &can, 1000000, Motor_type::m3508);

    vesc rpm4(4, &can, 1000000, Motor_type::m3508);
    vesc rpm63(63, &can, 1000000, Motor_type::m3508);
    vesc rpm53(53, &can, 1000000, Motor_type::m3508);
    vesc rpm108(108, &can, 1000000, Motor_type::m3508);

    DigitalOut homeFR(PC_10);
    DigitalOut homeFL(PA_1);
    DigitalOut homeBL(PC_12);
    DigitalOut homeBR(PC_11);

    // struct {
    //     int ps4_Left;
    //     int ps4_Down;
    //     int ps4_Right;
    //     int ps4_Up;
    //     int ps4_Square;
    //     int ps4_Cross;
    //     int ps4_Circle;
    //     int ps4_Triangle;

    //     int8_t PS4LStickX;
    //     int8_t PS4LStickY;
    //     int8_t PS4RStickX;
    //     int8_t PS4RStickY;

    // } myController;

    int main(){
        // bytes_send = int_to_byte(100);

        can.frequency(CAN_1MBPS_8MHZ);

        // CANMessage msg1(CAN_MSG_ID_1, CAN_MSG_DATA_1, 13);
        // CANMessage msg2(CAN_MSG_ID_2, CAN_MSG_DATA_2, 13);

        // CANMessage message(CAN_MSG_ID_1, bytes_send, 4);
        CANMessage message2;
        CANMessage msg1;
        CANMessage msg2;
        // CANMessage message_WS;

        while (1){
            // printf("start");
            // printf("pos: %d\n", offset_pos);

            // posR = encoder_tickRight.getAmountSPR();
            // posL = encoder_tickLeft.getAmountSPR();
            // printf("pos: %d, %d\n", posR, posL);
            
            if (homingFR == false){
                if (!homeFR.read()){
                    dir126.comm_can_set_mrpm(500);
                
                }

                else{
                    homingFR = true;
                    dir126.comm_can_set_current_brake(3);
                }
            }

            if (homingFL == false){
                if (!homeFL.read()){
                    dir47.comm_can_set_mrpm(500);
                
                }

                else{
                    homingFL = true;
                    dir47.comm_can_set_current_brake(3);
                }
            }

            if (homingBL == false){
                if (!homeBL.read()){
                    dir122.comm_can_set_mrpm(500);
                
                }


                else{
                    homingBL = true;
                    dir122.comm_can_set_current_brake(3);
                }
            }

            if (homingBR == false){
                if (!homeBR.read()){
                    dir71.comm_can_set_mrpm(500);
                
                }

                else{
                    homingBR = true;
                    dir71.comm_can_set_current_brake(3);
                }
            }

            if (home_finished == false){ 
                if (homingFR == true and homingFL == true and homingBL == true and homingBR == true ){
                    while (count_pos <= 500){
                        dir122.read_pos_status = false;
                        dir71.read_pos_status = false;
                        dir126.read_pos_status = false;
                        dir47.read_pos_status = false;
                        offset_posFR = (int)dir126.getPID_POS();
                        offset_posFL = (int)dir47.getPID_POS();
                        offset_posBL = (int)dir122.getPID_POS();
                        offset_posBR = (int)dir71.getPID_POS();
                        count_pos += 1;
                        printf("count: %d, pos: %d %d %d %d\n", count_pos, offset_posFR, offset_posFL, offset_posBL, offset_posBR);

                    }

                    home_finished = true;
                    printf("homimg finished\n");
                                
                }
            }

            else{
                // printf("error");
            }
            
            if (home_finished == true){
                if (msg1 == false or msg2 == false){
                    can2.read(message2);
                
                    if (message2.id == 0xBB){
                        myController.ps4_Left = message2.data[0];
                        myController.ps4_Down = message2.data[1];
                        myController.ps4_Right = message2.data[2];
                        myController.ps4_Up = message2.data[3];
                        myController.ps4_Square = message2.data[4];
                        myController.ps4_Cross = message2.data[5];
                        myController.ps4_Circle = message2.data[6];
                        myController.ps4_Triangle = message2.data[7];
                        
                        msg1 = true;

                    }
                    else{
                        // printf("ID: \n", message2.id);
                    }

                    if (message2.id == 0xCC){
                        myController.PS4LStickX = message2.data[0];
                        myController.PS4LStickY = message2.data[1];
                        myController.PS4RStickX = message2.data[2];
                        myController.PS4RStickY = message2.data[3];

                        msg2 = true;

                    }
                    else{

                    }

                }

                else{
                    // test_float = (float)myController.PS4LStickX / 127;
                    // printf("%d %d.%d\n", myController.PS4LStickX, (int8_t)test_float, (int)((float)(abs(test_float)-abs((int)test_float))*10000)) ;
                    // printf("%d\n", myController.PS4LStickX);
                    if ((float)myController.PS4LStickY / 127 < 0.2 and (float)myController.PS4LStickY / 127 > -0.2){
                        myController.PS4LStickY = 0;
                    }

                    if ((float)myController.PS4LStickX / 127 < 0.2 and (float)myController.PS4LStickX / 127 > -0.2){
                        myController.PS4LStickX = 0;
                    }

                    if ((float)myController.PS4RStickX / 127 < 0.2 and (float)myController.PS4RStickX / 127 > -0.2){
                        myController.PS4RStickX = 0;
                    }

                    robot1.move_cal((float)myController.PS4LStickY / 127, (float)myController.PS4LStickX / 127, (float)myController.PS4RStickX / 127);

                    // printf("%d %d %d %d L: %d D: %d R; %d U: %d S: %d Cro: %d Cir: %d T: %d\n", myController.PS4LStickX, myController.PS4LStickY, myController.PS4RStickX, myController.PS4RStickY, myController.ps4_Left, myController.ps4_Down, myController.ps4_Right, myController.ps4_Up, myController.ps4_Square, myController.ps4_Cross, myController.ps4_Circle, myController.ps4_Triangle);

                    // printf("%d.%d ", (int8_t)myController.PS4LStickX, (int)((float)((abs((int8_t)myController.PS4LStickX)-abs((int)myController.PS4LStickX))*1000)));
                    // printf("%d.%d ", (int8_t)myController.PS4LStickY, (int)((float)((abs((int8_t)myController.PS4LStickY)-abs((int)myController.PS4LStickY))*1000)));
                    // printf("%d.%d ", (int8_t)myController.PS4RStickX, (int)((float)((abs((int8_t)myController.PS4RStickX)-abs((int)myController.PS4RStickX))*1000)));
                    // printf("%d.%d\n", (int8_t)myController.PS4RStickY, (int)((float)((abs((int8_t)myController.PS4RStickY)-abs((int)myController.PS4RStickY))*1000)));

                    printf("WS: %d, %d, %d, %d WA: %d, %d, %d, %d\n", (int)robot1.WS1, (int)robot1.WS2, (int)robot1.WS3, (int)robot1.WS4, (int)robot1.WA1, (int)robot1.WA2, (int)robot1.WA3, (int)robot1.WA4);

                    if (robot1.WS1 == 0){
                        rpm108.comm_can_set_current_brake(3);
                    }
                    else{
                        rpm108.comm_can_set_mrpm(robot1.WS1);
                        printf("send");
                    }

                    if (robot1.WS2 == 0){
                        rpm63.comm_can_set_current_brake(3);
                    }
                    else{
                        rpm63.comm_can_set_mrpm(robot1.WS2);
                    }
                    
                    if (robot1.WS3 == 0){
                        rpm4.comm_can_set_current_brake(3);
                    }
                    else{
                        rpm4.comm_can_set_mrpm(robot1.WS2);
                    }

                    if (robot1.WS4 == 0){
                        rpm53.comm_can_set_current_brake(3);
                    }
                    else{
                        rpm53.comm_can_set_mrpm(robot1.WS4);
                    }

                    if ((offset_posFR + robot1.WA1) > 360){
                        dir126.comm_can_set_pos(robot1.WA1 + offset_posFR - 360);
                    }
                    else if(offset_posFR + robot1.WA1 < 0){
                        dir126.comm_can_set_pos(robot1.WA1 + offset_posFR + 360);
                    }
                    else{
                        dir126.comm_can_set_pos(robot1.WA1 + offset_posFR);
                    }

                    if ((offset_posFL + robot1.WA2) > 360){
                        dir47.comm_can_set_pos(robot1.WA2 + offset_posFL - 360);
                    }
                    else if(offset_posFL + robot1.WA2 < 0){
                        dir47.comm_can_set_pos(robot1.WA2 + offset_posFL + 360);
                    }
                    else{
                        dir47.comm_can_set_pos(robot1.WA2 + offset_posFL);
                    }

                    if ((offset_posBL + robot1.WA3) > 360){
                        dir122.comm_can_set_pos(robot1.WA3 + offset_posBL - 360);
                    }

                    else if(offset_posBL + robot1.WA3 < 0){
                        dir122.comm_can_set_pos(robot1.WA3 + offset_posBL + 360);
                    }

                    else{
                        dir122.comm_can_set_pos(robot1.WA3 + offset_posBL);
                    }

                    if ((offset_posBR + robot1.WA4) > 360){
                        dir71.comm_can_set_pos(robot1.WA4 + offset_posBR - 360);
                    }
                    else if(offset_posBR + robot1.WA4 < 0){
                        dir71.comm_can_set_pos(robot1.WA4 + offset_posBR + 360);
                    }

                    else{
                        dir71.comm_can_set_pos(robot1.WA4 + offset_posBR);
                    }

                    msg1 = false;
                    msg2 = false;
                }
                
            

                // while (WA_message_receive == false or WS1_message_receive == false or WS2_message_receive == false){

                //     can2.read(message2);

                //     // printf("%d %d %d %d %d\n", WA_message_receive, WS1_message_receive, WS2_message_receive, WS3_message_receive, WS4_message_receive);

                //     if (message2.id == 0xAA and WA_message_receive == false){
                        
                //         WA1 = message2.data[0] * 256 + message2.data[1];
                //         WA2 = message2.data[2] * 256 + message2.data[3];
                //         WA3 = message2.data[4] * 256 + message2.data[5];
                //         WA4 = message2.data[6] * 256 + message2.data[7];

                //         WA_message_receive = true;
                //     }

                //     if (message2.id == 0xAB and WS1_message_receive == false){

                //         WS1 = message2.data[0] * 256 + message2.data[1];
                //         WS2 = message2.data[2] * 256 + message2.data[3];

                //         WS1_message_receive = true;
                //     }

                //     if (message2.id == 0xAC and WS2_message_receive == false){

                //         WS3 = message2.data[0] * 256 + message2.data[1];
                //         WS4 = message2.data[2] * 256 + message2.data[3];

                //         WS2_message_receive = true;
                //     }



                //     // printf("%d %d %d\n", WA_message_receive, WS_message_receive, message2.id);

                //     wait_us(2000);
                // }

                // printf("WS: %d, %d, %d, %d WA: %d, %d, %d, %d\n", WS1, WS2, WS3, WS4, WA1, WA2, WA3, WA4);

                // if (WS1 == 0){
                //     rpm108.comm_can_set_current_brake(3);
                // }
                // else{
                //     rpm108.comm_can_set_mrpm(WS1);
                // }

                // if (WS2 == 0){
                //     rpm63.comm_can_set_current_brake(3);
                // }
                // else{
                //     rpm63.comm_can_set_mrpm(WS2);
                // }
                
                // if (WS3 == 0){
                //     rpm4.comm_can_set_current_brake(3);
                // }
                // else{
                //     rpm4.comm_can_set_mrpm(WS2);
                // }

                // if (WS4 == 0){
                //     rpm53.comm_can_set_current_brake(3);
                // }
                // else{
                //     rpm53.comm_can_set_mrpm(WS4);
                // }

                // if ((offset_posFR + WA1) > 360){
                //     dir126.comm_can_set_pos(WA1 + offset_posFR - 360);
                // }
                // else if(offset_posFR + WA1 < 0){
                //     dir126.comm_can_set_pos(WA1 + offset_posFR + 360);
                // }
                // else{
                //     dir126.comm_can_set_pos(WA1 + offset_posFR);
                // }

                // if ((offset_posFL + WA2) > 360){
                //     dir47.comm_can_set_pos(WA2 + offset_posFL - 360);
                // }
                // else if(offset_posFL + WA2 < 0){
                //     dir47.comm_can_set_pos(WA2 + offset_posFL + 360);
                // }
                // else{
                //     dir47.comm_can_set_pos(WA2 + offset_posFL);
                // }

                // if ((offset_posBL + WA3) > 360){
                //     dir122.comm_can_set_pos(WA3 + offset_posBL - 360);
                // }

                // else if(offset_posBL + WA3 < 0){
                //     dir122.comm_can_set_pos(WA3 + offset_posBL + 360);
                // }

                // else{
                //     dir122.comm_can_set_pos(WA3 + offset_posBL);
                // }

                // if ((offset_posBR + WA4) > 360){
                //     dir71.comm_can_set_pos(WA4 + offset_posBR - 360);
                // }
                // else if(offset_posBR + WA4 < 0){
                //     dir71.comm_can_set_pos(WA4 + offset_posBR + 360);
                // }

                // else{
                //     dir71.comm_can_set_pos(WA4 + offset_posBR);
                // }

                // WA_message_receive = false;
                // WS1_message_receive = false;
                // WS2_message_receive = false;
                // WS3_message_receive = false;
                // WS4_message_receive = false;

                // printf("end\n");

            // printf("byte: %x, %x, %x, %x, %x, %x, %x, %x ", message2.data[0], message2.data[1], message2.data[2], message2.data[3], message2.data[4], message2.data[5], message2.data[6], message2.data[7]);
            
            }

            else{
                // printf("error");
            }

    }   

        //////////////////////////////////////



        // if (!userbutton){
        //     dir46.comm_can_set_pos(90);  
        // }
        // else{
        //     dir46.comm_can_set_pos(0);
        // }



        // value_plus += 5;

        // if (value_plus >= 360){

        //     value_plus = 0;
        // }

        // wait_us(100000);
        
        // printf("123\n");
        // if(can.read(&message2)){
        //     printf("id: %u\n", message2.id);
        // }
    // printf("end\n");
    
}

    #elif BOARD == 2
    SPI spi(PA_7, PA_6, PA_5);
    CAN3 can(spi, PA_4);

    abi_encoder right_odom (PA_0, PA_1);
    abi_encoder left_odom (PC_12, PD_2);
    abi_encoder Aux_odom (PC_11, PC_10);
    
    odometry odom (&right_odom, &left_odom, &Aux_odom);

    unsigned char bytes[6];
    unsigned char* bytes_send;
    unsigned char* buf;

    CANMessage Txmsg;

    unsigned char* int_to_byte(int x, int y, int z){
        bytes[0] = (x >> 8) & 0xFF;
        bytes[1] = (x) & 0xFF;
        bytes[2] = (y >> 8) & 0xFF;
        bytes[3] = (y) & 0xFF;
        bytes[4] = (z >> 8) & 0xFF;
        bytes[5] = (z) & 0xFF;

        return bytes;
    }

    int main(){
        can.frequency(CAN_1MBPS_8MHZ);

        while (1) {
            odom.odometry_cal();

            // printf("cnt: %d, %d, %d ", (int)right_odom.getAmountSPR(), (int)left_odom.getAmountSPR(), (int)Aux_odom.getAmountSPR());
            // printf("X: %d.%d Y: %d.%d Pos: %d\n", (int)odom.position[0], (int)((float)(abs(odom.position[0])-abs((int)odom.position[0]))*10000), (int)odom.position[1], (int)((float)(abs(odom.position[1])-abs((int)odom.position[1]))*10000), (int)odom.position[3]);

            bytes_send = int_to_byte((int)odom.position[0], (int)odom.position[1], (int)odom.position[3]); 

            // printf("send: %d %d\n", bytes_send[0], bytes_send[1]);

            Txmsg = CANMessage(1111, (const char*) bytes_send, 6);

            can.write(&Txmsg);

            wait_us(3);


            // turn_R = right_odom.getAmountSPR();
            // turn_L = left_odom.getAmountSPR();
            // turn_A = Aux_odom.getAmountSPR();
            // printf("turn: %d, %d, %d\n", turn_R, turn_L, turn_A);
        }


    }

#elif BOARD == 3
    SPI spi(PA_7, PA_6, PA_5);
    CAN can2(PA_11, PA_12, 1000000);
    // CAN can3(PB_5, PB_13, 1000000);
    CAN3 can(spi, PA_4);

    vesc motor_FR(24, &can, 1000000, Motor_type::m3508);
    vesc motor_FL(8, &can, 1000000, Motor_type::m3508);
    
    vesc motor_BL(28, &can, 1000000, Motor_type::m3508);
    vesc motor_BR(16, &can, 1000000, Motor_type::m3508);

    rmd_can l7015;
    int16_t id = 1;  

    CANMessage message2;
    bool msg1 = false;
    bool msg2 = false;

    bool speed_message_receive = false;
    bool arm_message_receive = false;

    int16_t rpmFR;
    int16_t rpmFL;
    int16_t rpmBL;
    int16_t rpmBR;

    int8_t arm_command_UP;
    int8_t arm_command_DOWN;

    int main(){
        can.frequency(CAN_1MBPS_8MHZ);
        l7015.rmd_can_init(&can2);
        l7015.motor_enable(id);
        l7015.DEBUG_RMD_LIB_MSG = false;

        while (1){
            if (msg1 == false or msg2 == false){
                can2.read(message2);
                
                if (message2.id == 0xBB){
                    myController.ps4_Left = message2.data[0];
                    myController.ps4_Down = message2.data[1];
                    myController.ps4_Right = message2.data[2];
                    myController.ps4_Up = message2.data[3];
                    myController.ps4_Square = message2.data[4];
                    myController.ps4_Cross = message2.data[5];
                    myController.ps4_Circle = message2.data[6];
                    myController.ps4_Triangle = message2.data[7];
                    
                    msg1 = true;

                }
                else{
                    // printf("ID: \n", message2.id);
                }

                if (message2.id == 0xCC){
                    myController.PS4LStickX = message2.data[0];
                    myController.PS4LStickY = message2.data[1];
                    myController.PS4RStickX = message2.data[2];
                    myController.PS4RStickY = message2.data[3];

                    msg2 = true;

                }
                else{

                }

            }

            else{
                l7015.read_global_angle(id);

                printf("pos: %lld\n", (l7015.pos));

                if ((float)myController.PS4LStickY / 127 < 0.2 and (float)myController.PS4LStickY / 127 > -0.2){
                    myController.PS4LStickY = 0;
                }

                if ((float)myController.PS4LStickX / 127 < 0.2 and (float)myController.PS4LStickX / 127 > -0.2){
                    myController.PS4LStickX = 0;
                }

                if ((float)myController.PS4RStickX / 127 < 0.2 and (float)myController.PS4RStickX / 127 > -0.2){
                    myController.PS4RStickX = 0;
                }

                robot1.mecanum_wheel_move((float)myController.PS4LStickX /127, (float)myController.PS4LStickY/127, (float)myController.PS4RStickX/127);

                
                // printf("FR: %d, FL: %d, BL: %d, BR: %d\n", (int)robot1.frontRightPower, (int)robot1.frontLeftPower, (int)robot1.backLeftPower, (int)robot1.backRightPower);

                if (robot1.frontRightPower == 0){
                    motor_FR.comm_can_set_current_brake(3);
                }
                else{
                    motor_FR.comm_can_set_mrpm(robot1.frontRightPower);
                }

                if (robot1.frontLeftPower == 0){
                    motor_FL.comm_can_set_current_brake(3);
                }
                else{
                    motor_FL.comm_can_set_mrpm(robot1.frontLeftPower);
                }
                
                if (robot1.backLeftPower == 0){
                    motor_BL.comm_can_set_current_brake(3);
                }
                else{
                    motor_BL.comm_can_set_mrpm(robot1.backLeftPower);
                }

                if (robot1.backRightPower == 0){
                    motor_BR.comm_can_set_current_brake(3);
                }
                else{
                    motor_BR.comm_can_set_mrpm(robot1.backRightPower);
                }

                // printf("%d %d\n", myController.ps4_Triangle, myController.ps4_Cross);

                if ((int)myController.ps4_Triangle == 1){
                    l7015.set_velocity(id, 80000);
                }
            
                else if ((int)myController.ps4_Cross == 1){
                    l7015.set_velocity(id, -80000);
                }

                else{
                    l7015.set_velocity(id, 0);
                }

                msg1 = false;
                msg2 = false;

            }
        }
    }


        //     // l7015.set_velocity(id, 0);

        //     l7015.read_global_angle(id);
        //     // l7015.read_acc_pid_data(id);
        //     // l7015.read_angle(id);
        //     // l7015.read_encoder(id);

        //     printf("pos: %lld\n", (l7015.pos));
            
        //     while (speed_message_receive == false or arm_message_receive == false){

        //         can2.read(message2);

        //         // printf("%d %d %d %d %d\n", WA_message_receive, WS1_message_receive, WS2_message_receive, WS3_message_receive, WS4_message_receive);

        //         if (message2.id == 0xAA and speed_message_receive == false){
                    
        //             rpmFR = message2.data[0] * 256 + message2.data[1];
        //             rpmFL = message2.data[2] * 256 + message2.data[3];
        //             rpmBL = message2.data[4] * 256 + message2.data[5];
        //             rpmBR = message2.data[6] * 256 + message2.data[7];

        //             speed_message_receive = true;

        //         }

        //         if (message2.id == 0xBB and arm_message_receive == false){
                    
        //             arm_command_UP = message2.data[0];
        //             arm_command_DOWN = message2.data[1];

        //             arm_message_receive = true;

        //         }
            
        //     }

        //     // printf("%d %d %d %d %d\n", rpmFR, rpmFL, rpmBL, rpmBR, arm_command);

        //     if (rpmFR == 0){
        //             motor_FR.comm_can_set_current_brake(3);
        //         }
        //         else{
        //             motor_FR.comm_can_set_mrpm(rpmFR);
        //         }

        //     if (rpmFL == 0){
        //             motor_FL.comm_can_set_current_brake(3);
        //         }
        //         else{
        //             motor_FL.comm_can_set_mrpm(rpmFL);
        //         }
                
        //     if (rpmBL == 0){
        //             motor_BL.comm_can_set_current_brake(3);
        //         }
        //         else{
        //             motor_BL.comm_can_set_mrpm(rpmBL);
        //         }

        //     if (rpmBR == 0){
        //             motor_BR.comm_can_set_current_brake(3);
        //         }
        //         else{
        //             motor_BR.comm_can_set_mrpm(rpmBR);
        //         }

        //     if (arm_command_UP == 1){
        //         l7015.set_velocity(id, 400000);
        //     }
            
        //     else if (arm_command_DOWN == 1){
        //         l7015.set_velocity(id, -400000);
        //     }

        //     else{
        //         l7015.set_velocity(id, 0);
        //     }


                

            
            

        //     speed_message_receive = false;
        //     arm_message_receive = false;


        // }
    // }

#elif BOARD == 4
    CAN can(PA_11, PA_12, 1000000);  //rd, td, hz

    CANMessage message2;

    bool msg1 = false;
    bool msg2 = false;

    // int val = 8;
    // int val1 = 0;
    // int val2 = 0;
    // int val3 = 16;
    // int val_max;
    // int val_sqrt;

    // float test_float;

    struct {
        int ps4_Left;
        int ps4_Down;
        int ps4_Right;
        int ps4_Up;
        int ps4_Square;
        int ps4_Cross;
        int ps4_Circle;
        int ps4_Triangle;

        int8_t PS4LStickX;
        int8_t PS4LStickY;
        int8_t PS4RStickX;
        int8_t PS4RStickY;

    } myController;

    int main(){

        while (1){

            if (msg1 == false or msg2 == false){
                can.read(message2);
                
                if (message2.id == 0xBB){
                    myController.ps4_Left = message2.data[0];
                    myController.ps4_Down = message2.data[1];
                    myController.ps4_Right = message2.data[2];
                    myController.ps4_Up = message2.data[3];
                    myController.ps4_Square = message2.data[4];
                    myController.ps4_Cross = message2.data[5];
                    myController.ps4_Circle = message2.data[6];
                    myController.ps4_Triangle = message2.data[7];
                    
                    msg1 = true;

                }
                else{
                    // printf("ID: \n", message2.id);
                }

                if (message2.id == 0xCC){
                    myController.PS4LStickX = message2.data[0];
                    myController.PS4LStickY = message2.data[1];
                    myController.PS4RStickX = message2.data[2];
                    myController.PS4RStickY = message2.data[3];

                    msg2 = true;

                }
                else{

                }

            }

            else{
                // test_float = (float)myController.PS4LStickX / 127;
                // printf("%d %d.%d\n", myController.PS4LStickX, (int8_t)test_float, (int)((float)(abs(test_float)-abs((int)test_float))*10000)) ;
                // printf("%d\n", myController.PS4LStickX);
                if ((float)myController.PS4LStickY / 127 < 0.2 and (float)myController.PS4LStickY / 127 > -0.2){
                    myController.PS4LStickY = 0;
                }

                if ((float)myController.PS4LStickX / 127 < 0.2 and (float)myController.PS4LStickX / 127 > -0.2){
                    myController.PS4LStickX = 0;
                }

                if ((float)myController.PS4RStickX / 127 < 0.2 and (float)myController.PS4RStickX / 127 > -0.2){
                    myController.PS4RStickX = 0;
                }

                robot1.move_cal((float)myController.PS4LStickY / 127, (float)myController.PS4LStickX / 127, (float)myController.PS4RStickX / 127);

                // printf("%d %d %d %d L: %d D: %d R; %d U: %d S: %d Cro: %d Cir: %d T: %d\n", myController.PS4LStickX, myController.PS4LStickY, myController.PS4RStickX, myController.PS4RStickY, myController.ps4_Left, myController.ps4_Down, myController.ps4_Right, myController.ps4_Up, myController.ps4_Square, myController.ps4_Cross, myController.ps4_Circle, myController.ps4_Triangle);

                // printf("%d.%d ", (int8_t)myController.PS4LStickX, (int)((float)((abs((int8_t)myController.PS4LStickX)-abs((int)myController.PS4LStickX))*1000)));
                // printf("%d.%d ", (int8_t)myController.PS4LStickY, (int)((float)((abs((int8_t)myController.PS4LStickY)-abs((int)myController.PS4LStickY))*1000)));
                // printf("%d.%d ", (int8_t)myController.PS4RStickX, (int)((float)((abs((int8_t)myController.PS4RStickX)-abs((int)myController.PS4RStickX))*1000)));
                // printf("%d.%d\n", (int8_t)myController.PS4RStickY, (int)((float)((abs((int8_t)myController.PS4RStickY)-abs((int)myController.PS4RStickY))*1000)));

                msg1 = false;
                msg2 = false;
            }
            
        }
    }

#elif BOARD == 5
    SPI spi(PA_7, PA_6, PA_5);
    CAN can2(PA_11, PA_12, 1000000);  //rd, td, hz
    CAN3 can(spi, PB_6);

    xm_motor cybergear(1, &can);

    CANMessage message2;

    bool msg1 = false;
    bool msg2 = false;

    struct {
        int ps4_Left;
        int ps4_Down;
        int ps4_Right;
        int ps4_Up;
        int ps4_Square;
        int ps4_Cross;
        int ps4_Circle;
        int ps4_Triangle;

        int8_t PS4LStickX;
        int8_t PS4LStickY;
        int8_t PS4RStickX;
        int8_t PS4RStickY;

    } myController;

    int main(){
        can.frequency(CAN_1MBPS_8MHZ);

        cybergear.motor_enable(1);
        cybergear.motor_pos_value(1, 0);
        // cybergear.motor_pos_zero(1);
        cybergear.motor_mode(1, 1);
        cybergear.motor_pow_value(1, 5, 20, 0.2, 0.13);
            
        /// printf("%d, %d, %d, %d, %d, %d, %d, %d\n", cybergear.canMsg.data[0], cybergear.canMsg.data[1], cybergear.canMsg.data[2], cybergear.canMsg.data[3], cybergear.canMsg.data[4], cybergear.canMsg.data[5], cybergear.canMsg.data[6], cybergear.canMsg.data[7]);

         while (1){

            if (msg1 == false or msg2 == false){
                can2.read(message2);
                
                if (message2.id == 0xBB){
                    myController.ps4_Left = message2.data[0];
                    myController.ps4_Down = message2.data[1];
                    myController.ps4_Right = message2.data[2];
                    myController.ps4_Up = message2.data[3];
                    myController.ps4_Square = message2.data[4];
                    myController.ps4_Cross = message2.data[5];
                    myController.ps4_Circle = message2.data[6];
                    myController.ps4_Triangle = message2.data[7];
                    
                    msg1 = true;

                }
                else{
                    // printf("ID: \n", message2.id);
                }

                if (message2.id == 0xCC){
                    myController.PS4LStickX = message2.data[0];
                    myController.PS4LStickY = message2.data[1];
                    myController.PS4RStickX = message2.data[2];
                    myController.PS4RStickY = message2.data[3];

                    msg2 = true;

                }
                else{

                }

            }

            else{
                if (myController.ps4_Up == 1){
                    cybergear.motor_mode(1, 1);

                }

                else if (myController.ps4_Down == 1){
                    cybergear.motor_mode(1, 2);
                }

                if (myController.ps4_Circle == 1){
                    cybergear.motor_pos_value(1, 3.14/2);

                }

                else if (myController.ps4_Triangle == 1){
                    cybergear.motor_pos_value(1, 0);

                }

                else if (myController.ps4_Square == 1){
                    cybergear.motor_pos_value(1, 3.14 + 3.14/2);

                }

                else if (myController.ps4_Cross == 1){
                    cybergear.motor_pos_value(1, 3.14);

                }

                else if (myController.ps4_Right == 1){
                    cybergear.motor_speed_value(1, 10);

                }

                else if (myController.ps4_Left == 1){
                    cybergear.motor_speed_value(1, -10);

                }
                // test_float = (float)myController.PS4LStickX / 127;
                // printf("%d %d.%d\n", myController.PS4LStickX, (int8_t)test_float, (int)((float)(abs(test_float)-abs((int)test_float))*10000)) ;
                // printf("%d\n", myController.PS4LStickX);

                // printf("%d %d %d %d L: %d D: %d R; %d U: %d S: %d Cro: %d Cir: %d T: %d\n", myController.PS4LStickX, myController.PS4LStickY, myController.PS4RStickX, myController.PS4RStickY, myController.ps4_Left, myController.ps4_Down, myController.ps4_Right, myController.ps4_Up, myController.ps4_Square, myController.ps4_Cross, myController.ps4_Circle, myController.ps4_Triangle);

                // printf("%d.%d ", (int8_t)myController.PS4LStickX, (int)((float)((abs((int8_t)myController.PS4LStickX)-abs((int)myController.PS4LStickX))*1000)));
                // printf("%d.%d ", (int8_t)myController.PS4LStickY, (int)((float)((abs((int8_t)myController.PS4LStickY)-abs((int)myController.PS4LStickY))*1000)));
                // printf("%d.%d ", (int8_t)myController.PS4RStickX, (int)((float)((abs((int8_t)myController.PS4RStickX)-abs((int)myController.PS4RStickX))*1000)));
                // printf("%d.%d\n", (int8_t)myController.PS4RStickY, (int)((float)((abs((int8_t)myController.PS4RStickY)-abs((int)myController.PS4RStickY))*1000)));

                msg1 = false;
                msg2 = false;
            }
            
        }
    }

#elif BOARD == 6 
// testing new module - FRC swerve drive
// using nucleo f446re

    SPI spi(PA_7, PA_6, PA_5);
    CAN can2(PA_11, PA_12, 1000000);  //rd, td, hz
    CAN3 can(spi, PB_6);

    // module A
    // vesc dirfr(126, &can, 1000000, Motor_type::m3508); 
    // vesc dirfl(8, &can, 1000000, Motor_type::m3508);
    // vesc dirbl(57, &can, 1000000, Motor_type::m3508);  
    // vesc dirbr(16, &can, 1000000, Motor_type::m3508);

    // vesc rpmfr(108, &can, 1000000, Motor_type::m3508);
    // vesc rpmfl(95, &can, 1000000, Motor_type::m3508);
    // vesc rpmbl(79, &can, 1000000, Motor_type::m3508);
    // vesc rpmbr(101, &can, 1000000, Motor_type::m3508);

    // module B
    vesc dirfr(47, &can, 1000000, Motor_type::m3508); 
    vesc dirfl(53, &can, 1000000, Motor_type::m3508);
    vesc dirbl(71, &can, 1000000, Motor_type::m3508);  
    vesc dirbr(126, &can, 1000000, Motor_type::m3508);

    vesc rpmfr(108, &can, 1000000, Motor_type::m3508);
    vesc rpmfl(122, &can, 1000000, Motor_type::m3508);
    vesc rpmbl(63, &can, 1000000, Motor_type::m3508);
    vesc rpmbr(4, &can, 1000000, Motor_type::m3508);

    bool msg1 = false;
    bool msg2 = false;

    int main(){
        can.frequency(CAN_1MBPS_8MHZ);

        CANMessage message2;


        while (1){
            if (msg1 == false or msg2 == false){
                can2.read(message2);
                
                // reading first message from PS4 controller (button)
                if (message2.id == 0xBB){
                    myController.ps4_Left = message2.data[0];
                    myController.ps4_Down = message2.data[1];
                    myController.ps4_Right = message2.data[2];
                    myController.ps4_Up = message2.data[3];
                    myController.ps4_Square = message2.data[4];
                    myController.ps4_Cross = message2.data[5];
                    myController.ps4_Circle = message2.data[6];
                    myController.ps4_Triangle = message2.data[7];
                    
                    msg1 = true;

                }
                else{
                    // printf("ID: \n", message2.id);
                }

                // reading second message from PS4 controller (joystick)
                if (message2.id == 0xCC){
                    myController.PS4LStickX = message2.data[0];
                    myController.PS4LStickY = message2.data[1];
                    myController.PS4RStickX = message2.data[2];
                    myController.PS4RStickY = message2.data[3];

                    msg2 = true;

                }
                else{

                }

            }

            else{
                
                // calculate the kinematic using the controller data
                if ((float)myController.PS4LStickY / 127 < 0.2 and (float)myController.PS4LStickY / 127 > -0.2){
                    myController.PS4LStickY = 0;
                }

                if ((float)myController.PS4LStickX / 127 < 0.2 and (float)myController.PS4LStickX / 127 > -0.2){
                    myController.PS4LStickX = 0;
                }

                if ((float)myController.PS4RStickX / 127 < 0.2 and (float)myController.PS4RStickX / 127 > -0.2){
                    myController.PS4RStickX = 0;
                }

                robot1.move_cal((float)myController.PS4LStickY / 127, (float)myController.PS4LStickX / 127, (float)myController.PS4RStickX / 127);

                // printf("WS: %d, %d, %d, %d WA: %d, %d, %d, %d\n", (int)robot1.WS1, (int)robot1.WS2, (int)robot1.WS3, (int)robot1.WS4, (int)robot1.WA1, (int)robot1.WA2, (int)robot1.WA3, (int)robot1.WA4);

                // control the swerve drive using the kinematic data
                if (robot1.WS1 == 0){
                    rpmfr.comm_can_set_duty(0);                   // stop the drive motor (forward-right)
                }
                else{
                    rpmfr.comm_can_set_mrpm(robot1.WS1);                   // move the drive motor (forward-right)
                    // printf("send");
                }

                if (robot1.WS2 == 0){
                    rpmfl.comm_can_set_duty(0);                    // stop the drive motor (forward-left)
                }
                else{
                    rpmfl.comm_can_set_mrpm(robot1.WS2);                    // move the drive motor (forward-left)
                }
                    
                if (robot1.WS3 == 0){
                    rpmbl.comm_can_set_duty(0);                     // stop the drive motor (backward-left)
                }
                else{
                    rpmbl.comm_can_set_mrpm(robot1.WS2);                     // move the drive motor (backward-left)
                }

                if (robot1.WS4 == 0){
                    rpmbr.comm_can_set_duty(0);                    // stop the drive motor (backward-right)
                }
                else{
                    rpmbr.comm_can_set_mrpm(robot1.WS4);                    // move the drive motor (backward-right)
                }

                // moving the angle motor
                if ((offset_posFR + robot1.WA1) > 360){
                    dirfr.comm_can_set_pos(robot1.WA1 + offset_posFR - 360);
                }
                else if(offset_posFR + robot1.WA1 < 0){
                    dirfr.comm_can_set_pos(robot1.WA1 + offset_posFR + 360);
                }
                else{
                    dirfr.comm_can_set_pos(robot1.WA1 + offset_posFR);
                }

                if ((offset_posFL + robot1.WA2) > 360){
                    dirfl.comm_can_set_pos(robot1.WA2 + offset_posFL - 360);
                }
                else if(offset_posFL + robot1.WA2 < 0){
                    dirfl.comm_can_set_pos(robot1.WA2 + offset_posFL + 360);
                }
                else{
                    dirfl.comm_can_set_pos(robot1.WA2 + offset_posFL);
                }

                if ((offset_posBL + robot1.WA3) > 360){
                    dirbl.comm_can_set_pos(robot1.WA3 + offset_posBL - 360);
                }

                else if(offset_posBL + robot1.WA3 < 0){
                    dirbl.comm_can_set_pos(robot1.WA3 + offset_posBL + 360);
                }
                else{
                    dirbl.comm_can_set_pos(robot1.WA3 + offset_posBL);
                }

                if ((offset_posBR + robot1.WA4) > 360){
                    dirbr.comm_can_set_pos(robot1.WA4 + offset_posBR - 360);
                }
                else if(offset_posBR + robot1.WA4 < 0){
                    dirbr.comm_can_set_pos(robot1.WA4 + offset_posBR + 360);
                }
                else{
                    dirbr.comm_can_set_pos(robot1.WA4 + offset_posBR);
                }

                msg1 = false;
                msg2 = false;
                }
        }
    }

#elif BOARD == 7
// testing 100 times turning swerve drive from 0 to 90 and return to 0 again
// using nucleo f446re

    SPI spi(PA_7, PA_6, PA_5);
    CAN can2(PA_11, PA_12, 1000000);  //rd, td, hz
    CAN3 can(spi, PB_6);

    vesc dir122(122, &can, 1000000, Motor_type::m3508);
    vesc dir71(71, &can, 1000000, Motor_type::m3508);
    vesc dir126(126, &can, 1000000, Motor_type::m3508);
    vesc dir47(47, &can, 1000000, Motor_type::m3508);

    vesc rpm4(4, &can, 1000000, Motor_type::m3508);
    vesc rpm63(63, &can, 1000000, Motor_type::m3508);
    vesc rpm53(53, &can, 1000000, Motor_type::m3508);
    vesc rpm108(108, &can, 1000000, Motor_type::m3508);

    bool msg1 = false;
    bool msg2 = false;

    int count_time = 0;

    bool hold_button = false;

    int main(){
        can.frequency(CAN_1MBPS_8MHZ);

        CANMessage message2;


        while (1){
            if (!userbutton){
                dir126.comm_can_set_pos(90);

                if (hold_button == false){
                    count_time += 1;

                    hold_button = true;
                }

            }

            else{
                dir126.comm_can_set_pos(0);
                hold_button = false;
            }

            printf("count: %d\n", count_time);
             
        }

    }

#elif BOARD == 8
    // tesing MCP2515 readMessage function
    // using nucleo f446re

    SPI spi(PA_7, PA_6, PA_5);
    CAN can2(PA_11, PA_12, 1000000);  //rd, td, hz
    CAN3 can(spi, PB_6);

    bool msg1 = false;
    bool msg2 = false;

    int main(){
        can.frequency(CAN_1MBPS_8MHZ);

        CANMessage message2;

        while (1){
            // printf("%d %d\n", msg1, msg2);

            if (msg1 == false or msg2 == false){
                can2.read(message2);
            
                // reading first message from PS4 controller (button)
                if (message2.id == 0xBB){
                    myController.ps4_Left = message2.data[0];
                    myController.ps4_Down = message2.data[1];
                    myController.ps4_Right = message2.data[2];
                    myController.ps4_Up = message2.data[3];
                    myController.ps4_Square = message2.data[4];
                    myController.ps4_Cross = message2.data[5];
                    myController.ps4_Circle = message2.data[6];
                    myController.ps4_Triangle = message2.data[7];
                    
                    msg1 = true;

                }
                else{   
                    // printf("ID: \n", message2.id);
                }

                // reading second message from PS4 controller (joystick)
                if (message2.id == 0xCC){
                    myController.PS4LStickX = message2.data[0];
                    myController.PS4LStickY = message2.data[1];
                    myController.PS4RStickX = message2.data[2];
                    myController.PS4RStickY = message2.data[3];

                    msg2 = true;

                }
                else{

                }   

            }
            else{
                // calculate the kinematic using the controller data
                if ((float)myController.PS4LStickY / 127 < 0.2 and (float)myController.PS4LStickY / 127 > -0.2){
                    myController.PS4LStickY = 0;
                }

                if ((float)myController.PS4LStickX / 127 < 0.2 and (float)myController.PS4LStickX / 127 > -0.2){
                    myController.PS4LStickX = 0;
                }

                if ((float)myController.PS4RStickX / 127 < 0.2 and (float)myController.PS4RStickX / 127 > -0.2){
                    myController.PS4RStickX = 0;
                }

                robot1.move_cal((float)myController.PS4LStickY / 127, (float)myController.PS4LStickX / 127, (float)myController.PS4RStickX / 127);

                printf("WS: %d, %d, %d, %d WA: %d, %d, %d, %d\n", (int)robot1.WS1, (int)robot1.WS2, (int)robot1.WS3, (int)robot1.WS4, (int)robot1.WA1, (int)robot1.WA2, (int)robot1.WA3, (int)robot1.WA4);
                
                wait_us(10000);

                msg1 = false;
                msg2 = false;
            }

        }
    }

#elif BOARD == 9
//re board send message
    SPI spi(PA_7, PA_6, PA_5);
    CAN can2(PA_11, PA_12, 1000000);  //rd, td, hz
    CAN3 can(spi, PB_6);

    CANMessage message2;
    uint16_t value = 0x10;

    bool msg1 = false;
    bool msg2 = false;

    int main(){
        can.frequency(CAN_1MBPS_8MHZ);

        message2.id = 1;
        message2.data[0] = value; 

        while (1){
            can.write(&message2);
            printf("sent");

            wait_us(1000);
        }

    }



#else
    SPI spi(PA_7, PA_6, PA_5);
    CAN can2(PA_11, PA_12, 1000000);  //rd, td, hz
    CAN3 can(spi, PB_6);

#endif

