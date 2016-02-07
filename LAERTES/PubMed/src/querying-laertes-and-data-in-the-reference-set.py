#  querying-laertes-and-data-in-the-reference-set.py
#
#  Perform a set intersection of drug data with SemMedDB/UMLS data.
#
#  Author: Charles Kronk
#  2016

#  1) Load data file.
#    a) File should be a .tsv file and should be included
#       as the first argument when this script is run in
#       the command line.
#    b) The file should be of the following format:
#         - PubMed article identifier
#         - Drug name
#         - MeSH code for the drug
#         - HOI name
#         - MeSH code for the HOI
#         - Article type
#         - MeSH code for the article type
#       i.e.
#         311	Enflurane	D004737	Jaundice	D007565	Case Reports	D002363
#
#  2) Load the MeSH Drug Groupings file.
#    a) This file is currently located at the following URL:
#         https://github.com/OHDSI/KnowledgeBase/raw/master/LAERTES/terminology-mappings/MeSHPharmocologicActionToSubstances/pa2015.xml
#    b) This file should be downloaded and included as the
#       second argument when this script is run in the command
#       line.
#    c) This file will be loaded into a dictionary which can
#       be keyed by the MeSH identifier of the drug group.
#      i) In this file the XML tag <RecordUI> is the "key" while
#         the "value" is the tag <DescriptorUI>.
#
#  3) For each row of the .tsv file (see 1), the drug will be
#     checked in order to see whether or not the drug is a
#     MeSH Drug Group (utilizing the dictionary set up in 2).
#    a) If the drug is a MeSH Drug Group then query the Title
#       and Abstract of the article referenced by the PubMed
#       identifier. This is done via SemMedDB as loaded into
#	MySQL on the development server.
#    b) A file 'db-connection-semmeddb.conf' must be the same
#       directory that this python file is run in.
#         i) This file should be setup as follows:
#              semmeddb	USERNAME	PASSWORD	localhost	3306
#    c) A query of SemMedDB is then setup in order to return
#       a list of all UMLS CUIs associated with a particular
#       PubMed ID.
#    d) These UMLS CUIs are then queried in the UMLS database.
#      i) In order to query these, a connection to the UMLS
#         database is necessary; thus, the file
#         'db-connection-umls.conf' must also be in the same
#         directory that this python file is run in.
#      ii) This file should be setup as follows:
#           umls	USERNAME	PASSWORD	localhost	3306
#      iii) Note that the port 3306 is chosen for both of these
#         setups because that is the SQL port associated with
#         the dev servers databases.
#    e) Once the CUIs are queried, the query will return a
#       list of the MeSH identifiers associated with those CUIs.
#    f) From this list a simple intersection will be performed
#       comparing the drugs in the drug group with those returned
#       MeSH identifiers.
#    g) If the comparison yields true, the result will be written
#       to the file 
#       'querying-laertes-and-data-in-the-reference-set-v2.tsv' in
#       the following format:
#         PMID  UMLS_GROUP_ID   MESH_GROUP_ID   MESH_GROUP_NAME DRUG_MENTION_UMLS   DRUG_MENTION_MESH   DRUG_MENTION_NAME
#    h) Once finished, the program will terminate with the message:
#       'Program complete.'
#

import sys
import xml.etree.ElementTree as ET
import mysql.connector as sql
import csv

if(len(sys.argv) != 3):
  print "Invalid number of command-line arguments."
  print "Please inspect usage notes for further details."
  sys.exit(2)

TSV_DATA_FILE = sys.argv[1]

MESH_DRUG_GROUPINGS_FILE = sys.argv[2]

mesh_identifier_of_drug_group_dictionary = {}
mesh_drug_group_drug_name_dictionary = {}

# PARSE MESH DRUG GROUPINGS FILE
with open(MESH_DRUG_GROUPINGS_FILE) as f:
  tree = ET.parse(f)
  root = tree.getroot()

  for elem in root.getchildren():
    descriptorUI = ''

    for subElem in elem.findall('DescriptorReferredTo'):
      for i in subElem.getchildren():
        if(i.tag == 'DescriptorUI'):
          descriptorUI = i.text
        if(i.tag == 'DescriptorName'):
          for k in i.getchildren():
            if(k.tag == 'String'):
              descriptorName = k.text
              mesh_drug_group_drug_name_dictionary[descriptorUI] = descriptorName

    for subElem in elem.findall('PharmacologicalActionSubstanceList'):
        for i in subElem.getchildren():
          if(i.tag == 'Substance'):
            for j in i.getchildren():
              if(j.tag == 'RecordUI'):
                recordUI = j.text
                mesh_identifier_of_drug_group_dictionary[recordUI] = descriptorUI
                    

