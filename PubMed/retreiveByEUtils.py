#/usr/bin/python

import re, sys, pickle
sys.path = sys.path + ['.']

from Bio.EUtils  import HistoryClient


# TERMINOLOGY MAPPING FILES
RXNORM_TO_MESH = "../terminology-mappings/RxNorm-to-MeSH/rxnorm-to-MeSH-mapping-03032014.txt"
MESH_TO_LABEL = "../terminology-mappings/MeSHToMedDRA/mesh_cui_to_label.txt"
MEDDRA_TO_MESH = "../terminology-mappings/MeSHToMedDRA/meshToMeddra-partial-05202014.txt"

# OUTPUT DATA FILE
PICKLE_FILE = "drug-hoi-test.pickle"

# PUBLICATION TYPE FILTERS
RCT_FILTER = "Clinical Trial [PT]"
CASE_REPORT_FILTER = "Case Reports [PT]"
OTHER_FILTER = "NOT Case Reports [PT] NOT Clinical Trial [PT]"

# THE GLOBAL QUERY CLIENT
client1 = HistoryClient.HistoryClient()

# TEST DRUGS
DRUGS_D = {}
f = open(RXNORM_TO_MESH,"r")
buf = f.read()
f.close()
l = buf.split("\n")
for elt in l:
    if elt.strip() == "":
        break

    (rxcui,mesh,pt) = [x.strip() for x in elt.split("|")]
    if DRUGS_D.get(rxcui): # add a synonymn
        DRUGS_D[rxcui][1].append(pt)
    else: # create a new record
        DRUGS_D[rxcui] = (mesh,[pt])
    
### TEST CONDITIONS
COND_D = {}
f = open(MESH_TO_LABEL,"r")
buf = f.read()
f.close()
l = buf.split("\n")
for elt in l:
    if elt.strip() == "":
        break

    (mesh,term) = [x.strip() for x in elt.split("|")]
    if COND_D.get(mesh): # add a synonymn
        COND_D[mesh].append(term)
    else: # create a new record
        COND_D[mesh] = [term]

def retrieveByEUtils(drugD, condD, pubTypeFilter, pt):
    rslt_D = {}
    for d in drugD.keys():
        drugLabel = drugD[d][1][0]
        for cond in condD.keys():
            condLabel = condD[cond][0]
            print "INFO: Retrieving %s results for drug %s (%s) and condition %s (%s)" % (pt, d, drugLabel, cond, condLabel)
        
            k = "%s-%s" % (d,cond)
            rslt_D[k] = []

            q = '''%s AND ("%s" [MeSH Terms]) AND ("%s" [MeSH Terms])''' % (pubTypeFilter, drugLabel, condLabel)
            rslts = client1.search(q)
            for i in range(0,len(rslts)):
                rec = rslts[i].efetch(retmode = "text", rettype = "abstract").read()
                id = re.findall("PMID: \d+",rec)
                id = " ".join(id)
                id = id[6:]
                newD = {"pmid":id,
                        "abstract":rec}
                
                rslt_D[k].append(newD)

    return rslt_D

### GET RCTS
RCT_D = retrieveByEUtils(DRUGS_D, COND_D, RCT_FILTER, "RCT")

### GET CASE REPORTS
CR_D = retrieveByEUtils(DRUGS_D, COND_D, CASE_REPORT_FILTER, "CASE REPORT")

### GET OTHER
OTHER_D = retrieveByEUtils(DRUGS_D, COND_D, OTHER_FILTER, "OTHER")
            
results = [RCT_D, CR_D, OTHER_D]

f = open(PICKLE_FILE,"w")
pickle.dump(results, f)
f.close()
