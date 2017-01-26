#!/usr/bin/python -u
# -*- coding: utf-8 -*-

import smbus
import time


## smbus test

bus = smbus.SMBus(1)
addr = 0x0a


out_led = [1,0,1,0]
out_num = 0
got_num = 0

try:
  while True:
    
    for i in range(len(out_led)):
      out_led[i] = (1 if out_led[i] == 0 else 0)  
    bus.write_byte_data(addr, 0x01, out_led[0])
    bus.write_byte_data(addr, 0x02, out_led[1])

    
    out_num = (0x00 if out_num == 0xff-1 else out_num+1)
    bus.write_byte_data(addr, 0x03, out_num)
    got_num = bus.read_byte_data(addr,0x04)
    
    print("out num : " +str(out_num)+" , got num : " +str(got_num)
          + " | led_out : " +str(out_led))
    time.sleep(0.1)


except KeyboardInterrupt:
  pass
