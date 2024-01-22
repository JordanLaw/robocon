#ifndef _ABI_ENCODER_H
#define _ABI_ENCODER_H

#include <mbed.h>

class abi_encoder{
    private:
        InterruptIn A;
        InterruptIn B;

        uint8_t A_state, B_state = 0;

        volatile int64_t cnt = 0;

        volatile int before_state = 0;
        volatile int state = 0;

        uint16_t spr = 4000;
        float related_distance = 0.0f;

        void init_pins();
        void updateState();

        void A_rise();
        void B_rise();
        void A_fall();
        void B_fall();

    public:
        /** Creates abi_encoder object with specific content.
         *
         *  @param pin_A    Pin of incremental signal A
         *  @param pin_B    Pin of incremental signal B
         *  @param spr      Steps per revolution
         */
        abi_encoder(PinName pin_A, PinName pin_B, uint16_t spr = 4000);

        /** Set the Steps per revolution (SPR).
         *
         *  @param spr      Steps per revolution
         */
        void setSPR(uint16_t spr);

        /* Get the value of Steps per revolution (SPR)*/
        uint16_t getSPR();

        /** Get the amount of steps per revolution.
         *
         *  @return     Get the amount of steps per revolution
         */
        int64_t getAmountSPR();

        /** Get the number of related rotation turns
         *
         *  @return     Get the number of related rotation turns
         */
        float getRelatedTurns();
};

#endif