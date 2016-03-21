--
-- The purpose of this file is to create the tables into which
-- the data generated from drugbank_xml_to_sql.py can be loaded.
--
--

-- Note that the "drug_pathway" table is not created because
-- the columns within it are currently unknown.

CREATE TABLE Drug
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

CREATE TABLE DrugAltID
(
	secondary_drugbank_id	VARCHAR(15) NOT NULL PRIMARY KEY,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	CONSTRAINT fk_primary_drugbank_id FOREIGN KEY (primary_drugbank_id)
		REFERENCES Drug(primary_drugbank_id)
);

CREATE TABLE DrugGroup
(
	drug_group				VARCHAR(50) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	CONSTRAINT pk_drug_group PRIMARY KEY (drug_group, primary_drugbank_id),
	CONSTRAINT fk_primary_drugbank_id FOREIGN KEY (primary_drugbank_id)
		REFERENCES Drug(primary_drugbank_id)
);

CREATE TABLE DrugGeneralReference
(
	general_reference		VARCHAR(1000) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	CONSTRAINT pk_drug_general_reference PRIMARY KEY (general_reference, primary_drugbank_id),
	CONSTRAINT fk_primary_drugbank_id FOREIGN KEY (primary_drugbank_id)
		REFERENCES Drug(primary_drugbank_id)
);

CREATE TABLE DrugVolumeOfDistribution
(
	volume_of_distribution	VARCHAR(100) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	CONSTRAINT pk_drug_volume_of_distribution PRIMARY KEY (volume_of_distribution, primary_drugbank_id),
	CONSTRAINT fk_primary_drugbank_id FOREIGN KEY (primary_drugbank_id)
		REFERENCES Drug(primary_drugbank_id)
);

CREATE TABLE DrugClearance
(
	clearance				VARCHAR(100) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	CONSTRAINT pk_drug_clearance PRIMARY KEY (clearance, primary_drugbank_id),
	CONSTRAINT fk_primary_drugbank_id FOREIGN KEY (primary_drugbank_id)
		REFERENCES Drug(primary_drugbank_id)
);

CREATE TABLE DrugClassification
(
	primary_drugbank_id		VARCHAR(10) NOT NULL PRIMARY KEY,
	description				VARCHAR(1000),
	direct_parent			VARCHAR(100),
	kingdom					VARCHAR(100),
	superclass				VARCHAR(100),
	drug_class				VARCHAR(100),
	subclass				VARCHAR(100),
	CONSTRAINT fk_primary_drugbank_id FOREIGN KEY (primary_drugbank_id)
		REFERENCES Drug(primary_drugbank_id)
);

CREATE TABLE DrugClassificationAltParent
(
	alternative_parent		VARCHAR(100) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	CONSTRAINT pk_alternative_parent PRIMARY KEY (alternative_parent, primary_drugbank_id),
	CONSTRAINT fk_primary_drugbank_id FOREIGN KEY (primary_drugbank_id)
		REFERENCES Drug(primary_drugbank_id)	
);

CREATE TABLE DrugClassificationSubstituent
(
	substituent				VARCHAR(100) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	CONSTRAINT pk_substituent PRIMARY KEY (substituent, primary_drugbank_id),
	CONSTRAINT fk_primary_drugbank_id FOREIGN KEY (primary_drugbank_id)
		REFERENCES Drug(primary_drugbank_id)
);

CREATE TABLE DrugSalt
(
	primary_drugbank_id_salt	VARCHAR(10) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	name					VARCHAR(100) NOT NULL,
	cas_number				VARCHAR(50),
	inchikey				VARCHAR(100),
	CONSTRAINT pk_drug_salt PRIMARY KEY (primary_drugbank_id_salt, primary_drugbank_id),	
	CONSTRAINT fk_primary_drugbank_id_salt FOREIGN KEY (primary_drugbank_id)
		REFERENCES Drug(primary_drugbank_id)
	CONSTRAINT fk_primary_drugbank_id FOREIGN KEY (primary_drugbank_id)
		REFERENCES Drug(primary_drugbank_id)
);

