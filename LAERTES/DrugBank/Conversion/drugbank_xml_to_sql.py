#
# The purpose of this file is to convert XML data from DrugBank
# into SQL which can easily be uploaded to relational database.
#
# CHANGE TO POSTGRESQL (JUST RELATIONAL TABLE)

# There is an issue with " and ' within the references... Figure out how to escape both.

import os
import sys
import xml.etree.ElementTree as ET

source_xml_file = 'drugbank.xml'

# delete the other python file.
outfile_drugs = open('DRUGBANK_DRUGS.rrf', 'w', encoding='utf-8')
outfile_drug_alt_ids = open('DRUGBANK_DRUG_ALT_IDS.rrf', 'w', encoding='utf-8')
outfile_drug_groups = open('DRUGBANK_DRUG_GROUPS.rrf', 'w', encoding='utf-8')
outfile_drug_general_references = open('DRUGBANK_DRUG_GEN_REFS.rrf', 'w', encoding='utf-8')
outfile_drug_volumes_of_distribution = open('DRUGBANK_DRUG_VOL_DIST.rrf', 'w', encoding='utf-8')
outfile_drug_clearances = open('DRUGBANK_DRUG_CLEARANCES.rrf', 'w', encoding='utf-8')
outfile_drug_classifications = open('DRUGBANK_DRUG_CLASSIFICATIONS.rrf', 'w', encoding='utf-8')
outfile_drug_classification_alt_parents = open('DRUGBANK_DRUG_CLASSIFICATION_ALT_PARENTS.rrf', 'w', encoding='utf-8')
outfile_drug_classification_substituents = open('DRUGBANK_DRUG_CLASSIFICATION_SUBSTIT.rrf', 'w', encoding='utf-8')
outfile_drug_salts = open('DRUGBANK_DRUG_SALTS.rrf', 'w', encoding='utf-8')
outfile_drug_synonyms = open('DRUGBANK_DRUG_SYN.rrf', 'w', encoding='utf-8')
outfile_drug_products = open('DRUGBANK_DRUG_PROD.rrf', 'w', encoding='utf-8')
outfile_drug_international_brands = open('DRUGBANK_DRUG_INT_BRANDS.rrf', 'w', encoding='utf-8')
outfile_drug_mixtures = open('DRUGBANK_DRUG_MIX.rrf', 'w', encoding='utf-8')
outfile_drug_packagers = open('DRUGBANK_DRUG_PACK.rrf', 'w', encoding='utf-8')
outfile_drug_manufacturers = open('DRUGBANK_DRUG_MANUFACTURERS.rrf', 'w', encoding='utf-8')
outfile_drug_prices = open('DRUGBANK_DRUG_PRICES.rrf', 'w', encoding='utf-8')
outfile_drug_costs = open('DRUGBANK_DRUG_COSTS.rrf', 'w', encoding='utf-8')
outfile_drug_categories = open('DRUGBANK_DRUG_CATEGORIES.rrf', 'w', encoding='utf-8')
outfile_drug_mesh_ids = open('DRUGBANK_DRUG_MESH.rrf', 'w', encoding='utf-8')
outfile_drug_affected_organisms = open('DRUGBANK_DRUG_AFFECTED_ORGANISMS.rrf', 'w', encoding='utf-8')
outfile_drug_dosages = open('DRUGBANK_DRUG_DOSAGES.rrf', 'w', encoding='utf-8')
outfile_drug_atc_codes = open('DRUGBANK_DRUG_ATC_CODES.rrf', 'w', encoding='utf-8')
outfile_drug_atc_code_levels = open('DRUGBANK_DRUG_ATC_CODE_LVL.rrf', 'w', encoding='utf-8')
outfile_drug_ahfs_codes = open('DRUGBANK_DRUG_AHFS.rrf', 'w', encoding='utf-8')
outfile_drug_patents = open('DRUGBANK_DRUG_PATENTS.rrf', 'w', encoding='utf-8')
outfile_drug_food_interactions = open('DRUGBANK_DRUG_FOOD_INT.rrf', 'w', encoding='utf-8')
outfile_drug_drug_interactions = open('DRUGBANK_DRUG_DRUG_INT.rrf', 'w', encoding='utf-8')
outfile_drug_sequences = open('DRUGBANK_DRUG_SEQ.rrf', 'w', encoding='utf-8')
outfile_drug_properties = open('DRUGBANK_DRUG_PROPS.rrf', 'w', encoding='utf-8')
outfile_drug_external_identifiers = open('DRUGBANK_DRUG_EXT_IDS.rrf', 'w', encoding='utf-8')
outfile_drug_external_links = open('DRUGBANK_DRUG_EXT_LINKS.rrf', 'w', encoding='utf-8')
outfile_drug_pathways = open('DRUGBANK_DRUG_PATHWAYS.rrf', 'w', encoding='utf-8')
outfile_drug_reactions = open('DRUGBANK_DRUG_RXNS.rrf', 'w', encoding='utf-8')
outfile_drug_reaction_elements = open('DRUGBANK_DRUG_RXN_EL.rrf', 'w', encoding='utf-8')
outfile_drug_reaction_enzymes = open('DRUGBANK_DRUG_RXN_ENZYMES.rrf', 'w', encoding='utf-8')
outfile_drug_snp_effects = open('DRUGBANK_DRUG_SNP_EFF.rrf', 'w', encoding='utf-8')
outfile_drug_snp_adverse_drug_reactions = open('DRUGBANK_DRUG_SNP_ADV_DRUG_RXNS.rrf', 'w', encoding='utf-8')

outfile_drug_enzymes = open('DRUGBANK_DRUG_ENZYMES.rrf', 'w', encoding='utf-8')
outfile_drug_enzyme_actions = open('DRUGBANK_DRUG_ENZYME_ACTIONS.rrf', 'w', encoding='utf-8')
outfile_drug_enzyme_references = open('DRUGBANK_DRUG_ENZYME_REFS.rrf', 'w', encoding='utf-8')
outfile_drug_enzyme_polypeptides = open('DRUGBANK_DRUG_ENZYME_POLYPEPTIDES.rrf', 'w', encoding='utf-8')
outfile_drug_enzyme_polypeptide_transmembrane_regions = open('DRUGBANK_DRUG_ENZYME_POLYPEPTIDE_TRANSMEM_REGIONS.rrf', 'w', encoding='utf-8')
outfile_drug_enzyme_polypeptide_external_identifiers = open('DRUGBANK_DRUG_ENZYME_EXT_IDS.rrf', 'w', encoding='utf-8')
outfile_drug_enzyme_polypeptide_synonyms = open('DRUGBANK_DRUG_ENZYME_SYN.rrf', 'w', encoding='utf-8')
outfile_drug_enzyme_polypeptide_amino_acid_sequences = open('DRUGBANK_DRUG_ENZYME_AA_SEQ.rrf', 'w', encoding='utf-8')
outfile_drug_enzyme_polypeptide_gene_sequences = open('DRUGBANK_DRUG_ENZYMES_GENE_SEQ.rrf', 'w', encoding='utf-8')
outfile_drug_enzyme_polypeptide_pfams = open('DRUGBANK_DRUG_ENZYME_PFAMS.rrf', 'w', encoding='utf-8')
outfile_drug_enzyme_polypeptide_go_classifiers = open('DRUGBANK_DRUG_ENZYME_GO_CLASSIFIERS.rrf', 'w', encoding='utf-8')

outfile_drug_transporters = open('DRUGBANK_DRUG_TRANSPORTERS.rrf', 'w', encoding='utf-8')
outfile_drug_transporter_actions = open('DRUGBANK_DRUG_TRANSPORTER_ACTIONS.rrf', 'w', encoding='utf-8')
outfile_drug_transporter_references = open('DRUGBANK_DRUG_TRANSPORTER_REFS.rrf', 'w', encoding='utf-8')
outfile_drug_transporter_polypeptides = open('DRUGBANK_DRUG_TRANSPORTER_POLYPEPTIDES.rrf', 'w', encoding='utf-8')
outfile_drug_transporter_polypeptide_transmembrane_regions = open('DRUGBANK_DRUG_TRANSPORTER_POLYPEPTIDE_TRANSMEM_REGIONS.rrf', 'w', encoding='utf-8')
outfile_drug_transporter_polypeptide_external_identifiers = open('DRUGBANK_DRUG_TRANSPORTER_EXT_IDS.rrf', 'w', encoding='utf-8')
outfile_drug_transporter_polypeptide_synonyms = open('DRUGBANK_DRUG_TRANSPORTER_SYN.rrf', 'w', encoding='utf-8')
outfile_drug_transporter_polypeptide_amino_acid_sequences = open('DRUGBANK_DRUG_TRANSPORTER_AA_SEQ.rrf', 'w', encoding='utf-8')
outfile_drug_transporter_polypeptide_gene_sequences = open('DRUGBANK_DRUG_TRANSPORTERS_GENE_SEQ.rrf', 'w', encoding='utf-8')
outfile_drug_transporter_polypeptide_pfams = open('DRUGBANK_DRUG_TRANSPORTER_PFAMS.rrf', 'w', encoding='utf-8')
outfile_drug_transporter_polypeptide_go_classifiers = open('DRUGBANK_DRUG_TRANSPORTER_GO_CLASSIFIERS.rrf', 'w', encoding='utf-8')

outfile_drug_carriers = open('DRUGBANK_DRUG_CARRIERS.rrf', 'w', encoding='utf-8')
outfile_drug_carrier_actions = open('DRUGBANK_DRUG_CARRIER_ACTIONS.rrf', 'w', encoding='utf-8')
outfile_drug_carrier_references = open('DRUGBANK_DRUG_CARRIER_REFS.rrf', 'w', encoding='utf-8')
outfile_drug_carrier_polypeptides = open('DRUGBANK_DRUG_CARRIER_POLYPEPTIDES.rrf', 'w', encoding='utf-8')
outfile_drug_carrier_polypeptide_transmembrane_regions = open('DRUGBANK_DRUG_CARRIER_POLYPEPTIDE_TRANSMEM_REGIONS.rrf', 'w', encoding='utf-8')
outfile_drug_carrier_polypeptide_external_identifiers = open('DRUGBANK_DRUG_CARRIER_EXT_IDS.rrf', 'w', encoding='utf-8')
outfile_drug_carrier_polypeptide_synonyms = open('DRUGBANK_DRUG_CARRIER_SYN.rrf', 'w', encoding='utf-8')
outfile_drug_carrier_polypeptide_amino_acid_sequences = open('DRUGBANK_DRUG_CARRIER_AA_SEQ.rrf', 'w', encoding='utf-8')
outfile_drug_carrier_polypeptide_gene_sequences = open('DRUGBANK_DRUG_CARRIERS_GENE_SEQ.rrf', 'w', encoding='utf-8')
outfile_drug_carrier_polypeptide_pfams = open('DRUGBANK_DRUG_CARRIER_PFAMS.rrf', 'w', encoding='utf-8')
outfile_drug_carrier_polypeptide_go_classifiers = open('DRUGBANK_DRUG_CARRIER_GO_CLASSIFIERS.rrf', 'w', encoding='utf-8')

outfile_drug_targets = open('DRUGBANK_DRUG_TARGETS.rrf', 'w', encoding='utf-8')
outfile_drug_target_actions = open('DRUGBANK_DRUG_TARGET_ACTIONS.rrf', 'w', encoding='utf-8')
outfile_drug_target_references = open('DRUGBANK_DRUG_TARGET_REFS.rrf', 'w', encoding='utf-8')
outfile_drug_target_polypeptides = open('DRUGBANK_DRUG_TARGET_POLYPEPTIDES.rrf', 'w', encoding='utf-8')
outfile_drug_target_polypeptide_transmembrane_regions = open('DRUGBANK_DRUG_TARGET_POLYPEPTIDE_TRANSMEM_REGIONS.rrf', 'w', encoding='utf-8')
outfile_drug_target_polypeptide_external_identifiers = open('DRUGBANK_DRUG_TARGET_EXT_IDS.rrf', 'w', encoding='utf-8')
outfile_drug_target_polypeptide_synonyms = open('DRUGBANK_DRUG_TARGET_SYN.rrf', 'w', encoding='utf-8')
outfile_drug_target_polypeptide_amino_acid_sequences = open('DRUGBANK_DRUG_TARGET_AA_SEQ.rrf', 'w', encoding='utf-8')
outfile_drug_target_polypeptide_gene_sequences = open('DRUGBANK_DRUG_TARGETS_GENE_SEQ.rrf', 'w', encoding='utf-8')
outfile_drug_target_polypeptide_pfams = open('DRUGBANK_DRUG_TARGET_PFAMS.rrf', 'w', encoding='utf-8')
outfile_drug_target_polypeptide_go_classifiers = open('DRUGBANK_DRUG_TARGET_GO_CLASSIFIERS.rrf', 'w', encoding='utf-8')





with open(source_xml_file, encoding = "utf8") as f:
  tree = ET.parse(f)
  root = tree.getroot()

  for i in root.getchildren():
    DRUG_TYPE = 'NULL'
    CREATED = 'NULL'
    UPDATED = 'NULL'
    NAME = 'NULL'
    DESCRIPTION = 'NULL'
    CAS_NUMBER = 'NULL'
    SYNTHESIS_REFERENCE = 'NULL'
    INDICATION = 'NULL'
    PHARMACODYNAMICS = 'NULL'
    PROTEIN_BINDING = 'NULL'
    drugbank_ids = []
    properties = []

    if(i.tag == '{http://www.drugbank.ca}drug'):

#
#	GETTING DRUGBANK DRUG TYPES
#
      if(i.attrib == 'type'):
        DRUG_TYPE = i.attrib['type'].rstrip()

#
#	GETTING DRUGBANK DRUG CREATED AT
#
      if(i.attrib == 'created'):
        CREATED = i.attrib['created'].rstrip()

#
#	GETTING DRUGBANK DRUG UPDATED AT
#
      if(i.attrib == 'updated'):
        UPDATED = i.attrib['updated'].rstrip()
      

      for j in i.getchildren():

#
#	GETTING DRUGBANK IDS
#
        if(j.tag == '{http://www.drugbank.ca}drugbank-id'):
          if 'primary' in j.attrib:
            if(j.attrib['primary'] == 'true'):
              PRIMARY_DRUGBANK_ID = j.text.rstrip()
          else:
            drugbank_ids.append(j.text.rstrip())

#
#	GETTING DRUGBANK INTERNATIONAL BRANDS
#
        if(j.tag == '{http://www.drugbank.ca}international-brands'):
          international_brands = {}
          for k in j.getchildren():
            if(k.tag == '{http://www.drugbank.ca}international-brand'):
              INTERNATIONAL_BRAND_NAME = "NULL"
              INTERNATIONAL_BRAND_COMPANY = "NULL"
              for m in k.getchildren():
                if(m.tag == '{http://www.drugbank.ca}name'  and m.text is not None):
                  INTERNATIONAL_BRAND_NAME = m.text.rstrip()
                if(m.tag == '{http://www.drugbank.ca}company'  and m.text is not None):
                  INTERNATIONAL_BRAND_COMPANY = m.text.rstrip()
              international_brands[INTERNATIONAL_BRAND_NAME] = INTERNATIONAL_BRAND_COMPANY

#
#	GETTING DRUGBANK MIXTURES
#
        if(j.tag == '{http://www.drugbank.ca}mixtures'):
          mixtures = {}
          for k in j.getchildren():
            if(k.tag == '{http://www.drugbank.ca}mixture'):
              MIXTURE_NAME = "NULL"
              MIXTURE_INGREDIENTS = "NULL"
              for m in k.getchildren():
                if(m.tag == '{http://www.drugbank.ca}name' and m.text is not None):
                  MIXTURE_NAME = m.text.rstrip()
                if(m.tag == '{http://www.drugbank.ca}ingredients' and m.text is not None):
                  MIXTURE_INGREDIENTS = m.text.rstrip()
                mixtures[MIXTURE_NAME] = MIXTURE_INGREDIENTS

#
#	GETTING DRUGBANK PACKAGERS
#
        if(j.tag == '{http://www.drugbank.ca}packagers'):
          packagers = {}
          for k in j.getchildren():
            if(k.tag == '{http://www.drugbank.ca}packager'):
              PACKAGER_NAME = "NULL"
              PACKAGER_URL = "NULL"
              for m in k.getchildren():
                if(m.tag == '{http://www.drugbank.ca}name' and m.text is not None):
                  PACKAGER_NAME = m.text.rstrip()
                if(m.tag == '{http://www.drugbank.ca}url' and m.text is not None):
                  PACKAGER_URL = m.text.rstrip()
              packagers[PACKAGER_NAME] = PACKAGER_URL

#
#	GETTING DRUGBANK MANUFACTURERS
#
        if(j.tag == '{http://www.drugbank.ca}manufacturers'):
          manufacturers = {}
          for k in j.getchildren():
            if(k.tag == '{http://www.drugbank.ca}manufacturer'):
              MANUFACTURER_NAME = "NULL"
              MANUFACTURER_GENERIC = "NULL"
              MANUFACTURER_NAME = k.text.rstrip()
              if(k.attrib['generic'] != ""):
                MANUFACTURER_GENERIC = k.attrib['generic'].rstrip().upper()
              manufacturers[MANUFACTURER_NAME] = MANUFACTURER_GENERIC


