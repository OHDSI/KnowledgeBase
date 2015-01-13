# semMedSearch2rdf.py
#
# Convert the result of a SemMedDB drug-HOI evidence search to Open Data Annotation
#
# Author: Richard D Boyce, PhD
# 2014/2015
#

import sys
sys.path = sys.path + ['.']

import re, codecs, uuid, datetime
import json
from rdflib import Graph, Literal, Namespace, URIRef, RDF, RDFS
from lxml import etree
from lxml.etree import XMLParser, parse

import psycopg2 # for postgres 

## The result of selectTriplesPlusSentence.py (see README)
SEARCH_RESULTS = "semmedTriplesPlusSentence.tsv"

# TERMINOLOGY MAPPING FILES 
## NOTE: the drug concepts are mapped directly to RxNorm here but the
##       HOIs are retained as MeSH and then mapped using the Standard
##       Vocabu lary at load time by the code in
##       Schema/postgres/mergeCountsFromIntegratedSources.py based on
##       config information present in
##       Schema/postgres/integratedSources.conf
RXNORM_TO_MESH = "../terminology-mappings/RxNorm-to-MeSH/mesh-to-rxnorm-standard-vocab-v5.txt"
MESH_TO_STANDARD_VOCAB = "../terminology-mappings/StandardVocabToMeSH/mesh-to-standard-vocab-v5.txt"
MESH_PHARMACOLOGIC_ACTION_MAPPINGS = "../terminology-mappings/MeSHPharmocologicActionToSubstances/pa2015.xml"

# OUTPUT DATA FILE
OUTPUT_FILE = "drug-hoi-pubmed-semmed.nt"

# Connecting to the MEDLINE DB
DB_CONNECTION_INFO="db-connection-MEDLINE.conf"
## Set up the db connection
f = open(DB_CONNECTION_INFO,'r')
(db,user,pword,host,port) = f.readline().strip().split("\t")
f.close()
try:
    conn=psycopg2.connect(database=db, user=user, password=pword, host=host, port=port)
except Exception as e:
    print "ERROR: Unable to connect to database %s (user:%s) on host %s (port: %s). Check that the data in db-connection.conf is correct and that there is not barrier related to the network connection. Error: %s" % (db,user,host,port,e)
    sys.exit(1)
cur = conn.cursor()


############################################################
#  Load the  MeSH Pharmacologic Action mappings from an XML file
############################################################
pharmActionMaptD = {}
p = XMLParser(huge_tree=True)
tree = parse(MESH_PHARMACOLOGIC_ACTION_MAPPINGS, parser=p)
l = tree.xpath('PharmacologicalAction')
for elt in l:
    descriptorUI = elt.xpath('DescriptorReferredTo/DescriptorUI')[0].text
    descriptorName = elt.xpath('DescriptorReferredTo/DescriptorName/String')[0].text
    pharmacologicalActionSubstanceL = elt.xpath('PharmacologicalActionSubstanceList/Substance')
    substancesL = []
    for substanceElt in pharmacologicalActionSubstanceL:
        recordUI = substanceElt.xpath('RecordUI')[0].text
        recordName = substanceElt.xpath('RecordName/String')[0].text
        substancesL.append({'recordUI':recordUI,'recordName':recordName})

    pharmActionMaptD[descriptorUI] = {'descriptorName':descriptorName, 'substancesL':substancesL}

############################################################
#  Load the Drug ad HOI mappings that include OHDSI Standard Vocab codes
############################################################
DRUGS_D = {}
DRUGS_D_RXNORM = {}
f = open(RXNORM_TO_MESH,"r")
buf = f.read()
f.close()
l = buf.split("\n")
for elt in l[1:]:
    if elt.strip() == "":
        break

    (mesh,pt,rxcui,concept_name,ohdsiID,conceptClassId) = [x.strip() for x in elt.split("|")]
    if DRUGS_D.get(mesh): # add a synonymn
        DRUGS_D[mesh][1].append(pt)
    else: # create a new record
        DRUGS_D[mesh] = (rxcui, [pt], ohdsiID)
    
    if DRUGS_D_RXNORM.get(rxcui): # add a synonymn
        DRUGS_D_RXNORM[rxcui][1].append(pt)
    else: # create a new record
        DRUGS_D_RXNORM[rxcui] = (mesh, [pt], ohdsiID)


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

