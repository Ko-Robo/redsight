#include "mbed.h"
#include "motor.hpp"
#include "smbus.hpp"



//// test 




/* sample of pin structure
   motor_a -> vnh2sp30(2)
   dp2     -> digital5 (pwm)
   dp9     -> digital8 (rotate_direction)
   dp10    -> digital7 (rotate_direction)

*/


#define SDA dp5
#define SCL dp27
#define ADDR (0x1A << 1)



class Micon{
private:
  ByteSmbusSlave *smbus;
  Motor* motor_1;

  DigitalIn* micro_sw;
  DigitalOut* kicker;


  DigitalIn* ir1;
  DigitalIn* ir2;
  DigitalIn* ir3;
  DigitalIn* ir4;
  DigitalIn* ir5;
  DigitalIn* ir6;
  DigitalIn* ir7;
  DigitalIn* ir8;
  
  int val; // store value for a moment
  float float_val;
  char send_data[1] = {char(0)};
public:
  Micon(PinName sda, PinName scl, int addr,
        PinName pwm_pin1, PinName cw_pin1, PinName ccw_pin1,
        PinName _micro_sw, PinName _kicker,
        PinName _ir1, PinName _ir2, PinName _ir3, PinName _ir4,
        PinName _ir5, PinName _ir6, PinName _ir7, PinName _ir8){
    
    smbus = new ByteSmbusSlave(sda, scl, addr);
    motor_1 = new Motor(pwm_pin1, cw_pin1, ccw_pin1);

    micro_sw = new DigitalIn(_micro_sw);
    kicker = new DigitalOut(_kicker);

    ir1 = new DigitalIn(_ir1);
    ir2 = new DigitalIn(_ir2);
    ir3 = new DigitalIn(_ir3);
    ir4 = new DigitalIn(_ir4);
    ir5 = new DigitalIn(_ir5);
    ir6 = new DigitalIn(_ir6);
    ir7 = new DigitalIn(_ir7);
    ir8 = new DigitalIn(_ir8);

  }
  
  void update_of_read(){
    // for motor driver
    if(smbus->cmd == 0x01){
      val = smbus->data;
      if (val == 0){
        motor_1->set_rotate_dir(CW);
      }else {
        motor_1->set_rotate_dir(CCW);
      }
    }
    if(smbus->cmd == 0x02){
      float_val = smbus->data+0.00;
      motor_1->set_pwm(float(float_val/256.0));
    }
    // kicker 
    if(smbus->cmd == 0x04)  kicker->write(smbus->data) ;
  }

  void update_of_write(){
    // for micro switch
    if (smbus->cmd == 0x03) send_data[0] = int(micro_sw->read());

    // for liviing check
    if (smbus->cmd == 0x05) send_data[0] = int(10);
    
    // ir sensor
    if(smbus->cmd == 0x11)  send_data[0] = int(ir1->read()) ;
    if(smbus->cmd == 0x12)  send_data[0] = int(ir2->read()) ;
    if(smbus->cmd == 0x13)  send_data[0] = int(ir3->read()) ;
    if(smbus->cmd == 0x14)  send_data[0] = int(ir4->read()) ;
    if(smbus->cmd == 0x15)  send_data[0] = int(ir5->read()) ;
    if(smbus->cmd == 0x16)  send_data[0] = int(ir6->read()) ;
    if(smbus->cmd == 0x17)  send_data[0] = int(ir7->read()) ;
    if(smbus->cmd == 0x18)  send_data[0] = int(ir8->read()) ;


    // communication to master
    smbus->slave->write(send_data, 2);
  }

  
  void update(){

    smbus->cmd_executed = 0;

    smbus->i2c_communication();

    if(!smbus->cmd_executed){
      smbus->cmd_executed = 1;
      update_of_read();
      if (smbus->read_wanted) {
        smbus->read_wanted = 0;
        update_of_write();
      }

    }
  }
};


int main() {
  Micon micon(SDA, SCL, ADDR,
              dp2, dp9, dp10,
              dp13, dp14,
              dp18, dp25, dp26, dp28,
              dp1, dp15, dp16,dp17
              );
  
  while(1){
    micon.update();    
  }
}
