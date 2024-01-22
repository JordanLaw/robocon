#include "mbed.h"
#include "vesc.h"
#include "module.h"
#include "can_packet.h"
#include "abi_encoder.h"
#include "communication_format.h"
#include <math.h>

#define zigbee_tx PA_9
#define zigbee_rx PA_10
#define zigbee_baud 9600

BufferedSerial zigbee(zigbee_tx, zigbee_rx, zigbee_baud); //tx rx baud
// BufferedSerial pc(USBTX, USBRX, 9600);
remote_msg in_msg;

void getRemote_packet(){
  in_msg = remote_msg();
  uint8_t buf[1] = {0};
  zigbee.read(buf, sizeof(buf));
  in_msg.startByte = (int8_t)buf[0];
  
  if(in_msg.startByte != start_byte){
    return;
  }

  zigbee.read(buf, sizeof(buf));
  in_msg.x = (int8_t)buf[0];
  zigbee.read(buf, sizeof(buf));
  in_msg.y = (int8_t)buf[0];
  zigbee.read(buf, sizeof(buf));
  in_msg.w = (int8_t)buf[0];
  zigbee.read(buf, sizeof(buf));
  in_msg.operation1 = (int8_t)buf[0];
  zigbee.read(buf, sizeof(buf));
  in_msg.operation2 = (int8_t)buf[0];
  zigbee.read(buf, sizeof(buf));
  in_msg.operation3 = (int8_t)buf[0];
//   printf("%X %X %X %X %X %X %X\n", (int8_t)msg[0], (int8_t)msg[1], (int8_t)msg[2], (int8_t)msg[3], (int8_t)msg[4], (int8_t)msg[5], (int8_t)msg[6]);
//   printf("x: %d, y: %d, w: %d, oper1:%d, oper2:%d, oper3:%d \n\r", in_msg.x, in_msg.y, in_msg.w, in_msg.operation1, in_msg.operation2, in_msg.operation3);

  //   in_msg.x = (int8_t)zigbee.getc();
  //   in_msg.y = (int8_t)zigbee.getc();
  //   in_msg.w = (int8_t)zigbee.getc();
  //   in_msg.operation1 = (int8_t)zigbee.getc();
  //   in_msg.operation2 = (int8_t)zigbee.getc();
  //   in_msg.operation3 = (int8_t)zigbee.getc();

  in_msg.up_flag = (uint8_t) (in_msg.operation1 & 0x01);
  in_msg.down_flag = (uint8_t) ((in_msg.operation1 >> 1) & 0x01);
  in_msg.Left_flag = (uint8_t) ((in_msg.operation1 >> 2) & 0x01);
  in_msg.Right_flag = (uint8_t) ((in_msg.operation1 >> 3) & 0x01);
  in_msg.A_flag = (uint8_t) ((in_msg.operation1 >> 4) & 0x01);
  in_msg.B_flag = (uint8_t) ((in_msg.operation1 >> 5) & 0x01);
  in_msg.X_flag = (uint8_t) ((in_msg.operation1 >> 6) & 0x01);
  in_msg.Y_flag = (uint8_t) ((in_msg.operation1 >> 7) & 0x01);

  in_msg.L1 = (uint8_t) (in_msg.operation2 & 0x01);
  in_msg.L2 = (uint8_t) ((in_msg.operation2 >> 1) & 0x01);
  in_msg.R1 = (uint8_t) ((in_msg.operation2 >> 2) & 0x01);
  in_msg.R2 = (uint8_t) ((in_msg.operation2 >> 3) & 0x01);
  in_msg.LjoystickSW = (uint8_t) ((in_msg.operation2 >> 4) & 0x01);
  in_msg.RjoystickSW = (uint8_t) ((in_msg.operation2 >> 5) & 0x01);

  in_msg.ESTOP = (uint8_t) (in_msg.operation3 & 0x01);
  in_msg.Reset_button = (uint8_t) ((in_msg.operation3 >> 1) & 0x01);
  in_msg.Home = (uint8_t) ((in_msg.operation3 >> 2) & 0x01);

//   printf("x: %d, y: %d, w: %d, oper1:%d, oper2:%d, oper3:%d \n\r", in_msg.x, in_msg.y, in_msg.w, in_msg.operation1, in_msg.operation2, in_msg.operation3);
//   printf("x: %d, y: %d, w: %d, up:%d, down:%d, left:%d, right:%d, A:%d, B:%d, X:%d, Y:%d, L1:%d, L2:%d, R1:%d, R2:%d, LSW:%d, RSW:%d, estop:%d, reser:%d, Home:%d \n\r", in_msg.x, in_msg.y, in_msg.w, in_msg.up_flag, in_msg.down_flag, in_msg.Left_flag, in_msg.Right_flag, in_msg.A_flag, in_msg.B_flag, in_msg.X_flag, in_msg.Y_flag, in_msg.L1, in_msg.L2, in_msg.R1, in_msg.R2, in_msg.LjoystickSW, in_msg.RjoystickSW, in_msg.ESTOP, in_msg.Reset_button, in_msg.Home);
//  pc.puts((char*)&in_msg);
// printf("hello world\r\n");
//   pc.printf("X: %d, Y: %d, W: %d\n", x, y, w);
}

