Adverse Drug Reactions Database Import 
=======================================

This table of adverse events from the EU SPCs as downloaded from [PROTECT](http://www.imi-protect.eu/adverseDrugReactions.shtml)

The scripts in this folder add RxCUIs and MeSH IDs to the EU SPC drug list. In most cases, there was a simple string match betwee an entry in the 'substance' column with an RxNorm or MeSH preferred term. However, there are many cases of combination products, and a few things that were unable to be mapped. The combination products were manually mapped where possibly using the Bioportal's ontology search. 

The final dataset is in FinalRepository_DLP30Jun2012_withCUIs.csv


## USAGE:
1. `cd scripts`
2. `python processEuSPCToAddRxNormAndMeSH.py`
3. `python3 getMissingMappings.py FinalRepository_DLP30Jun2012_withCUIs_v2.csv ../data/missing`

### Processing the EU SPC Drug Listing

The **euspc-drug-listing** holds drug names for single ingredient drugs
listed in the adverse event table. This was created by:

1. `cat FinalRepository_DLP30Jun2012.csv| cut -f3 | sort | uniq > euspc-drug-listing.txt`
2. within emacs:
`replace-regexp  ".*, .*^J" -> ""`


## Subfolders
1. [json-rxcui](https://github.com/OHDSI/KnowledgeBase/tree/master/EuSPC/json-rxcui)
	- Contains the raw output from the [TRIADs drug named entity recognition program](https://swat-4-med-safety.googlecode.com/svn/trunk/u-of-pitt-SPL-drug-NER) used to input one of the big files.
2. [data/missing](https://github.com/OHDSI/KnowledgeBase/tree/master/EuSPC/data/missing)
	- contains the missing CUIs from the second run of [processEuSPCToAddRxNormAndMeSH.py](https://github.com/OHDSI/KnowledgeBase/blob/master/EuSPC/processEuSPCToAddRxNormAndMeSH.py)
3. [backup/missingCUIs](https://github.com/OHDSI/KnowledgeBase/tree/master/EuSPC/backup/missingCUIs)
	- A backup folder containing the output missing CUIs from the first run of [processEuSPCToAddRxNormAndMeSH.py](https://github.com/OHDSI/KnowledgeBase/blob/d2af5e16c2b6f05d59664b93457f90f90da83dea/EuSPC/processEuSPCToAddRxNormAndMeSH.py) using the first [getMissingMappings.py](https://github.com/OHDSI/KnowledgeBase/blob/d933222eca84247c7dcbcc03d203141fb3d98198/EuSPC/getMissingMappings.py) from commit [90f0a68842428c222b9606c05d2d5f129cee7ca4](https://github.com/OHDSI/KnowledgeBase/commit/90f0a68842428c222b9606c05d2d5f129cee7ca4)
	- Also contains the missing CUIs from the first run manually searched in [Bioportal](http://bioportal.bioontology.org/search?opt=advanced)
4. [scripts](https://github.com/OHDSI/KnowledgeBase/tree/master/EuSPC/scripts)
	- location of the scripts file to run
5. [data](https://github.com/OHDSI/KnowledgeBase/tree/master/EuSPC/data)
	- location of the scripts output files

