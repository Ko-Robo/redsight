import sys, os
sys.path.append(os.pardir)
import numpy as np
import layer  as layer
import optimize as opt

'''
Structure of this network

input -> (Affine -> batch norm -> relu) * n -> softmax


'''
  
class ActiceLayer(layer.Relu) :
  pass
    
class AffineLayer(layer.Affine) :
  pass

class BatchNormLayer(layer.BatchNormalization):
  pass

class DropoutLayer(layer.Dropout):
  pass


class NLayerNet:
  def __init__(self, size_list, grad_update_func=opt.SGD):
    # weights 
    self.layer_no_list = list(range(len(size_list)-1))
    self.layer_size_list = size_list
    
    self.w_params = {}
    self.b_params = {}
    for i in self.layer_no_list:
      self.w_params[i] = np.random.randn(size_list[i], size_list[i+1]) \
                                * np.sqrt(2/size_list[i])
      self.b_params[i] = np.zeros(size_list[i+1])
    
    #layers 
    self.affine_layers = {}
    self.dropout_layers = {}
    self.active_layers = {}

    
    for i in self.layer_no_list:
      self.affine_layers[i] = AffineLayer(self.w_params[i], self.b_params[i])
      self.dropout_layers[i] = DropoutLayer()
      self.active_layers[i] = ActiceLayer()

    # for batch_norm
    self.batch_norm_layers = {}
    self.gamma = {}
    self.beta = {}

    for i in self.layer_no_list[:]:
      self.gamma[i] = np.ones(self.layer_size_list[i+1])
      self.beta[i] = np.zeros(self.layer_size_list[i+1])
      self.batch_norm_layers[i] = BatchNormLayer(self.gamma[i], self.beta[i])
      
    
    self.lastLayer = layer.SoftmaxWithLoss()

    # update weights
    self.set_grad_update_func(grad_update_func)



  def set_grad_update_func(self, func):
    self.w_grad_update_func = func()
    self.b_grad_update_func = func()
    
  def predict(self, x):
    for i in self.layer_no_list:
      x = self.dropout_layers[i].forward(x)
      x = self.affine_layers[i].forward(x)
      #x = self.batch_norm_layers[i].forward(x)
      x = self.active_layers[i].forward(x)
    return x

  def loss(self, x, t):
    y = self.predict(x)
    return self.lastLayer.forward(y, t)

  def accuracy(self, x, t):
    y = self.predict(x)
    y = np.argmax(y, axis = 1)
    if t.ndim !=1 : t = np.argmax(t, axis=1)

    accuracy = np.sum(y==t) / float(x.shape[0])
    return accuracy

  def gradient(self, x,t):
    self.loss(x, t)
    dout = 1
    dout = self.lastLayer.backward(dout)

    rev_layer_no_list = self.layer_no_list[:]
    rev_layer_no_list.reverse()
    for i in rev_layer_no_list:
      dout = self.active_layers[i].backward(dout)
      #dout = self.batch_norm_layers[i].backward(dout)
      dout = self.affine_layers[i].backward(dout)
      dout = self.dropout_layers[i].backward(dout)

    w_grads = {}
    b_grads = {}
    for i in self.layer_no_list:
      w_grads[i] = self.affine_layers[i].dW
      b_grads[i] = self.affine_layers[i].db
    
    return w_grads, b_grads

  def training(self, x, t, lr=0.1):
    w_grads, b_grads = self.gradient(x, t)

    self.w_grad_update_func.update(self.w_params, w_grads)
    self.b_grad_update_func.update(self.b_params, b_grads)

    for i in self.layer_no_list:
      self.gamma[i] = self.batch_norm_layers[i].dgamma
      self.beta[i] = self.batch_norm_layers[i].dbeta
      pass
    

from mnist import load_mnist
import matplotlib.pyplot as plt 

def n_layer_test () :
  ### setup data
  (x_train, t_train), (x_test, t_test) = load_mnist(normalize=True, one_hot_label=True)

  x_train = x_train[:300]
  t_train = t_train[:300]
  
  network = NLayerNet([28*28, 50,50, 50, 50, 50, 50, 50, 10])
  #network = NLayerNet([28*28, 100, 100, 100, 100, 100,100, 100, 10])
  network.set_grad_update_func(opt.Momentum)

  iters_num = 1500
  train_size = x_train.shape[0]
  batch_size = 100
  
  train_loss_list = []
  train_acc_list = []
  test_acc_list = []
  iter_par_epoch = 100 # max(train_size / batch_size, 1)

  ### rearning and memo_result
  for i in range(iters_num):
    batch_mask = np.random.choice(train_size, batch_size)
    x_batch = x_train[batch_mask]
    t_batch = t_train[batch_mask]

    network.training(x_batch, t_batch)

     
    loss = network.loss(x_batch, t_batch)
    train_loss_list.append(loss)
    
    if i % iter_par_epoch == 0 :
      train_acc = network.accuracy(x_train, t_train)
      test_acc = network.accuracy(x_test, t_test)
      train_acc_list.append(train_acc)
      test_acc_list.append(test_acc)
      print("train acc, test acc | " + str(train_acc) + ", " + str(test_acc))


  ### figures
  # error
  plt.plot(train_loss_list)
  plt.show()

  # accuracy
  plt.plot(train_acc_list)
  plt.plot(test_acc_list)
  plt.show()

  #activation
  item_no = 0
  for key,w in network.w_params.items():
    item_no += 1
    plt.subplot(1, len(network.w_params), item_no)
    plt.title(key)
    plt.hist(w.flatten(), 30)
  plt.show()

  item_no = 0
  for key,b in network.b_params.items():
    item_no += 1
    plt.subplot(1, len(network.b_params), item_no)
    plt.title(key)
    plt.hist(b.flatten(), 30)
  plt.show()
  
n_layer_test()  

