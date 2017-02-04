


# item1:value1 item2:value2 item3:value3 ... item-n:value-n
def item_value_str(item_name, value):
  return " "+str(item_name)+":"+str(value)+""

def items_to_string(item_name_list, value_list):
  # [item_name] -> [value] -> String
  str_list = list(map(lambda str, value : item_value_str(str, value),
                      item_name_list , value_list))

  return_str = ""
  for s in str_list:
    return_str = return_str + s 
  return return_str


def parse_string(string):
  # String -> [(item_name, value)]
  item_string_list = string.split(" ")
  while '' in item_string_list: item_string_list.remove('')

  item_list = list(map(lambda item_str : item_str.split(':'),
                       item_string_list))
  item_list[:] = [value for value in item_list if len(value)==2]
  item_list = list(map(lambda item : (item[0], float(item[1])),
                       item_list))
  return item_list
  


### I/O class
class IOItem:
  # IOItem manages sense value and output values from/to each electronical parts.
  # and also used to connunicate internal params of socket 
  def __init__(self):
    
    # io
    # actuator
    self.motor1, self.motor2, self.motor3 = 0,0,0
    self.dribler = 0
    self.kicker = 0

    
    # sensor
    self.sw1, self.sw2, self.sw3 = -1,-1,-1
    self.micro_sw = -1
    self.acc_axis1, self.acc_axis2, self.acc_axis3 = -1,-1,-1 # acceleration
    self.ori_axis1, self.ori_axis2, self.ori_axis3 = -1,-1,-1 # orientation
    self.ang_axis1, self.ang_axis2, self.ang_axis3 = -1,-1,-1 #angular velocity
    self.ir1, self.ir2, self.ir3, self.ir4, self.ir5, self.ir6, self.ir7, self.ir8 =  \
      -1,-1,-1,-1,-1,-1,-1,-1
    self.line1, self.line2, self.line3, self.line4, self.line5, \
      self.line6, self.line7, self.line8, self.line9, self.line10 = \
        -1,-1,-1,-1,-1,-1,-1,-1,-1,-1

    # internal params
    self.robot_mode = 0  # 0:wait-mode, 1:neuralnet-mode
    self.neuralnet_output = [0,0,0,0,0] # motor1, motor2, motor3, dribler, kicker.

    # teaching
    self.save = 0
    self.teach = 0

    self.motor1_teach, self.motor2_teach, self.motor3_teach = 0,0,0
    self.dribler_teach = 0
    self.kicker_teach = 0
    self.teach_data = [0,0,0,0,0] 


  def neuralnet_output(self):
    return [self.motor1, self.motor2, self.motor3, self.dribler, self.kicker]

  def io_name_list (self):
    return [
      # actuator
      "motor1", "motor2", "motor3",
      "dribler",
      "kicker",
      # sensor
      "sw1", "sw2", "sw3",
      "micro_sw",
      "acc_axis1", "acc_axis2", "acc_axis3", 
      "ori_axis1", "ori_axis2", "ori_axis3", 
      "ang_axis1", "ang_axis2", "ang_axis3", 
      "ir1", "ir2", "ir3", "ir4", 
      "ir5", "ir6", "ir7", "ir8",
      "line1", "line2", "line3", "line4", "line5",
      "line6", "line7", "line8", "line9", "line10",
      # other
      "robot_mode",
      "save",
      "teach",
      "motor1_teach", "motor2_teach", "motor3_teach",
      "dribler_teach", "kicker_teach"]
  
  
  def io_value_list(self):
    return [
      # actuator
      self.motor1, self.motor2, self.motor3,
      self.dribler,
      self.kicker,
      # sensor
      self.sw1, self.sw2, self.sw3,
      self.micro_sw,
      self.acc_axis1, self.acc_axis2, self.acc_axis3,
      self.ori_axis1, self.ori_axis2, self.ori_axis3,
      self.ang_axis1, self.ang_axis2, self.ang_axis3,
      self.ir1, self.ir2, self.ir3, self.ir4, 
      self.ir5, self.ir6, self.ir7, self.ir8,
      self.line1, self.line2, self.line3, self.line4, self.line5,
      self.line6, self.line7, self.line8, self.line9, self.line10,
      # other
      self.robot_mode,
      self.save,
      self.teach ,
      self.motor1_teach, self.motor2_teach, self.motor3_teach,
      self.dribler_teach,
      self.kicker_teach
    ]
  

    
  def make_io_string (self):
    return items_to_string(self.io_name_list(), self.io_value_list())

  def make_item_string_list(self):
    str_list = list(map(lambda str, value : item_value_str(str, value),
                        self.io_name_list() , self.io_value_list()))
    return str_list
    

  def update_item (self, item_name, item_value):

    # io
    if False : pass
    
    # actuator
    elif item_name == "motor1" :self.motor1 = item_value
    elif item_name == "motor2" :self.motor2 = item_value
    elif item_name == "motor3" :self.motor3 = item_value

    elif item_name == "dribler" :self.dribler = item_value
    elif item_name == "kicker" :self.kicker = item_value
    
    # sensor
    elif item_name == "sw1" :self.sw1 = item_value
    elif item_name == "sw2" :self.sw2 = item_value
    elif item_name == "sw3" :self.sw3 = item_value
    elif item_name == "micro_sw" :self.micro_sw = item_value
    
    elif item_name == "acc_axis1" :self.acc_axis1 = item_value
    elif item_name == "acc_axis2" :self.acc_axis2 = item_value
    elif item_name == "acc_axis3" :self.acc_axis3 = item_value

    elif item_name == "ori_axis1" :self.ori_axis1 = item_value
    elif item_name == "ori_axis2" :self.ori_axis2 = item_value
    elif item_name == "ori_axis3" :self.ori_axis3 = item_value
    
    elif item_name == "ang_axis1" :self.ang_axis1 = item_value
    elif item_name == "ang_axis2" :self.ang_axis2 = item_value
    elif item_name == "ang_axis3" :self.ang_axis3 = item_value
    
    elif item_name == "ir1" : self.ir1 = item_value
    elif item_name == "ir2" : self.ir2 = item_value
    elif item_name == "ir3" : self.ir3 = item_value
    elif item_name == "ir4" : self.ir4 = item_value
    elif item_name == "ir5" : self.ir5 = item_value
    elif item_name == "ir6" : self.ir6 = item_value
    elif item_name == "ir7" : self.ir7 = item_value
    elif item_name == "ir8" : self.ir8 = item_value

    elif item_name == "line1" : self.line1 = item_value
    elif item_name == "line2" : self.line2 = item_value
    elif item_name == "line3" : self.line3 = item_value
    elif item_name == "line4" : self.line4 = item_value
    elif item_name == "line5" : self.line5 = item_value
    elif item_name == "line6" : self.line6 = item_value
    elif item_name == "line7" : self.line7 = item_value
    elif item_name == "line8" : self.line8 = item_value
    elif item_name == "line9" : self.line9 = item_value
    elif item_name == "line10" : self.line10 = item_value
    
    # other
    elif item_name == "robot_mode" : self.robot_mode = item_value
    elif item_name == "teach" : self.teach = item_value
    elif item_name == "save" : self.save = item_value
    elif item_name == "motor1_teach" : self.motor1_teach = item_value
    elif item_name == "motor2_teach" : self.motor2_teach = item_value
    elif item_name == "motor3_teach" : self.motor3_teach = item_value
    elif item_name == "dribler_teach" : self.dribler_teach = item_value
    elif item_name == "kicker_teach" : self.kicker_teach = item_value

    else :
      print(item_name ," is not contained in IOItem -> item_name" )
      
      

    

if __name__=="__main__":    
  io_item = IOItem()
  print(io_item.make_io_string())
  io_item.update_item("ir1", 1)

  print(io_item.make_io_string())
