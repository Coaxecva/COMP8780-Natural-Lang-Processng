import numpy as np
import scipy.linalg as SL
import matplotlib.pyplot as plt

#Pxx = np.genfromtxt('mBtasJLD.txt')

Pxx = np.array([[1, 1, 1, 0, 0], 
				[3, 3, 3, 0, 0], 
				[4, 4, 4, 0, 0],
				[5, 5, 5, 0, 0],
				[0, 2, 0, 4, 4],
				[0, 0, 0, 5, 5],
				[0, 1, 0, 2, 2]])

U, s, Vh = SL.svd(Pxx, full_matrices=False, lapack_driver='gesvd')

assert np.allclose(Pxx, np.dot(U, np.dot(np.diag(s), Vh)))

print(U)
print(s)
print(Vh)

s[2:] = 0
new_a = np.dot(U, np.dot(np.diag(s), Vh))
print(new_a)
print(np.dot([4, 0, 0, 0, 0], np.dot(np.diag(s), Vh)))
plt.plot(new_a)
plt.show()