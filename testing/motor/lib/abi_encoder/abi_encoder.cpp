#include "abi_encoder.h"

abi_encoder::abi_encoder(PinName pin_A, PinName pin_B, uint16_t spr) : A(pin_A), B(pin_B){
    setSPR(spr);

    init_pins();
}

void abi_encoder::init_pins(){
    A.mode(PullDown);
    B.mode(PullDown);

    A.rise(callback(this, &abi_encoder::A_rise));
    A.fall(callback(this, &abi_encoder::A_fall));
    B.rise(callback(this, &abi_encoder::B_rise));
    B.fall(callback(this, &abi_encoder::B_fall));
}

void abi_encoder::setSPR(uint16_t spr){
    this->spr = spr;
}

uint16_t abi_encoder::getSPR(){
    return spr;
}

void abi_encoder::A_rise(){
    A_state = 0x01;
    updateState();
}

void abi_encoder::B_rise(){
    B_state = 0x01;
    updateState();
}

void abi_encoder::A_fall(){
    A_state = 0x00;
    updateState();
}

void abi_encoder::B_fall(){
    B_state = 0x00;
    updateState();
}

void abi_encoder::updateState(){
    //AB    state_no
    //00    0
    //10    1
    //11    2
    //01    3

    before_state = state;

    switch(((uint16_t)A_state << 4) | (uint16_t)B_state){
        case (uint16_t)0x00:
            state = 0;
            break;

        case (uint16_t)0x10:
            state = 1;
            break;

        case (uint16_t)0x11:
            state = 2;
            break;

        case (uint16_t)0x01:
            state = 3;
            break;

        default:
            break;
    }

    //count plus
    // 01 -> 00 -> 10 -> 11 -> 01 forward(+)    3 -> 0 -> 1 -> 2 -> 3
    // 01 <- 00 <- 10 <- 11 <- 01 reverse(-)    3 <- 0 <- 1 <- 2 <- 3
    // 00 -> 00, 10 -> 10, 11 -> 11, 01 -> 01 no movement
    // 00 -> 11 -> 00, 01 -> 10 -> 01 error     0 -> 2 -> 0, 3 -> 1 -> 3

    int delta = before_state - state;
    if(abs(delta) == 2){
        //error
    }
    else if(delta == 0){
        //no movement
    }
    else if(delta == 3 || delta == -1){
        //forward
        cnt++;
    }
    else if(delta == -3 || delta == 1){
        //reverse
        cnt--;
    }
    else{
        //error
    }
}

int64_t abi_encoder::getAmountSPR(){
    return cnt;
}

float abi_encoder::getRelatedTurns(){
    return (float)((double)cnt/spr);
}