CREATE TABLE DrugSynonym
(
	drug_synonym			VARCHAR(50) NOT NULL,
	synonym_language		VARCHAR(50),
	coder					VARCHAR(50),
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	CONSTRAINT pk_drug_synonym PRIMARY KEY (drug_synonym, primary_drugbank_id),	
	CONSTRAINT fk_primary_drugbank_id FOREIGN KEY (primary_drugbank_id)
		REFERENCES Drug(primary_drugbank_id)
);

CREATE TABLE DrugProduct
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
	CONSTRAINT fk_primary_drugbank_id FOREIGN KEY (primary_drugbank_id)
		REFERENCES Drug(primary_drugbank_id)
);

CREATE TABLE DrugInternationalBrand
(
	name					VARCHAR(50) NOT NULL,
	company					VARCHAR(100) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	CONSTRAINT pk_international_brand PRIMARY KEY (name, company, primary_drugbank_id),
	CONSTRAINT fk_primary_drugbank_id FOREIGN KEY (primary_drugbank_id)
		REFERENCES Drug(primary_drugbank_id)
);

CREATE TABLE DrugMixture
(
	name					VARCHAR(50) NOT NULL,
    ingredients             VARCHAR(1000) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	CONSTRAINT pk_drug_mixture PRIMARY KEY (name, primary_drugbank_id),
	CONSTRAINT fk_primary_drugbank_id FOREIGN KEY (primary_drugbank_id)
		REFERENCES Drug(primary_drugbank_id)
);

CREATE TABLE DrugPackager
(
	name					VARCHAR(50) NOT NULL,
	url						VARCHAR(2083),
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	CONSTRAINT pk_drug_packager PRIMARY KEY (name, primary_drugbank_id),
	CONSTRAINT fk_primary_drugbank_id FOREIGN KEY (primary_drugbank_id)
		REFERENCES Drug(primary_drugbank_id)
);

CREATE TABLE DrugManufacturer
(
	name					VARCHAR(50) NOT NULL,
	generic					BOOLEAN,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	CONSTRAINT pk_drug_manufacturer PRIMARY KEY (name, primary_drugbank_id),
	CONSTRAINT fk_primary_drugbank_id FOREIGN KEY (primary_drugbank_id)
		REFERENCES Drug(primary_drugbank_id)
);

CREATE TABLE DrugPrice
(
	description				VARCHAR(100) NOT NULL,
	unit					VARCHAR(20) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	CONSTRAINT pk_drug_price PRIMARY KEY (description, unit, primary_drugbank_id),
	CONSTRAINT fk_primary_drugbank_id FOREIGN KEY (primary_drugbank_id)
		REFERENCES Drug(primary_drugbank_id)
);

CREATE TABLE DrugCost
(
	cost					SMALLMONEY NOT NULL,
	currency				VARCHAR(20) NOT NULL,
	description				VARCHAR(100) NOT NULL,
	unit					VARCHAR(20) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	CONSTRAINT pk_drug_cost PRIMARY KEY (cost, currency, description, unit, primary_drugbank_id),
	CONSTRAINT fk_description_unit_primary_drugbank_id FOREIGN KEY (description, unit, primary_drugbank_id)
		REFERENCES DrugPrice(pk_drug_price)
	CONSTRAINT fk_primary_drugbank_id FOREIGN KEY (primary_drugbank_id)
		REFERENCES Drug(primary_drugbank_id)
);

CREATE TABLE DrugCategory
(
	name					VARCHAR(100) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	CONSTRAINT pk_drug_category PRIMARY KEY (category, primary_drugbank_id),
	CONSTRAINT fk_primary_drugbank_id FOREIGN KEY (primary_drugbank_id)
		REFERENCES Drug(primary_drugbank_id)
);

