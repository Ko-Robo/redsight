#!/usr/bin/python -u
# -*- coding: utf-8 -*-

import smbus
import time


## Motor Driver


bus = smbus.SMBus(1)
addr = 0x5e



line = ""



while True:
  try:


    line = bus.read_word_data(addr, 0x01)


    # print
    print("line" , line)
    

    time.sleep(0.1)

  except KeyboardInterrupt:
    pass

  except IOError:
    print("io error")
    time.sleep(0.1)
