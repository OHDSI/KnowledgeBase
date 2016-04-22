This folder holds scripts that extend the LAERTES relational database
while being still fully a part of the project (e.g., the DrugBank load
scripts extend LAERTES but depend on an external data source). These
fall into three categories:

------------------------------------------------------------
CATEGORY 1
------------------------------------------------------------

Scripts that add data to the LAERTES relational model so that it is
possible to go from the drug_hoi_evidence table (coded as RxNorm and
SNOMED) to a) the original drug and HOI concepts (maybe from MeSH or
MeddRA), and b) the documents that are the target of annotation.

```
Loading these scripts:
-(DEVELOPMENT --- NOTE: YOU HAVE TO CHANGE TO TABLE PERMISSIONS STATEMENTS FIRST -- SEE 'Altering table permissions' BELOW)
  Within this folder run:
   $ nohup psql -U <user name> -h 127.0.0.1 -W -d laertes_cdm < rdf2relational.psql

-(RELEASE --- NOTE: YOU HAVE TO CHANGE TO TABLE PERMISSIONS STATEMENTS FIRST!)
   ssh to the OHDSI dev server, change to the /mnt/vol1/inbound folder
   and run:
    $ nohup psql -U <user name> -h 127.0.0.1 -W -d vocabularyv5 < rdf2relational.psql

- rdf2relational.psql -- Adds tables which originally appeared as RDF as open annotation data which enables queries of the open annotation data directly within the relational database e.g.:

  SELECT * FROM adr_annotation INNER JOIN adr_body ON adr_annotation.has_body = adr_body.adr_body_item
     INNER JOIN target ON adr_annotation.has_target = target.target_item
  LIMIT 10;

This script requires several SPARQL queries to be ran on the command
line (see the comments at the header of the script). It also requires that the program 

With the mapping file loaded, queries can cross from drug_hoi_evidence to the open annotation data. For example:
--
 EX 1: Get back data associated with a specific OA using a linkout
--
  (Development environment) 
   SELECT * FROM drug_hoi_evidence INNER JOIN linkout_to_adr_annotation ON evidence_linkout = linkout
   WHERE linkout = 'http://130.49.206.139/l/index.php?id=ctd-1';
--
  (Release environment) 
   SELECT * FROM drug_hoi_evidence INNER JOIN linkout_to_adr_annotation ON evidence_linkout = linkout
   WHERE linkout = 'http://dbmi-icode-01.dbmi.pitt.edu/l/index.php?id=ctd-1';
--
 EX 2: Get back all OA data associated with a drug_hoi_evidence record 
--
  (Development environment -- difference is the base IP of the linkout)
  WITH oa_data AS (
  SELECT * FROM adr_annotation INNER JOIN adr_body ON adr_annotation.has_body = adr_body.adr_body_item
     INNER JOIN target ON adr_annotation.has_target = target.target_item
  ) 
  SELECT * FROM drug_hoi_evidence INNER JOIN linkout_to_adr_annotation ON drug_hoi_evidence.evidence_linkout = linkout_to_adr_annotation.linkout
    INNER JOIN oa_data ON linkout_to_adr_annotation.adr_annotation_item = oa_data.adr_annotation_item
  WHERE linkout_to_adr_annotation.linkout = 'http://130.49.206.139/l/index.php?id=ctd-1';
--
--
  (Release environment)
  WITH oa_data AS (
  SELECT * FROM adr_annotation INNER JOIN adr_body ON adr_annotation.has_body = adr_body.adr_body_item
    INNER JOIN target ON adr_annotation.has_target = target.target_item
  ) 
  SELECT * FROM drug_hoi_evidence INNER JOIN linkout_to_adr_annotation ON drug_hoi_evidence.evidence_linkout = linkout_to_adr_annotation.linkout
    INNER JOIN oa_data ON linkout_to_adr_annotation.adr_annotation_item = oa_data.adr_annotation_item
  WHERE linkout_to_adr_annotation.linkout = 'http://dbmi-icode-01.dbmi.pitt.edu/l/index.php?id=ctd-1';
--
```