#
#	GETTING DRUGBANK PRICES
#
        if(j.tag == '{http://www.drugbank.ca}prices'):
          prices = {}
          for k in j.getchildren():
            if(k.tag == '{http://www.drugbank.ca}price'):
              PRICE_DESCRIPTION = "NULL"
              costs = {}
              PRICE_UNIT = "NULL"
              for m in k.getchildren():
                if(m.tag == '{http://www.drugbank.ca}description' and m.text is not None):
                  PRICE_DESCRIPTION = m.text.rstrip()
                if(m.tag == '{http://www.drugbank.ca}cost' and m.text is not None):
                  PRICE_COST = m.text.rstrip()
                  PRICE_CURRENCY = m.attrib['currency'].rstrip()
                  costs[PRICE_CURRENCY] = PRICE_COST
                if(m.tag == '{http://www.drugbank.ca}unit' and m.text is not None):
                  PRICE_UNIT = m.text.rstrip()
              prices[PRICE_DESCRIPTION] = [costs, PRICE_UNIT]

#
#		GETTING DRUGBANK CATEGORIES / CATEGORY MESH CODES
#
        if(j.tag == '{http://www.drugbank.ca}categories'):
          categories = {}
          for k in j.getchildren():
            if(k.tag == '{http://www.drugbank.ca}category'):
              CATEGORY_NAME = "NULL"
              mesh_ids = []
              for m in k.getchildren():
                if(m.tag == '{http://www.drugbank.ca}category'):
                  CATEGORY_NAME = m.text.rstrip()
                if(m.tag == '{http://www.drugbank.ca}mesh-id'):
                  temp_mesh_ids = m.text.rstrip().split(", ")
                  for index in range(len(temp_mesh_ids)):
                    mesh_ids.append((temp_mesh_ids[index]).replace('[', '').replace(']', ''))
            categories[CATEGORY_NAME] = mesh_ids

#
#		GETTING DRUGBANK AFFECTED ORGANISMS
#
        if(j.tag == '{http://www.drugbank.ca}affected-organisms'):
          affected_organisms = []
          for k in j.getchildren():
            if(k.tag == '{http://www.drugbank.ca}affected-organism'):
              AFFECTED_ORGANISM = k.text.rstrip()
              affected_organisms.append(AFFECTED_ORGANISM)

#
#		GETTING DRUGBANK DOSAGES
#
        if(j.tag == '{http://www.drugbank.ca}dosages'):
          dosages = {}
          for k in j.getchildren():
            if(k.tag == '{http://www.drugbank.ca}dosage'):
              FORM = "NULL"
              ROUTE = "NULL"
              STRENGTH = "NULL"
              for m in k.getchildren():
                if(m.tag == '{http://www.drugbank.ca}form' and m.text is not None):
                  FORM = m.text.rstrip()
                if(m.tag == '{http://www.drugbank.ca}route' and m.text is not None):
                  ROUTE = m.text.rstrip()
                if(m.tag == '{http://www.drugbank.ca}strength' and m.text is not None):
                  STRENGTH = m.text.rstrip()
              dosages[FORM] = [ROUTE, STRENGTH]

#
#		GETTING DRUGBANK ATC CODES / ATC CODE LEVELS
#
        if(j.tag == '{http://www.drugbank.ca}atc-codes'):
          atc_codes = []
          for k in j.getchildren():
            if(k.tag == '{http://www.drugbank.ca}atc-code'):
              ATC_CODE = k.attrib['code']
              atc_codes.append(ATC_CODE)
              atc_code_levels = []
              for m in k.getchildren():
                if(m.tag == '{http://www.drugbank.ca}level'):
                  LEVEL_NAME = m.text.rstrip()
                  LEVEL_CODE = m.attrib['code']
                  temp_atc_code = []
                  temp_atc_code.append(ATC_CODE)
                  temp_atc_code.append(LEVEL_CODE)
                  temp_atc_code.append(LEVEL_NAME)
                  atc_code_levels.append(temp_atc_code)

#
#		GETTING DRUGBANK AHFS CODES
#
        if(j.tag == '{http://www.drugbank.ca}ahfs-codes'):
          ahfs_codes = []
          for k in j.getchildren():
            if(k.tag == '{http://www.drugbank.ca}ahfs-code'):
              AHFS_CODE = k.text
              ahfs_codes.append(AHFS_CODE)

#
#		GETTING DRUGBANK PATENTS
#
        if(j.tag == '{http://www.drugbank.ca}patents'):
          patents = []
          for k in j.getchildren():
            if(k.tag == '{http://www.drugbank.ca}patent'):
              PATENT_NUMBER = "NULL"
              PATENT_COUNTRY = "NULL"
              PATENT_APPROVED = "NULL"
              PATENT_EXPIRES = "NULL"
              for m in k.getchildren():
                patent = []
                if(m.tag == '{http://www.drugbank.ca}number'):
                  PATENT_NUMBER = m.text
                if(m.tag == '{http://www.drugbank.ca}country'):
                  PATENT_COUNTRY = m.text
                if(m.tag == '{http://www.drugbank.ca}approved'):
                  PATENT_APPROVED = m.text
                if(m.tag == '{http://www.drugbank.ca}expires'):
                  PATENT_EXPIRES = m.text
                patent.append(PATENT_NUMBER)
                patent.append(PATENT_COUNTRY)
                patent.append(PATENT_APPROVED)
                patent.append(PATENT_EXPIRES)
              patents.append(patent)

#
#	GETTING DRUGBANK FOOD INTERACTIONS
#
        if(j.tag == '{http://www.drugbank.ca}food-interactions'):
          drug_food_interactions = []
          for k in j.getchildren():
            if(k.tag == '{http://www.drugbank.ca}food-interaction'):
              FOOD_INTERACTION = k.text.rstrip()
              drug_food_interactions.append(FOOD_INTERACTION)

#
#		GETTING DRUGBANK DRUG INTERACTIONS
#
        if(j.tag == '{http://www.drugbank.ca}drug-interactions'):
          drug_drug_interactions = []
          for k in j.getchildren():
            if(k.tag == '{http://www.drugbank.ca}drug-interaction'): 
              SECONDARY_DRUGBANK_ID = "NULL"
              DRUG_INTERACTION_NAME = "NULL"
              DRUG_INTERACTION_DESCRIPTION = "NULL"
              for m in k.getchildren():
                if(m.tag == '{http://www.drugbank.ca}drugbank-id'):
                  SECONDARY_DRUGBANK_ID = m.text.rstrip()
                if(m.tag == '{http://www.drugbank.ca}name'):
                  DRUG_INTERACTION_NAME = m.text.rstrip()
                if(m.tag == '{http://www.drugbank.ca}description'):
                  DRUG_INTERACTION_DESCRIPTION = m.text.rstrip()
                drug_interaction = [SECONDARY_DRUGBANK_ID, DRUG_INTERACTION_NAME, DRUG_INTERACTION_DESCRIPTION]
              drug_drug_interactions.append(drug_interaction)

#
#		GETTING DRUGBANK SEQUENCES
#
        if(j.tag == '{http://www.drugbank.ca}sequences'): 
          sequences = []
          for k in j.getchildren():
            if(k.tag == '{http://www.drugbank.ca}sequence'):
              SEQUENCE_FORMAT = k.attrib['format']
              DRUG_SEQUENCE = k.text
              sequence = []
              sequence.append(DRUG_SEQUENCE)
              sequence.append(SEQUENCE_FORMAT)
              sequences.append(sequence)

#
#		GETTING DRUGBANK EXPERIMENTAL PROPERTIES / CALCULATED PROPERTIES
#
        if(j.tag == '{http://www.drugbank.ca}experimental-properties'):
          EXPERIMENTAL = "TRUE" 
          CALCULATED = "FALSE"
          for k in j.getchildren():
            if(k.tag == '{http://www.drugbank.ca}property'):
              property = []
              KIND = "NULL"
              PROPERTY_VALUE = "NULL"
              PROPERTY_SOURCE = "NULL"
              for m in k.getchildren():
                if(m.tag == '{http://www.drugbank.ca}kind'):
                  KIND = m.text.rstrip()
                if(m.tag == '{http://www.drugbank.ca}value'):
                  PROPERTY_VALUE = m.text.rstrip()
                if(m.tag == '{http://www.drugbank.ca}source' and m.text is not None):
                  PROPERTY_SOURCE = m.text.rstrip()
              property.append(KIND)
              property.append(PROPERTY_VALUE)
              property.append(PROPERTY_SOURCE)
              property.append(EXPERIMENTAL)
              property.append(CALCULATED)
              properties.append(property)

        if(j.tag == '{http://www.drugbank.ca}calculated-properties'):
          EXPERIMENTAL = "FALSE" 
          CALCULATED = "TRUE"
          for k in j.getchildren():
            if(k.tag == '{http://www.drugbank.ca}property'):
              property = []
              KIND = "NULL"
              PROPERTY_VALUE = "NULL"
              PROPERTY_SOURCE = "NULL"
              for m in k.getchildren():
                if(m.tag == '{http://www.drugbank.ca}kind'):
                  KIND = m.text.rstrip()
                if(m.tag == '{http://www.drugbank.ca}value'):
                  PROPERTY_VALUE = m.text.rstrip()
                if(m.tag == '{http://www.drugbank.ca}source'):
                  PROPERTY_SOURCE = m.text.rstrip()
              property.append(KIND)
              property.append(PROPERTY_VALUE)
              property.append(PROPERTY_SOURCE)
              property.append(EXPERIMENTAL)
              property.append(CALCULATED)
              properties.append(property)

#
#		GETTING DRUGBANK EXTERNAL IDENTIFIERS
#
        if(j.tag == '{http://www.drugbank.ca}external-identifiers'):
          external_identifiers = []
          for k in j.getchildren():
            if(k.tag == '{http://www.drugbank.ca}external-identifier'):
              external_identifier = []
              RESOURCE = "NULL"
              IDENTIFIER = "NULL"
              for m in k.getchildren():
                if(m.tag == '{http://www.drugbank.ca}resource'):
                  RESOURCE = m.text
                if(m.tag == '{http://www.drugbank.ca}identifier'):
                  IDENTIFIER = m.text
              external_identifier.append(RESOURCE)
              external_identifier.append(IDENTIFIER)
              external_identifiers.append(external_identifier)

#
#		GETTING DRUGBANK EXTERNAL LINKS
#
        if(j.tag == '{http://www.drugbank.ca}external-links'):
          external_links = []
          for k in j.getchildren():
            if(k.tag == '{http://www.drugbank.ca}external-link'):
              external_link = []
              RESOURCE = "NULL"
              URL = "NULL"
              for m in k.getchildren():
                if(m.tag == '{http://www.drugbank.ca}resource'):
                  RESOURCE = m.text
                if(m.tag == '{http://www.drugbank.ca}url'):
                  URL = m.text
              external_link.append(RESOURCE)
              external_link.append(URL)
              external_links.append(external_link)

#
#		GETTING DRUGBANK PATHWAYS
#
#        if(j.tag == '{http://www.drugbank.ca}pathways'):

#
#		GETTING DRUGBANK REACTIONS / REACTION ELEMENTS / REACTION ENZYMES
#
        if(j.tag == '{http://www.drugbank.ca}reactions'):
          reactions = []
          for k in j.getchildren():
            if(k.tag == '{http://www.drugbank.ca}reaction'):
              reaction = []
              reaction_elements = []
              REACTION_SEQUENCE = "NULL"
              for m in k.getchildren():
                if(m.tag == '{http://www.drugbank.ca}sequence'):
                  REACTION_SEQUENCE = m.text
                if(m.tag == '{http://www.drugbank.ca}left-element'):
                  reaction_element = []
                  LEFT_ELEMENT = "TRUE"
                  RIGHT_ELEMENT = "FALSE"
                  REACTION_SECONDARY_DRUGBANK_ID = "NULL"
                  REACTION_NAME = "NULL"
                  for n in m.getchildren():
                    if(n.tag == '{http://www.drugbank.ca}drugbank-id'):
                      REACTION_SECONDARY_DRUGBANK_ID = n.text
                    if(n.tag == '{http://www.drugbank.ca}name'):
                      REACTION_NAME = n.text
                  reaction_element.append(REACTION_SECONDARY_DRUGBANK_ID)
                  reaction_element.append(REACTION_NAME)
                  reaction_element.append(LEFT_ELEMENT)
                  reaction_element.append(RIGHT_ELEMENT)
                  reaction_elements.append(reaction_element)
                if(m.tag == '{http://www.drugbank.ca}right-element'):
                  reaction_element = []
                  RIGHT_ELEMENT = "TRUE"
                  LEFT_ELEMENT = "FALSE"
                  REACTION_SECONDARY_DRUGBANK_ID = "NULL"
                  REACTION_NAME = "NULL"
                  for n in m.getchildren():
                    if(n.tag == '{http://www.drugbank.ca}drugbank-id'):
                      REACTION_SECONDARY_DRUGBANK_ID = n.text
                    if(n.tag == '{http://www.drugbank.ca}name'):
                      REACTION_NAME = n.text
                  reaction_element.append(REACTION_SECONDARY_DRUGBANK_ID)
                  reaction_element.append(REACTION_NAME)
                  reaction_element.append(LEFT_ELEMENT)
                  reaction_element.append(RIGHT_ELEMENT)
                  reaction_elements.append(reaction_element)
                if(m.tag == '{http://www.drugbank.ca}enzymes'):
                  reaction_enzymes = []
                  for n in m.getchildren():
                    if(n.tag == '{http://www.drugbank.ca}enzyme'):
                      reaction_enzyme = []
                      REACTION_ENZYME_DRUGBANK_ID = "NULL"
                      REACTION_ENZYME_NAME = "NULL"
                      REACTION_ENZYME_UNIPROT_ID = "NULL"
                      for p in n.getchildren():
                        if(p.tag == '{http://www.drugbank.ca}drugbank-id'):
                          REACTION_ENZYME_DRUGBANK_ID = p.text
                        if(p.tag == '{http://www.drugbank.ca}name'):
                          REACTION_ENZYME_NAME = p.text
                        if(p.tag == '{http://www.drugbank.ca}uniprot-id' and p.text is not None):
                          REACTION_ENZYME_UNIPROT_ID = p.text
                      reaction_enzyme.append(REACTION_ENZYME_DRUGBANK_ID)
                      reaction_enzyme.append(REACTION_ENZYME_NAME)
                      reaction_enzyme.append(REACTION_ENZYME_UNIPROT_ID)
                      reaction_enzymes.append(reaction_enzyme)
              reaction.append(REACTION_SEQUENCE)
              reaction.append(reaction_elements)
              reaction.append(reaction_enzymes)
              reactions.append(reaction)

#
#		GETTING DRUGBANK SNP EFFECTS
#
        if(j.tag == '{http://www.drugbank.ca}snp-effects'):
          effects = []
          for k in j.getchildren():
            if(k.tag == '{http://www.drugbank.ca}effect'):
              effect = []
              SNP_EFFECT_PROTEIN_NAME = "NULL"
              SNP_EFFECT_GENE_SYMBOL = "NULL"
              SNP_EFFECT_UNIPROT_ID = "NULL"
              SNP_EFFECT_RS_ID = "NULL"
              SNP_EFFECT_ALLELE = "NULL"
              SNP_EFFECT_DEFINING_CHANGE = "NULL"
              SNP_EFFECT_DESCRIPTION = "NULL"
              SNP_EFFECT_PUBMED_ID = "NULL"
              for m in k.getchildren():
                if(m.tag == '{http://www.drugbank.ca}protein-name'):
                  SNP_EFFECT_PROTEIN_NAME = m.text
                if(m.tag == '{http://www.drugbank.ca}gene-symbol'):
                  SNP_EFFECT_GENE_SYMBOL = m.text
                if(m.tag == '{http://www.drugbank.ca}uniprot-id'):
                  SNP_EFFECT_UNIPROT_ID = m.text
                if(m.tag == '{http://www.drugbank.ca}rs-id' and m.text is not None):
                  SNP_EFFECT_RS_ID = m.text
                if(m.tag == '{http://www.drugbank.ca}allele' and m.text is not None):
                  SNP_EFFECT_ALLELE = m.text
                if(m.tag == '{http://www.drugbank.ca}defining-change' and m.text is not None):
                  SNP_EFFECT_DEFINING_CHANGE = m.text
                if(m.tag == '{http://www.drugbank.ca}description'):
                  SNP_EFFECT_DESCRIPTION = m.text
                if(m.tag == '{http://www.drugbank.ca}pubmed-id'):
                  SNP_EFFECT_PUBMED_ID = m.text
              effect.append(SNP_EFFECT_PROTEIN_NAME)
              effect.append(SNP_EFFECT_GENE_SYMBOL)
              effect.append(SNP_EFFECT_UNIPROT_ID)
              effect.append(SNP_EFFECT_RS_ID)
              effect.append(SNP_EFFECT_ALLELE)
              effect.append(SNP_EFFECT_DEFINING_CHANGE)
              effect.append(SNP_EFFECT_DESCRIPTION)
              effect.append(SNP_EFFECT_PUBMED_ID)
              effects.append(effect)

