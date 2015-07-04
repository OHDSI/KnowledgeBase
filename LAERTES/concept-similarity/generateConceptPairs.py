# generateConceptPairs.py
#
# Create a file of SNOMED concept pairs using UMLS CUIs
#
# Author: Richard Boyce
# July 2015
#

import mysql.connector

QUERY_TMPL = "select distinct CUI,STR from MRCONSO where SAB = 'SNOMEDCT_US' and LAT = 'ENG' and TTY = 'PT' and  CODE = '@SNOMED@'"

cnx = mysql.connector.connect(user='umls-user', password='umls', host='127.0.0.1', database='umls')
cursor = cnx.cursor()

f = open("data/all-mapped-SNOMED.txt")
ln = f.readline()
code_l = []
while ln != "" and ln != None:
    concept_code = ln.strip()
    print "SNOMED: " + concept_code
    query = QUERY_TMPL.replace("@SNOMED@",concept_code)

    cursor.execute(query)

    row = cursor.fetchone()

    if row != None:
        print "UMLS CUI: " + concept_code
        code_l.append(row[0])
    
    ln = f.readline()

f.close()
cursor.close()
cnx.close()

f = open("data/umls-similarity-input.txt","w")
for c1 in code_l:
    for c2 in code_l:
        if c1 != c2:
            f.write("%s<>%s\n" % (c1,c2))
f.close()