flipped_dictionary = {}
for key, value in mesh_identifier_of_drug_group_dictionary.items():
  if value not in flipped_dictionary:
    flipped_dictionary[value] = [key]
  else:
    flipped_dictionary[value].append(key)

print "Dictionary loaded."

# SETUP OUTFILE
TSV_OUTFILE = "querying-laertes-and-data-in-the-reference-set-v2.tsv"
outfile = open(TSV_OUTFILE, 'w')

# SETUP COUNTER
counter = 0

# LOAD AND CHECK
with open(TSV_DATA_FILE) as f:
  reader = csv.reader(f, delimiter='\t')
  for pubmedID, drugName, drugMeSH, hoiName, hoiMeSH, articleType, articleTypeMeSH in reader:
    if(drugMeSH in mesh_identifier_of_drug_group_dictionary):
      drug_group_array = flipped_dictionary[mesh_identifier_of_drug_group_dictionary[drugMeSH]]
      print "PubMed ID: %s" % pubmedID

      # SETUP SEMMEDDB TO QUERY DRUGS IN THE GROUP
      DB_CONNECTION_INFO_SEMMEDDB="db-connection-semmeddb.conf"

      db_file_semmeddb = open(DB_CONNECTION_INFO_SEMMEDDB, 'r')
      (db,user,pword,host,port) = db_file_semmeddb.readline().strip().split("\t")
      db_file_semmeddb.close()

      try:
        conn_semmeddb = sql.connect(database = db, user = user, password = pword, host = host, port = port)
      except Exception as e:
        print "ERROR: Unable to connect to database %s (user:%s) on host %s (port: %s). Check that the data in db-connection.conf is correct and that there is not barrier related to the network connection. Error: %s" % (db, user, host, port, e)
      cur_semmeddb = conn_semmeddb.cursor()

      # QUERY SEMMEDDB, RETURN LIST OF UMLS CUIS
      query_semmeddb = ("""
        SELECT CUI, PREFERRED_NAME FROM
          PREDICATION_ARGUMENT,
          PREDICATION_AGGREGATE,
          CONCEPT_SEMTYPE,
          CONCEPT
        WHERE
          PREDICATION_ARGUMENT.PREDICATION_ID = PREDICATION_AGGREGATE.PID AND
          CONCEPT_SEMTYPE.CONCEPT_SEMTYPE_ID = PREDICATION_ARGUMENT.CONCEPT_SEMTYPE_ID AND
          CONCEPT.CONCEPT_ID = CONCEPT_SEMTYPE.CONCEPT_ID AND
          PREDICATION_AGGREGATE.PMID = %s
      """ % pubmedID)

      cur_semmeddb.execute(query_semmeddb)

      for x in cur_semmeddb:

        # SETUP UMLS TO QUERY CUIS RETRIEVED
        DB_CONNECTION_INFO_UMLS="db-connection-umls.conf"

        db_file_umls = open(DB_CONNECTION_INFO_UMLS, 'r')
        (db,user,pword,host,port) = db_file_umls.readline().strip().split("\t")
        db_file_umls.close()

        try:
          conn_umls = sql.connect(database = db, user = user, password = pword, host = host, port = port)
        except Exception as e:
          print "ERROR: Unable to connect to database %s (user:%s) on host %s (port: %s). Check that the data in db-connection.conf is correct and that there is not barrier related to the network connection. Error: %s" % (db, user, host, port, e)
        cur_umls = conn_umls.cursor()

        query_umls = ("""
          SELECT CODE, STR FROM
            MRCONSO
          WHERE
            LAT = 'ENG' AND
            SAB = 'MSH' AND
            CUI = '%s'
          """ % x[0])
        cur_umls.execute(query_umls)

        for y in cur_umls:
          print "  UMLS Group ID: %s" % x[0]
          print "  MeSH Group ID: %s" % mesh_identifier_of_drug_group_dictionary[drugMeSH]
          print "  MeSH Group Name: %s" % mesh_drug_group_drug_name_dictionary[mesh_identifier_of_drug_group_dictionary[drugMeSH]]
          print "  Drug Mention UMLS: %s" % y[1]
          print "  Drug Mention MeSH: %s" % y[0]
          print "  Drug Mention Name: %s" % x[1]
          if y[0] in drug_group_array:
            print "    Drug found in drug group."
            outfile.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (pubmedID, x[0], mesh_identifier_of_drug_group_dictionary[drugMeSH], mesh_drug_group_drug_name_dictionary[mesh_identifier_of_drug_group_dictionary[drugMeSH]], y[1], y[0], x[1]) )
            
        counter += 1
        
        if(counter == 40):
          break

outfile.close()
print "Program complete"
sys.exit(0)
