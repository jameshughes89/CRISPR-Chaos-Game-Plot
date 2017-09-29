'''
Author: James Alexander Hughes

Loads the data and produces the chaos game plots for each CRISPR.

###########
# WARNING #
###########

Do not save the pickls to dropbox. I have a feeling they'll be large. 

'''

import csv
import matplotlib.pylab as plt
import numpy as np
import pickle


def chaosGamePlot(seq):
	'''
	Produces the ChaosGamePlot for a given sequence. The plot will be created with just a 2D numpy array.
	Rules:	
	1. Each letter (A, T, G, C) gets a corner in the plot 
	2. Start in centre
	3. look at next letter in seq
	4. go from current point to half way to letter's corner
	5. mark point
	6. goto 3

	Do the above unil seq is done

	:param seq: Sequence to use to generate the chaos game plot.

	:return : Returns a 2D numpy array representing the chaos game plot.
	'''

	# The 2D matrix that'll end up being the plot.
	chaosPlot = np.zeros((IMAGE_SIZE,IMAGE_SIZE))

	# Start in the centre
	curPosition = np.array([IMAGE_SIZE/2,IMAGE_SIZE/2])

	# For each gene 'g' in the sequence, find the middle point between the currentPosition and g's respective corner and then mark it.
	for g in seq:
		curPosition = findMiddlePoint(curPosition, CORNERS[g])

		# Apparently I need to make the position a tuple to do the indexing I want
		chaosPlot[tuple(curPosition)] = 1

	return chaosPlot
		

def findMiddlePoint(p1,p2):
	'''
	Returns the point between two provided points (params). 
	The parans will be numpy arrays for easy math.

	:param p1: A numpy array containing the coordinates of the first point
	:prarm p2: A numpy array containing the coordinates of the second point

	:return : Numpy array containing the mid point. The mid point will be rounded to the closest point because we will do the math on floats.
	'''
	# Make copies and make them floats. 
	# Important because rounding would be better than truncating
	p1float = p1.astype(np.float)
	p2float = p2.astype(np.float)

	midpoint = (p1float + p2float)/2

	# return the rounded array for the new point
	return np.around(midpoint).astype(np.int)
	

##############
# PARAMETERS #
##############


# Make an odd number so we can start in centre.
IMAGE_SIZE = (2**8)-1

# How many genes are in the sequence
MIN_SIZE = 4000

# Which corner will each gene will be
# WARNING WARNING WARNING
# The placement of these things may be very important. I picked these labels out of nowhere. 
# In other words, there is no method to the madness here. 
# Should defo check back on these labels. 
# ###################################
# Lila used
# C   G
#
# A   T
# No idea if it will end up really making a difference...
CORNERS = {
'A':np.array([0,0]),
'T':np.array([0,IMAGE_SIZE]),
'G':np.array([IMAGE_SIZE,0]),
'C':np.array([IMAGE_SIZE,IMAGE_SIZE])
}


########
# LOAD #
########

# Load in the data as a numpy array and flatten it. Flattening  
# is needed because otherwise we get a list of lists of size 1
print 'Loading Data'
data = np.array(list(csv.reader(open('../../data/preprocess/CRISPR_' + str(MIN_SIZE) + '.csv','r')))).flatten()


##############
# MAKE PLOTS #
##############

# make small for testing
#data = data[:10]

# File for saving the length of the sequences. 
# This will be used to checking of the plot is clustering on length
oFile = open('/home/james/Desktop/CRISPR_PKL/seqLengths_' + str(MIN_SIZE) + '.csv','w')

# list of chaos plots
cps = []

print 'Making Plots (This Will Take A While)'
# For each sequence in our data file, make the chaos plot
for seq in data:
	cp = chaosGamePlot(seq)
	cps.append(cp)
	oFile.write(str(len(seq)) + '\n')

	# UNCOMMENT if you want to see the plot
	#plt.matshow(cp, cmap = 'binary')
	#plt.show()


# Save the output
print 'Saveing Plots'
# WARNING:
#		When the images were 11x11, the pkl was 12.6MB... 
#		In other words, if I make it bigger, I may have a problem!
pickle.dump(cps, open('/home/james/Desktop/CRISPR_PKL/chaosPlots_' + str(IMAGE_SIZE) + '_' + str(MIN_SIZE) + '.pkl','w'))
oFile.close()



