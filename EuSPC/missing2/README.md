missing2 subfolder
==================

Contains the output of [getMissingMappings.py](https://github.com/OHDSI/KnowledgeBase/blob/master/EuSPC/getMissingMappings.py) which ran on the [output](https://github.com/OHDSI/KnowledgeBase/blob/master/EuSPC/FinalRepository_DLP30Jun2012_withCUIs_v2.csv) of [processEuSPCToAddRxNormAndMeSH.py](processEuSPCToAddRxNormAndMeSH.py)

- **Ouptut**
	- format: **drug|substance**
	
	- [missingMeSHes.txt](https://github.com/OHDSI/KnowledgeBase/blob/master/EuSPC/missing2/missingMeSHes.txt)
		- single-substance drugs that are only missing the MeSH CUI
	- [missingRxNorms.txt](https://github.com/OHDSI/KnowledgeBase/blob/master/EuSPC/missing2/missingRxNorms.txt)
		- single substance drugs that are only missing the RxCUI
	- [bothCUIsMissing.txt](https://github.com/OHDSI/KnowledgeBase/blob/master/EuSPC/missing2/bothCUIsMissing.txt)
		- single-substance drugs that are missing both CUIs
	- [multipleSubstances.txt](https://github.com/OHDSI/KnowledgeBase/blob/master/EuSPC/missing2/multipleSubstances.txt)
		- all drugs that had multiple substances
