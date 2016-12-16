import numpy as np

### activation function
def indentity_function(x):
  return x

def step_function(x):
  return np.array(x > 0, dtype = np.int)

def sigmoid(x):
  return 1 / (1 + np.exp(-x))

def relu (x):
  return np.maximum(0,x)

### output layer
def softmax(a):
  c = np.max(a)
  exp_a = np.exp(a-c)
  sum_exp_a = np.sum(exp_a)
  y = exp_a / sum_exp_a
  return y

### d/dx
def sigmoid_ddx(y):
  return y*(1-y)

def relu_ddx(y):
  return 1 * (y >= 0)
  

### error
def mean_squared_error(y, t):
  return 0.5*np.sum((y-t) ** 2)

def cross_entropy_error(y,t):
  if y.ndim == 1:
    t = t.reshape(1, t.size)
    y = y.reshape(1, y.size)
    
  if t.size == y.size:
    t = t.argmax(axis=1)

  batch_size = y.shape[0]
  return -np.sum(np.log(y[np.arange(batch_size), t])) / batch_size

### loss
def softmax_loss(x, t):
  y = softmax(x)
  return cross_entropy_error(y, t)



### test

import matplotlib.pylab as plt

x = np.arange(-5.0, 5.0, 0.1)
y = []

#y.append(indentity_function(x))
#y.append(step_function(x))
#y.append(sigmoid(x))
#y.append(relu(x))

#y.append(softmax(x))  # should x to be more random

#y.append(sigmoid_ddx(x))
#y.append(relu_ddx(x))

#plt.ylim(-1.1, 1.1)
for i in range(len(y)) :
  print (y[i])
  plt.plot(x,y[i])

plt.show()
