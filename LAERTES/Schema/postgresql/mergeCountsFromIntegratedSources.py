## mergeCountsFromIntegratedSources.py
##
## synthesize the evidence source count and linkout data into
## tables that can them be loaded into the Schema relational DB model
## (that extends the OHDSI Standard Vocab). 
##
## Author: Richard D Boyce, PhD
## 2014 - 2016

import sys
import psycopg2 # for postgres 

## Development
DB_CONNECTION_INFO="db-connection-development.conf"

## Release
#DB_CONNECTION_INFO="db-connection.conf"

SOURCE_LISTING_FILE="integratedSources.conf"
DRUG_HOI_DATA_FILE="drug-hoi-evidence-data.tsv"
CACHED_DRUG_HOI_RELATIONSHIP_FILE="cached_uniq_drug_hoi_relationships.csv"
DRUG_HOI_RELATIONSHIP_FILE="uniq_drug_hoi_relationships.csv"
MEDDRA_TO_SNOMED_MAPPING_FILE="../../terminology-mappings/MedDRA-to-SNOMED/LU_MEDDRAPT_TO_SNOMED.txt"
MESH_TO_SNOMED_MAPPING_FILE="../../terminology-mappings/StandardVocabToMeSH/mesh-to-standard-vocab-v5.txt"

# load the meddra to snomed mapping
meddra_to_snomed_mapping_d = {}
inf = open(MEDDRA_TO_SNOMED_MAPPING_FILE,"r")
l = inf.readline() # skip header
l = inf.readline()
while l:
    s = l.strip()
    if s == "":
        break

    (meddra_concept_id,meddra_concept_name,snomed_concept_id,snomed_concept_name) = s.split("\t")
    meddra_to_snomed_mapping_d[meddra_concept_id] = [meddra_concept_name,snomed_concept_id,snomed_concept_name]
    
    l = inf.readline()
inf.close()

# TODO...
# # load the mesh to snomed mapping
# mesh_to_snomed_mapping_d = {}
# inf = open(MESH_TO_SNOMED_MAPPING_FILE,"r")
# l = inf.readline() # skip header
# l = inf.readline()
# while l:
#     s = l.strip()
#     if s == "":
#         break

#     (mesh_concept_id,mesh_concept_name,snomed_concept_id,snomed_concept_name) = s.split("\t")
#     mesh_to_snomed_mapping_d[mesh_concept_id] = [mesh_concept_name,snomed_concept_id,snomed_concept_name]
    
#     l = inf.readline()
# inf.close()


# Enum to help parse the data files
(KEY,EV_SOURCE_LABEL,MODALITY,EV_SOURCE_ID,STATISTIC,LINKOUT,STATISTIC_TYPE) = range(0,7)

## Set up the db connection
# NOTE: If you are running outside of the OHDSI dev server, be sure
# set up the SSH tunnel to postgres on the dev server first.
f = open(DB_CONNECTION_INFO,'r')
(db,user,pword,host,port) = f.readline().strip().split("\t")
f.close()
try:
    conn=psycopg2.connect(database=db, user=user, password=pword, host=host, port=port)
except Exception as e:
    print "ERROR: Unable to connect to database %s (user:%s) on host %s (port: %s). Check that the data in db-connection.conf is correct and that there is not barrier related to the network connection. Error: %s" % (db,user,host,port,e)

cur = conn.cursor()

## identify the data sources to be processed. Expects a tab-delimited
## file with name and path to data in each line
(SOURCE,PATH_TO_DATA,HOI_VOCAB_ID) = range(0,3)
f = open(SOURCE_LISTING_FILE,'r')
buf = f.read().strip()
f.close()
srcL = [x.strip().split("\t") for x in buf.split("\n")]
print "INFO: Source data locations:\n\t%s" % srcL

