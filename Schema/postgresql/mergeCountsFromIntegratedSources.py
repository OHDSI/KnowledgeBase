## mergeCountsFromIntegratedSources.py
##
## synthesize the evidence source count and linkout data into
## tables that can them be loaded into the Schema relational DB model
## (that extends the OHDSI Standard Vocab). 
##
## Author: Richard D Boyce, PhD
## Fall/Winter 2014

import psycopg2

SOURCE_LISTING_FILE="integratedSources.conf"
DB_CONNECTION_INFO="db-connection.conf"

f = open(DB_CONNECTION_INFO,'r')
(db,user,pword,host,port) = f.readline().strip().split("\t")
f.close()


# NOTE: If you are running outside of the OHDSI dev server, be sure
# set up the SSH tunnel to postgres on the dev server first.
try:
    conn=psycopg2.connect(database=db, user=user, password=pword, host=host, port=port)
except Exception as e:
    print "I am unable to connect to database %s (user:%s) on host %s (port: %s). Check that the data in db-connection.conf is correct and that there is not barrier related to the network connection. Error: %s" % (db,user,host,port,e)

cur = conn.cursor()
try:
    cur.execute("""SELECT * from concept where concept_id in (757688, 35708164, 36718347, 36718193, 36009711, 37320268, 36045300, 36045336, 36416514, 36918858, 37282586);""")
except:
    print "I can't SELECT from concept"

rows = cur.fetchall()
print "\nRows: \n"
for row in rows:
    print "   ", row[1]