#
#		GETTING DRUGBANK SNP ADVERSE DRUG REACTIONS
#
        if(j.tag == '{http://www.drugbank.ca}snp-adverse-drug-reactions'):
          adverse_drug_reactions = []
          for k in j.getchildren():
            if(k.tag == '{http://www.drugbank.ca}reaction'):
              adverse_drug_reaction = []
              ADVERSE_DRUG_REACTION_PROTEIN_NAME = "NULL"
              ADVERSE_DRUG_REACTION_GENE_SYMBOL = "NULL"
              ADVERSE_DRUG_REACTION_UNIPROT_ID = "NULL"
              ADVERSE_DRUG_REACTION_RS_ID = "NULL"
              ADVERSE_DRUG_REACTION_ALLELE = "NULL"
              ADVERSE_DRUG_REACTION_ADVERSE_REACTION = "NULL"
              ADVERSE_DRUG_REACTION_DESCRIPTION = "NULL"
              ADVERSE_DRUG_REACTION_PUBMED_ID = "NULL"
              for m in k.getchildren():
                if(m.tag == '{http://www.drugbank.ca}protein-name'):
                  ADVERSE_DRUG_REACTION_PROTEIN_NAME = m.text
                if(m.tag == '{http://www.drugbank.ca}gene-symbol'):
                  ADVERSE_DRUG_REACTION_GENE_SYMBOL = m.text
                if(m.tag == '{http://www.drugbank.ca}uniprot-id'):
                  ADVERSE_DRUG_REACTION_UNIPROT_ID = m.text
                if(m.tag == '{http://www.drugbank.ca}rs-id' and m.text is not None):
                  ADVERSE_DRUG_REACTION_RS_ID = m.text
                if(m.tag == '{http://www.drugbank.ca}allele' and m.text is not None):
                  ADVERSE_DRUG_REACTION_ALLELE = m.text
                if(m.tag == '{http://www.drugbank.ca}adverse-reaction' and m.text is not None):
                  ADVERSE_DRUG_REACTION_ADVERSE_REACTION = m.text
                if(m.tag == '{http://www.drugbank.ca}description'):
                  ADVERSE_DRUG_REACTION_DESCRIPTION = m.text
                if(m.tag == '{http://www.drugbank.ca}pubmed-id'):
                  ADVERSE_DRUG_REACTION_PUBMED_ID = m.text
              adverse_drug_reaction.append(ADVERSE_DRUG_REACTION_PROTEIN_NAME)
              adverse_drug_reaction.append(ADVERSE_DRUG_REACTION_GENE_SYMBOL)
              adverse_drug_reaction.append(ADVERSE_DRUG_REACTION_UNIPROT_ID)
              adverse_drug_reaction.append(ADVERSE_DRUG_REACTION_RS_ID)
              adverse_drug_reaction.append(ADVERSE_DRUG_REACTION_ALLELE)
              adverse_drug_reaction.append(ADVERSE_DRUG_REACTION_ADVERSE_REACTION)
              adverse_drug_reaction.append(ADVERSE_DRUG_REACTION_DESCRIPTION)
              adverse_drug_reaction.append(ADVERSE_DRUG_REACTION_PUBMED_ID)
              adverse_drug_reactions.append(adverse_drug_reaction)

#
#		GETTING DRUGBANK TARGETS
#
        if(j.tag == '{http://www.drugbank.ca}targets'):
          targets = []
          for k in j.getchildren():
            if(k.tag == '{http://www.drugbank.ca}target'):
              target = []
              POSITION = "NULL"
              NAME = "NULL"
              ORGANISM = "NULL"
              KNOWN_ACTION = "NULL"
              TARGET_INHIBITION_STRENGTH = "NULL"
              TARGET_INDUCTION_STRENGTH = "NULL"
              actions = []
              target_references = []
              target_polypeptides = []
              if(('position' in k.attrib.keys()) and k.attrib['position'] != ""):
                POSITION = k.attrib['position'].rstrip()
              for m in k.getchildren():
                if(m.tag == '{http://www.drugbank.ca}id'):
                  ID = m.text
                if(m.tag == '{http://www.drugbank.ca}name'):
                  NAME = m.text
                if(m.tag == '{http://www.drugbank.ca}organism' and m.text is not None):
                  ORGANISM = m.text
                if(m.tag == '{http://www.drugbank.ca}known-action' and m.text is not None):
                  KNOWN_ACTION = m.text
                if(m.tag == '{http://www.drugbank.ca}inhibition-strength'):
                  TARGET_INHIBITION_STRENGTH = m.text
                if(m.tag == '{http://www.drugbank.ca}induction-strength'):
                  TARGET_INDUCTION_STRENGTH = m.text
                if(m.tag == '{http://www.drugbank.ca}actions'):
                  for n in m.getchildren():
                    if(n.tag == '{http://www.drugbank.ca}action'): 
                      ACTION = n.text
                  actions.append(ACTION)
                if(m.tag == '{http://www.drugbank.ca}references' and m.text is not None):
                  temp_target_references = m.text.rstrip()
                  target_references = temp_target_references.split('#')
                if(m.tag == '{http://www.drugbank.ca}polypeptide' and m.text is not None):
                  target_polypeptide = []
                  TARGET_POLYPEPTIDE_TRANSMEMBRANE_REGIONS = []
                  TARGET_AMINO_ACID_SEQUENCE = "NULL"
                  TARGET_AMINO_ACID_SEQUENCE_FORMAT = "NULL"
                  TARGET_POLYPEPTIDE_GENERAL_FUNCTION = "NULL"
                  TARGET_POLYPEPTIDE_SIGNAL_REGIONS = []
                  TARGET_POLYPEPTIDE_LOCUS = "NULL"
                  TARGET_POLYPEPTIDE_THEORETICAL_PI = "NULL"
                  TARGET_POLYPEPTIDE_CHROMOSOME_LOCATION = "NULL"
                  TARGET_GENE_SEQUENCE = "NULL"
                  TARGET_GENE_SEQUENCE_FORMAT = "NULL"
                  TARGET_POLYPEPTIDE_CELLULAR_LOCATION = "NULL"
                  TARGET_POLYPEPTIDE_SPECIFIC_FUNCTION = "NULL"
                  TARGET_POLYPEPTIDE_GENE_NAME = "NULL"
                  TARGET_POLYPEPTIDE_MOLECULAR_WEIGHT = "NULL"
                  TARGET_POLYPEPTIDE_ORGANISM_NAME = "NULL"
                  TARGET_POLYPEPTIDE_ORGANISM_NCBI_TAXONOMY_ID = "NULL"
                  if(m.attrib['id'] != ""):
                    TARGET_POLYPEPTIDE_ID = m.attrib['id'].rstrip()
                  if(m.attrib['source'] != ""):
                    TARGET_POLYPEPTIDE_SOURCE = m.attrib['source'].rstrip()
                  for n in m.getchildren():
                    if(n.tag == '{http://www.drugbank.ca}name'):
                      TARGET_POLYPEPTIDE_NAME = n.text
                    if(n.tag == '{http://www.drugbank.ca}general-function' and n.text is not None):
                      TARGET_POLYPEPTIDE_GENERAL_FUNCTION = n.text
                    if(n.tag == '{http://www.drugbank.ca}specific-function' and n.text is not None):
                      TARGET_POLYPEPTIDE_SPECIFIC_FUNCTION = n.text
                    if(n.tag == '{http://www.drugbank.ca}gene-name' and n.text is not None):
                      TARGET_POLYPEPTIDE_GENE_NAME = n.text
                    if(n.tag == '{http://www.drugbank.ca}locus' and n.text is not None):
                      TARGET_POLYPEPTIDE_LOCUS = n.text
                    if(n.tag == '{http://www.drugbank.ca}cellular-location' and n.text is not None):
                      TARGET_POLYPEPTIDE_CELLULAR_LOCATION = n.text
                    if(n.tag == '{http://www.drugbank.ca}signal-regions' and n.text is not None):
                      temp_polypeptide_signal_regions = n.text
                      TARGET_POLYPEPTIDE_SIGNAL_REGIONS = temp_polypeptide_signal_regions.split('-')
                      TARGET_POLYPEPTIDE_SIGNAL_REGIONS_LOWER = TARGET_POLYPEPTIDE_SIGNAL_REGIONS[0]
                      TARGET_POLYPEPTIDE_SIGNAL_REGIONS_UPPER = TARGET_POLYPEPTIDE_SIGNAL_REGIONS[1]
                    if(n.tag == '{http://www.drugbank.ca}theoretical-pi' and n.text is not None):
                      TARGET_POLYPEPTIDE_THEORETICAL_PI = n.text
                    if(n.tag == '{http://www.drugbank.ca}molecular-weight' and n.text is not None):
                      TARGET_POLYPEPTIDE_MOLECULAR_WEIGHT = n.text
                    if(n.tag == '{http://www.drugbank.ca}chromosome-location' and n.text is not None):
                      TARGET_POLYPEPTIDE_CHROMOSOME_LOCATION = n.text
                    if(n.tag == '{http://www.drugbank.ca}organism' and n.text is not None):
                      TARGET_POLYPEPTIDE_ORGANISM = n.text
                      if(n.attrib['ncbi-taxonomy-id'] != ""):
                        TARGET_POLYPEPTIDE_ORGANISM_NCBI_TAXONOMY_ID = n.attrib['ncbi-taxonomy-id'].rstrip()
                    if(n.tag == '{http://www.drugbank.ca}transmembrane-regions' and n.text is not None):
                      temp_polypeptide_transmembrane_regions = n.text
                      TARGET_POLYPEPTIDE_TRANSMEMBRANE_REGIONS = temp_polypeptide_transmembrane_regions.split('-')
                    if(n.tag == '{http://www.drugbank.ca}external-identifiers'):
                      external_identifiers = []
                      for p in n.getchildren():
                        if(p.tag == '{http://www.drugbank.ca}external-identifier'):
                          external_identifier = []
                          for q in p.getchildren():
                            if(q.tag == '{http://www.drugbank.ca}resource'):
                              TARGET_POLYPEPTIDE_EXT_RESOURCE = q.text
                            if(q.tag == '{http://www.drugbank.ca}identifier'):
                              TARGET_POLYPEPTIDE_EXT_IDENTIFIER = q.text
                          external_identifier.append(TARGET_POLYPEPTIDE_EXT_RESOURCE)
                          external_identifier.append(TARGET_POLYPEPTIDE_EXT_IDENTIFIER)
                          external_identifiers.append(external_identifier)
                    if(n.tag == '{http://www.drugbank.ca}synonyms'):
                      target_synonyms = []
                      for p in n.getchildren():
                        if(p.tag == '{http://www.drugbank.ca}synonym'):
                          TARGET_SYNONYM = p.text
                          target_synonyms.append(TARGET_SYNONYM)
                    if(n.tag == '{http://www.drugbank.ca}amino-acid-sequence' and n.text is not None):
                      TARGET_AMINO_ACID_SEQUENCE = n.text
                      if(n.attrib['format'] != ""):
                        TARGET_AMINO_ACID_SEQUENCE_FORMAT = n.attrib['format'].rstrip()
                    if(n.tag == '{http://www.drugbank.ca}gene-sequence' and n.text is not None):
                      TARGET_GENE_SEQUENCE = n.text
                      if(n.attrib['format'] != ""):
                        TARGET_GENE_SEQUENCE_FORMAT = n.attrib['format'].rstrip()
                    if(n.tag == '{http://www.drugbank.ca}pfams'):
                      pfams = []
                      for p in n.getchildren():
                        if(p.tag == '{http://www.drugbank.ca}pfam'):
                          pfam = []
                          for q in p.getchildren():
                            if(q.tag == '{http://www.drugbank.ca}identifier'):
                              TARGET_POLYPEPTIDE_PFAM_IDENTIFIER = q.text
                            if(q.tag == '{http://www.drugbank.ca}name'):
                              TARGET_POLYPEPTIDE_PFAM_NAME = q.text
                          pfam.append(TARGET_POLYPEPTIDE_PFAM_IDENTIFIER)
                          pfam.append(TARGET_POLYPEPTIDE_PFAM_NAME)
                          pfams.append(pfam)
                    if(n.tag == '{http://www.drugbank.ca}go-classifiers'):
                      go_classifiers = []
                      for p in n.getchildren():
                        if(p.tag == '{http://www.drugbank.ca}go-classifier'):
                          go_classifier = []
                          for q in p.getchildren():
                            if(q.tag == '{http://www.drugbank.ca}category'):
                              TARGET_POLYPEPTIDE_GO_CATEGORY = q.text
                            if(q.tag == '{http://www.drugbank.ca}description'):
                              TARGET_POLYPEPTIDE_GO_DESCRIPTION = q.text
                          go_classifier.append(TARGET_POLYPEPTIDE_GO_CATEGORY)
                          go_classifier.append(TARGET_POLYPEPTIDE_GO_DESCRIPTION)
                          go_classifiers.append(go_classifier)
                    
                  target_polypeptide.append(TARGET_POLYPEPTIDE_ID)
                  target_polypeptide.append(TARGET_POLYPEPTIDE_SOURCE)
                  target_polypeptide.append(TARGET_POLYPEPTIDE_NAME)
                  target_polypeptide.append(TARGET_POLYPEPTIDE_GENERAL_FUNCTION)
                  target_polypeptide.append(TARGET_POLYPEPTIDE_SPECIFIC_FUNCTION)
                  target_polypeptide.append(TARGET_POLYPEPTIDE_GENE_NAME)
                  target_polypeptide.append(TARGET_POLYPEPTIDE_LOCUS)
                  target_polypeptide.append(TARGET_POLYPEPTIDE_CELLULAR_LOCATION)
                  target_polypeptide.append(TARGET_POLYPEPTIDE_SIGNAL_REGIONS_LOWER)
                  target_polypeptide.append(TARGET_POLYPEPTIDE_SIGNAL_REGIONS_UPPER)
                  target_polypeptide.append(TARGET_POLYPEPTIDE_THEORETICAL_PI)
                  target_polypeptide.append(TARGET_POLYPEPTIDE_MOLECULAR_WEIGHT)
                  target_polypeptide.append(TARGET_POLYPEPTIDE_CHROMOSOME_LOCATION)
                  target_polypeptide.append(TARGET_POLYPEPTIDE_ORGANISM)
                  target_polypeptide.append(TARGET_POLYPEPTIDE_ORGANISM_NCBI_TAXONOMY_ID)
                  target_polypeptide.append(TARGET_POLYPEPTIDE_TRANSMEMBRANE_REGIONS)
                  target_polypeptide.append(external_identifiers)
                  target_polypeptide.append(target_synonyms)
                  target_polypeptide.append(TARGET_AMINO_ACID_SEQUENCE)
                  target_polypeptide.append(TARGET_AMINO_ACID_SEQUENCE_FORMAT)
                  target_polypeptide.append(TARGET_GENE_SEQUENCE)
                  target_polypeptide.append(TARGET_GENE_SEQUENCE_FORMAT)
                  target_polypeptide.append(pfams)
                  target_polypeptide.append(go_classifiers)
                  target_polypeptides.append(target_polypeptide)
              target.append(POSITION)
              target.append(ID) 
              target.append(NAME) 
              target.append(ORGANISM) 
              target.append(KNOWN_ACTION)
              target.append(TARGET_INHIBITION_STRENGTH)
              target.append(TARGET_INDUCTION_STRENGTH)
              target.append(actions) 
              target.append(target_references) 
              target.append(target_polypeptides)
              targets.append(target)

