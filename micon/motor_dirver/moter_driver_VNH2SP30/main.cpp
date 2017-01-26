// micon for controll moterdriver VNH2SP30 using LPC1114
// refed URL: http://garagelab.com/profiles/blogs/tutorial-how-to-use-the-monster-moto-shield

#include "mbed.h"
#include "motor.hpp"
#include "smbus.hpp"


//// test 




/* sample of pin structure
   motor_a -> vnh2sp30(0)
   dp2   -> digital5 (pwm)
   dp14  -> digital8 (rotate_direction)
   dp13  -> digital7 (rotate_direction)

   motor_b -> vnh2sp30(0)
   dp1   -> digital6 (pwm)
   dp11  -> digital4 (rotate_direction)
   dp10  -> digital9 (rotate_direction)

*/

/*
  int main() {
  
  Motor motor_a(dp2, dp14, dp13);
  Motor motor_b(dp1, dp11, dp10);
  //Motor motor_c()
  
  while(1) {
  motor_a.run(0.8);
  motor_b.run(0.8);
  wait_ms(500);

    
  motor_a.run(-0.8);
  motor_b.run(-0.8);
  wait_ms(500);


  }
  }

*/



#define SDA dp5
#define SCL dp27
#define ADDR (0x0A << 1)



class MotorMicon{
private:
  ByteSmbusSlave *smbus;
  Motor* motor_1;
  Motor* motor_2;
  int val; // store value for a moment
  float float_val;
public:
  MotorMicon(PinName sda, PinName scl, int addr,
             PinName pwm_pin1, PinName cw_pin1, PinName ccw_pin1,
             PinName pwm_pin2, PinName cw_pin2, PinName ccw_pin2){
    
    smbus = new ByteSmbusSlave(sda, scl, addr);
    motor_1 = new Motor(pwm_pin1, cw_pin1, ccw_pin1);
    motor_2 = new Motor(pwm_pin2, cw_pin2, ccw_pin2);

  }
  
  void update_of_read(){

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
      //motor_1->set_pwm(0.5);
    }
    
    if (smbus->cmd == 0x03){
      val = smbus->data;
      if (val == 0){
        motor_2->set_rotate_dir(CW);
      }else {
        motor_2->set_rotate_dir(CCW);
      }
    }
    if (smbus->cmd == 0x04){
      float_val = smbus->data+0.00;
      motor_2->set_pwm(float(float_val/256.0));
      //motor_2->set_pwm(0.5);
    }

  }

  void update_of_write(){
    if (smbus->cmd == 0x05){
      char send_data[1] = {float_val};
      smbus->slave->write(send_data, 2);
    }
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
  MotorMicon motor_micon(SDA, SCL, ADDR,
                         dp2, dp14, dp13,
                         dp1, dp11, dp10);
  
  while(1){
    motor_micon.update();
    
  }
}