############################################################
## set up an RDF Open Annotation Data  graph
############################################################
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
umls = Namespace('http://linkedlifedata.com/resource/umls/id/')
mesh = Namespace('http://purl.bioontology.org/ontology/MESH/')
meddra = Namespace('http://purl.bioontology.org/ontology/MEDDRA/')
rxnorm = Namespace('http://purl.bioontology.org/ontology/RXNORM/')
pubmed = Namespace('http://www.ncbi.nlm.nih.gov/pubmed/')
snomed = Namespace('http://purl.bioontology.org/ontology/SNOMEDCT/')
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
graph.namespace_manager.bind('umls','http://linkedlifedata.com/resource/umls/id/')
graph.namespace_manager.bind('mesh', 'http://purl.bioontology.org/ontology/MESH/')
graph.namespace_manager.bind('meddra','http://purl.bioontology.org/ontology/MEDDRA/')
graph.namespace_manager.bind('snomed','http://purl.bioontology.org/ontology/SNOMEDCT/')
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

graph.add((poc['UmlsDrug'], RDFS.label, Literal("UMLS Drug code")))
graph.add((poc['UmlsDrug'], dcterms["description"], Literal("Drug code in the UMLS vocabulary.")))

graph.add((poc['MeshDrug'], RDFS.label, Literal("MeSH Drug code")))
graph.add((poc['MeshDrug'], dcterms["description"], Literal("Drug code in the MeSH vocabulary.")))

graph.add((poc['RxnormDrug'], RDFS.label, Literal("Rxnorm Drug code")))
graph.add((poc['RxnormDrug'], dcterms["description"], Literal("Drug code in the Rxnorm vocabulary.")))

graph.add((poc['UmlsHoi'], RDFS.label, Literal("UMLS HOI code")))
graph.add((poc['UmlsHoi'], dcterms["description"], Literal("HOI code in the UMLS vocabulary.")))

graph.add((poc['MeshHoi'], RDFS.label, Literal("MeSH HOI code")))
graph.add((poc['MeshHoi'], dcterms["description"], Literal("HOI code in the MeSH vocabulary.")))

graph.add((poc['SnomedHoi'], RDFS.label, Literal("SNOMED HOI code")))
graph.add((poc['SnomedHoi'], dcterms["description"], Literal("HOI code in the SNOMED vocabulary.")))

graph.add((poc['MeddraHoi'], RDFS.label, Literal("Meddra HOI code")))
graph.add((poc['MeddraHoi'], dcterms["description"], Literal("HOI code in the Meddra vocabulary.")))

################################################################################

# Load the results of querying SemMedDB for predicates indicating drug - HOI associations 
# TODO: consider using an iterator for this
(PMID, PREDICATE, PREDICATE_START_INDEX, PREDICATE_END_INDEX, DRUG_UMLS_CUI, DRUG_RXNORM, DRUG_MESH, DRUG_PREFERRED_TERM, DRUG_UMLS_ENTITY_TYPE, DRUG_START_INDEX, DRUG_END_INDEX, DRUG_DISTANCE, DRUG_MAX_DISTANCE, DRUG_MAX_SCORE, HOI_UMLS_CUI, HOI_SNOMED, HOI_MEDDRA, HOI_MESH, HOI_PREFERRED_TERM, HOI_UMLS_ENTITY_TYPE, HOI_START_INDEX, HOI_END_INDEX, HOI_DISTANCE, HOI_MAX_DISTANCE, HOI_SCORE, SENTENCE, SENTENCE_LOCATION, SENTENCE_TYPE) = range(0,28)
f = open(SEARCH_RESULTS,'r')
buf = f.read()
f.close()
recL = [x.strip().split("\t") for x in buf.strip().split("\n")]
recL.pop(0) # remove the header line

# Start building the open annotation data graph
annotationSetCntr = 1
annotationItemCntr = 1
annotationBodyCntr = 1
annotationEvidenceCntr = 1

annotatedCache = {} # indexes annotation ids by pmid
pubTypeCache = {} # used because some PMIDs have multiple publication type assignments TODO: determine pub types should be assigned to a Collection under the target's graph 
drugHoiPMIDCache = {} # used to avoid duplicating PMID - drug  - HOI combos for PMIDs that have multiple publication type assignments TODO: determine if a more robust source query is needed
currentAnnotation = annotationItemCntr

