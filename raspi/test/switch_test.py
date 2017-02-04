import  RPi.GPIO as gpio
from time import sleep

pin1 = 32
pin2 = 36
pin3 = 38




gpio.setmode(gpio.BOARD)
gpio.setup(pin1, gpio.IN)
gpio.setup(pin2, gpio.IN)
gpio.setup(pin3, gpio.IN)

while True:
  print(gpio.input(pin1), gpio.input(pin2), gpio.input(pin3))
  sleep(0.1)
