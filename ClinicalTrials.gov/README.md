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

UMLS Terminology date:
February 2014

We must be able to incrementally update this in order to make sure we get the latest data.

### USAGE:

Below will help you to understand how to run the files.

###### Prerequisites:
- NobleCoder .terminologies folder/file -> triads-test-Feb2014 (TODO: consider making a fast easy way to make this file)
	- At the moment, due to licensing issues with the UMLS library, this only able to be run on the dev server of Dr. Richard Boyce or my (Jeremy's) computer
- Unix-based machine -> TODO: no way to run this on Windows right now since I don't know where noblecoder saves the .terminologies on Windows 

###### To run our test case...
1. Move to the build file that contains the AddCuis class:
	`$ cd eclipse-workspace/CT.gov`
2. run the build task to run the AddCuis class
	`$ ant AddCuis`
	
## FILES AND FOLDERS:
- ctgov-inout
	- location to store the run's input and output files
- eclipse-workspace
	- location to open an eclipse project in
	- also, sub location to run the AddCui
- R-INPUT
	- The input CSV file is tab delimited export out of ct.gov
		1. One has to use first their CT.gov tab delimited export (20 fields, all trials)
		2. In a second step -  it has to be loaded into excel once and saved as CSV to import into R properly. (for some strange reason). Original file imports with errors.
- vojtech-huser
	- folder that contains further ct-gov data (has missing CUIs)
- ctgov001.R
	- R file created by Dr. Huser to get our input for the AddCuis class
