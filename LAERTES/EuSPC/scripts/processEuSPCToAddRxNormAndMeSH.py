# processEuSPCToAddRxNormAndMeSH.py
#
# Add columns with RxNorm and MeSH mappings from the original input
# using the input generated from the TRIADs drug named entity recognition program
# and manually searched CUIs missing from the data.
#
# Usage:
#	python processEuSPCToAddRxNormAndMeSH.py
#
# Author: Richard Boyce and Jeremy Jao
# 07.16.2014

import csv
import string
import pprint
##########INPUT STRING NAME FILES#######################################
inp = '../data/Finalrepository_2Sep2014_DLP30June2013.csv'
out = '../data/Finalrepository_2Sep2014_DLP30June2013_withCUIs_v1.csv'

## raw input from the TRIADs drug named entity recognition program
mapfolder = '../json-rxcui/'
rxmap = mapfolder + 'tempRXCUIMappings_pipe.txt'
meshmap = mapfolder + 'tempMESHCUImappings.txt'
rawmap = mapfolder + 'drugMappings.txt'

## missing CUIs not present from the above file
missingfolder = '../data/missing/'
rxmissing = missingfolder + 'missingRxNorms_CUIs.txt'
meshmissing = missingfolder + 'missingMeSHes_CUIs.txt'
bothmissing = missingfolder + 'bothCUIsMissing_CUIs.txt'
multiplesubs = missingfolder + 'multipleSubstances_CUIs.txt'
########################################################################

###########FUNCTIONS####################################################

#takes a csv map of 2 columns (first is CUI and 2nd is drug name
#and puts it into a dictionary.
#Only coded for an RxNorm or MeSH CUIs for now
##Deprecated!!
def makeDictMap(fil, dct):
	if 'RX' in fil:
		addTo = 'RxNorm'
	else:
		addTo = 'MeSH'
	with open(fil, 'r') as fi:
		cs = csv.reader(fi, delimiter="|")
		for row in cs:
			name = row[1].lower()
			cui = row[0]
			
			if name not in dct:
				dct[name] = {'RxNorm':None, 'MeSH':None}
				#print 'adding ' +  name + ' to the dict'
			
			elif dct[name][addTo] is not None:
				print name + "'s " + addTo + ' is already added. There is an error somewhere.'
				print 'old cui is ' + dct[name][addTo] + '. new cui is ' + cui
				
			dct[name][addTo] = cui

#Takes a file (see raw map) that handles drugs of 1+ strings to identify as a name
#Then puts it into a dictionary for either an rxnorm and/or mesh cui			
def makeCompleteDict(fil, dct):
	with open(fil, 'r') as fi:
		import string
		import re
		for line in fi:
			
			#will split all of this:
			#http://purl.bioontology.org/ontology/MESH/C114556 aprepitant 1785 1773
			row = string.split(line.strip(),' ')
			#splits the URL
			#ex http://purl.bioontology.org/ontology/MESH/C114556
			#grabs the last 2 things... MESH and C11456
			cui = string.split(row[0], '/')[-2:]
			addTo = cui[0]
			cui = cui[1]
			
			regexp = re.compile('[A-Za-z]')
			#if statement that handles whether or not the name of the CUI
			#contains one or two strings
			if regexp.search(row[2]) is not None:
				name = (row[1] + ' ' + row[2]).lower()
			else:
				name = row[1].lower()
				
			if name not in dct:
				dct[name] = {'RXNORM':None, 'MESH':None}
			
			
			plsadd = dct[name][addTo]
			#case where the cui has already been added
			if plsadd is not None:
				
				print name + "'s " + addTo + ' is already added.'
				print 'old cui is ' + plsadd + '. new cui is ' + cui
			#if cui is the same as the one already added, readding
			if dct[name][addTo] == cui:
				print 'cuis are the same. not adding.'
			else:
				dct[name][addTo] = cui
				