CREATE TABLE DrugMeSH
(
	mesh_id					VARCHAR(100) NOT NULL,
	name					VARCHAR(100) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	CONSTRAINT pk_drug_mesh PRIMARY KEY (mesh, name, primary_drugbank_id),
	CONSTRAINT fk_drug_category_primary_drugbank_id FOREIGN KEY (name, primary_drugbank_id)
		REFERENCES DrugPrice(pk_drug_category)
	CONSTRAINT fk_primary_drugbank_id FOREIGN KEY (primary_drugbank_id)
		REFERENCES Drug(primary_drugbank_id)
);

CREATE TABLE DrugAffectedOrganism
(
	name					VARCHAR(50) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	CONSTRAINT pk_affected_organism PRIMARY KEY (name, primary_drugbank_id),
	CONSTRAINT fk_primary_drugbank_id FOREIGN KEY (primary_drugbank_id)
		REFERENCES Drug(primary_drugbank_id)
);

CREATE TABLE DrugDosage
(
	form					VARCHAR(50) NOT NULL,
	route					VARCHAR(100) NOT NULL,
	strength				VARCHAR(50) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	CONSTRAINT pk_drug_dosage PRIMARY KEY (form, route, strength, primary_drugbank_id),
	CONSTRAINT fk_primary_drugbank_id FOREIGN KEY (primary_drugbank_id)
		REFERENCES Drug(primary_drugbank_id)
);

CREATE TABLE DrugATCCode
(
	code					VARCHAR(15) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	CONSTRAINT pk_atc_code PRIMARY KEY (code, primary_drugbank_id),
	CONSTRAINT fk_primary_drugbank_id FOREIGN KEY (primary_drugbank_id)
		REFERENCES Drug(primary_drugbank_id)
);

CREATE TABLE DrugATCCodeLevel
(
	level_code				VARCHAR(15) NOT NULL,
	name					VARCHAR(50) NOT NULL,
	code					VARCHAR(15) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	CONSTRAINT pk_atc_code_level PRIMARY KEY (level_code, name, code, primary_drugbank_id),
	CONSTRAINT fk_primary_drugbank_id FOREIGN KEY (primary_drugbank_id)
		REFERENCES Drug(primary_drugbank_id)
);

CREATE TABLE DrugAHFSCode
(
	ahfs_code				VARCHAR(25) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	CONSTRAINT pk_ahfs_code PRIMARY KEY (ahfs_code, primary_drugbank_id),
	CONSTRAINT fk_primary_drugbank_id FOREIGN KEY (primary_drugbank_id)
		REFERENCES Drug(primary_drugbank_id)
);

CREATE TABLE DrugPatent
(
	patent_number			VARCHAR(100) NOT NULL,
	country					VARCHAR(100) NOT NULL,
	approved				DATE NOT NULL,
	expires					DATE NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	CONSTRAINT pk_drug_patent PRIMARY KEY (patent_number, primary_drugbank_id),
	CONSTRAINT fk_primary_drugbank_id FOREIGN KEY (primary_drugbank_id)
		REFERENCES Drug(primary_drugbank_id)
);

CREATE TABLE DrugFoodInteraction
(
	name					VARCHAR(100) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	CONSTRAINT pk_food_interaction PRIMARY KEY (name, primary_drugbank_id),
	CONSTRAINT fk_primary_drugbank_id FOREIGN KEY (primary_drugbank_id)
		REFERENCES Drug(primary_drugbank_id)
);

CREATE TABLE DrugDrugInteraction
(
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	secondary_drugbank_id	VARCHAR(10) NOT NULL,
	name					VARCHAR(50) NOT NULL,
	description				VARCHAR(2000) NOT NULL,
	CONSTRAINT pk_drug_interaction PRIMARY KEY (primary_drugbank_id, secondary_drugbank_id),
	CONSTRAINT fk_primary_drugbank_id FOREIGN KEY (primary_drugbank_id)
		REFERENCES Drug(primary_drugbank_id),
	CONSTRAINT fk_secondary_drugbank_id FOREIGN KEY (secondary_drugbank_id)
		REFERENCES Drug(primary_drugbank_id)
);

