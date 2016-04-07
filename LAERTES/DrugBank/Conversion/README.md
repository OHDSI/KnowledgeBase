Scripts to load DrugBank into a schema that can be queried alongside
of OHDSI databases. For example, one can retrieve all drug targets and
associated literature references by omop concept id like this:

 SELECT concept.concept_id, concept.concept_name, dbomap.primary_drugbank_id, dbtr.target_id, drugbank.drug_targets.name, dbtr.reference
 FROM drugbank.drugbank_to_omop_mapping dbomap INNER JOIN concept on dbomap.concept_id = concept.concept_id
   INNER JOIN drugbank.drug_target_references dbtr on dbtr.primary_drugbank_id = dbomap.primary_drugbank_id
   INNER JOIN drugbank.drug_targets on dbtr.target_id = drugbank.drug_targets.target_id
 LIMIT 10;

---------
SCRIPTS:
---------

- drugbank_xml_to_sql.py : (requires Python 3) A script to convert all of the data in drugbank.xml to pipe-delimited files that can be loaded into a relational database (currently Postgres). To run it, download the newest DrugBank data from http://www.drugbank.ca/downloads and run "python drugbank_xml_to_sql.py"

- drugbank_schema.sql : schema creation script To run it:

   1. Create a scheme "drugbank" in your database

   2. Edit the file to change permissions if needed depending on your database configuration (see GRANT lines toward the end of the file)

   3. Run something like:
       $ nohup psql -U <USERNAME> -h 127.0.0.1 -W -d <DATABASE> < drugbank_schema.sql > log-create-drugbank-schema.txt

- drugbank_load_data.sql : NOTE: rxnorm-drugbank-omop-mapping-CLEANED.tsv needs to be copied into the same folder as this script from the LAERTES github project under terminology-mappings/RxNORM-to-UNII-PreferredName-To-DrugBank/. Run something like:
       $ nohup psql -U <USERNAME> -h 127.0.0.1 -W -d <DATABASE> < drugbank_load_data.sql > log-drugbank-load.txt




