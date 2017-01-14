import numpy as np
import optimize as opt
import matplotlib.pyplot as plt 

class Trainer:
  def __init__(self, network, x_train, t_train, x_test, t_test,
               epoches=20, mini_batch_size=100,
               optimizer='sgd', optimizer_param={'lr':0.01}):
    self.network = network
    self.x_train = x_train
    self.t_train = t_train
    self.x_test = x_test
    self.t_test = t_test

    self.epoches = epoches
    self.batch_size = mini_batch_size

    optimier_class_dict = {'sgd':opt.SGD, 'momentum':opt.Momentum}
    self.optimizer = optimier_class_dict[optimizer](**optimizer_param)

    self.train_size = x_train.shape[0]
    self.test_size = t_test.shape[0]
    self.iter_par_epoch = max(self.train_size/mini_batch_size, 1)
    self.max_iter = int(epoches*self.iter_par_epoch)
    self.current_iter = 0
    self.current_epoch = 0

    self.train_loss_list = []
    self.train_acc_list = []
    self.test_acc_list = []

  def accuracy_test(self, x_num=500, t_num=500):
    train_batch_mask = np.random.choice(self.train_size, x_num)
    test_batch_mask = np.random.choice(self.test_size, t_num)
    
    train_acc = \
      self.network.accuracy(self.x_train[train_batch_mask], self.t_train[train_batch_mask])
    test_acc = \
      self.network.accuracy(self.x_test[test_batch_mask], self.t_test[test_batch_mask])
    print("train acc, test acc | " + str(train_acc) + ", " + str(test_acc))
    self.train_acc_list.append(train_acc)
    self.test_acc_list.append(test_acc)
    
    
  def train_step(self):
    batch_mask = np.random.choice(self.train_size, self.batch_size)
    x_batch = self.x_train[batch_mask]
    t_batch = self.t_train[batch_mask]

    grads = self.network.gradient(x_batch, t_batch)
    self.optimizer.update(self.network.params, grads)
    
    
    loss = self.network.loss(x_batch, t_batch)
    self.train_loss_list.append(loss)

    if self.current_iter % self.iter_par_epoch == 0:
      self.current_epoch += 1
      self.accuracy_test()
    self.current_iter += 1

  def train(self):
    for i in range(self.max_iter):
      self.train_step()
