'''
Author: James Alexander Hughes

Loads up the distance matrices of the chaos plots based on DSSIM. Then does multidimensional scaling (MDS). 

Fortunately this MDS is implemented in sklearn. 
http://scikit-learn.org/stable/modules/generated/sklearn.manifold.MDS.html

We save the embedding too at the end. 

****WARNING!
********It seems that this just embeds them based on the length of the sequences. 
********EXCEPT 33 seemed to get something a little better than grouping on size, but really, it was still just grouping on size.


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

IMAGE_SIZE = 67
MIN_SIZE = 2000

DO_EVERY = 1

COMPONENTS = 2
N_JOBS = -1		# a way to make the comp use all processors apparently (sweet!)
METRIC = True	# not sure what this one will do: "If True, perform metric MDS; otherwise, perform nonmetric MDS." <- From http://scikit-learn.org/stable/modules/generated/sklearn.manifold.MDS.html
#METRIC = False
N_INIT = 4
MAX_ITER = 300
DISSIMILARITY = 'precomputed'	# we need to set this to precomputed because we're using a DSSIM nxn dissimilarity matrix. If we don't change it, it will try to compute it with euclidean (bad)


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
print 'Doing 2D MDS (This Will Take A While)'
mds = sklearn.manifold.MDS(n_components=COMPONENTS, n_jobs=N_JOBS, metric=METRIC, n_init=N_INIT, max_iter=MAX_ITER, dissimilarity=DISSIMILARITY)
embedding = mds.fit_transform(distMat)

#plt.scatter(embedding)
print 'Plotting Embedding'
plt.scatter(embedding[:,0], embedding[:,1], color=colours)
plt.show()


########
# SAVE #
########

np.savetxt('3-MDS-embedding_' + str(IMAGE_SIZE) + '_' + str(MIN_SIZE) + '.csv',embedding)


# Try in 3D
'''
from mpl_toolkits.mplot3d import Axes3D

print 'Doing 3D MDS (This Will Take A While)'
mds = sklearn.manifold.MDS(n_components=3, n_jobs=N_JOBS, metric=METRIC, n_init=N_INIT, max_iter=MAX_ITER, dissimilarity=DISSIMILARITY)
embedding = mds.fit_transform(distMat)

print 'Plotting 3D Embedding'
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(embedding[:,0], embedding[:,1], embedding[:,2], color=colours)
plt.show()
'''




