import sys, os
sys.path.append(os.pardir)

import numpy as np
import chainer
from chainer import cuda, Function, gradient_check, \
  Variable, optimizers, serializers, utils
from chainer import Link, Chain, ChainList
import chainer.functions as F
import chainer.links as L

from util import classification_accuracy
import graph as graph

from trainer import Trainer
sys.path.append(os.pardir + '/require')
from require.mnist import load_mnist



#### dataset 
(x_train, t_train), (x_test, t_test) = load_mnist(normalize=True, one_hot_label=True, flatten=False)
x_train = np.float32(x_train) 
t_train = np.float32(t_train)

x_test = np.float32(x_test)
t_test = np.float32(t_test)


#### neuralnet
class CNN (Chain):
  def __init__(self):
    super(CNN, self).__init__(
      conv1 = L.Convolution2D(1, 32, 5),
      #conv2 = L.Convolution2D(32, 10, 5),
      l1 = L.Linear(4608, 100),
      l2 = L.Linear(100, 10),
    )
    self.train = True
    
  def __call__(self, x, t):
    y = self.forward(x)
    e = F.mean_squared_error(y, t)
    #e = F.softmax_cross_entropy(y, t)
    return e

  def forward(self, x):
    #h = F.max_pooling_2d(F.relu(self.conv1(x)), 3)
    h = F.max_pooling_2d(F.local_response_normalization(
      (F.relu(self.conv1(x)))), 2)
    h = F.relu(self.l1(h))
    h = self.l2(h)
    return h

  def accuracy(self, x, t):
    return classification_accuracy(self, x, t)

#### training

model = CNN()
#optimizer = optimizers.Adam()
optimizer = optimizers.MomentumSGD(lr=0.5)

trainer = Trainer(model, optimizer, x_train, t_train, x_test, t_test,
                  iter_num=1000, epoch_num=10, mini_batch_size=100)


graph.show_filter(trainer.model.conv1.W.data)
#graph.show_filter(trainer.model.conv2.W.data)


trainer.train()
trainer.accuracy_test()

graph.plot_error(trainer)
graph.plot_accuracy(trainer)


graph.plot_w_activation([trainer.model.l1,
                         trainer.model.conv1])
                         #trainer.model.conv2])

graph.show_filter(trainer.model.conv1.W.data)
#graph.show_filter(trainer.model.conv2.W.data)
