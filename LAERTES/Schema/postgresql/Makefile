copy-schema-load-script-to-OHDSI:
	scp ohdsiTest3.psql  rich@laertes.ohdsi.org:/mnt/vol1/inbound/

copy-relational-schema-and-data-to-OHDSI:
	scp ohdsiTest3.psql drug-hoi-evidence-data.tsv uniq_drug_hoi_relationships.csv rich@laertes.ohdsi.org:/mnt/vol1/inbound/

copy-test-reference-data-to-OHDSI:
	scp test-reference-data/LU_DRUG_HOI_DEF.csv test-reference-data/LU_HOI_DEF.csv rich@laertes.ohdsi.org:/mnt/vol1/inbound/
