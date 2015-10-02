data/missing
===========

This is the subfolder that contains the missing output of the first and second run of [processEuSPCToAddRxNormAndMeSH.py](https://github.com/OHDSI/KnowledgeBase/blob/d2af5e16c2b6f05d59664b93457f90f90da83dea/EuSPC/processEuSPCToAddRxNormAndMeSH.py) from commit [90f0a68842428c222b9606c05d2d5f129cee7ca4](https://github.com/OHDSI/KnowledgeBase/commit/90f0a68842428c222b9606c05d2d5f129cee7ca4) using the first [getMissingMappings.py](https://github.com/OHDSI/KnowledgeBase/blob/d933222eca84247c7dcbcc03d203141fb3d98198/EuSPC/getMissingMappings.py)


**Files**
- from [getMissingMappings.py](https://github.com/OHDSI/KnowledgeBase/blob/d933222eca84247c7dcbcc03d203141fb3d98198/EuSPC/getMissingMappings.py)
	- format: **drug|substance**
	- [missingMeSHes.txt](https://github.com/OHDSI/KnowledgeBase/blob/master/EuSPC/data/missing/missingMeSHes.txt)
		- single-substance drugs that are only missing the MeSH CUI
	- [missingRxNorms.txt](https://github.com/OHDSI/KnowledgeBase/blob/master/EuSPC/data/missing/missingRxNorms.txt)
		- single substance drugs that are only missing the RxCUI
	- [bothCUIsMissing.txt](https://github.com/OHDSI/KnowledgeBase/blob/master/EuSPC/data/missing/bothCUIsMissing.txt)
		- single-substance drugs that are missing both CUIs
	- [multipleSubstances.txt](https://github.com/OHDSI/KnowledgeBase/blob/master/EuSPC/data/missing/multipleSubstances.txt)
		- all drugs that had multiple substances
- the CUIs that were manually attained through the description below:
	- format: **drug|substance|CUI**
		- [missingMeSHes_CUIs.txt](https://github.com/OHDSI/KnowledgeBase/blob/master/EuSPC/data/missing/missingMeSHes_CUIs.txt)
			- single-substance drugs with their manually found MeSH CUI
		- [missingRxNorms_CUIs.txt](https://github.com/OHDSI/KnowledgeBase/blob/master/EuSPC/data/missing/missingRxNorms_CUIs.txt)
			- single-substance drugs with their manually found RxCUI
	- format: **drug|substance|RxCUI|MeSH**
		- [bothCUIsMissing_CUIs.txt](https://github.com/OHDSI/KnowledgeBase/blob/master/EuSPC/data/missing/bothCUIsMissing_CUIs.txt)
			- single-substance drugs previously missing both CUIs manually searched
		- [multipleSubstances_CUIs.txt](https://github.com/OHDSI/KnowledgeBase/blob/master/EuSPC/data/missing/multipleSubstances_CUIs.txt)
			- all drugs that had multiple substances that hopefully have their CUIs

## Manually Searching RxNorm and MeSH CUIs
