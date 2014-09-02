missing subfolder
==================

Contains the output of [getMissingMappings.py](https://github.com/OHDSI/KnowledgeBase/blob/master/EuSPC/scripts/getMissingMappings.py) which ran on the [output](https://github.com/OHDSI/KnowledgeBase/blob/master/EuSPC/FinalRepository_DLP30Jun2012_withCUIs_v2.csv) of [processEuSPCToAddRxNormAndMeSH.py](https://github.com/OHDSI/KnowledgeBase/blob/master/EuSPC/processEuSPCToAddRxNormAndMeSH.py)

- **Ouptut**
	- format: **drug|substance**
	
	- [missingMeSHes.txt](https://github.com/OHDSI/KnowledgeBase/blob/master/EuSPC/data/missing/missingMeSHes.txt)
		- single-substance drugs that are only missing the MeSH CUI
	- [missingRxNorms.txt](https://github.com/OHDSI/KnowledgeBase/blob/master/EuSPC/data/missing/missingRxNorms.txt)
		- single substance drugs that are only missing the RxCUI
	- [bothCUIsMissing.txt](https://github.com/OHDSI/KnowledgeBase/blob/master/EuSPC/data/missing/bothCUIsMissing.txt)
		- single-substance drugs that are missing both CUIs
	- [multipleSubstances.txt](https://github.com/OHDSI/KnowledgeBase/blob/master/EuSPC/data/missing/multipleSubstances.txt)
		- all drugs that had multiple substances
