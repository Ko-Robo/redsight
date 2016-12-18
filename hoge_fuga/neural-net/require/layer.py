
import numpy as np
from functions import *


### abbreviations 
# w : weight (np.array 2d)
# x : activity-value-of-previous-layer (np.array 1d)
# b : bias (np.array 1d)
# f : activation function (func)
# df : d/dx activation func (func)
# y : activity value of this layer, which is sent in to next layer
# 

class Layer:
  
  def __init__ (self,  input_size, output_size, activ_func, d_active_func):
    
    self.input_size = input_size
    self.output_size = output_size
    
    self.w = (np.random.rand(self.input_size, self.output_size) -0.5) * 0.1
    self.b = (np.random.rand(self.output_size) - 0.5) *0.2
    self.f = activ_func
    self.df = d_active_func
    self.y = np.zeros(self.output_size)

    

  def layer_output (self, x):
    self.y = layer_output(self.f, x, self.w, self.b)
    return self.y

  
  ### util
  def input_sample(self):
    return (np.random.rand(self.input_size) -0.5) *0.1
      
def layer_output (func, x, weight, bias):
  a = np.dot (x, weight) + bias
  return func(a)
  

### test
sample_in = np.array([0.1, 0.2, 0.3, 0.4, 0.5])

l1 = Layer(5, 3, relu, relu_ddx)
print(l1.input_sample())
print(l1.w)
print(l1.b)

print(layer_output(relu, sample_in, l1.w, l1.b))
print(l1.layer_output(sample_in))
