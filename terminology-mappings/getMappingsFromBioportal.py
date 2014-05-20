## getMappingsFromBioportal.py
#
#
# Python script to query http://sparql.bioontology.org/mappings/sparql
# for mappings between various terminologies. See
# http://www.bioontology.org/wiki/index.php/BioPortal_Mappings for
# further explanation.
#
# Author: Richard D Boyce - University of Pittsburgh

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

BIOPORTAL_PURL = "http://purl.bioontology.org/ontology"
MESH = "MSH"
MEDDRA = "MDR"

def query(q,apikey,epr,f='application/json'):
    """Function that uses urllib/urllib2 to issue a SPARQL query.
       By default it requests json as data format for the SPARQL resultset"""

    try:
        params = {'query': q, 'apikey': apikey}
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

if __name__ == "__main__":
    sparql_service = " http://sparql.bioontology.org/mappings/sparql"

    print "SPARQL service initialized..."

    #To get your API key register at http://bioportal.bioontology.org/accounts/new
    api_key = "74028721-e60e-4ece-989b-1d2c17d14e9c"


    ## TODO: make the input a file and a command line paramater specifying the terminology so that this script is more general
    sl = ["D054198","D002658","D003924","D020936","D006948","D029593","D009422","D029597","D019969","D002277","D008175","D008223","D015674","D029424","D011656","D058186","D001169","D002289","D002318","D018450","D056486","D064420","D004827","D007024","D007676","D008106","D009325","D010149","D014178","D000505","D006973","D007938","D011471","D006528","C535575","D002543","D015179","D017449","D004487","D004938","D008545","D012163","D013226","C562942","D001284","D001930","D001932","D001943","D002294","D002471","D020256","D016510","C536830","D003928","D003930","D016889","D005909","D005911","D006394","D008607","D015473","D008103","D008569","D015428","D009362","D009374","D009410","D011833","D012164","D012208","D012559","D012878","D054058","D000230","C538231","D000544","D000740","D015535","D001238","D001321","D001327","D002056","D018376","D015209","D003110","D004381","C562729","D005334","D005923","D006333"]

    ## TODO: make the term filter depend on a command line paramater specifying the terminology so that this script is more general
    termFilter = "%s/%s" % (BIOPORTAL_PURL,MEDDRA) 

    for s in sl:
        ## TODO: make the input a file and a command line paramater specifying the terminology so that this script is more general
        sourceUrl = "<%s/%s/%s>" % (BIOPORTAL_PURL,MESH,s)
        query_string = """ 
PREFIX maps: <http://protege.stanford.edu/ontologies/mappings/mappings.rdfs#>
SELECT DISTINCT * WHERE {
   ?s maps:source %s;
      maps:target ?target. } 
""" % (sourceUrl)

        print "query_string: %s" % query_string
        json_string = query(query_string, api_key, sparql_service)
        resultset=json.loads(json_string)

        if len(resultset["results"]["bindings"]) == 0:
            print "INFO: No result for %s" % sourceUrl
        else:
            print "INFO: %d results for %s; showing PURL for each unique result" % (len(resultset["results"]["bindings"]), sourceUrl)
            cache = []
            for i in range(0, len(resultset["results"]["bindings"])):
                if resultset["results"]["bindings"][i]["target"]["value"] in cache:
                    continue

                target = resultset["results"]["bindings"][i]["target"]["value"]
                if target.find(termFilter) != -1:
                    print "RESULT: %s	%s"  % (sourceUrl, target)

                cache.append(resultset["results"]["bindings"][i]["target"]["value"])

## TODO: pretty print the results to a file
