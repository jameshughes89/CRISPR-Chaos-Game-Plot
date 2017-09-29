'''
Author: James Alexander Hughes

Loads up the already created chaos plots and calculated the Structural Dissimilarity Index (DSSIM)

DDSIM(x,y) = (1 - SSIM(x,y))/2

Lila's process used DSSIM instead of TSNE. So let's see what happens. 


'''

import csv
import matplotlib.pylab as plt
import numpy as np
import pickle
import scipy
import skimage.measure
import sklearn.manifold


def DSSIM(x, y):
	'''
	Calculates the Structural Dissimilarity Index (DSSIM) between two images (numpy array)

	****WARNING:
	********THIS SCRIPT WORKS BY RESHAPING THE IMAGES TO WHATEVER *IMAGE_SIZE* IS SET TO
	********THIS WAS A HACK TO MAKE pdist WORK. 

	:param x: Image 1 (numpy array)
	:param y: Image 2 (numpy array)

	:return : The DSSIM between the two images 
	'''
	import sklearn.manifold
	SSIM = skimage.measure.compare_ssim(x.reshape(IMAGE_SIZE,IMAGE_SIZE),y.reshape(IMAGE_SIZE,IMAGE_SIZE), data_range=y.max()-y.min())
	DSSIM = (1 - SSIM)/2
	return DSSIM



##############
# PARAMETERS #
##############

IMAGE_SIZE = 33
MIN_SIZE = 1000
DO_EVERY = 1

########
# LOAD #
########

# Load in the data as a numpy array and flatten it. 
print 'Loading Data'
cps = pickle.load(open('/home/james/Desktop/CRISPR_PKL/chaosPlots_' + str(IMAGE_SIZE) + '_' + str(MIN_SIZE) + '.pkl','r'))

# flatten each matrix 
# I HAVE TO DO THIS BECAUSE OF HOW pdist WORKS...
print 'Flattening Data'
cpsFlat = [cp.flatten() for cp in cps[::DO_EVERY]]


############
# DO DSSIM #
############


print 'Calculating the distance matrix'

# NONE OF THIS WILL WORK BECAUSE I HAVE AN n by (m x m) matrix. 
# DSSIM will not work right when flattened images
# Compute the distance matrix (but it will be in an array) based on the DSSIM function above
distMat = scipy.spatial.distance.pdist(cpsFlat, metric=DSSIM)
# Convert the distance *array* to a distance matrix
distMat = scipy.spatial.distance.squareform(distMat)

#distMat = np.zeros((len(cps), len(cps)))
#for i, x in enumerate(cps):
#	if i % 100 == 0:
#		print i
#	for j, y in enumerate(cps):
#		distMat[i,j] = DSSIM(x, y)

###############
# Save DSSIMs #
###############

print 'Saving results'
# Make sure not to save on Dropbox (large files)
pickle.dump(distMat, open('/home/james/Desktop/CRISPR_PKL/DSSIM_' + str(IMAGE_SIZE) + '_' + str(MIN_SIZE) + '.pkl','w'))



