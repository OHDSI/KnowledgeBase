# splicer2rdf.py
#
# Convert the result of a SPLICER drug-HOI evidence search to Open Data Annotation
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

SPLICER_DATA = "/media/Backup/SPLICER-data/SPLICER_JANSSEN_July2014.tsv"

# TERMINOLOGY MAPPING FILES
RXNORM_TO_MESH = "../terminology-mappings/RxNorm-to-MeSH/rxnorm-to-MeSH-mapping-03032014.txt"
RXNORM_TO_OMOP = "../terminology-mappings/StandardVocabToRxNorm/imeds_drugids_to_rxcuis.csv"
MESH_TO_LABEL = "../terminology-mappings/MeSHToMedDRA/mesh_cui_to_label.txt"
MEDDRA_TO_MESH = "../terminology-mappings/MeSHToMedDRA/meshToMeddra-partial-05202014.txt"

# OUTPUT DATA FILE
OUTPUT_FILE = "drug-hoi-splicer.rdf"

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

DRUGS_D_OMOP = {}
f = open(RXNORM_TO_OMOP,"r")
buf = f.read()
f.close()
l = buf.split("\n")
for elt in l:
    if elt.strip() == "":
        break

    (omop,rxcui) = [x.strip() for x in elt.split("|")]
    DRUGS_D_OMOP[omop] = rxcui
        
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


def splicer_f_generator():
    # open the SPLICER data file and parse it incrementally
    #
    # @returns: a dictionary containing all of the data in a single
    #           SPLICER record.
    f = open(SPLICER_DATA, 'r')
    if not f:
        f.close()
        raise StopIteration

    # skips header 
    l = f.readline()
    while 1:
        l = f.readline()

        # stops at EOF
        if l == "":
            f.close()
            raise StopIteration

        elts = l.strip("\n").replace('"',"").split("\t")
        rowD = {}
        (rowD["DRUG_CONCEPT_ID"], rowD["SPL_ID"], rowD["SET_ID"], rowD["TRADE_NAME"], rowD["SPL_DATE"], rowD["SPL_SECTION"], rowD["CONDITION_CONCEPT_ID"], rowD["CONDITION_PT"], rowD["CONDITION_LLT"], rowD["CONDITION_SOURCE_VALUE"], rowD["parseMethod"], rowD["sentenceNum"], rowD["labdirection"], rowD["drugfreq"], rowD["exclude"]) = elts
        
        # return the dictionary entry
        yield rowD



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
dailymed = Namespace('http://dbmi-icode-01.dbmi.pitt.edu/linkedSPLs/vocab/resource/')
ohdsi = Namespace('http://purl.org/net/ohdsi#')
poc = Namespace('http://purl.org/net/nlprepository/ohdsi-adr-splicer-poc#')

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
graph.namespace_manager.bind('dailymed', 'http://dbmi-icode-01.dbmi.pitt.edu/linkedSPLs/vocab/resource/')
graph.namespace_manager.bind('ohdsi', 'http://purl.org/net/ohdsi#')
graph.namespace_manager.bind('poc','http://purl.org/net/nlprepository/ohdsi-adr-splicer-poc#')

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

graph.add((poc['ImedsDrug'], RDFS.label, Literal("IMEDS Drug code")))
graph.add((poc['ImedsDrug'], dcterms["description"], Literal("Drug code in the IMEDS standard vocabulary.")))

graph.add((poc['RxnormDrug'], RDFS.label, Literal("Rxnorm Drug code")))
graph.add((poc['RxnormDrug'], dcterms["description"], Literal("Drug code in the Rxnorm vocabulary.")))

graph.add((poc['MeshHoi'], RDFS.label, Literal("MeSH HOI code")))
graph.add((poc['MeshHoi'], dcterms["description"], Literal("HOI code in the MeSH vocabulary.")))

graph.add((poc['MeddraHoi'], RDFS.label, Literal("Meddra HOI code")))
graph.add((poc['MeddraHoi'], dcterms["description"], Literal("HOI code in the Meddra vocabulary.")))

graph.add((poc['adrSectionIdentified'], RDFS.label, Literal("SPL section location of ADR")))
graph.add((poc['adrSectionIdentified'], dcterms["description"], Literal("SPL section location of the ADR.")))

################################################################################

annotationSetCntr = 1
annotationItemCntr = 1
annotationBodyCntr = 1
annotationEvidenceCntr = 1

annotatedCache = {} # indexes annotation ids by pmid
currentAnnotation = annotationItemCntr

currentAnnotSet = 'ohdsi-splicer-annotation-set-%s' % annotationSetCntr 
annotationSetCntr += 1
graph.add((poc[currentAnnotSet], RDF.type, oa["DataAnnotation"])) # TODO: find out what is being used for collections in OA
graph.add((poc[currentAnnotSet], oa["annotatedAt"], Literal(datetime.date.today())))
graph.add((poc[currentAnnotSet], oa["annotatedBy"], URIRef(u"http://www.pitt.edu/~rdb20/triads-lab.xml#TRIADS")))


