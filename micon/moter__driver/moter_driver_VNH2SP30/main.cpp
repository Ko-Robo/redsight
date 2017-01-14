// micon for controll moterdriver VNH2SP30 using LPC1114
// refed URL: http://garagelab.com/profiles/blogs/tutorial-how-to-use-the-monster-moto-shield

#include "mbed.h"

#define CW 1  // clock wise
#define CCW 2 // counter clock wise
#define ERR_WISE 0 // Error wise
#define SAFERY_CURRENT 100 // max analog value of current of each motor

class Motor{
private:
  PwmOut *pwm; 
  DigitalOut *cw;  // clock wise
  DigitalOut *ccw; // counter clock wise 
  
  int direction; // rotate dir :: cw or cww. 
  float pwm_val; // 0 to 1

  void _run(int _direction, float _pwm_val){
    set_rotate_dir(_direction);
    set_pwm(_pwm_val);
  }

  void set_rotate_dir(int _direction){
    direction = _direction;
    if(direction == CW){
      *cw = 1;  *ccw = 0;
    } else if (direction == CCW){
      *cw = 0; *ccw = 1;
    } else {
      *cw = 0; *ccw = 0;
    }
  }
  
  void set_pwm(float _pwm_val){
    pwm_val = _pwm_val;
    pwm->write(pwm_val);
  }
  
public:
  Motor(PinName pwm_pin, PinName cw_pin,
        PinName ccw_pin){
    pwm = new PwmOut(pwm_pin);
    cw = new DigitalOut(cw_pin);
    ccw = new DigitalOut(ccw_pin);
  }

  void stop(){
    set_pwm(0);
    set_rotate_dir(ERR_WISE);
  }

  void run(float _pwm_val){
    if(0 > _pwm_val && -1 < _pwm_val){
      _run(CW, -_pwm_val);
    } else if(0 <= _pwm_val && 1 > _pwm_val) {
      _run(CCW, _pwm_val);
    } else {
      stop();
    }
  }
};


//// test 

int main() {
  
  Motor motor_a(dp2, dp14, dp13);
  
  while(1) {
    motor_a.run(0.8);
    wait_ms(500);

    motor_a.run(0.1);
    wait_ms(500);
    
    motor_a.run(-0.8);
    wait_ms(500);
    
    motor_a.run(-0.1);
    wait_ms(500);    
  }
}
