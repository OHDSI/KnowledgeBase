# pmSearch2rdf.py
#
# Convert the result of a pubmed drug-HOI evidence search to Open Data Annotation
#
# Author: Richard D Boyce, PhD
# 2014/2015
#

import sys
sys.path = sys.path + ['.']

import re, codecs, uuid, datetime
import json
import pickle
from rdflib import Graph, Literal, Namespace, URIRef, RDF, RDFS

SEARCH_RESULTS = "drug-hoi-associations-from-mesh.tsv"

###  TODO: revise this script to use the TSV output and map to OMOP CUIs for RxNorm drugs and SNOMED HOIs (if possible)


# TERMINOLOGY MAPPING FILES
#RXNORM_TO_MESH = "../terminology-mappings/RxNorm-to-MeSH/rxnorm-to-MeSH-mapping-03032014.txt"
RXNORM_TO_MESH = "../terminology-mappings/RxNorm-to-MeSH/mesh-to-rxnorm-standard-vocab-v5.txt"
MESH_TO_STANDARD_VOCAB = "../terminology-mappings/StandardVocabToMeSH/mesh-to-standard-vocab-v5.txt"
MESH_TO_LABEL = "../terminology-mappings/MeSHToMedDRA/mesh_cui_to_label.txt"
MEDDRA_TO_MESH = "../terminology-mappings/MeSHToMedDRA/meshToMeddra-partial-05202014.txt"

# OUTPUT DATA FILE
OUTPUT_FILE = "drug-hoi-pubmed-mesh.rdf"


