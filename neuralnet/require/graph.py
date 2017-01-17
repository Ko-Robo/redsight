import numpy as np
import matplotlib.pyplot as plt
from trainer import Trainer

def plot_error(trainer):
  plt.plot(trainer.train_loss_list)
  plt.show()

def plot_accuracy(trainer):
  plt.plot(trainer.train_acc_list)
  plt.plot(trainer.test_acc_list)
  plt.show()

def plot_activation(trainer):
  item_no = 0
  for key, w in trainer.network.params.items():
    item_no += 1
    plt.subplot(1, len(trainer.network.params), item_no)
    plt.title(key)
    plt.hist(w.flatten(), 30)
  plt.show()


def show_filter(filters, nx=8, margin=3, scale=10):
  FN, C, FH, FW = filters.shape
  ny = int(np.ceil(FN / nx))
  
  fig = plt.figure()
  fig.subplots_adjust(left=0, right=1, bottom=0, top=1, hspace=0.05, wspace=0.05)
  
  for i in range(FN):
    ax = fig.add_subplot(ny, nx, i+1, xticks=[], yticks=[])
    ax.imshow(filters[i, 0], cmap=plt.cm.gray_r, interpolation='nearest')
  plt.show()
  
