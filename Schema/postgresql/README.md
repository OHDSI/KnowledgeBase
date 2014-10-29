Scripts to synthesize the evidence source count and linkout data into
tables that can them be loaded into the Schema relational DB model
(that extends the OHDSI Standard Vocab). 

LOADING THE SCHEMA AND DATA INTO THE OHDSI STANDARD VOCABULARY: 

1) Edit integratedSources.conf and the run the script
   'mergeCountsFromIntegratedSources.py'. This creates the files
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