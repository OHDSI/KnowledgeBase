#
# The purpose of this file is to convert XML data from DrugBank
# into SQL which can easily be uploaded to relational database.
#
#

import os
import sys
import xml.etree.ElementTree as ET

source_xml_file = 'drugbank.xml'

sample_outfile = open('sample_outfile.txt', 'w', encoding='utf-8')


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
    NDICATION = 'NULL'
    PHARMACODYNAMICS = 'NULL'
    PROTEIN_BINDING = 'NULL'
    drugbank_ids = []

    if(i.tag == '{http://www.drugbank.ca}drug'):

#
#	GETTING DRUGBANK DRUG TYPES
#
      if(i.attrib == 'type'):
        DRUG_TYPE = '"' + i.attrib['type'].rstrip() + '"'

#
#	GETTING DRUGBANK DRUG CREATED AT
#
      if(i.attrib == 'created'):
        CREATED = '"' + i.attrib['created'].rstrip() + '"'

#
#	GETTING DRUGBANK DRUG UPDATED AT
#
      if(i.attrib == 'updated'):
        UPDATED = '"' + i.attrib['updated'].rstrip() + '"'
      

      for j in i.getchildren():

#
#	GETTING DRUGBANK IDS
#
        if(j.tag == '{http://www.drugbank.ca}drugbank-id'):
          if 'primary' in j.attrib:
            if(j.attrib['primary'] == 'true'):
              PRIMARY_DRUGBANK_ID = '"' + j.text.rstrip() + '"'
          else:
            drugbank_ids.append('"' + j.text.rstrip() + '"')

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
                  INTERNATIONAL_BRAND_NAME = '"' + m.text.rstrip() + '"'
                if(m.tag == '{http://www.drugbank.ca}company'  and m.text is not None):
                  INTERNATIONAL_BRAND_COMPANY = '"' + m.text.rstrip() + '"'
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
                  MIXTURE_NAME = '"' + m.text.rstrip() + '"'
                if(m.tag == '{http://www.drugbank.ca}ingredients' and m.text is not None):
                  MIXTURE_INGREDIENTS = '"' + m.text.rstrip() + '"'
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
                if(m.tag == '{http://www.drugbank.ca}packager' and m.text is not None):
                  PACKAGER_NAME = '"' + m.text.rstrip() + '"'
                if(m.tag == '{http://www.drugbank.ca}url' and m.text is not None):
                  PACKAGER_URL = '"' + m.text.rstrip() + '"'
                packagers[PACKAGER_NAME] = PACKAGER_URL

#
#	GETTING DRUGBANK MANUFACTURERS
#
        if(j.tag == '{http://www.drugbank.ca}manufacturers'):
          manufacturers = {}
          for k in j.getchildren():
            MANUFACTURER_NAME = "NULL"
            MANUFACTURER_GENERIC = "NULL"
            if(k.tag == '{http://www.drugbank.ca}manufacturer'):
              MANUFACTURER_NAME = '"' + k.text.rstrip() + '"'
              if(k.attrib == 'generic'):
                MANUFACTURER_GENERIC = k.attrib['generic'].rstrip().upper()
            manufacturers[PACKAGER_NAME] = MANUFACTURER_GENERIC

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
                  PRICE_DESCRIPTION = '"' + m.text.rstrip() + '"'
                if(m.tag == '{http://www.drugbank.ca}cost' and m.text is not None):
                  PRICE_COST = m.text.rstrip()
                  PRICE_CURRENCY = '"' + m.attrib['currency'].rstrip() + '"'
                  costs[PRICE_CURRENCY] = PRICE_COST
                if(m.tag == '{http://www.drugbank.ca}unit' and m.text is not None):
                  PRICE_UNIT = '"' + m.text.rstrip() + '"'
              prices[PRICE_DESCRIPTION] = [costs, PRICE_UNIT]

