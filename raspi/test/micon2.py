#!/usr/bin/python -u
# -*- coding: utf-8 -*-

import smbus
import time


## Motor Driver

CW = 0   # clockwise
CCW = 1  # counter clock wise


bus = smbus.SMBus(1)
addr = 0x1a


dir1 = CW
pwm1 = 0

frame = 0

kicker = 0 # 4
micro_sw = 0 #3


ir1 = 0
ir2 = 0
ir3 = 0
ir4 = 0
ir5 = 0
ir6 = 0
ir7 = 0
ir8 = 0

try:
  while True:

    # set motor val
    if pwm1 >= 255-10:
      dir1 = CCW if dir1==CW else CW
    pwm1 = 0 if pwm1 >= 255-10 else pwm1 + 10

    kicker = 0
    if frame % 20 == 0 :
      kicker = 1
      #kicker = 1 if kicker != 1 else 0

    
    # i2c
    bus.write_byte_data(addr, 0x01, dir1)
    bus.write_byte_data(addr, 0x02, pwm1)

    micro_sw = bus.read_byte_data(addr, 0x03)
    bus.write_byte_data(addr, 0x04, kicker)

    ir1 = bus.read_byte_data(addr, 0x11)
    ir2 = bus.read_byte_data(addr, 0x12)
    ir3 = bus.read_byte_data(addr, 0x13)
    ir4 = bus.read_byte_data(addr, 0x14)
    ir5 = bus.read_byte_data(addr, 0x15)
    ir6 = bus.read_byte_data(addr, 0x16)
    ir7 = bus.read_byte_data(addr, 0x17)
    ir8 = bus.read_byte_data(addr, 0x18)

    v1 = bus.read_byte_data(addr, 0x05)

    # print
    print("pwm1 : " + str(pwm1) + " dir1 : "+str(dir1)
          + " micro_sw :" + str(micro_sw)
          + " kicker : " + str(kicker)
          + "\t ir:"+ str([ir1,ir2,ir3,ir4,ir5,ir6,ir7,ir8])
          + " " + str(v1))
    
    time.sleep(0.1)
    frame += 1


except KeyboardInterrupt:
  pass
