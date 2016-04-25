# getLinkoutOADataMapping.py
#
# get a mapping from linkouts to annotation identifiers so that
# queries can be done in the relational data to across the
# drug_hoi_evidence and OA tables

import sys
import json
import urllib2

import pymysql # for mysql connection to lil_urls

LIL_URL_CONNECTION_INFO="db-connection-lil_urls.conf"
OUT_MAPPING_FILE="linkouts_to_annotation_ids.dsv"
LINKOUT_PREFIX="http://dbmi-icode-01.dbmi.pitt.edu/l/index.php?id="

# An iterator that uses fetchmany to keep memory usage down
def ResultIter(cursor, arraysize=1000):
    while True:
        results = cursor.fetchmany(arraysize)
        if not results:
            break
        for result in results:
            yield result

# Step 1: Open a connection to the lil_url database from which we will
# pull the linkout urls and sparql queries
f = open(LIL_URL_CONNECTION_INFO,'r')
(db,user,pword,host,port) = f.readline().strip().split("\t")
f.close()
try:
    conn=pymysql.connect(host=host, port=3306, user=user, passwd=pword, db=db)
except Exception as e:
    print "ERROR: Unable to connect to database %s (user:%s) on host %s (port: %s). Check that the data in db-connection-lil_urls.conf is correct and that there is not barrier related to the network connection. Error: %s" % (db,user,host,port,e)
cur = conn.cursor()

q = """SELECT id, url FROM lil_urls"""
cur.execute(q)

f = open(OUT_MAPPING_FILE,'w')
ctr = -1
for rslt in ResultIter(cur):
    ctr +=1
    (url_suffix,url) = (rslt[0],rslt[1])

    ## TEMPORARY FIX TO PICK UP RUN WHERE IT LEFT OFF
    if url_suffix.find('ctd') != -1 or url_suffix.find('splicer') != -1:
        continue
    ## END OF TEMP FIX

    
    print "Retrieving data for " + url_suffix
    
    # Step 2: Run the SPARQL queries and get the JSON data back
    rslt = json.load(urllib2.urlopen(url))

    ## Debug
    #print "%s" % rslt['results']['bindings'][0]['an']['value']
    
    # Step 3: Append the linkout url and annotation id to the mapping file
    for rec in rslt['results']['bindings']:
        anVal = rec['an']['value']
        f.write(LINKOUT_PREFIX + url_suffix + "\t" + anVal + "\n")

    ## Debug    
    #if ctr == 100:
    #    sys.exit(0)

f.close
conn.close()
