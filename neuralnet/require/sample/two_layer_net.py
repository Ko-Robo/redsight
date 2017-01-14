import sys, os
sys.path.append(os.pardir)
from layer import *
import optimize as opt
from collections import OrderedDict
    

class TwoLayernet:
  def __init__(self, input_size, hidden_size, output_size):
    self.params = {}
    self.params['W1'] = np.random.randn(input_size, hidden_size) * np.sqrt(2/input_size)
    self.params['b1'] = np.zeros(hidden_size)
    self.params['W2'] = np.random.randn(hidden_size, output_size)* np.sqrt(2/hidden_size)
    self.params['b2'] = np.zeros(output_size)

    self.layers = OrderedDict()
    self.layers['Affine1'] = Affine(self.params['W1'], self.params['b1'])
    self.layers['Relu1'] = Relu()
    self.layers['Affine2'] = Affine(self.params['W2'], self.params['b2'])
    self.lastLayer = SoftmaxWithLoss()

  def predict(self, x):
    for layer in self.layers.values():
      x = layer.forward(x)
    return x

  def loss(self, x, t):
    y = self.predict(x)
    
    return self.lastLayer.forward(y, t)

  def accuracy(self, x,t):
    y = self.predict(x)
    y = np.argmax(y, axis = 1)
    if t.ndim != 1 : t = np.argmax(t, axis=1)

    accuracy = np.sum(y == t) / float(x.shape[0])
    return accuracy

  def gradient(self, x, t):
    self.loss(x, t)
    
    dout = 1
    dout = self.lastLayer.backward(dout)

    layers = list(self.layers.values())
    layers.reverse()
    for layer in layers:
      dout = layer.backward(dout)

    grads = {}
    grads['W1'] = self.layers['Affine1'].dW
    grads['b1'] = self.layers['Affine1'].db
    grads['W2'] = self.layers['Affine2'].dW
    grads['b2'] = self.layers['Affine2'].db
    
    return grads

    
# training test

from mnist import load_mnist
from trainer import Trainer
import graph as graph


(x_train, t_train), (x_test, t_test) = load_mnist(normalize=True, one_hot_label=True)

network = TwoLayernet(input_size=784, hidden_size=50, output_size=10)
#trainer = Trainer(network, x_train, t_train, x_test, t_test)
trainer = Trainer(network, x_train, t_train, x_test, t_test,
                  optimizer='momentum', optimizer_param={'lr':0.01,'momentum':0.9})

trainer.train()

graph.plot_error(trainer)
graph.plot_accuracy(trainer)
graph.plot_activation(trainer)