#
#		GETTING DRUGBANK ENZYMES / ENZYME ACTIONS / ENZYME REFERENCES / ENZYME POLYPEPTIDES / ENZYME POLYPEPTIDE TRANSMEMBRANE REGIONS / ENZYME POLYPEPTIDE EXTERNAL IDENTIFIERS / ENZYME POLYPEPTIDE SYNONYMS / ENZYME AMINO ACID SEQUENCES / ENZYME GENE SEQUENCES / ENZYME PFAM / ENZYME GO CLASSIFIERS
#
        if(j.tag == '{http://www.drugbank.ca}enzymes'):
          enzymes = []
          for k in j.getchildren():
            if(k.tag == '{http://www.drugbank.ca}enzyme'):
              enzyme = []
              POSITION = "NULL"
              NAME = "NULL"
              ORGANISM = "NULL"
              KNOWN_ACTION = "NULL"
              ENZYME_INHIBITION_STRENGTH = "NULL"
              ENZYME_INDUCTION_STRENGTH = "NULL"
              actions = []
              enzyme_references = []
              enzyme_polypeptides = []
              if(('position' in k.attrib.keys()) and k.attrib['position'] != ""):
                POSITION = k.attrib['position'].rstrip()
              for m in k.getchildren():
                if(m.tag == '{http://www.drugbank.ca}id'):
                  ID = m.text
                if(m.tag == '{http://www.drugbank.ca}name'):
                  NAME = m.text
                if(m.tag == '{http://www.drugbank.ca}organism' and m.text is not None):
                  ORGANISM = m.text
                if(m.tag == '{http://www.drugbank.ca}known-action' and m.text is not None):
                  KNOWN_ACTION = m.text
                if(m.tag == '{http://www.drugbank.ca}inhibition-strength'):
                  ENZYME_INHIBITION_STRENGTH = m.text
                if(m.tag == '{http://www.drugbank.ca}induction-strength'):
                  ENZYME_INDUCTION_STRENGTH = m.text
                if(m.tag == '{http://www.drugbank.ca}actions'):
                  for n in m.getchildren():
                    if(n.tag == '{http://www.drugbank.ca}action'): 
                      ACTION = n.text
                  actions.append(ACTION)
                if(m.tag == '{http://www.drugbank.ca}references' and m.text is not None):
                  temp_enzyme_references = m.text.rstrip()
                  enzyme_references = temp_enzyme_references.split('#')
                if(m.tag == '{http://www.drugbank.ca}polypeptide' and m.text is not None):
                  enzyme_polypeptide = []
                  ENZYME_POLYPEPTIDE_TRANSMEMBRANE_REGIONS = []
                  ENZYME_AMINO_ACID_SEQUENCE = "NULL"
                  ENZYME_AMINO_ACID_SEQUENCE_FORMAT = "NULL"
                  ENZYME_POLYPEPTIDE_GENERAL_FUNCTION = "NULL"
                  ENZYME_POLYPEPTIDE_SIGNAL_REGIONS = []
                  ENZYME_POLYPEPTIDE_LOCUS = "NULL"
                  ENZYME_POLYPEPTIDE_THEORETICAL_PI = "NULL"
                  ENZYME_POLYPEPTIDE_CHROMOSOME_LOCATION = "NULL"
                  ENZYME_GENE_SEQUENCE = "NULL"
                  ENZYME_GENE_SEQUENCE_FORMAT = "NULL"
                  ENZYME_POLYPEPTIDE_CELLULAR_LOCATION = "NULL"
                  ENZYME_POLYPEPTIDE_SPECIFIC_FUNCTION = "NULL"
                  ENZYME_POLYPEPTIDE_GENE_NAME = "NULL"
                  ENZYME_POLYPEPTIDE_MOLECULAR_WEIGHT = "NULL"
                  ENZYME_POLYPEPTIDE_ORGANISM_NAME = "NULL"
                  ENZYME_POLYPEPTIDE_ORGANISM_NCBI_TAXONOMY_ID = "NULL"
                  if(m.attrib['id'] != ""):
                    ENZYME_POLYPEPTIDE_ID = m.attrib['id'].rstrip()
                  if(m.attrib['source'] != ""):
                    ENZYME_POLYPEPTIDE_SOURCE = m.attrib['source'].rstrip()
                  for n in m.getchildren():
                    if(n.tag == '{http://www.drugbank.ca}name'):
                      ENZYME_POLYPEPTIDE_NAME = n.text
                    if(n.tag == '{http://www.drugbank.ca}general-function' and n.text is not None):
                      ENZYME_POLYPEPTIDE_GENERAL_FUNCTION = n.text
                    if(n.tag == '{http://www.drugbank.ca}specific-function' and n.text is not None):
                      ENZYME_POLYPEPTIDE_SPECIFIC_FUNCTION = n.text
                    if(n.tag == '{http://www.drugbank.ca}gene-name' and n.text is not None):
                      ENZYME_POLYPEPTIDE_GENE_NAME = n.text
                    if(n.tag == '{http://www.drugbank.ca}locus' and n.text is not None):
                      ENZYME_POLYPEPTIDE_LOCUS = n.text
                    if(n.tag == '{http://www.drugbank.ca}cellular-location' and n.text is not None):
                      ENZYME_POLYPEPTIDE_CELLULAR_LOCATION = n.text
                    if(n.tag == '{http://www.drugbank.ca}signal-regions' and n.text is not None):
                      temp_polypeptide_signal_regions = n.text
                      ENZYME_POLYPEPTIDE_SIGNAL_REGIONS = temp_polypeptide_signal_regions.split('-')
                      ENZYME_POLYPEPTIDE_SIGNAL_REGIONS_LOWER = ENZYME_POLYPEPTIDE_SIGNAL_REGIONS[0]
                      ENZYME_POLYPEPTIDE_SIGNAL_REGIONS_UPPER = ENZYME_POLYPEPTIDE_SIGNAL_REGIONS[1]
                    if(n.tag == '{http://www.drugbank.ca}theoretical-pi' and n.text is not None):
                      ENZYME_POLYPEPTIDE_THEORETICAL_PI = n.text
                    if(n.tag == '{http://www.drugbank.ca}molecular-weight' and n.text is not None):
                      ENZYME_POLYPEPTIDE_MOLECULAR_WEIGHT = n.text
                    if(n.tag == '{http://www.drugbank.ca}chromosome-location' and n.text is not None):
                      ENZYME_POLYPEPTIDE_CHROMOSOME_LOCATION = n.text
                    if(n.tag == '{http://www.drugbank.ca}organism' and n.text is not None):
                      ENZYME_POLYPEPTIDE_ORGANISM = n.text
                      if(n.attrib['ncbi-taxonomy-id'] != ""):
                        ENZYME_POLYPEPTIDE_ORGANISM_NCBI_TAXONOMY_ID = n.attrib['ncbi-taxonomy-id'].rstrip()
                    if(n.tag == '{http://www.drugbank.ca}transmembrane-regions' and n.text is not None):
                      temp_polypeptide_transmembrane_regions = n.text
                      ENZYME_POLYPEPTIDE_TRANSMEMBRANE_REGIONS = temp_polypeptide_transmembrane_regions.split('-')
                    if(n.tag == '{http://www.drugbank.ca}external-identifiers'):
                      external_identifiers = []
                      for p in n.getchildren():
                        if(p.tag == '{http://www.drugbank.ca}external-identifier'):
                          external_identifier = []
                          for q in p.getchildren():
                            if(q.tag == '{http://www.drugbank.ca}resource'):
                              ENZYME_POLYPEPTIDE_EXT_RESOURCE = q.text
                            if(q.tag == '{http://www.drugbank.ca}identifier'):
                              ENZYME_POLYPEPTIDE_EXT_IDENTIFIER = q.text
                          external_identifier.append(ENZYME_POLYPEPTIDE_EXT_RESOURCE)
                          external_identifier.append(ENZYME_POLYPEPTIDE_EXT_IDENTIFIER)
                          external_identifiers.append(external_identifier)
                    if(n.tag == '{http://www.drugbank.ca}synonyms'):
                      enzyme_synonyms = []
                      for p in n.getchildren():
                        if(p.tag == '{http://www.drugbank.ca}synonym'):
                          ENZYME_SYNONYM = p.text
                          enzyme_synonyms.append(ENZYME_SYNONYM)
                    if(n.tag == '{http://www.drugbank.ca}amino-acid-sequence' and n.text is not None):
                      ENZYME_AMINO_ACID_SEQUENCE = n.text
                      if(n.attrib['format'] != ""):
                        ENZYME_AMINO_ACID_SEQUENCE_FORMAT = n.attrib['format'].rstrip()
                    if(n.tag == '{http://www.drugbank.ca}gene-sequence' and n.text is not None):
                      ENZYME_GENE_SEQUENCE = n.text
                      if(n.attrib['format'] != ""):
                        ENZYME_GENE_SEQUENCE_FORMAT = n.attrib['format'].rstrip()
                    if(n.tag == '{http://www.drugbank.ca}pfams'):
                      pfams = []
                      for p in n.getchildren():
                        if(p.tag == '{http://www.drugbank.ca}pfam'):
                          pfam = []
                          for q in p.getchildren():
                            if(q.tag == '{http://www.drugbank.ca}identifier'):
                              ENZYME_POLYPEPTIDE_PFAM_IDENTIFIER = q.text
                            if(q.tag == '{http://www.drugbank.ca}name'):
                              ENZYME_POLYPEPTIDE_PFAM_NAME = q.text
                          pfam.append(ENZYME_POLYPEPTIDE_PFAM_IDENTIFIER)
                          pfam.append(ENZYME_POLYPEPTIDE_PFAM_NAME)
                          pfams.append(pfam)
                    if(n.tag == '{http://www.drugbank.ca}go-classifiers'):
                      go_classifiers = []
                      for p in n.getchildren():
                        if(p.tag == '{http://www.drugbank.ca}go-classifier'):
                          go_classifier = []
                          for q in p.getchildren():
                            if(q.tag == '{http://www.drugbank.ca}category'):
                              ENZYME_POLYPEPTIDE_GO_CATEGORY = q.text
                            if(q.tag == '{http://www.drugbank.ca}description'):
                              ENZYME_POLYPEPTIDE_GO_DESCRIPTION = q.text
                          go_classifier.append(ENZYME_POLYPEPTIDE_GO_CATEGORY)
                          go_classifier.append(ENZYME_POLYPEPTIDE_GO_DESCRIPTION)
                          go_classifiers.append(go_classifier)
                    
                  enzyme_polypeptide.append(ENZYME_POLYPEPTIDE_ID)
                  enzyme_polypeptide.append(ENZYME_POLYPEPTIDE_SOURCE)
                  enzyme_polypeptide.append(ENZYME_POLYPEPTIDE_NAME)
                  enzyme_polypeptide.append(ENZYME_POLYPEPTIDE_GENERAL_FUNCTION)
                  enzyme_polypeptide.append(ENZYME_POLYPEPTIDE_SPECIFIC_FUNCTION)
                  enzyme_polypeptide.append(ENZYME_POLYPEPTIDE_GENE_NAME)
                  enzyme_polypeptide.append(ENZYME_POLYPEPTIDE_LOCUS)
                  enzyme_polypeptide.append(ENZYME_POLYPEPTIDE_CELLULAR_LOCATION)
                  enzyme_polypeptide.append(ENZYME_POLYPEPTIDE_SIGNAL_REGIONS_LOWER)
                  enzyme_polypeptide.append(ENZYME_POLYPEPTIDE_SIGNAL_REGIONS_UPPER)
                  enzyme_polypeptide.append(ENZYME_POLYPEPTIDE_THEORETICAL_PI)
                  enzyme_polypeptide.append(ENZYME_POLYPEPTIDE_MOLECULAR_WEIGHT)
                  enzyme_polypeptide.append(ENZYME_POLYPEPTIDE_CHROMOSOME_LOCATION)
                  enzyme_polypeptide.append(ENZYME_POLYPEPTIDE_ORGANISM)
                  enzyme_polypeptide.append(ENZYME_POLYPEPTIDE_ORGANISM_NCBI_TAXONOMY_ID)
                  enzyme_polypeptide.append(ENZYME_POLYPEPTIDE_TRANSMEMBRANE_REGIONS)
                  enzyme_polypeptide.append(external_identifiers)
                  enzyme_polypeptide.append(enzyme_synonyms)
                  enzyme_polypeptide.append(ENZYME_AMINO_ACID_SEQUENCE)
                  enzyme_polypeptide.append(ENZYME_AMINO_ACID_SEQUENCE_FORMAT)
                  enzyme_polypeptide.append(ENZYME_GENE_SEQUENCE)
                  enzyme_polypeptide.append(ENZYME_GENE_SEQUENCE_FORMAT)
                  enzyme_polypeptide.append(pfams)
                  enzyme_polypeptide.append(go_classifiers)
                  enzyme_polypeptides.append(enzyme_polypeptide)
              enzyme.append(POSITION)
              enzyme.append(ID) 
              enzyme.append(NAME) 
              enzyme.append(ORGANISM) 
              enzyme.append(KNOWN_ACTION)
              enzyme.append(ENZYME_INHIBITION_STRENGTH)
              enzyme.append(ENZYME_INDUCTION_STRENGTH)
              enzyme.append(actions) 
              enzyme.append(enzyme_references) 
              enzyme.append(enzyme_polypeptides)
              enzymes.append(enzyme)
              
#
#		GETTING DRUGBANK CARRIERS / CARRIER ACTIONS / CARRIER REFERENCES / CARRIER POLYPEPTIDES / CARRIER POLYPEPTIDE TRANSMEMBRANE REGIONS / CARRIER POLYPEPTIDE EXTERNAL IDENTIFIERS / CARRIER POLYPEPTIDE SYNONYMS / CARRIER AMINO ACID SEQUENCES / CARRIER GENE SEQUENCES / CARRIER PFAM / CARRIER GO CLASSIFIERS
#
        if(j.tag == '{http://www.drugbank.ca}carriers'):
          carriers = []
          for k in j.getchildren():
            if(k.tag == '{http://www.drugbank.ca}carrier'):
              carrier = []
              POSITION = "NULL"
              NAME = "NULL"
              ORGANISM = "NULL"
              KNOWN_ACTION = "NULL"
              CARRIER_INHIBITION_STRENGTH = "NULL"
              CARRIER_INDUCTION_STRENGTH = "NULL"
              actions = []
              carrier_references = []
              carrier_polypeptides = []
              if(('position' in k.attrib.keys()) and k.attrib['position'] != ""):
                POSITION = k.attrib['position'].rstrip()
              for m in k.getchildren():
                if(m.tag == '{http://www.drugbank.ca}id'):
                  ID = m.text
                if(m.tag == '{http://www.drugbank.ca}name'):
                  NAME = m.text
                if(m.tag == '{http://www.drugbank.ca}organism' and m.text is not None):
                  ORGANISM = m.text
                if(m.tag == '{http://www.drugbank.ca}known-action' and m.text is not None):
                  KNOWN_ACTION = m.text
                if(m.tag == '{http://www.drugbank.ca}inhibition-strength'):
                  print(m.text)
                  CARRIER_INHIBITION_STRENGTH = m.text
                if(m.tag == '{http://www.drugbank.ca}induction-strength'):
                  CARRIER_INDUCTION_STRENGTH = m.text
                if(m.tag == '{http://www.drugbank.ca}actions'):
                  for n in m.getchildren():
                    if(n.tag == '{http://www.drugbank.ca}action'): 
                      ACTION = n.text
                  actions.append(ACTION)
                if(m.tag == '{http://www.drugbank.ca}references' and m.text is not None):
                  temp_carrier_references = m.text.rstrip()
                  carrier_references = temp_carrier_references.split('#')
                if(m.tag == '{http://www.drugbank.ca}polypeptide' and m.text is not None):
                  carrier_polypeptide = []
                  CARRIER_POLYPEPTIDE_TRANSMEMBRANE_REGIONS = []
                  CARRIER_AMINO_ACID_SEQUENCE = "NULL"
                  CARRIER_AMINO_ACID_SEQUENCE_FORMAT = "NULL"
                  CARRIER_POLYPEPTIDE_GENERAL_FUNCTION = "NULL"
                  CARRIER_POLYPEPTIDE_SIGNAL_REGIONS = []
                  CARRIER_POLYPEPTIDE_LOCUS = "NULL"
                  CARRIER_POLYPEPTIDE_THEORETICAL_PI = "NULL"
                  CARRIER_POLYPEPTIDE_CHROMOSOME_LOCATION = "NULL"
                  CARRIER_GENE_SEQUENCE = "NULL"
                  CARRIER_GENE_SEQUENCE_FORMAT = "NULL"
                  CARRIER_POLYPEPTIDE_CELLULAR_LOCATION = "NULL"
                  CARRIER_POLYPEPTIDE_SPECIFIC_FUNCTION = "NULL"
                  CARRIER_POLYPEPTIDE_GENE_NAME = "NULL"
                  CARRIER_POLYPEPTIDE_MOLECULAR_WEIGHT = "NULL"
                  CARRIER_POLYPEPTIDE_ORGANISM_NAME = "NULL"
                  CARRIER_POLYPEPTIDE_ORGANISM_NCBI_TAXONOMY_ID = "NULL"
                  if(m.attrib['id'] != ""):
                    CARRIER_POLYPEPTIDE_ID = m.attrib['id'].rstrip()
                  if(m.attrib['source'] != ""):
                    CARRIER_POLYPEPTIDE_SOURCE = m.attrib['source'].rstrip()
                  for n in m.getchildren():
                    if(n.tag == '{http://www.drugbank.ca}name'):
                      CARRIER_POLYPEPTIDE_NAME = n.text
                    if(n.tag == '{http://www.drugbank.ca}general-function' and n.text is not None):
                      CARRIER_POLYPEPTIDE_GENERAL_FUNCTION = n.text
                    if(n.tag == '{http://www.drugbank.ca}specific-function' and n.text is not None):
                      CARRIER_POLYPEPTIDE_SPECIFIC_FUNCTION = n.text
                    if(n.tag == '{http://www.drugbank.ca}gene-name' and n.text is not None):
                      CARRIER_POLYPEPTIDE_GENE_NAME = n.text
                    if(n.tag == '{http://www.drugbank.ca}locus' and n.text is not None):
                      CARRIER_POLYPEPTIDE_LOCUS = n.text
                    if(n.tag == '{http://www.drugbank.ca}cellular-location' and n.text is not None):
                      CARRIER_POLYPEPTIDE_CELLULAR_LOCATION = n.text
                    if(n.tag == '{http://www.drugbank.ca}signal-regions' and n.text is not None):
                      temp_polypeptide_signal_regions = n.text
                      CARRIER_POLYPEPTIDE_SIGNAL_REGIONS = temp_polypeptide_signal_regions.split('-')
                      CARRIER_POLYPEPTIDE_SIGNAL_REGIONS_LOWER = CARRIER_POLYPEPTIDE_SIGNAL_REGIONS[0]
                      CARRIER_POLYPEPTIDE_SIGNAL_REGIONS_UPPER = CARRIER_POLYPEPTIDE_SIGNAL_REGIONS[1]
                    if(n.tag == '{http://www.drugbank.ca}theoretical-pi' and n.text is not None):
                      CARRIER_POLYPEPTIDE_THEORETICAL_PI = n.text
                    if(n.tag == '{http://www.drugbank.ca}molecular-weight' and n.text is not None):
                      CARRIER_POLYPEPTIDE_MOLECULAR_WEIGHT = n.text
                    if(n.tag == '{http://www.drugbank.ca}chromosome-location' and n.text is not None):
                      CARRIER_POLYPEPTIDE_CHROMOSOME_LOCATION = n.text
                    if(n.tag == '{http://www.drugbank.ca}organism' and n.text is not None):
                      CARRIER_POLYPEPTIDE_ORGANISM = n.text
                      if(n.attrib['ncbi-taxonomy-id'] != ""):
                        CARRIER_POLYPEPTIDE_ORGANISM_NCBI_TAXONOMY_ID = n.attrib['ncbi-taxonomy-id'].rstrip()
                    if(n.tag == '{http://www.drugbank.ca}inhibition-strength'):
                      print("Does inhibition strength exist in carrier?")
                      CARRIER_POLYPEPTIDE_INHIBITION_STRENGTH = n.text
                    if(n.tag == '{http://www.drugbank.ca}induction-strength'):
                      CARRIER_POLYPEPTIDE_INDUCTION_STRENGTH = n.text
                    if(n.tag == '{http://www.drugbank.ca}transmembrane-regions' and n.text is not None):
                      temp_polypeptide_transmembrane_regions = n.text
                      CARRIER_POLYPEPTIDE_TRANSMEMBRANE_REGIONS = temp_polypeptide_transmembrane_regions.split('-')
                    if(n.tag == '{http://www.drugbank.ca}external-identifiers'):
                      external_identifiers = []
                      for p in n.getchildren():
                        if(p.tag == '{http://www.drugbank.ca}external-identifier'):
                          external_identifier = []
                          for q in p.getchildren():
                            if(q.tag == '{http://www.drugbank.ca}resource'):
                              CARRIER_POLYPEPTIDE_EXT_RESOURCE = q.text
                            if(q.tag == '{http://www.drugbank.ca}identifier'):
                              CARRIER_POLYPEPTIDE_EXT_IDENTIFIER = q.text
                          external_identifier.append(CARRIER_POLYPEPTIDE_EXT_RESOURCE)
                          external_identifier.append(CARRIER_POLYPEPTIDE_EXT_IDENTIFIER)
                          external_identifiers.append(external_identifier)
                    if(n.tag == '{http://www.drugbank.ca}synonyms'):
                      carrier_synonyms = []
                      for p in n.getchildren():
                        if(p.tag == '{http://www.drugbank.ca}synonym'):
                          CARRIER_SYNONYM = p.text
                          carrier_synonyms.append(CARRIER_SYNONYM)
                    if(n.tag == '{http://www.drugbank.ca}amino-acid-sequence' and n.text is not None):
                      CARRIER_AMINO_ACID_SEQUENCE = n.text
                      if(n.attrib['format'] != ""):
                        CARRIER_AMINO_ACID_SEQUENCE_FORMAT = n.attrib['format'].rstrip()
                    if(n.tag == '{http://www.drugbank.ca}gene-sequence' and n.text is not None):
                      CARRIER_GENE_SEQUENCE = n.text
                      if(n.attrib['format'] != ""):
                        CARRIER_GENE_SEQUENCE_FORMAT = n.attrib['format'].rstrip()
                    if(n.tag == '{http://www.drugbank.ca}pfams'):
                      pfams = []
                      for p in n.getchildren():
                        if(p.tag == '{http://www.drugbank.ca}pfam'):
                          pfam = []
                          for q in p.getchildren():
                            if(q.tag == '{http://www.drugbank.ca}identifier'):
                              CARRIER_POLYPEPTIDE_PFAM_IDENTIFIER = q.text
                            if(q.tag == '{http://www.drugbank.ca}name'):
                              CARRIER_POLYPEPTIDE_PFAM_NAME = q.text
                          pfam.append(CARRIER_POLYPEPTIDE_PFAM_IDENTIFIER)
                          pfam.append(CARRIER_POLYPEPTIDE_PFAM_NAME)
                          pfams.append(pfam)
                    if(n.tag == '{http://www.drugbank.ca}go-classifiers'):
                      go_classifiers = []
                      for p in n.getchildren():
                        if(p.tag == '{http://www.drugbank.ca}go-classifier'):
                          go_classifier = []
                          for q in p.getchildren():
                            if(q.tag == '{http://www.drugbank.ca}category'):
                              CARRIER_POLYPEPTIDE_GO_CATEGORY = q.text
                            if(q.tag == '{http://www.drugbank.ca}description'):
                              CARRIER_POLYPEPTIDE_GO_DESCRIPTION = q.text
                          go_classifier.append(CARRIER_POLYPEPTIDE_GO_CATEGORY)
                          go_classifier.append(CARRIER_POLYPEPTIDE_GO_DESCRIPTION)
                          go_classifiers.append(go_classifier)
                    
                  carrier_polypeptide.append(CARRIER_POLYPEPTIDE_ID)
                  carrier_polypeptide.append(CARRIER_POLYPEPTIDE_SOURCE)
                  carrier_polypeptide.append(CARRIER_POLYPEPTIDE_NAME)
                  carrier_polypeptide.append(CARRIER_POLYPEPTIDE_GENERAL_FUNCTION)
                  carrier_polypeptide.append(CARRIER_POLYPEPTIDE_SPECIFIC_FUNCTION)
                  carrier_polypeptide.append(CARRIER_POLYPEPTIDE_GENE_NAME)
                  carrier_polypeptide.append(CARRIER_POLYPEPTIDE_LOCUS)
                  carrier_polypeptide.append(CARRIER_POLYPEPTIDE_CELLULAR_LOCATION)
                  carrier_polypeptide.append(CARRIER_POLYPEPTIDE_SIGNAL_REGIONS_LOWER)
                  carrier_polypeptide.append(CARRIER_POLYPEPTIDE_SIGNAL_REGIONS_UPPER)
                  carrier_polypeptide.append(CARRIER_POLYPEPTIDE_THEORETICAL_PI)
                  carrier_polypeptide.append(CARRIER_POLYPEPTIDE_MOLECULAR_WEIGHT)
                  carrier_polypeptide.append(CARRIER_POLYPEPTIDE_CHROMOSOME_LOCATION)
                  carrier_polypeptide.append(CARRIER_POLYPEPTIDE_ORGANISM)
                  carrier_polypeptide.append(CARRIER_POLYPEPTIDE_ORGANISM_NCBI_TAXONOMY_ID)
                  carrier_polypeptide.append(CARRIER_POLYPEPTIDE_TRANSMEMBRANE_REGIONS)
                  carrier_polypeptide.append(external_identifiers)
                  carrier_polypeptide.append(carrier_synonyms)
                  carrier_polypeptide.append(CARRIER_AMINO_ACID_SEQUENCE)
                  carrier_polypeptide.append(CARRIER_AMINO_ACID_SEQUENCE_FORMAT)
                  carrier_polypeptide.append(CARRIER_GENE_SEQUENCE)
                  carrier_polypeptide.append(CARRIER_GENE_SEQUENCE_FORMAT)
                  carrier_polypeptide.append(pfams)
                  carrier_polypeptide.append(go_classifiers)
                  carrier_polypeptides.append(carrier_polypeptide)
              carrier.append(POSITION)
              carrier.append(ID) 
              carrier.append(NAME) 
              carrier.append(ORGANISM) 
              carrier.append(KNOWN_ACTION)
              carrier.append(CARRIER_INHIBITION_STRENGTH)
              carrier.append(CARRIER_INDUCTION_STRENGTH)
              carrier.append(actions) 
              carrier.append(carrier_references) 
              carrier.append(carrier_polypeptides)
              carriers.append(carrier)

