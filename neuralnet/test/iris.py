import sys

import numpy as np
import chainer
from chainer import cuda, Function, gradient_check, \
  Variable, optimizers, serializers, utils
from chainer import Link, Chain, ChainList
import chainer.functions as F
import chainer.links as L

from sklearn import datasets

### dataset 
iris = datasets.load_iris()

X = iris.data.astype(np.float32)
Y = iris.target
N = Y.size

Y2 = np.zeros(3*N).reshape(N, 3).astype(np.float32)
for i in range(N):
  Y2[i, Y[i]] = 1.0  

index = np.arange(N)
xtrain = X[index[index%2!=0], :]
ytrain = Y2[index[index%2!=0], :]
xtest = X[index[index%2==0], :]
yans = Y[index[index%2==0]]


#### neuralnet
class IrisChain(Chain):
  def __init__(self):
    super(IrisChain, self).__init__(
      l1 = L.Linear(4, 100),
      l2 = L.Linear(100,3),
      )

  def __call__(self, x,y):
    o = self.forward(x)
    print(o.shape)
    print(y.shape)
    return F.mean_squared_error(o, y)

  def forward(self, x):
    h1 = F.sigmoid(self.l1(x))
    h2 = self.l2(h1)
    h3 = F.softmax(h2)
    return h3

### setup model
n = 75
bs = 25


model = IrisChain()
optimizer = optimizers.SGD()
optimizer.setup(model)

for j in range(1):
  accum_loss = None
  sffindx = np.random.permutation(n)
  for i in range(0, n, bs):
    x = Variable(xtrain[sffindx[i:(i+bs) if (i+bs) < n else n]])
    y = Variable(ytrain[sffindx[i:(i+bs) if (i+bs) < n else n]])
    
    model.zerograds()
    loss = model(x, y)
    accum_loss = loss if accum_loss is None \
                 else accum_loss + loss
    loss.backward()
    optimizer.update()
  
    
xt = Variable(xtest, volatile='on')
yt = model.forward(xt)
ans = yt.data

nrow, ncol = ans.shape
ok = 0
for i in range(nrow):
  cls = np.argmax(ans[i,:])
  if cls == yans[i]:
    ok += 1


print(ok, "/", nrow, " = ", (ok*1.0)/nrow)
