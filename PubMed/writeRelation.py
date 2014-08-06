# writeRelation.py
#
# Write a summary and index of pubmed drug-hoi data identified by mesh indexing
#
# Author: Richard D Boyce, PhD
# July 2014
#

import tinyurl

DATAFILE = "sample-summary-query.txt"
EVTYPE = "MEDLINE_MeSH"

# replace the @IMEDS_DRUG@ and @MEDDRA_HOI@ strings with the appropriate values
TEMPLATE = "http://dbmi-icode-01.dbmi.pitt.edu:8080/sparql?default-graph-uri=&query=PREFIX+ohdsi%3A%3Chttp%3A%2F%2Fpurl.org%2Fnet%2Fohdsi%23%3E%0D%0APREFIX+oa%3A%3Chttp%3A%2F%2Fwww.w3.org%2Fns%2Foa%23%3E%0D%0APREFIX+meddra%3A%3Chttp%3A%2F%2Fpurl.bioontology.org%2Fontology%2FMEDDRA%2F%3E%0D%0APREFIX+ncbit%3A+%3Chttp%3A%2F%2Fncicb.nci.nih.gov%2Fxml%2Fowl%2FEVS%2FThesaurus.owl%23%3E%0D%0APREFIX+foaf%3A+%3Chttp%3A%2F%2Fxmlns.com%2Ffoaf%2F0.1%2F%3E%0D%0APREFIX+dailymed%3A%3Chttp%3A%2F%2Fdbmi-icode-01.dbmi.pitt.edu%2FlinkedSPLs%2Fvocab%2Fresource%2F%3E%0D%0A%0D%0ASELECT+DISTINCT%28%3Fan%29%0D%0AWHERE+%7B%0D%0A+%3Fan+a+ohdsi%3APubMedDrugHOIAnnotation%3B%0D%0A+++oa%3AhasBody+%3Fbody%3B%0D%0A+++oa%3AhasTarget+%3Ftarget.%0D%0A%0D%0A+%3Fbody+ohdsi%3AImedsDrug+ohdsi%3A@IMEDS_DRUG@.%0D%0A+%3Fbody+ohdsi%3AMeddraHois+%3Fhois.+%0D%0A%0D%0A+%3Fhois+ohdsi%3AMeddraHoi+meddra%3A@MEDDRA_HOI@.%0D%0A%0D%0A+%3Ftarget+ohdsi%3AMeshStudyType+%22case+reports+%28publication+type%29%22.%0D%0A%0D%0A%7D&format=text%2Fhtml&timeout=0&debug=on"


f = open(DATAFILE)
buf = f.read()
f.close()
buf = buf.replace("http://purl.org/net/ohdsi#","").replace("http://purl.bioontology.org/ontology/MEDDRA/","").replace('"',"")
l = buf.split("\n")[1:]

i = 0
for elt in l:
    i += 1
    (cnt,drug,hoi) = [x.strip() for x in elt.split(",")]
    q = TEMPLATE.replace("@IMEDS_DRUG@",drug).replace("@MEDDRA_HOI@",hoi)
    turl = tinyurl.create_one(q)
    print "\t".join([str(i),drug,hoi,'literature_case_report',str(3),str(cnt),turl])

