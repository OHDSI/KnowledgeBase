## mergeCountsFromIntegratedSources.py
##
## synthesize the evidence source count and linkout data into
## tables that can them be loaded into the Schema relational DB model
## (that extends the OHDSI Standard Vocab). 
##
## Author: Richard D Boyce, PhD
## Fall/Winter 2014

import psycopg2 # for postgres 

DB_CONNECTION_INFO="db-connection.conf"
SOURCE_LISTING_FILE="integratedSources.conf"
DRUG_HOI_DATA_FILE="drug-hoi-evidence-data.tsv"
CACHED_DRUG_HOI_RELATIONSHIP_FILE="cached_uniq_drug_hoi_relationships.csv"
DRUG_HOI_RELATIONSHIP_FILE="uniq_drug_hoi_relationships.csv"

# Enum to help parse the data files
(ID,KEY,EV_SOURCE_LABEL,MODALITY,EV_SOURCE_ID,STATISTIC,LINKOUT,STATISTIC_TYPE) = range(0,8)

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

## iterate through each source and write the data to go into drug_hoi_evidence
## Map the HOI concepts to SNOMED if not already done by the source
##
cntr = 0 # serves as an unique key for the output table ('id')
drugHoiDataOutF = open(DRUG_HOI_DATA_FILE,'w')
dhKeyD = {} # used to accumulate all drug-HOI keys so that the drug-hoi relationship table can be created
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

    # TODO: write validation checks for the data files to be loaded (e.g., col number, types, etc)
    for elt in dhL[0:10]:
    #for elt in dhL:
        cntr += 1
        
        # the schema calls for a bool type for 'modality'
        elt = elt.replace("positive","true").replace("negative","false") 
        
        # write in the id for the record
        s = "%d\t%s\n" % (cntr, elt)

        # skip nulls
        if s.find("NULL") != -1:
            print "WARNING: skipping creation of DRUG_HOI_DATA_FILE entry with NULL. TODO: edit this the script to avoid capturing NULLS to begin with."
            continue

        tpl = s.split("\t")            
        if len(tpl) == 1:
            break

        if src[HOI_VOCAB_ID] == "SNOMED":
            drugHoiDataOutF.write("\t".join(tpl)) 
            if not dhKeyD.has_key(tpl[KEY]):
                (drug,hoi) = tpl[KEY].split("-")
                dhKeyD[tpl[KEY]] = {'drug_id':drug, 'drug_label':None, 'hoi_id':hoi, 'hoi_label':None}
        else:
            try:
                (drug,hoi) = tpl[KEY].split("-")
            except ValueError:
                print "WARNING: could not split out drug and hoi from tpl[KEY]: %s" % tpl[KEY]
                continue

            rows = []
            if src[HOI_VOCAB_ID] == "Mesh":
                try:
                    print "INFO: Attempting to map concept id for Mesh coded HOI %s to SNOMED" % hoi
                    cur.execute("""SELECT B.CONCEPT_ID, B.CONCEPT_NAME, B.CONCEPT_CODE, A.CONCEPT_NAME, A.CONCEPT_CODE FROM CONCEPT A, CONCEPT B, CONCEPT_RELATIONSHIP CR WHERE A.CONCEPT_ID = %s AND CR.CONCEPT_ID_1 = A.CONCEPT_ID AND CR.CONCEPT_ID_2 = B.CONCEPT_ID AND CR.RELATIONSHIP_ID = 'Maps to' AND B.CONCEPT_ID = CR.CONCEPT_ID_2 AND B.VOCABULARY_ID = 'SNOMED';""" % hoi)
                except Exception as e:
                    print "ERROR: Attempt to map concept id for Mesh HOI to SNOMED failed. Error string: %s" % e
                rows = cur.fetchall()
                if len(rows) == 0:
                    print "WARNING: Attempt to map concept id for Mesh HOI %s to SNOMED failed because no mapping could be found in the standard vocabulary." % hoi
                    continue 

            if src[HOI_VOCAB_ID] == "MedDRA":
                try:
                    print "INFO: Attempting to map concept id for MedDRA coded HOI '%s' to SNOMED" % hoi
                    cur.execute("""SELECT B.CONCEPT_ID, B.CONCEPT_NAME, B.CONCEPT_CODE, A.CONCEPT_NAME, A.CONCEPT_CODE FROM CONCEPT A, CONCEPT B, CONCEPT_RELATIONSHIP CR WHERE A.CONCEPT_ID = %s AND  CR.CONCEPT_ID_1 = A.CONCEPT_ID AND  CR.CONCEPT_ID_2 = B.CONCEPT_ID AND  CR.RELATIONSHIP_ID = 'MedDRA - SNOMED eq' AND B.CONCEPT_ID = CR.CONCEPT_ID_2 AND  B.VOCABULARY_ID = 'SNOMED';""" % hoi)
                except Exception as e:
                    print "ERROR: Attempt to map concept id for MedDRA HOI to SNOMED failed. Error string: %s" % e
                rows = cur.fetchall()
                if len(rows) == 0:
                    print "WARNING: Attempt to map concept id for MedDRA HOI %s to SNOMED failed because no mapping could be found in the standard vocabulary." % hoi
                    continue 

            for row in rows:
                snomedHoi = row[B_CONCEPT_ID]
                print "INFO: mapped HOI concept id from %s (%s - %s : %s) to %s (SNOMED - %s : %s)" % (hoi, src[HOI_VOCAB_ID], row[A_CONCEPT_CODE], row[A_CONCEPT_NAME], snomedHoi, row[B_CONCEPT_CODE], row[B_CONCEPT_NAME])
                tpl[KEY] = "%s-%s" % (drug, snomedHoi)
                drugHoiDataOutF.write("\t".join(tpl))
                if not dhKeyD.has_key(tpl[KEY]):
                    dhKeyD[tpl[KEY]] = {'drug_id':drug, 'drug_label':None, 'hoi_id':snomedHoi, 'hoi_label':None}

drugHoiDataOutF.close()

## Now, create the data file for the drug-hoi relationship table
f = open(CACHED_DRUG_HOI_RELATIONSHIP_FILE,'r') # use cached data from previous runs to save queries
buf = f.read().strip()
f.close()
cachedDhrL = [x.strip() for x in buf.split("\n")]
capturedKeysD = {}
capturedDrugsD = {}
capturedHoisD = {}
for elt in cachedDhrL:
    if not elt:
        break

    (k,dId,dLab,hId,hLab) = elt.strip().split("|")
    if dhKeyD.has_key(k):
        capturedKeysD[k] = k
        dhKeyD[k]['drug_label'] = dLab
        dhKeyD[k]['hoi_label'] = hLab
        
        capturedDrugsD[dhKeyD[k]['drug_id']] = dhKeyD[k]['drug_id']
        capturedHoisD[dhKeyD[k]['hoi_id']] = dhKeyD[k]['hoi_id']

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
    capturedDrugsD[dhKeyD[key]['drug_label']] = dhKeyD[key]['drug_label']
    capturedDrugsD[dhKeyD[key]['drug_id']] = dhKeyD[key]['drug_id']

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
    capturedHoisD[dhKeyD[key]['hoi_label']] = dhKeyD[key]['hoi_label']
    capturedHoisD[dhKeyD[key]['hoi_id']] = dhKeyD[key]['hoi_id']

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
