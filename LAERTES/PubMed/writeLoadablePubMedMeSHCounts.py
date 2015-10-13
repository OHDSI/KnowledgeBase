# writeRelation.py
#
# Write a summary and index of pubmed drug-hoi data identified by mesh indexing
#
# Author: Richard D Boyce, PhD
# 2014
#

import urllib2, urllib, re, sys

DATAFILE = "pubmed-graph-count-query-10092015.txt"
EVTYPE = "MEDLINE_MeSH"
URL_ID_PREFIX = "pm-mesh-"
URL_PREFIX = "http://dbmi-icode-01.dbmi.pitt.edu/l/index.php?id="
SQL_INSERT_OUTFILE = "insertShortURLs-ALL.txt"

## count data retrieved from the Virtuoso SPARQL endpoint using the
## following  query. 
##
## NOTE: that the ohdsi:MeddrraHoi is misleading because its actually
## the HOI concept code from OMOP.
##
## NOTE: run the query using the following isql command because
## queries from curl or the virtuoso sparql web form truncate the
## results:
##
## $ isql-vt -H localhost -S 1111  -U <user name> -P <password> errors=stdout < /tmp/test.sparql > /tmp/test.out
## $ egrep "^[0-9]+ +http.*" /tmp/test.out | sed 's/.(/\_(/g' | sed 's/.type/\_type/g' | sed 's/e r/e_r/g' | sed 's/l t/l_t/g' | tr -s '  *' ',' > sample-summary-query.txt
##
## QUERY (paste into /tmp/test.sparql):
# SPARQL PREFIX ohdsi:<http://purl.org/net/ohdsi#> PREFIX oa:<http://www.w3.org/ns/oa#> PREFIX meddra:<http://purl.bioontology.org/ontology/MEDDRA/> PREFIX ncbit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#> PREFIX foaf: <http://xmlns.com/foaf/0.1/> PREFIX poc: <http://purl.org/net/nlprepository/ohdsi-pubmed-mesh-poc#>  SELECT count(distinct ?an) ?drug ?hoi ?studyType  FROM <http://purl.org/net/nlprepository/ohdsi-pubmed-mesh-poc> WHERE {       ?an a ohdsi:PubMedDrugHOIAnnotation;               oa:hasTarget ?target;           oa:hasBody ?body.           ?target ohdsi:MeshStudyType ?studyType.            {?body ohdsi:ImedsDrug ?drug.}    UNION        {?body ohdsi:adeAgents ?agents.          ?agents ohdsi:ImedsDrug ?drug.       }          {?body ohdsi:ImedsHoi ?hoi.}        UNION    {?body ohdsi:adeEffects ?effects.          ?effects ohdsi:ImedsHoi ?hoi.    }  };

## The old query (deprecated)
# PREFIX ohdsi:<http://purl.org/net/ohdsi#> PREFIX oa:<http://www.w3.org/ns/oa#> PREFIX meddra:<http://purl.bioontology.org/ontology/MEDDRA/> PREFIX ncbit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#> PREFIX foaf: <http://xmlns.com/foaf/0.1/> PREFIX dailymed:<http://dbmi-icode-01.dbmi.pitt.edu/linkedSPLs/vocab/resource/>  SELECT count(distinct ?an) ?drug ?hoi ?studyType FROM <http://purl.org/net/nlprepository/ohdsi-pubmed-mesh-poc> WHERE {  ?an a ohdsi:PubMedDrugHOIAnnotation;    oa:hasBody ?body;    oa:hasTarget ?target.   ?body ohdsi:ImedsDrug ?drug.  ?body ohdsi:ImedsHoi ?hoi.  ?target ohdsi:MeshStudyType ?studyType.  };

############################################################