## iterate through each source and write the data to go into
## drug_hoi_evidence Map the HOI concepts to SNOMED if not already
## done by the source. Use the local mapping file first, then try to
## query for the mapping.
##
cntr = 0 # serves as an unique key for the output table ('id')
drugHoiDataOutF = open(DRUG_HOI_DATA_FILE,'w')
dhKeyD = {} # used to accumulate all drug-HOI keys so that the drug-hoi relationship table can be created
idToSnomedD = {} # cache for mesh or meddra to snomed mapping. The
                 # coding systems use distinct patterns for CUIs so it
                 # should be safe to combine them into one dictionary
noMappingFoundD = {} # stores concept ids that cannot be mapped by any
                     # method to prevent repetitive querying
(B_CONCEPT_ID, B_CONCEPT_NAME, B_CONCEPT_CODE, A_CONCEPT_NAME, A_CONCEPT_CODE) = range(0,5) # enum for vocab query results
for src in srcL[1:]: # skip header
    print "INFO: loading source: %s" % src[0]
    try:
        f = open(src[PATH_TO_DATA], 'r')
        buf = f.read().strip()
        dhL = [x.strip() for x in buf.split("\n")]
        f.close()
    except Exception as e:
        print "ERROR: unable to open data file for source %s located at %s. Error string: %s" % (src[SOURCE],src[PATH_TO_DATA],e)
        sys.exit(1)
        
    # TODO: write validation checks for the data files to be loaded (e.g., col number, types, etc)
    #for elt in dhL[0:10]:
    for elt in dhL:    
        # the schema calls for a bool type for 'modality'
        s = elt.replace("positive","true").replace("negative","false") 

        # skip nulls
        if s.find("NULL") != -1:
            print "WARNING: skipping creation of DRUG_HOI_DATA_FILE entry with NULL. TODO: edit this the script to avoid capturing NULLS to begin with."
            continue

        tpl = s.split("\t")            
        if len(tpl) == 1:
            break

        if src[HOI_VOCAB_ID] == "Standard_Vocab":
            drugHoiDataOutF.write("\t".join([str(cntr)] + tpl) + "\n")
            cntr += 1
            if not dhKeyD.has_key(tpl[KEY]):
                (drug,hoi) = tpl[KEY].split("-")
                dhKeyD[tpl[KEY]] = {'drug_id':drug, 'drug_label':None, 'hoi_id':hoi, 'hoi_label':None}
                print "DRUG_RELATIONSHIP: %s|%s||%s|" % (tpl[KEY],drug,hoi) # something we can grep that we can load the partial drug relationship and evidence data if the script crashes         
        elif src[HOI_VOCAB_ID] == "SNOMED":
            drugHoiDataOutF.write("\t".join([str(cntr)] + tpl) + "\n")
            cntr += 1
            if not dhKeyD.has_key(tpl[KEY]):
                (drug,hoi) = tpl[KEY].split("-")
                dhKeyD[tpl[KEY]] = {'drug_id':drug, 'drug_label':None, 'hoi_id':hoi, 'hoi_label':None}
                print "DRUG_RELATIONSHIP: %s|%s||%s|" % (tpl[KEY],drug,hoi) # something we can grep that we can load the partial drug relationship and evidence data if the script crashes 
        else:
            mixedMapped = False # used only if the mapping type is 'Mixed'
            try:
                (drug,hoi) = tpl[KEY].split("-")
            except ValueError:
                print "WARNING: could not split out drug and hoi from tpl[KEY]: %s" % tpl[KEY]
                continue

            if noMappingFoundD.has_key(hoi):
                print "INFO: HOI concept id has already been found to be un-mappable at the present time %s" % hoi
                continue
            
            mappingFound = False
            
            rows = []
            if (mappingFound == False) and meddra_to_snomed_mapping_d.has_key(hoi):
                mappingFound = True
                rows = [[meddra_to_snomed_mapping_d[hoi][1],meddra_to_snomed_mapping_d[hoi][2],"","",meddra_to_snomed_mapping_d[hoi][0]]]
                print "INFO: MedDRA concept id %s mapped to SNOMED HOI %s using local mapping" % (hoi,meddra_to_snomed_mapping_d[hoi][1])
            
            if (mappingFound == False) and idToSnomedD.has_key(hoi):
                mappingFound = True
                rows = idToSnomedD[hoi]
                print "INFO: MedDRA concept id %s mapped to SNOMED HOI from cache"

            if (mappingFound == False) and (src[HOI_VOCAB_ID] == "Mesh" or (src[HOI_VOCAB_ID] == "Mixed" and mixedMapped == False)):
                try:
                    print "INFO: Attempting to map concept id for Mesh coded HOI %s to SNOMED" % hoi
                    cur.execute("""
SELECT DISTINCT c2.CONCEPT_ID AS SNOMED_CONCEPT_ID, c2.concept_name AS SNOMED_CONCEPT_NAME, c2.concept_code AS SNOMED_CONCEPT_CODE, c1.concept_id AS MESH_CONCEPT_ID, c1.concept_name AS MESH_CONCEPT_NAME, c1.CONCEPT_CODE AS MESH_CONCEPT_CODE
FROM concept c1 JOIN concept_relationship cr ON cr.concept_id_1 = c1.CONCEPT_ID
  JOIN CONCEPT c2 ON c2.CONCEPT_ID = cr.CONCEPT_ID_2
   AND c2.invalid_reason IS NULL
   AND c2.vocabulary_id = 'SNOMED'
   AND c2.concept_class_id = 'Clinical Finding'
WHERE c1.concept_id = '%s'
   AND c1.vocabulary_id = 'MeSH'
   AND c1.invalid_reason IS NULL
   AND cr.INVALID_REASON IS NULL
   AND c1.CONCEPT_CLASS_ID = 'Main Heading'
""" % hoi)
                except Exception as e:
                    print "ERROR: Attempt to map concept id for Mesh HOI to SNOMED failed. Error string: %s" % e

                rows = cur.fetchall()
                if len(rows) == 0:
                    print "WARNING: Attempt to map concept id for Mesh HOI %s to SNOMED failed because no mapping could be found in the standard vocabulary." % hoi
                    if src[HOI_VOCAB_ID] == "Mixed":
                        print "WARNING: this case will be tested for other vocabs"
                    else:
                        print "WARNING: this case will NOT be tested for other vocabs"
                        noMappingFoundD[hoi] = None
                        continue 
                else:
                    mappingFound == True
                    if src[HOI_VOCAB_ID] == "Mixed":
                        mixedMapped = True
                        
                    # cache hoi mapping 
                    if not idToSnomedD.has_key(hoi):
                        idToSnomedD[hoi] = rows

            if (mappingFound == False) and (src[HOI_VOCAB_ID] == "MedDRA" or (src[HOI_VOCAB_ID] == "Mixed" and mixedMapped == False)):
                try:
                    print "INFO: Attempting to map concept id for MedDRA coded HOI '%s' to SNOMED" % hoi
                    # The way this works is it tries to find the
                    # SNOMED codes that have the closest relationship
                    # to the MedDRA PT code.  We could expand this to
                    # other MedDRA levels but it gets fuzzier.
                    cur.execute("""
SELECT z.SNOMED_CONCEPT_ID, z.SNOMED_CONCEPT_NAME, z.SNOMED_CONCEPT_CODE, z.MEDDRA_CONCEPT_NAME, z.MEDDRA_CONCEPT_CODE 
FROM ( SELECT ca.max_levels_of_separation, ca.min_levels_of_separation, c.concept_id AS MEDDRA_CONCEPT_ID, c.concept_code AS MEDDRA_CONCEPT_CODE, c.concept_name AS MEDDRA_CONCEPT_NAME, c2.concept_id AS SNOMED_CONCEPT_ID, c2.concept_name AS SNOMED_CONCEPT_NAME, c2.concept_code AS SNOMED_CONCEPT_CODE, ROW_NUMBER() OVER(PARTITION BY c.CONCEPT_ID ORDER BY c.CONCEPT_ID, ca.min_levels_of_separation, ca.max_levels_of_separation, c.CONCEPT_ID, c2.CONCEPT_ID) AS ROW_NUM
FROM CONCEPT c JOIN concept_ancestor ca ON ca.ancestor_concept_id = c.concept_id
  JOIN CONCEPT c2 ON c2.concept_id = ca.descendant_concept_id
    AND c2.vocabulary_id = 'SNOMED'
    AND c2.CONCEPT_CLASS_ID = 'Clinical Finding'
    AND c2.INVALID_REASON IS NULL
WHERE c.concept_id = '%s'
AND c.vocabulary_id = 'MedDRA'
-- AND c.concept_class_id = 'PT'
AND c.INVALID_REASON IS NULL
) z
WHERE z.ROW_NUM = 1
""" % hoi)
                except Exception as e:
                    print "ERROR: Attempt to map concept id for MedDRA HOI to SNOMED failed. Error string: %s" % e
                rows = cur.fetchall()
                if len(rows) == 0:
                    print "WARNING: Attempt to map concept id for MedDRA HOI %s to SNOMED failed because no mapping could be found in the standard vocabulary." % hoi
                    if src[HOI_VOCAB_ID] == "Mixed":
                        print "WARNING: this case will be tested for other vocabs"
                    else:
                        print "WARNING: this case will NOT be tested for other vocabs"
                        noMappingFoundD[hoi] = None
                        continue 
                else:
                    mappingFound == True
                    
                    if src[HOI_VOCAB_ID] == "Mixed":
                        mixedMapped = True
                        
                    # cache hoi mapping 
                    if not idToSnomedD.has_key(hoi):
                        idToSnomedD[hoi] = rows

            if (mappingFound == False) and ((src[HOI_VOCAB_ID] == "Mixed" and mixedMapped == False)):
                try:
                    print "INFO: Testing if coded HOI %s is already a SNOMED" % hoi
                    cur.execute("""
SELECT c1.CONCEPT_ID AS SNOMED_CONCEPT_ID, c1.concept_name AS SNOMED_CONCEPT_NAME, c1.concept_code AS SNOMED_CONCEPT_CODE
FROM CONCEPT AS c1
WHERE c1.invalid_reason IS NULL
AND c1.vocabulary_id = 'SNOMED'
AND c1.concept_class_id = 'Clinical Finding'
AND c1.concept_id = %s
""" % hoi)
                except Exception as e:
                    print "ERROR: Test if concept id is SNOMED failed. Error string: %s" % e                
                rows = cur.fetchall()
                if len(rows) == 0:
                    print "WARNING: Test if concept id HOI %s is SNOMED failed. It's possible that the concept is not in SNOMED or that it's not a Clinical Finding or the concept is invalid according to the standard vocabulary." % hoi
                    print "WARNING: There are no other tests for this concept: %s" % hoi
                    noMappingFoundD[hoi] = None
                    continue
                
                cntr += 1
                if not dhKeyD.has_key(tpl[KEY]):
                    dhKeyD[tpl[KEY]] = {'drug_id':drug, 'drug_label':None, 'hoi_id':hoi, 'hoi_label':None}
                print "INFO: This concept from a Mixed source is SNOMED: %s" % hoi
                continue

            
            for row in rows:
                # write out results
                snomedHoi = row[B_CONCEPT_ID]
                print "INFO: mapped HOI concept id from %s (%s - %s : %s) to %s (SNOMED - %s : %s)" % (hoi, src[HOI_VOCAB_ID], row[A_CONCEPT_CODE], row[A_CONCEPT_NAME], snomedHoi, row[B_CONCEPT_CODE], row[B_CONCEPT_NAME])
                tpl[KEY] = "%s-%s" % (drug, snomedHoi)
                drugHoiDataOutF.write("\t".join([str(cntr)] + tpl) + "\n")
                cntr += 1
                if not dhKeyD.has_key(tpl[KEY]):
                    dhKeyD[tpl[KEY]] = {'drug_id':drug, 'drug_label':None, 'hoi_id':snomedHoi, 'hoi_label':None}
                    print "DRUG_RELATIONSHIP: %s|%s||%s|" % (tpl[KEY],drug,hoi) # something we can grep that we can load the partial drug relationship and evidence data if the script crashes 

