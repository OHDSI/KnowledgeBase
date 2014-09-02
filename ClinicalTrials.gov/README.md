ClinicalTrials.gov
==================

- Jeremy Jao
- Dr. Richard Boyce
- Dr. Vojtech Huser

This folder represents a way to bring ClinicalTrials.gov data into the 
Knowledgebase.

What Dr. Boyce and I (Jeremy Jao - epicstar) did was to add CUIs to the 
ClinicalTrials.gov in ctgov-inout folder to guide us to the drilldown 
and summary use cases for our project which will help us get the correct
OMOP CUI. The way to do this is explained in the USAGE section of this 
readme.

***USAGE:

To run our test case...
1. Move to the build file that contains the AddCuis class:
	`$ cd eclipse-workspace/CT.gov`
2. run the build task to run the AddCuis class
	`$ ant AddCuis`
	
**FILES AND FOLDERS:
- ctgov-inout
	- location to store the run's input and output files
- eclipse-workspace
	- location to open an eclipse project in
	- also, sub location to run the AddCui
- vojtech-huser
	- folder that contains further ct-gov data (has missing CUIs)
- ctgov001.R
	- R file created by Dr. Huser to get our input for the AddCuis class
