#include <Arduino.h>

#ifndef MSG_h
#define MSG_h

    class msg{
        private:
        uint8_t start_byte= 0xff;
        HardwareSerial * nano;

        int x_speed=0;
        int y_speed=0;
        int w_speed=0;

        bool isCloseClip =false;
        int lifting_status =0 ;

        public:

        void init(HardwareSerial * serial);
        bool read();
        int getX_speed();
        int getY_speed(); 
        int getW_speed();

        bool get_isCloseClip();
        int getLifting_status();
    };
#endif

