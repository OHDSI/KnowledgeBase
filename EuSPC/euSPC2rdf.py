# euSPC2rdf.py
#
# Convert the result of the European Union Adverse Drug Reactions from
# Summary of Product Characteristics (EU SPC) Database Import to Open
# Annotation Data
#
# Author: Richard D Boyce, PhD
# Summer and Fall 2014
#

import sys
sys.path = sys.path + ['.']

import re, codecs, uuid, datetime
import json
import pickle
from rdflib import Graph, Literal, Namespace, URIRef, RDF, RDFS

DATA_FILE = "data/FinalRepository_DLP30Jun2012_withCUIs_v2.csv"
(PRODUCT,SCIENTIFICGROUP_ID,SUBSTANCE,RxNorm,MeSH,DATE_OF_THE_SPC,ADR_AS_IT_APPEARS_IN_THE_SPC,SOC,HLGT,HLT,LLT,MEDDRA_PT,PT_CODE,SOC_CODE,AGE_GROUP,GENDER,CAUSALITY,FREQUENCY,CLASS_WARNING,CLINICAL_TRIALS,POST_MARKETING,COMMENT) = range(0,22)


# TERMINOLOGY MAPPING FILES
RXNORM_TO_OMOP = "../terminology-mappings/StandardVocabToRxNorm/imeds_drugids_to_rxcuis.csv"
MEDDRA_TO_OMOP = "../terminology-mappings/StandardVocabToMeddra/imeds_conceptids_to_meddra.csv"

# OUTPUT DATA FILE
OUTPUT_FILE = "drug-hoi-eu-spc.nt"

DRUGS_D_OMOP = {}
f = open(RXNORM_TO_OMOP,"r")
buf = f.read()
f.close()
l = buf.split("\n")
for elt in l:
    if elt.strip() == "":
        break

    (omop,rxcui) = [x.strip() for x in elt.split("|")]
    DRUGS_D_OMOP[rxcui] = omop

MEDDRA_D_OMOP = {}
f = open(MEDDRA_TO_OMOP,"r")
buf = f.read()
f.close()
l = buf.split("\n")
for elt in l[1:]:
    if elt.strip() == "":
        break

    (omop,meddra) = [x.strip() for x in elt.split("|")]
    MEDDRA_D_OMOP[meddra] = omop


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
poc = Namespace('http://purl.org/net/nlprepository/ohdsi-adr-eu-spc-poc#')

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
graph.namespace_manager.bind('poc','http://purl.org/net/nlprepository/ohdsi-adr-eu-spc-poc#')

## TODO: add datatype=XSD.string to all string Literals and port queries appropriately

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

annotatedCache = {} # indexes annotation ids so that multiple bodies can be attached
currentAnnotation = annotationItemCntr

currentAnnotSet = 'ohdsi-eu-spc-annotation-set-%s' % annotationSetCntr 
annotationSetCntr += 1
graph.add((poc[currentAnnotSet], RDF.type, oa["DataAnnotation"])) # TODO: find out what is being used for collections in OA
graph.add((poc[currentAnnotSet], oa["annotatedAt"], Literal(datetime.date.today())))
graph.add((poc[currentAnnotSet], oa["annotatedBy"], URIRef(u"http://www.pitt.edu/~rdb20/triads-lab.xml#TRIADS")))

outf = codecs.open(OUTPUT_FILE,"w","utf8")
s = graph.serialize(format="n3",encoding="utf8", errors="replace")
outf.write(s)

# DEBUG
cntr = 0 