# TEST DRUGS
DRUGS_D = {}
f = open(RXNORM_TO_MESH,"r")
buf = f.read()
f.close()
l = buf.split("\n")
for elt in l[1:]:
    if elt.strip() == "":
        break

    (mesh,pt,rxcui,concept_name,ohdsiID,conceptClassId) = [x.strip() for x in elt.split("|")]

    # for now, limit to drugs in the top 50K of SPLICER results
    #if ohdsiID not in ['1036233','1103359','1103360','1111243','1113076','1118047','1118118','1119155','1135359','1135469','1136682','1139215','1150347','1151423','1154313','1154350','1154380','1154654','1167323','1178665','1178666','1236610','1304567','1305450','1309995','1310347','1314006','1314009','1318031','1328691','1332529','1341268','1348267','1350490','1363390','1381564','1398400','1507838','1513914','1513916','1516979','1539411','1550775','1551101','1560556','1597772','1703607','1703743','1707313','1710316','1713520','1716904','1717503','1717706','1736925','1738542','1742284','1745073','1758539','1769391','1769413','1781408','1836452','1836953','19003030','19003084','19003394','19005965','19007332','19010556','19016698','19018781','19018820','19018872','19018874','19018906','19018934','19019072','19019074','19019115','19019272','19019273','19019334','19019483','19019581','19019851','19019852','19021102','19022749','19022750','19022830','19023368','19023636','19025637','19027427','19027625','19028313','19028689','19028939','19030093','19030686','19030822','19032895','19033681','19034050','19036750','19037187','19037481','19041106','19041141','19044704','19046028','19047527','19047768','19049686','19054243','19054824','19057665','19058200','19061194','19068190','19069199','19071471','19071718','19072294','19073093','19073186','19073189','19073215','19073776','19073778','19073831','19074694','19074910','19075001','19075003','19075010','19075375','19075380','19075428','19075605','19076330','19076621','19077215','19077244','19077402','19077462','19077463','19077464','19077513','19077550','19077577','19077705','19079160','19079220','19079250','19079300','19079711','19079774','19079834','19079928','19080128','19080251','19080258','19086178','19087105','19091379','19096595','19098439','19100691','19101553','19102203','19102214','19102553','19102759','19106768','19112640','19113340','19113754','19114110','19114249','19121195','19121913','19122808','19123159','19123167','19123171','19123328','19123591','19123596','19123989','19124085','19126315','19127044','19127925','19128149','19128295','19129350','19129513','19129586','19130125','19130670','19131533','19132401','19133574','19133614','19133844','19134047','19134103','19135444','40161123','40162335','40162431','40162433','40162450','40162465','40162499','40162511','40162522','40162552','40162570','40162587','40162672','40162683','40163312','40163342','40163492','40163496','40163497','40163520','40163764','40163861','40163905','40163938','40163985','40164524','40164715','40164897','40164929','40164946','40164962','40165069','40165080','40165161','40165191','40165389','40165411','40165773','40165997','40166131','40166704','40166814','40167213','40167218','40167435','40167443','40167447','40167801','40168116','40168884','40168941','40168991','40169239','40169353','40169683','40169685','40169706','40169770','40169892','40169908','40169944','40171075','40171229','40171426','40171497','40171547','40171668','40171852','40172167','40173099','40173131','40173346','40173415','40173421','40173473','40173759','40173866','40173888','40173900','40174765','40174811','40174880','40174907','40174914','40175001','40175174','40175180','40175281','40175376','40175390','40175463','40176329','40176686','40176744','40177239','40177829','40179635','40180096','40180718','40183394','40184084','40184184','40184189','40184727','40185276','40185277','40221776','40221856','40221859','40221873','40221956','40221966','40221996','40222616','40222636','40222653','40222663','40222930','40223154','40223184','40223454','40223554','40224133','40224162','40224399','40224577','40224785','40225692','40225949','40226430','40226853','40226969','40227095','40228203','40230786','40231928','40232730','40233236','40234056','40236420','40236448','40236824','40237546','40238240','40240888','40241955','40241972','40242563','40242773','40243726','42707286','42707747','42708144','42708259','42800842','42873814','42901674','43011870','43012055','43013076','43013665','704944','704990','705109','711588','715298','718127','720730','722067','722071','722158','736015','736020','739207','739209','742304','743717','744800','748032','749932','751362','778355','778478','778479','778508','778765','781126','789581','798875','798876','800881','836718','902732','902807','906891','917338','920949','923647','928111','950137','961050','961263','964362','964369','964406','966010','968464','968640','968987','974199']:
        #continue

    print "%s - rxnorm: %s (ohdsi: %s)" % (concept_name,rxcui,ohdsiID)

    if DRUGS_D.get(rxcui): # add a synonymn
        DRUGS_D[rxcui][1].append(pt)
    else: # create a new record
        DRUGS_D[rxcui] = (mesh,[pt], ohdsiID)
    
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

MESH_D_SV = {}
f = open(MESH_TO_STANDARD_VOCAB, "r")
buf = f.read()
f.close()
l = buf.split("\n")
for elt in l[1:]: # skip header
    if elt.strip() == "":
        break

    (imeds,label,mesh) = [x.strip() for x in elt.split("|")]
    MESH_D_SV[mesh] = imeds


COND_D_MEDDRA = {}
f = open(MEDDRA_TO_MESH,"r")
buf = f.read()
f.close()
buf = buf.replace("<http://purl.bioontology.org/ontology/MSH/","").replace(">","").replace("http://purl.bioontology.org/ontology/MDR/","")
l = buf.split("\n")
for elt in l:
    if elt.strip() == "":
        break

    (mesh,meddra) = [x.strip() for x in elt.split("\t")]
    if COND_D_MEDDRA.get(mesh): # add a synonymn
        COND_D_MEDDRA[mesh].append(meddra)
    else: # create a new record
        COND_D_MEDDRA[mesh] = [meddra]


