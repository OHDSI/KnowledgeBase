# writeLoadableSemMedDbCounts.py
#
# Write a summary and index of SemMedDB drug-hoi data 
#
# Author: Richard D Boyce, PhD
# 2014/2015
#

import urllib2, urllib, re, sys

DATAFILE = "sample-summary-query-10092015.txt"
EVTYPE = "MEDLINE_SemMedDB"
URL_ID_PREFIX = "pm-semmed-"
URL_PREFIX = "http://dbmi-icode-01.dbmi.pitt.edu/l/index.php?id="
SQL_INSERT_OUTFILE = "insertShortURLs-ALL.txt"

## count data retrieved from the Virtuoso SPARQL endpoint using the
## following  query. 
##
##
## NOTE: run the query using the following isql command because
## queries from curl or the virtuoso sparql web form truncate the
## results:
##
## $ isql-vt -H localhost -S 1111  -U <user name> -P <password> errors=stdout < /tmp/test.sparql > /tmp/test.out
## $ egrep "^[0-9]+ +.*publication type.*" /tmp/test.out | sed -n 's/  \+/\t/gp' > sample-summary-query.txt
##
## QUERY (paste into /tmp/test.sparql):
# SPARQL PREFIX ohdsi:<http://purl.org/net/ohdsi#>  PREFIX oa:<http://www.w3.org/ns/oa#>  PREFIX meddra:<http://purl.bioontology.org/ontology/MEDDRA/>  PREFIX ncbit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>  PREFIX foaf: <http://xmlns.com/foaf/0.1/>  PREFIX poc: <http://purl.org/net/nlprepository/ohdsi-pubmed-semmed-poc#>    SELECT count(distinct ?an) ?drug ?hoi ?modality ?studyType FROM <http://purl.org/net/nlprepository/ohdsi-pubmed-semmed-poc> WHERE {   ?an a ohdsi:SemMedDrugHOIAnnotation;         oa:hasTarget ?target;     oa:hasBody ?body.    ?target ohdsi:MeshStudyType ?studyType.    ?body poc:modality ?modality.    {?body ohdsi:ImedsDrug ?drug.}    UNION    {     ?body ohdsi:adeAgents ?agents.     ?agents ohdsi:ImedsDrug ?drug.   }    {?body ohdsi:ImedsHoi ?hoi.}    UNION    {     ?body ohdsi:adeEffects ?effects.     ?effects ohdsi:ImedsHoi ?hoi.   } };
############################################################


