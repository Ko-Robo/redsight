import numpy as np


def classification_accuracy(model, x, teach):
  y = model.forward(x)
  ans = y.data
  nrow, ncol = ans.shape
  ok = 0
  for i in range(nrow):
    cls = np.argmax(ans[i,:])
    if cls == np.argmax(teach[i]):
      ok +=1
  acc = ok/nrow
  return acc