## set up RDF graph
# identify namespaces for other ontologies to be used                                                                                    
dcterms = Namespace("http://purl.org/dc/terms/")
pav = Namespace("http://purl.org/pav")
dctypes = Namespace("http://purl.org/dc/dcmitype/")
sio = Namespace('http://semanticscience.org/resource/')
oa = Namespace('http://www.w3.org/ns/oa#')
aoOld = Namespace('http://purl.org/ao/core/') # needed for AnnotationSet and item until the equivalent is in Open Data Annotation
cnt = Namespace('http://www.w3.org/2011/content#')
siocns = Namespace('http://rdfs.org/sioc/ns#')
swande = Namespace('http://purl.org/swan/1.2/discourse-elements#')
ncbit = Namespace('http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#')
mesh = Namespace('http://purl.bioontology.org/ontology/MESH/')
meddra = Namespace('http://purl.bioontology.org/ontology/MEDDRA/')
rxnorm = Namespace('http://purl.bioontology.org/ontology/RXNORM/')
pubmed = Namespace('http://www.ncbi.nlm.nih.gov/pubmed/')
ohdsi = Namespace('http://purl.org/net/ohdsi#')
poc = Namespace('http://purl.org/net/nlprepository/ohdsi-pubmed-mesh-poc#')


graph = Graph()
graph.namespace_manager.reset()
graph.namespace_manager.bind("dcterms", "http://purl.org/dc/terms/")
graph.namespace_manager.bind("pav", "http://purl.org/pav");
graph.namespace_manager.bind("dctypes", "http://purl.org/dc/dcmitype/")
graph.namespace_manager.bind('sio', 'http://semanticscience.org/resource/')
graph.namespace_manager.bind('oa', 'http://www.w3.org/ns/oa#')
graph.namespace_manager.bind('aoOld', 'http://purl.org/ao/core/') # needed for AnnotationSet and item until the equivalent is in Open Data Annotation
graph.namespace_manager.bind('cnt', 'http://www.w3.org/2011/content#')
graph.namespace_manager.bind('siocns','http://rdfs.org/sioc/ns#')
graph.namespace_manager.bind('swande','http://purl.org/swan/1.2/discourse-elements#')
graph.namespace_manager.bind('ncbit','http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#')
graph.namespace_manager.bind('mesh', 'http://purl.bioontology.org/ontology/MESH/')
graph.namespace_manager.bind('meddra','http://purl.bioontology.org/ontology/MEDDRA/')
graph.namespace_manager.bind('rxnorm','http://purl.bioontology.org/ontology/RXNORM/')
graph.namespace_manager.bind('pubmed', 'http://www.ncbi.nlm.nih.gov/pubmed/')
graph.namespace_manager.bind('ohdsi', 'http://purl.org/net/ohdsi#')
graph.namespace_manager.bind('poc','http://purl.org/net/nlprepository/ohdsi-pubmed-mesh-poc#')

### open annotation ontology properties and classes
graph.add((dctypes["Collection"], RDFS.label, Literal("Collection"))) # Used in lieau of the AnnotationSet https://code.google.com/p/annotation-ontology/wiki/AnnotationSet
graph.add((dctypes["Collection"], dcterms["description"], Literal("A collection is described as a group; its parts may also be separately described. See http://dublincore.org/documents/dcmi-type-vocabulary/#H7")))

graph.add((oa["Annotation"], RDFS.label, Literal("Annotation")))
graph.add((oa["Annotation"], dcterms["description"], Literal("Typically an Annotation has a single Body (oa:hasBody), which is the comment or other descriptive resource, and a single Target (oa:hasTarget) that the Body is somehow 'about'. The Body provides the information which is annotating the Target. See  http://www.w3.org/ns/oa#Annotation")))

graph.add((oa["annotatedBy"], RDFS.label, Literal("annotatedBy")))
graph.add((oa["annotatedBy"], RDF.type, oa["objectproperties"]))

graph.add((oa["annotatedAt"], RDFS.label, Literal("annotatedAt")))
graph.add((oa["annotatedAt"], RDF.type, oa["dataproperties"]))

graph.add((oa["TextQuoteSelector"], RDFS.label, Literal("TextQuoteSelector")))
graph.add((oa["TextQuoteSelector"], dcterms["description"], Literal("A Selector that describes a textual segment by means of quoting it, plus passages before or after it. See http://www.w3.org/ns/oa#TextQuoteSelector")))