inf = open(DATA_FILE, 'r')
buf = inf.read()
inf.close()
lines = buf.split("\n")
it = [unicode(x.strip(),'utf-8', 'replace').split("\t") for x in lines[1:]] # skip header
for elt in it:
    if elt == [u'']:
        break 

    #if cntr == 50000:
    #    break
    cntr += 1
    print cntr
    
    rxcuiDrug = elt[RxNorm]
    meshDrug = elt[MeSH]
    drugLabs = elt[SUBSTANCE]
    imedsDrug = None
    if DRUGS_D_OMOP.has_key(rxcuiDrug):
        imedsDrug = DRUGS_D_OMOP[rxcuiDrug]
        print "INFO: rxcuiDrug : %s" % rxcuiDrug
    else:
        print "WARNING: skipping rxcuiDrug, no mapping to OMOP : %s" % rxcuiDrug
        continue

    imedsHoi = None
    if MEDDRA_D_OMOP.has_key(elt[PT_CODE]):
        imedsHoi = MEDDRA_D_OMOP[elt[PT_CODE]]
        print "INFO: meddraHoi : %s" % elt[PT_CODE]
    else:
        print "WARNING: skipping rxcuiDrug %s + meddra HOI %s : unable to map HOI to OMOP" % (rxcuiDrug, elt[PT_CODE])
        continue


    ###################################################################
    ### Each annotations holds one target that points to the source
    ### record in DailyMed, and one or more bodies each of which
    ### indicates the MedDRA terms that triggered the result and holds
    ### some metadata
    ###################################################################
    currentAnnotItem = None

    if annotatedCache.has_key(cntr):
        currentAnnotation = annotatedCache[cntr]
        currentAnnotItem = "ohdsi-eu-spc-annotation-item-%s" % currentAnnotation
    else:
        currentAnnotation = annotationItemCntr
        annotatedCache[cntr] = currentAnnotation
        annotationItemCntr += 1
        
        currentAnnotItem = "ohdsi-eu-spc-annotation-item-%s" % currentAnnotation

        tplL = []
        #tplL.append((poc[currentAnnotSet], aoOld["item"], poc[currentAnnotItem])) # TODO: find out what is being used for items of collections in OA
        tplL.append((poc[currentAnnotItem], RDF.type, oa["DataAnnotation"]))
        tplL.append((poc[currentAnnotItem], RDF.type, ohdsi["ADRAnnotation"]))
        tplL.append((poc[currentAnnotItem], oa["annotatedAt"], Literal(datetime.date.today())))
        tplL.append((poc[currentAnnotItem], oa["annotatedBy"], URIRef(u"http://www.pitt.edu/~rdb20/triads-lab.xml#TRIADS")))
        tplL.append((poc[currentAnnotItem], oa["motivatedBy"], oa["tagging"]))
        # TODO: add in PROV wasGeneratedBY

        currentAnnotTargetUuid = URIRef(u"urn:uuid:%s" % uuid.uuid4())
        tplL.append((poc[currentAnnotItem], oa["hasTarget"], currentAnnotTargetUuid))
        tplL.append((currentAnnotTargetUuid, RDF.type, oa["SpecificResource"]))
        tplL.append((currentAnnotTargetUuid, oa["hasSource"], URIRef(u"http://www.imi-protect.eu/adverseDrugReactions.shtml")))

        s = ""
        for t in tplL:
            s += unicode.encode(" ".join((t[0].n3(), t[1].n3(), t[2].n3(), u".\n")), 'utf-8', 'replace')
        outf.write(s)
                
    # TODO: EU ADR data has nothing to use for OA:Selector at this
    # time. Work with UMC to get links to the original SPC documents
    # annotated

    # Specify the bodies of the annotation - for this type each
    # body contains the drug and condition as a semantic tags
    currentAnnotationBody = "ohdsi-eu-spc-annotation-body-%s" % annotationBodyCntr
    annotationBodyCntr += 1
    
    tplL = []
    tplL.append((poc[currentAnnotItem], oa["hasBody"], poc[currentAnnotationBody]))
    tplL.append((poc[currentAnnotationBody], RDFS.label, Literal(u"Drug-HOI tag for %s-%s" % (imedsDrug, imedsHoi))))
    tplL.append((poc[currentAnnotationBody], RDF.type, ohdsi["adrAnnotationBody"])) # TODO: this is not yet formalized in a public ontology but should be

    tplL.append((poc[currentAnnotationBody], dcterms["description"], Literal(u"Drug-HOI tag for %s (rxnorm) - %s" % (rxcuiDrug, elt[MEDDRA_PT]))))
    tplL.append((poc[currentAnnotationBody], ohdsi['ImedsDrug'], ohdsi[imedsDrug]))
    tplL.append((poc[currentAnnotationBody], ohdsi['RxnormDrug'], rxnorm[rxcuiDrug]))
                        
    tplL.append((poc[currentAnnotationBody], ohdsi['MeddrraHoi'], meddra[elt[PT_CODE]])) # TODO: consider adding the values as a collection
    tplL.append((poc[currentAnnotationBody], ohdsi['ImedsHoi'], ohdsi[imedsHoi])) # TODO: consider adding the values as a collection
    s = ""
    for t in tplL:
        s += unicode.encode(" ".join((t[0].n3(), t[1].n3(), t[2].n3(), u".\n")), 'utf-8', 'replace')
    outf.write(unicode(s,'utf-8', 'replace'))

outf.close

graph.close()
