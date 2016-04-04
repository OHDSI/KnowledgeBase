--
-- The purpose of this file is to create the tables into which
-- the data generated from drugbank_xml_to_sql.py can be loaded.
--
--

--  Use XPATH Command line with Raptor to parse out fields and find max lengths (make sure to pad).

-- Remove secondary foreign keys if POSTGRESQL doesn't create indices.
-- -- mysql_indexes.sql

DROP TABLE IF EXISTS drugs CASCADE;
CREATE TABLE drugs
(
	primary_drugbank_id		VARCHAR(10) NOT NULL PRIMARY KEY,
	name					VARCHAR(50),
	description				VARCHAR(2000) NOT NULL,
	cas_number				VARCHAR(50),
	synthesis_reference		VARCHAR(1000),
	indication				VARCHAR(1000),
	pharmacodynamics		VARCHAR(2000),
	mechanism_of_action		VARCHAR(1000),
	toxicity				VARCHAR(1000),
	metabolism				VARCHAR(1000),
	absorption				VARCHAR(200),
	half_life				VARCHAR(100),
	protein_binding			VARCHAR(500),
	route_of_elimination	VARCHAR(1000),
	drug_type				VARCHAR(20),
	created					DATE,
	updated					DATE
);

DROP TABLE IF EXISTS drug_alt_ids CASCADE;
CREATE TABLE drug_alt_ids
(
	secondary_drugbank_id	VARCHAR(15) NOT NULL PRIMARY KEY,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	FOREIGN KEY (primary_drugbank_id)
		REFERENCES drugs(primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_groups CASCADE;
CREATE TABLE drug_groups
(
	drug_group				VARCHAR(50) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	PRIMARY KEY (drug_group, primary_drugbank_id),
	FOREIGN KEY (primary_drugbank_id)
		REFERENCES drugs(primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_general_references CASCADE;
CREATE TABLE drug_general_references
(
	general_reference		VARCHAR(1000) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	PRIMARY KEY (general_reference, primary_drugbank_id),
	FOREIGN KEY (primary_drugbank_id)
		REFERENCES drugs(primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_volumes_of_distribution CASCADE;
CREATE TABLE drug_volumes_of_distribution
(
	volume_of_distribution	VARCHAR(100) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	PRIMARY KEY (volume_of_distribution, primary_drugbank_id),
	FOREIGN KEY (primary_drugbank_id)
		REFERENCES drugs(primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_clearances CASCADE;
CREATE TABLE drug_clearances
(
	clearance				VARCHAR(100) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	PRIMARY KEY (clearance, primary_drugbank_id),
	FOREIGN KEY (primary_drugbank_id)
		REFERENCES drugs(primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_classifications CASCADE;
CREATE TABLE drug_classifications
(
	primary_drugbank_id		VARCHAR(10) NOT NULL PRIMARY KEY,
	description				VARCHAR(1000),
	direct_parent			VARCHAR(100),
	kingdom					VARCHAR(100),
	superclass				VARCHAR(100),
	drug_class				VARCHAR(100),
	subclass				VARCHAR(100),
	FOREIGN KEY (primary_drugbank_id)
		REFERENCES drugs(primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_classification_alt_parents CASCADE;
CREATE TABLE drug_classification_alt_parents
(
	alternative_parent		VARCHAR(100) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	PRIMARY KEY (alternative_parent, primary_drugbank_id),
	FOREIGN KEY (primary_drugbank_id)
		REFERENCES drugs(primary_drugbank_id)	
);

DROP TABLE IF EXISTS drug_classification_substituents CASCADE;
CREATE TABLE drug_classification_substituents
(
	substituent				VARCHAR(100) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	PRIMARY KEY (substituent, primary_drugbank_id),
	FOREIGN KEY (primary_drugbank_id)
		REFERENCES drugs(primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_salts CASCADE;
CREATE TABLE drug_salts
(
	primary_drugbank_id_salt	VARCHAR(10) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	name					VARCHAR(100) NOT NULL,
	cas_number				VARCHAR(50),
	inchikey				VARCHAR(100),
	PRIMARY KEY (primary_drugbank_id_salt, primary_drugbank_id),	
	FOREIGN KEY (primary_drugbank_id)
		REFERENCES drugs(primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_synonyms CASCADE;
CREATE TABLE drug_synonyms
(
	drug_synonym			VARCHAR(50) NOT NULL,
	synonym_language		VARCHAR(50),
	coder					VARCHAR(50),
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	PRIMARY KEY (drug_synonym, primary_drugbank_id),	
	FOREIGN KEY (primary_drugbank_id)
		REFERENCES drugs(primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_products CASCADE;
CREATE TABLE drug_products
(
	name					VARCHAR(20) NOT NULL PRIMARY KEY,
	ndc_id					VARCHAR(20),
	ndc_product_code		VARCHAR(20),
	dpd_id					VARCHAR(20),
	started_marketing_on	DATE,
	ended_marketing_on		DATE,
	dosage_form				VARCHAR(50),
	strength				VARCHAR(20),
	route					VARCHAR(50),
    fda_application_number  VARCHAR(50),
	generic					BOOLEAN,
	over_the_counter		BOOLEAN,
	approved				BOOLEAN,
	country					VARCHAR(100),
	source					VARCHAR(10),
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	FOREIGN KEY (primary_drugbank_id)
		REFERENCES drugs(primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_international_brands CASCADE;
CREATE TABLE drug_international_brands
(
	name					VARCHAR(50) NOT NULL,
	company					VARCHAR(100) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	PRIMARY KEY (name, company, primary_drugbank_id),
	FOREIGN KEY (primary_drugbank_id)
		REFERENCES drugs(primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_mixtures CASCADE;
CREATE TABLE drug_mixtures
(
	name					VARCHAR(50) NOT NULL,
    ingredients             VARCHAR(1000) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	PRIMARY KEY (name, primary_drugbank_id),
	FOREIGN KEY (primary_drugbank_id)
		REFERENCES drugs(primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_packagers CASCADE;
CREATE TABLE drug_packagers
(
	name					VARCHAR(50) NOT NULL,
	url						VARCHAR(2083),
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	PRIMARY KEY (name, primary_drugbank_id),
	FOREIGN KEY (primary_drugbank_id)
		REFERENCES drugs(primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_manufacturers CASCADE;
CREATE TABLE drug_manufacturers
(
	name					VARCHAR(50) NOT NULL,
	generic					BOOLEAN,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	PRIMARY KEY (name, primary_drugbank_id),
	FOREIGN KEY (primary_drugbank_id)
		REFERENCES drugs(primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_prices CASCADE;
CREATE TABLE drug_prices
(
	description				VARCHAR(100) NOT NULL,
	unit					VARCHAR(20) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	PRIMARY KEY (description, unit, primary_drugbank_id),
	FOREIGN KEY (primary_drugbank_id)
		REFERENCES drugs(primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_costs CASCADE;
CREATE TABLE drug_costs
(
	cost					NUMERIC NOT NULL			CHECK (cost > 0),
	currency				VARCHAR(20) NOT NULL,
	description				VARCHAR(100) NOT NULL,
	unit					VARCHAR(20) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	PRIMARY KEY (cost, currency, description, unit, primary_drugbank_id),
	FOREIGN KEY (description, unit, primary_drugbank_id)
		REFERENCES drug_prices(description, unit, primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_categories CASCADE;
CREATE TABLE drug_categories
(
	name					VARCHAR(100) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	PRIMARY KEY (name, primary_drugbank_id),
	FOREIGN KEY (primary_drugbank_id)
		REFERENCES drugs(primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_mesh_ids CASCADE;
CREATE TABLE drug_mesh_ids
(
	mesh_id					VARCHAR(100) NOT NULL,
	name					VARCHAR(100) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	PRIMARY KEY (mesh_id, name, primary_drugbank_id),
	FOREIGN KEY (name, primary_drugbank_id)
		REFERENCES drug_categories(name, primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_affected_organisms CASCADE;
CREATE TABLE drug_affected_organisms
(
	name					VARCHAR(50) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	PRIMARY KEY (name, primary_drugbank_id),
	FOREIGN KEY (primary_drugbank_id)
		REFERENCES drugs(primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_dosages CASCADE;
CREATE TABLE drug_dosages
(
	form					VARCHAR(50) NOT NULL,
	route					VARCHAR(100) NOT NULL,
	strength				VARCHAR(50) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	PRIMARY KEY (form, route, strength, primary_drugbank_id),
	FOREIGN KEY (primary_drugbank_id)
		REFERENCES drugs(primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_atc_codes CASCADE;
CREATE TABLE drug_atc_codes
(
	code					VARCHAR(15) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	PRIMARY KEY (code, primary_drugbank_id),
	FOREIGN KEY (primary_drugbank_id)
		REFERENCES drugs(primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_atc_code_levels CASCADE;
CREATE TABLE drug_atc_code_levels
(
	level_code				VARCHAR(15) NOT NULL,
	name					VARCHAR(50) NOT NULL,
	code					VARCHAR(15) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	PRIMARY KEY (level_code, name, code, primary_drugbank_id),
	FOREIGN KEY (primary_drugbank_id)
		REFERENCES drugs(primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_ahfs_codes CASCADE;
CREATE TABLE drug_ahfs_codes
(
	ahfs_code				VARCHAR(25) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	PRIMARY KEY (ahfs_code, primary_drugbank_id),
	FOREIGN KEY (primary_drugbank_id)
		REFERENCES drugs(primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_patents CASCADE;
CREATE TABLE drug_patents
(
	patent_number			VARCHAR(100) NOT NULL,
	country					VARCHAR(100) NOT NULL,
	approved				DATE NOT NULL,
	expires					DATE NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	PRIMARY KEY (patent_number, primary_drugbank_id),
	FOREIGN KEY (primary_drugbank_id)
		REFERENCES drugs(primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_food_interactions CASCADE;
CREATE TABLE drug_food_interactions
(
	name					VARCHAR(100) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	PRIMARY KEY (name, primary_drugbank_id),
	FOREIGN KEY (primary_drugbank_id)
		REFERENCES drugs(primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_drug_interactions CASCADE;
CREATE TABLE drug_drug_interactions
(
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	secondary_drugbank_id	VARCHAR(10) NOT NULL,
	name					VARCHAR(50) NOT NULL,
	description				VARCHAR(2000) NOT NULL,
	PRIMARY KEY (primary_drugbank_id, secondary_drugbank_id),
	FOREIGN KEY (primary_drugbank_id)
		REFERENCES drugs(primary_drugbank_id),
	FOREIGN KEY (secondary_drugbank_id)
		REFERENCES drugs(primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_sequences CASCADE;
CREATE TABLE drug_sequences
(
	drug_sequence			VARCHAR(10000) NOT NULL,
	sequence_format			VARCHAR(50) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	PRIMARY KEY (drug_sequence, sequence_format, primary_drugbank_id),
	FOREIGN KEY (primary_drugbank_id)
		REFERENCES drugs(primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_properties CASCADE;
CREATE TABLE drug_properties
(
	kind					VARCHAR(100) NOT NULL,
	property_value			VARCHAR(100) NOT NULL,
	source					VARCHAR(1000) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	experimental			BOOLEAN NOT NULL,
	calculated				BOOLEAN NOT NULL,
	PRIMARY KEY (kind, property_value, source, primary_drugbank_id),
	FOREIGN KEY (primary_drugbank_id)
		REFERENCES drugs(primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_external_identifiers CASCADE;
CREATE TABLE drug_external_identifiers
(
	external_resource		VARCHAR(100) NOT NULL,
	identifier				VARCHAR(50) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	PRIMARY KEY (external_resource, identifier, primary_drugbank_id),
	FOREIGN KEY (primary_drugbank_id)
		REFERENCES drugs(primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_external_links CASCADE;
CREATE TABLE drug_external_links
(
	external_resource		VARCHAR(100) NOT NULL,
	url						VARCHAR(2083) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	PRIMARY KEY (external_resource, url, primary_drugbank_id),
	FOREIGN KEY (primary_drugbank_id)
		REFERENCES drugs(primary_drugbank_id)
);

-- I still know nothing about what should be in this table.
DROP TABLE IF EXISTS drug_pathways CASCADE;
CREATE TABLE drug_pathways
(
	primary_drugbank_id		VARCHAR(10) PRIMARY KEY,
	FOREIGN KEY (primary_drugbank_id)
		REFERENCES drugs(primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_reactions CASCADE;
CREATE TABLE drug_reactions
(
	reaction_sequence		VARCHAR(10000) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	PRIMARY KEY (reaction_sequence, primary_drugbank_id),
	FOREIGN KEY (primary_drugbank_id)
		REFERENCES drugs(primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_reaction_elements CASCADE;
CREATE TABLE drug_reaction_elements
(
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	secondary_drugbank_id	VARCHAR(10) NOT NULL,
	name					VARCHAR(50) NOT NULL,
	left_element			BOOLEAN,
	right_element			BOOLEAN,
	reaction_sequence		VARCHAR(10000) NOT NULL,
	PRIMARY KEY (name, left_element, right_element, reaction_sequence, primary_drugbank_id, secondary_drugbank_id),
	FOREIGN KEY (reaction_sequence, primary_drugbank_id)
		REFERENCES drug_reactions(reaction_sequence, primary_drugbank_id),
	FOREIGN KEY (primary_drugbank_id)
		REFERENCES drugs(primary_drugbank_id),
	FOREIGN KEY (secondary_drugbank_id)
		REFERENCES drugs(primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_reaction_enzymes CASCADE;
CREATE TABLE drug_reaction_enzymes
(
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	secondary_drugbank_id	VARCHAR(10) NOT NULL,
	reaction_sequence		VARCHAR(10000) NOT NULL,
	name					VARCHAR(50) NOT NULL,
	uniprot_id				VARCHAR(50) NOT NULL,
	PRIMARY KEY (name, uniprot_id, reaction_sequence, primary_drugbank_id, secondary_drugbank_id),
	FOREIGN KEY (reaction_sequence, primary_drugbank_id)
		REFERENCES drug_reactions(reaction_sequence, primary_drugbank_id),
	FOREIGN KEY (primary_drugbank_id)
		REFERENCES drugs(primary_drugbank_id),
	FOREIGN KEY (secondary_drugbank_id)
		REFERENCES drugs(primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_snp_effects CASCADE;
CREATE TABLE drug_snp_effects
(
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	protein_name			VARCHAR(100) NOT NULL,
	gene_symbol				VARCHAR(25) NOT NULL,
	uniprot_id				VARCHAR(50),
	rs_id					VARCHAR(25),
	allele					VARCHAR(50) NOT NULL,
	defining_change			VARCHAR(50) NOT NULL,
	description				VARCHAR(1000),
	pubmed_id				VARCHAR(100),
	PRIMARY KEY (protein_name, defining_change, primary_drugbank_id),
	FOREIGN KEY (primary_drugbank_id)
		REFERENCES drugs(primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_snp_adverse_drug_reactions CASCADE;
CREATE TABLE drug_snp_adverse_drug_reactions
(
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	protein_name			VARCHAR(100) NOT NULL,
	gene_symbol				VARCHAR(25) NOT NULL,
	uniprot_id				VARCHAR(50),
	rs_id					VARCHAR(25),
	allele					VARCHAR(50) NOT NULL,
	adverse_reaction		VARCHAR(200) NOT NULL,
	description				VARCHAR(1000),
	pubmed_id				VARCHAR(100),
	PRIMARY KEY (protein_name, adverse_reaction, primary_drugbank_id),
	FOREIGN KEY (primary_drugbank_id)
		REFERENCES drugs(primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_enzymes CASCADE;
CREATE TABLE drug_enzymes
(
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	position				INT,
	id						VARCHAR(25) NOT NULL,
	name					VARCHAR(50) NOT NULL,
	organism				VARCHAR(50),
	known_action			VARCHAR(100),
	inhibition_strength		VARCHAR(20),
	induction_strength		VARCHAR(20),
	PRIMARY KEY (id, primary_drugbank_id),
	FOREIGN KEY (primary_drugbank_id)
		REFERENCES drugs(primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_enzyme_actions CASCADE;
CREATE TABLE drug_enzyme_actions
(
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	id						VARCHAR(25) NOT NULL,
	action					VARCHAR(200) NOT NULL,
	PRIMARY KEY (id, action, primary_drugbank_id),
	FOREIGN KEY (primary_drugbank_id, id)
		REFERENCES drug_enzymes(primary_drugbank_id, id)
);

DROP TABLE IF EXISTS drug_enzyme_references CASCADE;
CREATE TABLE drug_enzyme_references
(
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	id						VARCHAR(25) NOT NULL,
	reference				VARCHAR(1000) NOT NULL,
	PRIMARY KEY (id, reference, primary_drugbank_id),
	FOREIGN KEY (primary_drugbank_id, id)
		REFERENCES drug_enzymes(primary_drugbank_id, id)
);

DROP TABLE IF EXISTS drug_enzyme_polypeptides CASCADE;
CREATE TABLE drug_enzyme_polypeptides
(
	polypeptide_id			VARCHAR(200) NOT NULL,
	polypeptide_source		VARCHAR(1000) NOT NULL,
	name					VARCHAR(50) NOT NULL,
	general_function		VARCHAR(1000),
	specific_function		VARCHAR(2000),
	id						VARCHAR(25) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	gene_name				VARCHAR(50),
	locus					VARCHAR(20),
	cellular_location		VARCHAR(50),
	signal_regions_lower	INT,
	signal_regions_upper	INT,
	theoretical_pi			DECIMAL,
	molecular_weight		DECIMAL,
	chromosome_location		VARCHAR(10),
	organism_name			VARCHAR(50),
	organism_ncbi_taxonomy_id	VARCHAR(10),
	PRIMARY KEY (polypeptide_id, polypeptide_source, id, primary_drugbank_id),
	FOREIGN KEY (primary_drugbank_id, id)
		REFERENCES drug_enzymes(primary_drugbank_id, id)
);

DROP TABLE IF EXISTS drug_enzyme_polypeptide_transmembrane_regions CASCADE;
CREATE TABLE drug_enzyme_polypeptide_transmembrane_regions
(
	polypeptide_id			VARCHAR(200) NOT NULL,
	polypeptide_source		VARCHAR(1000) NOT NULL,
	id						VARCHAR(25) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	transmembrane_region	INT,
	PRIMARY KEY (polypeptide_id, polypeptide_source, id, primary_drugbank_id, transmembrane_region),
	FOREIGN KEY (polypeptide_id, polypeptide_source, id, primary_drugbank_id)
		REFERENCES drug_enzyme_polypeptides(polypeptide_id, polypeptide_source, id, primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_enzyme_polypeptide_external_identifiers CASCADE;
CREATE TABLE drug_enzyme_polypeptide_external_identifiers
(
	external_resource		VARCHAR(100) NOT NULL,
	identifier				VARCHAR(25) NOT NULL,
	polypeptide_id			VARCHAR(200) NOT NULL,
	polypeptide_source		VARCHAR(1000) NOT NULL,
	id						VARCHAR(25) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	PRIMARY KEY (external_resource, identifier, polypeptide_id, polypeptide_source, id, primary_drugbank_id),
	FOREIGN KEY (polypeptide_id, polypeptide_source, id, primary_drugbank_id)
		REFERENCES drug_enzyme_polypeptides(polypeptide_id, polypeptide_source, id, primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_enzyme_polypeptide_synonyms CASCADE;
CREATE TABLE drug_enzyme_polypeptide_synonyms
(
	polypeptide_synonym		VARCHAR(100) NOT NULL,
	polypeptide_id			VARCHAR(200) NOT NULL,
	polypeptide_source		VARCHAR(1000) NOT NULL,
	id						VARCHAR(25) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	PRIMARY KEY (polypeptide_synonym, polypeptide_id, polypeptide_source, id, primary_drugbank_id),
	FOREIGN KEY (polypeptide_id, polypeptide_source, id, primary_drugbank_id)
		REFERENCES drug_enzyme_polypeptides(polypeptide_id, polypeptide_source, id, primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_enzyme_polypeptide_amino_acid_sequences CASCADE;
CREATE TABLE drug_enzyme_polypeptide_amino_acid_sequences
(
	amino_acid_sequence		VARCHAR(10000) NOT NULL,
	sequence_format			VARCHAR(10) NOT NULL,
	polypeptide_id			VARCHAR(200) NOT NULL,
	polypeptide_source		VARCHAR(1000) NOT NULL,
	id						VARCHAR(25) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	PRIMARY KEY (amino_acid_sequence, sequence_format, id, primary_drugbank_id),
	FOREIGN KEY (polypeptide_id, polypeptide_source, id, primary_drugbank_id)
		REFERENCES drug_enzyme_polypeptides(polypeptide_id, polypeptide_source, id, primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_enzyme_polypeptide_gene_sequences CASCADE;
CREATE TABLE drug_enzyme_polypeptide_gene_sequences
(
	gene_sequence			VARCHAR(10000) NOT NULL,
	sequence_format			VARCHAR(10) NOT NULL,
	polypeptide_id			VARCHAR(200) NOT NULL,
	polypeptide_source		VARCHAR(1000) NOT NULL,
	id						VARCHAR(25) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	PRIMARY KEY (gene_sequence, sequence_format, id, primary_drugbank_id),
	FOREIGN KEY (polypeptide_id, polypeptide_source, id, primary_drugbank_id)
		REFERENCES drug_enzyme_polypeptides(polypeptide_id, polypeptide_source, id, primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_enzyme_polypeptide_pfams CASCADE;
CREATE TABLE drug_enzyme_polypeptide_pfams
(
	name					VARCHAR(100) NOT NULL,
	identifier				VARCHAR(25) NOT NULL,
	polypeptide_id			VARCHAR(200) NOT NULL,
	polypeptide_source		VARCHAR(1000) NOT NULL,
	id						VARCHAR(25) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	PRIMARY KEY (name, identifier, id, primary_drugbank_id),
	FOREIGN KEY (polypeptide_id, polypeptide_source, id, primary_drugbank_id)
		REFERENCES drug_enzyme_polypeptides(polypeptide_id, polypeptide_source, id, primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_enzyme_polypeptide_go_classifiers CASCADE;
CREATE TABLE drug_enzyme_polypeptide_go_classifiers
(
	category				VARCHAR(100) NOT NULL,
	description				VARCHAR(1000) NOT NULL,
	polypeptide_id			VARCHAR(200) NOT NULL,
	polypeptide_source		VARCHAR(1000) NOT NULL,
	id						VARCHAR(25) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	PRIMARY KEY (category, description, id, primary_drugbank_id),
	FOREIGN KEY (polypeptide_id, polypeptide_source, id, primary_drugbank_id)
		REFERENCES drug_enzyme_polypeptides(polypeptide_id, polypeptide_source, id, primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_carriers CASCADE;
CREATE TABLE drug_carriers
(
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	position				INT,
	id						VARCHAR(25) NOT NULL,
	name					VARCHAR(50) NOT NULL,
	organism				VARCHAR(50),
	known_action			VARCHAR(100),
	inhibition_strength		VARCHAR(20),
	induction_strength		VARCHAR(20),
	PRIMARY KEY (id, primary_drugbank_id),
	FOREIGN KEY (primary_drugbank_id)
		REFERENCES drugs(primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_carrier_actions CASCADE;
CREATE TABLE drug_carrier_actions
(
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	id						VARCHAR(25) NOT NULL,
	action					VARCHAR(200) NOT NULL,
	PRIMARY KEY (id, action, primary_drugbank_id),
	FOREIGN KEY (primary_drugbank_id, id)
		REFERENCES drug_carriers(primary_drugbank_id, id)
);

DROP TABLE IF EXISTS drug_carrier_references CASCADE;
CREATE TABLE drug_carrier_references
(
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	id						VARCHAR(25) NOT NULL,
	reference				VARCHAR(1000) NOT NULL,
	PRIMARY KEY (id, reference, primary_drugbank_id),
	FOREIGN KEY (primary_drugbank_id, id)
		REFERENCES drug_carriers(primary_drugbank_id, id)
);

DROP TABLE IF EXISTS drug_carrier_polypeptides CASCADE;
CREATE TABLE drug_carrier_polypeptides
(
	polypeptide_id			VARCHAR(200) NOT NULL,
	polypeptide_source		VARCHAR(1000) NOT NULL,
	name					VARCHAR(50) NOT NULL,
	general_function		VARCHAR(1000),
	specific_function		VARCHAR(2000),
	id						VARCHAR(25) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	gene_name				VARCHAR(50),
	locus					VARCHAR(20),
	cellular_location		VARCHAR(50),
	signal_regions_lower	INT,
	signal_regions_upper	INT,
	theoretical_pi			DECIMAL,
	molecular_weight		DECIMAL,
	chromosome_location		VARCHAR(10),
	organism_name			VARCHAR(50),
	organism_ncbi_taxonomy_id	VARCHAR(10),
	PRIMARY KEY (polypeptide_id, polypeptide_source, id, primary_drugbank_id),
	FOREIGN KEY (primary_drugbank_id, id)
		REFERENCES drug_carriers(primary_drugbank_id, id)
);

DROP TABLE IF EXISTS drug_carrier_polypeptide_transmembrane_regions CASCADE;
CREATE TABLE drug_carrier_polypeptide_transmembrane_regions
(
	polypeptide_id			VARCHAR(200) NOT NULL,
	polypeptide_source		VARCHAR(1000) NOT NULL,
	id						VARCHAR(25) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	transmembrane_region	INT,
	PRIMARY KEY (polypeptide_id, polypeptide_source, id, primary_drugbank_id, transmembrane_region),
	FOREIGN KEY (polypeptide_id, polypeptide_source, id, primary_drugbank_id)
		REFERENCES drug_carrier_polypeptides(polypeptide_id, polypeptide_source, id, primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_carrier_polypeptide_external_identifiers CASCADE;
CREATE TABLE drug_carrier_polypeptide_external_identifiers
(
	external_resource		VARCHAR(100) NOT NULL,
	identifier				VARCHAR(25) NOT NULL,
	polypeptide_id			VARCHAR(200) NOT NULL,
	polypeptide_source		VARCHAR(1000) NOT NULL,
	id						VARCHAR(25) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	PRIMARY KEY (external_resource, identifier, polypeptide_id, polypeptide_source, id, primary_drugbank_id),
	FOREIGN KEY (polypeptide_id, polypeptide_source, id, primary_drugbank_id)
		REFERENCES drug_carrier_polypeptides(polypeptide_id, polypeptide_source, id, primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_carrier_polypeptide_synonyms CASCADE;
CREATE TABLE drug_carrier_polypeptide_synonyms
(
	polypeptide_synonym		VARCHAR(100) NOT NULL,
	polypeptide_id			VARCHAR(200) NOT NULL,
	polypeptide_source		VARCHAR(1000) NOT NULL,
	id						VARCHAR(25) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	PRIMARY KEY (polypeptide_synonym, polypeptide_id, polypeptide_source, id, primary_drugbank_id),
	FOREIGN KEY (polypeptide_id, polypeptide_source, id, primary_drugbank_id)
		REFERENCES drug_carrier_polypeptides(polypeptide_id, polypeptide_source, id, primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_carrier_polypeptide_amino_acid_sequences CASCADE;
CREATE TABLE drug_carrier_polypeptide_amino_acid_sequences
(
	amino_acid_sequence		VARCHAR(10000) NOT NULL,
	sequence_format			VARCHAR(10) NOT NULL,
	polypeptide_id			VARCHAR(200) NOT NULL,
	polypeptide_source		VARCHAR(1000) NOT NULL,
	id						VARCHAR(25) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	PRIMARY KEY (amino_acid_sequence, sequence_format, id, primary_drugbank_id),
	FOREIGN KEY (polypeptide_id, polypeptide_source, id, primary_drugbank_id)
		REFERENCES drug_carrier_polypeptides(polypeptide_id, polypeptide_source, id, primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_carrier_polypeptide_gene_sequences CASCADE;
CREATE TABLE drug_carrier_polypeptide_gene_sequences
(
	gene_sequence			VARCHAR(10000) NOT NULL,
	sequence_format			VARCHAR(10) NOT NULL,
	polypeptide_id			VARCHAR(200) NOT NULL,
	polypeptide_source		VARCHAR(1000) NOT NULL,
	id						VARCHAR(25) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	PRIMARY KEY (gene_sequence, sequence_format, id, primary_drugbank_id),
	FOREIGN KEY (polypeptide_id, polypeptide_source, id, primary_drugbank_id)
		REFERENCES drug_carrier_polypeptides(polypeptide_id, polypeptide_source, id, primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_carrier_polypeptide_pfams CASCADE;
CREATE TABLE drug_carrier_polypeptide_pfams
(
	name					VARCHAR(100) NOT NULL,
	identifier				VARCHAR(25) NOT NULL,
	polypeptide_id			VARCHAR(200) NOT NULL,
	polypeptide_source		VARCHAR(1000) NOT NULL,
	id						VARCHAR(25) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	PRIMARY KEY (name, identifier, id, primary_drugbank_id),
	FOREIGN KEY (polypeptide_id, polypeptide_source, id, primary_drugbank_id)
		REFERENCES drug_carrier_polypeptides(polypeptide_id, polypeptide_source, id, primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_carrier_polypeptide_go_classifiers CASCADE;
CREATE TABLE drug_carrier_polypeptide_go_classifiers
(
	category				VARCHAR(100) NOT NULL,
	description				VARCHAR(1000) NOT NULL,
	polypeptide_id			VARCHAR(200) NOT NULL,
	polypeptide_source		VARCHAR(1000) NOT NULL,
	id						VARCHAR(25) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	PRIMARY KEY (category, description, id, primary_drugbank_id),
	FOREIGN KEY (polypeptide_id, polypeptide_source, id, primary_drugbank_id)
		REFERENCES drug_carrier_polypeptides(polypeptide_id, polypeptide_source, id, primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_transporters CASCADE;
CREATE TABLE drug_transporters
(
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	position				INT,
	id						VARCHAR(25) NOT NULL,
	name					VARCHAR(50) NOT NULL,
	organism				VARCHAR(50),
	known_action			VARCHAR(100),
	inhibition_strength		VARCHAR(20),
	induction_strength		VARCHAR(20),
	PRIMARY KEY (id, primary_drugbank_id),
	FOREIGN KEY (primary_drugbank_id)
		REFERENCES drugs(primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_transporter_actions CASCADE;
CREATE TABLE drug_transporter_actions
(
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	id						VARCHAR(25) NOT NULL,
	action					VARCHAR(200) NOT NULL,
	PRIMARY KEY (id, action, primary_drugbank_id),
	FOREIGN KEY (primary_drugbank_id, id)
		REFERENCES drug_transporters(primary_drugbank_id, id)
);

DROP TABLE IF EXISTS drug_transporter_references CASCADE;
CREATE TABLE drug_transporter_references
(
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	id						VARCHAR(25) NOT NULL,
	reference				VARCHAR(1000) NOT NULL,
	PRIMARY KEY (id, reference, primary_drugbank_id),
	FOREIGN KEY (primary_drugbank_id, id)
		REFERENCES drug_transporters(primary_drugbank_id, id)
);

DROP TABLE IF EXISTS drug_transporter_polypeptides CASCADE;
CREATE TABLE drug_transporter_polypeptides
(
	polypeptide_id			VARCHAR(200) NOT NULL,
	polypeptide_source		VARCHAR(1000) NOT NULL,
	name					VARCHAR(50) NOT NULL,
	general_function		VARCHAR(1000),
	specific_function		VARCHAR(2000),
	id						VARCHAR(25) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	gene_name				VARCHAR(50),
	locus					VARCHAR(20),
	cellular_location		VARCHAR(50),
	signal_regions_lower	INT,
	signal_regions_upper	INT,
	theoretical_pi			DECIMAL,
	molecular_weight		DECIMAL,
	chromosome_location		VARCHAR(10),
	organism_name			VARCHAR(50),
	organism_ncbi_taxonomy_id	VARCHAR(10),
	PRIMARY KEY (polypeptide_id, polypeptide_source, id, primary_drugbank_id),
	FOREIGN KEY (primary_drugbank_id, id)
		REFERENCES drug_transporters(primary_drugbank_id, id)
);

DROP TABLE IF EXISTS drug_transporter_polypeptide_transmembrane_regions CASCADE;
CREATE TABLE drug_transporter_polypeptide_transmembrane_regions
(
	polypeptide_id			VARCHAR(200) NOT NULL,
	polypeptide_source		VARCHAR(1000) NOT NULL,
	id						VARCHAR(25) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	transmembrane_region	INT,
	PRIMARY KEY (polypeptide_id, polypeptide_source, id, primary_drugbank_id, transmembrane_region),
	FOREIGN KEY (polypeptide_id, polypeptide_source, id, primary_drugbank_id)
		REFERENCES drug_transporter_polypeptides(polypeptide_id, polypeptide_source, id, primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_transporter_polypeptide_external_identifiers CASCADE;
CREATE TABLE drug_transporter_polypeptide_external_identifiers
(
	external_resource		VARCHAR(100) NOT NULL,
	identifier				VARCHAR(25) NOT NULL,
	polypeptide_id			VARCHAR(200) NOT NULL,
	polypeptide_source		VARCHAR(1000) NOT NULL,
	id						VARCHAR(25) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	PRIMARY KEY (external_resource, identifier, polypeptide_id, polypeptide_source, id, primary_drugbank_id),
	FOREIGN KEY (polypeptide_id, polypeptide_source, id, primary_drugbank_id)
		REFERENCES drug_transporter_polypeptides(polypeptide_id, polypeptide_source, id, primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_transporter_polypeptide_synonyms CASCADE;
CREATE TABLE drug_transporter_polypeptide_synonyms
(
	polypeptide_synonym		VARCHAR(100) NOT NULL,
	polypeptide_id			VARCHAR(200) NOT NULL,
	polypeptide_source		VARCHAR(1000) NOT NULL,
	id						VARCHAR(25) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	PRIMARY KEY (polypeptide_synonym, polypeptide_id, polypeptide_source, id, primary_drugbank_id),
	FOREIGN KEY (polypeptide_id, polypeptide_source, id, primary_drugbank_id)
		REFERENCES drug_transporter_polypeptides(polypeptide_id, polypeptide_source, id, primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_transporter_polypeptide_amino_acid_sequences CASCADE;
CREATE TABLE drug_transporter_polypeptide_amino_acid_sequences
(
	amino_acid_sequence		VARCHAR(10000) NOT NULL,
	sequence_format			VARCHAR(10) NOT NULL,
	polypeptide_id			VARCHAR(200) NOT NULL,
	polypeptide_source		VARCHAR(1000) NOT NULL,
	id						VARCHAR(25) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	PRIMARY KEY (amino_acid_sequence, sequence_format, id, primary_drugbank_id),
	FOREIGN KEY (polypeptide_id, polypeptide_source, id, primary_drugbank_id)
		REFERENCES drug_transporter_polypeptides(polypeptide_id, polypeptide_source, id, primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_transporter_polypeptide_gene_sequences CASCADE;
CREATE TABLE drug_transporter_polypeptide_gene_sequences
(
	gene_sequence			VARCHAR(10000) NOT NULL,
	sequence_format			VARCHAR(10) NOT NULL,
	polypeptide_id			VARCHAR(200) NOT NULL,
	polypeptide_source		VARCHAR(1000) NOT NULL,
	id						VARCHAR(25) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	PRIMARY KEY (gene_sequence, sequence_format, id, primary_drugbank_id),
	FOREIGN KEY (polypeptide_id, polypeptide_source, id, primary_drugbank_id)
		REFERENCES drug_transporter_polypeptides(polypeptide_id, polypeptide_source, id, primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_transporter_polypeptide_pfams CASCADE;
CREATE TABLE drug_transporter_polypeptide_pfams
(
	name					VARCHAR(100) NOT NULL,
	identifier				VARCHAR(25) NOT NULL,
	polypeptide_id			VARCHAR(200) NOT NULL,
	polypeptide_source		VARCHAR(1000) NOT NULL,
	id						VARCHAR(25) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	PRIMARY KEY (name, identifier, id, primary_drugbank_id),
	FOREIGN KEY (polypeptide_id, polypeptide_source, id, primary_drugbank_id)
		REFERENCES drug_transporter_polypeptides(polypeptide_id, polypeptide_source, id, primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_transporter_polypeptide_go_classifiers CASCADE;
CREATE TABLE drug_transporter_polypeptide_go_classifiers
(
	category				VARCHAR(100) NOT NULL,
	description				VARCHAR(1000) NOT NULL,
	polypeptide_id			VARCHAR(200) NOT NULL,
	polypeptide_source		VARCHAR(1000) NOT NULL,
	id						VARCHAR(25) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	PRIMARY KEY (category, description, id, primary_drugbank_id),
	FOREIGN KEY (polypeptide_id, polypeptide_source, id, primary_drugbank_id)
		REFERENCES drug_transporter_polypeptides(polypeptide_id, polypeptide_source, id, primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_targets CASCADE;
CREATE TABLE drug_targets
(
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	position				INT,
	id						VARCHAR(25) NOT NULL,
	name					VARCHAR(50) NOT NULL,
	organism				VARCHAR(50),
	known_action			VARCHAR(100),
	inhibition_strength		VARCHAR(20),
	induction_strength		VARCHAR(20),
	PRIMARY KEY (id, primary_drugbank_id),
	FOREIGN KEY (primary_drugbank_id)
		REFERENCES drugs(primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_target_actions CASCADE;
CREATE TABLE drug_target_actions
(
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	id						VARCHAR(25) NOT NULL,
	action					VARCHAR(200) NOT NULL,
	PRIMARY KEY (id, action, primary_drugbank_id),
	FOREIGN KEY (primary_drugbank_id, id)
		REFERENCES drug_targets(primary_drugbank_id, id)
);

DROP TABLE IF EXISTS drug_target_references CASCADE;
CREATE TABLE drug_target_references
(
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	id						VARCHAR(25) NOT NULL,
	reference				VARCHAR(1000) NOT NULL,
	PRIMARY KEY (id, reference, primary_drugbank_id),
	FOREIGN KEY (primary_drugbank_id, id)
		REFERENCES drug_targets(primary_drugbank_id, id)
);

DROP TABLE IF EXISTS drug_target_polypeptides CASCADE;
CREATE TABLE drug_target_polypeptides
(
	polypeptide_id			VARCHAR(200) NOT NULL,
	polypeptide_source		VARCHAR(1000) NOT NULL,
	name					VARCHAR(50) NOT NULL,
	general_function		VARCHAR(1000),
	specific_function		VARCHAR(2000),
	id						VARCHAR(25) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	gene_name				VARCHAR(50),
	locus					VARCHAR(20),
	cellular_location		VARCHAR(50),
	signal_regions_lower	INT,
	signal_regions_upper	INT,
	theoretical_pi			DECIMAL,
	molecular_weight		DECIMAL,
	chromosome_location		VARCHAR(10),
	organism_name			VARCHAR(50),
	organism_ncbi_taxonomy_id	VARCHAR(10),
	PRIMARY KEY (polypeptide_id, polypeptide_source, id, primary_drugbank_id),
	FOREIGN KEY (primary_drugbank_id, id)
		REFERENCES drug_targets(primary_drugbank_id, id)
);

DROP TABLE IF EXISTS drug_target_polypeptide_transmembrane_regions CASCADE;
CREATE TABLE drug_target_polypeptide_transmembrane_regions
(
	polypeptide_id			VARCHAR(200) NOT NULL,
	polypeptide_source		VARCHAR(1000) NOT NULL,
	id						VARCHAR(25) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	transmembrane_region	INT,
	PRIMARY KEY (polypeptide_id, polypeptide_source, id, primary_drugbank_id, transmembrane_region),
	FOREIGN KEY (polypeptide_id, polypeptide_source, id, primary_drugbank_id)
		REFERENCES drug_target_polypeptides(polypeptide_id, polypeptide_source, id, primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_target_polypeptide_external_identifiers CASCADE;
CREATE TABLE drug_target_polypeptide_external_identifiers
(
	external_resource		VARCHAR(100) NOT NULL,
	identifier				VARCHAR(25) NOT NULL,
	polypeptide_id			VARCHAR(200) NOT NULL,
	polypeptide_source		VARCHAR(1000) NOT NULL,
	id						VARCHAR(25) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	PRIMARY KEY (external_resource, identifier, polypeptide_id, polypeptide_source, id, primary_drugbank_id),
	FOREIGN KEY (polypeptide_id, polypeptide_source, id, primary_drugbank_id)
		REFERENCES drug_target_polypeptides(polypeptide_id, polypeptide_source, id, primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_target_polypeptide_synonyms CASCADE;
CREATE TABLE drug_target_polypeptide_synonyms
(
	polypeptide_synonym		VARCHAR(100) NOT NULL,
	polypeptide_id			VARCHAR(200) NOT NULL,
	polypeptide_source		VARCHAR(1000) NOT NULL,
	id						VARCHAR(25) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	PRIMARY KEY (polypeptide_synonym, polypeptide_id, polypeptide_source, id, primary_drugbank_id),
	FOREIGN KEY (polypeptide_id, polypeptide_source, id, primary_drugbank_id)
		REFERENCES drug_target_polypeptides(polypeptide_id, polypeptide_source, id, primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_target_polypeptide_amino_acid_sequences CASCADE;
CREATE TABLE drug_target_polypeptide_amino_acid_sequences
(
	amino_acid_sequence		VARCHAR(10000) NOT NULL,
	sequence_format			VARCHAR(10) NOT NULL,
	polypeptide_id			VARCHAR(200) NOT NULL,
	polypeptide_source		VARCHAR(1000) NOT NULL,
	id						VARCHAR(25) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	PRIMARY KEY (amino_acid_sequence, sequence_format, id, primary_drugbank_id),
	FOREIGN KEY (polypeptide_id, polypeptide_source, id, primary_drugbank_id)
		REFERENCES drug_target_polypeptides(polypeptide_id, polypeptide_source, id, primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_target_polypeptide_gene_sequences CASCADE;
CREATE TABLE drug_target_polypeptide_gene_sequences
(
	gene_sequence			VARCHAR(10000) NOT NULL,
	sequence_format			VARCHAR(10) NOT NULL,
	polypeptide_id			VARCHAR(200) NOT NULL,
	polypeptide_source		VARCHAR(1000) NOT NULL,
	id						VARCHAR(25) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	PRIMARY KEY (gene_sequence, sequence_format, id, primary_drugbank_id),
	FOREIGN KEY (polypeptide_id, polypeptide_source, id, primary_drugbank_id)
		REFERENCES drug_target_polypeptides(polypeptide_id, polypeptide_source, id, primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_target_polypeptide_pfams CASCADE;
CREATE TABLE drug_target_polypeptide_pfams
(
	name					VARCHAR(100) NOT NULL,
	identifier				VARCHAR(25) NOT NULL,
	polypeptide_id			VARCHAR(200) NOT NULL,
	polypeptide_source		VARCHAR(1000) NOT NULL,
	id						VARCHAR(25) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	PRIMARY KEY (name, identifier, id, primary_drugbank_id),
	FOREIGN KEY (polypeptide_id, polypeptide_source, id, primary_drugbank_id)
		REFERENCES drug_target_polypeptides(polypeptide_id, polypeptide_source, id, primary_drugbank_id)
);

DROP TABLE IF EXISTS drug_target_polypeptide_go_classifiers CASCADE;
CREATE TABLE drug_target_polypeptide_go_classifiers
(
	category				VARCHAR(100) NOT NULL,
	description				VARCHAR(1000) NOT NULL,
	polypeptide_id			VARCHAR(200) NOT NULL,
	polypeptide_source		VARCHAR(1000) NOT NULL,
	id						VARCHAR(25) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	PRIMARY KEY (category, description, id, primary_drugbank_id),
	FOREIGN KEY (polypeptide_id, polypeptide_source, id, primary_drugbank_id)
		REFERENCES drug_target_polypeptides(polypeptide_id, polypeptide_source, id, primary_drugbank_id)
);