# Simple Python script to query CTD for drug adverse events
#
# No extra libraries required.

# Authors: Richard D Boyce and Vojtech Huser
#
# May 2014
#

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import urllib2
import urllib
import traceback
import sys 
import pickle
import codecs

sys.path = sys.path + ['.']

#############  GLOBALS ###################################################################

CTD_SPARQL = "http://s4.semanticscience.org:14004/sparql"

LOG_FILE = "ctd_gov_queryresults.log"
OUT_FILE = "ctd__gov_queryresults.tsv"
PICKLE_FILE = "ctd_gov_queryresults.pickle" # a python data structure containing the results will be stored


drugsF = "drugsToSearch.txt"
HOIsF = "HOIsToSearch.txt"

## ADJUST THE OFFSETS AND LIMITS IF THE RESULT SETS ARE VERY LARGE
offset = 0
maxoffset = 20000
limit = 5000

############## QUERY  ##################################################################
def getQueryString(drug, HOI, offset, limit):
    return """ 
SELECT ?url ?article ?label
WHERE {
 ?url a <http://bio2rdf.org/ctd_vocabulary:Chemical-Disease-Association>;
   <http://bio2rdf.org/ctd_vocabulary:disease> <http://bio2rdf.org/mesh:%s>;
   <http://bio2rdf.org/ctd_vocabulary:chemical>  <http://bio2rdf.org/mesh:%s>;
   <http://bio2rdf.org/ctd_vocabulary:article> ?article;
   <http://www.w3.org/2000/01/rdf-schema#label> ?label.
}
OFFSET %d
LIMIT %d

""" % (HOI, drug, offset, limit)


def getCTDDict():
    """A dictionary to hold selected data from CTD"""
    d = {
        "HOI_MESH":None,
        "HOI_MEDDRA":None,
        "chemical_MESH":None,
        "chemical_RXNORM":None,
        "article":None,
        "label":None,
        "url":None,
        "dataSource":None
      }

    return d

def createCTD(qResult, drug, HOI, sparql_service):
    newCTD = getCTDDict()
    newCTD["dataSource"] = sparql_service
    newCTD["HOI_MESH"] = HOI
    newCTD["chemical_MESH"] = drug
    newCTD["url"] = qResult["url"]["value"]
    newCTD["article"] = qResult["article"]["value"]
    newCTD["label"] = qResult["label"]["value"]
       
    return newCTD


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
    
    f = open(drugsF, "r")
    buf = f.read()
    f.close()
    drugDataList = buf.strip().split("\n")
    drugD = {}
    for elt in drugDataList[1:]: # skip first line
        (rxnorm,mesh,label) = [x.strip() for x in elt.split("|")]
        if not drugD.has_key(mesh):
            drugD[mesh] = (rxnorm,label)

    f = open(HOIsF, "r")
    buf = f.read()
    f.close()
    HOIDataList = buf.strip().split("\n")
    HOID = {}
    for elt in HOIDataList[1:]: # skip first line
        (mesh,meddra) = [x.strip() for x in elt.split("|")]
        if not HOID.has_key(mesh):
            HOID[mesh] = meddra

    ctD = {}
    sparql_service = CTD_SPARQL

    colLabs = ["url", "HOI_MESH", "HOI_MEDDRA", "chemical_MESH", "chemical_RXNORM", "article", "label", "dataSource"]
   
    for drugSymbol in drugD.keys():
        for HOISymbol in HOID.keys():
            logf.write("\nINFO: trying drug %s and HOI %s\n" % (drugSymbol,HOISymbol))
            q = getQueryString(drugSymbol, HOISymbol, offset, limit) 
            resultset = queryEndpoint(sparql_service, q)

            if len(resultset["results"]["bindings"]) == 0:
                logf.write("\nINFO: no results for drug %s and HOI %s\n" % (drugSymbol,HOISymbol))
                continue
        
            goFlag = True
            while len(resultset["results"]["bindings"]) != 0 and goFlag:

                # print json.dumps(resultset,indent=1) # you can dump the results as JSON if needed
                for i in range(0, len(resultset["results"]["bindings"])):
                    qResult = resultset["results"]["bindings"][i]
                    newCT = createCTD(qResult, drugSymbol, HOISymbol, sparql_service)

                    newCT["HOI_MEDDRA"] = HOID[newCT["HOI_MESH"]]
                    
                    if drugD.has_key(newCT["chemical_MESH"]):
                        newCT["chemical_RXNORM"] = drugD[newCT["chemical_MESH"]][0]

                    dKey = "%s-%s" % (drugSymbol,HOISymbol)
                    if not ctD.has_key(dKey):
                        ctD[dKey] = [newCT]
                    else:
                        ctD[dKey].append(newCT)

                    logf.write("\nRESULT: %s" % dKey)
                    for key in colLabs:
                        logf.write("\t%s" % newCT[key])
                    
                    if len(resultset["results"]["bindings"]) == limit and offset < maxoffset:
                        offset += limit
                        q = getQueryString(drugSymbol, HOISymbol, offset, limit)
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
        logf.write("\n%d records found for drug %s and HOI %s" % (len(v),k.split("-")[0],k.split("-")[1]))

    logf.write("\nmapping data saved to %s" % pickleF)
        
    # write tab delimitted output
    outf.write("%s\n" % "\t".join(["key"] + colLabs))
    for k,v in ctD.iteritems():
        for elt in v:
            outf.write("%s" % k)
            for key in colLabs:
                outf.write("\t%s" % elt[key])
            outf.write("\n")

    logf.close()
    outf.close()

        

