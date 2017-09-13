'''

Single purpose script to rip out the DRs from the copy paste of the CRISPR utility:

http://crispr.i2bc.paris-saclay.fr/crispr/CRISPRUtilitiesPage.html

This was a lazy way to do it, but it hsould do the trick

'''

iFile = open('DR_copyPasteFromUtil.txt','r')
oFile = open('DR.csv','w')

for l in iFile:
	# HAX
	# The thought is, if the line is longer than 19 chars, then it's probably a CRISPR
	if len(l) > 19:
		oFile.write(l)


iFile.close()
oFile.close()
