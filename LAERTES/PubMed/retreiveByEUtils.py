#/usr/bin/python
# -*- coding: utf-8
#
# retreiveByEUtils.py
#
# Retrieve MEDLINE records for indexed literature reporting adverse
# drug events and store the data for further processing. This program uses a similar method to that described in:
#    Avillach P, Dufour JC, Diallo G, Salvo F, Joubert M, Thiessard F, Mougin F, Trifirò G, Fourrier-Réglat A, Pariente A, Fieschi M. Design and val     idation of an automated method to detect known adverse drug reactions in MEDLINE: a contribution from the EU-ADR project. J Am Med Inform Assoc    . 2013 May 1;20(3):446-52. doi: 10.1136/amiajnl-2012-001083. Epub 2012 Nov 29. PubMed PMID: 23195749; PubMed Central PMCID: PMC3628051.
#
# Author: Richard Boyce
# September 2014
#

import re, sys, pickle
sys.path = sys.path + ['.']

from httplib import BadStatusLine
from Bio.EUtils  import HistoryClient

# maximum number of drugs to search 
#MAX_DRUGS = 100
MAX_DRUGS = 50

# TERMINOLOGY MAPPING FILES
#RXNORM_TO_MESH = "../terminology-mappings/RxNorm-to-MeSH/rxnorm-to-MeSH-mapping-03032014.txt"
RXNORM_TO_MESH = "../terminology-mappings/RxNorm-to-MeSH/mesh-to-rxnorm-standard-vocab-v5.txt"
MESH_TO_LABEL = "../terminology-mappings/MeSHToMedDRA/mesh_cui_to_label.txt"
MEDDRA_TO_MESH = "../terminology-mappings/MeSHToMedDRA/meshToMeddra-partial-05202014.txt"

# OUTPUT DATA FILE
PICKLE_FILE = "drug-hoi-test.pickle"
TEMP_STAGING_PICKLE = "temp.pickle"

# PUBLICATION TYPE FILTERS
RCT_FILTER = "Clinical Trial [PT]"
CASE_REPORT_FILTER = "Case Reports [PT]"
OTHER_FILTER = "NOT Case Reports [PT] NOT Clinical Trial [PT]"

################################################################################

# THE GLOBAL QUERY CLIENT
client1 = HistoryClient.HistoryClient()

# TEST DRUGS
DRUGS_D = {}
f = open(RXNORM_TO_MESH,"r")
buf = f.read()
f.close()
l = buf.split("\n")
for elt in l[1:]: # skip header
    if elt.strip() == "":
        break

    # use rxcui,mesh,pt for rxnorm-to-MeSH-mapping-03032014.txt

    (mesh,pt,rxcui,concept_name,ohdsi,conceptClass) = [x.strip() for x in elt.split("|")]

    print "adding to drug dictionary: %s - rxnorm: %s (ohdsi: %s)" % (concept_name,rxcui,ohdsi)

    if DRUGS_D.get(rxcui): # add a synonymn
        DRUGS_D[rxcui][1].append(pt)
    else: # create a new record
        DRUGS_D[rxcui] = (mesh,[pt], ohdsi)
    
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

def retrieveByEUtils(drugD, condD, pubTypeFilter, pt, limit=None, stageNamePrefix=""):
    rslt_D = {}
    if limit:
        i = 0
    keys = drugD.keys()
    keys.sort()
    for d in keys:
        if limit:
            if i <= limit:
                i += 1
            else:
                break
        drugLabel = drugD[d][1][0]
        for cond in condD.keys():
            condLabel = condD[cond][0]
            print "INFO: Retrieving %s results for drug %s (%s) and condition %s (%s)" % (pt, d, drugLabel, cond, condLabel)
        
            k = "%s-%s" % (d,cond)
            rslt_D[k] = []

            q = '''(%s) AND ("%s" [MeSH Terms] OR "%s" [Ti]) AND ("%s" [MeSH Terms] OR "%s" [Ti])''' % (pubTypeFilter, drugLabel, drugLabel, condLabel, condLabel)
            rslts = client1.search(q)

            print "INFO: %d results" % len(rslts)
            for i in range(0,len(rslts)):
                try:
                    rec = rslts[i].efetch(retmode = "text", rettype = "medline").read()
                   
                    newD = parseMedlineForADE(rec)
                    if newD != None:
                        rslt_D[k].append(newD)
                except BadStatusLine:
                    print "INFO: unable to retrieve result %d for drug %s - httplib.BadStatusLine" % (i,k)

        f = open(stageNamePrefix + TEMP_STAGING_PICKLE,"w")
        pickle.dump(rslt_D, f)
        f.close()
        "INFO: staging results up to drug %s and condition %s are stored as the rslt_d dictionary in %s" % (d.upper(), cond.upper(), stageNamePrefix + TEMP_STAGING_PICKLE)

    return rslt_D


