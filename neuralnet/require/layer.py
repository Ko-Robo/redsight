
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

  def backprop_output_layer(self, error):
    # error value of output layer
    self.error = (self.y - error)*self.df(self.y)
    self.w_grad = np.dot(np.transpose([self.x]), [self.error])
    return self

  def backprop(self, error, next_weight):
    # error : error of next layer
    # next weight : weight of next layer
    # returns : error of the function
    # d_Error : d_a
    # ref : https://github.com/tiny-dnn/tiny-dnn/wiki/%E5%AE%9F%E8%A3%85%E3%83%8E%E3%83%BC%E3%83%88
    self.error = np.dot(error,next_weight.T)*self.df(self.a)
    #self.df(np.dot(error, next_weight.T))
    self.w_grad = np.dot(np.transpose([self.x]), [self.error])
    print(self.w.shape)
    print(self.w_grad.shape)
    return self
    

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
    self.loss = 0

    self.layer_list = \
      list(map(lambda data:Layer(data[0], data[1], data[2], data[3]),
               self.layer_data_list)) 
    
    self.loss_func = loss_func
    
    
  def forward (self, input_vec):
    self.output_vec = functools.reduce(lambda in_v, layer : layer.layer_output(in_v),
                                       self.layer_list, input_vec)
    return self.output_vec
        
  def get_loss(self, input_vec, teach_vec):
    self.output_vec = self.forward(input_vec)
    self.loss = self.loss_func(self.output_vec, teach_vec)
    return self.loss

  def gradient (self, input_vec, teach_vec) :
    self.get_loss(input_vec, teach_vec)    

    self.layer_list[-1].backprop_output_layer(self.loss)
    

    functools.reduce (lambda back_layer, front_layer : \
                      front_layer.backprop(back_layer.error, back_layer.w),
                      self.layer_list[::-1]) # L[::-1] : reverse of list
    
  def training (self, input_vec, teach_vec, lr=1e-4):
    self.gradient(input_vec, teach_vec)
    for layer in (self.layer_list):
      layer.w = layer.w - lr*layer.w_grad
      
### test
from functions import *
import matplotlib.pylab as plt

sample_in = np.random.rand(28*28)

sample_teach = np.array([0,1,0,0,0,0,0,0,0,0])

nn1 = NeuralNet([(28*28, 50,  relu, relu_ddx),
                 (50,    100, relu, relu_ddx),
                 (100,   10,  relu, relu_ddx)])
nn1.loss_func = mean_squared_error

#print(sample_teach)

def layer_test () :
  l1 = Layer(5, 3, relu, relu_ddx)
  print(l1.input_sample())
  print(l1.w)
  print(l1.b)
  print(layer_a_vals(sample_in, l1.w, l1.b))
  l1.layer_output(sample_in)
#layer_test()

def net_test () :
  #print(nn1.forward(sample_in))

  vec_lis = []
  loss_lis = []
  time = 10
  for i in range(time) :
    nn1.training(sample_in, sample_teach)
    vec_lis.append(nn1.output_vec)
    loss_lis.append(nn1.loss)

  for i in range(time):
    #print(str(loss_lis[i]) + " \t " + str(vec_lis[i]))
    pass
    
  plt.plot(vec_lis)
  plt.show()
  
  plt.plot(loss_lis)
  plt.show()

  return nn1
net_test()

#import mnist as mnist
def mnist_test():
  (x_train, t_train), (x_test, t_test) = mnist.load_mnist(normalize=True,
                                                          one_hot_label=True)
  train_size = x_train.shape[0]
  iters_num = 100
  loss_list = []
  
  for i in range(iters_num):
    mask = np.random.choice(train_size, 1)
    x = x_train[mask]
    t = t_train[mask]
    nn1.training(x, t)
    #loss = nn1.loss(x, t)
    #loss_list.append(loss)

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

  

