
import numpy as np
from functions import *


### abbreviations 
# w : weight (np.array 2d)
# x : activity-value-of-previous-layer (np.array 1d)
# b : bias (np.array 1d)
# f : activation function (func)
# df : d/dx activation func (func)



class Layer:
  
  
  def __init__ (self,  input_size, output_size, activ_func, d_active_func):
    self.input_size = input_size
    self.output_size = output_size
    self.w = (np.random.rand(self.input_size, self.output_size) -0.5) * 0.1
    self.b = (np.random.rand(self.output_size) - 0.5) *0.2
    self.f = activ_func
    self.df = d_active_func
    
  def layer_output (self, x):
    self.a = np.dot (x, self.w) + self.b
    output = self.f(self.a)
    return output
    
    
  ### util


  def input_sample(self):
    return (np.random.rand(self.input_size) -0.5) *0.1
      


### test
sample_in = np.array([0.1, 0.2, 0.3, 0.4, 0.5])

l1 = Layer(5, 3, relu, relu_ddx)
print(l1.input_sample())
print(l1.w)
print(l1.b)

print(l1.layer_output(sample_in))
