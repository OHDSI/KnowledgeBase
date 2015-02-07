# writeLoadableEUSPCcounts.py
#
# Write a summary and index of EU SPC drug-hoi data 
#
# Author: Richard D Boyce, PhD
# Summer/Fall 2014
#
import urllib2, urllib, re, sys

DATAFILE = "test-query-of-counts-10272014.csv" # NOTE: this data comes a CSV export of the following query
## count data retrieved from the EU SPC graph in the SPARQL endpoint
## (http://dbmi-icode-01.dbmi.pitt.edu:8080/sparql) using the
## following query. 
# PREFIX ohdsi:<http://purl.org/net/ohdsi#>
# PREFIX oa:<http://www.w3.org/ns/oa#>
# PREFIX meddra:<http://purl.bioontology.org/ontology/MEDDRA/>
# PREFIX ncbit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
# PREFIX foaf: <http://xmlns.com/foaf/0.1/>
# PREFIX dailymed:<http://dbmi-icode-01.dbmi.pitt.edu/linkedSPLs/vocab/resource/>

# SELECT count(distinct ?an) ?drug ?hoi 
# FROM <http://purl.org/net/nlprepository/ohdsi-adr-eu-spc-poc>
# WHERE {
#  ?an a ohdsi:ADRAnnotation;
#    oa:hasBody ?body;
#    oa:hasTarget ?target.

#  ?body ohdsi:ImedsDrug ?drug.
#  ?body ohdsi:ImedsHoi ?hoi. 

# }

EVTYPE = "SPL_EU_SPC"

# simple function to retrieve custom tiny urls
def query(q,service):
    """Function that uses urllib/urllib2  query for a shortened url"""

    try:
        params = {'longurl': q}
        params = urllib.urlencode(params)
        opener = urllib2.build_opener(urllib2.HTTPHandler)
        request = urllib2.Request(service, params)
        request.get_method = lambda: 'POST'
        url = opener.open(request)
        return url.read()
    except Exception, e:
        traceback.print_exc(file=sys.stdout)
        raise e


def shortenURL(longurl):
    result = query(longurl, "http://dbmi-icode-01.dbmi.pitt.edu/l/index.php")

    rgx = re.compile('''<p class="success">URL is: <a href="(.*)">''')
    urlL = rgx.findall(result)
    if len(urlL) == 0:
        print "ERROR: could not retrieve short URL for longurl %s" % longurl
        return None
    else:
        return urlL[0]

# replace the @IMEDS_DRUG@ and @IMEDS_HOI@ strings with the appropriate values
TEMPLATE = "http://dbmi-icode-01.dbmi.pitt.edu:8080/sparql?default-graph-uri=&query=PREFIX+ohdsi%3A%3Chttp%3A%2F%2Fpurl.org%2Fnet%2Fohdsi%23%3E%0D%0APREFIX+oa%3A%3Chttp%3A%2F%2Fwww.w3.org%2Fns%2Foa%23%3E%0D%0APREFIX+meddra%3A%3Chttp%3A%2F%2Fpurl.bioontology.org%2Fontology%2FMEDDRA%2F%3E%0D%0APREFIX+ncbit%3A+%3Chttp%3A%2F%2Fncicb.nci.nih.gov%2Fxml%2Fowl%2FEVS%2FThesaurus.owl%23%3E%0D%0APREFIX+foaf%3A+%3Chttp%3A%2F%2Fxmlns.com%2Ffoaf%2F0.1%2F%3E%0D%0APREFIX+dailymed%3A%3Chttp%3A%2F%2Fdbmi-icode-01.dbmi.pitt.edu%2FlinkedSPLs%2Fvocab%2Fresource%2F%3E%0D%0A%0D%0ASELECT+*+%0D%0AWHERE+{%0D%0A+GRAPH+%3Chttp%3A%2F%2Fpurl.org%2Fnet%2Fnlprepository%2Fohdsi-adr-eu-spc-poc%3E{%0D%0A++%3Fan+a+ohdsi%3AADRAnnotation%3B%0D%0A++++oa%3AhasBody+%3Fbody%3B%0D%0A++++oa%3AhasTarget+%3Ftarget.%0D%0A%0D%0A++%3Fbody+ohdsi%3AImedsDrug+ohdsi%3A@IMEDS_DRUG@.%0D%0A++%3Fbody+ohdsi%3AImedsHoi+ohdsi%3A@IMEDS_HOI@.+%0D%0A+}%0D%0A}&format=text%2Fhtml&timeout=0&debug=on"


f = open(DATAFILE)
buf = f.read()
f.close()
l = buf.split("\n")[1:]

i = 0
for elt in l:
    i += 1
    (cnt,drug,hoi) = [x.strip() for x in elt.split(",")]
    q = TEMPLATE.replace("@IMEDS_DRUG@",drug).replace("@IMEDS_HOI@",hoi)
    turl = shortenURL(q)
    if turl == None:
        print "Not continuing because of error shortening the URL for the drill down query"
        sys.exit(1)

    key = "%s-%s" % (drug,hoi)
    print "\t".join([key,EVTYPE,'positive',"1",str(cnt),turl,"COUNT"])

