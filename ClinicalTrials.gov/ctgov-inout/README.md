ctgov-inout
===========

Jeremy Jao

Location for the inputs and outputs of the ClinicalTrials.gov portion of the CUIs.

[Example-CT.gov-data-v3-v011.csv_CUIs_v3.csv](https://github.com/OHDSI/KnowledgeBase/blob/master/ClinicalTrials.gov/ctgov-inout/Example-CT.gov-data-v3-v011.csv_CUIs_v3.csv) contains the CUIs needed to run a drilldown and summary case

### Files:
- [Example-CT.gov-data-v3-v011.csv](https://github.com/OHDSI/KnowledgeBase/blob/master/ClinicalTrials.gov/ctgov-inout/Example-CT.gov-data-v3-v011.csv)
	- input for [AddCuis](https://github.com/OHDSI/KnowledgeBase/blob/master/ClinicalTrials.gov/eclipse-workspace/CT.gov/src/edu/pitt/dbmi/map/addcuis/AddCuis.java) (the main)
	- contains the data to add CUIs for
- [MeSHHashMap.ser](https://github.com/OHDSI/KnowledgeBase/blob/master/ClinicalTrials.gov/ctgov-inout/MeSHHashMap.ser)
	- input for [AddCuis](https://github.com/OHDSI/KnowledgeBase/blob/master/ClinicalTrials.gov/eclipse-workspace/CT.gov/src/edu/pitt/dbmi/map/addcuis/AddCuis.java) to get the cuis for mesh interventions and conditions by exact string matching
	- is a serialized java HashMap<Source, String>
	- output from [MeSHMapper.java](https://github.com/OHDSI/KnowledgeBase/blob/master/ClinicalTrials.gov/eclipse-workspace/CT.gov/src/edu/pitt/dbmi/mapping/MeSHMapper.java) which can only be run in Dr. Boyce's dev server.
- [Example-CT.gov-data-v3-v011.csv_CUIs_v3.csv](https://github.com/OHDSI/KnowledgeBase/blob/master/ClinicalTrials.gov/ctgov-inout/Example-CT.gov-data-v3-v011.csv_CUIs_v3.csv)
	- output from [AddCuis](https://github.com/OHDSI/KnowledgeBase/blob/master/ClinicalTrials.gov/eclipse-workspace/CT.gov/src/edu/pitt/dbmi/map/addcuis/AddCuis.java) (the main)
	- this is the main file to use for the outputs
- [Example-CT.gov-data-v3-v011.csv_CUIs_v3.csv_report.txt](https://github.com/OHDSI/KnowledgeBase/blob/master/ClinicalTrials.gov/ctgov-inout/Example-CT.gov-data-v3-v011.csv_CUIs_v3.csv_report.txt)
	- output report that specifies the number of CUIs are missing and the properties from [AddCuis](https://github.com/OHDSI/KnowledgeBase/blob/master/ClinicalTrials.gov/eclipse-workspace/CT.gov/src/edu/pitt/dbmi/map/addcuis/AddCuis.java)
- [missingCUIs.txt](https://github.com/OHDSI/KnowledgeBase/blob/master/ClinicalTrials.gov/ctgov-inout/missingCUIs.txt)
	- output report that specifies which words are missing CUIs from [AddCuis](https://github.com/OHDSI/KnowledgeBase/blob/master/ClinicalTrials.gov/eclipse-workspace/CT.gov/src/edu/pitt/dbmi/map/addcuis/AddCuis.java)