// BufferedSerial pc (USBTX, USBRX,9600);
DigitalIn userbutton(USER_BUTTON);

CAN can2(PA_11, PA_12, 1000000);  //rd, td, hz
CAN can1(PB_5, PB_13, 1000000);  //rd, td, hz
// CAN can2(PB_5, PB_13, 1000000);  //rd, td, hz
// vesc direction(6, &can1, 1000000, Motor_type::m3508);
vesc dir6(6, &can2, 1000000, Motor_type::m3508);
vesc dir10(10, &can2, 1000000, Motor_type::m3508);
vesc dir57(57, &can2, 1000000, Motor_type::m3508);
vesc rpm20(20, &can1, 1000000, Motor_type::m3508);
vesc rpm114(114, &can1, 1000000, Motor_type::m3508);
vesc rpm61(61, &can1, 1000000, Motor_type::m3508);

abi_encoder encoder57(PA_1, PA_0); //rx, tx
abi_encoder encoder6(PD_2, PC_12); //rx, tx
abi_encoder encoder10(PC_11, PC_10); //rx, tx

abi_encoder encoder_tickLeft(PD_2, PC_12); //rx, tx
abi_encoder encoder_tickRight(PC_11, PC_10); //rx, tx
abi_encoder encoder_tickAux(PA_1, PA_0); //rx, tx

int old_R_pos = 0;
int old_L_pos = 0;
int old_A_pos = 0;

int current_R_pos = 0;
int current_L_pos = 0;
int current_A_pos = 0;

float L = 14.0f;
float B = 14.0f;
float R = 4.95f/2;
float N = 4000.0f;
float cm_per_tick = 2.0 * M_PI * R / N;

float pos_x = 0.0f;
float pos_y = 0.0f;
float pos_h = 0.0f;

void odometry(){
    old_A_pos = current_A_pos;
    old_L_pos = current_L_pos;
    old_R_pos = current_R_pos;

    current_A_pos = -encoder_tickAux.getAmountSPR();
    current_L_pos = encoder_tickLeft.getAmountSPR();
    current_R_pos = encoder_tickRight.getAmountSPR();

    int dn1 = current_L_pos - old_L_pos;
    int dn2 = current_R_pos - old_R_pos;
    int dn3 = current_A_pos - old_A_pos;

    float dtheta = cm_per_tick * (dn2 - dn1) / L ;
    float dx = cm_per_tick * (dn1 + dn2) / 2.0;
    float dy = cm_per_tick * (dn3 - (dn2 - dn1) * B /L);

    float theta = pos_h * (dtheta / 2.0);
    pos_x += dx * cos(theta) - dy * sin(theta);
    pos_y += dx * sin(theta) + dy * cos(theta);
    pos_h += dtheta;

    float tL = current_L_pos * cm_per_tick;
    float tR = current_R_pos * cm_per_tick;

    printf("pos_x: %d.%d\n", (int)pos_x, abs((int)((float)(pos_x-(int)pos_x)*100000000)));
    printf("pos_y: %d.%d\n", (int)pos_y, abs((int)((float)(pos_y-(int)pos_y)*100000000)));
    // printf("pos_h: %d.%d\n", (int)pos_h, abs((int)((float)(pos_h-(int)pos_h)*100000000)));

}

#define PI 3.1415926535897932384626433832795

// module module1(&direction, &rpm);

float target_turns10;
float target_turns6;
float target_turns57;

float kp10 = 0.11f;
float ki10 = 0.01f;
float kd10 = 1000.0f;

float turns10 = 0.0f;
float Theta10, Theta_d10;
float derdt10;
int dt10;
unsigned long t10;
unsigned long t10_prev;
float e10, e10_prev = 0, inte10, inte10_prev = 0;
float rpm_10 = 0.0f;

float kp6 = 0.11f;
float ki6 = 0.01f;
float kd6 = 1000.0f;

float turns6 = 0.0f;
float Theta6, Theta_d6;
int dt6;
unsigned long t6;
unsigned long t6_prev;
float e6, e6_prev = 0, inte6, inte6_prev = 0;
float derdt6 = 0.0f;
float rpm_6 = 0.0f;

