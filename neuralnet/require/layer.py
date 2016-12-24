
import numpy as np
import functools

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
    self.a = self.y


  def layer_output (self, x):
    self.a = layer_a_vals(x, self.w, self.b)
    self.y = layer_output(self.f, self.a)
    return self.y

  
  ### util
  def input_sample(self):
    return (np.random.rand(self.input_size) -0.5) *0.1

    
def layer_a_vals (x, weight, bias):
  # a[n]= (sigma weight[n] * x[n]) + b[n]
  return np.dot (x, weight) + bias

def layer_output(func, sums):
  # y[n] = activation_function(a[n])
  return func(sums)


class NeuralNet:
  # layer_data_list : list of each layer's input size, outout size, activ_funcs and d/dx_funcs.
  #<ex> [(28*28,50,relu,relu_ddx), (50,100,relu,relu_ddx),(100,10,softmax,softmax_loss)]
  
  def __init__ (self, layer_data_list):
    self.layer_data_list = layer_data_list
    self.layer_length = len(self.layer_data_list)
    self.labels = {}
    self.output_vec = []
    
    self.layer_list = \
      list(map(lambda data:Layer(data[0], data[1], data[2], data[3]),
               self.layer_data_list))
    
      
  def forward (self, input_vec):
    self.output_vec = functools.reduce(lambda in_v, layer : layer.layer_output(in_v),
                                self.layer_list, input_vec)
    return self.output_vec
    
  def back_forward (self):
    return 1
    
  
### test
from functions import *
#import mnist


sample_in = np.random.rand(28*28)
#sample_in np.array([0.1, 0.2, 0.3, 0.4, 0.5])

nn1 = NeuralNet([(28*28, 50,  relu, relu_ddx),
                 (50,    100, relu, relu_ddx),
                 (100,   10,  softmax, softmax_loss)])

print(nn1.layer_list[1].w[0][0:5])
print(nn1.forward(sample_in))
print(nn1.layer_list[1].w[0][0:5])



def layer_test () :
  l1 = Layer(5, 3, relu, relu_ddx)
  print(l1.input_sample())
  print(l1.w)
  print(l1.b)

  print(layer_a_vals(sample_in, l1.w, l1.b))
  print(l1.layer_output(sample_in))



#layer_test()   
