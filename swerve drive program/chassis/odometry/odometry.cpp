#include "odometry.h"
#include <math.h>

odometry::odometry(abi_encoder* Right, abi_encoder* Left, abi_encoder* Aux){
    this->Right = Right;
    this->Left = Left;
    this->Aux = Aux;

}

float* odometry::odometry_cal(){
    old_A_pos = current_A_pos;
    old_L_pos = current_L_pos;
    old_R_pos = current_R_pos;

    current_A_pos = Aux->getAmountSPR();
    current_L_pos = Left->getAmountSPR();
    current_R_pos = Right->getAmountSPR();

    // printf("A: %d, L: %d, R: %d\n", current_A_pos, current_L_pos, current_R_pos);

    int dn1 = current_L_pos - old_L_pos;
    int dn2 = current_R_pos - old_R_pos;
    int dn3 = current_A_pos - old_A_pos;

    double dtheta = cm_per_tick * (dn2 - dn1) / L ;
    float dx = cm_per_tick * (dn1 + dn2) / 2.0;
    float dy = cm_per_tick * (dn3 - (dn2 - dn1) * B /L);

    // theta = pos_h * (dtheta / 2.0);
    // theta_test = pos_h * 180 / PI;
    // test_n = cos(pos_h);
    // pos_x += dx * cos(pos_h) - dy * sin(pos_h);
    // pos_y += dx * sin(pos_h) + dy * cos(pos_h);
    pos_h += dtheta;

    position[0] += dx * cos(pos_h) - dy * sin(pos_h);
    position[1] += dx * sin(pos_h) + dy * cos(pos_h);
    position[2] += dtheta;
    position[3] = position[2] * 180 / M_PI;

    //  

    return position;
}

void odometry::odom_send(){

    current_A_pos = -Aux->getAmountSPR();
    current_L_pos = Left->getAmountSPR();
    current_R_pos = Right->getAmountSPR();

    buf[0] = byte_start;

    bytes_A = int_to_byte(current_A_pos);

    for (int i = 0; i < 4; i++){
        buf[i+1] = bytes_A[i];
    }

    bytes_L = int_to_byte(current_L_pos);

    for (int i = 0; i < 4; i++){
        buf[i+5] = bytes_L[i];
    }

    bytes_R = int_to_byte(current_R_pos);    

    for (int i = 0; i < 4; i++){
        buf[i+9] = bytes_R[i];
    }

    // printf("%X, %X, %X, %X, %X, %X, %X, %X, %X, %X, %X, %X", buf[0], buf[1], buf[2], buf[3], buf[4], buf[5], buf[6], buf[7], buf[8], buf[9], buf[10], buf[11]);
    // printf("\n");


    unsigned int A = buf[1]*256*256*256 + buf[2]*256*256 + buf[3]*256 + buf[4];
    unsigned int L = buf[5]*256*256*256 + buf[6]*256*256 + buf[7]*256 + buf[8];
    unsigned int R = buf[9]*256*256*256 + buf[10]*256*256 + buf[11]*256 + buf[12];
    printf("F: %d, L: %d, R: %d\n", A, L, R);

    if (Message_odom->writable()){
        Message_odom->write(&buf, 13);
        wait_us(1);

    }
    else{
        printf("Serial port not connected\n");
    }

}

unsigned char* odometry::int_to_byte(int z){
    bytes[0] = (z >> 24) & 0xFF;
    bytes[1] = (z >> 16) & 0xFF;
    bytes[2] = (z >> 8) & 0xFF;
    bytes[3] = (z) & 0xFF;

    return bytes;
}