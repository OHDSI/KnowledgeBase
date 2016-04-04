LOAD DATA LOCAL INFILE 'DRUGBANK_DRUGS.rrf' INTO TABLE drugs
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@primary_drugbank_id, @name, @description, @cas_number, @synthesis_reference, @indication, @pharmacodynamics, @mechanism_of_action, @toxicity, @metabolism, @absorption, @half_life, @protein_binding, @route_of_elimination, @drug_type, @created, @updated)
SET		primary_drugbank_id =@primary_drugbank_id,
		name =@name,
		cas_number =@cas_number,
		synthesis_reference =@synthesis_reference,
		indication =@indication,
		pharmacodynamics =@pharmacodynamics,
		mechanism_of_action =@mechanism_of_action,
		toxicity =@toxicity,
		metabolism =@metabolism,
		absorption =@absorption,
		half_life =@half_life,
		protein_binding =@protein_binding,
		route_of_elimination =@route_of_elimination,
		drug_type =@drug_type,
		created =@created,
		updated =@updated;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_ALT_IDS.rrf' INTO TABLE drug_alt_ids
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@secondary_drugbank_id, @primary_drugbank_id)
SET		primary_drugbank_id =@primary_drugbank_id,
		secondary_drugbank_id =@secondary_drugbank_id;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_GROUPS.rrf' INTO TABLE drug_groups
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@drug_group, @primary_drugbank_id)
SET		drug_group =@drug_group,
		primary_drugbank_id =@primary_drugbank_id;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_GEN_REFS.rrf' INTO TABLE drug_general_references
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@general_reference, @primary_drugbank_id)
SET		general_reference =@general_reference,
		primary_drugbank_id =@primary_drugbank_id;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_VOL_DIST.rrf' INTO TABLE drug_volumes_of_distribution
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@volume_of_distribution, @primary_drugbank_id)
SET		volume_of_distribution =@volume_of_distribution,
		primary_drugbank_id =@primary_drugbank_id;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_CLEARANCES.rrf' INTO TABLE drug_clearances
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@clearance, @primary_drugbank_id)
SET		clearance =@clearance,
		primary_drugbank_id =@primary_drugbank_id;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_CLASSIFICATIONS.rrf' INTO TABLE drug_classifications
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@primary_drugbank_id, @description, @direct_parent, @kingdom, @superclass, @drug_class, @subclass)
SET		primary_drugbank_id =@primary_drugbank_id,
		description =@description,
		direct_parent =@direct_parent,
		kingdom =@kingdom,
		superclass =@superclass,
		drug_class =@drug_class,
		subclass =@subclass;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_CLASSIFICATION_ALT_PARENTS.rrf' INTO TABLE drug_classification_alt_parents
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@alternative_parent, @primary_drugbank_id)
SET		alternative_parent =@alternative_parent,
		primary_drugbank_id =@primary_drugbank_id;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_CLASSIFICATION_SUBSTIT.rrf' INTO TABLE drug_classification_substituents
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@substituent, @primary_drugbank_id)
SET		substituent =@substituent,
		primary_drugbank_id =@primary_drugbank_id;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_SALTS.rrf' INTO TABLE drug_salts
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@primary_drugbank_id_salt, @primary_drugbank_id, @name, @cas_number, @inchikey)
SET		primary_drugbank_id_salt =@primary_drugbank_id_salt,
		primary_drugbank_id =@primary_drugbank_id,
		name =@name,
		cas_number =@cas_number,
		inchikey =@inchikey;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_SYN.rrf' INTO TABLE drug_synonyms
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@drug_synonym, @synonym_language, @coder, @primary_drugbank_id)
SET		drug_synonym =@drug_synonym,
		synonym_language =@synonym_language,
		coder =@coder,
		primary_drugbank_id =@primary_drugbank_id;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_PROD.rrf' INTO TABLE drug_products
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@name, @ndc_id, @ndc_product_code, @dpd_id, @started_marketing_on, @ended_marketing_on, @dosage_form, @strength, @route, @fda_application_number, @generic, @over_the_counter, @approved, @country, @source, @primary_drugbank_id)
SET		name =@name,
		ndc_id =@ndc_id,
		ndc_product_code =@ndc_product_code,
		dpd_id =@dpd_id,
		started_marketing_on =@started_marketing_on,
		ended_marketing_on =@ended_marketing_on,
		dosage_form =@dosage_form,
		strength =@strength,
		route =@route,
		fda_application_number =@fda_application_number,
		generic =@generic,
		over_the_counter =@over_the_counter,
		approved =@approved,
		country =@country,
		source =@source,
		primary_drugbank_id =@primary_drugbank_id;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_INT_BRANDS.rrf' INTO TABLE drug_international_brands
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@name, @company, @primary_drugbank_id)
SET		name =@name,
		company =@company,
		primary_drugbank_id =@primary_drugbank_id;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_MIX.rrf' INTO TABLE drug_mixtures
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@name, @ingredients, @primary_drugbank_id)
SET		name =@name,
		company =@company,
		primary_drugbank_id =@primary_drugbank_id;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_PACK.rrf' INTO TABLE drug_packagers
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@name, @url, @primary_drugbank_id)
SET		name =@name,
		url =@url,
		primary_drugbank_id =@primary_drugbank_id;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_MANUFACTURERS.rrf' INTO TABLE drug_manufacturers
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@name, @generic, @primary_drugbank_id)
SET		name =@name,
		generic =@generic,
		primary_drugbank_id =@primary_drugbank_id;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_PRICES.rrf' INTO TABLE drug_prices
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@description, @unit, @primary_drugbank_id)
SET		description =@description,
		unit =@unit,
		primary_drugbank_id =@primary_drugbank_id;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_COSTS.rrf' INTO TABLE drug_costs
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@cost, @currency, @description, @unit, @primary_drugbank_id)
SET		cost =@cost,
		currency =@currency,
		description =@description,
		unit =@unit,
		primary_drugbank_id =@primary_drugbank_id;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_CATEGORIES.rrf' INTO TABLE drug_categories
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@name, @primary_drugbank_id)
SET		name =@name,
		primary_drugbank_id =@primary_drugbank_id;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_MESH.rrf' INTO TABLE drug_mesh_ids
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@mesh_id, @name, @primary_drugbank_id)
SET		mesh_id =@mesh_id,
		name =@name,
		primary_drugbank_id =@primary_drugbank_id;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_AFFECTED_ORGANISMS.rrf' INTO TABLE drug_affected_organisms
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@name, @primary_drugbank_id)
SET		name =@name,
		primary_drugbank_id =@primary_drugbank_id;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_DOSAGES.rrf' INTO TABLE drug_dosages
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@form, @route, @strength, @primary_drugbank_id)
SET		form =@form,
		route =@route,
		strength =@strength;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_ATC_CODES.rrf' INTO TABLE drug_atc_codes
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@code, @primary_drugbank_id)
SET		code =@code,
		primary_drugbank_id =@primary_drugbank_id;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_ATC_CODE_LVL.rrf' INTO TABLE drug_atc_code_levels
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@level_code, @name, @code, @primary_drugbank_id)
SET		level_code =@level_code,
		name =@name,
		code =@code,
		primary_drugbank_id =@primary_drugbank_id;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_AHFS.rrf' INTO TABLE drug_ahfs_codes
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@ahfs_code, @primary_drugbank_id)
SET		ahfs_code =@ahfs_code,
		primary_drugbank_id =@primary_drugbank_id;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_PATENTS.rrf' INTO TABLE drug_patents
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@patent_number, @country, @approved, @expires, @primary_drugbank_id)
SET		patent_number =@patent_number,
		country =@country,
		approved =@approved,
		expires =@expires,
		primary_drugbank_id =@primary_drugbank_id;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_FOOD_INT.rrf' INTO TABLE drug_food_interactions
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@name, @primary_drugbank_id)
SET		name =@name,
		primary_drugbank_id =@primary_drugbank_id;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_DRUG_INT.rrf' INTO TABLE drug_drug_interactions
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@primary_drugbank_id, @secondary_drugbank_id, @name, @description)
SET		primary_drugbank_id =@primary_drugbank_id,
		secondary_drugbank_id =@secondary_drugbank_id,
		name =@name,
		description =@description;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_SEQ.rrf' INTO TABLE drug_sequences
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@drug_sequence, @sequence_format, @primary_drugbank_id)
SET		primary_drugbank_id =@primary_drugbank_id,
		sequence_format =@sequence_format,
		primary_drugbank_id =@primary_drugbank_id;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_PROPS.rrf' INTO TABLE drug_properties
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@kind, @property_value, @source, @primary_drugbank_id, @experimental, @calculated)
SET		kind =@kind,
		property_value =@property_value,
		source =@source,
		primary_drugbank_id =@primary_drugbank_id,
		experimental =@experimental,
		calculated =@calculated;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_EXT_IDS.rrf' INTO TABLE drug_external_identifiers
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@external_resource, @identifier, @primary_drugbank_id)
SET		external_resource =@external_resource,
		identifier =@identifier,
		primary_drugbank_id =@primary_drugbank_id;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_EXT_LINKS.rrf' INTO TABLE drug_external_links
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@external_resource, @url, @primary_drugbank_id)
SET		external_resource =@external_resource,
		url =@url,
		primary_drugbank_id =@primary_drugbank_id;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_PATHWAYS.rrf' INTO TABLE drug_pathways
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@primary_drugbank_id)
SET		primary_drugbank_id =@primary_drugbank_id;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_RXNS.rrf' INTO TABLE drug_reactions
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@reaction_sequence, @primary_drugbank_id)
SET		reaction_sequence =@reaction_sequence,
		primary_drugbank_id =@primary_drugbank_id;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_RXN_EL.rrf' INTO TABLE drug_reaction_elements
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@primary_drugbank_id, @secondary_drugbank_id, @name, @left_element, @right_element, @reaction_sequence)
SET		primary_drugbank_id =@primary_drugbank_id,
		secondary_drugbank_id =@secondary_drugbank_id,
		name =@name,
		left_element =@left_element,
		right_element =@right_element,
		reaction_sequence =@reaction_sequence;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_RXN_ENZYMES.rrf' INTO TABLE drug_reaction_enzymes
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@primary_drugbank_id, @secondary_drugbank_id, @reaction_sequence, @name, @uniprot_id)
SET		primary_drugbank_id =@primary_drugbank_id,
		secondary_drugbank_id =@secondary_drugbank_id,
		reaction_sequence =@reaction_sequence,
		name =@name,
		uniprot_id =@uniprot_id;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_SNP_EFF.rrf' INTO TABLE drug_snp_effects
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@primary_drugbank_id, @protein_name, @gene_symbol, @uniprot_id, @rs_id, @allele, @defining_change, @description, @pubmed_id)
SET		primary_drugbank_id =@primary_drugbank_id,
		protein_name =@protein_name,
		gene_symbol =@gene_symbol,
		uniprot_id =@uniprot_id,
		rs_id =@rs_id,
		allele =@allele,
		defining_change =@defining_change,
		description =@description,
		pubmed_id =@pubmed_id;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_SNP_ADV_DRUG_RXNS.rrf' INTO TABLE drug_snp_adverse_drug_reactions
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@primary_drugbank_id, @protein_name, @gene_symbol, @uniprot_id, @rs_id, @allele, @adverse_reaction, @description, @pubmed_id)
SET		primary_drugbank_id =@primary_drugbank_id,
		protein_name =@protein_name,
		gene_symbol =@gene_symbol,
		uniprot_id =@uniprot_id,
		rs_id =@rs_id,
		allele =@allele,
		adverse_reaction =@adverse_reaction,
		description =@description,
		pubmed_id =@pubmed_id;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_ENZYMES.rrf' INTO TABLE drug_enzymes
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@primary_drugbank_id, @position, @id, @name, @organism, @known_action, @inhibition_strength, @induction_strength)
SET		primary_drugbank_id =@primary_drugbank_id,
		position =@position,
		id =@id,
		name =@name,
		organism =@organism,
		known_action =@known_action,
		inhibition_strength =@inhibition_strength,
		induction_strength =@induction_strength;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_ENZYME_ACTIONS' INTO TABLE drug_enzyme_actions
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@primary_drugbank_id, @id, @action)
SET		primary_drugbank_id =@primary_drugbank_id,
		id =@id,
		action =@action;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_ENZYME_REFS.rrf' INTO TABLE drug_enzyme_references
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@primary_drugbank_id, @id, @reference)
SET		primary_drugbank_id =@primary_drugbank_id,
		id =@id,
		reference =@reference;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_ENZYME_POLYPEPTIDES.rrf' INTO TABLE drug_enzyme_polypeptides
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@polypeptide_id, @polypeptide_source, @name, @general_function, @specific_function, @id, @primary_drugbank_id, @gene_name, @locus, @cellular_location, @signal_regions_lower, @signal_regions_upper, @theoretical_pi, @molecular_weight, @chromosome_location, @organism_name, @organism_ncbi_taxonomy_id)
SET		polypeptide_id =@polypeptide_id,
		polypeptide_source =@polypeptide_source,
		name =@name,
		general_function =@general_function,
		specific_function =@specific_function,
		id =@id,
		primary_drugbank_id =@primary_drugbank_id,
		gene_name =@gene_name,
		locus =@locus,
		cellular_location =@cellular_location,
		signal_regions_lower =@signal_regions_lower,
		signal_regions_upper =@signal_regions_upper,
		theoretical_pi =@theoretical_pi,
		molecular_weight =@molecular_weight,
		chromosome_location =@chromosome_location,
		organism_name =@organism_name,
		organism_ncbi_taxonomy_id =@organism_ncbi_taxonomy_id;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_ENZYME_POLYPEPTIDE_TRANSMEM_REGIONS.rrf' INTO TABLE drug_enzyme_polypeptide_transmembrane_regions
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@polypeptide_id, @polypeptide_source, @id, @primary_drugbank_id, @transmembrane_region)
SET		polypeptide_id =@polypeptide_id,
		polypeptide_source =@polypeptide_source,
		id =@id,
		primary_drugbank_id =@primary_drugbank_id,
		transmembrane_region =@transmembrane_region;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_ENZYME_EXT_IDS.rrf' INTO TABLE drug_enzyme_polypeptide_external_identifiers
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@external_resource, @identifier, @polypeptide_id, @polypeptide_source, @id, @primary_drugbank_id)
SET		external_resource =@external_resource,
		identifier =@identifier,
		polypeptide_id =@polypeptide_id,
		polypeptide_source =@polypeptide_source
		id =@id,
		primary_drugbank_id =@primary_drugbank_id;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_ENZYME_SYN.rrf' INTO TABLE drug_enzyme_polypeptide_synonyms
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@polypeptide_synonym, @polypeptide_id, @polypeptide_source, @id, @primary_drugbank_id)
SET		polypeptide_synonym =@polypeptide_synonym,
		polypeptide_id =@polypeptide_id,
		polypeptide_source =@polypeptide_source,
		id =@id,
		primary_drugbank_id =@primary_drugbank_id;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_ENZYME_AA_SEQ.rrf' INTO TABLE drug_enzyme_polypeptide_amino_acid_sequences
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@amino_acid_sequence, @sequence_format, @polypeptide_id, @polypeptide_source, @id, @primary_drugbank_id)
SET		amino_acid_sequence =@gene_sequence,
		sequence_format =@sequence_format,
		polypeptide_id =@polypeptide_id,
		polypeptide_source =@polypeptide_source,
		primary_drugbank_id =@primary_drugbank_id;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_ENZYMES_GENE_SEQ.rrf' INTO TABLE drug_enzyme_polypeptide_gene_sequences
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@gene_sequence, @sequence_format, @polypeptide_id, @polypeptide_source, @id, @primary_drugbank_id)
SET		gene_sequence =@gene_sequence,
		sequence_format =@sequence_format,
		polypeptide_id =@polypeptide_id,
		polypeptide_source =@polypeptide_source,
		primary_drugbank_id =@primary_drugbank_id;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_ENZYME_PFAMS.rrf' INTO TABLE drug_enzyme_polypeptide_pfams
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@name, @identifier, @polypeptide_id, @polypeptide_source, @id, @primary_drugbank_id)
SET		name =@name,
		identifier =@identifier,
		polypeptide_id =@polypeptide_id,
		polypeptide_source =@polypeptide_source,
		id =@id,
		primary_drugbank_id =@primary_drugbank_id;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_ENZYME_GO_CLASSIFIERS.rrf' INTO TABLE drug_enzyme_polypeptide_go_classifiers
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@category, @description, @polypeptide_id, @polypeptide_source, @id, @primary_drugbank_id)
SET		category =@category,
		description =@description,
		polypeptide_id =@polypeptide_id,
		polypeptide_source =@polypeptide_source,
		id =@id,
		primary_drugbank_id =@primary_drugbank_id;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_TARGETS.rrf' INTO TABLE drug_targets
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@primary_drugbank_id, @position, @id, @name, @organism, @known_action, @inhibition_strength, @induction_strength)
SET		primary_drugbank_id =@primary_drugbank_id,
		position =@position,
		id =@id,
		name =@name,
		organism =@organism,
		known_action =@known_action,
		inhibition_strength =@inhibition_strength,
		induction_strength =@induction_strength;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_TARGET_ACTIONS' INTO TABLE drug_target_actions
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@primary_drugbank_id, @id, @action)
SET		primary_drugbank_id =@primary_drugbank_id,
		id =@id,
		action =@action;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_TARGET_REFS.rrf' INTO TABLE drug_target_references
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@primary_drugbank_id, @id, @reference)
SET		primary_drugbank_id =@primary_drugbank_id,
		id =@id,
		reference =@reference;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_TARGET_POLYPEPTIDES.rrf' INTO TABLE drug_target_polypeptides
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@polypeptide_id, @polypeptide_source, @name, @general_function, @specific_function, @id, @primary_drugbank_id, @gene_name, @locus, @cellular_location, @signal_regions_lower, @signal_regions_upper, @theoretical_pi, @molecular_weight, @chromosome_location, @organism_name, @organism_ncbi_taxonomy_id)
SET		polypeptide_id =@polypeptide_id,
		polypeptide_source =@polypeptide_source,
		name =@name,
		general_function =@general_function,
		specific_function =@specific_function,
		id =@id,
		primary_drugbank_id =@primary_drugbank_id,
		gene_name =@gene_name,
		locus =@locus,
		cellular_location =@cellular_location,
		signal_regions_lower =@signal_regions_lower,
		signal_regions_upper =@signal_regions_upper,
		theoretical_pi =@theoretical_pi,
		molecular_weight =@molecular_weight,
		chromosome_location =@chromosome_location,
		organism_name =@organism_name,
		organism_ncbi_taxonomy_id =@organism_ncbi_taxonomy_id;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_TARGET_POLYPEPTIDE_TRANSMEM_REGIONS.rrf' INTO TABLE drug_target_polypeptide_transmembrane_regions
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@polypeptide_id, @polypeptide_source, @id, @primary_drugbank_id, @transmembrane_region)
SET		polypeptide_id =@polypeptide_id,
		polypeptide_source =@polypeptide_source,
		id =@id,
		primary_drugbank_id =@primary_drugbank_id,
		transmembrane_region =@transmembrane_region;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_TARGET_EXT_IDS.rrf' INTO TABLE drug_target_polypeptide_external_identifiers
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@external_resource, @identifier, @polypeptide_id, @polypeptide_source, @id, @primary_drugbank_id)
SET		external_resource =@external_resource,
		identifier =@identifier,
		polypeptide_id =@polypeptide_id,
		polypeptide_source =@polypeptide_source
		id =@id,
		primary_drugbank_id =@primary_drugbank_id;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_TARGET_SYN.rrf' INTO TABLE drug_target_polypeptide_synonyms
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@polypeptide_synonym, @polypeptide_id, @polypeptide_source, @id, @primary_drugbank_id)
SET		polypeptide_synonym =@polypeptide_synonym,
		polypeptide_id =@polypeptide_id,
		polypeptide_source =@polypeptide_source,
		id =@id,
		primary_drugbank_id =@primary_drugbank_id;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_TARGET_AA_SEQ.rrf' INTO TABLE drug_target_polypeptide_amino_acid_sequences
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@amino_acid_sequence, @sequence_format, @polypeptide_id, @polypeptide_source, @id, @primary_drugbank_id)
SET		amino_acid_sequence =@gene_sequence,
		sequence_format =@sequence_format,
		polypeptide_id =@polypeptide_id,
		polypeptide_source =@polypeptide_source,
		primary_drugbank_id =@primary_drugbank_id;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_TARGETS_GENE_SEQ.rrf' INTO TABLE drug_target_polypeptide_gene_sequences
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@gene_sequence, @sequence_format, @polypeptide_id, @polypeptide_source, @id, @primary_drugbank_id)
SET		gene_sequence =@gene_sequence,
		sequence_format =@sequence_format,
		polypeptide_id =@polypeptide_id,
		polypeptide_source =@polypeptide_source,
		primary_drugbank_id =@primary_drugbank_id;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_TARGET_PFAMS.rrf' INTO TABLE drug_target_polypeptide_pfams
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@name, @identifier, @polypeptide_id, @polypeptide_source, @id, @primary_drugbank_id)
SET		name =@name,
		identifier =@identifier,
		polypeptide_id =@polypeptide_id,
		polypeptide_source =@polypeptide_source,
		id =@id,
		primary_drugbank_id =@primary_drugbank_id;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_TARGET_GO_CLASSIFIERS.rrf' INTO TABLE drug_target_polypeptide_go_classifiers
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@category, @description, @polypeptide_id, @polypeptide_source, @id, @primary_drugbank_id)
SET		category =@category,
		description =@description,
		polypeptide_id =@polypeptide_id,
		polypeptide_source =@polypeptide_source,
		id =@id,
		primary_drugbank_id =@primary_drugbank_id;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_CARRIERS.rrf' INTO TABLE drug_carriers
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@primary_drugbank_id, @position, @id, @name, @organism, @known_action, @inhibition_strength, @induction_strength)
SET		primary_drugbank_id =@primary_drugbank_id,
		position =@position,
		id =@id,
		name =@name,
		organism =@organism,
		known_action =@known_action,
		inhibition_strength =@inhibition_strength,
		induction_strength =@induction_strength;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_CARRIER_ACTIONS' INTO TABLE drug_carrier_actions
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@primary_drugbank_id, @id, @action)
SET		primary_drugbank_id =@primary_drugbank_id,
		id =@id,
		action =@action;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_CARRIER_REFS.rrf' INTO TABLE drug_carrier_references
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@primary_drugbank_id, @id, @reference)
SET		primary_drugbank_id =@primary_drugbank_id,
		id =@id,
		reference =@reference;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_CARRIER_POLYPEPTIDES.rrf' INTO TABLE drug_carrier_polypeptides
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@polypeptide_id, @polypeptide_source, @name, @general_function, @specific_function, @id, @primary_drugbank_id, @gene_name, @locus, @cellular_location, @signal_regions_lower, @signal_regions_upper, @theoretical_pi, @molecular_weight, @chromosome_location, @organism_name, @organism_ncbi_taxonomy_id)
SET		polypeptide_id =@polypeptide_id,
		polypeptide_source =@polypeptide_source,
		name =@name,
		general_function =@general_function,
		specific_function =@specific_function,
		id =@id,
		primary_drugbank_id =@primary_drugbank_id,
		gene_name =@gene_name,
		locus =@locus,
		cellular_location =@cellular_location,
		signal_regions_lower =@signal_regions_lower,
		signal_regions_upper =@signal_regions_upper,
		theoretical_pi =@theoretical_pi,
		molecular_weight =@molecular_weight,
		chromosome_location =@chromosome_location,
		organism_name =@organism_name,
		organism_ncbi_taxonomy_id =@organism_ncbi_taxonomy_id;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_CARRIER_POLYPEPTIDE_TRANSMEM_REGIONS.rrf' INTO TABLE drug_carrier_polypeptide_transmembrane_regions
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@polypeptide_id, @polypeptide_source, @id, @primary_drugbank_id, @transmembrane_region)
SET		polypeptide_id =@polypeptide_id,
		polypeptide_source =@polypeptide_source,
		id =@id,
		primary_drugbank_id =@primary_drugbank_id,
		transmembrane_region =@transmembrane_region;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_CARRIER_EXT_IDS.rrf' INTO TABLE drug_carrier_polypeptide_external_identifiers
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@external_resource, @identifier, @polypeptide_id, @polypeptide_source, @id, @primary_drugbank_id)
SET		external_resource =@external_resource,
		identifier =@identifier,
		polypeptide_id =@polypeptide_id,
		polypeptide_source =@polypeptide_source
		id =@id,
		primary_drugbank_id =@primary_drugbank_id;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_CARRIER_SYN.rrf' INTO TABLE drug_carrier_polypeptide_synonyms
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@polypeptide_synonym, @polypeptide_id, @polypeptide_source, @id, @primary_drugbank_id)
SET		polypeptide_synonym =@polypeptide_synonym,
		polypeptide_id =@polypeptide_id,
		polypeptide_source =@polypeptide_source,
		id =@id,
		primary_drugbank_id =@primary_drugbank_id;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_CARRIER_AA_SEQ.rrf' INTO TABLE drug_carrier_polypeptide_amino_acid_sequences
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@amino_acid_sequence, @sequence_format, @polypeptide_id, @polypeptide_source, @id, @primary_drugbank_id)
SET		amino_acid_sequence =@gene_sequence,
		sequence_format =@sequence_format,
		polypeptide_id =@polypeptide_id,
		polypeptide_source =@polypeptide_source,
		primary_drugbank_id =@primary_drugbank_id;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_CARRIERS_GENE_SEQ.rrf' INTO TABLE drug_carrier_polypeptide_gene_sequences
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@gene_sequence, @sequence_format, @polypeptide_id, @polypeptide_source, @id, @primary_drugbank_id)
SET		gene_sequence =@gene_sequence,
		sequence_format =@sequence_format,
		polypeptide_id =@polypeptide_id,
		polypeptide_source =@polypeptide_source,
		primary_drugbank_id =@primary_drugbank_id;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_CARRIER_PFAMS.rrf' INTO TABLE drug_carrier_polypeptide_pfams
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@name, @identifier, @polypeptide_id, @polypeptide_source, @id, @primary_drugbank_id)
SET		name =@name,
		identifier =@identifier,
		polypeptide_id =@polypeptide_id,
		polypeptide_source =@polypeptide_source,
		id =@id,
		primary_drugbank_id =@primary_drugbank_id;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_CARRIER_GO_CLASSIFIERS.rrf' INTO TABLE drug_carrier_polypeptide_go_classifiers
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@category, @description, @polypeptide_id, @polypeptide_source, @id, @primary_drugbank_id)
SET		category =@category,
		description =@description,
		polypeptide_id =@polypeptide_id,
		polypeptide_source =@polypeptide_source,
		id =@id,
		primary_drugbank_id =@primary_drugbank_id;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_TRANSPORTERS.rrf' INTO TABLE drug_transporters
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@primary_drugbank_id, @position, @id, @name, @organism, @known_action, @inhibition_strength, @induction_strength)
SET		primary_drugbank_id =@primary_drugbank_id,
		position =@position,
		id =@id,
		name =@name,
		organism =@organism,
		known_action =@known_action,
		inhibition_strength =@inhibition_strength,
		induction_strength =@induction_strength;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_TRANSPORTER_ACTIONS' INTO TABLE drug_transporter_actions
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@primary_drugbank_id, @id, @action)
SET		primary_drugbank_id =@primary_drugbank_id,
		id =@id,
		action =@action;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_TRANSPORTER_REFS.rrf' INTO TABLE drug_transporter_references
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@primary_drugbank_id, @id, @reference)
SET		primary_drugbank_id =@primary_drugbank_id,
		id =@id,
		reference =@reference;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_TRANSPORTER_POLYPEPTIDES.rrf' INTO TABLE drug_transporter_polypeptides
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@polypeptide_id, @polypeptide_source, @name, @general_function, @specific_function, @id, @primary_drugbank_id, @gene_name, @locus, @cellular_location, @signal_regions_lower, @signal_regions_upper, @theoretical_pi, @molecular_weight, @chromosome_location, @organism_name, @organism_ncbi_taxonomy_id)
SET		polypeptide_id =@polypeptide_id,
		polypeptide_source =@polypeptide_source,
		name =@name,
		general_function =@general_function,
		specific_function =@specific_function,
		id =@id,
		primary_drugbank_id =@primary_drugbank_id,
		gene_name =@gene_name,
		locus =@locus,
		cellular_location =@cellular_location,
		signal_regions_lower =@signal_regions_lower,
		signal_regions_upper =@signal_regions_upper,
		theoretical_pi =@theoretical_pi,
		molecular_weight =@molecular_weight,
		chromosome_location =@chromosome_location,
		organism_name =@organism_name,
		organism_ncbi_taxonomy_id =@organism_ncbi_taxonomy_id;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_TRANSPORTER_POLYPEPTIDE_TRANSMEM_REGIONS.rrf' INTO TABLE drug_transporter_polypeptide_transmembrane_regions
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@polypeptide_id, @polypeptide_source, @id, @primary_drugbank_id, @transmembrane_region)
SET		polypeptide_id =@polypeptide_id,
		polypeptide_source =@polypeptide_source,
		id =@id,
		primary_drugbank_id =@primary_drugbank_id,
		transmembrane_region =@transmembrane_region;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_TRANSPORTER_EXT_IDS.rrf' INTO TABLE drug_transporter_polypeptide_external_identifiers
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@external_resource, @identifier, @polypeptide_id, @polypeptide_source, @id, @primary_drugbank_id)
SET		external_resource =@external_resource,
		identifier =@identifier,
		polypeptide_id =@polypeptide_id,
		polypeptide_source =@polypeptide_source
		id =@id,
		primary_drugbank_id =@primary_drugbank_id;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_TRANSPORTER_SYN.rrf' INTO TABLE drug_transporter_polypeptide_synonyms
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@polypeptide_synonym, @polypeptide_id, @polypeptide_source, @id, @primary_drugbank_id)
SET		polypeptide_synonym =@polypeptide_synonym,
		polypeptide_id =@polypeptide_id,
		polypeptide_source =@polypeptide_source,
		id =@id,
		primary_drugbank_id =@primary_drugbank_id;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_TRANSPORTER_AA_SEQ.rrf' INTO TABLE drug_transporter_polypeptide_amino_acid_sequences
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@amino_acid_sequence, @sequence_format, @polypeptide_id, @polypeptide_source, @id, @primary_drugbank_id)
SET		amino_acid_sequence =@gene_sequence,
		sequence_format =@sequence_format,
		polypeptide_id =@polypeptide_id,
		polypeptide_source =@polypeptide_source,
		primary_drugbank_id =@primary_drugbank_id;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_TRANSPORTERS_GENE_SEQ.rrf' INTO TABLE drug_transporter_polypeptide_gene_sequences
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@gene_sequence, @sequence_format, @polypeptide_id, @polypeptide_source, @id, @primary_drugbank_id)
SET		gene_sequence =@gene_sequence,
		sequence_format =@sequence_format,
		polypeptide_id =@polypeptide_id,
		polypeptide_source =@polypeptide_source,
		primary_drugbank_id =@primary_drugbank_id;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_TRANSPORTER_PFAMS.rrf' INTO TABLE drug_transporter_polypeptide_pfams
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@name, @identifier, @polypeptide_id, @polypeptide_source, @id, @primary_drugbank_id)
SET		name =@name,
		identifier =@identifier,
		polypeptide_id =@polypeptide_id,
		polypeptide_source =@polypeptide_source,
		id =@id,
		primary_drugbank_id =@primary_drugbank_id;

LOAD DATA LOCAL INFILE 'DRUGBANK_DRUG_TRANSPORTER_GO_CLASSIFIERS.rrf' INTO TABLE drug_transporter_polypeptide_go_classifiers
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
(@category, @description, @polypeptide_id, @polypeptide_source, @id, @primary_drugbank_id)
SET		category =@category,
		description =@description,
		polypeptide_id =@polypeptide_id,
		polypeptide_source =@polypeptide_source,
		id =@id,
		primary_drugbank_id =@primary_drugbank_id;