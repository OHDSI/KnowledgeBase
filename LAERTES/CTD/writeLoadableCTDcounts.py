# writeLoadableEUSPCcounts.py
#
# Write a summary and index of CTD drug-hoi data 
#
# Authors: Charles Kronk and Rich Boyce
# Spring 2016
#
import urllib2, urllib, re, sys

VT_SERVER="virtuoso.ohdsi.org" # Release 
# VT_SERVER="130.49.206.139"  # Development
VT_PORT="8890"

URL_SHORTENER_URL="http://dbmi-icode-01.dbmi.pitt.edu/l" # Release
# URL_SHORTENER_URL="http://130.49.206.139/l" # Development

DATAFILE = "ctd-graph-count-query-March2016.txt" # NOTE: this data comes a CSV export of the  query below
EVTYPE = "CTD_ChemicalDisease"
URL_ID_PREFIX = "ctd-"
URL_PREFIX = "%s/index.php?id=" % URL_SHORTENER_URL
SQL_INSERT_OUTFILE = "insertShortURLs-ALL.txt"

## NOTE: run the query using the following isql command because
## queries from curl or the virtuoso sparql web form truncate the
## results:
##
## $ isql-vt -H localhost -S 1111  -U <user name> -P <password> errors=stdout < /tmp/test.sparql > /tmp/test.out
## $ egrep "^[0-9]+ +http.*" /tmp/test.out | sed 's/.(/\_(/g' | sed 's/.type/\_type/g' | sed 's/e r/e_r/g' | sed 's/l t/l_t/g' | tr -s '  *' ',' > sample-summary-query.txt
##
## count data retrieved from the EU SPC graph in the SPARQL endpoint
## (http://virtuoso.ohdsi.org:8890/sparql) using the
## following query.
## QUERY (paste into /tmp/test.sparql):
## SPARQL PREFIX ohdsi:<http://purl.org/net/ohdsi#> PREFIX oa:<http://www.w3.org/ns/oa#> PREFIX meddra:<http://purl.bioontology.org/ontology/MEDDRA/> PREFIX ncbit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#> PREFIX foaf: <http://xmlns.com/foaf/0.1/> PREFIX dailymed:<http://dbmi-icode-01.dbmi.pitt.edu/linkedSPLs/vocab/resource/>  SELECT count distinct ?an ?drug ?hoi FROM <http://purl.org/net/nlprepository/ohdsi-ctd-chem-disease-poc> WHERE {  ?an a ohdsi:ADRAnnotation;    oa:hasBody ?body;    oa:hasTarget ?target.   ?body ohdsi:ImedsDrug ?drug.  ?body ohdsi:ImedsHoi ?hoi.   };


# replace the @IMEDS_DRUG@ and @IMEDS_HOI@ strings with the appropriate values
TEMPLATE = "http://@VT_SERVER@:@VT_PORT@/sparql?default-graph-uri=&query=PREFIX+ohdsi%3A<http%3A%2F%2Fpurl.org%2Fnet%2Fohdsi%23>%0D%0APREFIX+oa%3A<http%3A%2F%2Fwww.w3.org%2Fns%2Foa%23>%0D%0A%0D%0ASELECT+*+%0D%0AWHERE+%7B%0D%0A+GRAPH+<http%3A%2F%2Fpurl.org%2Fnet%2Fnlprepository%2Fohdsi-ctd-chem-disease-poc>%7B%0D%0A++%3Fan+a+ohdsi%3AADRAnnotation%3B%0D%0A++++oa%3AhasBody+%3Fbody%3B%0D%0A++++oa%3AhasTarget+%3Ftarget.%0D%0A%0D%0A++%3Fbody+ohdsi%3AImedsDrug+ohdsi%3A@IMEDS_DRUG@.%0D%0A++%3Fbody+ohdsi%3AImedsHoi+ohdsi%3A@IMEDS_HOI@.%0D%0A++%3Fbody+ohdsi%3ADirectEvidence+%3FdirectEvidence.%0D%0A++%3Fbody+ohdsi%3AInferenceGeneSymbol+%3FinferenceGeneSymbol.%0D%0A++%3Fbody+ohdsi%3AInferenceScore+%3FinferenceScore.%0D%0A++%0D%0A++%3Ftarget+oa%3AhasSource+%3Fsource.+%0D%0A+%7D%0D%0A%7D%0D%0A%0D%0A&format=json&timeout=0&debug=on"

TEMPLATE = TEMPLATE.replace('@VT_SERVER@', VT_SERVER).replace('@VT_PORT@',VT_PORT)

f = open(DATAFILE)
buf = f.read()
f.close()
l = buf.split("\n")[1:]

f = open(SQL_INSERT_OUTFILE,'w')
i = 0
pre = ""
for elt in l:
    if not elt:
        break

    i += 1
    (cnt,drug,hoi) = [x.strip() for x in elt.replace("http://purl.org/net/ohdsi#","").split(",")]
    q = TEMPLATE.replace("@IMEDS_DRUG@",drug).replace("@IMEDS_HOI@",hoi)
    url_id = URL_ID_PREFIX + str(i)
    if i > 1:
        pre = ",\n"
    else:
        f.write("INSERT INTO lil_urls VALUES \n")

    f.write("%s('%s','%s',CURRENT_TIMESTAMP)" % (pre,url_id, q))
    turl = URL_PREFIX + url_id
    key = "%s-%s" % (drug,hoi)
    print "\t".join([key,EVTYPE,'positive',"1",str(cnt),turl,"COUNT"])
f.write(";")
f.close()
