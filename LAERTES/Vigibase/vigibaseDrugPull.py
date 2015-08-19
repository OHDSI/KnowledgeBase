# -*- coding: utf-8 -*-
# VigibaseTestQuery.py
#
# Test access to Vigibase® via a pilot REST API
# 
# Author: Richard D. Boyce, PhD

import json
import urllib2
import urllib
import traceback
import sys
import base64
import csv

# Connection information 
DB_CONNECTION_INFO="/home/likewise-open/ARCS/blm14/Downloads/db-connection.conf"
f = open(DB_CONNECTION_INFO,'r')
(client,user,clientkey,username,pw) = f.readline().strip().split("\t")
f.close()


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
    service = "https://api.who-umc.org/vigibase/icsrstatistics/dimensions/"

    #Some sample query.
    query_domain = "drug"

    print "WHO Global ICSR database – VigiBase®"

    write_header=True

    item_keys = []

    json_data = []

    count=1
    with open('/home/likewise-open/ARCS/blm14/rxnorm.txt','rb') as tsvin,  open('output.csv','wb',0) as out:
        tsvin = csv.reader(tsvin,delimiter='\t')
        out.write('rxnorm_id\tvigibase_id\tvigibase_desc\n')
        for line in tsvin:
            try:
                rxid = line[0]
                drugname = line[1]
                query_params = {'tradename': drugname}
                print(query_params)
                json_string = query(query_domain, query_params, userkey, clientkey, service)
                data=json.loads(json_string)
                print(data)
                out.write(rxid + "\t" + data[0]['Code'] + "\t" + data[0]['Value'] + "\n")
                out.flush()

            except Exception, e:    
                pass
                print('fail')
            
    #Printing the json object.
    csv_file.close()
