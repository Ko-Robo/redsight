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

sys.path.append(os.pardir + '/require')
from require.mnist import load_mnist
from trainer import Trainer


#### dataset 
(x_train, t_train), (x_test, t_test) = load_mnist(normalize=True, one_hot_label=True)
x_train = np.float32(x_train) 
t_train = np.float32(t_train)

#### neuralnet
class MnistNet (Chain):
  def __init__(self):
    super(MnistNet, self).__init__(
      l1=L.Linear(28*28, 100),
      l2=L.Linear(100, 100),
      l3=L.Linear(100,10),
    )
  def __call__(self, x, y):
    o = self.forward(x)
    return F.mean_squared_error(self.forward(x), y)

  def forward(self, x):
    h1 = F.relu(self.l1(x))
    h2 = F.relu(self.l2(h1))
    h3 = F.relu(self.l3(h2))
    return h3

  def accuracy(self, x, t):
    return classification_accuracy(self, x, t)

#### training

model = MnistNet()
optimizer = optimizers.Adam()

trainer = Trainer(model, optimizer, x_train, t_train, x_test, t_test,
                  iter_num=4000)
trainer.train()
trainer.accuracy_test()

graph.plot_error(trainer)
graph.plot_accuracy(trainer)
graph.plot_w_activation([trainer.model.l1,
                         trainer.model.l2,
                         trainer.model.l3])
