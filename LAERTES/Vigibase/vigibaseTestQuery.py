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

# Connection information 
DB_CONNECTION_INFO="db-connection.conf"
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
        url = opener.open(request)
        return url.read()
    except Exception, e:
        traceback.print_exc(file=sys.stdout)
        raise e

if __name__ == "__main__":
    userkey = base64.b64encode("%s:%s" % (username,pw))
    service = "https://api.who-umc.org/vigibase/icsrstatistics/dimensions/"

    #Some sample query.
    query_domain = "drug"
    query_params = {'tradename': 'Alvedon'}
    json_string = query(query_domain, query_params, userkey, clientkey, service)
    resultset=json.loads(json_string)

    #Printing the json object.
    print "WHO Global ICSR database – VigiBase®"
    print json.dumps(resultset,indent=1)
