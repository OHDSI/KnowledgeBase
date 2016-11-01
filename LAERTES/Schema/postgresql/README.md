Scripts to synthesize the evidence source count and linkout data into
tables that can them be loaded into the Schema relational DB model
(that extends the OHDSI Standard Vocab). 

LOADING THE SCHEMA AND DATA INTO THE OHDSI STANDARD VOCABULARY: 

1) Edit integratedSources.conf and the run the script
   mergeCountsFromIntegratedSources.py. This creates the files
   uniq_drug_hoi_relationships.csv and drug-hoi-evidence-data.tsv

2) (if deploying on the release server)
   load uniq_drug_hoi_relationships.csv, drug-hoi-evidence-data.tsv,
   and ohdsiTest3.psql to the /mnt/vol1/inbound folder on the OHDSI
   dev server.

3)
 (DEVELOPMENT --- NOTE: YOU HAVE TO CHANGE TO TABLE PERMISSIONS STATEMENTS FIRST -- SEE 'Altering table permissions' BELOW)
 Within this folder run:
    nohup psql -U <user name> -h 127.0.0.1 -W -d laertes_cdm < ohdsiTest3.psql

(RELEASE)
 ssh to the OHDSI dev server, change to the /mnt/vol1/inbound folder
   and run:
   nohup psql -U <user name> -h 127.0.0.1 -W -d vocabularyv5 < ohdsiTest3.psql

4) Wait - estimated time - more than a couple of hours

5) Run the load scripts in the folder additional-load-scripts using
similar commands to (3) but read rdf2relational.psql for how to create
the data needed to run that script



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

- additional-load-scripts/CONDITION_UNIVERSE.sql : used to generating negative drug-HOI controls - the universe includes those CONDITIONS that have at least one evidence item from some evidence source (as defined in the query) 

- additional-load-scripts/DRUG_UNIVERSE.sql : used to generating negative drug-HOI controls - the universe includes those DRUGS that have at least one evidence item from some evidence source (as defined in the query) 

- additional-load-scripts/PENELOPE_WEBAPI.sql : a table used in the WebAPI to connect roll up and summary drug-HOI data to linkouts

- additional-load-scripts/CONDITIONS_AND_CHILDREN_CONDITIONS.sql : table that assists with roll ups on the conditions table

- additional-load-scripts/POSITIVE_NEGATIVE_CONTROL_BETAS.sql : table that assists with the negative control application

---------------------------------------------------------------
NOTES ON April 1 2016 LOAD (NOTE: MEDLINE UPDATED IN SEPTEMBER 2016 TO FIX BUGS - old an new data shown together below)
---------------------------------------------------------------

* Sources: 
PUBMED
SEMMED
CTD
SPLICER
FDA Adverse Event Reporting System
EU_SPC_ADR


* Total rows available (e.g., cat drug-hoi-counts-with-linkouts-PUBMED-March2016.tsv | cut -f1 | sort | uniq | wc -l):
PUBMED : 79119
SEMMED : 5023
CTD :  503835
SPLICER : 272436
FDA Adverse Event Reporting System : 3766382
EU_SPC_ADR : 26989

TOTAL: 4653784

* Rows dropped because of NULL concept ids: 

PUBMED : 
SEMMED :
CTD : 
SPLICER : 
FDA Adverse Event Reporting System : 
EU_SPC_ADR : 

TOTAL:   (%)

* Total number of rows after mapping HOI concepts to SNOMED: 

laertes_cdm=> select evidence_type, count(distinct drug_hoi_relationship) from drug_hoi_evidence group by evidence_type;
       evidence_type        |  count  
----------------------------+---------
 aers_report_count          | 2753078
 aers_report_prr            | 2753078
 CTD_ChemicalDisease        |  432850
 MEDLINE_MeSH_ClinTrial     |   11035 (April) 15540 (September)
 MEDLINE_MeSH_CR            |   41229 (April) 43506 (September)
 MEDLINE_MeSH_Other         |   67002 (April) 71150 (September)
 MEDLINE_SemMedDB_ClinTrial |     636
 MEDLINE_SemMedDB_CR        |     915
 MEDLINE_SemMedDB_Other     |    2681
 SPL_EU_SPC                 |   24537
 SPL_SPLICER_ADR            |  254738
(11 rows)

Grouping by higher level type:
laertes_cdm=> select count(distinct drug_hoi_relationship) from drug_hoi_evidence  where evidence_type like 'MEDLINE_MeSH%';
count 
-------
 73024 (April) 77395 (September)

laertes_cdm=> select count(distinct drug_hoi_relationship) from drug_hoi_evidence  where evidence_type like 'MEDLINE_SemMedDB%';
 count 
-------
  2813 

laertes_cdm=> select count(distinct drug_hoi_relationship) from drug_hoi_evidence  where evidence_type like 'CTD%';
 count  
--------
 432850

laertes_cdm=> select count(distinct drug_hoi_relationship) from drug_hoi_evidence  where evidence_type like 'aers%';
  count  
---------
 2753078

laertes_cdm=> select count(distinct drug_hoi_relationship) from drug_hoi_evidence  where evidence_type like 'SPL_EU%';
 count 
-------
 24537

laertes_cdm=> select count(distinct drug_hoi_relationship) from drug_hoi_evidence  where evidence_type like 'SPL_SPLICER%';
 count  
--------
 254738 -- Clinical Drug Level

laertes_cdm=> select count(*) from (select distinct ingredient_id, hoi_id  from laertes_summary where report_order = 2 and splicer_count is not null) sub1;
 count
 -------
  89498 -- Ingredient level
  


