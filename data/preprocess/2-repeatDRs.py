'''
Author: James Alexander Hughes

Build a script to take the DRs and just repeat them a bunch of times until they are of a certain length. 

'''


LENGTH = 10000			# How long do we want our sequences to be?
iFile = open('DR.csv','r')
oFile = open('/home/james/Desktop/CRISPR_PKL/DRs_' + str(LENGTH) + '.csv','w')

# For each DR, take it, and repeat it multiple times until it is longer than LENGTH
for l in iFile:
	startSize = len(l)		# How long was each DR before we do anything
	DRDRDR = l.strip() * ((LENGTH/startSize) + 1)
	oFile.write(DRDRDR + '\n')



iFile.close()
oFile.close()


'''
# Characters that we will allow in our sequences.
# Some K, Y, Ms and others kept popping up. 
goodChars = set('ATGC\n')	

for l in iFile:
	# if l[0] is the '>' character, then it's just a label, so we'll hold onto that.  
	if l[0] == '>':
		label = l
	else:
		# If l[0] is a new line character only, then we know that there is a space, and the CRISPR sequence is done
		# and we are about to roll over into the next CRISPR (next line will be a label anyways)
		if l[0] == '\n':
			# Checks if the sequence only contains ATGCs. Not sure what the other stuff is. Proteins? idk. 
			# Could probably make this a regex, but whatever. 
			# Anyways, if the letters check out, save the label and the CRISPR to their respective files. 
			if set(CRISPR) <= goodChars:
				
				# If the CRISPR is actually longer than MIN_SIZE, we'll take it.
				# We want to make sure there is enough info in there to eliminate noise. 
				if len(CRISPR) >= MIN_SIZE:
					labelFile.write(l)
					oFile.write(CRISPR + '\n')
			
			CRISPR = ''

		# OK, here we just have part (or possibly all?) of a CRISPR sequence
		else:
			CRISPR = CRISPR + l.strip()
'''