CREATE TABLE DrugSequence
(
	drug_sequence			VARCHAR(10000) NOT NULL,
	sequence_format			VARCHAR(50) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	CONSTRAINT pk_drug_sequence PRIMARY KEY (drug_sequence, sequence_format, primary_drugbank_id),
	CONSTRAINT fk_primary_drugbank_id FOREIGN KEY (primary_drugbank_id)
		REFERENCES Drug(primary_drugbank_id)
);

CREATE TABLE DrugProperty
(
	kind					VARCHAR(100) NOT NULL,
	property_value			VARCHAR(100) NOT NULL,
	source					VARCHAR(1000) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	experimental			BOOLEAN NOT NULL,
	calculated				BOOLEAN NOT NULL,
	CONSTRAINT pk_drug_property PRIMARY KEY (kind, property, source, primary_drugbank_id),
	CONSTRAINT fk_primary_drugbank_id FOREIGN KEY (primary_drugbank_id)
		REFERENCES Drug(primary_drugbank_id)
);

CREATE TABLE DrugExternalIdentifier
(
	external_resource		VARCHAR(100) NOT NULL,
	identifier				VARCHAR(50) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	CONSTRAINT pk_drug_external_identifier PRIMARY KEY (external_resource, identifier, primary_drugbank_id),
	CONSTRAINT fk_primary_drugbank_id FOREIGN KEY (primary_drugbank_id)
		REFERENCES Drug(primary_drugbank_id)
);

CREATE TABLE DrugExternalLink
(
	external_resource		VARCHAR(100) NOT NULL,
	url						VARCHAR(2083) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	CONSTRAINT pk_drug_external_link PRIMARY KEY (external_resource, url, primary_drugbank_id),
	CONSTRAINT fk_primary_drugbank_id FOREIGN KEY (primary_drugbank_id)
		REFERENCES Drug(primary_drugbank_id)
);

-- I still know nothing about what should be in this table.
CREATE TABLE DrugPathway
(
	primary_drugbank_id		VARCHAR(10) PRIMARY KEY,
	CONSTRAINT fk_primary_drugbank_id FOREIGN KEY (primary_drugbank_id)
		REFERENCES Drug(primary_drugbank_id)
);

CREATE TABLE DrugReaction
(
	reaction_sequence		VARCHAR(10000) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	CONSTRAINT pk_drug_reaction PRIMARY KEY (reaction_sequence, primary_drugbank_id),
	CONSTRAINT fk_primary_drugbank_id FOREIGN KEY (primary_drugbank_id)
		REFERENCES Drug(primary_drugbank_id)
);

CREATE TABLE DrugReactionElement
(
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	secondary_drugbank_id	VARCHAR(10) NOT NULL,
	name					VARCHAR(50) NOT NULL,
	left_element			BOOLEAN,
	right_element			BOOLEAN,
	reaction_sequence		VARCHAR(10000) NOT NULL,
	CONSTRAINT pk_drug_reaction_element PRIMARY KEY (name, left_element, right_element, reaction_sequence, primary_drugbank_id, secondary_drugbank_id),
	CONSTRAINT fk_reaction_sequence_primary_drugbank_id FOREIGN KEY (reaction_sequence, primary_drugbank_id)
		REFERENCES DrugReaction(pk_drug_reaction),
	CONSTRAINT fk_primary_drugbank_id FOREIGN KEY (primary_drugbank_id)
		REFERENCES Drug(primary_drugbank_id),
	CONSTRAINT fk_secondary_drugbank_id FOREIGN KEY (secondary_drugbank_id)
		REFERENCES Drug(primary_drugbank_id)
);

