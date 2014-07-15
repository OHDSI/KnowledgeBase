# pmSearch2rdf.py
#
# Convert the result of a pubmed drug-HOI evidence search to Open Data Annotation
#
# Author: Richard D Boyce, PhD
# July 2014
#

import sys
sys.path = sys.path + ['.']

import re, codecs, uuid, datetime
import json
import pickle
from rdflib import Graph, BNode, Literal, Namespace, URIRef, RDF, RDFS

SEARCH_RESULTS = "drug-hoi-test.pickle"

# TERMINOLOGY MAPPING FILES
RXNORM_TO_MESH = "../terminology-mappings/RxNorm-to-MeSH/rxnorm-to-MeSH-mapping-03032014.txt"
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
(rct_d, cr_d, other_d) = pickle.load( open( SEARCH_RESULTS, "rb" ) )
commonKeys = rct_d.keys()

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

for k in commonKeys:  
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

        if curDict[k] != []:
            for elt in curDict[k]:
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
                    graph.add((poc[currentAnnotItem], oa["annotatedAt"], Literal(datetime.date.today())))
                    graph.add((poc[currentAnnotItem], oa["annotatedBy"], URIRef(u"http://www.pitt.edu/~rdb20/triads-lab.xml#TRIADS")))
                    graph.add((poc[currentAnnotItem], oa["motivatedBy"], oa["tagging"]))
                    
                    currentAnnotTargetUuid = URIRef(u"urn:uuid:%s" % uuid.uuid4())
                    graph.add((poc[currentAnnotItem], oa["hasTarget"], currentAnnotTargetUuid))
                    graph.add((currentAnnotTargetUuid, RDF.type, oa["SpecificResource"]))
                    graph.add((currentAnnotTargetUuid, oa["hasSource"], pubmed[elt['pmid']]))

                    if i == RCT:
                        graph.add((currentAnnotTargetUuid, poc["MeshStudyType"], Literal("clinical trial (publication type)")))
                    elif i == CR:
                        graph.add((currentAnnotTargetUuid, poc["MeshStudyType"], Literal("case reports (publication type)")))

                
                    # Specify the bodies of the annotation - for this type each
                    # body contains the MESH drug and condition as a semantic tag
                    currentAnnotationBody = "ohdsi-pubmed-mesh-annotation-annotation-body-%s" % annotationBodyCntr
                    annotationBodyCntr += 1
         
                    graph.add((poc[currentAnnotItem], oa["hasBody"], poc[currentAnnotationBody]))
                    graph.add((poc[currentAnnotationBody], RDFS.label, "Drug-HOI tag for %s" % k))
                    graph.add((poc[currentAnnotationBody], RDF.type, poc["OHDSIMeshTags"])) # TODO: this is not yet formalized in a public ontology but should be
                    if DRUGS_D.has_key(rxnormDrug) and COND_D.has_key(meshCond):
                        graph.add((poc[currentAnnotationBody], dcterms["description"], "Drug-HOI tag for %s (%s - %s)" % (k, DRUGS_D[rxnormDrug][1], COND_D[meshCond][0])))

                    # NOTE: to resolve using Bioportal, append these PURLS to "http://bioportal.bioontology.org/ontologies/MEDDRA?p=classes&conceptid="
                    graph.add((poc[currentAnnotationBody], poc['RxnormDrug'], rxnorm[rxnormDrug]))
                    if DRUGS_D.has_key(rxnormDrug):
                        graph.add((poc[currentAnnotationBody], poc['MeshDrug'], mesh[DRUGS_D[rxnormDrug][0]])) # TODO: consider adding the values as a collection
                    else:
                        print "ERROR: no MeSH equivalent to the rxnorm drug %s" % rxnormDrug
                        
                    graph.add((poc[currentAnnotationBody], poc['MeshHoi'], mesh[meshCond]))
                    if COND_D_MEDDRA.has_key(meshCond):
                        graph.add((poc[currentAnnotationBody], poc['MeddrraHoi'], meddra[COND_D_MEDDRA[meshCond][0]])) # TODO: consider adding the values as a collection
                    else:
                        print "ERROR: no MedDRA equivalent to the MeSH condition %s" % meshCond


# display the graph
f = codecs.open(OUTPUT_FILE,"w","utf8")
#graph.serialize(destination=f,format="xml",encoding="utf8")
s = graph.serialize(format="xml",encoding="utf8")

#f.write(graph.serialize(format="xml",encoding="utf8"))
f.write(unicode(s,errors='replace'))
#print graph.serialize(format="xml")
f.close

graph.close()