#
#		GETTING DRUGBANK TRANSPORTERS / TRANSPORTER ACTIONS / TRANSPORTER REFERENCES / TRANSPORTER POLYPEPTIDES / TRANSPORTER POLYPEPTIDE TRANSMEMBRANE REGIONS / TRANSPORTER POLYPEPTIDE EXTERNAL IDENTIFIERS / TRANSPORTER POLYPEPTIDE SYNONYMS / TRANSPORTER AMINO ACID SEQUENCES / TRANSPORTER GENE SEQUENCES / TRANSPORTER PFAM / TRANSPORTER GO CLASSIFIERS
#
        if(j.tag == '{http://www.drugbank.ca}transporters'):
          transporters = []
          for k in j.getchildren():
            if(k.tag == '{http://www.drugbank.ca}transporter'):
              transporter = []
              POSITION = "NULL"
              NAME = "NULL"
              ORGANISM = "NULL"
              KNOWN_ACTION = "NULL"
              TRANSPORTER_INHIBITION_STRENGTH = "NULL"
              TRANSPORTER_INDUCTION_STRENGTH = "NULL"
              actions = []
              transporter_references = []
              transporter_polypeptides = []
              if(('position' in k.attrib.keys()) and k.attrib['position'] != ""):
                POSITION = k.attrib['position'].rstrip()
              for m in k.getchildren():
                if(m.tag == '{http://www.drugbank.ca}id'):
                  ID = m.text
                if(m.tag == '{http://www.drugbank.ca}name'):
                  NAME = m.text
                if(m.tag == '{http://www.drugbank.ca}organism' and m.text is not None):
                  ORGANISM = m.text
                if(m.tag == '{http://www.drugbank.ca}known-action' and m.text is not None):
                  KNOWN_ACTION = m.text
                if(m.tag == '{http://www.drugbank.ca}inhibition-strength'):
                  TRANSPORTER_INHIBITION_STRENGTH = m.text
                if(m.tag == '{http://www.drugbank.ca}induction-strength'):
                  TRANSPORTER_INDUCTION_STRENGTH = m.text
                if(m.tag == '{http://www.drugbank.ca}actions'):
                  for n in m.getchildren():
                    if(n.tag == '{http://www.drugbank.ca}action'): 
                      ACTION = n.text
                  actions.append(ACTION)
                if(m.tag == '{http://www.drugbank.ca}references' and m.text is not None):
                  temp_transporter_references = m.text.rstrip()
                  transporter_references = temp_transporter_references.split('#')
                if(m.tag == '{http://www.drugbank.ca}polypeptide' and m.text is not None):
                  transporter_polypeptide = []
                  TRANSPORTER_POLYPEPTIDE_TRANSMEMBRANE_REGIONS = []
                  TRANSPORTER_AMINO_ACID_SEQUENCE = "NULL"
                  TRANSPORTER_AMINO_ACID_SEQUENCE_FORMAT = "NULL"
                  TRANSPORTER_POLYPEPTIDE_GENERAL_FUNCTION = "NULL"
                  TRANSPORTER_POLYPEPTIDE_SIGNAL_REGIONS = []
                  TRANSPORTER_POLYPEPTIDE_LOCUS = "NULL"
                  TRANSPORTER_POLYPEPTIDE_THEORETICAL_PI = "NULL"
                  TRANSPORTER_POLYPEPTIDE_CHROMOSOME_LOCATION = "NULL"
                  TRANSPORTER_GENE_SEQUENCE = "NULL"
                  TRANSPORTER_GENE_SEQUENCE_FORMAT = "NULL"
                  TRANSPORTER_POLYPEPTIDE_CELLULAR_LOCATION = "NULL"
                  TRANSPORTER_POLYPEPTIDE_SPECIFIC_FUNCTION = "NULL"
                  TRANSPORTER_POLYPEPTIDE_GENE_NAME = "NULL"
                  TRANSPORTER_POLYPEPTIDE_MOLECULAR_WEIGHT = "NULL"
                  TRANSPORTER_POLYPEPTIDE_ORGANISM_NAME = "NULL"
                  TRANSPORTER_POLYPEPTIDE_ORGANISM_NCBI_TAXONOMY_ID = "NULL"
                  TRANSPORTER_POLYPEPTIDE_SIGNAL_REGIONS_LOWER = "NULL"
                  TRANSPORTER_POLYPEPTIDE_SIGNAL_REGIONS_UPPER = "NULL"
                  if(m.attrib['id'] != ""):
                    TRANSPORTER_POLYPEPTIDE_ID = m.attrib['id'].rstrip()
                  if(m.attrib['source'] != ""):
                    TRANSPORTER_POLYPEPTIDE_SOURCE = m.attrib['source'].rstrip()
                  for n in m.getchildren():
                    if(n.tag == '{http://www.drugbank.ca}name'):
                      TRANSPORTER_POLYPEPTIDE_NAME = n.text
                    if(n.tag == '{http://www.drugbank.ca}general-function' and n.text is not None):
                      TRANSPORTER_POLYPEPTIDE_GENERAL_FUNCTION = n.text
                    if(n.tag == '{http://www.drugbank.ca}specific-function' and n.text is not None):
                      TRANSPORTER_POLYPEPTIDE_SPECIFIC_FUNCTION = n.text
                    if(n.tag == '{http://www.drugbank.ca}gene-name' and n.text is not None):
                      TRANSPORTER_POLYPEPTIDE_GENE_NAME = n.text
                    if(n.tag == '{http://www.drugbank.ca}locus' and n.text is not None):
                      TRANSPORTER_POLYPEPTIDE_LOCUS = n.text
                    if(n.tag == '{http://www.drugbank.ca}cellular-location' and n.text is not None):
                      TRANSPORTER_POLYPEPTIDE_CELLULAR_LOCATION = n.text
                    if(n.tag == '{http://www.drugbank.ca}signal-regions' and n.text is not None):
                      temp_polypeptide_signal_regions = n.text
                      TRANSPORTER_POLYPEPTIDE_SIGNAL_REGIONS = temp_polypeptide_signal_regions.split('-')
                      TRANSPORTER_POLYPEPTIDE_SIGNAL_REGIONS_LOWER = TRANSPORTER_POLYPEPTIDE_SIGNAL_REGIONS[0]
                      TRANSPORTER_POLYPEPTIDE_SIGNAL_REGIONS_UPPER = TRANSPORTER_POLYPEPTIDE_SIGNAL_REGIONS[1]
                    if(n.tag == '{http://www.drugbank.ca}theoretical-pi' and n.text is not None):
                      TRANSPORTER_POLYPEPTIDE_THEORETICAL_PI = n.text
                    if(n.tag == '{http://www.drugbank.ca}molecular-weight' and n.text is not None):
                      TRANSPORTER_POLYPEPTIDE_MOLECULAR_WEIGHT = n.text
                    if(n.tag == '{http://www.drugbank.ca}chromosome-location' and n.text is not None):
                      TRANSPORTER_POLYPEPTIDE_CHROMOSOME_LOCATION = n.text
                    if(n.tag == '{http://www.drugbank.ca}organism' and n.text is not None):
                      TRANSPORTER_POLYPEPTIDE_ORGANISM = n.text
                      if(n.attrib['ncbi-taxonomy-id'] != ""):
                        TRANSPORTER_POLYPEPTIDE_ORGANISM_NCBI_TAXONOMY_ID = n.attrib['ncbi-taxonomy-id'].rstrip()
                    if(n.tag == '{http://www.drugbank.ca}inhibition-strength'):
                      TRANSPORTER_POLYPEPTIDE_INHIBITION_STRENGTH = n.text
                    if(n.tag == '{http://www.drugbank.ca}induction-strength'):
                      TRANSPORTER_POLYPEPTIDE_INDUCTION_STRENGTH = n.text
                    if(n.tag == '{http://www.drugbank.ca}transmembrane-regions' and n.text is not None):
                      temp_polypeptide_transmembrane_regions = n.text
                      TRANSPORTER_POLYPEPTIDE_TRANSMEMBRANE_REGIONS = temp_polypeptide_transmembrane_regions.split('-')
                    if(n.tag == '{http://www.drugbank.ca}external-identifiers'):
                      external_identifiers = []
                      for p in n.getchildren():
                        if(p.tag == '{http://www.drugbank.ca}external-identifier'):
                          external_identifier = []
                          for q in p.getchildren():
                            if(q.tag == '{http://www.drugbank.ca}resource'):
                              TRANSPORTER_POLYPEPTIDE_EXT_RESOURCE = q.text
                            if(q.tag == '{http://www.drugbank.ca}identifier'):
                              TRANSPORTER_POLYPEPTIDE_EXT_IDENTIFIER = q.text
                          external_identifier.append(TRANSPORTER_POLYPEPTIDE_EXT_RESOURCE)
                          external_identifier.append(TRANSPORTER_POLYPEPTIDE_EXT_IDENTIFIER)
                          external_identifiers.append(external_identifier)
                    if(n.tag == '{http://www.drugbank.ca}synonyms'):
                      transporter_synonyms = []
                      for p in n.getchildren():
                        if(p.tag == '{http://www.drugbank.ca}synonym'):
                          TRANSPORTER_SYNONYM = p.text
                          transporter_synonyms.append(TRANSPORTER_SYNONYM)
                    if(n.tag == '{http://www.drugbank.ca}amino-acid-sequence' and n.text is not None):
                      TRANSPORTER_AMINO_ACID_SEQUENCE = n.text
                      if(n.attrib['format'] != ""):
                        TRANSPORTER_AMINO_ACID_SEQUENCE_FORMAT = n.attrib['format'].rstrip()
                    if(n.tag == '{http://www.drugbank.ca}gene-sequence' and n.text is not None):
                      TRANSPORTER_GENE_SEQUENCE = n.text
                      if(n.attrib['format'] != ""):
                        TRANSPORTER_GENE_SEQUENCE_FORMAT = n.attrib['format'].rstrip()
                    if(n.tag == '{http://www.drugbank.ca}pfams'):
                      pfams = []
                      for p in n.getchildren():
                        if(p.tag == '{http://www.drugbank.ca}pfam'):
                          pfam = []
                          for q in p.getchildren():
                            if(q.tag == '{http://www.drugbank.ca}identifier'):
                              TRANSPORTER_POLYPEPTIDE_PFAM_IDENTIFIER = q.text
                            if(q.tag == '{http://www.drugbank.ca}name'):
                              TRANSPORTER_POLYPEPTIDE_PFAM_NAME = q.text
                          pfam.append(TRANSPORTER_POLYPEPTIDE_PFAM_IDENTIFIER)
                          pfam.append(TRANSPORTER_POLYPEPTIDE_PFAM_NAME)
                          pfams.append(pfam)
                    if(n.tag == '{http://www.drugbank.ca}go-classifiers'):
                      go_classifiers = []
                      for p in n.getchildren():
                        if(p.tag == '{http://www.drugbank.ca}go-classifier'):
                          go_classifier = []
                          for q in p.getchildren():
                            if(q.tag == '{http://www.drugbank.ca}category'):
                              TRANSPORTER_POLYPEPTIDE_GO_CATEGORY = q.text
                            if(q.tag == '{http://www.drugbank.ca}description'):
                              TRANSPORTER_POLYPEPTIDE_GO_DESCRIPTION = q.text
                          go_classifier.append(TRANSPORTER_POLYPEPTIDE_GO_CATEGORY)
                          go_classifier.append(TRANSPORTER_POLYPEPTIDE_GO_DESCRIPTION)
                          go_classifiers.append(go_classifier)
                    
                  transporter_polypeptide.append(TRANSPORTER_POLYPEPTIDE_ID)
                  transporter_polypeptide.append(TRANSPORTER_POLYPEPTIDE_SOURCE)
                  transporter_polypeptide.append(TRANSPORTER_POLYPEPTIDE_NAME)
                  transporter_polypeptide.append(TRANSPORTER_POLYPEPTIDE_GENERAL_FUNCTION)
                  transporter_polypeptide.append(TRANSPORTER_POLYPEPTIDE_SPECIFIC_FUNCTION)
                  transporter_polypeptide.append(TRANSPORTER_POLYPEPTIDE_GENE_NAME)
                  transporter_polypeptide.append(TRANSPORTER_POLYPEPTIDE_LOCUS)
                  transporter_polypeptide.append(TRANSPORTER_POLYPEPTIDE_CELLULAR_LOCATION)
                  transporter_polypeptide.append(TRANSPORTER_POLYPEPTIDE_SIGNAL_REGIONS_LOWER)
                  transporter_polypeptide.append(TRANSPORTER_POLYPEPTIDE_SIGNAL_REGIONS_UPPER)
                  transporter_polypeptide.append(TRANSPORTER_POLYPEPTIDE_THEORETICAL_PI)
                  transporter_polypeptide.append(TRANSPORTER_POLYPEPTIDE_MOLECULAR_WEIGHT)
                  transporter_polypeptide.append(TRANSPORTER_POLYPEPTIDE_CHROMOSOME_LOCATION)
                  transporter_polypeptide.append(TRANSPORTER_POLYPEPTIDE_ORGANISM)
                  transporter_polypeptide.append(TRANSPORTER_POLYPEPTIDE_ORGANISM_NCBI_TAXONOMY_ID)
                  transporter_polypeptide.append(TRANSPORTER_POLYPEPTIDE_TRANSMEMBRANE_REGIONS)
                  transporter_polypeptide.append(external_identifiers)
                  transporter_polypeptide.append(transporter_synonyms)
                  transporter_polypeptide.append(TRANSPORTER_AMINO_ACID_SEQUENCE)
                  transporter_polypeptide.append(TRANSPORTER_AMINO_ACID_SEQUENCE_FORMAT)
                  transporter_polypeptide.append(TRANSPORTER_GENE_SEQUENCE)
                  transporter_polypeptide.append(TRANSPORTER_GENE_SEQUENCE_FORMAT)
                  transporter_polypeptide.append(pfams)
                  transporter_polypeptide.append(go_classifiers)
                  transporter_polypeptides.append(transporter_polypeptide)
              transporter.append(POSITION)
              transporter.append(ID) 
              transporter.append(NAME) 
              transporter.append(ORGANISM) 
              transporter.append(KNOWN_ACTION)
              transporter.append(TRANSPORTER_INHIBITION_STRENGTH)
              transporter.append(TRANSPORTER_INDUCTION_STRENGTH)
              transporter.append(actions) 
              transporter.append(transporter_references) 
              transporter.append(transporter_polypeptides)
              transporters.append(transporter)