#Makes the dict of manually searched RxNorm and MeSH CUIs that the TRIADS
#output could not be obtained automatically
def makeMissingDict(dic, fil, typ):
	
	with open(fil, 'r') as fi:
		rows = csv.reader(fi, delimiter='|')
		rows.next()
		line = 1
		for row in rows:
			drug = row[0].lower().strip()
			substance = row[1].lower().strip()
			if drug not in dic:
				dic[drug] = {'substance': substance, 'RXNORM': None, 'MESH': None}
			try:
				if typ is 'BOTH':
					notNullAdd(dic[drug], 'RXNORM', row[2])
					notNullAdd(dic[drug],'MESH' , row[3])
				elif typ is 'RXNORM' or typ is 'MESH':
					notNullAdd(dic[drug], typ, row[2])
				else:
					print 'Was supposed to add to missing but nope...'
			except IndexError:
				print('%s, %d)', (fil, line))
				
			line += 1
			
			
#adds to the dictionary if the object being added is not null
def notNullAdd(dic, index, obj):
	if obj is not None and obj is not '':
		if dic[index] is None:
			dic[index] = obj
		elif dic[index] == obj:
			print 'missing cuis are the same. not adding.'
		else:
			print 'Something probably wrong with the missing CUIs'
##########################################################################

################################MAIN######################################
mapdict = {} # the TRIADS RxNorm and MeSH CUIs by substance
missingdict = {} # the manually searched CUIs by drug name

#Filling up mapdict
makeCompleteDict(rawmap, mapdict)

#filling up missingdict
makeMissingDict(missingdict, rxmissing, 'RXNORM')
makeMissingDict(missingdict, meshmissing, 'MESH')
makeMissingDict(missingdict, bothmissing, 'BOTH')
makeMissingDict(missingdict, multiplesubs, 'BOTH')

outfile = open(out, 'w')
outcsv = csv.writer(outfile, delimiter = "\t")

#opening the main input that the CUIs will be added to
with open(inp, 'r') as fil:
	repo = csv.reader(fil, delimiter = "\t")
	row = repo.next()
	# adding the extra header CUIs to the 3rd index
	row.insert(3, 'MeSH')
	row.insert(3, 'RxNorm')
	outcsv.writerow(row)
	
	# now applying to all rows of data
	for row in repo:
		
		#getting substance of row
		substance = row[1].lower().strip()
		#getting drug of row
		drug = row[0].lower().strip()
		
		#initializing the MeSH and RxCUI variables
		MESH = None
		RXNORM = None
		
		#case where substance is found in the TRIADS input
		if substance in mapdict:
			subdata = mapdict[substance]
			RXNORM = subdata['RXNORM']
			MESH = subdata['MESH']
			
			#if the drug name is in the manually searched CUIs dict
			if drug in missingdict:
				
				#if the RxCUI was not in the TRIADS input
				if RXNORM is None and missingdict[drug]['RXNORM'] is not None:
					#add the RxNorm CUI from the manually searched CUIs dict
					RXNORM = missingdict[drug]['RXNORM']
				
				#if the MeSH CUI was not in the TRIADS input					
				if MESH is None and missingdict[drug]['MESH'] is not None:
					#add the MeSH CUI from the manually searched CUIs dict
					MESH = missingdict[drug]['MESH']
					
		#case where the substance was not found in the TRIAD input
		#but the drug name was found in the manually searched CUIs dict
		elif drug in missingdict:
			drugdata = missingdict[drug]
			if drugdata['RXNORM'] is not None and RXNORM is None:
				#if the RxCUI was found in the manually searched
				#CUIs dict, we use this 
				RXNORM = drugdata['RXNORM']
			if drugdata['MESH'] is not None and MESH is None:
				#if the MeSH CUI was found in the manually searched
				#CUIs dict, we use this 
				MESH = drugdata['MESH']
		#adding the MeSH and RxNorm CUIs, doesn't have to have a value
		row.insert(3, MESH)
		row.insert(3, RXNORM)
		#write to the output file	
		outcsv.writerow(row)

outfile.close()

