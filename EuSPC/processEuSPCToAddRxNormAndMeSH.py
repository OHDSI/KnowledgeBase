# processEuSPCToAddRxNormAndMeSH.py
#
# Add columns with RxNorm and MeSH mappings
#
# Author: Richard Boyce and Jeremy Jao
# 07.16.2014

import csv
import string
import pprint
##########INPUT STRING NAME FILES#######################################
inp = 'FinalRepository_DLP30Jun2012.csv'
out = 'FinalRepository_DLP30Jun2012_withCUIs_v2.csv'

mapfolder = 'json-rxcui/'
rxmap = mapfolder + 'tempRXCUIMappings_pipe.txt'
meshmap = mapfolder + 'tempMESHCUImappings.txt'
rawmap = mapfolder + 'drugMappings.txt'

missingfolder = 'missingCUIs/'
rxmissing = missingfolder + 'missingRxNorms_CUIs.txt'
meshmissing = missingfolder + 'missingMeSHes_CUIs.txt'
bothmissing = missingfolder + 'bothCUIsMissing_CUIs.txt'
multiplesubs = missingfolder + 'multipleSubstances_CUIs.txt'
########################################################################

###########FUNCTIONS####################################################

#takes a csv map of 2 columns (first is CUI and 2nd is drug name
#and puts it into a dictionary.
#Only coded for an RxNorm or MeSH CUIs for now
##Deprecated
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
mapdict = {}
missingdict = {}

#makeDictMap(meshmap, mapdict)
#makeDictMap(rxmap, mapdict)

makeCompleteDict(rawmap, mapdict)

makeMissingDict(missingdict, rxmissing, 'RXNORM')
makeMissingDict(missingdict, meshmissing, 'MESH')
makeMissingDict(missingdict, bothmissing, 'BOTH')
makeMissingDict(missingdict, multiplesubs, 'BOTH')

hi = open('missingict.txt', 'w')
pprint.pprint(missingdict, hi)
hi.close()

outfile = open(out, 'w')
outcsv = csv.writer(outfile, delimiter = "\t")

with open(inp, 'r') as fil:
	repo = csv.reader(fil, delimiter = "\t")
	row = repo.next()
	row.insert(3, 'MeSH')
	row.insert(3, 'RxNorm')
	outcsv.writerow(row)
	
	for row in repo:
		substance = row[2].lower().strip()
		drug = row[0].lower().strip()
		
		MESH = None
		RXNORM = None
		
		if substance in mapdict:
			subdata = mapdict[substance]
			RXNORM = subdata['RXNORM']
			MESH = subdata['MESH']
			if drug in missingdict:
				if RXNORM is None and missingdict[drug]['RXNORM'] is not None:
					RXNORM = missingdict[drug]['RXNORM']
					#print drug
					#print RXNORM
					
				if MESH is None and missingdict[drug]['MESH'] is not None:
					MESH = missingdict[drug]['MESH']
					
		elif drug in missingdict:
			drugdata = missingdict[drug]
			if drug == 'mixtard':
				print 'hi'
			if drugdata['RXNORM'] is not None and RXNORM is None:
				RXNORM = drugdata['RXNORM']
			if drugdata['MESH'] is not None and MESH is None:
				MESH = drugdata['MESH']
		row.insert(3, MESH)
		row.insert(3, RXNORM)
				
		#notdone = True
		#case where the drug is identified with multiple drug names
		#for lame in string.split(names, ', '):
			#name = lame.strip()
			##if the drug with multiple drug names is found, add the cuis
			##then break
			#if(name in mapdict):
				#row.insert(3, mapdict[name]['MESH'])
				#row.insert(3, mapdict[name]['RXNORM'])
				#notdone = False
				#break
		##if the drug was never found, keep the rows in sync
		#if notdone:
			#row.insert(3, None)
			#row.insert(3, None)
		outcsv.writerow(row)

outfile.close()

