Scripts to synthesize the evidence source count and linkout data into
tables that can them be loaded into the Schema relational DB model
(that extends the OHDSI Standard Vocab). 

LOADING THE SCHEMA AND DATA INTO THE OHDSI STANDARD VOCABULARY: 

1) Edit integratedSources.conf and the run the script
   mergeCountsFromIntegratedSources.py. This creates the files
   uniq_drug_hoi_relationships.csv and drug-hoi-evidence-data.tsv

2) load uniq_drug_hoi_relationships.csv, drug-hoi-evidence-data.tsv,
   and ohdsiTest3.psql to the /mnt/vol1/inbound folder on the OHDSI
   dev server.

3) ssh to the OHDSI dev server, change to the /mnt/vol1/inbound folder
   and run:
   psql -U <user name> -h 127.0.0.1 -W -d vocabulary < ohdsiTest3.psql

4) Wait - estimated time - more than a couple of hours


------------------------------------------------------------------------
FOLDER LAYOUT
------------------------------------------------------------------------

- ohdsiTest3.psql : the work horse for this process - creates the
                    schema tables, loads data, and creates a pivot
                    table as a view to make the system more user
                    friendly. 

- mergeCountsFromIntegratedSources.py : merges all sources listed in
    				      	integratedSources.conf into
    				      	two data
    				      	files: uniq_drug_hoi_relationships.csv
    				      	and drug-hoi-evidence-data.tsv

- integratedSources.conf : a tab delimitted text file (unix linefeeds)
  			   specifying integrated sources. Each line
  			   lists the name of a source and the path to
  			   the data file containing counts and
  			   linkouts

- uniq_drug_hoi_relationships.csv : data to be loaded into the
  				    drug_HOI_relationship table

- drug-hoi-evidence-data.tsv : data to be loaded into the
    			       drug_HOI_evidence table

---------------------------------------------------------------
NOTES ON 05/12/2015 LOAD
---------------------------------------------------------------

* Sources: 
PUBMED
SEMMED
SPLICER
FDA Adverse Event Reporting System
EU_SPC_ADR


* Total rows available:
PUBMED : 58303
SEMMED : 64959
SPLICER : 287931
FDA Adverse Event Reporting System : 3478558
EU_SPC_ADR : 23920

TOTAL: 3913671

* Rows dropped because of NULL concept ids: 

PUBMED : 0
SEMMED : 0
SPLICER : 339 (0.1%)
FDA Adverse Event Reporting System : 1130346 (32.5%)
EU_SPC_ADR : 0

TOTAL: 1130685  (28.9%)

* Total number of rows after mapping HOI concepts to SNOMED: 

PUBMED : 48118  (decrease of 10185  (21.2%))
SEMMED : 30444 (decrease of 34515 (53.1%)) NOTE: Lot's of MeSH concepts not getting mapped
SPLICER : 263661 (decrease of 24270 (8.4%))  ---- WAS (*increase* of 207481  (72.1%)) -- Probably mostly due to one to many mappings from MedDRA to SNOMED
FDA Adverse Event Reporting System : 1174106  (decrease of 2304452 (66.2%)) - due to NULL concept ids
EU_SPC_ADR : 20806 (decrease of 3114 (13.0%)) ----- WAS (*increase* of 13939 (58.3%)) -- Probably mostly due to one to many mappings from MedDRA to SNOMED

TOTAL: 1537135 (decrease of 2376536 (64.6%) - mostly due to NULLs in the FAERS data)