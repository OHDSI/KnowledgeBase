copy-schema-load-script-to-OHDSI:
	scp ohdsiTest3.psql  rich@laertes.ohdsi.org:/mnt/vol1/inbound/

copy-relational-schema-and-data-to-OHDSI:
	scp ohdsiTest3.psql drug-hoi-evidence-data.tsv uniq_drug_hoi_relationships.csv rich@laertes.ohdsi.org:/mnt/vol1/inbound/

copy-test-reference-data-to-OHDSI:
	scp test-reference-data/loadTestDruHOIUniverse.psql test-reference-data/LU_REF_SET_HOI_DEF.csv test-reference-data/LU_REF_SET_DRUG_HOI_DEF.csv test-reference-data/LU_AZ_CERT.csv rich@laertes.ohdsi.org:/mnt/vol1/inbound/
