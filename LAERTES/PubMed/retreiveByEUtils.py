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
MAX_DRUGS = 100

# TERMINOLOGY MAPPING FILES
#RXNORM_TO_MESH = "../terminology-mappings/RxNorm-to-MeSH/rxnorm-to-MeSH-mapping-03032014.txt"
RXNORM_TO_MESH = "../terminology-mappings/RxNorm-to-MeSH/mesh-to-rxnorm-standard-vocab-v4.txt"
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

    (mesh,pt,rxcui,concept_name,ohdsi) = [x.strip() for x in elt.split("|")]

    # uncomment to limit to drugs in the top 50K of SPLICER results
    #if ohdsi not in ['1036233','1103359','1103360','1111243','1113076','1118047','1118118','1119155','1135359','1135469','1136682','1139215','1150347','1151423','1154313','1154350','1154380','1154654','1167323','1178665','1178666','1236610','1304567','1305450','1309995','1310347','1314006','1314009','1318031','1328691','1332529','1341268','1348267','1350490','1363390','1381564','1398400','1507838','1513914','1513916','1516979','1539411','1550775','1551101','1560556','1597772','1703607','1703743','1707313','1710316','1713520','1716904','1717503','1717706','1736925','1738542','1742284','1745073','1758539','1769391','1769413','1781408','1836452','1836953','19003030','19003084','19003394','19005965','19007332','19010556','19016698','19018781','19018820','19018872','19018874','19018906','19018934','19019072','19019074','19019115','19019272','19019273','19019334','19019483','19019581','19019851','19019852','19021102','19022749','19022750','19022830','19023368','19023636','19025637','19027427','19027625','19028313','19028689','19028939','19030093','19030686','19030822','19032895','19033681','19034050','19036750','19037187','19037481','19041106','19041141','19044704','19046028','19047527','19047768','19049686','19054243','19054824','19057665','19058200','19061194','19068190','19069199','19071471','19071718','19072294','19073093','19073186','19073189','19073215','19073776','19073778','19073831','19074694','19074910','19075001','19075003','19075010','19075375','19075380','19075428','19075605','19076330','19076621','19077215','19077244','19077402','19077462','19077463','19077464','19077513','19077550','19077577','19077705','19079160','19079220','19079250','19079300','19079711','19079774','19079834','19079928','19080128','19080251','19080258','19086178','19087105','19091379','19096595','19098439','19100691','19101553','19102203','19102214','19102553','19102759','19106768','19112640','19113340','19113754','19114110','19114249','19121195','19121913','19122808','19123159','19123167','19123171','19123328','19123591','19123596','19123989','19124085','19126315','19127044','19127925','19128149','19128295','19129350','19129513','19129586','19130125','19130670','19131533','19132401','19133574','19133614','19133844','19134047','19134103','19135444','40161123','40162335','40162431','40162433','40162450','40162465','40162499','40162511','40162522','40162552','40162570','40162587','40162672','40162683','40163312','40163342','40163492','40163496','40163497','40163520','40163764','40163861','40163905','40163938','40163985','40164524','40164715','40164897','40164929','40164946','40164962','40165069','40165080','40165161','40165191','40165389','40165411','40165773','40165997','40166131','40166704','40166814','40167213','40167218','40167435','40167443','40167447','40167801','40168116','40168884','40168941','40168991','40169239','40169353','40169683','40169685','40169706','40169770','40169892','40169908','40169944','40171075','40171229','40171426','40171497','40171547','40171668','40171852','40172167','40173099','40173131','40173346','40173415','40173421','40173473','40173759','40173866','40173888','40173900','40174765','40174811','40174880','40174907','40174914','40175001','40175174','40175180','40175281','40175376','40175390','40175463','40176329','40176686','40176744','40177239','40177829','40179635','40180096','40180718','40183394','40184084','40184184','40184189','40184727','40185276','40185277','40221776','40221856','40221859','40221873','40221956','40221966','40221996','40222616','40222636','40222653','40222663','40222930','40223154','40223184','40223454','40223554','40224133','40224162','40224399','40224577','40224785','40225692','40225949','40226430','40226853','40226969','40227095','40228203','40230786','40231928','40232730','40233236','40234056','40236420','40236448','40236824','40237546','40238240','40240888','40241955','40241972','40242563','40242773','40243726','42707286','42707747','42708144','42708259','42800842','42873814','42901674','43011870','43012055','43013076','43013665','704944','704990','705109','711588','715298','718127','720730','722067','722071','722158','736015','736020','739207','739209','742304','743717','744800','748032','749932','751362','778355','778478','778479','778508','778765','781126','789581','798875','798876','800881','836718','902732','902807','906891','917338','920949','923647','928111','950137','961050','961263','964362','964369','964406','966010','968464','968640','968987','974199']:
        #continue

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
