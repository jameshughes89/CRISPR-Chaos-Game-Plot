'''
Author: James Alexander Hughes

Loads up the distance matrices of the chaos plots based on DSSIM. Then does TSNE on the distance matrices (DSSIM matricies)

This script differs from 2-doTSNE.py because we do TSNE on the DSSIM dist matrices. 2-doTSNE does TSNE on the flattened images and uses euclidean distance. 

Fortunately, like MDS, TSNE is implemented in sklearn. 
http://scikit-learn.org/stable/modules/generated/sklearn.manifold.TSNE.html

We save the embedding too at the end. 

MIN 1000
	IMAGE_SIZE
		33 --- Got something interesting, but I suspect it was just doing color, but there was somethign neat (but could also be a consequence of there being more things between 1000-2000)
		51 --- Looked OK, but looser than 67
		67 --- Looked OK, but tighter than 51
		101 --- A little too cloud-ie

'''

import csv
import matplotlib.pylab as plt
import numpy as np
import pickle
import sklearn.manifold


def assignColours(seq):
	'''
	Assigns colours to the sequences based on the lengths. There is probably a nicer way of doing this, but whatever. 

	:param seq: A list (or array) of numbers corresponding to the length of the sequences. 

	:return : A list of colours where they are used to represent different lengths. 
	'''

	cols = []
	for s in seq:
		if s < 5000:
			cols.append('m')
		elif s < 6000:
			cols.append('c')
		elif s < 7000:
			cols.append('b')
		elif s < 8000:
			cols.append('g')
		elif s < 9000:
			cols.append('y')
		else:
			cols.append('r')
	return cols


##############
# PARAMETERS #
##############

IMAGE_SIZE = 67
MIN_SIZE = 4000

DO_EVERY = 1

COMPONENTS = 2
PERPLEXITY = 40
EARLY_EXAGGERATION = 20.0
LEARNING_RATE = 100
N_ITER = 4000
METRIC = 'precomputed'	# we need to set this to precomputed because we're using a DSSIM nxn dissimilarity matrix. If we don't change it, it will try to compute it with euclidean (bad)


########
# LOAD #
########

# Load in the data
print 'Loading Data'
distMat = pickle.load(open('/home/james/Desktop/CRISPR_PKL/DSSIM_' + str(IMAGE_SIZE) + '_' + str(MIN_SIZE) + '.pkl','r'))

# Load up the lengths of the sequences here. 
seqLens = np.array(list(csv.reader(open('/home/james/Desktop/CRISPR_PKL/seqLengths_' + str(MIN_SIZE) + '.csv','r')))).astype(float)
colours = assignColours(seqLens)


###########
# DO MDS #
###########

# Creating the TSNE object
print 'Doing 2D TSNE (This Will Take A While)'
tsne = sklearn.manifold.TSNE(n_components=COMPONENTS, early_exaggeration=EARLY_EXAGGERATION, perplexity=PERPLEXITY, metric=METRIC, n_iter=N_ITER, learning_rate=LEARNING_RATE)
embedding = tsne.fit_transform(distMat)

#plt.scatter(embedding)
print 'Plotting Embedding'
plt.scatter(embedding[:,0], embedding[:,1], color=colours)
plt.show()


########
# SAVE #
########

np.savetxt('4-TSNE-embedding_' + str(IMAGE_SIZE) + '_' + str(MIN_SIZE) + '.csv',embedding)


# Try in 3D
'''
from mpl_toolkits.mplot3d import Axes3D

print 'Doing 3D TSNE (This Will Take A While)'
tsne = sklearn.manifold.TSNE(n_components=3, early_exaggeration=EARLY_EXAGGERATION, perplexity=PERPLEXITY, metric=METRIC, n_iter=N_ITER, learning_rate=LEARNING_RATE)
embedding = tsne.fit_transform(distMat)

print 'Plotting 3D Embedding'
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(embedding[:,0], embedding[:,1], embedding[:,2], color=colours)
plt.show()
'''


