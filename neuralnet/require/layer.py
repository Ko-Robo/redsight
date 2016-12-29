
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
    self.x = np.zeros(self.input_size)
    
    self.w_grad = np.zeros_like(self.w)
    self.b_grad = np.zeros_like(self.b)
    self.error = np.zeros_like(self.y)

    self.loss_func = activ_func
    self.d_loss_func = d_active_func
    
  def layer_output (self, input_vec):
    self.x = input_vec
    self.a =  np.dot (self.x, self.w) + self.b
    self.y = self.f(self.a)

    return self.y
    
  def backprop_error(self, error, next_weight):
    # error : error of next layer
    # next weight : weight of next layer
    # returns : error of the function
    # d_Error : d_a
    # ref : https://github.com/tiny-dnn/tiny-dnn/wiki/%E5%AE%9F%E8%A3%85%E3%83%8E%E3%83%BC%E3%83%88
    self.error = self.df(np.dot(error, next_weight.T))
    return self.error

  def backprop(self, error, next_weight):
    self.error = self.backprop_error(error, next_weight)
    self.w_grad = np.dot(self.x.T, self.error)
    return self
    
  ### util
  def input_sample(self):
    return (np.random.rand(self.input_size) -0.5) *0.1




def numerical_gradient_1d(f, x):
  h = 1e-4 # 0.0001
  grad = np.zeros_like(x)

  for idx in range(x.size):
    tmp_val = x[idx]
    # f(x + dh)
    x[idx] = tmp_val + h
    fxh1 = f(x)
    # f(x -h)
    x[idx] = tmp_val -h
    fxh2 = f(x)
    grad[idx] = (fxh1 - fxh2) / (2*h)

  return grad

def numerical_gradient(f, X):
  if X.ndim == 1:
    return numerical_gradient_1d(f, X)

  else:
    grad = np.zeros_like(X)
    for idx, x in enumerate(X):
      grad[idx] = numerical_gradient(f, x)
    return grad
    
class NeuralNet:
  
# layer_data_list : list of each layer's input size, outout size, activ_funcs and d/dx_funcs.
  #<ex> [(28*28,50,relu,relu_ddx), (50,100,relu,relu_ddx),(100,10,relu, relu_ddx)]
  
  def __init__ (self, layer_data_list, loss_func=None):
    self.layer_data_list = layer_data_list
    self.labels = {}
    self.output_vec = []

    self.id_layer = Layer(self.layer_data_list[-1][1], self.layer_data_list[-1][1],
                          idfunc, idfunc_ddx)
    self.id_layer.w = np.matrix(np.identity (self.layer_data_list[-1][1]))
    self.id_layer.b = np.zeros_like(self.layer_data_list[-1][1])
    
    self.layer_list = \
      list(map(lambda data:Layer(data[0], data[1], data[2], data[3]),
               self.layer_data_list)) 
    
    self.loss_func = loss_func
    
    
  def forward (self, input_vec):
    
    self.output_vec = functools.reduce(lambda in_v, layer : layer.layer_output(in_v),
                                       self.layer_list, input_vec)
    
    return self.output_vec
        
  def loss(self, input_vec, teach_vec):
    output_vec = self.forward(input_vec)

    return self.loss_func(output_vec, teach_vec)

  def numerical_gradient(self, input_vec, teach_vec):
    # gradient whithout backward propagation
    loss_W = lambda W: self.loss(input_vec, teach_vec)
    for layer in (self.layer_list):
      layer.w_grad = numerical_gradient(loss_W, layer.w)
      layer.b_grad = numerical_gradient(loss_W, layer.b)

  def gradient (self, input_vec, teach_vec) :
    #backprop(self, error, next_weight):
    #self.layer_list[-1].error = self.loss(input_vec, teach_vec) #* self.layer_list[-1].y
    
    self.id_layer.y = self.loss(input_vec, teach_vec) * np.ones_like(self.id_layer)
    functools.reduce (lambda back_layer, front_layer : \
                      front_layer.backprop(front_layer.error, front_layer.w),
                      self.layer_list, self.id_layer)
  
  def training (self, input_vec, teach_vec, lr=0.01):
    self.numerical_gradient(input_vec, teach_vec)
    for layer in (self.layer_list):
      layer.w = layer.w - lr*layer.w_grad
      layer.b = layer.b - lr*layer.b_grad


      
### test
from functions import *

sample_in = np.random.rand(28*28)
sample_teach = np.random.rand(10)
nn1 = NeuralNet([(28*28, 50,  relu, relu_ddx),
                 (50,    100, idfunc, relu_ddx),
                 (100,   10,  idfunc, relu_ddx)])
nn1.loss_func = cross_entropy_error  


print(sample_teach)
print(softmax(sample_teach))




def layer_test () :
  l1 = Layer(5, 3, relu, relu_ddx)
  print(l1.input_sample())
  print(l1.w)
  print(l1.b)
  print(layer_a_vals(sample_in, l1.w, l1.b))
  l1.layer_output(sample_in)
#layer_test()

def net_test () :
  nn1.forward(sample_in)
  #nn1.training(sample_in, sample_teach)
  #grad2 = nn1.numerical_gradient(sample_in, sample_teach)
  grad2 = nn1.gradient(sample_in, sample_teach)
  return nn1
net_test()

import mnist as mnist
def mnist_test():
  (x_train, t_train), (x_test, t_test) = mnist.load_mnist(normalize=True,
                                                          one_hot_label=True)
  train_size = x_train.shape[0]
  iters_num = 1
  loss_list = []
  
  for i in range(iters_num):
    mask = np.random.choice(train_size, 1)
    x = x_train[mask]
    t = t_train[mask]

    nn1.training(x, t)
    loss = nn1.loss(x, t)
    loss_list.append(loss)

  print(loss_list)
#mnist_test()

  
from line_profiler import LineProfiler
def profile(call_func, test_funcs):
  prf = LineProfiler()
  for func in test_funcs:
    prf.add_function(func)
  prf.runcall(call_func)
  prf.print_stats()
#profile(mnist_test, [numerical_gradient, numerical_gradient_1d])

  