#
#	GETTING DRUGBANK FOOD INTERACTIONS
#
        if(j.tag == '{http://www.drugbank.ca}food-interactions'):
          drug_food_interactions = []
          for k in j.getchildren():
            if(k.tag == '{http://www.drugbank.ca}food-interaction'):
              FOOD_INTERACTION = '"' + k.text.rstrip() + '"'
              drug_food_interactions.append(FOOD_INTERACTION)

#
#	GETTING DRUGBANK NAMES
#
        if(j.tag == '{http://www.drugbank.ca}name'):
          NAME = '"' + j.text.rstrip() + '"'

#
#	GETTING DRUGBANK DESCRIPTIONS
#
        if(j.tag == '{http://www.drugbank.ca}description' and j.text is not None):
          DESCRIPTION = '"' + j.text.rstrip() + '"'
          
#
#	GETTING DRUGBANK CAS NUMBERS
#
        if(j.tag == '{http://www.drugbank.ca}cas-number' and j.text is not None):
          CAS_NUMBER = '"' + j.text.rstrip() + '"'

#
#	GETTING DRUGBANK GROUPS
#
        if(j.tag == '{http://www.drugbank.ca}groups'):
          drug_groups = []
          for k in j.getchildren():
            if(k.tag == '{http://www.drugbank.ca}group'):
              DRUG_GROUP = '"' + k.text.rstrip() + '"'
              drug_groups.append(DRUG_GROUP)

#
#	GETTING DRUGBANK GENERAL REFERENCSE
#
        if(j.tag == '{http://www.drugbank.ca}general-references' and j.text is not None):
          temp_drug_references = j.text.rstrip()
          drug_general_references = temp_drug_references.split('#')

#
#	GETTING DRUGBANK SYNTHESIS REFERENCES
#
        if(j.tag == '{http://www.drugbank.ca}synthesis-reference' and j.text is not None):
          SYNTHESIS_REFERENCE = '"' + j.text.rstrip() + '"'

#
#	GETTING DRUGBANK INDICATIONS
#
        if(j.tag == '{http://www.drugbank.ca}indication' and j.text is not None):
          INDICATION = '"' + j.text.rstrip() + '"'

#
#	GETTING DRUGBANK PHARMACODYNAMICS
#
        if(j.tag == '{http://www.drugbank.ca}pharmacodynamics' and j.text is not None):
          PHARMACODYNAMICS = '"' + j.text.rstrip() + '"'

#
#	GETTING DRUGBANK MECHANISMS OF ACTION
#
        if(j.tag == '{http://www.drugbank.ca}mechanism-of-action' and j.text is not None):
          MECHANISM_OF_ACTION = '"' + j.text.rstrip() + '"'

#
#	GETTING DRUGBANK TOXICITY
#
        if(j.tag == '{http://www.drugbank.ca}toxicity' and j.text is not None):
          TOXICITY = '"' + j.text.rstrip() + '"'

#
#	GETTING DRUGBANK METABOLISMS
#
        if(j.tag == '{http://www.drugbank.ca}metabolism' and j.text is not None):
          METABOLISM = '"' + j.text.rstrip() + '"'

#
#	GETTING DRUGBANK ABSORPTIONS
#
        if(j.tag == '{http://www.drugbank.ca}absorption' and j.text is not None):
          ABSORPTION = '"' + j.text.rstrip() + '"'

#
#	GETTING DRUGBANK HALF LIVES
#
        if(j.tag == '{http://www.drugbank.ca}half-life' and j.text is not None):
          HALF_LIFE = '"' + j.text.rstrip() + '"'

#
#	GETTING DRUGBANK PROTEIN BINDINGS
#
        if(j.tag == '{http://www.drugbank.ca}protein-binding' and j.text is not None):
          PROTEIN_BINDING = '"' + j.text.rstrip() + '"'

