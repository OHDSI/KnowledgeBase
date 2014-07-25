Adverse Drug Reactions Database Import 
=======================================

This table of adverse events from the EU SPCs as downloaded from [PROTECT](http://www.imi-protect.eu/adverseDrugReactions.shtml)

The scripts in this folder add RxCUIs and MeSH IDs to the EU SPC drug list.

### EU SPC Drug Listing

The **euspc-drug-listing** holds drug names for single ingredient drugs
listed in the adverse event table. This was created by:

1. `cat FinalRepository_DLP30Jun2012.csv| cut -f3 | sort | uniq > euspc-drug-listing.txt`
2. within emacs:
`replace-regexp  ".*, .*^J" -> ""`

## Subfolders
1. [json-rxcui](https://github.com/OHDSI/KnowledgeBase/tree/master/EuSPC/json-rxcui)
	- Contains the raw output from the [TRIADs drug named entity recognition program](https://swat-4-med-safety.googlecode.com/svn/trunk/u-of-pitt-SPL-drug-NER) used to input one of the big files.
2. [missingCUIs](https://github.com/OHDSI/KnowledgeBase/tree/master/EuSPC/missingCUIs)
	- contains the output missing CUIs from the first run of [processEuSPCToAddRxNormAndMeSH.py](https://github.com/OHDSI/KnowledgeBase/blob/d2af5e16c2b6f05d59664b93457f90f90da83dea/EuSPC/processEuSPCToAddRxNormAndMeSH.py) using the first [getMissingMappings.py](https://github.com/OHDSI/KnowledgeBase/blob/d933222eca84247c7dcbcc03d203141fb3d98198/EuSPC/getMissingMappings.py) from commit [90f0a68842428c222b9606c05d2d5f129cee7ca4](https://github.com/OHDSI/KnowledgeBase/commit/90f0a68842428c222b9606c05d2d5f129cee7ca4)
	- Also contains the missing CUIs from the first run manually searched in [Bioportal](http://bioportal.bioontology.org/search?opt=advanced)
3. [missing2](https://github.com/OHDSI/KnowledgeBase/tree/master/EuSPC/missing2)
	- contains the missing CUIs from the second run of [processEuSPCToAddRxNormAndMeSH.py](https://github.com/OHDSI/KnowledgeBase/blob/master/EuSPC/processEuSPCToAddRxNormAndMeSH.py)

## Scripts to Run

The main point of the scripts was to add RxCUIs and MeSH IDs to the EU SPC drug list.

1. [processEuSPCToAddRxNormAndMeSH.py](https://github.com/OHDSI/KnowledgeBase/blob/master/EuSPC/processEuSPCToAddRxNormAndMeSH.py)
	- **Description**
		- python2 script
		- if RxNorm and/or MeSH CUI is found in the map files by substance or drug, the CUIs in RxNorm and MeSH will be added 
	- **Input**
		- original file:
			- [FinalRepository_DLP30Jun2012.csv](https://github.com/OHDSI/KnowledgeBase/blob/master/EuSPC/FinalRepository_DLP30Jun2012.csv)
		- map files:
			- [json-rxcui/drugMappings.txt](https://github.com/OHDSI/KnowledgeBase/blob/master/EuSPC/json-rxcui/drugMappings.txt)
			- [missingCUIs/bothCUIsMissing_CUIs.txt](https://github.com/OHDSI/KnowledgeBase/blob/master/EuSPC/missingCUIs/bothCUIsMissing_CUIs.txt)
			- [missingCUIs/missingMeSHes_CUIs.txt](https://github.com/OHDSI/KnowledgeBase/blob/master/EuSPC/missingCUIs/missingMeSHes_CUIs.txt)
			- [missingCUIs/missingRxNorms_CUIs.txt](https://github.com/OHDSI/KnowledgeBase/blob/master/EuSPC/missingCUIs/missingRxNorms_CUIs.txt)
			- [missingCUIs/multipleSubstances_CUIs.txt](https://github.com/OHDSI/KnowledgeBase/blob/master/EuSPC/missingCUIs/multipleSubstances_CUIs.txt)
	- **output**
		- [FinalRepository_DLP30Jun2012_withCUIs_v2.csv](https://github.com/OHDSI/KnowledgeBase/blob/master/EuSPC/FinalRepository_DLP30Jun2012_withCUIs_v2.csv)
2. [getMissingMappings.py](https://github.com/OHDSI/KnowledgeBase/blob/master/EuSPC/getMissingMappings.py)
	- **Description**
		- python3 script
		- This will make a list of drugs with the MeSH or RxCUIs not found from [processEuSPCToAddRxNormAndMeSH.py](https://github.com/OHDSI/KnowledgeBase/blob/master/EuSPC/processEuSPCToAddRxNormAndMeSH.py)
		- finds the missing CUIs of each drug and outputs it into the subfolder [missing2](https://github.com/OHDSI/KnowledgeBase/tree/master/EuSPC/missing2)
	- **Input**
		- [FinalRepository_DLP30Jun2012_withCUIs_v2.csv](https://github.com/OHDSI/KnowledgeBase/blob/master/EuSPC/FinalRepository_DLP30Jun2012_withCUIs_v2.csv)
	- **[Output](https://github.com/OHDSI/KnowledgeBase/tree/master/EuSPC/missing2)**
		- [bothCUIsMissing.txt](https://github.com/OHDSI/KnowledgeBase/blob/master/EuSPC/missing2/bothCUIsMissing.txt)
			- all drugs that are missing both an RxCUI and MeSH CUI
		- [missingMeSHes.txt](https://github.com/OHDSI/KnowledgeBase/blob/master/EuSPC/missing2/missingMeSHes.txt)
			- all drugs missing a MeSH CUI
		- [missingRxNorms.txt](https://github.com/OHDSI/KnowledgeBase/blob/master/EuSPC/missing2/missingRxNorms.txt)
			- all drugs missing an RxCUI
		- [multipleSubstances.txt](https://github.com/OHDSI/KnowledgeBase/blob/master/EuSPC/missing2/multipleSubstances.txt)
			- all drugs that are composed of multiple substances

##### Usage:

Prerequirements: **python2** and **python3** need to be installed

1. `python processEuSPCToAddRxNormAndMeSH.py`
2. `python3 getMissingMappings.py FinalRepository_DLP30Jun2012_withCUIs_v2.csv missing2`