float kp57 = 0.11f;
float ki57 = ki10;
float kd57 = kd10;

float turns57 = 0.0f;
float Theta57, Theta_d57;
int dt57;
unsigned long t57;
unsigned long t57_prev;
float e57, e57_prev = 0, inte57, inte57_prev = 0;
float derdt57 = 0.0f;
float rpm_57 = 0.0f;

float currentMax = 1.5;
float currentMin = -1.5;
float rpm_Max = 7000.000000f;
float rpm_Min = -7000.000000f;
float rpm_61_speed = 0.0f;
float rpm_20_speed = 0.0f;
float rpm_114_speed = 0.0f;

Timer timer1;

void direction10_change(){
    Theta10 = encoder10.getAmountSPR();
    Theta_d10 = target_turns10;

    timer1.stop();
    t10 = timer1.read_us();

    dt10 = (t10 - t10_prev);

    e10 = Theta_d10 - Theta10;
    inte10 += dt10 * e10/1000000;
    derdt10 = (e10 - e10_prev) / dt10;
    rpm_10 = kp10 * e10 + ki10 * inte10 + (kd10 * derdt10);

    // dir10.comm_can_set_duty(duty_10);
    dir10.comm_can_set_mrpm(rpm_10);

    // printf("e10: %d\n", (int)e10);
    // printf("dt10: %d\n", (int)dt10);

    // printf("turn10: %d\n", (int)Theta10);
    // printf("%d",(int)derdt10);
    
    // inte10_prev = inte10;
    e10_prev = e10;
    t10_prev = t10;
    timer1.start();

}

void direction6_change(){
    Theta6 = encoder6.getAmountSPR();
    Theta_d6 = target_turns6;

    timer1.stop();
    t6 = timer1.read_us();

    dt6 = (t6 - t6_prev);

    e6 = Theta_d6 - Theta6;
    inte6 += dt6 * e6 / 1000000;
    derdt6 = (e6 - e6_prev) / dt6;
    rpm_6 = kp6 * e6 + ki6 * inte6 + (kd6 * derdt6);

    // rpm_6 = rpm_Max * PID_6;
    // printf("duty_6b: %d.%d\n", (int)duty_6, (int)((float)(duty_6-(int)duty_6)*600000000));

    // dir6.comm_can_set_duty(duty_6);
    dir6.comm_can_set_mrpm(rpm_6);
    
    // inte6_prev = inte6;
    e6_prev = e6;
    t6_prev = t6;
    timer1.start();

}

void direction57_change(){
    Theta57 = encoder57.getAmountSPR();
    Theta_d57 = target_turns57;

    timer1.stop();
    t57 = timer1.read_us();

    dt57 = (t57 - t57_prev);

    e57 = Theta_d57 - Theta57;
    inte57 += dt57 * e57 /1000000;
    derdt57 = (e57 - e57_prev) / dt57;
    rpm_57 = kp57 * e57 + ki57 * inte57 + (kd57 * derdt57);

    // rpm_57 = rpm_Max * PID_57;


    // printf("duty_57b: %d.%d\n", (int)duty_57, (int)((float)(duty_57-(int)duty_57)*5700000000));

    if (rpm_57 >= rpm_Max) {
        rpm_57 = rpm_Max;
    }

    if (rpm_57 <= rpm_Min){
        rpm_57 = rpm_Min;
    }
    
    // dir57.comm_can_set_duty(duty_57);
    dir57.comm_can_set_mrpm(rpm_57);

    // inte57_prev = inte57;
    e57_prev = e57;
    t57_prev = t57;
    timer1.start();

}