# DEBUG
cntr = 0 
it = splicer_f_generator()
for elt in it:
    if cntr == 50000:
        break
    cntr += 1

    # for now, only process those ADR records for drugs that we have
    # mesh mappings for
    imedsDrug = elt["DRUG_CONCEPT_ID"]
    rxcuiDrug = meshDrug = drugLabs = None
    if DRUGS_D_OMOP.has_key(imedsDrug):
        rxcuiDrug = DRUGS_D_OMOP[imedsDrug]
        print "INFO: rxcuiDrug : %s" % rxcuiDrug

        # if DRUGS_D.has_key(rxcuiDrug):
        #     drugLabs = DRUGS_D[rxcuiDrug][1]
        #     meshDrug = DRUGS_D[rxcuiDrug][0]
        #     print "INFO: processing adr record with OMOP concept id %s" % imedsDrug
        # else:
        #     print "INFO: Skipping - no mesh mapping in rxnorm to mesh drug list for OMOP concept id %s" % imedsDrug
        #     continue

    ###################################################################
    ### Each annotations holds one target that points to the source
    ### record in DailyMed, and one or more bodies each of which
    ### indicates the MedDRA terms that triggered the result and holds
    ### some metadata
    ###################################################################
    currentAnnotItem = None

    if annotatedCache.has_key(elt['SET_ID']):
        currentAnnotation = annotatedCache[elt['SET_ID']]
        currentAnnotItem = "ohdsi-splicer-annotation-item-%s" % currentAnnotation
    else:
        currentAnnotation = annotationItemCntr
        annotatedCache[elt['SET_ID']] = currentAnnotation
        annotationItemCntr += 1
        
        currentAnnotItem = "ohdsi-splicer-annotation-item-%s" % currentAnnotation

        graph.add((poc[currentAnnotSet], aoOld["item"], poc[currentAnnotItem])) # TODO: find out what is being used for items of collections in OA
        graph.add((poc[currentAnnotItem], RDF.type, oa["DataAnnotation"]))
        graph.add((poc[currentAnnotItem], RDF.type, ohdsi["ADRAnnotation"]))
        graph.add((poc[currentAnnotItem], oa["annotatedAt"], Literal(datetime.date.today())))
        graph.add((poc[currentAnnotItem], oa["annotatedBy"], URIRef(u"http://www.pitt.edu/~rdb20/triads-lab.xml#TRIADS")))
        graph.add((poc[currentAnnotItem], oa["motivatedBy"], oa["tagging"]))
        # TODO: add in PROV wasGeneratedBY

        currentAnnotTargetUuid = URIRef(u"urn:uuid:%s" % uuid.uuid4())
        graph.add((poc[currentAnnotItem], oa["hasTarget"], currentAnnotTargetUuid))
        graph.add((currentAnnotTargetUuid, RDF.type, oa["SpecificResource"]))
        graph.add((currentAnnotTargetUuid, oa["hasSource"], URIRef(u"http://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=" + elt['SET_ID'])))

        # TODO: make these custom Selectors for SPLs
        currentAnnotSelectorUuid = URIRef(u"urn:uuid:%s" % uuid.uuid4())
        graph.add((currentAnnotTargetUuid, oa["hasSelector"], currentAnnotSelectorUuid))
        graph.add((currentAnnotSelectorUuid, RDF.type, dailymed["SectionSelector"]))

        if elt["SPL_SECTION"] == "Adverse Reactions" or elt["SPL_SECTION"] == "Post Marketing":
            graph.add((currentAnnotSelectorUuid, dailymed["splSection"], dailymed["adverseReactions"]))
        elif elt["SPL_SECTION"] == "Precautions (beta)":
            graph.add((currentAnnotSelectorUuid, dailymed["splSection"], dailymed["precautions"]))
        elif elt["SPL_SECTION"] == "Black Box (beta)":
            graph.add((currentAnnotSelectorUuid, dailymed["splSection"], dailymed["boxedWarning"]))

                
    # Specify the bodies of the annotation - for this type each
    # body contains the MESH drug and condition as a semantic tag
    currentAnnotationBody = "ohdsi-splicer-annotation-body-%s" % annotationBodyCntr
    annotationBodyCntr += 1
        
    graph.add((poc[currentAnnotItem], oa["hasBody"], poc[currentAnnotationBody]))
    graph.add((poc[currentAnnotationBody], RDFS.label, Literal("Drug-HOI tag for %s-%s" % (imedsDrug, elt["CONDITION_CONCEPT_ID"]))))
    graph.add((poc[currentAnnotationBody], RDF.type, ohdsi["adrAnnotationBody"])) # TODO: this is not yet formalized in a public ontology but should be

    graph.add((poc[currentAnnotationBody], dcterms["description"], Literal("Drug-HOI tag for %s (rxnorm) - %s" % (rxcuiDrug, elt["CONDITION_PT"]))))
    graph.add((poc[currentAnnotationBody], ohdsi['ImedsDrug'], ohdsi[imedsDrug]))
    graph.add((poc[currentAnnotationBody], ohdsi['RxnormDrug'], rxnorm[rxcuiDrug]))
    #graph.add((poc[currentAnnotationBody], poc['MeshDrug'], mesh[meshDrug])) # TODO: consider adding the values as a collection
                        
    graph.add((poc[currentAnnotationBody], ohdsi['MeddrraHoi'], meddra[elt["CONDITION_CONCEPT_ID"]])) # TODO: consider adding the values as a collection


# display the graph
f = codecs.open(OUTPUT_FILE,"w","utf8")
#graph.serialize(destination=f,format="xml",encoding="utf8")
s = graph.serialize(format="xml",encoding="utf8")

#f.write(graph.serialize(format="xml",encoding="utf8"))
f.write(unicode(s,errors='replace'))
#print graph.serialize(format="xml")
f.close

graph.close()
