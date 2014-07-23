Adverse Drug Reactions Database
================================
 

The PROTECT ADR database is a downloadable Excel file listing of all MedDRA PT or LLT adverse drug reactions (ADRs). It is a structured Excel database of all adverse drug reactions (ADRs) listed in section 4.8 of the Summary of Product Characteristics (SPC) of medicinal products authorised in the EU according to the centralised procedure. It is based exclusively on MedDRA terminology. In principle, MedDRA Preferred Terms (PT) are used to map terms of the SPC. When they are used in the SPC to add precision in the description of the ADR, Low Level Terms (LLTs) are also coded. PTs and LLTs are linked to a primary System Organ Class (SOC). The database also includes information on gender, causality, frequency, class warning and source of information for ADRs for which additional information is provided in the SPC. Fields are described in the file Database structure.


The current database has been updated up to 31 December 2012 based on latest available SPC which can be found on the European Commission website. The database includes for each product the date of the SPC which has been used to list ADRs.


The database has been created by EMA and partners in PROTECT Work Package 3 through a stepwise approach using automated mapping of ADR terms listed in section 4.8 of the SPC to the MedDRA terminology, fuzzy text matching (Bergvall et al. Pharmacoepidemiol Drug Saf. 2011;20(S1), S143) and expert review.
It is aimed to routinely update the database at least once a year based on amended SPCs. It can also be amended between routine updates to correct data entries.

#### Objectives

A time-consuming step in signal detection of adverse reactions is the determination of whether an effect is already recorded in the European Summary of Product Characteristics (SPC). Thus there is a need for a structured database which can be searched for this information. Such a database also allows filtering or flagging reaction monitoring reports for signals related to unlisted reactions only, thus improving considerably the efficiency of the signal detection process.

A data set of established ADRs also allows a comparison to coincidental or unidentified drug-adverse event combinations only, an adjustment of statistical signals for known ADRs, and an evaluation of the effect of background restriction on the performance of statistical signal detection.
The objective of the ADR database is not to provide a continuously updated list of ADRs to centrally-authorised products.

#### Disclaimer


The establishment of this database, which is set up and maintained by the EMA and PROTECT partners, is not required by legislation and it is intended to provide an additional tool for signal detection activities and research purposes. Although all parties involved in the project have made their best efforts to provide comprehensive and up-to-date information, the EMA and PROTECT partners cannot be held responsible for failure to list some adverse drug reactions, inaccuracies in the MedDRA mapping and for any inappropriate use of this database.

This table of adverse events from the EU SPCs as downloaded from [PROTECT](http://www.imi-protect.eu/adverseDrugReactions.shtml)


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
	- contains the output of the first run of [processEuSPCToAddRxNormAndMeSH.py](https://github.com/OHDSI/KnowledgeBase/blob/d2af5e16c2b6f05d59664b93457f90f90da83dea/EuSPC/processEuSPCToAddRxNormAndMeSH.py) from commit [d2af5e16c2b6f05d59664b93457f90f90da83dea](https://github.com/OHDSI/KnowledgeBase/commit/d2af5e16c2b6f05d59664b93457f90f90da83dea)
	- Also contains the missing CUIs from the first run manually searched in [Bioportal](http://bioportal.bioontology.org/search?opt=advanced)
3. [missing2](https://github.com/OHDSI/KnowledgeBase/tree/master/EuSPC/missing2)
	- contains the missing CUIs from the second run of [processEuSPCToAddRxNormAndMeSH.py](https://github.com/OHDSI/KnowledgeBase/blob/master/EuSPC/processEuSPCToAddRxNormAndMeSH.py)

## Scripts to Run

1. [processEuSPCToAddRxNormAndMeSH.py](https://github.com/OHDSI/KnowledgeBase/blob/master/EuSPC/processEuSPCToAddRxNormAndMeSH.py)
	- **Description**
		- python2 script
		- Add columns with RxNorm and MeSH mappings
		- These mappings come from input for each drug from the map files
		- if found, the CUIs in RxNorm and MeSH will be added to the dict
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


