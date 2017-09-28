'''

Loads up the already created chaos plots and performs TSNE.

NOTES:
- Lila used Structural Similarity Index (or, dissimiliarity) --- DSSIM (available in skimage)
- Lila also used Multi-Dimensional Scaling (MDS) for mapping to a space. (available in sklean manifold)


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
		if s < 2000:
			cols.append('m')
		elif s < 3000:
			cols.append('c')
		elif s < 4000:
			cols.append('b')
		elif s < 5000:
			cols.append('g')
		elif s < 6000:
			cols.append('y')
		else:
			cols.append('r')
	return cols


##############
# PARAMETERS #
##############

IMAGE_SIZE = 101
MIN_SIZE = 1000

DO_EVERY = 1

COMPONENTS = 2
PERPLEXITY = 30
EARLY_EXAGGERATION = 20.0
LEARNING_RATE = 100
METRIC = 'euclidean'
#METRIC = 'mahalanobis'
N_ITER = 2000

########
# LOAD #
########

# Load in the data as a numpy array and flatten it. Flattening  
# is needed because otherwise we get a list of lists of size 1
print 'Loading Data'
cps = pickle.load(open('/home/james/Desktop/CRISPR_PKL/chaosPlots_' + str(IMAGE_SIZE) + '_' + str(MIN_SIZE) + '.pkl','r'))

# Load up the lengths of the sequences here. 
seqLens = np.array(list(csv.reader(open('/home/james/Desktop/CRISPR_PKL/seqLengths_' + str(MIN_SIZE) + '.csv','r')))).astype(float)
colours = assignColours(seqLens)

# flatten each matrix (DO NOT DO THIS IF USING A DISTANCE FUNCTION FOR 2D MATRICES
# I have it set so that we can do every DO_EVERY-th sequence (to speed things up)
print 'Flattening Data'
cpsFlat = [cp.flatten() for cp in cps[::DO_EVERY]]

###########
# DO TSNE #
###########

# Creating the TSNE object
print 'Doing TSNE (This Will Take A While)'
tsne = sklearn.manifold.TSNE(n_components=COMPONENTS, early_exaggeration=EARLY_EXAGGERATION, perplexity=PERPLEXITY, metric=METRIC, n_iter=N_ITER)
embedding = tsne.fit_transform(cpsFlat)

#plt.scatter(embedding)
print 'Plotting Embedding'
plt.scatter(embedding[:,0], embedding[:,1], color=colours)
plt.show()


# Save the embedding
np.savetxt('embedding_' + str(IMAGE_SIZE) + '_' + str(MIN_SIZE) + 'csv',embedding)

'''
# Try in 3D

from mpl_toolkits.mplot3d import Axes3D

print 'Doing TSNE in 3D (This Will Also Take A While)'
tsne = sklearn.manifold.TSNE(n_components=3, perplexity=PERPLEXITY, metric=METRIC, n_iter=N_ITER)
embedding = tsne.fit_transform(cpsFlat)

print 'Plotting 3D Embedding'
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(embedding[:,0], embedding[:,1], embedding[:,2], color=colours)
plt.show()
'''




