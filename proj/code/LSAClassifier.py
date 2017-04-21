from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer

from sklearn.random_projection import sparse_random_matrix

import numpy as np

n_components = 10

svd = TruncatedSVD(n_components)
normalizer = Normalizer(copy=False)
lsa = make_pipeline(svd, normalizer)

X = sparse_random_matrix(20, 20, density=0.01, random_state=42)

print(X)

for i in range(20):
	for j in range(20):
		print(X[i][j], " ", end="")
	print()

X_train_lsa = lsa.fit_transform(X)

print(X_train_lsa)
for i in range(10):
	for j in range(10):
		print(X_train_lsa[i][j], " ", end="")
	print()