drugHoiDataOutF.close()

## Now, create the data file for the drug-hoi relationship table
capturedKeysD = {}
capturedDrugsD = {}
capturedHoisD = {}
try:
    f = open(CACHED_DRUG_HOI_RELATIONSHIP_FILE,'r') # use cached data from previous runs to save queries
    buf = f.read().strip()
    f.close()
    cachedDhrL = [x.strip() for x in buf.split("\n")]
    for elt in cachedDhrL:
        if not elt:
            break

        (k,dId,dLab,hqId,hLab) = elt.strip().split("|")
        if dhKeyD.has_key(k):
            capturedKeysD[k] = k
            dhKeyD[k]['drug_label'] = dLab
            dhKeyD[k]['hoi_label'] = hLab
        
            capturedDrugsD[dhKeyD[k]['drug_id']] = dhKeyD[k]['drug_label']
            capturedHoisD[dhKeyD[k]['hoi_id']] = dhKeyD[k]['hoi_label']
except IOError:
    print "WARNING: Caught IOError exception indicating that the file %s does not exist. Proceeding without using cached concepts." % CACHED_DRUG_HOI_RELATIONSHIP_FILE

print "INFO: number of cached keys: %d; number of keys needed: %d" % (len(capturedKeysD.keys()), len(dhKeyD.keys()))