graph.add((oa["hasSelector"], RDFS.label, Literal("hasSelector")))
graph.add((oa["hasSelector"], dcterms["description"], Literal("The relationship between a oa:SpecificResource and a oa:Selector. See http://www.w3.org/ns/oa#hasSelector")))

graph.add((oa["SpecificResource"], RDFS.label, Literal("SpecificResource")))
graph.add((oa["SpecificResource"], dcterms["description"], Literal("A resource identifies part of another Source resource, a particular representation of a resource, a resource with styling hints for renders, or any combination of these. See http://www.w3.org/ns/oa#SpecificResource")))

# these predicates are specific to SPL annotation
graph.add((sio["SIO_000628"], RDFS.label, Literal("refers to")))
graph.add((sio["SIO_000628"], dcterms["description"], Literal("refers to is a relation between one entity and the entity that it makes reference to.")))

graph.add((sio["SIO_000563"], RDFS.label, Literal("describes")))
graph.add((sio["SIO_000563"], dcterms["description"], Literal("describes is a relation between one entity and another entity that it provides a description (detailed account of)")))

graph.add((sio["SIO_000338"], RDFS.label, Literal("specifies")))
graph.add((sio["SIO_000338"], dcterms["description"], Literal("A relation between an information content entity and a product that it (directly/indirectly) specifies")))

graph.add((poc['MeshDrug'], RDFS.label, Literal("MeSH Drug code")))
graph.add((poc['MeshDrug'], dcterms["description"], Literal("Drug code in the MeSH vocabulary.")))

graph.add((poc['RxnormDrug'], RDFS.label, Literal("Rxnorm Drug code")))
graph.add((poc['RxnormDrug'], dcterms["description"], Literal("Drug code in the Rxnorm vocabulary.")))

graph.add((poc['MeshHoi'], RDFS.label, Literal("MeSH HOI code")))
graph.add((poc['MeshHoi'], dcterms["description"], Literal("HOI code in the MeSH vocabulary.")))

graph.add((poc['MeddraHoi'], RDFS.label, Literal("Meddra HOI code")))
graph.add((poc['MeddraHoi'], dcterms["description"], Literal("HOI code in the Meddra vocabulary.")))

################################################################################

# the dataset holds three dictionaries, one for RCTs, one for case
# reports, and one for other study types. All three dicts have the
# same set of keys

# Debugging
rct_d = pickle.load(open("RCT-temp.pickle", "rb"))
cr_d = pickle.load(open("CR-temp.pickle", "rb"))
other_d = {}

# Deployment
#(rct_d, cr_d, other_d) = pickle.load( open( SEARCH_RESULTS, "rb" ) )

allKeys = list(set(rct_d.keys()).union(set(cr_d.keys())).union(set(other_d.keys())))

annotationSetCntr = 1
annotationItemCntr = 1
annotationBodyCntr = 1
annotationEvidenceCntr = 1

annotatedCache = {} # indexes annotation ids by pmid
currentAnnotation = annotationItemCntr

currentAnnotSet = 'ohdsi-pubmed-mesh-annotation-set-%s' % annotationSetCntr 
annotationSetCntr += 1
graph.add((poc[currentAnnotSet], RDF.type, oa["DataAnnotation"])) # TODO: find out what is being used for collections in OA
graph.add((poc[currentAnnotSet], oa["annotatedAt"], Literal(datetime.date.today())))
graph.add((poc[currentAnnotSet], oa["annotatedBy"], URIRef(u"http://www.pitt.edu/~rdb20/triads-lab.xml#TRIADS")))

dataL = (rct_d, cr_d, other_d)
(RCT,CR,OTHER) = range(0,len(dataL))

