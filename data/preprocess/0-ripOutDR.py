'''

Single purpose script to rip out the DRs from the copy paste of the CRISPR utility:

http://crispr.i2bc.paris-saclay.fr/crispr/CRISPRUtilitiesPage.html

This was a lazy way to do it, but it should do the trick

'''

iFile = open('DR_copyPasteFromUtil.txt','r')
oFile = open('DR.csv','w')

for l in iFile:
	# HAX
	# The thought is, if the line is longer than 20 chars, then it's probably a CRISPR
	# If you have it set to 19, some of the non sequences will pass the test (just an FYI)
	# if you have 
	if len(l) > 20: #
		# skips the last 2 chars in each line. 2nd last char is a tab, last is a new line.
		# we really only want to cut the tab char, so that's why I re-add the new line char after
		oFile.write(l.strip() + '\n')		



iFile.close()
oFile.close()
