## mergeCountsFromIntegratedSources.py
##
## synthesize the evidence source count and linkout data into
## tables that can them be loaded into the Schema relational DB model
## (that extends the OHDSI Standard Vocab). 
##
## Author: Richard D Boyce, PhD
## Fall/Winter 2014

import psycopg2

DB_CONNECTION_INFO="db-connection.conf"
SOURCE_LISTING_FILE="integratedSources.conf"
DRUG_HOI_DATA_FILE="drug-hoi-evidence-data.tsv"
CACHED_DRUG_HOI_RELATIONSHIP_FILE="cached_uniq_drug_hoi_relationships.csv"
DRUG_HOI_RELATIONSHIP_FILE="uniq_drug_hoi_relationships.csv"

# Enum to help parse the data files
(KEY,EV_SOURCE_LABEL,MODALITY,EV_SOURCE_ID,STATISTIC,LINKOUT,STATISTIC_TYPE) = range(0,7)

## Set up the db connection
f = open(DB_CONNECTION_INFO,'r')
(db,user,pword,host,port) = f.readline().strip().split("\t")
f.close()

## identify the data sources to be processed. Expects a tab-delimited
## file with name and path to data in each line
f = open(SOURCE_LISTING_FILE,'r')
buf = f.read().strip()
f.close()
srcL = [x.strip().split("\t") for x in buf.split("\n")]
print "INFO: Source data locations:\n\t%s" % srcL

## iterate through each source and write the data to go into drug_hoi_evidence
cntr = 0 # serves as an unique key for the output table ('id')
drugHoiDataOutF = open(DRUG_HOI_DATA_FILE,'w')
dhKeyD = {} # used to accumulate all drug-HOI keys so that the drug-hoi relationship table can be created
for src in srcL:
    print "INFO: loading source: %s" % src[0]
    try:
        f = open(src[1], 'r')
        buf = f.read().strip()
        dhL = [x.strip() for x in buf.split("\n")]
        f.close()
    except Exception as e:
        print "ERROR: unable to open data file for source %s located at %s. Error string: %s" % (src[0],src[1],e)

    # TODO: write validation checks for the data files to be loaded (e.g., col number, types, etc)
    for elt in dhL:
        cntr += 1
        tpl = elt.split("\t")            
        if len(tpl) == 1:
            break

        elt = elt.replace("positive","true").replace("negative","false") # the schema calls for a bool type for 'modality'
        drugHoiDataOutF.write("%d\t%s\n" % (cntr, elt)) # just need to add the id column
        
        if not dhKeyD.has_key(tpl[KEY]):
            (drug,hoi) = tpl[KEY].split("-")
            dhKeyD[KEY] = {'drug_id':drug, 'drug_label':None, 'hoi_id':hoi, 'hoi_label':None}

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
        
        capturedDrugsD[dhKeyD[k]['drug_id']] = dhKeyD[k]['drug_label']
        capturedHoisD[dhKeyD[k]['hoi_id']] = dhKeyD[k]['hoi_label']

# NOTE: If you are running outside of the OHDSI dev server, be sure
# set up the SSH tunnel to postgres on the dev server first.
try:
    conn=psycopg2.connect(database=db, user=user, password=pword, host=host, port=port)
except Exception as e:
    print "ERROR: Unable to connect to database %s (user:%s) on host %s (port: %s). Check that the data in db-connection.conf is correct and that there is not barrier related to the network connection. Error: %s" % (db,user,host,port,e)

cur = conn.cursor()

for key in dhKeyD.keys():
    if capturedKeysD.has_key(key):
        continue
    
    dLab = hLab = None
    if capturedDrugsD.has_key(dhKeyD[key]['drug_id']):
       dLab  = capturedDrugsD[dhKeyD[key]['drug_id']]
    else:
        print "CHECK 1"
        try:
            print "INFO: Attempting to SELECT from concept table where concept id - %d" % int(dhKeyD[key]['drug_id'])
            cur.execute("""SELECT concept_name from concept where concept_id = %d;""" % int(dhKeyD[key]['drug_id']))
        except Exception as e:
            print "ERROR: Attempt to SELECT from concept table failed. Error string: %s" % e

        rows = cur.fetchall()
        print "INFO: result count: %d" % len(rows)
        if len(rows) > 0:
            print "   ", rows[0]
            dLab = rows[0]
    dhKeyD[key]['drug_label'] = dLab
    capturedDrugsD[dhKeyD[key]['drug_id']] = dhKeyD[key]['drug_label']

    if capturedHoisD.has_key(dhKeyD[key]['hoi_id']):
       hLab  = capturedHoisD[dhKeyD[key]['hoi_id']]
    else:
        print "CHECK 2"
        try:
            print "INFO: Attempting to SELECT from concept table where concept id - %d" % int(dhKeyD[key]['hoi_id'])
            cur.execute("""SELECT concept_name from concept where concept_id = %d;""" % int(dhKeyD[key]['hoi_id']))
        except Exception as e:
            print "ERROR: Attempt to SELECT from concept table failed. Error string: %s" % e
        rows = cur.fetchall()
        print "INFO: result count: %d" % len(rows)
        if len(rows) > 0:
            print "   ", rows[0][0]
            hLab = rows[0][0]
    dhKeyD[key]['hoi_label'] = hLab
    capturedHoisD[dhKeyD[key]['hoi_id']] = dhKeyD[key]['hoi_label']

## write out the DRUG_HOI_RELATIONSHIP_FILE from dhKeyD
dHROutf = open(DRUG_HOI_RELATIONSHIP_FILE,'w')
for k,v in dhKeyD.iteritems():
    s = "|".join([k,v['drug_id'],v['drug_label'],v['hoi_id'],v['hoi_label']]) + "\n"
    dHROutf.write(s)
dHROutf.write("\n")
dHROutf.close()
