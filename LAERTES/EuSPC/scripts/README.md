SCRIPTS
=======

Prerequirements: **python2** and **python3** need to be installed

## USAGE:

1. `python processEuSPCToAddRxNormAndMeSH.py` # NOTE: first edit the paths in this script to hold <EU SPC drug-HOI data file>
2. `python3 getMissingMappings.py ../data/<EU SPC drug-HOI data file>_withCUIs_v1.csv ../data/missing`


- [processEuSPCToAddRxNormAndMeSH.py](https://github.com/OHDSI/KnowledgeBase/blob/master/EuSPC/processEuSPCToAddRxNormAndMeSH.py)
	- **Description**
		- python2 script
		- if RxNorm and/or MeSH CUI is found in the map files by substance or drug, the CUIs in RxNorm and MeSH will be added 
	- **Input**
		- original file:
			- <EU SPC drug-HOI data file>
		- map files:
			- [json-rxcui/drugMappings.txt](https://github.com/OHDSI/KnowledgeBase/blob/master/EuSPC/json-rxcui/drugMappings.txt)
			- [missingCUIs/bothCUIsMissing_CUIs.txt](https://github.com/OHDSI/KnowledgeBase/blob/master/EuSPC/missingCUIs/bothCUIsMissing_CUIs.txt)
			- [missingCUIs/missingMeSHes_CUIs.txt](https://github.com/OHDSI/KnowledgeBase/blob/master/EuSPC/missingCUIs/missingMeSHes_CUIs.txt)
			- [missingCUIs/missingRxNorms_CUIs.txt](https://github.com/OHDSI/KnowledgeBase/blob/master/EuSPC/missingCUIs/missingRxNorms_CUIs.txt)
			- [missingCUIs/multipleSubstances_CUIs.txt](https://github.com/OHDSI/KnowledgeBase/blob/master/EuSPC/missingCUIs/multipleSubstances_CUIs.txt)
	- **output**
		- <EU SPC drug-HOI data file>_withCUIs_v1.csv
- [getMissingMappings.py](https://github.com/OHDSI/KnowledgeBase/blob/master/EuSPC/scripts/getMissingMappings.py)
	- **Description**
		- python3 script
		- This will make a list of drugs with the MeSH or RxCUIs not found from [processEuSPCToAddRxNormAndMeSH.py](https://github.com/OHDSI/KnowledgeBase/blob/master/EuSPC/data/processEuSPCToAddRxNormAndMeSH.py)
		- finds the missing CUIs of each drug and outputs it into the subfolder [missing](https://github.com/OHDSI/KnowledgeBase/tree/master/EuSPC/data/missing)
	- **Input**
		- <EU SPC drug-HOI data file>_withCUIs_v1.csv
	- **[Output](https://github.com/OHDSI/KnowledgeBase/tree/master/EuSPC/data/missing)**
		- [bothCUIsMissing.txt](https://github.com/OHDSI/KnowledgeBase/blob/master/EuSPC/data/missing/bothCUIsMissing.txt)
			- all drugs that are missing both an RxCUI and MeSH CUI
		- [missingMeSHes.txt](https://github.com/OHDSI/KnowledgeBase/blob/master/EuSPC/data/missing/missingMeSHes.txt)
			- all drugs missing a MeSH CUI
		- [missingRxNorms.txt](https://github.com/OHDSI/KnowledgeBase/blob/master/EuSPC/data/missing/missingRxNorms.txt)
			- all drugs missing an RxCUI
		- [multipleSubstances.txt](https://github.com/OHDSI/KnowledgeBase/blob/master/EuSPC/data/missing2/multipleSubstances.txt)
			- all drugs that are composed of multiple substances