#
#	GETTING DRUGBANK ROUTES OF ELIMINATION
#
        if(j.tag == '{http://www.drugbank.ca}route-of-elimination' and j.text is not None):
          ROUTE_OF_ELIMINATION = '"' + j.text.rstrip() + '"'

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
              CLASSIFICATION_DESCRIPTION = '"' + k.text.rstrip() + '"'
            if(k.tag == '{http://www.drugbank.ca}direct-parent' and k.text is not None):
              CLASSIFICATION_DIRECT_PARENT = '"' + k.text.rstrip() + '"'
            if(k.tag == '{http://www.drugbank.ca}kingdom' and k.text is not None):
              CLASSIFICATION_KINGDOM = '"' + k.text.rstrip() + '"'
            if(k.tag == '{http://www.drugbank.ca}superclass' and k.text is not None):
              CLASSIFICATION_SUPERCLASS = '"' + k.text.rstrip() + '"'
            if(k.tag == '{http://www.drugbank.ca}drug-class' and k.text is not None):
              CLASSIFICATION_DRUG_CLASS = '"' + k.text.rstrip() + '"'
            if(k.tag == '{http://www.drugbank.ca}subclass' and k.text is not None):
              CLASSIFICATION_SUBCLASS = '"' + k.text.rstrip() + '"'
            if(k.tag == '{http://www.drugbank.ca}alternative-parent' and k.text is not None):
              alternative_parents.append('"' + k.text.rstrip() + '"')
            if(k.tag == '{http://www.drugbank.ca}substituent' and k.text is not None):
              substituents.append('"' + k.text.rstrip() + '"')
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
                  PRIMARY_DRUGBANK_ID_SALT = '"' + m.text.rstrip() + '"'
                if(m.tag == '{http://www.drugbank.ca}name' and m.text is not None):
                  SALT_NAME = '"' + m.text.rstrip() + '"'
                if(m.tag == '{http://www.drugbank.ca}cas-number' and m.text is not None):
                  SALT_CAS_NUMBER = '"' + m.text.rstrip() + '"'
                if(m.tag == '{http://www.drugbank.ca}inchikey' and m.text is not None):
                  SALT_INCHIKEY = '"' + m.text.rstrip() + '"'
              salts[PRIMARY_DRUGBANK_ID_SALT] = [SALT_NAME, SALT_CAS_NUMBER, SALT_INCHIKEY]