for k in allKeys:  
    (rxnormDrug,meshCond) = k.split("-")
    
    ###################################################################
    ### Each annotations holds one target that points to the source
    ### record in pubmed, and one or more bodies each of which
    ### indicates the MeSH terms that triggered the result and holds
    ### some metadata
    ###################################################################
    currentAnnotItem = None
    for i in range(0,len(dataL)):
        curDict = None
        if i == RCT:
            curDict = rct_d
        elif i == CR:
            curDict = cr_d
        elif i == OTHER:
            curDict = other_d

        if curDict.has_key(k) and curDict[k] != []: 
            # iterate through the list of dictionaries containing potential drug-HOI assocations
            for elt in curDict[k]:
                if elt["adeAgent"] == []:
                    continue
                if elt["adeEffect"] == [] and elt["drugComplication"] == []:
                    continue
                
                if annotatedCache.has_key(elt['pmid']):
                    currentAnnotation = annotatedCache[elt['pmid']]
                    currentAnnotItem = "ohdsi-pubmed-mesh-annotation-item-%s" % currentAnnotation
                else:
                    currentAnnotation = annotationItemCntr
                    annotatedCache[elt['pmid']] = currentAnnotation
                    annotationItemCntr += 1
                    
                    currentAnnotItem = "ohdsi-pubmed-mesh-annotation-item-%s" % currentAnnotation

                    graph.add((poc[currentAnnotSet], aoOld["item"], poc[currentAnnotItem])) # TODO: find out what is being used for items of collections in OA
                    graph.add((poc[currentAnnotItem], RDF.type, oa["DataAnnotation"])) 
                    graph.add((poc[currentAnnotItem], RDF.type, ohdsi["PubMedDrugHOIAnnotation"])) # TODO: should be a subclass of oa:DataAnnotation
                    graph.add((poc[currentAnnotItem], oa["annotatedAt"], Literal(datetime.date.today())))
                    graph.add((poc[currentAnnotItem], oa["annotatedBy"], URIRef(u"http://www.pitt.edu/~rdb20/triads-lab.xml#TRIADS")))
                    graph.add((poc[currentAnnotItem], oa["motivatedBy"], oa["tagging"]))
                    
                    currentAnnotTargetUuid = URIRef(u"urn:uuid:%s" % uuid.uuid4())
                    graph.add((poc[currentAnnotItem], oa["hasTarget"], currentAnnotTargetUuid))
                    graph.add((currentAnnotTargetUuid, RDF.type, oa["SpecificResource"]))
                    graph.add((currentAnnotTargetUuid, oa["hasSource"], pubmed[elt['pmid']]))

                    if i == RCT:
                        graph.add((currentAnnotTargetUuid, ohdsi["MeshStudyType"], Literal("clinical trial (publication type)")))
                    elif i == CR:
                        graph.add((currentAnnotTargetUuid, ohdsi["MeshStudyType"], Literal("case reports (publication type)")))
                    else:
                        graph.add((currentAnnotTargetUuid, ohdsi["MeshStudyType"], Literal("other (publication type)")))

                
                # Specify the bodies of the annotation - for this type each
                # body contains the MESH drug and condition as a semantic tag
                currentAnnotationBody = "ohdsi-pubmed-mesh-annotation-annotation-body-%s" % annotationBodyCntr
                annotationBodyCntr += 1
         
                graph.add((poc[currentAnnotItem], oa["hasBody"], poc[currentAnnotationBody]))
                graph.add((poc[currentAnnotationBody], RDFS.label, Literal("Drug-HOI tag for %s" % k)))
                graph.add((poc[currentAnnotationBody], RDF.type, ohdsi["OHDSIMeshTags"])) # TODO: this is not yet formalized in a public ontology but should be
                
                # temporarily, include the mesh tags from the record as preferred terms as well as data from the drug and HOI query
                
                ## mesh tags from the record
                collectionHead = URIRef(u"urn:uuid:%s" % uuid.uuid4())
                graph.add((poc[currentAnnotationBody], ohdsi['adeAgents'], collectionHead))
                for agent in elt["adeAgent"]:
                    graph.add((collectionHead, ohdsi['adeAgent'], Literal(agent)))

                if elt["adeEffect"] != []:
                    collectionHead = URIRef(u"urn:uuid:%s" % uuid.uuid4())
                    graph.add((poc[currentAnnotationBody], ohdsi['adeEffects'], collectionHead))
                    for effect in elt["adeEffect"]:
                        graph.add((collectionHead, ohdsi['adeEffect'], Literal(effect)))

                if elt["drugComplication"] != []:
                    collectionHead = URIRef(u"urn:uuid:%s" % uuid.uuid4())
                    graph.add((poc[currentAnnotationBody], ohdsi['drugComplications'], collectionHead))
                    for complication in elt["drugComplication"]:
                        graph.add((collectionHead, ohdsi['drugComplication'], Literal(complication)))


                ## data from the drug and HOI query
                if DRUGS_D.has_key(rxnormDrug) and COND_D.has_key(meshCond):
                    graph.add((poc[currentAnnotationBody], dcterms["description"], Literal("Drug-HOI tag for %s (%s - %s)" % (k, DRUGS_D[rxnormDrug][1], COND_D[meshCond][0]))))

                # NOTE: to resolve using Bioportal, append these PURLS to "http://bioportal.bioontology.org/ontologies/MEDDRA?p=classes&conceptid="
                graph.add((poc[currentAnnotationBody], ohdsi['RxnormDrug'], rxnorm[rxnormDrug]))
                if DRUGS_D.has_key(rxnormDrug):
                    graph.add((poc[currentAnnotationBody], ohdsi['MeshDrug'], mesh[DRUGS_D[rxnormDrug][0]])) # TODO: consider adding the values as a collection
                    graph.add((poc[currentAnnotationBody], ohdsi['ImedsDrug'], ohdsi[DRUGS_D[rxnormDrug][2]]))
                else:
                    print "ERROR: no MeSH equivalent to the rxnorm drug %s, skipping %s" % (rxnormDrug, k)
                    continue

                if MESH_D_SV.has_key(meshCond):
                    graph.add((poc[currentAnnotationBody], ohdsi['ImedsHoi'], ohdsi[MESH_D_SV[meshCond]]))
                graph.add((poc[currentAnnotationBody], ohdsi['MeshHoi'], mesh[meshCond]))
                if COND_D_MEDDRA.has_key(meshCond):
                    collectionHead = URIRef(u"urn:uuid:%s" % uuid.uuid4())
                    graph.add((poc[currentAnnotationBody], ohdsi['MeddraHois'], collectionHead))
                    condL = COND_D_MEDDRA[meshCond]
                    for i in range(0,len(condL)):
                        graph.add((collectionHead, ohdsi['MeddraHoi'], meddra[condL[i]]))
                    # TESTED: Create a collection for the MeSH condition
                    # restUuid = URIRef(u"urn:uuid:%s" % uuid.uuid4())
                    # collectionHead = restUuid
                    # for i in range(0,len(condL)):
                    #     if i == len(condL):
                    #         graph.add((restUuid, RDF.rest, RDF.nil))
                    #     else:
                    #         graph.add((restUuid, RDF.first, meddra[condL[i]]))                            
                    #         restUuid2 = URIRef(u"urn:uuid:%s" % uuid.uuid4())
                    #         graph.add((restUuid, RDF.rest, restUuid2))
                    #         restUuid = restUuid2                             
                    #graph.add((poc[currentAnnotationBody], ohdsi['MeddrraHois'], collectionHead))
                else:
                    print "ERROR: no MedDRA equivalent to the MeSH condition %s, skipping %s" % (meshCond, k)
                    continue


# display the graph
f = codecs.open(OUTPUT_FILE,"w","utf8")
#graph.serialize(destination=f,format="xml",encoding="utf8")
s = graph.serialize(format="xml",encoding="utf8")

#f.write(graph.serialize(format="xml",encoding="utf8"))
f.write(unicode(s,errors='replace'))
#print graph.serialize(format="xml")
f.close

graph.close()