def parseMedlineForADE(rec):
    """ Parse a medline record for an adverse drug event association using the method described in: 
    Avillach P, Dufour JC, Diallo G, Salvo F, Joubert M, Thiessard F, Mougin F, Trifirò G, Fourrier-Réglat A, Pariente A, Fieschi M. Design and validation of an automated method to detect known adverse drug reactions in MEDLINE: a contribution from the EU-ADR project. J Am Med Inform Assoc. 2013 May 1;20(3):446-52. doi: 10.1136/amiajnl-2012-001083. Epub 2012 Nov 29. PubMed PMID: 23195749; PubMed Central PMCID: PMC3628051.
    """
    d = {"pmid":None,
         "adeAgent":[],
         "adeEffect":[],
         "drugComplication":[],
         "otherComplication":[],
         "substances":[]}

    pmidRgx = re.compile("PMID-(.*)")
    l = pmidRgx.findall(rec)
    if len(l) == 0:
        print "ERROR: unable to process a PMID from the following medline record:\n\t%s" % rec
        return None
    else:
        d["pmid"] = l[0].strip()

    mshRgx = re.compile("MH  - (.*)")
    l = mshRgx.findall(rec)
    for elt in l:
        tpl = elt.split("/")
        msh = tpl[0]
        rest = "/".join(tpl[1:])
        if rest.find("adverse effects") != -1:
            d["adeAgent"].append(msh.strip())
        elif rest.find("chemically induced") != -1:          
            if rest.find("complications") != -1:
                d["drugComplication"].append(msh.strip())
            else:
                d["adeEffect"].append(msh.strip())

        elif rest.find("complications") != -1:
            d["otherComplication"].append(msh.strip())
    
    # TODO: extend processing of substances to only take into account
    # drugs from the ‘substances’ field if their pharmacological
    # action was qualified by the subheading ‘AE’
    #
    # TODO: consider how to best use the FDA UNII mappings for
    # substances where present
    substanceRgx = re.compile("RN  - (.*)")
    l = substanceRgx.findall(rec)
    for elt in l:
        d["substances"].append(elt.strip())

    return d
        

RCT_D = CR_D = OTHER_D = None

### GET RCTS
RCT_D = retrieveByEUtils(DRUGS_D, COND_D, RCT_FILTER, "RCT", MAX_DRUGS, "RCT-")
print "INFO: writing RCT results to %s. Case report and Other pending" % PICKLE_FILE
results = [RCT_D, CR_D, OTHER_D]
f = open(PICKLE_FILE,"w")
pickle.dump(results, f)
f.close()

### GET CASE REPORTS
CR_D = retrieveByEUtils(DRUGS_D, COND_D, CASE_REPORT_FILTER, "CASE REPORT", MAX_DRUGS, "CR-")
print "INFO: writing RCT and Case Report results to %s.  Other pending" % PICKLE_FILE
results = [RCT_D, CR_D, OTHER_D]
f = open(PICKLE_FILE,"w")
pickle.dump(results, f)
f.close()

### GET OTHER
OTHER_D = retrieveByEUtils(DRUGS_D, COND_D, OTHER_FILTER, "OTHER", MAX_DRUGS, "OTHER-")
            
results = [RCT_D, CR_D, OTHER_D]
print "INFO: writing RCT, Case Report, and Other results to %s." % PICKLE_FILE
f = open(PICKLE_FILE,"w")
pickle.dump(results, f)
f.close()