#
#	GETTING DRUGBANK NAMES
#
        if(j.tag == '{http://www.drugbank.ca}name'):
          NAME = j.text.rstrip()

#
#	GETTING DRUGBANK DESCRIPTIONS
#
        if(j.tag == '{http://www.drugbank.ca}description' and j.text is not None):
          DESCRIPTION = j.text.rstrip()
          
#
#	GETTING DRUGBANK CAS NUMBERS
#
        if(j.tag == '{http://www.drugbank.ca}cas-number' and j.text is not None):
          CAS_NUMBER = j.text.rstrip()

#
#	GETTING DRUGBANK GROUPS
#
        if(j.tag == '{http://www.drugbank.ca}groups'):
          drug_groups = []
          for k in j.getchildren():
            if(k.tag == '{http://www.drugbank.ca}group'):
              DRUG_GROUP = k.text.rstrip()
              drug_groups.append(DRUG_GROUP)

#
#	GETTING DRUGBANK GENERAL REFERENCES
#
        if(j.tag == '{http://www.drugbank.ca}general-references' and j.text is not None):
          temp_drug_references = j.text.rstrip()
          drug_general_references = temp_drug_references.split('#')

#
#	GETTING DRUGBANK SYNTHESIS REFERENCES
#
        if(j.tag == '{http://www.drugbank.ca}synthesis-reference' and j.text is not None):
          SYNTHESIS_REFERENCE = j.text.rstrip()

#
#	GETTING DRUGBANK INDICATIONS
#
        if(j.tag == '{http://www.drugbank.ca}indication' and j.text is not None):
          INDICATION = j.text.rstrip()

#
#	GETTING DRUGBANK PHARMACODYNAMICS
#
        if(j.tag == '{http://www.drugbank.ca}pharmacodynamics' and j.text is not None):
          PHARMACODYNAMICS = j.text.rstrip()

#
#	GETTING DRUGBANK MECHANISMS OF ACTION
#
        if(j.tag == '{http://www.drugbank.ca}mechanism-of-action' and j.text is not None):
          MECHANISM_OF_ACTION = j.text.rstrip()

#
#	GETTING DRUGBANK TOXICITY
#
        if(j.tag == '{http://www.drugbank.ca}toxicity' and j.text is not None):
          TOXICITY = j.text.rstrip()

#
#	GETTING DRUGBANK METABOLISMS
#
        if(j.tag == '{http://www.drugbank.ca}metabolism' and j.text is not None):
          METABOLISM = j.text.rstrip()

#
#	GETTING DRUGBANK ABSORPTIONS
#
        if(j.tag == '{http://www.drugbank.ca}absorption' and j.text is not None):
          ABSORPTION = j.text.rstrip()

#
#	GETTING DRUGBANK HALF LIVES
#
        if(j.tag == '{http://www.drugbank.ca}half-life' and j.text is not None):
          HALF_LIFE = j.text.rstrip()

#
#	GETTING DRUGBANK PROTEIN BINDINGS
#
        if(j.tag == '{http://www.drugbank.ca}protein-binding' and j.text is not None):
          PROTEIN_BINDING = j.text.rstrip()

#
#	GETTING DRUGBANK ROUTES OF ELIMINATION
#
        if(j.tag == '{http://www.drugbank.ca}route-of-elimination' and j.text is not None):
          ROUTE_OF_ELIMINATION = j.text.rstrip()

#
#	GETTING DRUGBANK VOLUMES OF DISTRIBUTION
#
        if(j.tag == '{http://www.drugbank.ca}volume-of-distribution' and j.text is not None):
          temp_volume_of_distribution = j.text.rstrip()
          volumes_of_distribution = temp_volume_of_distribution.split('*')

#
#	GETTING DRUGBANK CLEARANCES
#
        if(j.tag == '{http://www.drugbank.ca}clearance' and j.text is not None):
          temp_clearances = j.text.rstrip()
          clearances = temp_clearances.split('*')

#
#	GETTING DRUGBANK CLASSIFICATIONS / ALTERNATIVE PARENTS / SUBSTITUENTS
#
        if(j.tag == '{http://www.drugbank.ca}classification'):
          classification = []
          alternative_parents = []
          substituents = []
          CLASSIFICATION_DESCRIPTION = "NULL"
          CLASSIFICATION_DIRECT_PARENT = "NULL"
          CLASSIFICATION_KINGDOM = "NULL"
          CLASSIFICATION_SUPERCLASS = "NULL"
          CLASSIFICATION_DRUG_CLASS = "NULL"
          CLASSIFICATION_SUBCLASS = "NULL"
          for k in j.getchildren():
            if(k.tag == '{http://www.drugbank.ca}description' and k.text is not None):
              CLASSIFICATION_DESCRIPTION = k.text.rstrip()
            if(k.tag == '{http://www.drugbank.ca}direct-parent' and k.text is not None):
              CLASSIFICATION_DIRECT_PARENT = k.text.rstrip()
            if(k.tag == '{http://www.drugbank.ca}kingdom' and k.text is not None):
              CLASSIFICATION_KINGDOM = k.text.rstrip()
            if(k.tag == '{http://www.drugbank.ca}superclass' and k.text is not None):
              CLASSIFICATION_SUPERCLASS = k.text.rstrip()
            if(k.tag == '{http://www.drugbank.ca}drug-class' and k.text is not None):
              CLASSIFICATION_DRUG_CLASS = k.text.rstrip()
            if(k.tag == '{http://www.drugbank.ca}subclass' and k.text is not None):
              CLASSIFICATION_SUBCLASS = k.text.rstrip()
            if(k.tag == '{http://www.drugbank.ca}alternative-parent' and k.text is not None):
              alternative_parents.append(k.text.rstrip())
            if(k.tag == '{http://www.drugbank.ca}substituent' and k.text is not None):
              substituents.append(k.text.rstrip())
          classification.append([CLASSIFICATION_DESCRIPTION, CLASSIFICATION_DIRECT_PARENT, CLASSIFICATION_KINGDOM, CLASSIFICATION_SUPERCLASS, CLASSIFICATION_DRUG_CLASS, CLASSIFICATION_SUBCLASS])

#
#	GETTING DRUGBANK SALT
#
        if(j.tag == '{http://www.drugbank.ca}salts'):
          salts = {}
          for k in j.getchildren():
            if(k.tag == '{http://www.drugbank.ca}salt'):
              PRIMARY_DRUGBANK_ID_SALT = "NULL"
              SALT_NAME = "NULL"
              SALT_CAS_NUMBER = "NULL"
              SALT_INCHIKEY = "NULL"
              for m in k.getchildren():
                if(m.tag == '{http://www.drugbank.ca}drugbank-id' and m.text is not None):
                  PRIMARY_DRUGBANK_ID_SALT = m.text.rstrip()
                if(m.tag == '{http://www.drugbank.ca}name' and m.text is not None):
                  SALT_NAME = m.text.rstrip()
                if(m.tag == '{http://www.drugbank.ca}cas-number' and m.text is not None):
                  SALT_CAS_NUMBER = m.text.rstrip()
                if(m.tag == '{http://www.drugbank.ca}inchikey' and m.text is not None):
                  SALT_INCHIKEY = m.text.rstrip()
              salts[PRIMARY_DRUGBANK_ID_SALT] = [SALT_NAME, SALT_CAS_NUMBER, SALT_INCHIKEY]

#
#	GETTING DRUGBANK SYNONYMS
#
        if(j.tag == '{http://www.drugbank.ca}synonyms'):
          synonyms = {}
          for k in j.getchildren():
            SYNONYM = "NULL"
            SYNONYM_LANGUAGE = "NULL"
            SYNONYM_CODER = "NULL"
            if(k.tag == '{http://www.drugbank.ca}synonym' and k.text is not None):
              SYNONYM = k.text.rstrip()
              if(k.attrib['language'] != ""):
                SYNONYM_LANGUAGE = k.attrib['language'].rstrip()
              if(k.attrib['coder'] != ""):
                SYNONYM_CODER = k.attrib['coder'].rstrip()
            synonyms[SYNONYM] = [SYNONYM_LANGUAGE, SYNONYM_CODER]

