import sys
import numpy as np
#import optimize as opt
import matplotlib.pyplot as plt 
#from util import accuracy

    
class Trainer:
  def __init__(self, model, optimizer, x_train, t_train, x_test, t_test,
               iter_num=1000 ,mini_batch_size=100, epoch_num=20):
    ## defines
    self.model = model
    self.optimizer = optimizer
    self.optimizer.setup(model)
    self.x_train = x_train
    self.t_train = t_train
    self.x_test = x_test
    self.t_test = t_test

    self.iter_num = iter_num
    self.batch_size = mini_batch_size
    self.epoch_num = epoch_num
    self.iter_par_epoch = int(iter_num/epoch_num)

    ## parameters
    self.train_size = t_train.shape[0]
    self.test_size = t_test.shape[0]
    
    self.current_iter = 0
    self.current_epoch = 0
    
    self.train_loss_list = []
    self.train_acc_list = []
    self.test_acc_list = []

    
  def accuracy_test(self, x_num=500, t_num=500):
    train_batch_mask = np.random.choice(self.train_size, x_num)
    test_batch_mask = np.random.choice(self.test_size, t_num)
    
    train_acc = \
      self.model.accuracy(self.x_train[train_batch_mask], self.t_train[train_batch_mask])
    test_acc = \
      self.model.accuracy(self.x_test[test_batch_mask], self.t_test[test_batch_mask])
    
    print("train acc, test acc | " + str(train_acc) + ", " + str(test_acc))
    self.train_acc_list.append(train_acc)
    self.test_acc_list.append(test_acc)

  def train_step(self):
    # train model
    batch_mask = np.random.choice(self.train_size, self.batch_size)
    x_batch = self.x_train[batch_mask]
    t_batch = self.t_train[batch_mask]

    self.model.zerograds()
    loss = self.model(x_batch, t_batch)
    loss.backward()
    self.optimizer.update()

    # test
    loss = self.model(x_batch, t_batch).data
    self.train_loss_list.append(loss)

    if self.current_iter % self.iter_par_epoch == 0 :
      self.current_epoch += 1
      self.accuracy_test()
      
    # update    
    self.current_iter += 1

    

  def train(self):
    for i in range(self.iter_num):
      self.train_step()


