#!/usr/bin/python -u
# -*- coding: utf-8 -*-

import smbus
import time


## Motor Driver

CW = 0   # clockwise
CCW = 1  # counter clock wise


bus = smbus.SMBus(1)
addr = 0x0a

dir1 = CW
pwm1 = 0
dir2 = CCW
pwm2 = 128

frame = 0

try:
  while True:

    # set motor val
    if pwm1 >= 255-10:
      dir1 = CCW if dir1==CW else CW
    pwm1 = 0 if pwm1 >= 255-10 else pwm1 + 3
    
    if pwm2 >= 255-10:
      dir2 = CCW if dir2==CW else CW
    pwm2 = 0 if pwm2 >= 255-10 else pwm2 + 3
    
    # i2c
    bus.write_byte_data(addr, 0x01, dir1)
    bus.write_byte_data(addr, 0x02, pwm1)
    bus.write_byte_data(addr, 0x03, dir2)
    bus.write_byte_data(addr, 0x04, pwm2)
    bus.write_byte_data(addr, 0x05, dir2)
    bus.write_byte_data(addr, 0x06, pwm2)

    v1 = bus.read_byte_data(addr, 0x07)

    # print
    print("pwm1 : " + str(pwm1) + " dir1 : "+str(dir1)
          +"\t | pwm2 : " + str(pwm2) + " dir1 : "+str(dir2)
          +" " + str(v1))
    
    time.sleep(0.1)
    frame += 1


except KeyboardInterrupt:
  pass