void control(){
       if (in_msg.Left_flag or in_msg.Right_flag or in_msg.up_flag or in_msg.down_flag){
            if(in_msg.Left_flag){
                target_turns10 = 76575/4;
                target_turns6 = 76575/4;
                target_turns57 = 76575/4;
                direction10_change();
                direction57_change();
                direction6_change();
            }

            else if (in_msg.Right_flag)
            {
                target_turns10 = -76575/4;
                target_turns6 = -76575/4;
                target_turns57 = -76575/4;
                direction10_change();
                direction57_change();
                direction6_change();
            }
        
            // else if (in_msg.down_flag)
            // {
            //     target_turns = 19.18575f/4*2;
            //     target_turns57 = 19.10625f/4*2;
            //     direction10_change();
            //     direction57_change();
            //     direction6_change();

            // }
        
        }
        // // }

        else{
                target_turns10 = 0;
                target_turns6 = 0;
                target_turns57 = 0;
                direction10_change();
                direction57_change();
                direction6_change();
        }

        if (in_msg.Y_flag or in_msg.X_flag){
            if (in_msg.Y_flag){
                rpm_61_speed += 1000;
                rpm_20_speed += 1000;
                rpm_114_speed += 1000;
                rpm61.comm_can_set_mrpm(rpm_61_speed);
                rpm20.comm_can_set_mrpm(rpm_20_speed);
                rpm114.comm_can_set_mrpm(rpm_114_speed);

            }

            else if (in_msg.X_flag){
                rpm_61_speed -= 1000;
                rpm_20_speed -= 1000;
                rpm_114_speed -= 1000;
                rpm61.comm_can_set_mrpm(rpm_61_speed);
                rpm20.comm_can_set_mrpm(rpm_20_speed);
                rpm114.comm_can_set_mrpm(rpm_114_speed);
            }

        }

        else{
            rpm61.comm_can_set_mrpm(rpm_61_speed);
            rpm20.comm_can_set_mrpm(rpm_20_speed);
            rpm114.comm_can_set_mrpm(rpm_114_speed);
        }

        if (in_msg.ESTOP){
            rpm_61_speed = 0;
            rpm_20_speed = 0;
            rpm_114_speed = 0;
            rpm61.comm_can_set_mrpm(rpm_61_speed);
            rpm20.comm_can_set_mrpm(rpm_20_speed);
            rpm114.comm_can_set_mrpm(rpm_114_speed);
        }

}


int main(){

    //setup

    while(1){
        // getRemote_packet();
        // control();

        odometry();
            




        // // else{
        // //     target_turns = 0;
        // //     target_turns57 = 0;
        // //     direction10_change();
        // //     direction57_change();
        // //     direction6_change();
        // //     rpm61.comm_can_set_duty(0.0f);
        // //     rpm20.comm_can_set_duty(0.0f);
        // //     rpm114.comm_can_set_duty(0.0f);
        
        // // turns10 = encoder10.getAmountSPR();
        // // printf("turn10: %d\n", (int)turns10);

        // // turns6 = encoder6.getRelatedTurns();
        // // printf("turn6: %d.%d\n", (int)turns6, (int)((float)(turns6-(int)turns6)*100000000));

        // // turns57 = encoder57.getRelatedTurns();
        // // printf("turn57: %d.%d\n", (int)turns57, (int)((float)(turns57-(int)turns57)*100000000));
        // printf("turn57: %d\n", (int)e57);
        // printf("rpm_57: %d\n", (int)rpm_57);

        // if (!userbutton){

        //     target_turns10 = 76575/4;
        //     target_turns6 = 76575/4;
        //     target_turns57 = 76575/4;
        //     direction10_change();
        //     direction57_change();
        //     direction6_change();
        //     rpm61.comm_can_set_mrpm(200);
        //     rpm20.comm_can_set_mrpm(200);
        //     rpm114.comm_can_set_mrpm(200);



        
        
        // }

        // else{
        //     target_turns10 = 0;
        //     target_turns6 = 0;
        //     target_turns57 = 0;
        //     direction10_change();
        //     direction57_change();
        //     direction6_change();
        //     rpm61.comm_can_set_mrpm(0);
        //     rpm20.comm_can_set_mrpm(0);
        //     rpm114.comm_can_set_mrpm(0);
        // }



        // if (!userbutton){
        //     if (turns <= target_turns){
        //         dir.comm_can_set_duty(0.2f);
        //         reverse_turn = 1;                
        //     }
        //     else if (turns >= target_turns)
        //     {
        //         dir.comm_can_set_duty(-0.2f);
        //         reverse_turn = 0;  
                       
        //     }

        //     rpm.comm_can_set_duty(0.2f);

        //     // module1.module_set_direction(90)
        // }
        // else{
        //     rpm.comm_can_set_duty(0.0f);
        // }

        // printf("turn: %d.%d\n", (int)turns, (int)((float)(turns-(int)turns)*1000000000));
        // printf("direction: %d\n", reverse_turn);

            
        // //     printf("angle: %lld\n", encoder.getAmountSPR());

        
        // if (turns >= target_turns && reverse_turn == 1){
        //     dir.comm_can_set_duty(0.0f);
        //     rpm.comm_can_set_duty(0.0f);

        // }

        // else if (turns <= target_reverse_turns && reverse_turn == 0){
        //     dir.comm_can_set_duty(0.0f);
        //     rpm.comm_can_set_duty(0.0f);
        // }

        // if (!userbutton){

        //     rpm.comm_can_set_mrpm(2000.0f);
        // }

        // else{
        //     rpm.comm_can_set_mrpm(0.0f);
        //}



        wait_ns(1);
    }
}