#
#	GETTING DRUGBANK SYNONYMS
#
        if(j.tag == '{http://www.drugbank.ca}synonyms'):
          synonyms = {}
          for k in j.getchildren():
            if(k.tag == '{http://www.drugbank.ca}synonym'):
              SYNONYM = "NULL"
              SYNONYM_LANGUAGE = "NULL"
              SYNONYM_CODER = "NULL"
              if(k.tag == '{http://www.drugbank.ca}synonym' and k.text is not None):
                SYNONYM = '"' + k.text.rstrip() + '"'
                if(k.attrib == 'language'):
                  SYNONYM_LANGUAGE = '"' + k.attrib['language'].rstrip() + '"'
                if(k.attrib == 'coder'):
                  SYNONYM_CODER = '"' + k.attrib['coder'].rstrip() + '"'
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
                  PRODUCT_NAME = '"' + m.text.rstrip() + '"'
                if(m.tag == '{http://www.drugbank.ca}ndc-id' and m.text is not None):
                  PRODUCT_NDC_ID = '"' + m.text.rstrip() + '"'
                if(m.tag == '{http://www.drugbank.ca}ndc-product-code' and m.text is not None):
                  PRODUCT_NDC_PRODUCT_CODE = '"' + m.text.rstrip() + '"'
                if(m.tag == '{http://www.drugbank.ca}dpd-id' and m.text is not None):
                  PRODUCT_DPD_ID = '"' + m.text.rstrip() + '"'
                if(m.tag == '{http://www.drugbank.ca}started-marketing-on' and m.text is not None):
                  PRODUCT_STARTED_MARKETING_ON = '"' + m.text.rstrip() + '"'
                if(m.tag == '{http://www.drugbank.ca}ended-marketing-on' and m.text is not None):
                  PRODUCT_ENDED_MARKETING_ON = '"' + m.text.rstrip() + '"'
                if(m.tag == '{http://www.drugbank.ca}dosage-form' and m.text is not None):
                  PRODUCT_DOSAGE_FORM = '"' + m.text.rstrip() + '"'
                if(m.tag == '{http://www.drugbank.ca}strength' and m.text is not None):
                  PRODUCT_STRENGTH = '"' + m.text.rstrip() + '"'
                if(m.tag == '{http://www.drugbank.ca}route' and m.text is not None):
                  PRODUCT_ROUTE = '"' + m.text.rstrip() + '"'
                if(m.tag == '{http://www.drugbank.ca}fda-application-number' and m.text is not None):
                  PRODUCT_FDA_APPLICATION_NUMBER = '"' + m.text.rstrip() + '"'
                if(m.tag == '{http://www.drugbank.ca}generic' and m.text is not None):
                  PRODUCT_GENERIC = m.text.rstrip().upper()
                if(m.tag == '{http://www.drugbank.ca}over-the-counter' and m.text is not None):
                  PRODUCT_OVER_THE_COUNTER = m.text.rstrip().upper()
                if(m.tag == '{http://www.drugbank.ca}approved' and m.text is not None):
                  PRODUCT_APPROVED = m.text.rstrip().upper()
                if(m.tag == '{http://www.drugbank.ca}country' and m.text is not None):
                  PRODUCT_COUNTRY = '"' + m.text.rstrip() + '"'
                if(m.tag == '{http://www.drugbank.ca}source' and m.text is not None):
                  PRODUCT_SOURCE = '"' + m.text.rstrip() + '"'
                products[PRODUCT_NAME] = [PRODUCT_NDC_ID, PRODUCT_NDC_PRODUCT_CODE, PRODUCT_DPD_ID, PRODUCT_STARTED_MARKETING_ON, PRODUCT_ENDED_MARKETING_ON, PRODUCT_DOSAGE_FORM, PRODUCT_STRENGTH, PRODUCT_ROUTE, PRODUCT_FDA_APPLICATION_NUMBER, PRODUCT_GENERIC, PRODUCT_OVER_THE_COUNTER, PRODUCT_APPROVED, PRODUCT_COUNTRY, PRODUCT_SOURCE]
              

      sample_outfile.write("INSERT INTO Drug VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);\n" % (PRIMARY_DRUGBANK_ID, NAME, DESCRIPTION, CAS_NUMBER, SYNTHESIS_REFERENCE, INDICATION, PHARMACODYNAMICS, MECHANISM_OF_ACTION, TOXICITY, METABOLISM, ABSORPTION, HALF_LIFE, PROTEIN_BINDING, ROUTE_OF_ELIMINATION, DRUG_TYPE, CREATED, UPDATED))
      for DRUG_ALT_ID in drugbank_ids: 
        sample_outfile.write("INSERT INTO DrugAltID VALUES (%s, %s);\n" % (DRUG_ALT_ID, PRIMARY_DRUGBANK_ID))
      for key, value in international_brands.items():
        if(key != "NULL" and value != "NULL"):
          sample_outfile.write("INSERT INTO DrugInternationalBrand VALUES (%s, %s, %s);\n" % (PRIMARY_DRUGBANK_ID, key, value))
      for FOOD_INTERACTION in drug_food_interactions:
        if(FOOD_INTERACTION is not None):
          sample_outfile.write("INSERT INTO DrugFoodInteraction VALUES (%s, %s);\n" % (FOOD_INTERACTION, PRIMARY_DRUGBANK_ID))
      for DRUG_GROUP in drug_groups:
        if(DRUG_GROUP is not None):
          sample_outfile.write("INSERT INTO DrugGroup VALUES (%s, %s);\n" % (DRUG_GROUP, PRIMARY_DRUGBANK_ID))
      for GENERAL_REFERENCE in drug_general_references:
        if(GENERAL_REFERENCE is not None and GENERAL_REFERENCE != ""):
          sample_outfile.write("INSERT INTO DrugGeneralReference VALUES (%s, %s);\n" % ('"' + GENERAL_REFERENCE.lstrip().rstrip() + '"', PRIMARY_DRUGBANK_ID))
      for VOLUME_OF_DISTRIBUTION in volumes_of_distribution:
        if(VOLUME_OF_DISTRIBUTION is not None and VOLUME_OF_DISTRIBUTION != ""):
          sample_outfile.write("INSERT INTO DrugVolumeOfDistribution VALUES (%s, %s);\n" % ('"' + VOLUME_OF_DISTRIBUTION.lstrip().rstrip() + '"', PRIMARY_DRUGBANK_ID))
      for CLEARANCE in clearances:
        if(CLEARANCE is not None and CLEARANCE != ""):
          sample_outfile.write("INSERT INTO DrugClearance VALUES (%s, %s);\n" % ('"' + CLEARANCE.lstrip().rstrip() + '"', PRIMARY_DRUGBANK_ID))
      for CLASSIFICATION in classification:
        if CLASSIFICATION:
          sample_outfile.write("INSERT INTO DrugClassification VALUES (%s, %s, %s, %s, %s, %s, %s);\n" % (PRIMARY_DRUGBANK_ID, CLASSIFICATION[0], CLASSIFICATION[1], CLASSIFICATION[2], CLASSIFICATION[3], CLASSIFICATION[4], CLASSIFICATION[5]))
      for ALTERNATIVE_PARENT in alternative_parents:
        if(ALTERNATIVE_PARENT is not None):
          sample_outfile.write("INSERT INTO DrugClassificationAltParent VALUES (%s, %s);\n" % (PRIMARY_DRUGBANK_ID, ALTERNATIVE_PARENT))
      for SUBSTITUENT in substituents:
        if(SUBSTITUENT is not None):
          sample_outfile.write("INSERT INTO DrugClassificationSubstituent VALUES (%s, %s);\n" % (PRIMARY_DRUGBANK_ID, SUBSTITUENT))
      for key, value in salts.items():
        if(key != "NULL" and value != "NULL"):
          sample_outfile.write("INSERT INTO DrugSalts VALUES (%s, %s, %s, %s, %s);\n" % (key, PRIMARY_DRUGBANK_ID, value[0], value[1], value[2]))
      for key, value in synonyms.items():
        if(key != "NULL" and value != "NULL"):
          sample_outfile.write("INSERT INTO DrugSynonym VALUES (%s, %s, %s, %s);\n" % (key, value[0], value[1], PRIMARY_DRUGBANK_ID))
      for key, value in products.items():
        if(key != "NULL" and value != "NULL"):
          sample_outfile.write("INSERT INTO DrugProduct VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);\n" % (key, value[0], value[1], value[2], value[3], value[4], value[5], value[6], value[7], value[8], value[9], value[10], value[11], value[12], value[13], PRIMARY_DRUGBANK_ID))
      for key, value in mixtures.items():
        if(key != "NULL" and value != "NULL"):
          sample_outfile.write("INSERT INTO DrugMixture VALUES (%s, %s, %s);\n" % (key, value, PRIMARY_DRUGBANK_ID))
      for key, value in packagers.items():
        if(key != "NULL" and value != "NULL"):
          sample_outfile.write("INSERT INTO DrugPackager VALUES (%s, %s, %s);\n" % (key, value, PRIMARY_DRUGBANK_ID))
      for key, value in manufacturers.items():
        if(key != "NULL" and value != "NULL"):
          sample_outfile.write("INSERT INTO DrugManufacturer VALUES (%s, %s, %s);\n" % (key, value, PRIMARY_DRUGBANK_ID))
      for key, value in prices.items():
        if(key != "NULL" and value != "NULL"):
          sample_outfile.write("INSERT INTO DrugPrice VALUES (%s, %s, %s);\n" % (key, value[1], PRIMARY_DRUGBANK_ID))
          for key2, value2 in value[0].items():
            if(key2 != "NULL" and value2 != "NULL"):
              sample_outfile.write("INSERT INTO DrugCost VALUES (%s, %s, %s, %s, %s);\n" % (key2, value2, key, value[1], PRIMARY_DRUGBANK_ID))
 


sample_outfile.close()

sys.exit(0)