# replace the @IMEDS_DRUG@, @IMEDS_HOI@, @STUDY_TYPE@ strings with the appropriate values
TEMPLATE = "http://virtuoso.ohdsi.org:8890/sparql?default-graph-uri=&query=PREFIX+ohdsi%3A%3Chttp%3A%2F%2Fpurl.org%2Fnet%2Fohdsi%23%3E+%0D%0APREFIX+oa%3A%3Chttp%3A%2F%2Fwww.w3.org%2Fns%2Foa%23%3E+%0D%0APREFIX+meddra%3A%3Chttp%3A%2F%2Fpurl.bioontology.org%2Fontology%2FMEDDRA%2F%3E+%0D%0APREFIX+ncbit%3A+%3Chttp%3A%2F%2Fncicb.nci.nih.gov%2Fxml%2Fowl%2FEVS%2FThesaurus.owl%23%3E+%0D%0APREFIX+foaf%3A+%3Chttp%3A%2F%2Fxmlns.com%2Ffoaf%2F0.1%2F%3E+%0D%0APREFIX+poc%3A+%3Chttp%3A%2F%2Fpurl.org%2Fnet%2Fnlprepository%2Fohdsi-pubmed-mesh-poc%23%3E++%0D%0A%0D%0ASELECT+count%28distinct+%3Fan%29+%3Fpmid+%3Fexact%0D%0AFROM+%3Chttp%3A%2F%2Fpurl.org%2Fnet%2Fnlprepository%2Fohdsi-pubmed-mesh-poc%3E%0D%0AWHERE+%7B%0D%0A++%3Fan+a+ohdsi%3APubMedDrugHOIAnnotation%3B++++%0D%0A++++oa%3AhasTarget+%3Ftarget%3B%0D%0A++++oa%3AhasBody+%3Fbody.%0D%0A%0D%0A++%3Ftarget+ohdsi%3AMeshStudyType+@STUDY_TYPE@%3B%0D%0A+++++++++oa%3AhasSource+%3Fpmid%3B%0D%0A+++++++++oa%3AhasSelector+%3Fsel.%0D%0A++%3Fsel+oa%3Aexact+%3Fexact.%0D%0A%0D%0A++%7B%3Fbody+ohdsi%3AImedsDrug+ohdsi%3A@IMEDS_DRUG@.%7D+%0D%0A++UNION+%0D%0A++%7B%0D%0A++++%3Fbody+ohdsi%3AadeAgents+%3Fagents.%0D%0A++++%3Fagents+ohdsi%3AImedsDrug+ohdsi%3A@IMEDS_DRUG@.%0D%0A++%7D%0D%0A%0D%0A++%7B%3Fbody+ohdsi%3AImedsHoi+ohdsi%3A@IMEDS_HOI@.%7D+%0D%0A++UNION+%0D%0A++%7B%0D%0A++++%3Fbody+ohdsi%3AadeEffects+%3Feffects.%0D%0A++++%3Feffects+ohdsi%3AImedsHoi+ohdsi%3A@IMEDS_HOI@.%0D%0A++%7D%0D%0A%7D&format=application%2Fsparql-results%2Bjson&timeout=0&debug=on"

f = open(DATAFILE)
buf = f.read()
f.close()
buf = buf.replace("http://purl.org/net/ohdsi#","").replace("http://purl.bioontology.org/ontology/MEDDRA/","").replace('"',"").replace("_"," ")
l = buf.split("\n") # assumes no header. Format should be count,drug,hoi, study type

f = open(SQL_INSERT_OUTFILE,'w')
i = 0
pre = ""
for elt in l:
    if not elt:
        break

    i += 1
    (cnt,drug,hoi,pubType) = [x.strip() for x in elt.split(",")]
    escapedPubType = "%22" + pubType.replace("(","%28").replace(")","%29") + "%22"

    q = TEMPLATE.replace("@IMEDS_DRUG@",drug).replace("@IMEDS_HOI@",hoi).replace("@STUDY_TYPE@",escapedPubType)
    url_id = URL_ID_PREFIX + str(i)
    if i > 1:
        pre = ",\n"
    f.write("%s('%s','%s',CURRENT_TIMESTAMP)" % (pre,url_id, q))
    turl = URL_PREFIX + url_id

    key = "%s-%s" % (drug,hoi)
    if pubType == 'clinical trial (publication type)':
        print "\t".join([key,EVTYPE + "_ClinTrial",'positive',"7",str(cnt),turl,"COUNT"])
    elif pubType == 'case reports (publication type)':
        print "\t".join([key,EVTYPE + "_CR",'positive',"6",str(cnt),turl,"COUNT"])
    elif pubType == 'other (publication type)':
        print "\t".join([key,EVTYPE + "_Other",'positive',"8",str(cnt),turl,"COUNT"])
    else:
        print "Not continuing because there is a record with un-recognized publication type: %s" % pubType
        sys.exit(1)
f.close()        
