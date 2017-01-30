
#include "mbed.h"




class ByteSmbusSlave{
private:


public:
  I2CSlave* slave;
  int receive;
  char cmd;
  char data;
  char buff[2];
  int read_wanted;
  int cmd_executed;

  
  ByteSmbusSlave(PinName sda, PinName scl, int address){
    slave = new I2CSlave(sda, scl);
    slave->address(address);
  }

  void i2c_communication(){
    receive = slave->receive();
        
    if(receive==I2CSlave::WriteAddressed){
      slave->read(buff, 3);
      cmd = buff[0];
      data = buff[1];
      cmd_executed = 0;
    } 
    if(receive==I2CSlave::ReadAddressed){
      read_wanted =1;
      cmd_executed = 0;
    }
  }


};






//// sample code
// depended on I2C test.py 

/*
#define SDA dp5
#define SCL dp27
#define ADDR (0x0A << 1)

DigitalOut led1(dp10);
DigitalOut led2(dp11);
int got_num;    


class SmbusTest{
private:
  ByteSmbusSlave *smbus;
public:
  SmbusTest(PinName sda, PinName scl, int addr){
    smbus = new ByteSmbusSlave(sda, scl, addr);

    
  }
  void update_of_read(){

    if(smbus->cmd == 0x01){
      led1 = smbus->data;
    }
    if(smbus->cmd == 0x02){
      led2 = smbus->data;
    }
    if (smbus->cmd == 0x03){
      got_num = smbus->data;
    }
  }

  void update_of_write(){
    if (smbus->cmd == 0x04){
      char send_data[1] = {got_num};
      smbus->slave->write(send_data, 2);
    }
  }

  void update(){

    smbus->read_wanted = 0;
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
  SmbusTest smbus_test(SDA, SCL, ADDR);
  
  while(1){
    smbus_test.update();
    
  }
}
*/
