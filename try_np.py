import numpy as np

# ONEHOT = np.zeros(5)
# print ONEHOT

# ONEHOT = np.zeros((5,3,2))
# print ONEHOT

# ONEHOT = np.zeros((5,3))
# print ONEHOT

# ONEHOT = np.ones((5,3,2))
# print ONEHOT

x = np.arange(6)
x = x.reshape((2, 3))
print x

x = np.arange(6)
x = x.reshape(2, 3)
print x

print np.zeros_like(x)
print np.empty_like(x)

y = np.arange(3, dtype=float)
print y