currentAnnotSet = 'ohdsi-semmed-annotation-set-%s' % annotationSetCntr 
annotationSetCntr += 1
graph.add((poc[currentAnnotSet], RDF.type, oa["DataAnnotation"])) # TODO: find out what is being used for collections in OA
graph.add((poc[currentAnnotSet], oa["annotatedAt"], Literal(datetime.date.today())))
graph.add((poc[currentAnnotSet], oa["annotatedBy"], URIRef(u"http://www.pitt.edu/~rdb20/triads-lab.xml#TRIADS")))

f = codecs.open(OUTPUT_FILE,"w","utf8")
s = graph.serialize(format="n3",encoding="utf8", errors="replace")
f.write(s)

for elt in recL[0:3]:  
    ###################################################################
    ### Each annotations holds one target that points to the source
    ### record in pubmed, and one or more bodies each of which
    ### indicates the MeSH terms that triggered the result and holds
    ### some metadata
    ###################################################################
    currentAnnotItem = None
    createNewTarget = False
    tplL = []
    if annotatedCache.has_key(elt[PMID]):
        currentAnnotation = annotatedCache[elt[PMID]]
        pubTypeL = pubTypeCache[elt[PMID]]
        # if elt[PUB_TYPE] not in pubTypeL:
        #     print "INFO: MEDLINE record %s has more than one pub type assigned" % elt[PMID]
        #     pubTypeCache[elt[PMID]].append(elt[PUB_TYPE])
        #     if elt[PUB_TYPE] == "Clinical Trial": 
        #         tplL.append((currentAnnotTargetUuid, ohdsi["MeshStudyType"], Literal("clinical trial (publication type)")))
        #     elif elt[PUB_TYPE] == "Case Reports": 
        #         tplL.append((currentAnnotTargetUuid, ohdsi["MeshStudyType"], Literal("case reports (publication type)")))
        #     elif elt[PUB_TYPE] == "Meta-Analysis": 
        #         tplL.append((currentAnnotTargetUuid, ohdsi["MeshStudyType"], Literal("other (publication type)")))
    else:
        currentAnnotation = annotationItemCntr
        annotatedCache[elt[PMID]] = currentAnnotation
        annotationItemCntr += 1
        createNewTarget = True
    
    currentAnnotItem = "ohdsi-semmed-annotation-item-%s" % currentAnnotation

    if createNewTarget:
        tplL.append((poc[currentAnnotSet], aoOld["item"], poc[currentAnnotItem])) # TODO: find out what is being used for items of collections in OA
        tplL.append((poc[currentAnnotItem], RDF.type, oa["DataAnnotation"])) 
        tplL.append((poc[currentAnnotItem], RDF.type, ohdsi["SemMedDrugHOIAnnotation"])) # TODO: should be a subclass of oa:DataAnnotation
        tplL.append((poc[currentAnnotItem], oa["annotatedAt"], Literal(datetime.date.today())))
        tplL.append((poc[currentAnnotItem], oa["annotatedBy"], URIRef(u"http://www.pitt.edu/~rdb20/triads-lab.xml#TRIADS")))
        tplL.append((poc[currentAnnotItem], oa["motivatedBy"], oa["tagging"]))
        
        currentAnnotTargetUuid = URIRef(u"urn:uuid:%s" % uuid.uuid4())
        tplL.append((poc[currentAnnotItem], oa["hasTarget"], currentAnnotTargetUuid))
        tplL.append((currentAnnotTargetUuid, RDF.type, oa["SpecificResource"]))
        tplL.append((currentAnnotTargetUuid, oa["hasSource"], pubmed[elt[PMID]]))

        # TODO: use the MeSH UIs to generate purls for the pub types
        # TODO: add more publication types
        # NOTE: a change here requires a change up above!
        # pubTypeCache[elt[PMID]] = [elt[PUB_TYPE]]
        # if elt[PUB_TYPE] == "Clinical Trial": 
        #     tplL.append((currentAnnotTargetUuid, ohdsi["MeshStudyType"], Literal("clinical trial (publication type)")))
        # elif elt[PUB_TYPE] == "Case Reports": 
        #     tplL.append((currentAnnotTargetUuid, ohdsi["MeshStudyType"], Literal("case reports (publication type)")))
        # elif elt[PUB_TYPE] == "Meta-Analysis": 
        #     tplL.append((currentAnnotTargetUuid, ohdsi["MeshStudyType"], Literal("other (publication type)")))

    s = ""
    for t in tplL:
        s += unicode.encode(" ".join((t[0].n3(), t[1].n3(), t[2].n3(), u".\n")), 'utf-8', 'replace')
    f.write(s)
    

    # Specify the bodies of the annotation - for this type each body
    # contains the MESH drug and UMLS condition as a semantic tag. If
    # possible, drug UIs from RxNorm, OHDSI/IMEDS Standard Vocab, and
    # MeSH are provided, and HOI UIs from SNOMED, MEDDRA, and MeSH are
    # also provided

    # to begin with, avoid duplicating PMID - drug  - HOI combos for PMIDs that have multiple publication type assignments
    concat = "%s-%s-%s" % (elt[PMID], elt[DRUG_MESH], elt[HOI_UMLS_CUI])
    if drugHoiPMIDCache.has_key(concat):
        print "INFO: skipping generation of a new body graph because the PMID, drug, and HOI (%s) have already been processed. Probably a MEDLINE record with multiple pub type assignments" % concat
        continue
    else:
        drugHoiPMIDCache[concat] = None

    currentAnnotationBody = "ohdsi-semmed-annotation-annotation-body-%s" % annotationBodyCntr
    annotationBodyCntr += 1

    tplL = []  # Clearing out the Target data tuple
    tplL.append((poc[currentAnnotItem], oa["hasBody"], poc[currentAnnotationBody]))
    tplL.append((poc[currentAnnotationBody], RDFS.label, Literal("Drug-HOI tag for PMID %s" % elt[PMID])))
    tplL.append((poc[currentAnnotationBody], RDF.type, ohdsi["OHDSIUMLSTags"])) # TODO: this is not yet formalized in a public ontology but should be
    tplL.append((poc[currentAnnotationBody], RDF.type, oa["SemanticTag"])) 
    tplL.append((poc[currentAnnotationBody], dcterms["description"], Literal("Drug-HOI body from PUBMED PMID %s using predicates in SemMedDB : drug %s (%s) and HOI %s (%s)" % (elt[PMID], elt[DRUG_PREFERRED_TERM], elt[DRUG_UMLS_CUI], elt[HOI_PREFERRED_TERM], elt[HOI_UMLS_CUI]))))

    ### INCLUDE THE UMLS TAGS FROM THE RECORD AS WELL AS OTHER
    ### AVAILABLE SEMANTIC TAGGING DATA FROM THE DRUG AND HOI QUERY
    tplL.append((poc[currentAnnotationBody], ohdsi['UmlsDrug'], umls[elt[DRUG_UMLS_CUI]])) 
    
    if elt[DRUG_MESH] != "":
        tplL.append((poc[currentAnnotationBody], ohdsi['MeshDrug'], mesh[elt[DRUG_MESH]])) 

        if DRUGS_D.has_key(elt[DRUG_MESH]): # the rxnorm cui might be in the dataset but the Standard Vocab is not
            tplL.append((poc[currentAnnotationBody], ohdsi['RxnormDrug'], rxnorm[DRUGS_D[elt[DRUG_MESH]][0]]))
            tplL.append((poc[currentAnnotationBody], ohdsi['ImedsDrug'], ohdsi[DRUGS_D[elt[DRUG_MESH]][2]]))
        elif elt[DRUG_MESH] in pharmActionMaptD.keys():
            (descriptorName, substancesL) =  (pharmActionMaptD[elt[DRUG_MESH]]['descriptorName'], pharmActionMaptD[elt[DRUG_MESH]]['substancesL'])
            print "INFO: The MeSH drug %s might be a grouping (%s). Attempting to expand to the %d individual drugs mapped in the MeSH pharmacologic action mapping" % (elt[DRUG_MESH], descriptorName, len(substancesL))
        
            collectionHead = URIRef(u"urn:uuid:%s" % uuid.uuid4()) # TODO: give this URI a type
            tplL.append((poc[currentAnnotationBody], ohdsi['adeAgents'], collectionHead))
            # add each substance to a collection in the body
            for substance in substancesL:
                tplL.append((collectionHead, ohdsi['MeshDrug'], mesh[substance['recordUI']]))
                if DRUGS_D.has_key(substance['recordUI']):
                    tplL.append((collectionHead, ohdsi['RxnormDrug'], rxnorm[DRUGS_D[substance['recordUI']][0]]))
                    tplL.append((collectionHead, ohdsi['ImedsDrug'], ohdsi[DRUGS_D[substance['recordUI']][2]]))
                else:
                    print "WARNING: no RxNorm or IMEDS equivalent to the MeSH drug %s (%s) belonging to the pharmacologic action mapping %s" % (substance['recordUI'], substance['recordName'], elt[DRUG_MESH])
        else:
            print "ERROR: no RxNorm equivalent to the MeSH drug %s (%s) and this does not appear in the pharmacologic action mapping (not a grouping?), skipping" % (elt[DRUG_MESH], elt[DRUG_PREFERRED_TERM])
            continue
    elif elt[DRUG_RXNORM] != "":
        tplL.append((poc[currentAnnotationBody], ohdsi['RxnormDrug'], rxnorm[elt[DRUG_RXNORM]]))

        if DRUGS_D_RXNORM.has_key(elt[DRUG_RXNORM]): 
            tplL.append((poc[currentAnnotationBody], ohdsi['ImedsDrug'], ohdsi[DRUGS_D_RXNORM[elt[DRUG_RXNORM]][2]]))
        else:
            print "WARNING: RxNorm drug mapping but no Standard Vocab mapping for the UMLS drug %s (%s)" % (elt[DRUG_UMLS_CUI], elt[DRUG_PREFERRED_TERM])
    else:
        print "WARNING: no MeSH or RxNorm drug mapping for the UMLS drug %s (%s)" % (elt[DRUG_UMLS_CUI], elt[DRUG_PREFERRED_TERM])
                                                                                    
    # TODO: for now, I am only using the UMLS HOI concept and the first SNOMED entry if it exists. This will need to be revised to use all available mappings in the dataset
    tplL.append((poc[currentAnnotationBody], ohdsi['UmlsHoi'], umls[elt[HOI_UMLS_CUI]]))
    if elt[HOI_SNOMED] != "":
        snomedValL = elt[HOI_SNOMED].split("|")
        tplL.append((poc[currentAnnotationBody], ohdsi['SnomedHoi'], snomed[snomedValL[0]]))
    else:
        print "WARNING: no SNOMED UI for the UMLS HOI %s (%s)" % (elt[HOI_UMLS_CUI], elt[HOI_PREFERRED_TERM])
    
    # if MESH_D_SV.has_key(elt[HOI_MESH]):
    #     tplL.append((poc[currentAnnotationBody], ohdsi['ImedsHoi'], ohdsi[MESH_D_SV[elt[HOI_MESH]]]))
    #     tplL.append((poc[currentAnnotationBody], ohdsi['MeshHoi'], mesh[elt[HOI_MESH]]))
    # else:
    #     print "ERROR: no OHDSI/IMEDS equivalent to the MeSH HOI %s, skipping" % (elt[DRUG_MESH])
    #     continue
 
    # # add the ADE effect to a collection in the body
    # if not adeEffectCollectionCache.has_key(elt[PMID]):
    #     collectionHead = URIRef(u"urn:uuid:%s" % uuid.uuid4())
    #     tplL.append((poc[currentAnnotationBody], ohdsi['adeEffects'], collectionHead))
    #     tplL.append((collectionHead, ohdsi['adeEffect'], Literal(elt[ADR_HOI_UI])))
    #     adeEffectCollectionCache[elt[PMID]] = [(elt[ADR_HOI_UI],collectionHead)]
    # else:
    #     effectTplL = adeEffectCollectionCache[elt[PMID]]
    #     prevEffectsL = [x[0] for x in effectTplL]
    #     if elt[ADR_HOI_UI] not in prevEffectsL:
    #         collectionHead = effectTplL[0][1] # pull the UUID already create for this collection head to add a new effect
    #         tplL.append((collectionHead, ohdsi['adeEffect'], Literal(elt[ADR_HOI_UI])))
    #         adeEffectCollectionCache[elt[PMID]].append((elt[ADR_HOI_UI],collectionHead))

    s = ""
    for t in tplL:
        s += unicode.encode(" ".join((t[0].n3(), t[1].n3(), t[2].n3(), u".\n")), 'utf-8', 'replace')
    f.write(s)


f.close
graph.close()
