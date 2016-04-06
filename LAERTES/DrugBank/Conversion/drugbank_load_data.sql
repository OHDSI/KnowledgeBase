--------------------------------------------------------------------
-- The purpose of this file is to load the tables with
-- the data generated from drugbank_xml_to_sql.py.
--
-- Author: Charles Kronk
-- 2016
--
----------------------------

--
-- Note that the absolute path to each .rrf file should be
-- used in each copy statement. Further, \echo does not function
-- with PostgreSQL 9.5 when used in PgAdmin III's SQL query
-- function. In this case, all \echo statements should be
-- deleted and all \copy statements should have the "\" removed.
-- 

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drugs FROM 'DRUGBANK_DRUGS.rrf' (DELIMITER '|', FORMAT TEXT);
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_alt_ids FROM 'DRUGBANK_DRUG_ALT_IDS.rrf' DELIMITER '|' CSV;
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_groups FROM 'DRUGBANK_DRUG_GROUPS.rrf' DELIMITER '|' CSV;
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
CREATE TEMP TABLE tmp_table 
ON COMMIT DROP
AS
SELECT * 
FROM drug_general_references
WITH NO DATA;
\copy tmp_table FROM 'DRUGBANK_DRUG_GEN_REFS.rrf' (DELIMITER '|', FORMAT TEXT);
INSERT INTO drug_general_references
SELECT DISTINCT ON (general_reference, primary_drugbank_id) *
FROM tmp_table
ORDER BY (primary_drugbank_id);
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_volumes_of_distribution FROM 'DRUGBANK_DRUG_VOL_DIST.rrf' DELIMITER '|' CSV;
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
CREATE TEMP TABLE tmp_table 
ON COMMIT DROP
AS
SELECT * 
FROM drug_clearances
WITH NO DATA;
\copy tmp_table FROM 'DRUGBANK_DRUG_CLEARANCES.rrf' DELIMITER '|' CSV;
INSERT INTO drug_clearances
SELECT DISTINCT ON (clearance, primary_drugbank_id) *
FROM tmp_table WHERE clearance IS NOT NULL
ORDER BY (primary_drugbank_id);
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_classifications FROM 'DRUGBANK_DRUG_CLASSIFICATIONS.rrf' DELIMITER '|' CSV;
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_classification_alt_parents FROM 'DRUGBANK_DRUG_CLASSIFICATION_ALT_PARENTS.rrf' DELIMITER '|' CSV;
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_classification_substituents FROM 'DRUGBANK_DRUG_CLASSIFICATION_SUBSTIT.rrf' DELIMITER '|' CSV;
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_salts FROM 'DRUGBANK_DRUG_SALTS.rrf' DELIMITER '|' CSV;
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_synonyms FROM 'DRUGBANK_DRUG_SYN.rrf' DELIMITER '|' CSV;
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_products FROM 'DRUGBANK_DRUG_PROD.rrf' DELIMITER '|' CSV;
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_international_brands FROM 'DRUGBANK_DRUG_INT_BRANDS.rrf' DELIMITER '|' CSV;
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_mixtures FROM 'DRUGBANK_DRUG_MIX.rrf' DELIMITER '|' CSV;
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_packagers FROM 'DRUGBANK_DRUG_PACK.rrf' DELIMITER '|' CSV;
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_manufacturers FROM 'DRUGBANK_DRUG_MANUFACTURERS.rrf' DELIMITER '|' CSV;
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_prices FROM 'DRUGBANK_DRUG_PRICES.rrf' DELIMITER '|' CSV;
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_costs FROM 'DRUGBANK_DRUG_COSTS.rrf' DELIMITER '|' CSV;
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_categories FROM 'DRUGBANK_DRUG_CATEGORIES.rrf' DELIMITER '|' CSV;
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_mesh_ids FROM 'DRUGBANK_DRUG_MESH.rrf' DELIMITER '|' CSV;
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_affected_organisms FROM 'DRUGBANK_DRUG_AFFECTED_ORGANISMS.rrf' DELIMITER '|' CSV;
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_dosages FROM 'DRUGBANK_DRUG_DOSAGES.rrf' DELIMITER '|' CSV;
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_atc_codes FROM 'DRUGBANK_DRUG_ATC_CODES.rrf' DELIMITER '|' CSV;
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_atc_code_levels FROM 'DRUGBANK_DRUG_ATC_CODE_LVL.rrf' DELIMITER '|' CSV;
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_ahfs_codes FROM 'DRUGBANK_DRUG_AHFS.rrf' DELIMITER '|' CSV;
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_patents FROM 'DRUGBANK_DRUG_PATENTS.rrf' DELIMITER '|' CSV;
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_food_interactions FROM 'DRUGBANK_DRUG_FOOD_INT.rrf' DELIMITER '|' CSV;
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_drug_interactions FROM 'DRUGBANK_DRUG_DRUG_INT.rrf' DELIMITER '|' CSV;
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_sequences FROM 'DRUGBANK_DRUG_SEQ.rrf' (DELIMITER '|', FORMAT TEXT);
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_properties FROM 'DRUGBANK_DRUG_PROPS.rrf' (DELIMITER '|', FORMAT TEXT);
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_external_identifiers FROM 'DRUGBANK_DRUG_EXT_IDS.rrf' DELIMITER '|' CSV;
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_external_links FROM 'DRUGBANK_DRUG_EXT_LINKS.rrf' DELIMITER '|' CSV;
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_pathways FROM 'DRUGBANK_DRUG_PATHWAYS.rrf' DELIMITER '|' CSV;
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_reactions FROM 'DRUGBANK_DRUG_RXNS.rrf' DELIMITER '|' CSV;
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_reaction_elements FROM 'DRUGBANK_DRUG_RXN_EL.rrf' DELIMITER '|' CSV;
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_reaction_enzymes FROM 'DRUGBANK_DRUG_RXN_ENZYMES.rrf' DELIMITER '|' CSV;
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_snp_effects FROM 'DRUGBANK_DRUG_SNP_EFF.rrf' DELIMITER '|' CSV;
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_snp_adverse_drug_reactions FROM 'DRUGBANK_DRUG_SNP_ADV_DRUG_RXNS.rrf' DELIMITER '|' CSV;
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_enzymes FROM 'DRUGBANK_DRUG_ENZYMES.rrf' DELIMITER '|' CSV;
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_enzyme_actions FROM 'DRUGBANK_DRUG_ENZYME_ACTIONS.rrf' DELIMITER '|' CSV;
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
CREATE TEMP TABLE tmp_table 
ON COMMIT DROP
AS
SELECT * 
FROM drug_enzyme_references
WITH NO DATA;
\copy tmp_table FROM 'DRUGBANK_DRUG_ENZYME_REFS.rrf' DELIMITER '|' CSV;
INSERT INTO drug_enzyme_references
SELECT DISTINCT ON (reference, id, primary_drugbank_id) *
FROM tmp_table
ORDER BY (id);
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_enzyme_polypeptides FROM 'DRUGBANK_DRUG_ENZYME_POLYPEPTIDES.rrf' DELIMITER '|' NULL AS '';
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_enzyme_polypeptide_transmembrane_regions FROM 'DRUGBANK_DRUG_ENZYME_POLYPEPTIDE_TRANSMEM_REGIONS.rrf' DELIMITER '|' CSV;
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_enzyme_polypeptide_external_identifiers FROM 'DRUGBANK_DRUG_ENZYME_EXT_IDS.rrf' DELIMITER '|' CSV;
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_enzyme_polypeptide_synonyms FROM 'DRUGBANK_DRUG_ENZYME_SYN.rrf' DELIMITER '|' CSV;
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_enzyme_polypeptide_amino_acid_sequences FROM 'DRUGBANK_DRUG_ENZYME_AA_SEQ.rrf' (DELIMITER '|', FORMAT TEXT);
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_enzyme_polypeptide_gene_sequences FROM 'DRUGBANK_DRUG_ENZYMES_GENE_SEQ.rrf' (DELIMITER '|', FORMAT TEXT);
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_enzyme_polypeptide_pfams FROM 'DRUGBANK_DRUG_ENZYME_PFAMS.rrf' DELIMITER '|' CSV;
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_enzyme_polypeptide_go_classifiers FROM 'DRUGBANK_DRUG_ENZYME_GO_CLASSIFIERS.rrf' DELIMITER '|' CSV;
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_targets FROM 'DRUGBANK_DRUG_TARGETS.rrf' DELIMITER '|' CSV;
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_target_actions FROM 'DRUGBANK_DRUG_TARGET_ACTIONS.rrf' DELIMITER '|' CSV;
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
CREATE TEMP TABLE tmp_table 
ON COMMIT DROP
AS
SELECT * 
FROM drug_target_references
WITH NO DATA;
\copy tmp_table FROM 'DRUGBANK_DRUG_TARGET_REFS.rrf' DELIMITER '|' CSV;
INSERT INTO drug_target_references
SELECT DISTINCT ON (reference, id, primary_drugbank_id) *
FROM tmp_table
ORDER BY (id);
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_target_polypeptides FROM 'DRUGBANK_DRUG_TARGET_POLYPEPTIDES.rrf' DELIMITER '|' NULL AS '';
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_target_polypeptide_transmembrane_regions FROM 'DRUGBANK_DRUG_TARGET_POLYPEPTIDE_TRANSMEM_REGIONS.rrf' DELIMITER '|' CSV;
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_target_polypeptide_external_identifiers FROM 'DRUGBANK_DRUG_TARGET_EXT_IDS.rrf' DELIMITER '|' CSV;
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_target_polypeptide_synonyms FROM 'DRUGBANK_DRUG_TARGET_SYN.rrf' DELIMITER '|' CSV;
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_target_polypeptide_amino_acid_sequences FROM 'DRUGBANK_DRUG_TARGET_AA_SEQ.rrf' (DELIMITER '|', FORMAT TEXT);
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_target_polypeptide_gene_sequences FROM 'DRUGBANK_DRUG_TARGETS_GENE_SEQ.rrf' (DELIMITER '|', FORMAT TEXT);
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_target_polypeptide_pfams FROM 'DRUGBANK_DRUG_TARGET_PFAMS.rrf' DELIMITER '|' CSV;
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_target_polypeptide_go_classifiers FROM 'DRUGBANK_DRUG_TARGET_GO_CLASSIFIERS.rrf' DELIMITER '|' CSV;
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_carriers FROM 'DRUGBANK_DRUG_CARRIERS.rrf' DELIMITER '|' CSV;
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_carrier_actions FROM 'DRUGBANK_DRUG_CARRIER_ACTIONS.rrf' DELIMITER '|' CSV;
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_carrier_references FROM 'DRUGBANK_DRUG_CARRIER_REFS.rrf' DELIMITER '|' CSV;
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_carrier_polypeptides FROM 'DRUGBANK_DRUG_CARRIER_POLYPEPTIDES.rrf' DELIMITER '|' CSV;
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_carrier_polypeptide_transmembrane_regions FROM 'DRUGBANK_DRUG_CARRIER_POLYPEPTIDE_TRANSMEM_REGIONS.rrf' DELIMITER '|' CSV;
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_carrier_polypeptide_external_identifiers FROM 'DRUGBANK_DRUG_CARRIER_EXT_IDS.rrf' DELIMITER '|' CSV;
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_carrier_polypeptide_synonyms FROM 'DRUGBANK_DRUG_CARRIER_SYN.rrf' DELIMITER '|' CSV;
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_carrier_polypeptide_amino_acid_sequences FROM 'DRUGBANK_DRUG_CARRIER_AA_SEQ.rrf' (DELIMITER '|', FORMAT TEXT);
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_carrier_polypeptide_gene_sequences FROM 'DRUGBANK_DRUG_CARRIERS_GENE_SEQ.rrf' (DELIMITER '|', FORMAT TEXT);
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_carrier_polypeptide_pfams FROM 'DRUGBANK_DRUG_CARRIER_PFAMS.rrf' DELIMITER '|' CSV;
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_carrier_polypeptide_go_classifiers FROM 'DRUGBANK_DRUG_CARRIER_GO_CLASSIFIERS.rrf' DELIMITER '|' CSV;
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_transporters FROM 'DRUGBANK_DRUG_TRANSPORTERS.rrf' DELIMITER '|' CSV;
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_transporter_actions FROM 'DRUGBANK_DRUG_TRANSPORTER_ACTIONS.rrf' DELIMITER '|' CSV;
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
CREATE TEMP TABLE tmp_table 
ON COMMIT DROP
AS
SELECT * 
FROM drug_transporter_references
WITH NO DATA;
\copy tmp_table FROM 'DRUGBANK_DRUG_TRANSPORTER_REFS.rrf' DELIMITER '|' CSV;
INSERT INTO drug_transporter_references
SELECT DISTINCT ON (reference, id, primary_drugbank_id) *
FROM tmp_table
ORDER BY (id);
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_transporter_polypeptides FROM 'DRUGBANK_DRUG_TRANSPORTER_POLYPEPTIDES.rrf' DELIMITER '|' NULL AS '';
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_transporter_polypeptide_transmembrane_regions FROM 'DRUGBANK_DRUG_TRANSPORTER_POLYPEPTIDE_TRANSMEM_REGIONS.rrf' DELIMITER '|' CSV;
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_transporter_polypeptide_external_identifiers FROM 'DRUGBANK_DRUG_TRANSPORTER_EXT_IDS.rrf' DELIMITER '|' CSV;
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_transporter_polypeptide_external_identifiers FROM 'DRUGBANK_DRUG_TRANSPORTER_SYN.rrf' DELIMITER '|' CSV;
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_transporter_polypeptide_amino_acid_sequences FROM 'DRUGBANK_DRUG_TRANSPORTER_AA_SEQ.rrf' (DELIMITER '|', FORMAT TEXT);
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_transporter_polypeptide_gene_sequences FROM 'DRUGBANK_DRUG_TRANSPORTERS_GENE_SEQ.rrf' (DELIMITER '|', FORMAT TEXT);
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_transporter_polypeptide_pfams FROM 'DRUGBANK_DRUG_TRANSPORTER_PFAMS.rrf' DELIMITER '|' CSV;
COMMIT;

\echo 'Starting transaction'
START TRANSACTION;
\echo 'Loading data into drugs from file '
\copy drug_transporter_polypeptide_go_classifiers FROM 'DRUGBANK_DRUG_TRANSPORTER_GO_CLASSIFIERS.rrf' DELIMITER '|' CSV;
COMMIT;

\echo 'Done copying relevant tables to the schema.'