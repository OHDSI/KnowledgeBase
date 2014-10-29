eclipse-workspace
=================

Jeremy Jao

Location the eclipse workspace I used to run my source code in.

I used Eclipse Luna under Lubuntu 14.04

### Instructions to use Eclipse:
1. open eclipse
2. move the workspace to $GITHUB-FOLDER/KnowledgeBase/ClinicalTrials.gov/eclipe-workspace

The project should just automatically open.

The only project here anyway is CT.gov.

If you do not want to use Eclipse, just use the Ant task...
`ant AddCuis`

But you will need any java that can run on Java SE 1.6 (Java 7 or Java 8 works fine!)

#### MAIN: [AddCuis](https://github.com/OHDSI/KnowledgeBase/blob/master/ClinicalTrials.gov/eclipse-workspace/CT.gov/src/edu/pitt/dbmi/map/addcuis/AddCuis.java)
- USAGE, either:
	- Run it in Eclipse
	- Run the build ant task
		1. `cd CT.gov`
		2. `ant AddCuis`
- Outside Libraries:
	- [Nobletools](https://sourceforge.net/projects/nobletools/) -> Already in as a library
- Input:
	- [Example-CT.gov-data-v3-v011.csv](https://github.com/OHDSI/KnowledgeBase/blob/master/ClinicalTrials.gov/ctgov-inout/Example-CT.gov-data-v3-v011.csv)
		- original CT.gov data with no CUIs
	- [MeSHHashMap.ser](https://github.com/OHDSI/KnowledgeBase/blob/master/ClinicalTrials.gov/ctgov-inout/MeSHHashMap.ser)
		- One-Off Serialized java HashMap that was created from the TRIADS February 2014
		- used for exact string matching for the above's msh_condition and msh_intervention columns
		- created from `ant MeSHMapper` which was only designed to run on Dr. Boyce's dev server
- Output:
	- [Example-CT.gov-data-v3-v011.csv_CUIs_v3.csv](https://github.com/OHDSI/KnowledgeBase/blob/master/ClinicalTrials.gov/ctgov-inout/Example-CT.gov-data-v3-v011.csv_CUIs_v3.csv)
		- CT.gov data with the
			- CUIs for the Text Column
				- MedDRA
				- SNOMEDCT_US
				- MeSH
			- CUIs from exact string matching (see input)
				- MSH_CONDITION
				- MSH_INTERVENTION
	- Report Files
		- [missingCUIs.txt](https://github.com/OHDSI/KnowledgeBase/blob/master/ClinicalTrials.gov/ctgov-inout/missingCUIs.txt)
			- shows which words are missing CUIs
		- [Example-CT.gov-data-v3-v011.csv_CUIs_v3.csv_report.txt](https://github.com/OHDSI/KnowledgeBase/blob/master/ClinicalTrials.gov/ctgov-inout/Example-CT.gov-data-v3-v011.csv_CUIs_v3.csv_report.txt)
			- shows the Nobletools settings and which Semantic Types that were used
			- Amount of missing CUIs from all CUI searches
- Description
	- Adds CUIs to the CT.gov
		- Exact String Matching
			- MESH_CONDITION
			- MESH_INTERVENTION
		- Text Column through [Nobletools](https://sourceforge.net/projects/nobletools/)
			- CUIs
				- MeSH
				- SNOMEDCT_US
				- MedDRA
	- Algorithm
		- First, add the headers by position to [Example-CT.gov-data-v3-v011.csv_CUIs_v3.csv_report.txt](https://github.com/OHDSI/KnowledgeBase/blob/master/ClinicalTrials.gov/ctgov-inout/Example-CT.gov-data-v3-v011.csv_CUIs_v3.csv_report.txt)
		
		- For each column from [Example-CT.gov-data-v3-v011.csv](https://github.com/OHDSI/KnowledgeBase/blob/master/ClinicalTrials.gov/ctgov-inout/Example-CT.gov-data-v3-v011.csv)
			
			- time to add both MESH CONDITIONS and INTERVENTIONS CUIs
				- add the MeSH CUI from the exact string match from the [MeSHHashMap.ser](https://github.com/OHDSI/KnowledgeBase/blob/master/ClinicalTrials.gov/ctgov-inout/MeSHHashMap.ser)
			
			- time to add CUIs for the text column
				- if results are found
					- make temphashmapcui
					- for each result
						- if a specific cui is found
								- if not in the temphashmapcui OR the name of the match matches exactly what is in the text column
									- add to temphashmap
								- else continue
					- add cui to respective column by position if present with the temphashmapcui
				- else write blanks for all text cui columns
