#ifndef _XM_MOTOR_H
#define _XM_MOTOR_H

#include "mbed.h"
#include <SPI.h>
#include "CAN3.h"

#define pi 3.14159265359f
#define Communication_Type_MotorEnable 0x03
#define Master_CAN_ID 0x00
#define CanID 0x01
#define P_MIN -12.5f
#define P_MAX 12.5f
#define V_MIN -30.0f
#define V_MAX 30.0f
#define KP_MIN 0.0f
#define KP_MAX 500.0f
#define KD_MIN 0.0f
#define KD_MAX 5.0f
#define T_MIN -12.0f
#define T_MAX 12.0f
#define MAX_P 720
#define MIN_P -720

#define Communication_Type_GetID 0x00           //获取设备的ID和64位MCU唯一标识符
#define Communication_Type_MotionControl 0x01         //用来向主机发送控制指令
#define Communication_Type_MotorRequest 0x02        //用来向主机反馈电机运行状态
#define Communication_Type_MotorEnable 0x03            //电机使能运行
#define Communication_Type_MotorStop 0x04            //电机停止运行
#define Communication_Type_SetPosZero 0x06            //设置电机机械零位
#define Communication_Type_CanID 0x07                //更改当前电机CAN_ID
#define Communication_Type_Control_Mode 0x12
#define Communication_Type_GetSingleParameter 0x11        //读取单个参数
#define Communication_Type_SetSingleParameter 0x12        //设定单个参数
#define Communication_Type_ErrorFeedback 0x15            //故障反馈帧
//参数读取宏定义
#define Run_mode 0x7005        
#define Iq_Ref   0x7006
#define Spd_Ref  0x700A
#define Limit_Torque 0x700B
#define Cur_Kp 0x7010
#define Cur_Ki 0x7011
#define Cur_Filt_Gain 0x7014
#define Loc_Ref 0x7016
#define Limit_Spd 0x7017
#define Limit_Cur 0x7018
#define Gain_Angle 720/32767.0
#define Bias_Angle 0x8000
#define Gain_Speed 30/32767.0
#define Bias_Speed 0x8000
#define Gain_Torque 12/32767.0
#define Bias_Torque 0x8000
#define Temp_Gain   0.1

#define Motor_Error 0x00
#define Motor_OK 0X01

#define CAN_EFF_FLAG 0x80000000UL


class xm_motor{
    private:
        enum CONTROL_MODE   //控制模式定义
            {
                Motion_mode = 0,//运控模式  
                Position_mode,  //位置模式
                Speed_mode,     //速度模式  
                Current_mode    //电流模式
            };
        enum ERROR_TAG      //错误回传对照
            {
                OK                 = 0,//无故障
                BAT_LOW_ERR        = 1,//欠压故障
                OVER_CURRENT_ERR   = 2,//过流
                OVER_TEMP_ERR      = 3,//过温
                MAGNETIC_ERR       = 4,//磁编码故障
                HALL_ERR_ERR       = 5,//HALL编码故障
                NO_CALIBRATION_ERR = 6//未标定
            };
        typedef struct{           //小米电机结构体
                    uint8_t CAN_ID;       //CAN ID
                    uint8_t MCU_ID;       //MCU唯一标识符【后8位，共64位】
                    float Angle;          //回传角度
                    float Speed;          //回传速度
                    float Torque;         //回传力矩
                    float Temp;                          //回传温度
                    
                    uint16_t set_current;
                    uint16_t set_speed;
                    uint16_t set_position;
                    
                    uint8_t error_code;
                    
                    float Angle_Bias;
                    
            }MI_Motor;

        MI_Motor mi_motor;//预先定义1个小米电机

        int id;
        CAN3* CAN0;
        // CAN* CAN0;
        
        CANMessage Txmsg;
        CANMessage Rxmsg;

        uint32_t ExtId;             //定义can扩展id
        uint8_t rx_data[8];         //接收数据
        uint32_t Motor_Can_ID;      //接收数据电机ID
        uint8_t byte_ls[4];  //转换临时数据
        uint8_t tx_data[8];         //can写入的数据

        typedef unsigned char byte;

    public:
        CANMessage canMsg;

        xm_motor(int CAN_ID, CAN3* _CAN);
        void xm_motor_init(int CAN_ID, CAN3* _CAN);

        uint8_t* Float_to_Byte(float f);
        static float uint16_to_float(uint16_t x, float x_min, float x_max, int bits);
        static int float_to_uint(float x, float x_min, float x_max, int bits);

        void exid_count(uint8_t Communication_Type, uint16_t msid, uint8_t can_id);

        void data_count_dcs(uint16_t Index, float Value, char Value_type);

        void data_count_zero();

        void xm_can_start();
        void motor_enable( uint8_t id ) ;
        void motor_mode( uint8_t id ,char type );
        void motor_speed_value( uint8_t id ,float speed_ref );//-30rad-30rad
        void motor_yk( uint8_t id ,float torque, float MechPosition, float speed, float kp, float kd );
        void motor_pos_zero( uint8_t id ); //位置置0
        void motor_pos_value( uint8_t id ,float speed_ref );
        void motor_pow_value( uint8_t id , float torque,float limit_cur ,float  kp,float kd );

        int filter(int queue[], char n) ; //数值过滤
        // int check(byte ao_port, byte n); //获取ad口电压</font></font></font>

};

#endif