# replace the @SV_DRUG@, @SV_HOI@, @MODALITY@, @STUDY_TYPE@ strings with the appropriate values
TEMPLATE = "http://virtuoso.ohdsi.org:8890/sparql?default-graph-uri=&query=PREFIX+ohdsi%3A%3Chttp%3A%2F%2Fpurl.org%2Fnet%2Fohdsi%23%3E+%0D%0APREFIX+oa%3A%3Chttp%3A%2F%2Fwww.w3.org%2Fns%2Foa%23%3E+%0D%0APREFIX+meddra%3A%3Chttp%3A%2F%2Fpurl.bioontology.org%2Fontology%2FMEDDRA%2F%3E+%0D%0APREFIX+ncbit%3A+%3Chttp%3A%2F%2Fncicb.nci.nih.gov%2Fxml%2Fowl%2FEVS%2FThesaurus.owl%23%3E+%0D%0APREFIX+foaf%3A+%3Chttp%3A%2F%2Fxmlns.com%2Ffoaf%2F0.1%2F%3E+%0D%0APREFIX+poc%3A+%3Chttp%3A%2F%2Fpurl.org%2Fnet%2Fnlprepository%2Fohdsi-pubmed-semmed-poc%23%3E++%0D%0A%0D%0ASELECT+count%28distinct+%3Fan%29+%3FpredicateLab+%3Fpmid+%3Fexact+%3Fprefix+%3Fpostfix%0D%0AFROM+%3Chttp%3A%2F%2Fpurl.org%2Fnet%2Fnlprepository%2Fohdsi-pubmed-semmed-poc%3E%0D%0AWHERE+{%0D%0A++%3Fan+a+ohdsi%3ASemMedDrugHOIAnnotation%3B++++%0D%0A++++oa%3AhasTarget+%3Ftarget%3B%0D%0A++++oa%3AhasBody+%3Fbody.%0D%0A%0D%0A++%3Ftarget+ohdsi%3AMeshStudyType+@STUDY_TYPE@%3B%0D%0A+++++++++oa%3AhasSource+%3Fpmid%3B%0D%0A+++++++++oa%3AhasSelector+%3Fsel.%0D%0A++%3Fsel+oa%3Aexact+%3Fexact.%0D%0A++OPTIONAL+{%0D%0A+++++%3Fsel+oa%3Aprefix+%3Fprefix.%0D%0A++}%0D%0A++OPTIONAL+{%0D%0A+++++%3Fsel+oa%3Apostfix+%3Fpostfix.%0D%0A++}%0D%0A%0D%0A++%3Fbody+poc%3Amodality+%22@MODALITY@%22%3B%0D%0A++++++++poc%3AsemanticNetworkPredicate+%3Fpredicate.%0D%0A++%3Fpredicate+rdfs%3Alabel+%3FpredicateLab.%0D%0A%0D%0A++{%3Fbody+ohdsi%3AImedsDrug+ohdsi%3A@SV_DRUG@.}+%0D%0A++UNION+%0D%0A++{%0D%0A++++%3Fbody+ohdsi%3AadeAgents+%3Fagents.%0D%0A++++%3Fagents+ohdsi%3AImedsDrug+ohdsi%3A@SV_DRUG@.%0D%0A++}%0D%0A%0D%0A++{%3Fbody+ohdsi%3AImedsHoi+ohdsi%3A@SV_HOI@.}+%0D%0A++UNION+%0D%0A++{%0D%0A++++%3Fbody+ohdsi%3AadeEffects+%3Feffects.%0D%0A++++%3Feffects+ohdsi%3AImedsHoi+ohdsi%3A@SV_HOI@.%0D%0A++}%0D%0A}&format=json&timeout=0&debug=on"


f = open(DATAFILE)
buf = f.read()
f.close()
l = buf.split("\n") 

f = open(SQL_INSERT_OUTFILE,'w')
i = 0
pre = "INSERT INTO lil_urls VALUES "
for elt in l:
    if not elt:
        break

    i += 1
    (cnt,drug,hoi,modality,pubType) = [x.strip() for x in elt.split("\t")]
    drug = drug.replace("http://purl.org/net/ohdsi#","")
    hoi = hoi.replace("http://purl.org/net/ohdsi#","")
    escapedPubType = "%22" + pubType.replace("(","%28").replace(")","%29") + "%22"

    q = TEMPLATE.replace("@SV_DRUG@",drug).replace("@SV_HOI@",hoi).replace("@STUDY_TYPE@",escapedPubType).replace("@MODALITY@",modality)
    url_id = URL_ID_PREFIX + str(i)
    if i > 1:
        pre = ",\n"
    f.write("%s('%s','%s',CURRENT_TIMESTAMP)" % (pre,url_id, q))
    turl = URL_PREFIX + url_id

    key = "%s-%s" % (drug,hoi)
    if pubType == 'case reports (publication type)':
        print "\t".join([key,EVTYPE + "_CR",modality,"9",str(cnt),turl,"COUNT"])
    elif pubType == 'clinical trial (publication type)':
        print "\t".join([key,EVTYPE + "_ClinTrial",modality,"10",str(cnt),turl,"COUNT"])
    elif pubType == 'other (publication type)':
        print "\t".join([key,EVTYPE + "_Other",modality,"11",str(cnt),turl,"COUNT"])
    else:
        print "Not continuing because there is a record with un-recognized publication type: %s" % pubType
        sys.exit(1)
f.close()        
