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
NOTES ON 05/05/2015 LOAD
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
FDA Adverse Event Reporting System : 4860068
EU_SPC_ADR : 23920

TOTAL: 5295181

* Rows dropped because of NULL concept ids: 

PUBMED : 0
SEMMED : 0
SPLICER : 339 (0.1%)
FDA Adverse Event Reporting System : 1564856 (32.2%)
EU_SPC_ADR : 0

TOTAL: 1565195  (29.6%)

* Total number of rows after mapping HOI concepts to SNOMED: 

PUBMED : 49214  (decrease of 9089 (18.5%))
SEMMED : 39778 (decrease of 25181 (38.8%)) -- NOTE: many concepts were assumed to be SNOMED that are really un-mappable MeSH - all data with non-SNOMED HOIs needs to be dropped from all of the tables where they exist
SPLICER : 495412 (*increase* of 207481  (72.1%)) -- Probably mostly due to one to many mappings from MedDRA to SNOMED
FDA Adverse Event Reporting System : 3295212  (decrease of  (32.2%)) - due to NULL concept ids
EU_SPC_ADR : 37859 (*increase* of 13939 (58.3%)) -- Probably mostly due to one to many mappings from MedDRA to SNOMED

TOTAL: 3917475