for key in dhKeyD.keys():
    if capturedKeysD.has_key(key):
        continue
    
    dLab = hLab = None
    if capturedDrugsD.has_key(dhKeyD[key]['drug_id']):
       dLab  = capturedDrugsD[dhKeyD[key]['drug_id']]
    else:
        try:
            print "INFO: Attempting to SELECT from concept table where concept id - %d" % int(dhKeyD[key]['drug_id'])
            cur.execute("""SELECT concept_name from concept where concept_id = %d;""" % int(dhKeyD[key]['drug_id']))
        except Exception as e:
            print "ERROR: Attempt to SELECT from concept table failed. Error string: %s" % e

        rows = cur.fetchall()
        if len(rows) > 0:
            print "   ", rows[0][0]
            dLab = rows[0][0]
    dhKeyD[key]['drug_label'] = dLab
    capturedDrugsD[dhKeyD[key]['drug_id']] = dhKeyD[key]['drug_label']

    if capturedHoisD.has_key(dhKeyD[key]['hoi_id']):
       hLab  = capturedHoisD[dhKeyD[key]['hoi_id']]
    else:
        try:
            print "INFO: Attempting to SELECT from concept table where concept id - %d" % int(dhKeyD[key]['hoi_id'])
            cur.execute("""SELECT concept_name from concept where concept_id = %d;""" % int(dhKeyD[key]['hoi_id']))
        except Exception as e:
            print "ERROR: Attempt to SELECT from concept table failed. Error string: %s" % e
        rows = cur.fetchall()
        if len(rows) > 0:
            print "   ", rows[0][0]
            hLab = rows[0][0]
    dhKeyD[key]['hoi_label'] = hLab
    capturedHoisD[dhKeyD[key]['hoi_id']] = dhKeyD[key]['hoi_label']

## write out the DRUG_HOI_RELATIONSHIP_FILE from dhKeyD
dHROutf = open(DRUG_HOI_RELATIONSHIP_FILE,'w')
srtdKeys = dhKeyD.keys()
srtdKeys.sort()
for k in srtdKeys:
    v = dhKeyD[k]
    s = "|".join([str(k),str(v['drug_id']),str(v['drug_label']),str(v['hoi_id']),str(v['hoi_label'])]) + "\n"
    if s.find("NULL") != -1:
        print "WARNING: skipping creation of DRUG_HOI_RELATIONSHIP_FILE entry with NULL. TODO: edit this the script to avoid capturing NULLS to begin with."
        continue

    dHROutf.write(s)
dHROutf.close()

print "INFO: To make future use of this script more efficient, be sure to APPEND (i.e., copy without overwriting) the data in the file %s to %s" % (DRUG_HOI_RELATIONSHIP_FILE,CACHED_DRUG_HOI_RELATIONSHIP_FILE)
