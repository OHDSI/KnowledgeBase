# writeLoadableSPLICERcounts.py Write a summary and index of splicer
#drug-hoi data Author: Richard D Boyce, PhD Summer/Fall 2014 

import urllib2, urllib, re, sys

DATAFILE = "test-query-of-counts-05052015.csv" # NOTE: this data comes from CSV export of the following query
EVTYPE = "SPL_SPLICER"
URL_ID_PREFIX = "splicer-"
URL_PREFIX = "http://dbmi-icode-01.dbmi.pitt.edu/l/index.php?id="
SQL_INSERT_OUTFILE = "insertShortURLs-ALL.txt"

## count data retrieved from the Virtuoso SPARQL endpoint using the
## following  query. 
##
## NOTE: that the ohdsi:MeddrraHoi is misleading because its actually
## the HOI concept code from OMOP.
##
## NOTE: Please the README for how to load the short URL data in mysql
##
## NOTE: run the query using the following isql command because
## queries from curl or the virtuoso sparql web form truncate the
## results:
##
## $ isql-vt -H localhost -S 1111  -U <user name> -P <password> errors=stdout < /tmp/test.sparql > /tmp/test.out
## $ egrep "^[0-9]+ +http.*" /tmp/test.out | tr -s ' ' ',' > /tmp/test-query-of-counts.csv
##
## QUERY (paste into /tmp/test.sparql -- keep the 'SPARQL' string at the beginning!):
# SPARQL PREFIX ohdsi:<http://purl.org/net/ohdsi#> PREFIX oa:<http://www.w3.org/ns/oa#> PREFIX meddra:<http://purl.bioontology.org/ontology/MEDDRA/> PREFIX ncbit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#> PREFIX foaf: <http://xmlns.com/foaf/0.1/> PREFIX linkedspls_vocabulary:<http://bio2rdf.org/linkedspls_vocabulary:>  SELECT count(distinct ?an) ?drug ?hoi ?sect FROM <http://purl.org/net/nlprepository/ohdsi-adr-splicer-poc> WHERE { ?an a ohdsi:ADRAnnotation; oa:hasBody ?body; oa:hasTarget ?target.  ?body ohdsi:ImedsDrug ?drug. ?body ohdsi:ImedsHoi ?hoi.  ?target oa:hasSelector ?sel. ?sel linkedspls_vocabulary:splSection ?sect. }


# replace the @IMEDS_DRUG@ and @IMEDS_HOI@ strings with the appropriate values
TEMPLATE = "http://dbmi-icode-01.dbmi.pitt.edu:8080/sparql?default-graph-uri=&query=%23+drill+down+query+for+a+drug+and+HOI+in+the+SPLICER+ADRAnnotation+graph+joined+with+LinkedSPLs%0D%0APREFIX+ohdsi%3A%3Chttp%3A%2F%2Fpurl.org%2Fnet%2Fohdsi%23%3E%0D%0APREFIX+oa%3A%3Chttp%3A%2F%2Fwww.w3.org%2Fns%2Foa%23%3E%0D%0APREFIX+meddra%3A%3Chttp%3A%2F%2Fpurl.bioontology.org%2Fontology%2FMEDDRA%2F%3E%0D%0APREFIX+ncbit%3A+%3Chttp%3A%2F%2Fncicb.nci.nih.gov%2Fxml%2Fowl%2FEVS%2FThesaurus.owl%23%3E%0D%0APREFIX+foaf%3A+%3Chttp%3A%2F%2Fxmlns.com%2Ffoaf%2F0.1%2F%3E%0D%0APREFIX+linkedspls_vocabulary%3A+%3Chttp%3A%2F%2Fbio2rdf.org%2Flinkedspls_vocabulary%3A%3E%0D%0A%0D%0ASELECT+*%0D%0AWHERE+{%0D%0A+GRAPH+%3Chttp%3A%2F%2Fpurl.org%2Fnet%2Fnlprepository%2Fohdsi-adr-splicer-poc%3E+{%0D%0A++%3Fan+a+ohdsi%3AADRAnnotation%3B%0D%0A+++oa%3AhasBody+%3Fbody%3B%0D%0A+++oa%3AhasTarget+%3Ftarget.%0D%0A%0D%0A+++%3Fbody+ohdsi%3AImedsDrug+ohdsi%3A@IMEDS_DRUG@.%0D%0A+++%3Fbody+ohdsi%3AImedsHoi+ohdsi%3A@IMEDS_HOI@.%0D%0A%0D%0A+++%3Ftarget+oa%3AhasSource+%3FsourceURL.%0D%0A+++%3Ftarget+oa%3AhasSelector+%3Fselector.%0D%0A%0D%0A+++%3Fselector+linkedspls_vocabulary%3AsplSection+%3Fsection.%0D%0A++}%0D%0A+GRAPH+%3Chttp%3A%2F%2Fpurl.org%2Fnet%2Fnlprepository%2Fspl-core%3E+{%0D%0A++%3Fspl+a+ncbit%3ALabel%3B%0D%0A+++foaf%3Ahomepage+%3FsourceURL%3B%0D%0A+++%3Fsection+%3Ftext.%0D%0A+}%0D%0A}%0D%0A&format=text%2Fhtml&timeout=0&debug=on"

f = open(DATAFILE)
buf = f.read()
f.close()
# TODO: this is a work around for a bug in the model. This will need to be fixed.
buf = buf.replace("http://purl.org/net/ohdsi#","").replace("http://purl.bioontology.org/ontology/MEDDRA/","").replace('"',"")
l = buf.split("\n") # assumes no header. Format should be count,drug,hoi

f = open(SQL_INSERT_OUTFILE,'w')
i = 0
pre = ""
for elt in l:
    i += 1
    # TODO: be more specific about how to terminate this loop!
    try:
        (cnt,drug,hoi) = [x.strip() for x in elt.split(",")]
    except ValueError:
        break
    q = TEMPLATE.replace("@IMEDS_DRUG@",drug).replace("@IMEDS_HOI@",hoi)
    url_id = URL_ID_PREFIX + str(i)
    if i > 1:
        pre = ",\n"
    f.write("%s('%s','%s',CURRENT_TIMESTAMP)" % (pre,url_id, q))
    turl = URL_PREFIX + url_id
    key = "%s-%s" % (drug,hoi)
    print "\t".join([key,EVTYPE,'positive',"2",str(cnt),turl,"COUNT"])
f.close()