Totals:
PUBMED : APRIL -- 73024 (decrease of 6095  (7.7%)) ; SEPTEMBER -- 77395 (decrease of 1724 (2.2%))
SEMMED : 2813 (decrease of 2210 (44%)) NOTE: Lot's of MeSH concepts not getting mapped
CTD : 432850 (decrease of 70985  (14.1%)) 
SPLICER : 254738 (decrease of 17698  (6.5%)) 
FDA Adverse Event Reporting System : 2753078  (decrease of 1013304 (26.9%)) 
EU_SPC_ADR : 24537 (decrease of 2452 (9.1%)) 

Examining overlap:

Denominators:
Literature vs spontaneous reporting --
-- denominator
select count(*) from (select distinct ingredient_id, hoi_id from laertes_summary where report_order = 2 and (medline_ct_count is not null or medline_case_count is not null or medline_other_count is not null or ctd_chemical_disease_count is not null or semmeddb_ct_count is not null or semmeddb_case_count is not null or semmeddb_other_count is not null) or (aers_report_count is not null)) sub1; -- 3049743


-- numerator
select count(*) from (select distinct ingredient_id, hoi_id from laertes_summary where report_order = 2 and (medline_ct_count is not null or medline_case_count is not null or medline_other_count is not null or ctd_chemical_disease_count is not null or semmeddb_ct_count is not null or semmeddb_case_count is not null or semmeddb_other_count is not null) and (aers_report_count is not null)) sub1; -- 119293


Product labeling vs spontaneous reporting --
-- denominator:
select count(*) from (select distinct ingredient_id, hoi_id  from laertes_summary where report_order = 2 and (aers_report_count is not null) or (splicer_count is not null or eu_spc_count is not null)) sub1; -- 2702577

-- numerator
select count(*) from (select distinct ingredient_id, hoi_id  from laertes_summary where report_order = 2 and (aers_report_count is not null) and (splicer_count is not null or eu_spc_count is not null)) sub1; -- 87279



Literature vs product labeling --
-- denominator:
select count(*) from (select distinct ingredient_id, hoi_id  from laertes_summary where report_order = 2 and (semmeddb_ct_count is not null or semmeddb_case_count is not null or semmeddb_other_count is not null or medline_ct_count is not null or medline_case_count is not null or medline_other_count is not null or ctd_chemical_disease_count is not null) or (splicer_count is not null or eu_spc_count is not null)) sub1; -- 566379

-- numerator
select count(*) from (select distinct ingredient_id, hoi_id  from laertes_summary where report_order = 2 and (semmeddb_ct_count is not null or semmeddb_case_count is not null or semmeddb_other_count is not null or medline_ct_count is not null or medline_case_count is not null or medline_other_count is not null or ctd_chemical_disease_count is not null) and (splicer_count is not null or eu_spc_count is not null)) sub1; -- 14838


All sources (11 results):
select * from laertes_summary where report_order = 2 and (medline_ct_count is not null or medline_case_count is not null or medline_other_count is not null) and ctd_chemical_disease_count is not null and splicer_count is not null and eu_spc_count is not null and (semmeddb_ct_count is not null or semmeddb_case_count is not null or semmeddb_other_count is not null) and (aers_report_count is not null or prr is not null);

Combinations of lit, product labeling, and spontaneous reporting

All three:
-- denominator
select count(*) from (select distinct ingredient_id, hoi_id  from laertes_summary where report_order = 2 and ((medline_ct_count is not null or medline_case_count is not null or medline_other_count is not null or ctd_chemical_disease_count is not null or semmeddb_ct_count is not null or semmeddb_case_count is not null or semmeddb_other_count is not null) or (splicer_count is not null or eu_spc_count is not null) or (aers_report_count is not null))) sub1; -- 3057406

--numerator
select count(*) from (select distinct ingredient_id, hoi_id  from laertes_summary where report_order = 2 and ((medline_ct_count is not null or medline_case_count is not null or medline_other_count is not null or ctd_chemical_disease_count is not null or semmeddb_ct_count is not null or semmeddb_case_count is not null or semmeddb_other_count is not null) and (splicer_count is not null or eu_spc_count is not null) and (aers_report_count is not null))) sub1; -- 14295



------------------
DEPRECATED (does not use distinct, uses PRR which is unnecessary): Literature and spontaneous reporting:
select count(*) from laertes_summary where report_order = 2 and (medline_ct_count is not null or medline_case_count is not null or medline_other_count is not null or ctd_chemical_disease_count is not null or semmeddb_ct_count is not null or semmeddb_case_count is not null or semmeddb_other_count is not null) and (aers_report_count is not null or prr is not null);
-- 117190 (April)  -- 119293 (September)

DEPRECATED (does not use distinct, uses PRR which is unnecessary): Literature and labeling:
select count(*) from laertes_summary where report_order = 2 and (medline_ct_count is not null or medline_case_count is not null or medline_other_count is not null or ctd_chemical_disease_count is not null or semmeddb_ct_count is not null or semmeddb_case_count is not null or semmeddb_other_count is not null) and (splicer_count is not null or eu_spc_count is not null);
-- 14182 (April) -- 14838 (September)

DEPRECATED (does not use distinct, uses PRR which is unnecessary): All
select count(*) from laertes_summary where report_order = 2 and (medline_ct_count is not null or medline_case_count is not null or medline_other_count is not null or ctd_chemical_disease_count is not null or semmeddb_ct_count is not null or semmeddb_case_count is not null or semmeddb_other_count is not null) and (splicer_count is not null or eu_spc_count is not null) and (aers_report_count is not null or prr is not null);
-- 13639 (April) -- 14295 (September)

-----------------------------------------------------------------------------
------------------------------  ARCHIVED NOTES ------------------------------

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