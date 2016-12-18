# this file manages some constant value for neural net
# ,such as path to dataset directory .

import os


# dataset directories

config_dir =  os.path.dirname(os.path.abspath( __file__ ) ) + "/"
dataset_dir = config_dir + "../../dataset"
mnist_dir = dataset_dir + "/mnist"


# test
'''
def ls_test(path):
  for file in (os.listdir(path)):
    print(file)


print(config_dir)

# code to test
"""
from config import *

print(config_dir)
ls_test(dataset_dir)
"""
'''