------------------------------------------------------------
CATEGORY 2
------------------------------------------------------------

```
Scripts that are useful for analyses that leverage the LAERTES
evidence base to infer positive and negative controls. These scripts
depend on a concept called "LAERTES UNIVERSE" which is the set of
drugs and HOIs that have evidence in all three sources - spontaneous
reporting, literature, and product labeling.

- DRUG_UNIVERSE.sql : pre-processes ingredients that contain enough
                      evidence to be part of the LAERTES UNIVERSE

- CONDITION_UNIVERSE.sql : pre-processes conditions that contain enough
                          evidence to be part of the LAERTES UNIVERSE

- CONDITIONS_AND_CHILDREN_CONDITIONS.sql : This program pre-processes
                                           for every conditions what
                                           what descendant concepts as
                                           associated to that in the
                                           OMOP Vocabulary

- POSITIVE_NEGATIVE_CONTROL_BETAS.sql : Saves the betas generated from
                                        the model trying to tell apart
                                        drugs that cause an HOI
                                        (positive controls) and drugs
                                        that do not cause an HOI
                                        (negative controls).

-(DEVELOPMENT --- NOTE: YOU HAVE TO CHANGE TO TABLE PERMISSIONS STATEMENTS FIRST!)
  Within this folder run:
   $ nohup psql -U <user name> -h 127.0.0.1 -W -d  laertes_cdm <  DRUG_UNIVERSE.sql
   $ nohup psql -U <user name> -h 127.0.0.1 -W -d  laertes_cdm <  CONDITION_UNIVERSE.sql
   $ nohup psql -U <user name> -h 127.0.0.1 -W -d  laertes_cdm <  CONDITIONS_AND_CHILDREN_CONDITIONS.sql
   $ nohup psql -U <user name> -h 127.0.0.1 -W -d  laertes_cdm <  POSITIVE_NEGATIVE_CONTROL_BETAS.sql

-(RELEASE --- NOTE: YOU HAVE TO CHANGE TO TABLE PERMISSIONS STATEMENTS FIRST!)
   ssh to the OHDSI dev server, change to the /mnt/vol1/inbound folder
   and run:
    $ nohup psql -U <user name> -h 127.0.0.1 -W -d vocabularyv5 < DRUG_UNIVERSE.sql
    $ nohup psql -U <user name> -h 127.0.0.1 -W -d vocabularyv5 < CONDITION_UNIVERSE.sql
    $ nohup psql -U <user name> -h 127.0.0.1 -W -d vocabularyv5 <  CONDITIONS_AND_CHILDREN_CONDITIONS.sql
    $ nohup psql -U <user name> -h 127.0.0.1 -W -d vocabularyv5 <  POSITIVE_NEGATIVE_CONTROL_BETAS.sql
```

------------------------------------------------------------
CATEGORY 3
------------------------------------------------------------
```
Scripts that enhance the WebAPI but that depend on the tables in categories 1 or 2 (run these last)

- PENELOPE_WEBAPI.sql -- This creates a table that organizes the
		      -- LAERTES evidence into a summary with data
		      -- rolled up to the ingredient level and with
		      -- all linkouts associated with a drug-HOI
		      -- association in a pipe-delimited variable.

-(DEVELOPMENT --- NOTE: YOU HAVE TO CHANGE TO TABLE PERMISSIONS STATEMENTS FIRST -- SEE 'Altering table permissions' BELOW)
  Within this folder run:
   $ nohup psql -U <user name> -h 127.0.0.1 -W -d  laertes_cdm <  PENELOPE_WEBAPI.sql

-(RELEASE)
   ssh to the OHDSI dev server, change to the /mnt/vol1/inbound folder
   and run:
    $ nohup psql -U <user name> -h 127.0.0.1 -W -d vocabularyv5 < PENELOPE_WEBAPI.sql

```