CREATE TABLE DrugReactionEnzyme
(
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	secondary_drugbank_id	VARCHAR(10) NOT NULL,
	reaction_sequence		VARCHAR(10000) NOT NULL,
	name					VARCHAR(50) NOT NULL,
	uniprot_id				VARCHAR(50) NOT NULL,
	CONSTRAINT pk_drug_reaction_enzyme PRIMARY KEY (name, uniprot_id, reaction_sequence, primary_drugbank_id, secondary_drugbank_id),
	CONSTRAINT fk_reaction_sequence_primary_drugbank_id FOREIGN KEY (reaction_sequence, primary_drugbank_id)
		REFERENCES DrugReaction(pk_drug_reaction),
	CONSTRAINT fk_primary_drugbank_id FOREIGN KEY (primary_drugbank_id)
		REFERENCES Drug(primary_drugbank_id),
	CONSTRAINT fk_secondary_drugbank_id FOREIGN KEY (secondary_drugbank_id)
		REFERENCES Drug(primary_drugbank_id)
);

CREATE TABLE DrugSNPEffect
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
	CONSTRAINT pk_drug_snp_effect PRIMARY KEY (protein_name, defining_change, primary_drugbank_id),
	CONSTRAINT fk_primary_drugbank_id FOREIGN KEY (primary_drugbank_id)
		REFERENCES Drug(primary_drugbank_id)
);

CREATE TABLE DrugSNPAdverseDrugReaction
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
	CONSTRAINT pk_drug_snp_adverse_drug_reaction PRIMARY KEY (protein_name, adverse_reaction, primary_drugbank_id),
	CONSTRAINT fk_primary_drugbank_id FOREIGN KEY (primary_drugbank_id)
		REFERENCES Drug(primary_drugbank_id)
);

CREATE TABLE DrugEnzyme
(
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	position				INT,
	id						VARCHAR(25) NOT NULL,
	name					VARCHAR(50) NOT NULL,
	organism				VARCHAR(50),
	known_action			VARCHAR(100),
	CONSTRAINT pk_drug_enzyme PRIMARY KEY (id, primary_drugbank_id),
	CONSTRAINT fk_primary_drugbank_id FOREIGN KEY (primary_drugbank_id)
		REFERENCES Drug(primary_drugbank_id)
);

CREATE TABLE DrugEnzymeAction
(
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	id						VARCHAR(25) NOT NULL,
	action					VARCHAR(200) NOT NULL,
	CONSTRAINT pk_drug_enzyme_action PRIMARY KEY (id, action, primary_drugbank_id),
	CONSTRAINT fk_primary_drugbank_id FOREIGN KEY (primary_drugbank_id)
		REFERENCES Drug(primary_drugbank_id)
);

CREATE TABLE DrugEnzymeReference
(
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	id						VARCHAR(25) NOT NULL,
	reference				VARCHAR(1000) NOT NULL,
	CONSTRAINT pk_drug_enzyme_reference PRIMARY KEY (id, reference, primary_drugbank_id),
	CONSTRAINT fk_primary_drugbank_id FOREIGN KEY (primary_drugbank_id)
		REFERENCES Drug(primary_drugbank_id)
);

CREATE TABLE DrugEnzymePolypeptide
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
	inhibition_strength		VARCHAR(20),
	induction_strength		VARCHAR(20)
	CONSTRAINT pk_drug_enzyme_polypeptide PRIMARY KEY (polypeptide_id, polypeptide_source, id, primary_drugbank_id),
	CONSTRAINT fk_enzyme_id_primary_drugbank_id FOREIGN KEY (id, primary_drugbank_id)
		REFERENCES DrugEnzyme(pk_drug_enzyme),
	CONSTRAINT fk_primary_drugbank_id FOREIGN KEY (primary_drugbank_id)
		REFERENCES Drug(primary_drugbank_id)
);

