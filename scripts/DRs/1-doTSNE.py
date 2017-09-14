'''

Loads up the already created chaos plots and performs TSNE.

'''

import csv
import matplotlib.pylab as plt
import numpy as np
import pickle
import sklearn.manifold



##############
# PARAMETERS #
##############

COMPONENTS = 2
PERPLEXITY = 30
EARLY_EXAGGERATION = 20.0
LEARNING_RAGE = 100
METRIC = 'euclidean'
#METRIC = 'mahalanobis'

########
# LOAD #
########

# Load in the data as a numpy array and flatten it. Flattening  
# is needed because otherwise we get a list of lists of size 1
cps = pickle.load(open('chaosPlots.pkl','r'))

# flatten each matrix (DO NOT DO THIS IF USING A DISTANCE FUNCTION FOR 2D MATRICES
cpsFlat = [cp.flatten() for cp in cps]

###########
# DO TSNE #
###########

# Creating the TSNE object
tsne = sklearn.manifold.TSNE(n_components=COMPONENTS, early_exaggeration=EARLY_EXAGGERATION, perplexity=PERPLEXITY, metric=METRIC)
embedding = tsne.fit_transform(cpsFlat)

#plt.scatter(embedding)
plt.scatter(embedding[:,0], embedding[:,1])
plt.show()

# Try in 3D
'''
from mpl_toolkits.mplot3d import Axes3D

tsne = sklearn.manifold.TSNE(n_components=3, perplexity=PERPLEXITY, metric=METRIC)
embedding = tsne.fit_transform(cpsFlat)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(embedding[:,0], embedding[:,1], embedding[:,2])
plt.show()
'''


