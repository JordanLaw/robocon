#include "module.h"
#include "mbed.h"
#include "vesc.h"

module::module(vesc* direction, vesc* rpm)
{
    this-> direction = direction;
    this-> rpm = rpm;

}

void module::module_set_mrpm(float mrpm)
{
    rpm->comm_can_set_mrpm(mrpm);



}

void module::module_set_direction(float pos)
{
    direction->comm_can_set_pos(pos);



}

void module::module_set_gearratio(float new_gear_ratio)
{
    gear_ratio = new_gear_ratio; 



}

float module::module_get_direction(){
    
}

float module::module_get_mrpm(){

}

