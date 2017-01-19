import  RPi.GPIO as gpio
from time import sleep

def my_callback(channel):
  global ledState
  global pushed_num
  if channel == 24 :
    ledState = not ledState
    if ledState == gpio.HIGH:
      gpio.output(25, gpio.HIGH)
    else :
      gpio.output(25, gpio.LOW)
    pushed_num += 1
    print(pushed_num)

      
gpio.setmode(gpio.BCM)
gpio.setup(25, gpio.OUT, initial=gpio.LOW)
gpio.setup(24, gpio.IN, pull_up_down=gpio.PUD_DOWN)
gpio.add_event_detect(24, gpio.RISING, callback=my_callback, bouncetime=200)

pushed_num = 0
ledState = gpio.HIGH

try:
  while True:
    sleep(0.01)

except KeyboardInterrupt:
  pass

print("ending test")
gpio.cleanup()  



