import sys, os
sys.path.append(os.pardir)
import numpy as np
from collections import OrderedDict
from layer import *
import optimize as opt


'''
Structure of this network

input -> (conv->relu->pooling)*n -> (affine->relu)*m -> (affine->softmax)

'''


class SimpleCNN:
  def __init__(self, input_dim=(1,28,28),
               conv_parm={'filter_num':30, 'filter_size':5, 'pad':0, 'stride':1},
               hidden_size=50, output_size=10,
               weight_init_std = 0.01):
    
    filter_num = conv_parm['filter_num']
    filter_size = conv_parm['filter_size']
    filter_pad = conv_parm['pad']
    filter_stride = conv_parm['stride']
    input_size = input_dim[1]
    conv_output_size = (input_size - filter_size + 2*filter_pad) / filter_stride + 1
    pool_output_size = int(filter_num * (conv_output_size/2) ** 2)

    # weights
    self.params = {}
    self.params['W1'] = weight_init_std * \
      np.random.randn(filter_num, input_dim[0], filter_size, filter_size)
    self.params['b1'] = np.zeros(filter_num)
    
    self.params['W2'] = weight_init_std * \
      np.random.randn(pool_output_size, hidden_size)
    self.params['b2'] = np.zeros(hidden_size)
    
    self.params['W3'] = weight_init_std * \
      np.random.randn(hidden_size, output_size)
    self.params['b3'] = np.zeros(output_size)

    # layers
    self.layers = OrderedDict()
    self.layers['conv1'] = Convolution(self.params['W1'], self.params['b1'],
                                     conv_parm['stride'], conv_parm['pad'])
    self.layers['relu1'] = Relu()
    self.layers['pool1'] = Pooling(pool_h=2, pool_w=2, stride=2)
    
    self.layers['affine2'] = Affine(self.params['W2'], self.params['b2'])
    self.layers['relu2'] = Relu()

    self.layers['affine3'] = Affine(self.params['W3'], self.params['b3'])
    

    self.last_layer = SoftmaxWithLoss()
    
  def predict(self, x):
    for layer in self.layers.values():
      x = layer.forward(x)
      #print("layer:", layer , " | shape:", x.shape)
    return x
    

  def loss(self, x, t):
    y = self.predict(x)
    return self.last_layer.forward(y, t)

  def accuracy(self, x, t, batch_size=100):
    if t.ndim != 1 : t=np.argmax(t, axis=1)

    acc = 0.0

    for i in range(int(x.shape[0] / batch_size)):
      tx = x[i*batch_size:(i+1)*batch_size]
      tt = t[i*batch_size:(i+1)*batch_size]
      y = self.predict(tx)
      y = np.argmax(y, axis=1)
      acc += np.sum(y==tt)
      
    return acc/x.shape[0]
    

  def gradient(self, x,t):
    self.loss(x, t)

    dout = 1
    dout = self.last_layer.backward(dout)

    layers = list(self.layers.values())
    layers.reverse()
    for layer in layers:
      dout = layer.backward(dout)
    
    grads={}
    grads['W1'], grads['b1'] = self.layers['conv1'].dW, self.layers['conv1'].db
    grads['W2'], grads['b2'] = self.layers['affine2'].dW, self.layers['affine2'].db
    grads['W3'], grads['b3'] = self.layers['affine3'].dW, self.layers['affine3'].db

    return grads
    

from mnist import load_mnist
from trainer import Trainer
import graph as graph

(x_train, t_train), (x_test, t_test) = load_mnist(normalize=True, one_hot_label=True, flatten=False)

x_train , t_train = x_train[:5000], t_train[:5000]
x_test , t_test = x_test[:5000], t_test[:5000]

network = SimpleCNN() 

#trainer = Trainer(network, x_train, t_train, x_test, t_test)
trainer = Trainer(network, x_train, t_train, x_test, t_test,
                  optimizer='momentum', optimizer_param={'lr':0.01,'momentum':0.9},
                  epoches=2)



trainer.train()



graph.plot_error(trainer)
graph.plot_accuracy(trainer)
graph.plot_activation(trainer)
graph.show_filter(trainer.network.params['W1'])

