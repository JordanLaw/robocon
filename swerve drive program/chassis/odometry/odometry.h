#ifndef _ODOMETRY_H
#define _ODOMETRY_H

#include "mbed.h"
#include "abi_encoder.h"

class odometry{
    private:
        // Encoder variable
        int old_R_pos = 0;
        int old_L_pos = 0;
        int old_A_pos = 0;

        int current_R_pos = 0;
        int current_L_pos = 0;
        int current_A_pos = 0;

        // Hardware setting value
        float L = 56.5f;                            // distance between left encoder and right encoder
        float B = 13.5f;                            // distance between aux encoder and 2 encoder
        float R = 4.95f/2;                          // R of wheel
        float N = 4000.0f;                          // ticks per round of the encoder
        float cm_per_tick = 2.0 * M_PI * R / N;     // tranform the distance travel unit to cm

        abi_encoder* Right;
        abi_encoder* Left;
        abi_encoder* Aux;
        BufferedSerial* Message_odom;

        uint8_t buf [13];
        unsigned char bytes[4];
        unsigned char byte_start = 0xAA;

        unsigned char* bytes_A;
        unsigned char* bytes_R;
        unsigned char* bytes_L;

    public:

        odometry(abi_encoder* Right, abi_encoder* Left, abi_encoder* Aux);

        float* odometry_cal();
        void odom_send();
        unsigned char* int_to_byte(int z);

        // Position variable
        float position [4];
        float pos_x = 0.0f;
        float pos_y = 0.0f;
        float pos_h = 0.0f;
        float theta = 0.0f;
};

#endif