CREATE TABLE DrugEnzymePolypeptideTransmembraneRegion
(
	polypeptide_id			VARCHAR(200) NOT NULL,
	polypeptide_source		VARCHAR(1000) NOT NULL,
	id						VARCHAR(25) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	transmembrane_region_lower	INT,
	transmembrane_region_upper	INT,
	CONSTRAINT pk_drug_enzyme_polypeptide_transmembrane_region PRIMARY KEY (polypeptide_id, polypeptide_source, id, primary_drugbank_id, transmembrane_region_lower, transmembrane_region_upper),
	CONSTRAINT fk_drug_enzyme_polypeptide PRIMARY KEY (polypeptide_id, polypeptide_source, id, primary_drugbank_id)
		REFERENCES DrugEnzymePolypeptide(pk_drug_enzyme_polypeptide),
	CONSTRAINT fk_primary_drugbank_id FOREIGN KEY (primary_drugbank_id)
		REFERENCES Drug(primary_drugbank_id)
);

CREATE TABLE DrugEnzymePolypeptideExternalIdentifier
(
	external_resource		VARCHAR(100) NOT NULL,
	identifier				VARCHAR(25) NOT NULL,
	polypeptide_id			VARCHAR(200) NOT NULL,
	polypeptide_source		VARCHAR(1000) NOT NULL,
	id						VARCHAR(25) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	CONSTRAINT pk_drug_enzyme_polypeptide_external_identifier PRIMARY KEY (external_resource, identifier, polypeptide_id, polypeptide_source, id, primary_drugbank_id),
	CONSTRAINT fk_drug_enzyme_polypeptide FOREIGN KEY (polypeptide_id, polypeptide_source, id, primary_drugbank_id)
		REFERENCES DrugEnzymePolypeptide(pk_drug_enzyme_polypeptide),
	CONSTRAINT fk_primary_drugbank_id FOREIGN KEY (primary_drugbank_id)
		REFERENCES Drug(primary_drugbank_id)
);

CREATE TABLE DrugEnzymePolypeptideSynonym
(
	polypeptide_synonym		VARCHAR(100) NOT NULL,
	polypeptide_id			VARCHAR(200) NOT NULL,
	polypeptide_source		VARCHAR(1000) NOT NULL,
	id						VARCHAR(25) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	CONSTRAINT pk_drug_enzyme_polypeptide_synonym PRIMARY KEY (polypeptide_synonym, polypeptide_id, polypeptide_source, id, primary_drugbank_id),
	CONSTRAINT fk_drug_enzyme_polypeptide FOREIGN KEY (polypeptide_id, polypeptide_source, id, primary_drugbank_id)
		REFERENCES DrugEnzymePolypeptide(pk_drug_enzyme_polypeptide),
	CONSTRAINT fk_primary_drugbank_id FOREIGN KEY (primary_drugbank_id)
		REFERENCES Drug(primary_drugbank_id)
);

CREATE TABLE DrugEnzymeAminoAcidSequence
(
	amino_acid_sequence		VARCHAR(10000) NOT NULL,
	sequence_format			VARCHAR(10) NOT NULL,
	polypeptide_id			VARCHAR(200) NOT NULL,
	polypeptide_source		VARCHAR(1000) NOT NULL,
	id						VARCHAR(25) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	CONSTRAINT pk_drug_enzyme_amino_acid_sequence PRIMARY KEY (amino_acid_sequence, sequence_format, id, primary_drugbank_id),
	CONSTRAINT fk_enzyme_id_primary_drugbank_id FOREIGN KEY (id, primary_drugbank_id)
		REFERENCES DrugEnzyme(pk_drug_enzyme),
	CONSTRAINT fk_primary_drugbank_id FOREIGN KEY (primary_drugbank_id)
		REFERENCES Drug(primary_drugbank_id)
);

