'''
Author: James Alexander Hughes

Single purpose script to pull the CRISPRs out of the file that I got from the Parisians. 
Their file had some formatting that I didn't want, so I'm just gonna strip out what I want. 

I originally tried to get this data from the CRISPR db website (http://crispr.i2bc.paris-saclay.fr/crispr/CRISPRUtilitiesPage.html),
but unfortunately that was gonna take forever. I ended up having to get the data by emailing the owners, 
and then they sent me the data (see last email below, or your inbox). 


# EMAIL FROM DAVID COUVIN
Dear James,

Sorry for the delayed response due to other ongoing works.

You will find enclosed a zipped file ("completeCRISPRs.txt.zip") containing all nucleotides corresponding to CRISPRs arrays available in CRISPRdb.

Best regards,
David

'''


MIN_SIZE = 4000								# Minimum size of a CRISPR before we take it
iFile = open('completeCRISPRs.txt','r')
oFile = open('CRISPR_' + str(MIN_SIZE) + '.csv','w')
labelFile = open('CRISPR_labels_' + str(MIN_SIZE) + '.csv','w')	# File for the labels. No idea if this will be handy, but why not save it?

CRISPR = ''



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


iFile.close()
oFile.close()
labelFile.close()