#
#	GETTING DRUGBANK PRODUCTS
#
        if(j.tag == '{http://www.drugbank.ca}products'):
          products = {}
          for k in j.getchildren():
            if(k.tag == '{http://www.drugbank.ca}product'):
              PRODUCT_NAME = "NULL"
              PRODUCT_NDC_ID = "NULL"
              PRODUCT_NDC_PRODUCT_CODE = "NULL"
              PRODUCT_DPD_ID = "NULL"
              PRODUCT_STARTED_MARKETING_ON = "NULL"
              PRODUCT_ENDED_MARKETING_ON = "NULL"
              PRODUCT_DOSAGE_FORM = "NULL"
              PRODUCT_STRENGTH = "NULL"
              PRODUCT_ROUTE = "NULL"
              PRODUCT_FDA_APPLICATION_NUMBER = "NULL"
              PRODUCT_GENERIC = "NULL"
              PRODUCT_OVER_THE_COUNTER = "NULL"
              PRODUCT_APPROVED = "NULL"
              PRODUCT_COUNTRY = "NULL"
              PRODUCT_SOURCE = "NULL"
              for m in k.getchildren():
                if(m.tag == '{http://www.drugbank.ca}name' and m.text is not None):
                  PRODUCT_NAME = m.text.rstrip()
                if(m.tag == '{http://www.drugbank.ca}ndc-id' and m.text is not None):
                  print("Product NDC ID??")
                  PRODUCT_NDC_ID = m.text.rstrip()
                if(m.tag == '{http://www.drugbank.ca}ndc-product-code' and m.text is not None):
                  PRODUCT_NDC_PRODUCT_CODE = m.text.rstrip()
                if(m.tag == '{http://www.drugbank.ca}dpd-id' and m.text is not None):
                  PRODUCT_DPD_ID = m.text.rstrip()
                if(m.tag == '{http://www.drugbank.ca}started-marketing-on' and m.text is not None):
                  PRODUCT_STARTED_MARKETING_ON = m.text.rstrip()
                if(m.tag == '{http://www.drugbank.ca}ended-marketing-on' and m.text is not None):
                  PRODUCT_ENDED_MARKETING_ON = m.text.rstrip()
                if(m.tag == '{http://www.drugbank.ca}dosage-form' and m.text is not None):
                  PRODUCT_DOSAGE_FORM = m.text.rstrip()
                if(m.tag == '{http://www.drugbank.ca}strength' and m.text is not None):
                  PRODUCT_STRENGTH = m.text.rstrip()
                if(m.tag == '{http://www.drugbank.ca}route' and m.text is not None):
                  PRODUCT_ROUTE = m.text.rstrip()
                if(m.tag == '{http://www.drugbank.ca}fda-application-number' and m.text is not None):
                  PRODUCT_FDA_APPLICATION_NUMBER = m.text.rstrip()
                if(m.tag == '{http://www.drugbank.ca}generic' and m.text is not None):
                  PRODUCT_GENERIC = m.text.rstrip().upper()
                if(m.tag == '{http://www.drugbank.ca}over-the-counter' and m.text is not None):
                  PRODUCT_OVER_THE_COUNTER = m.text.rstrip().upper()
                if(m.tag == '{http://www.drugbank.ca}approved' and m.text is not None):
                  PRODUCT_APPROVED = m.text.rstrip().upper()
                if(m.tag == '{http://www.drugbank.ca}country' and m.text is not None):
                  PRODUCT_COUNTRY = m.text.rstrip()
                if(m.tag == '{http://www.drugbank.ca}source' and m.text is not None):
                  PRODUCT_SOURCE = m.text.rstrip()
                products[PRODUCT_NAME] = [PRODUCT_NDC_ID, PRODUCT_NDC_PRODUCT_CODE, PRODUCT_DPD_ID, PRODUCT_STARTED_MARKETING_ON, PRODUCT_ENDED_MARKETING_ON, PRODUCT_DOSAGE_FORM, PRODUCT_STRENGTH, PRODUCT_ROUTE, PRODUCT_FDA_APPLICATION_NUMBER, PRODUCT_GENERIC, PRODUCT_OVER_THE_COUNTER, PRODUCT_APPROVED, PRODUCT_COUNTRY, PRODUCT_SOURCE]
              

      outfile_drugs.write("%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s\n" % (PRIMARY_DRUGBANK_ID, NAME, DESCRIPTION, CAS_NUMBER, SYNTHESIS_REFERENCE, INDICATION, PHARMACODYNAMICS, MECHANISM_OF_ACTION, TOXICITY, METABOLISM, ABSORPTION, HALF_LIFE, PROTEIN_BINDING, ROUTE_OF_ELIMINATION, DRUG_TYPE, CREATED, UPDATED))

      for DRUG_ALT_ID in drugbank_ids: 
        outfile_drug_alt_ids.write("%s|%s\n" % (DRUG_ALT_ID, PRIMARY_DRUGBANK_ID))

      for key, value in international_brands.items():
        if(key != "NULL" and value != "NULL"):
          outfile_drug_international_brands.write("%s|%s|%s\n" % (PRIMARY_DRUGBANK_ID, key, value))

      for FOOD_INTERACTION in drug_food_interactions:
        if(FOOD_INTERACTION is not None):
          outfile_drug_food_interactions.write("%s|%s\n" % (FOOD_INTERACTION, PRIMARY_DRUGBANK_ID))

      for DRUG_GROUP in drug_groups:
        if(DRUG_GROUP is not None):
          outfile_drug_groups.write("%s|%s\n" % (DRUG_GROUP, PRIMARY_DRUGBANK_ID))

      for GENERAL_REFERENCE in drug_general_references:
        if(GENERAL_REFERENCE is not None and GENERAL_REFERENCE != ""):
          outfile_drug_general_references.write("%s|%s\n" % (GENERAL_REFERENCE.lstrip().rstrip(), PRIMARY_DRUGBANK_ID))

      for VOLUME_OF_DISTRIBUTION in volumes_of_distribution:
        if(VOLUME_OF_DISTRIBUTION is not None and VOLUME_OF_DISTRIBUTION != ""):
          outfile_drug_volumes_of_distribution.write("%s|%s\n" % (VOLUME_OF_DISTRIBUTION.lstrip().rstrip(), PRIMARY_DRUGBANK_ID))

      for CLEARANCE in clearances:
        if(CLEARANCE is not None and CLEARANCE != ""):
          outfile_drug_clearances.write("%s|%s\n" % (CLEARANCE.lstrip().rstrip(), PRIMARY_DRUGBANK_ID))

      for CLASSIFICATION in classification:
        if(CLASSIFICATION):
          outfile_drug_classifications.write("%s|%s|%s|%s|%s|%s|%s\n" % (PRIMARY_DRUGBANK_ID, CLASSIFICATION[0], CLASSIFICATION[1], CLASSIFICATION[2], CLASSIFICATION[3], CLASSIFICATION[4], CLASSIFICATION[5]))

      for ALTERNATIVE_PARENT in alternative_parents:
        if(ALTERNATIVE_PARENT is not None):
          outfile_drug_classification_alt_parents.write("%s|%s\n" % (PRIMARY_DRUGBANK_ID, ALTERNATIVE_PARENT))

      for SUBSTITUENT in substituents:
        if(SUBSTITUENT is not None):
          outfile_drug_classification_substituents.write("%s|%s\n" % (PRIMARY_DRUGBANK_ID, SUBSTITUENT))

      for key, value in salts.items():
        if(key != "NULL" and value != "NULL"):
          outfile_drug_salts.write("%s|%s|%s|%s|%s\n" % (key, PRIMARY_DRUGBANK_ID, value[0], value[1], value[2]))

      for key, value in synonyms.items():
        if(key != "NULL" and value != "NULL"):
          outfile_drug_synonyms.write("%s|%s|%s|%s\n" % (key, value[0], value[1], PRIMARY_DRUGBANK_ID))

      for key, value in products.items():
        if(key != "NULL" and value != "NULL"):
          outfile_drug_products.write("%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s\n" % (key, value[0], value[1], value[2], value[3], value[4], value[5], value[6], value[7], value[8], value[9], value[10], value[11], value[12], value[13], PRIMARY_DRUGBANK_ID))

      for key, value in mixtures.items():
        if(key != "NULL" and value != "NULL"):
          outfile_drug_mixtures.write("%s|%s|%s\n" % (key, value, PRIMARY_DRUGBANK_ID))

      for key, value in packagers.items(): 
        if(key != "NULL"):
          outfile_drug_packagers.write("%s|%s|%s\n" % (key, value, PRIMARY_DRUGBANK_ID))

      for key, value in manufacturers.items():
        if(key != "NULL"):
          outfile_drug_manufacturers.write("%s|%s|%s\n" % (key, value, PRIMARY_DRUGBANK_ID))

      for key, value in prices.items():
        if(key != "NULL" and value != "NULL"):
          outfile_drug_prices.write("%s|%s|%s\n" % (key, value[1], PRIMARY_DRUGBANK_ID))

          for key2, value2 in value[0].items():
            if(key2 != "NULL" and value2 != "NULL"):
              outfile_drug_costs.write("%s|%s|%s|%s|%s\n" % (key2, value2, key, value[1], PRIMARY_DRUGBANK_ID))

      for key, value in categories.items():
        if(key != "NULL" and value != "NULL"):
          outfile_drug_categories.write("%s|%s\n" % (key, PRIMARY_DRUGBANK_ID))

          for mesh_id in value:
            outfile_drug_mesh_ids.write("%s|%s|%s\n" % (mesh_id, key, PRIMARY_DRUGBANK_ID))

      for AFFECTED_ORGANISM in affected_organisms:
        if (AFFECTED_ORGANISM is not None):
          outfile_drug_affected_organisms.write("%s|%s\n" % (AFFECTED_ORGANISM, PRIMARY_DRUGBANK_ID))

      for key, value in dosages.items():
        if(key != "NULL" and value != "NULL"):
          outfile_drug_dosages.write("%s|%s|%s|%s\n" % (key, value[0], value[1], PRIMARY_DRUGBANK_ID))

      for ATC_CODE in atc_codes:
        if(ATC_CODE is not None):
          outfile_drug_atc_codes.write("%s|%s\n" % (ATC_CODE, PRIMARY_DRUGBANK_ID))

      for ATC_CODE_LEVEL in atc_code_levels:
        if(ATC_CODE_LEVEL is not None):
          outfile_drug_atc_code_levels.write("%s|%s|%s|%s\n" % (ATC_CODE_LEVEL[1], ATC_CODE_LEVEL[2], ATC_CODE_LEVEL[0], PRIMARY_DRUGBANK_ID))

      for AHFS_CODE in ahfs_codes:
        if(AHFS_CODE is not None):
          outfile_drug_ahfs_codes.write("%s|%s\n" % (AHFS_CODE, PRIMARY_DRUGBANK_ID))

      for PATENT in patents:
        if(PATENT is not None):
          outfile_drug_patents.write("%s|%s|%s|%s|%s\n" % (PATENT[0], PATENT[1], PATENT[2], PATENT[3], PRIMARY_DRUGBANK_ID))

      for DRUG_INTERACTION in drug_drug_interactions:
        if(DRUG_INTERACTION is not None):
          outfile_drug_drug_interactions.write("%s|%s|%s|%s\n" % (PRIMARY_DRUGBANK_ID, DRUG_INTERACTION[0], DRUG_INTERACTION[1], DRUG_INTERACTION[2]))

      for PROPERTY in properties:
        if(PROPERTY is not None):
          outfile_drug_properties.write("%s|%s|%s|%s|%s|%s\n" % (PROPERTY[0], PROPERTY[1], PROPERTY[2], PRIMARY_DRUGBANK_ID, PROPERTY[3], PROPERTY[4]))

      for SEQUENCE in sequences:
        if(SEQUENCE is not None):
          outfile_drug_sequences.write("%s|%s|%s\n" % (SEQUENCE[0], SEQUENCE[1], PRIMARY_DRUGBANK_ID))

      for EXTERNAL_IDENTIFIER in external_identifiers:
        if(EXTERNAL_IDENTIFIER is not None):
          outfile_drug_external_identifiers.write("%s|%s|%s\n" % (EXTERNAL_IDENTIFIER[0], EXTERNAL_IDENTIFIER[1], PRIMARY_DRUGBANK_ID))

      for EXTERNAL_LINK in external_links:
        if(EXTERNAL_LINK is not None):
          outfile_drug_external_links.write("%s|%s|%s\n" % (EXTERNAL_LINK[0], EXTERNAL_LINK[1], PRIMARY_DRUGBANK_ID))

      for REACTION in reactions:
        if(REACTION is not None):
          outfile_drug_reactions.write("%s|%s\n" % (REACTION[0], PRIMARY_DRUGBANK_ID))

          for REACTION_ELEMENT in REACTION[1]:
            if(REACTION_ELEMENT is not None):
              outfile_drug_reaction_elements.write("%s|%s|%s|%s|%s|%s\n" % (PRIMARY_DRUGBANK_ID, REACTION_ELEMENT[0], REACTION_ELEMENT[1], REACTION_ELEMENT[2], REACTION_ELEMENT[3], REACTION[0]))

          for REACTION_ENZYME in REACTION[2]:
            if(REACTION_ENZYME is not None):
              outfile_drug_reaction_enzymes.write("%s|%s|%s|%s|%s\n" % (PRIMARY_DRUGBANK_ID, REACTION_ENZYME[0], REACTION[0], REACTION_ENZYME[1], REACTION_ENZYME[2]))
 
      for EFFECT in effects:
        if(EFFECT is not None):
          outfile_drug_snp_effects.write("%s|%s|%s|%s|%s|%s|%s|%s|%s\n" % (PRIMARY_DRUGBANK_ID, EFFECT[0], EFFECT[1], EFFECT[2], EFFECT[3], EFFECT[4], EFFECT[5], EFFECT[6], EFFECT[7]))

      for ADVERSE_DRUG_REACTION in adverse_drug_reactions:
        if(ADVERSE_DRUG_REACTION is not None):
          outfile_drug_snp_adverse_drug_reactions.write("%s|%s|%s|%s|%s|%s|%s|%s|%s\n" % (PRIMARY_DRUGBANK_ID, ADVERSE_DRUG_REACTION[0], ADVERSE_DRUG_REACTION[1], ADVERSE_DRUG_REACTION[2], ADVERSE_DRUG_REACTION[3], ADVERSE_DRUG_REACTION[4], ADVERSE_DRUG_REACTION[5], ADVERSE_DRUG_REACTION[6], ADVERSE_DRUG_REACTION[7]))

      for TARGET in targets:
        if(TARGET is not None):
          outfile_drug_targets.write("%s|%s|%s|%s|%s|%s|%s|%s\n" % (PRIMARY_DRUGBANK_ID, TARGET[0], TARGET[1], TARGET[2], TARGET[3], TARGET[4], TARGET[5], TARGET[6]) )

          for TARGET_ACTION in TARGET[7]:
            outfile_drug_target_actions.write("%s|%s|%s\n" % (PRIMARY_DRUGBANK_ID, TARGET[1], TARGET_ACTION) )

          for TARGET_REFERENCE in TARGET[8]:
            if(TARGET_REFERENCE != "" and TARGET_REFERENCE is not None):
              outfile_drug_target_references.write("%s|%s|%s\n" % (PRIMARY_DRUGBANK_ID, TARGET[1], TARGET_REFERENCE.lstrip().rstrip()) )

          for TARGET_POLYPEPTIDE in TARGET[9]:
            if(TARGET_POLYPEPTIDE != "" and TARGET_POLYPEPTIDE is not None):
              outfile_drug_target_polypeptides.write("%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s\n" % (TARGET_POLYPEPTIDE[0], TARGET_POLYPEPTIDE[1], TARGET_POLYPEPTIDE[2], TARGET_POLYPEPTIDE[3], TARGET_POLYPEPTIDE[4], TARGET[1], PRIMARY_DRUGBANK_ID, TARGET_POLYPEPTIDE[5], TARGET_POLYPEPTIDE[6], TARGET_POLYPEPTIDE[7], TARGET_POLYPEPTIDE[8], TARGET_POLYPEPTIDE[9], TARGET_POLYPEPTIDE[10], TARGET_POLYPEPTIDE[11], TARGET_POLYPEPTIDE[12], TARGET_POLYPEPTIDE[13], TARGET_POLYPEPTIDE[14]) )

              for TARGET_TRANSMEMBRANE_REGION in TARGET_POLYPEPTIDE[15]:
                if(TARGET_TRANSMEMBRANE_REGION != "" and TARGET_TRANSMEMBRANE_REGION is not None):
                  outfile_drug_target_polypeptide_transmembrane_regions.write("%s|%s|%s|%s|%s\n" % (TARGET_POLYPEPTIDE[0], TARGET_POLYPEPTIDE[1], TARGET[1], PRIMARY_DRUGBANK_ID, TARGET_TRANSMEMBRANE_REGION.replace('\n', '')) )

              for TARGET_EXT_IDENTIFIER in TARGET_POLYPEPTIDE[16]:
                if(TARGET_EXT_IDENTIFIER != "" and TARGET_EXT_IDENTIFIER is not None):
                  outfile_drug_target_polypeptide_external_identifiers.write("%s|%s|%s|%s|%s|%s\n" % (TARGET_EXT_IDENTIFIER[0], TARGET_EXT_IDENTIFIER[1], TARGET_POLYPEPTIDE[0], TARGET_POLYPEPTIDE[1], TARGET[1], PRIMARY_DRUGBANK_ID) )

              for TARGET_SYNONYM in TARGET_POLYPEPTIDE[17]:
                if(TARGET_SYNONYM != "" and TARGET_SYNONYM is not None):
                  outfile_drug_target_polypeptide_synonyms.write("%s|%s|%s|%s|%s\n" % (TARGET_SYNONYM, TARGET_POLYPEPTIDE[0], TARGET_POLYPEPTIDE[1], TARGET[1], PRIMARY_DRUGBANK_ID) )

              outfile_drug_target_polypeptide_amino_acid_sequences.write("%s|%s|%s|%s|%s|%s\n" % (TARGET_POLYPEPTIDE[18], TARGET_POLYPEPTIDE[19], TARGET_POLYPEPTIDE[0], TARGET_POLYPEPTIDE[1], TARGET[1], PRIMARY_DRUGBANK_ID) )

              outfile_drug_target_polypeptide_gene_sequences.write("%s|%s|%s|%s|%s|%s\n" % (TARGET_POLYPEPTIDE[20], TARGET_POLYPEPTIDE[21], TARGET_POLYPEPTIDE[0], TARGET_POLYPEPTIDE[1], TARGET[1], PRIMARY_DRUGBANK_ID) )

              for TARGET_PFAM in TARGET_POLYPEPTIDE[22]:
                if(TARGET_PFAM!= "" and TARGET_PFAM is not None):
                  outfile_drug_target_polypeptide_pfams.write("%s|%s|%s|%s|%s|%s\n" % (TARGET_PFAM[0], TARGET_PFAM[1], TARGET_POLYPEPTIDE[0], TARGET_POLYPEPTIDE[1], TARGET[1], PRIMARY_DRUGBANK_ID) )

              for TARGET_GO_CLASSIFIER in TARGET_POLYPEPTIDE[23]:
                if(TARGET_GO_CLASSIFIER != "" and TARGET_GO_CLASSIFIER is not None):
                  outfile_drug_target_polypeptide_go_classifiers.write("%s|%s|%s|%s|%s|%s\n" % (TARGET_GO_CLASSIFIER[0], TARGET_GO_CLASSIFIER[1], TARGET_POLYPEPTIDE[0], TARGET_POLYPEPTIDE[1], TARGET[1], PRIMARY_DRUGBANK_ID) )

      for CARRIER in carriers:
        if(CARRIER is not None):
          outfile_drug_carriers.write("%s|%s|%s|%s|%s|%s|%s|%s\n" % (PRIMARY_DRUGBANK_ID, CARRIER[0], CARRIER[1], CARRIER[2], CARRIER[3], CARRIER[4], CARRIER[5], CARRIER[6]) )

          for CARRIER_ACTION in CARRIER[7]:
            outfile_drug_carrier_actions.write("%s|%s|%s\n" % (PRIMARY_DRUGBANK_ID, CARRIER[1], CARRIER_ACTION) )

          for CARRIER_REFERENCE in CARRIER[8]:
            if(CARRIER_REFERENCE != "" and CARRIER_REFERENCE is not None):
              outfile_drug_carrier_references.write("%s|%s|%s\n" % (PRIMARY_DRUGBANK_ID, CARRIER[1], CARRIER_REFERENCE.lstrip().rstrip()) )

          for CARRIER_POLYPEPTIDE in CARRIER[9]:
            if(CARRIER_POLYPEPTIDE != "" and CARRIER_POLYPEPTIDE is not None):
              outfile_drug_carrier_polypeptides.write("%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s\n" % (CARRIER_POLYPEPTIDE[0], CARRIER_POLYPEPTIDE[1], CARRIER_POLYPEPTIDE[2], CARRIER_POLYPEPTIDE[3], CARRIER_POLYPEPTIDE[4], CARRIER[1], PRIMARY_DRUGBANK_ID, CARRIER_POLYPEPTIDE[5], CARRIER_POLYPEPTIDE[6], CARRIER_POLYPEPTIDE[7], CARRIER_POLYPEPTIDE[8], CARRIER_POLYPEPTIDE[9], CARRIER_POLYPEPTIDE[10], CARRIER_POLYPEPTIDE[11], CARRIER_POLYPEPTIDE[12], CARRIER_POLYPEPTIDE[13], CARRIER_POLYPEPTIDE[14]) )

              for CARRIER_TRANSMEMBRANE_REGION in CARRIER_POLYPEPTIDE[15]:
                if(CARRIER_TRANSMEMBRANE_REGION != "" and CARRIER_TRANSMEMBRANE_REGION is not None):
                  outfile_drug_carrier_polypeptide_transmembrane_regions.write("%s|%s|%s|%s|%s\n" % (CARRIER_POLYPEPTIDE[0], CARRIER_POLYPEPTIDE[1], CARRIER[1], PRIMARY_DRUGBANK_ID, CARRIER_TRANSMEMBRANE_REGION.replace('\n', '')) )

              for CARRIER_EXT_IDENTIFIER in CARRIER_POLYPEPTIDE[16]:
                if(CARRIER_EXT_IDENTIFIER != "" and CARRIER_EXT_IDENTIFIER is not None):
                  outfile_drug_carrier_polypeptide_external_identifiers.write("%s|%s|%s|%s|%s|%s\n" % (CARRIER_EXT_IDENTIFIER[0], CARRIER_EXT_IDENTIFIER[1], CARRIER_POLYPEPTIDE[0], CARRIER_POLYPEPTIDE[1], CARRIER[1], PRIMARY_DRUGBANK_ID) )

              for CARRIER_SYNONYM in CARRIER_POLYPEPTIDE[17]:
                if(CARRIER_SYNONYM != "" and CARRIER_SYNONYM is not None):
                  outfile_drug_carrier_polypeptide_synonyms.write("%s|%s|%s|%s|%s\n" % (CARRIER_SYNONYM, CARRIER_POLYPEPTIDE[0], CARRIER_POLYPEPTIDE[1], CARRIER[1], PRIMARY_DRUGBANK_ID) )

              outfile_drug_carrier_polypeptide_amino_acid_sequences.write("%s|%s|%s|%s|%s|%s\n" % (CARRIER_POLYPEPTIDE[18], CARRIER_POLYPEPTIDE[19], CARRIER_POLYPEPTIDE[0], CARRIER_POLYPEPTIDE[1], CARRIER[1], PRIMARY_DRUGBANK_ID) )

              outfile_drug_carrier_polypeptide_gene_sequences.write("%s|%s|%s|%s|%s|%s\n" % (CARRIER_POLYPEPTIDE[20], CARRIER_POLYPEPTIDE[21], CARRIER_POLYPEPTIDE[0], CARRIER_POLYPEPTIDE[1], CARRIER[1], PRIMARY_DRUGBANK_ID) )

              for CARRIER_PFAM in CARRIER_POLYPEPTIDE[22]:
                if(CARRIER_PFAM!= "" and CARRIER_PFAM is not None):
                  outfile_drug_carrier_polypeptide_pfams.write("%s|%s|%s|%s|%s|%s\n" % (CARRIER_PFAM[0], CARRIER_PFAM[1], CARRIER_POLYPEPTIDE[0], CARRIER_POLYPEPTIDE[1], CARRIER[1], PRIMARY_DRUGBANK_ID) )

              for CARRIER_GO_CLASSIFIER in CARRIER_POLYPEPTIDE[23]:
                if(CARRIER_GO_CLASSIFIER != "" and CARRIER_GO_CLASSIFIER is not None):
                  outfile_drug_carrier_polypeptide_go_classifiers.write("%s|%s|%s|%s|%s|%s\n" % (CARRIER_GO_CLASSIFIER[0], CARRIER_GO_CLASSIFIER[1], CARRIER_POLYPEPTIDE[0], CARRIER_POLYPEPTIDE[1], CARRIER[1], PRIMARY_DRUGBANK_ID) )

      for ENZYME in enzymes:
        if(ENZYME is not None):
          outfile_drug_enzymes.write("%s|%s|%s|%s|%s|%s|%s|%s\n" % (PRIMARY_DRUGBANK_ID, ENZYME[0], ENZYME[1], ENZYME[2], ENZYME[3], ENZYME[4], ENZYME[5], ENZYME[6]) )

          for ENZYME_ACTION in ENZYME[7]:
            outfile_drug_enzyme_actions.write("%s|%s|%s\n" % (PRIMARY_DRUGBANK_ID, ENZYME[1], ENZYME_ACTION) )

          for ENZYME_REFERENCE in ENZYME[8]:
            if(ENZYME_REFERENCE != "" and ENZYME_REFERENCE is not None):
              outfile_drug_enzyme_references.write("%s|%s|%s\n" % (PRIMARY_DRUGBANK_ID, ENZYME[1], ENZYME_REFERENCE.lstrip().rstrip()) )

          for ENZYME_POLYPEPTIDE in ENZYME[9]:
            if(ENZYME_POLYPEPTIDE != "" and ENZYME_POLYPEPTIDE is not None):
              outfile_drug_enzyme_polypeptides.write("%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s\n" % (ENZYME_POLYPEPTIDE[0], ENZYME_POLYPEPTIDE[1], ENZYME_POLYPEPTIDE[2], ENZYME_POLYPEPTIDE[3], ENZYME_POLYPEPTIDE[4], ENZYME[1], PRIMARY_DRUGBANK_ID, ENZYME_POLYPEPTIDE[5], ENZYME_POLYPEPTIDE[6], ENZYME_POLYPEPTIDE[7], ENZYME_POLYPEPTIDE[8], ENZYME_POLYPEPTIDE[9], ENZYME_POLYPEPTIDE[10], ENZYME_POLYPEPTIDE[11], ENZYME_POLYPEPTIDE[12], ENZYME_POLYPEPTIDE[13], ENZYME_POLYPEPTIDE[14]) )

              for ENZYME_TRANSMEMBRANE_REGION in ENZYME_POLYPEPTIDE[15]:
                if(ENZYME_TRANSMEMBRANE_REGION != "" and ENZYME_TRANSMEMBRANE_REGION is not None):
                  outfile_drug_enzyme_polypeptide_transmembrane_regions.write("%s|%s|%s|%s|%s\n" % (ENZYME_POLYPEPTIDE[0], ENZYME_POLYPEPTIDE[1], ENZYME[1], PRIMARY_DRUGBANK_ID, ENZYME_TRANSMEMBRANE_REGION.replace('\n', '')) )

              for ENZYME_EXT_IDENTIFIER in ENZYME_POLYPEPTIDE[16]:
                if(ENZYME_EXT_IDENTIFIER != "" and ENZYME_EXT_IDENTIFIER is not None):
                  outfile_drug_enzyme_polypeptide_external_identifiers.write("%s|%s|%s|%s|%s|%s\n" % (ENZYME_EXT_IDENTIFIER[0], ENZYME_EXT_IDENTIFIER[1], ENZYME_POLYPEPTIDE[0], ENZYME_POLYPEPTIDE[1], ENZYME[1], PRIMARY_DRUGBANK_ID) )

              for ENZYME_SYNONYM in ENZYME_POLYPEPTIDE[17]:
                if(ENZYME_SYNONYM != "" and ENZYME_SYNONYM is not None):
                  outfile_drug_enzyme_polypeptide_synonyms.write("%s|%s|%s|%s|%s\n" % (ENZYME_SYNONYM, ENZYME_POLYPEPTIDE[0], ENZYME_POLYPEPTIDE[1], ENZYME[1], PRIMARY_DRUGBANK_ID) )

              outfile_drug_enzyme_polypeptide_amino_acid_sequences.write("%s|%s|%s|%s|%s|%s\n" % (ENZYME_POLYPEPTIDE[18], ENZYME_POLYPEPTIDE[19], ENZYME_POLYPEPTIDE[0], ENZYME_POLYPEPTIDE[1], ENZYME[1], PRIMARY_DRUGBANK_ID) )

              outfile_drug_enzyme_polypeptide_gene_sequences.write("%s|%s|%s|%s|%s|%s\n" % (ENZYME_POLYPEPTIDE[20], ENZYME_POLYPEPTIDE[21], ENZYME_POLYPEPTIDE[0], ENZYME_POLYPEPTIDE[1], ENZYME[1], PRIMARY_DRUGBANK_ID) )

              for ENZYME_PFAM in ENZYME_POLYPEPTIDE[22]:
                if(ENZYME_PFAM!= "" and ENZYME_PFAM is not None):
                  outfile_drug_enzyme_polypeptide_pfams.write("%s|%s|%s|%s|%s|%s\n" % (ENZYME_PFAM[0], ENZYME_PFAM[1], ENZYME_POLYPEPTIDE[0], ENZYME_POLYPEPTIDE[1], ENZYME[1], PRIMARY_DRUGBANK_ID) )

              for ENZYME_GO_CLASSIFIER in ENZYME_POLYPEPTIDE[23]:
                if(ENZYME_GO_CLASSIFIER != "" and ENZYME_GO_CLASSIFIER is not None):
                  outfile_drug_enzyme_polypeptide_go_classifiers.write("%s|%s|%s|%s|%s|%s\n" % (ENZYME_GO_CLASSIFIER[0], ENZYME_GO_CLASSIFIER[1], ENZYME_POLYPEPTIDE[0], ENZYME_POLYPEPTIDE[1], ENZYME[1], PRIMARY_DRUGBANK_ID) )

      for TRANSPORTER in transporters:
        if(TRANSPORTER is not None):
          outfile_drug_transporters.write("%s|%s|%s|%s|%s|%s|%s|%s\n" % (PRIMARY_DRUGBANK_ID, TRANSPORTER[0], TRANSPORTER[1], TRANSPORTER[2], TRANSPORTER[3], TRANSPORTER[4], TRANSPORTER[5], TRANSPORTER[6]) )

          for TRANSPORTER_ACTION in TRANSPORTER[7]:
            outfile_drug_transporter_actions.write("%s|%s|%s\n" % (PRIMARY_DRUGBANK_ID, TRANSPORTER[1], TRANSPORTER_ACTION) )

          for TRANSPORTER_REFERENCE in TRANSPORTER[8]:
            if(TRANSPORTER_REFERENCE != "" and TRANSPORTER_REFERENCE is not None):
              outfile_drug_transporter_references.write("%s|%s|%s\n" % (PRIMARY_DRUGBANK_ID, TRANSPORTER[1], TRANSPORTER_REFERENCE.lstrip().rstrip()) )

          for TRANSPORTER_POLYPEPTIDE in TRANSPORTER[9]:
            if(TRANSPORTER_POLYPEPTIDE != "" and TRANSPORTER_POLYPEPTIDE is not None):
              outfile_drug_transporter_polypeptides.write("%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s\n" % (TRANSPORTER_POLYPEPTIDE[0], TRANSPORTER_POLYPEPTIDE[1], TRANSPORTER_POLYPEPTIDE[2], TRANSPORTER_POLYPEPTIDE[3], TRANSPORTER_POLYPEPTIDE[4], TRANSPORTER[1], PRIMARY_DRUGBANK_ID, TRANSPORTER_POLYPEPTIDE[5], TRANSPORTER_POLYPEPTIDE[6], TRANSPORTER_POLYPEPTIDE[7], TRANSPORTER_POLYPEPTIDE[8], TRANSPORTER_POLYPEPTIDE[9], TRANSPORTER_POLYPEPTIDE[10], TRANSPORTER_POLYPEPTIDE[11], TRANSPORTER_POLYPEPTIDE[12], TRANSPORTER_POLYPEPTIDE[13], TRANSPORTER_POLYPEPTIDE[14]) )

              for TRANSPORTER_TRANSMEMBRANE_REGION in TRANSPORTER_POLYPEPTIDE[15]:
                if(TRANSPORTER_TRANSMEMBRANE_REGION != "" and TRANSPORTER_TRANSMEMBRANE_REGION is not None):
                  outfile_drug_transporter_polypeptide_transmembrane_regions.write("%s|%s|%s|%s|%s\n" % (TRANSPORTER_POLYPEPTIDE[0], TRANSPORTER_POLYPEPTIDE[1], TRANSPORTER[1], PRIMARY_DRUGBANK_ID, TRANSPORTER_TRANSMEMBRANE_REGION.replace('\n', '')) )

              for TRANSPORTER_EXT_IDENTIFIER in TRANSPORTER_POLYPEPTIDE[16]:
                if(TRANSPORTER_EXT_IDENTIFIER != "" and TRANSPORTER_EXT_IDENTIFIER is not None):
                  outfile_drug_transporter_polypeptide_external_identifiers.write("%s|%s|%s|%s|%s|%s\n" % (TRANSPORTER_EXT_IDENTIFIER[0], TRANSPORTER_EXT_IDENTIFIER[1], TRANSPORTER_POLYPEPTIDE[0], TRANSPORTER_POLYPEPTIDE[1], TRANSPORTER[1], PRIMARY_DRUGBANK_ID) )

              for TRANSPORTER_SYNONYM in TRANSPORTER_POLYPEPTIDE[17]:
                if(TRANSPORTER_SYNONYM != "" and TRANSPORTER_SYNONYM is not None):
                  outfile_drug_transporter_polypeptide_synonyms.write("%s|%s|%s|%s|%s\n" % (TRANSPORTER_SYNONYM, TRANSPORTER_POLYPEPTIDE[0], TRANSPORTER_POLYPEPTIDE[1], TRANSPORTER[1], PRIMARY_DRUGBANK_ID) )

              outfile_drug_transporter_polypeptide_amino_acid_sequences.write("%s|%s|%s|%s|%s|%s\n" % (TRANSPORTER_POLYPEPTIDE[18], TRANSPORTER_POLYPEPTIDE[19], TRANSPORTER_POLYPEPTIDE[0], TRANSPORTER_POLYPEPTIDE[1], TRANSPORTER[1], PRIMARY_DRUGBANK_ID) )

              outfile_drug_transporter_polypeptide_gene_sequences.write("%s|%s|%s|%s|%s|%s\n" % (TRANSPORTER_POLYPEPTIDE[20], TRANSPORTER_POLYPEPTIDE[21], TRANSPORTER_POLYPEPTIDE[0], TRANSPORTER_POLYPEPTIDE[1], TRANSPORTER[1], PRIMARY_DRUGBANK_ID) )

              for TRANSPORTER_PFAM in TRANSPORTER_POLYPEPTIDE[22]:
                if(TRANSPORTER_PFAM!= "" and TRANSPORTER_PFAM is not None):
                  outfile_drug_transporter_polypeptide_pfams.write("%s|%s|%s|%s|%s|%s\n" % (TRANSPORTER_PFAM[0], TRANSPORTER_PFAM[1], TRANSPORTER_POLYPEPTIDE[0], TRANSPORTER_POLYPEPTIDE[1], TRANSPORTER[1], PRIMARY_DRUGBANK_ID) )

              for TRANSPORTER_GO_CLASSIFIER in TRANSPORTER_POLYPEPTIDE[23]:
                if(TRANSPORTER_GO_CLASSIFIER != "" and TRANSPORTER_GO_CLASSIFIER is not None):
                  outfile_drug_transporter_polypeptide_go_classifiers.write("%s|%s|%s|%s|%s|%s\n" % (TRANSPORTER_GO_CLASSIFIER[0], TRANSPORTER_GO_CLASSIFIER[1], TRANSPORTER_POLYPEPTIDE[0], TRANSPORTER_POLYPEPTIDE[1], TRANSPORTER[1], PRIMARY_DRUGBANK_ID) )