CREATE TABLE DrugEnzymeGeneSequence
(
	gene_sequence			VARCHAR(10000) NOT NULL,
	sequence_format			VARCHAR(10) NOT NULL,
	polypeptide_id			VARCHAR(200) NOT NULL,
	polypeptide_source		VARCHAR(1000) NOT NULL,
	id						VARCHAR(25) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	CONSTRAINT pk_drug_enzyme_gene_sequence PRIMARY KEY (gene_sequence, sequence_format, id, primary_drugbank_id),
	CONSTRAINT fk_enzyme_id_primary_drugbank_id FOREIGN KEY (id, primary_drugbank_id)
		REFERENCES DrugEnzyme(pk_drug_enzyme),
	CONSTRAINT fk_primary_drugbank_id FOREIGN KEY (primary_drugbank_id)
		REFERENCES Drug(primary_drugbank_id)
);

CREATE TABLE DrugEnzymePfam
(
	name					VARCHAR(100) NOT NULL,
	identifier				VARCHAR(25) NOT NULL,
	id						VARCHAR(25) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	CONSTRAINT pk_drug_enzyme_pfam PRIMARY KEY (name, identifier, id, primary_drugbank_id),
	CONSTRAINT fk_enzyme_id_primary_drugbank_id FOREIGN KEY (id, primary_drugbank_id)
		REFERENCES DrugEnzyme(pk_drug_enzyme),
	CONSTRAINT fk_primary_drugbank_id FOREIGN KEY (primary_drugbank_id)
		REFERENCES Drug(primary_drugbank_id)
);

CREATE TABLE DrugEnzymeGOClassifier
(
	category				VARCHAR(100) NOT NULL,
	description				VARCHAR(1000) NOT NULL,
	id						VARCHAR(25) NOT NULL,
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	CONSTRAINT pk_drug_enzyme_go_classifier PRIMARY KEY (category, description, id, primary_drugbank_id),
	CONSTRAINT fk_enzyme_id_primary_drugbank_id FOREIGN KEY (id, primary_drugbank_id)
		REFERENCES DrugEnzyme(pk_drug_enzyme),
	CONSTRAINT fk_primary_drugbank_id FOREIGN KEY (primary_drugbank_id)
		REFERENCES Drug(primary_drugbank_id)
);

CREATE TABLE DrugCarrier
(
	primary_drugbank_id		VARCHAR(10) NOT NULL,
	position				INT,
	id						VARCHAR(25) NOT NULL,
	name					VARCHAR(100) NOT NULL,
	organism				VARCHAR(50) NOT NULL,
	known_action			VARCHAR(100) NOT NULL,
	CONSTRAINT pk_drug_carrier PRIMARY KEY (id, primary_drugbank_id),
	CONSTRAINT fk_primary_drugbank_id FOREIGN KEY (primary_drugbank_id)
		REFERENCES Drug(primary_drugbank_id)
);

CREATE TABLE DrugCarrierAction
(
);

CREATE TABLE DrugCarrierReference
(
);

CREATE TABLE DrugCarrierPolypeptide
(
);

CREATE TABLE DrugCarrierPolypeptideTransmembraneRegion
(
);

CREATE TABLE DrugCarrierPolypeptideSynonym
(
);

CREATE TABLE DrugCarrierAminoAcidSequence
(
);

CREATE TABLE DrugCarrerGeneSequence
(
);

CREATE TABLE DrugCarrierPfam
(
);

CREATE TABLE DrugCarrierGOClassifier
(
);

CREATE TABLE DrugTransporter
(
);

CREATE TABLE DrugTransporterAction
(
);

CREATE TABLE DrugTransporterReference
(
);

CREATE TABLE DrugTransporterPolypeptide
(
);

CREATE TABLE DrugTransporterPolypeptideTransmembraneRegion
(
);

CREATE TABLE DrugTransporterPolypeptideExternalIdentifier
(
);

CREATE TABLE DrugTransporterPolypeptideSynonym
(
);

CREATE TABLE DrugTransporterAminoAcidSequence
(
);

CREATE TABLE DrugTransporterGeneSequence
(
);

CREATE TABLE DrugTransporterPfam
(
);

CREATE TABLE DrugTransporterGOClassifier
(
);