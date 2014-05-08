""" Simple Python script to query ClinicalTrials.gov for drug adverse events"
    No extra libraries required.

# Authors: Richard D Boyce and Vojtech Huser
#
# May 2014
# 

"""

import json
import urllib2
import urllib
import traceback
import sys 
import pickle
import codecs

sys.path = sys.path + ['.']

#############  GLOBALS ###################################################################

CT_SPARQL = "http://s2.semanticscience.org:12050/sparql"

LOG_FILE = "ct_gov_queryresults.log"
OUT_FILE = "ct_gov_queryresults.tsv"
PICKLE_FILE = "ct_gov_queryresults.pickle" # where a python data structure containing the results will be stored


drugs = "drugsToSearch.txt"
HOIs = "HOIsToSearch.txt"

## ADJUST THE OFFSETS AND LIMITS IF THE RESULT SETS ARE VERY LARGE
offset = 0
maxoffset = 20000
limit = 5000

############## QUERY  ##################################################################
def getQueryString(drug, offset, limit):
    return """ 
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX ct: <http://bio2rdf.org/clinicaltrials:>
PREFIX ctv: <http://bio2rdf.org/clinicaltrials_vocabulary:>

SELECT ?trialURI ?trialLabel ?completionDate ?interventionURI ?conditionURI ?conditionLabel
WHERE {
  ?interventionURI dct:title "%s"@en.

  ?trialURI a ctv:Clinical-Study;
     ctv:intervention ?interventionURI;
     rdfs:label ?trialLabel;
     ctv:condition ?conditionURI; 
     ctv:completion-date ?completionDate.

  ?conditionURI rdfs:label ?conditionLabel. 
}
OFFSET %d
LIMIT %d

""" % (drug, offset, limit)

def getTrialDict():
    """A dictionary to hold selected data about at clinical trial"""
    d = {
        "trialLabel":None,
        "trialURI":None,
        "interventionLabel":None,
        "interventionURI":None,
        "conditionLabel":None,
        "conditionURI":None,
        "completionDate":None,        
        "dataSource":None
      }

    return d

def createTrialDrugIntervention(qResult, drug, sparql_service):
    newTrial = getTrialDict()
    newTrial["dataSource"] = sparql_service
    newTrial["trialLabel"] = qResult["trialLabel"]["value"]
    newTrial["trialURI"] = qResult["trialURI"]["value"]
    newTrial["interventionLabel"] = drug
    newTrial["interventionURI"] = qResult["interventionURI"]["value"]
    newTrial["conditionLabel"] = qResult["conditionLabel"]["value"]
    newTrial["conditionURI"] = qResult["conditionURI"]["value"]
    newTrial["completionDate"] = qResult["completionDate"]["value"]
       
    return newTrial


############## SPARQL FUNCTIONS  ##################################################################
def query(q,epr,f='application/json'):
    """Function that uses urllib/urllib2 to issue a SPARQL query.
       By default it requests json as data format for the SPARQL resultset"""

    try:
        params = {'query': q}
        params = urllib.urlencode(params)
        opener = urllib2.build_opener(urllib2.HTTPHandler)
        request = urllib2.Request(epr+'?'+params)
        request.add_header('Accept', f)
        request.get_method = lambda: 'GET'
        url = opener.open(request)
        return url.read()
    except Exception, e:
        traceback.print_exc(file=sys.stdout)
        raise e


def queryEndpoint(sparql_service, q):
    print "query string: %s" % q
    json_string = query(q, sparql_service)
    #print "%s" % json_string
    resultset=json.loads(json_string)
    
    return resultset

########### MAIN  #####################################################################

if __name__ == "__main__":

    logf = codecs.open(LOG_FILE,'w','utf-8')
    outf = codecs.open(OUT_FILE,'w','utf-8')

    drugList = ["Omalizumab"]
    
    ## ALTERNATIVELY, WRITE DRUGS TO FILE
    # f = open(drugF, "r")
    # buf = f.read()
    # f.close()
    # drugList = buf.strip().split(";")

    ctD = {}
    sparql_service = CT_SPARQL

   
    for drugSymbol in drugList:
        logf.write("INFO: trying symbol %s\n" % drugSymbol)
        q = getQueryString(drugSymbol, offset, limit) 
        resultset = queryEndpoint(sparql_service, q)

        if len(resultset["results"]["bindings"]) == 0:
            logf.write("INFO: no results for drug %s" % drugSymbol)
            continue
        
        goFlag = True
        while len(resultset["results"]["bindings"]) != 0 and goFlag:

            # print json.dumps(resultset,indent=1) # you can dump the results as JSON if needed
            for i in range(0, len(resultset["results"]["bindings"])):
                qResult = resultset["results"]["bindings"][i]
                newCT = createTrialDrugIntervention(qResult, drugSymbol, sparql_service)
            
                if not ctD.has_key(drugSymbol):
                    ctD[drugSymbol] = [newCT]
                else:
                    ctD[drugSymbol].append(newCT)
                    
            if len(resultset["results"]["bindings"]) == offset:
                offset += offset
                q = getQueryString(drugSymbol, offset, limit)
                resultset = queryEndpoint(sparql_service, q)
            else:
                goFlag = False

    # serialize the results 
    pickleF = PICKLE_FILE
    f = open(pickleF,"w")
    pickle.dump(ctD, f)
    f.close()

    # write a summary to log
    for k,v in ctD.iteritems():
        logf.write("%d trials found for drug %s" % (len(v),k))

    logf.write("mapping data saved to %s" % pickleF)
        
    # write tab delimitted output
    outf.write("%s\n" % "\t".join(["drug"] + getTrialDict().keys()))
    for k,v in ctD.iteritems():
        for elt in v:
            outf.write("%s" % k)
            for key in getTrialDict().keys():
                outf.write("\t%s" % elt[key])
            outf.write("\n")

    logf.close()
    outf.close()

        