outfile_drugs.close()
outfile_drug_alt_ids.close()
outfile_drug_groups.close()
outfile_drug_general_references.close()
outfile_drug_volumes_of_distribution.close()
outfile_drug_clearances.close()
outfile_drug_classifications.close()
outfile_drug_classification_alt_parents.close()
outfile_drug_classification_substituents.close()
outfile_drug_salts.close()
outfile_drug_synonyms.close()
outfile_drug_products.close()
outfile_drug_international_brands.close()
outfile_drug_mixtures.close()
outfile_drug_packagers.close()
outfile_drug_manufacturers.close()
outfile_drug_prices.close()
outfile_drug_costs.close()
outfile_drug_categories.close()
outfile_drug_mesh_ids.close()
outfile_drug_affected_organisms.close()
outfile_drug_dosages.close()
outfile_drug_atc_codes.close()
outfile_drug_atc_code_levels.close()
outfile_drug_ahfs_codes.close()
outfile_drug_patents.close()
outfile_drug_food_interactions.close()
outfile_drug_drug_interactions.close()
outfile_drug_sequences.close()
outfile_drug_properties.close()
outfile_drug_external_identifiers.close()
outfile_drug_external_links.close()
outfile_drug_pathways.close()
outfile_drug_reactions.close()
outfile_drug_reaction_elements.close()
outfile_drug_reaction_enzymes.close()
outfile_drug_snp_effects.close()
outfile_drug_snp_adverse_drug_reactions.close()

outfile_drug_enzymes.close()
outfile_drug_enzyme_actions.close()
outfile_drug_enzyme_references.close()
outfile_drug_enzyme_polypeptides.close()
outfile_drug_enzyme_polypeptide_transmembrane_regions.close()
outfile_drug_enzyme_polypeptide_external_identifiers.close()
outfile_drug_enzyme_polypeptide_synonyms.close()
outfile_drug_enzyme_polypeptide_amino_acid_sequences.close()
outfile_drug_enzyme_polypeptide_gene_sequences.close()
outfile_drug_enzyme_polypeptide_pfams.close()
outfile_drug_enzyme_polypeptide_go_classifiers.close()

outfile_drug_transporters.close()
outfile_drug_transporter_actions.close()
outfile_drug_transporter_references.close()
outfile_drug_transporter_polypeptides.close()
outfile_drug_transporter_polypeptide_transmembrane_regions.close()
outfile_drug_transporter_polypeptide_external_identifiers.close()
outfile_drug_transporter_polypeptide_synonyms.close()
outfile_drug_transporter_polypeptide_amino_acid_sequences.close()
outfile_drug_transporter_polypeptide_gene_sequences.close()
outfile_drug_transporter_polypeptide_pfams.close()
outfile_drug_transporter_polypeptide_go_classifiers.close()

outfile_drug_carriers.close()
outfile_drug_carrier_actions.close()
outfile_drug_carrier_references.close()
outfile_drug_carrier_polypeptides.close()
outfile_drug_carrier_polypeptide_transmembrane_regions.close()
outfile_drug_carrier_polypeptide_external_identifiers.close()
outfile_drug_carrier_polypeptide_synonyms.close()
outfile_drug_carrier_polypeptide_amino_acid_sequences.close()
outfile_drug_carrier_polypeptide_gene_sequences.close()
outfile_drug_carrier_polypeptide_pfams.close()
outfile_drug_carrier_polypeptide_go_classifiers.close()

outfile_drug_targets.close()
outfile_drug_target_actions.close()
outfile_drug_target_references.close()
outfile_drug_target_polypeptides.close()
outfile_drug_target_polypeptide_transmembrane_regions.close()
outfile_drug_target_polypeptide_external_identifiers.close()
outfile_drug_target_polypeptide_synonyms.close()
outfile_drug_target_polypeptide_amino_acid_sequences.close()
outfile_drug_target_polypeptide_gene_sequences.close()
outfile_drug_target_polypeptide_pfams.close()
outfile_drug_target_polypeptide_go_classifiers.close()




sys.exit(0)