"""
Jeremy Jao
07-19-2014

This is a script that opens the input which will then find missing CUIs
or multiple substances per one drug and then writes them into one of the 4
outputs written below.

Usage:
- python3 getMissingMappings.py

Input:
- The output of the processEuSPCToAddRxNormAndMeSH.py script

Outputs:
- format on all:
	- product|substance
1. missingRxNorms.txt
	- writes single-substance drug with only a missing RxNorm CUI
2. missingMeSHes.txt
	- writes single-substance drug with only a missing MeSH CUI
3. bothCUIsMissing.txt
	- writes single-substance drug with both CUIs missing
4. multipleSubstances.txt
	- writes multi-substance drugs to here

Use python3
"""

import csv
import sys
import os

#opening the new output file generated
with open(sys.argv[1], 'r') as fil:
	
	folder = sys.argv[2]
	
	if not os.path.exists(folder):
		os.makedirs(folder)
	
	rows = csv.reader(fil, delimiter = "\t")
	#skip the header
	next(rows)
	
	'''
	
	opening 4 files for output:
		- for single substances:
			1. missing rxNorm
			2. missing MeSH
			3. both missing
		4. multiple substances output as product name
		
		- output:
			product|substance names(s)
			pipe delimited csvs
	'''
	
	missingRxNorms = open(folder + '/missingRxNorms.txt', 'w')
	missingMeSHes = open(folder + '/missingMeSHes.txt', 'w')
	bothCUIsMissing = open(folder + '/bothCUIsMissing.txt', 'w')
	multipleSubstances = open(folder + '/multipleSubstances.txt', 'w')
	
	currentSubstance = None
	for row in rows:
		# if the substance is already been seen, skip
		if currentSubstance == row[1].strip():
			continue
		
		#if not seen, save the substance name
		currentSubstance = row[1].strip()
		
		#output format in product|substance names(s)
		writeTo = row[0].strip() + '|' + currentSubstance + '\n'
		
		if len(currentSubstance.split(', ')) > 1:
			#if there are multiple substances, write to multipleSubstances.txt
			#else move to all single substance cases
			multipleSubstances.write(writeTo)
		if row[3].strip() == '' and row[4].strip() == '':
			#if both MeSH and RxNorm CUIs are missing, write to bothCUIsMissing.txt
			bothCUIsMissing.write(writeTo)
		elif row[3].strip() == '':
			#if only the RxNorm CUI is missing, write to missingRxNorm.txt
			missingRxNorms.write(writeTo)
		elif row[4].strip() == '':
			#if only the MeSH CUI is missing, write to missingMeSHes.txt
			missingMeSHes.write(writeTo)
		#if it reaches here, then none of the codes are missing on a single-substance drug
