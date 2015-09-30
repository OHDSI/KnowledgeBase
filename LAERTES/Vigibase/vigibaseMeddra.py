# -*- coding: utf-8 -*-
# VigibaseMeddra.py
#
# Access to Vigibase® via a pilot REST API to pull drug/event pairs
# 
# Author: Richard D. Boyce, PhD

import json
import urllib2
import urllib
import traceback
import sys
import base64
import csv
import pprint
import time

# Connection information 
DB_CONNECTION_INFO="/home/likewise-open/ARCS/blm14/Downloads/db-connection.conf"
f = open(DB_CONNECTION_INFO,'r')
(client,user,clientkey,username,pw) = f.readline().strip().split("\t")
f.close()

pp = pprint.PrettyPrinter(indent=4)

def query(q_domain, q_params, userkey, clientkey, epr, f='application/json'):
    """Function that uses urllib/urllib2 to issue a SPARQL query.
       By default it requests json as data format for the SPARQL resultset"""

    try:
        params = urllib.urlencode(q_params)
        opener = urllib2.build_opener(urllib2.HTTPHandler)
        request = urllib2.Request(epr + q_domain + "?" + params)
        request.add_header('Accept', f)
        request.add_header('umc-client-key', clientkey)
        request.add_header('Authorization', " Basic " + userkey)
        request.get_method = lambda: 'GET'
        #print(request.get_full_url())
        url = opener.open(request)
        return url.read()
    except Exception, e:
        #traceback.print_exc()
        pass
        #raise e

if __name__ == "__main__":
    userkey = base64.b64encode("%s:%s" % (username,pw))
    service = "https://api.who-umc.org/vigibase/icsrstatistics/distributions"

    #Some sample query.
    query_domain = "/reactions"
    #query_domain = ""

    print "WHO Global ICSR database – VigiBase®"

    write_header=True

    item_keys = []

    json_data = []

    start_time = time.time()
    #query_params = {'substanceFilter':'mZXg5P2glyB6%2FMNxNZEj0w%3D%3D','reactionFilter':'10076087,10076088,10076089,10076090,10076091,10076092,10065484,10076096,10076097,10076098,10076099,10076100,10076101,10076102,10076103,10076104,10076105,10076106,10076107,10076108,10076109,10076110,10076111,10076112,10076113,10076114,10076115,10076116,10076117,10076118,10076119,10076120,10076121,10076122,10076123,10076124,10076125,10076126,10076127,10076128,10076129,10076130,10076131,10076132,10076133,10076134,10076135,10076136,10076137,10076138,10076139,10076140,10076141,10076142,10076143,10076144,10076145,10076146,10076147,10076148,10076155,10076156,10076157,10076158,10076159,10076160,10076161,10076162,10076163,10076164,10076165,10076166,10076167,10076168,10076169,10076170,10076171,10076172,10076173,10076174,10076175,10076176,10076177,10076178,10076179,10076180,10076181,10076182,10076183,10076184,10076185,10076186,10076187,10076188,10076189,10076190,10076191,10076192,10076199,10076202,10076203,10076204,10076205,10076206,10076211,10076215,10076216,10076217,10028561,10076222,10076223,10076224,10076227,10076229,10076230,10076233,10076235,10076236,10076237,10076238,10076239,10076240,10076241,10076242,10076245,10076246,10076247,10076248,10076249,10076251,10076253,10076254,10076255,10009243,10076260,10076265,10076266,10076267,10076268,10076269,10076270,10076271,10076272,10076273,10076278,10076279,10076280,10034099,10076286,10076287,10076288,10071400,10076299,10076300,10076301,10076302,10076308,10076309,10076310,10076311,10076312,10076313,10076327,10076328,10076329,10076330,10076331,10076338,10076339,10076360,10076362,10076367,10076368,10063769,10076370,10076371,10076372,10076373,10076374,10039906'}
    firstline=True

    meddra_arr = []
    with open('/home/likewise-open/ARCS/blm14/LAERTES/KnowledgeBase/LAERTES/Vigibase/pt.asc','rb') as meddra_f:
        meddra = csv.reader(meddra_f,delimiter='$')
        for m in meddra:
            meddra_arr.append(m[0])
    
    meddra_f.close()
    query_params={'substanceFilter':'mZXg5P2glyB6%2FMNxNZEj0w%3D%3D','reactionFilter':'10000060'}
    print('TEST params:');
    print(query_params)
    
    json_string = query(query_domain, query_params, userkey, clientkey, service)
    
    print('TEST json_string:')
    print(json_string)

    data=json.loads(json_string)
    print('TEST data:')
    pp.pprint(data)

    with open('/home/likewise-open/ARCS/blm14/LAERTES/KnowledgeBase/LAERTES/Vigibase/vigibasedrug.csv','rb') as tsvin,  open('output.csv','wb',0) as out:
        tsvin = csv.reader(tsvin,delimiter='\t')
        out.write('rxnorm_id\tvigibase_id\tvigibase_desc\tmeddra_code\vigibase_observations\n')
        for drug in tsvin:
            #ignore header row
            if firstline:
                firstline = False
                continue
            for m in meddra_arr:
                query_params={'substanceFilter':drug[1],'reactionFilter':str(m)}
                print('params:');
                print(query_params)

                json_string = query(query_domain, query_params, userkey, clientkey, service)

                print('json_string:')
                print(json_string)
                observations = '0'
                try:
                    data=json.loads(json_string)
                    print('data:')
                    pp.pprint(data)

                    if len(data['Observations']) > 0:
                        observations=str(data['Observations'][0]['NumberOfReports'])
                except:
                    pass

                out.write(drug[0] + '\t' + drug[1] + '\t' + drug[2] + '\t' + m + '\t' + observations)

                out.write('\n')
                out.flush()
    end_time = time.time()
    print("--- %s seconds ---" % (end_time - start_time))
