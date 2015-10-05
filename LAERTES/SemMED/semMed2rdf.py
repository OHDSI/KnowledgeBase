# semMed2rdf.py
# -*- coding: utf-8 -*-
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

# use lxml to parse the MeSH pharmacologic action mappings
from lxml import etree
from lxml.etree import XMLParser, parse


import psycopg2 # for postgres

## The result of the query of SemMedDB (see README)
SEARCH_RESULTS = "semmedTriplesPlusSentence.tsv"

# OUTPUT DATA FILE
OUTPUT_FILE = "drug-hoi-pubmed-semmeddb.nt"

# Connection info to the MEDLINE database
DB_CONNECTION_INFO="db-connection.conf"

# number of characters used to creat the prefix and postfix text strings for TextQuoteSelectors
NUMB_CHARACTERS_PRE_AND_POST = 50 

# various mappings to the standard vocabulary
RXNORM_TO_MESH = "../terminology-mappings/RxNorm-to-MeSH/mesh-to-rxnorm-standard-vocab-v5.txt"
MESH_TO_STANDARD_VOCAB = "../terminology-mappings/StandardVocabToMeSH/mesh-to-standard-vocab-v5.txt"
MESH_PHARMACOLOGIC_ACTION_MAPPINGS = "../terminology-mappings/MeSHPharmocologicActionToSubstances/pa2015.xml"

SNOMED_TO_STANDARD_VOCAB = "../terminology-mappings/StandardVocabToSnomed/standard_vocab_conceptids_to_snomed.csv"
MEDDRA_TO_STANDARD_VOCAB = "../terminology-mappings/StandardVocabToMeddra/standard_vocab_to_meddra.csv"

## Set up the db connection to the MEDLINE DB. This is used to collect
## a bit more information on the MEDLINE entries than is provided by
## SemMedDB
f = open(DB_CONNECTION_INFO,'r')
(db,user,pword,host,port) = f.readline().strip().split("\t")
f.close()
try:
    conn=psycopg2.connect(database=db, user=user, password=pword, host=host, port=port)
except Exception as e:
    print "ERROR: Unable to connect to database %s (user:%s) on host %s (port: %s). Check that the data in db-connection.conf is correct and that there is not barrier related to the network connection. Error: %s" % (db,user,host,port,e)
cur = conn.cursor()

############################################################
#  Load the MeSH Pharmacologic Action mappings from an XML file
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
#  Load the Drug and HOI mappings that include OHDSI Standard Vocab codes
############################################################
DRUGS_D_MESH_KEYED = {}
DRUGS_D_RXNORM_KEYED = {}
f = open(RXNORM_TO_MESH,"r")
buf = f.read()
f.close()
l = buf.split("\n")
for elt in l[1:]:
    if elt.strip() == "":
        break

    (mesh,pt,rxcui,concept_name,ohdsiID,conceptClassId) = [x.strip() for x in elt.split("|")]
    if DRUGS_D_MESH_KEYED.get(mesh): # add a synonymn
        DRUGS_D_MESH_KEYED[mesh][1].append(pt)
    else: # create a new record
        DRUGS_D_MESH_KEYED[mesh] = (rxcui, [pt], ohdsiID)

    if DRUGS_D_RXNORM_KEYED.get(rxcui): # add a synonymn
        DRUGS_D_RXNORM_KEYED[rxcui][1].append(pt)
    else: # create a new record
        DRUGS_D_RXNORM_KEYED[rxcui] = (mesh, [pt], ohdsiID)

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

SNOMED_D_SV = {}
f = open(SNOMED_TO_STANDARD_VOCAB, "r")
buf = f.read()
f.close()
l = buf.split("\n")
for elt in l[1:]: # skip header
    if elt.strip() == "":
        break

    (imeds,snomed) = [x.strip() for x in elt.split("|")]
    SNOMED_D_SV[snomed] = imeds


MEDDRA_D_SV = {}
f = open(MEDDRA_TO_STANDARD_VOCAB, "r")
buf = f.read()
f.close()
l = buf.split("\n")
for elt in l[1:]: # skip header
    if elt.strip() == "":
        break

    (imeds,meddra) = [x.strip() for x in elt.split("|")]
    MEDDRA_D_SV[meddra] = imeds

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
snomed = Namespace('http://purl.bioontology.org/ontology/SNOMEDCT/')
pubmed = Namespace('http://www.ncbi.nlm.nih.gov/pubmed/')
ohdsi = Namespace('http://purl.org/net/ohdsi#')
poc = Namespace('http://purl.org/net/nlprepository/ohdsi-pubmed-semmed-poc#')

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
graph.namespace_manager.bind('umls', 'http://linkedlifedata.com/resource/umls/id/')
graph.namespace_manager.bind('mesh', 'http://purl.bioontology.org/ontology/MESH/')
graph.namespace_manager.bind('meddra','http://purl.bioontology.org/ontology/MEDDRA/')
graph.namespace_manager.bind('rxnorm','http://purl.bioontology.org/ontology/RXNORM/')
graph.namespace_manager.bind('snomed','http://purl.bioontology.org/ontology/SNOMEDCT/')
graph.namespace_manager.bind('pubmed', 'http://www.ncbi.nlm.nih.gov/pubmed/')
graph.namespace_manager.bind('ohdsi', 'http://purl.org/net/ohdsi#')
graph.namespace_manager.bind('poc','http://purl.org/net/nlprepository/ohdsi-pubmed-semmed-poc#')

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

graph.add((poc['UMLSDrug'], RDFS.label, Literal("UMLS Drug code")))
graph.add((poc['UMLSDrug'], dcterms["description"], Literal("Drug code in the UMLS.")))

graph.add((poc['MeshDrug'], RDFS.label, Literal("MeSH Drug code")))
graph.add((poc['MeshDrug'], dcterms["description"], Literal("Drug code in the MeSH vocabulary.")))

graph.add((poc['RxnormDrug'], RDFS.label, Literal("Rxnorm Drug code")))
graph.add((poc['RxnormDrug'], dcterms["description"], Literal("Drug code in the Rxnorm vocabulary.")))

graph.add((poc['UMLSHoi'], RDFS.label, Literal("UMLS HOI code")))
graph.add((poc['UMLSHoi'], dcterms["description"], Literal("HOI code in the UMLS vocabulary.")))

graph.add((poc['MeshHoi'], RDFS.label, Literal("MeSH HOI code")))
graph.add((poc['MeshHoi'], dcterms["description"], Literal("HOI code in the MeSH vocabulary.")))

graph.add((poc['MeddraHoi'], RDFS.label, Literal("Meddra HOI code")))
graph.add((poc['MeddraHoi'], dcterms["description"], Literal("HOI code in the Meddra vocabulary.")))

## TODO: The namespace for these entities should be 'umls'. Find out
## why linked life data does not include the Semantic Network
## predicates.
graph.add((poc['modality'], RDFS.label, Literal("modality")))
graph.add((poc['modality'], dcterms["description"], Literal("The epistemic modality of an assertion. For now, this can only be 'positive' or 'negative'")))

graph.add((poc['semanticNetworkPredicate'], RDFS.label, Literal("semanticNetworkPredicate")))
graph.add((poc['semanticNetworkPredicate'], dcterms["description"], Literal("A UMLS Semantic Network predicate tag")))

# 'DISRUPTS',
graph.add((poc['T146'], RDFS.label, Literal("disrupts")))
graph.add((poc['T146'], dcterms["description"], Literal("Alters or influences an already existing condition, state, or situation.")))

# 'NEG_DISRUPTS'
## use  'negative' modality with NEG_DISRUPTS


# 'CAUSES',
graph.add((poc['T147'], RDFS.label, Literal("causes")))
graph.add((poc['T147'], dcterms["description"], Literal("Brings about a condition or an effect. Implied here is that an agent, such as for example, a pharmacologic substance or an organism, has brought about the effect. This includes induces, effects, evokes, and etiology.||||CA|caused_by.")))

# 'NEG_CAUSES',
## use  'negative' modality with 'CAUSES'

# 'AFFECTS',
graph.add((poc['T151'], RDFS.label, Literal("affects")))
graph.add((poc['T151'], dcterms["description"], Literal("Produces a direct effect on. Implied here is the altering or influencing of an existing condition, state, situation, or entity. This includes has a role in, alters, influences, predisposes, catalyzes, stimulates, regulates, depresses, impedes, enhances, contributes to, leads to, and modifies.")))

# 'NEG_AFFECTS',
## use  'negative' modality with AFFECTS

# 'ASSOCIATED_WITH',
graph.add((poc['T166'], RDFS.label, Literal("associated_with")))
graph.add((poc['T166'], dcterms["description"], Literal("has a significant or salient relationship to.")))

# 'NEG_ASSOCIATED_WITH',
## use  'negative' modality with ASSOCIATED_WITH

# 'COMPLICATES',
graph.add((poc['T149'], RDFS.label, Literal("complicates")))
graph.add((poc['T149'], dcterms["description"], Literal("Causes to become more severe or complex or results in adverse effects")))

# 'NEG_COMPLICATES',
## use  'negative' modality with NEG_COMPLICATES



################################################################################

# Load the results of querying for selected predicates from Kilicoglu et al. to SemMedDB
# TODO: consider using an iterator for this
(PMID, PREDICATE, PREDICATE_START_INDEX, PREDICATE_END_INDEX, DRUG_UMLS_CUI, DRUG_RXNORM, DRUG_MESH, DRUG_PREFERRED_TERM, DRUG_UMLS_ENTITY_TYPE, DRUG_START_INDEX, DRUG_END_INDEX, DRUG_DISTANCE, DRUG_MAX_DISTANCE, DRUG_MAX_SCORE, HOI_UMLS_CUI, HOI_SNOMED, HOI_MEDDRA, HOI_MESH, HOI_PREFERRED_TERM, HOI_UMLS_ENTITY_TYPE, HOI_START_INDEX, HOI_END_INDEX, HOI_DISTANCE, HOI_MAX_DISTANCE, HOI_SCORE, SENTENCE, SENTENCE_LOCATION, SENTENCE_TYPE) = range(0,28)
f = open(SEARCH_RESULTS,'r')
buf = f.read()
f.close()
recL = [x.strip().split("\t") for x in buf.strip().split("\n")]
recL.pop(0)

# Start building the open annotation data graph
annotationSetCntr = 1
annotationItemCntr = 1
annotationBodyCntr = 1
annotationEvidenceCntr = 1

annotatedCache = {} # indexes annotation ids by pmid-drug-hoi
abstractCache = {} # cache for abstract text
pubTypeCache = {} # used because some PMIDs have multiple publication type assignments TODO: determine pub types should be assigned to a Collection under the target's graph 
drugHoiPMIDCache = {} # used to avoid duplicating PMID - drug  - HOI combos for PMIDs that have multiple publication type assignments TODO: determine if a more robust source query is needed
currentAnnotation = annotationItemCntr

currentAnnotSet = 'ohdsi-pubmed-semmed-annotation-set-%s' % annotationSetCntr 
annotationSetCntr += 1
graph.add((poc[currentAnnotSet], RDF.type, oa["DataAnnotation"])) # TODO: find out what is being used for collections in OA
graph.add((poc[currentAnnotSet], oa["annotatedAt"], Literal(datetime.date.today())))
graph.add((poc[currentAnnotSet], oa["annotatedBy"], URIRef(u"http://www.pitt.edu/~rdb20/triads-lab.xml#TRIADS")))

f = codecs.open(OUTPUT_FILE,"w","utf8")
s = graph.serialize(format="n3",encoding="utf8", errors="replace")
f.write(s)

#for elt in recL[0:50]:  
for elt in recL:  
    ## Only process papers of specific publication types
    # TODO: use the MeSH UIs to generate purls for the pub types
    # TODO: add more publication types
    if not pubTypeCache.has_key(elt[PMID]):
        try:
            print "INFO: Attempting to get publication types for PMID %s from the MEDLINE DB" % elt[PMID]
            cur.execute("""SELECT value FROM medcit_art_publicationtypelist_publicationtype WHERE pmid = %s AND value IN ('Case Reports','Clinical Trial','Meta-Analysis','Comparative Study','Multicenter Study','Journal Article')""" % elt[PMID])
        except Exception as e:
            print "ERROR: Attempt to get publication types for PMID failed. Error string: %s" % e
            sys.exit(1)

        rows = cur.fetchall()
        if len(rows) == 0:
            print "WARNING: None of the selected publication types found for PMID %s. Skipping this record." % elt[PMID]
            continue 
            
        pubTypeCache[elt[PMID]] = [x[0] for x in rows]
        print "%s" % pubTypeCache[elt[PMID]]

    # get abstract if not already cached
    if not abstractCache.has_key(elt[PMID]):
        try:
            print "INFO: Attempting to retrieve the abstract for PMID %s from the MEDLINE DB" % elt[PMID]
            cur.execute("""SELECT value,label,medcit_art_abstract_abstracttext_order  FROM medcit_art_abstract_abstracttext WHERE pmid = %s ORDER BY medcit_art_abstract_abstracttext_order""" % elt[PMID])
        except Exception as e:
            print "ERROR: Attempt to get the abstract for PMID failed. Error string: %s" % e
            sys.exit(1)

        rows = cur.fetchall()
        if len(rows) == 0:
            abstractCache[elt[PMID]] = ""
            print "INFO: No abstract found for PMID %s." % elt[PMID]
        elif rows[0][1] != None:
            print "INFO: Abstract found for PMID %s and it appears to be a structured abstract. Concatenating all parts of the structured abstract." % elt[PMID]
            structAbstr = ""
            for ii in range(0,len(rows)):
                secLab = rows[ii][1]
                if secLab.upper() == 'UNLABELLED':
                    structAbstr += "%s " % (rows[ii][0])
                else:
                    structAbstr += "%s: %s " % (secLab,rows[ii][0])
            abstractCache[elt[PMID]] = structAbstr
            print "%s" % abstractCache[elt[PMID]]            
        else:
            abstractCache[elt[PMID]] = rows[0][0]
            print "%s" % abstractCache[elt[PMID]]


    ###################################################################
    ### A new annotation is created for each pmid-drug-hoi
    ### triple. Each annotation holds one target that points to the
    ### source record in pubmed, and one or more bodies each of which
    ### indicates the SNOMED and/or MeSH terms that triggered the
    ### result and holds some metadata
    ###################################################################
    currentAnnotItem = None
    createNewTarget = False
    tplL = []
    anotKey = "%s-%s-%s" % (elt[PMID],elt[DRUG_UMLS_CUI],elt[HOI_UMLS_CUI])
    if annotatedCache.has_key(anotKey):
        currentAnnotation = annotatedCache[anotKey]
    else:
        currentAnnotation = annotationItemCntr
        annotatedCache[anotKey] = currentAnnotation
        annotationItemCntr += 1
        createNewTarget = True
    
    currentAnnotItem = "ohdsi-pubmed-semmed-annotation-item-%s" % currentAnnotation

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

        # add a predicate for EACH publication type (some medline
        # records have more than one assignment)
        ctFlg = crFlg = otherFlg = False # make sure only one of each type is added to the graph 
        for pt in pubTypeCache[elt[PMID]]:
            if pt == "Clinical Trial" and ctFlg == False: 
                tplL.append((currentAnnotTargetUuid, ohdsi["MeshStudyType"], Literal("clinical trial (publication type)")))
                ctFlg = True
            if pt == "Case Reports" and crFlg == False: 
                tplL.append((currentAnnotTargetUuid, ohdsi["MeshStudyType"], Literal("case reports (publication type)")))
                crFlg = True
            if pt in ['Meta-Analysis','Comparative Study','Multicenter Study','Journal Article'] and otherFlg == False: 
                tplL.append((currentAnnotTargetUuid, ohdsi["MeshStudyType"], Literal("other (publication type)")))
                otherFlg = True
                
        # add the text quote selector. Sentences from titles will only
        # have an "exact". 
        # TODO: test that this approach is sufficient (i.e., no titles have more than one sentence.
        elt[SENTENCE] = elt[SENTENCE].replace("UNLABELLED: ","").replace("CONLCUSION:","CONCLUSION:").replace("        "," ").replace("       "," ").replace("hyperkalemia >/= 9.0","hyperkalemia >= 9.0").replace("alternative therapies  for RLS","alternative therapies for RLS").replace("hepatic  failure","hepatic failure").replace("are not yet  accessible","are not yet accessible").replace('""','"').strip('"') # TODO: this was a temporary bug fix because for some unknown reason extra whitespace and extra quotes was inserted into the exact sentence text in SemMedDB
        textConstraintUuid = URIRef("urn:uuid:%s" % uuid.uuid4())
        tplL.append((currentAnnotTargetUuid, oa["hasSelector"], textConstraintUuid))         
        tplL.append((textConstraintUuid, RDF.type, oa["TextQuoteSelector"]))
        tplL.append((textConstraintUuid, oa["exact"], Literal(elt[SENTENCE])))
        
        # if the sentence if from an abstract, retrieve the pre and
        # post text string from the abstract
        if elt[SENTENCE_TYPE] == 'ab':
            abstractTxt = abstractCache[elt[PMID]]
            abstractTxt = abstractTxt.replace("¿","?").replace("·",".").replace("²","2").replace("μ","mu").replace("₂","2").replace("α","alpha").replace("β","beta").replace("…","...").replace("≥",">=").replace("≤","</=").replace(" = "," = ").replace(" "," ").replace(" >= "," >= ").replace(" "," ").replace(" "," ").replace("ï","i").replace("×","x").replace('®',"(r)").replace("ô","o").replace("ö","o").replace("ä","a").replace("ó","o").replace("ü","u").replace("é","e") # TODO: temporary fix beause load of SemMed or method of querying it is messing up non-ascii characters
            if abstractTxt == "":
                print "ERROR: SemMed indicates that there is an abstract but one not present in the abstract cache!"
                sys.exit(1)
            
            exactSpanFrom = abstractTxt.upper().find(elt[SENTENCE].upper())
            if exactSpanFrom == -1:
                # try to remove some text that might be added as metadata and see if the match hits
                nsentence = elt[SENTENCE].upper().replace("ABSTRACT ","")
                exactSpanFrom = abstractTxt.upper().find(nsentence)
                if exactSpanFrom == -1:
                    print "ERROR:Could not find annotated sentence sequence in abstractTxt!\n\tsentence:\n\t\t%s\n\tabstractTxt:\n\t\t%s" % (nsentence, abstractTxt)
                    sys.exit(1)
     
            exactSpanTo = exactSpanFrom + len(elt[SENTENCE])
            pre = post = ""
            if exactSpanFrom - NUMB_CHARACTERS_PRE_AND_POST < 0:
                pre = abstractTxt[:exactSpanFrom]
            else:
                pre = abstractTxt[exactSpanFrom - NUMB_CHARACTERS_PRE_AND_POST:exactSpanFrom]
     
            if exactSpanTo + NUMB_CHARACTERS_PRE_AND_POST > len(abstractTxt):
                post = abstractTxt[exactSpanTo:]
            else:
                post = abstractTxt[exactSpanTo:exactSpanTo + NUMB_CHARACTERS_PRE_AND_POST]

            tplL.append((textConstraintUuid, oa["prefix"], Literal(unicode(pre,'utf-8', 'replace'))))
            tplL.append((textConstraintUuid, oa["postfix"], Literal(unicode(post,'utf-8', 'replace'))))

    s = u""
    for t in tplL:
        #s += unicode.encode(" ".join((t[0].n3(), t[1].n3(), t[2].n3(), u".\n")), 'utf-8', 'replace')
        s += u" ".join((t[0].n3(), t[1].n3(), t[2].n3(), u".\n"))
    f.write(s)
    

    # Specify the bodies of the annotation - for this type each
    # body contains the drug and condition as a semantic tag
    currentAnnotationBody = "ohdsi-pubmed-semmed-annotation-annotation-body-%s" % annotationBodyCntr
    annotationBodyCntr += 1

    tplL = []  # Clearing out the Target data tuple
    tplL.append((poc[currentAnnotItem], oa["hasBody"], poc[currentAnnotationBody]))
    tplL.append((poc[currentAnnotationBody], RDFS.label, Literal("Drug-HOI tag for PMID %s" % elt[PMID])))
    tplL.append((poc[currentAnnotationBody], RDF.type, ohdsi["OHDSIUMLSTags"])) # TODO: this is not yet formalized in a public ontology but should be
    tplL.append((poc[currentAnnotationBody], RDF.type, oa["SemanticTag"])) 
    tplL.append((poc[currentAnnotationBody], dcterms["description"], Literal("Drug-HOI body from MEDLINE PMID %s using UMLS drug %s (%s) and UMLS HOI %s (%s)" % (elt[PMID], elt[DRUG_UMLS_CUI], elt[DRUG_PREFERRED_TERM], elt[HOI_UMLS_CUI], elt[HOI_PREFERRED_TERM]))))

    if elt[PREDICATE] == 'DISRUPTS':
        tplL.append((poc[currentAnnotationBody], poc["modality"], Literal("positive")))
        tplL.append((poc[currentAnnotationBody], poc["semanticNetworkPredicate"], poc["T146"]))
    elif elt[PREDICATE] == 'NEG_DISRUPTS':
        tplL.append((poc[currentAnnotationBody], poc["modality"], Literal("negative")))
        tplL.append((poc[currentAnnotationBody], poc["semanticNetworkPredicate"], poc["T146"]))
    elif elt[PREDICATE] == 'CAUSES':
        tplL.append((poc[currentAnnotationBody], poc["modality"], Literal("positive")))
        tplL.append((poc[currentAnnotationBody], poc["semanticNetworkPredicate"], poc["T147"]))
    elif elt[PREDICATE] == 'NEG_CAUSES':
        tplL.append((poc[currentAnnotationBody], poc["modality"], Literal("negative")))
        tplL.append((poc[currentAnnotationBody], poc["semanticNetworkPredicate"], poc["T147"]))
    elif elt[PREDICATE] == 'AFFECTS':
        tplL.append((poc[currentAnnotationBody], poc["modality"], Literal("positive")))
        tplL.append((poc[currentAnnotationBody], poc["semanticNetworkPredicate"], poc["T151"]))
    elif elt[PREDICATE] == 'NEG_AFFECTS':
        tplL.append((poc[currentAnnotationBody], poc["modality"], Literal("negative")))
        tplL.append((poc[currentAnnotationBody], poc["semanticNetworkPredicate"], poc["T151"]))
    elif elt[PREDICATE] == 'ASSOCIATED_WITH':
        tplL.append((poc[currentAnnotationBody], poc["modality"], Literal("positive")))
        tplL.append((poc[currentAnnotationBody], poc["semanticNetworkPredicate"], poc["T166"]))
    elif elt[PREDICATE] == 'NEG_ASSOCIATED_WITH':
        tplL.append((poc[currentAnnotationBody], poc["modality"], Literal("negative")))
        tplL.append((poc[currentAnnotationBody], poc["semanticNetworkPredicate"], poc["T166"]))
    elif elt[PREDICATE] == 'COMPLICATES':
        tplL.append((poc[currentAnnotationBody], poc["modality"], Literal("positive")))
        tplL.append((poc[currentAnnotationBody], poc["semanticNetworkPredicate"], poc["T149"]))
    elif elt[PREDICATE] == 'NEG_COMPLICATES':
        tplL.append((poc[currentAnnotationBody], poc["modality"], Literal("negative")))
        tplL.append((poc[currentAnnotationBody], poc["semanticNetworkPredicate"], poc["T149"]))


    ### INCLUDE THE UMLS TAGS FROM THE RECORD AS PREFERRED TERMS AS
    ### WELL AS ANY RXNORM AND SNOMED/MEDDRA MAPPINGS 
    tplL.append((poc[currentAnnotationBody], ohdsi['UMLSDrug'], umls[elt[DRUG_UMLS_CUI]])) 
    tplL.append((poc[currentAnnotationBody], ohdsi['UMLSHoi'], umls[elt[HOI_UMLS_CUI]])) 

    # Adding RxNorm CUI if it exists
    if elt[DRUG_RXNORM] != "":
        if len(elt[DRUG_RXNORM].split("|")) > 1:
            print "ERROR: more than one RxNORM drug CUI (%s). This case is not yet handled by this program" % elt[DRUG_RXNORM]
        else:
            tplL.append((poc[currentAnnotationBody], ohdsi['RxnormDrug'], rxnorm[elt[DRUG_RXNORM]]))
            if DRUGS_D_RXNORM_KEYED.has_key(elt[DRUG_RXNORM]):
                tplL.append((poc[currentAnnotationBody], ohdsi['ImedsDrug'], ohdsi[DRUGS_D_RXNORM_KEYED[elt[DRUG_RXNORM]][2]]))
    else:
        print "WARNING: no RxNorm CUI for UMLS drug %s" % elt[DRUG_UMLS_CUI]

    if elt[DRUG_MESH] != "":
        if len(elt[DRUG_MESH].split("|")) > 1:
            print "ERROR: more than one MeSH drug CUI (%s). This case is not yet handled by this program" % elt[DRUG_MESH]
        else:
            tplL.append((poc[currentAnnotationBody], ohdsi['MeshDrug'], mesh[elt[DRUG_MESH]])) 

        # check if the MeSH UI is a grouping
        if elt[DRUG_MESH] in pharmActionMaptD.keys():
            (descriptorName, substancesL) =  (pharmActionMaptD[elt[DRUG_MESH]]['descriptorName'], pharmActionMaptD[elt[DRUG_MESH]]['substancesL'])
            print "INFO: The MeSH drug %s might be a grouping (%s). Attempting to expand to the %d individual drugs mapped in the MeSH pharmacologic action mapping" % (elt[DRUG_MESH], descriptorName, len(substancesL))
        
            collectionHead = URIRef(u"urn:uuid:%s" % uuid.uuid4()) # TODO: give this URI a type
            tplL.append((poc[currentAnnotationBody], ohdsi['adeAgents'], collectionHead))
            # add each substance to a collection in the body
            for substance in substancesL:
                tplL.append((collectionHead, ohdsi['MeshDrug'], mesh[substance['recordUI']]))
                if DRUGS_D_MESH_KEYED.has_key(substance['recordUI']):
                    tplL.append((collectionHead, ohdsi['RxnormDrug'], rxnorm[DRUGS_D_MESH_KEYED[substance['recordUI']][0]]))
                    tplL.append((collectionHead, ohdsi['ImedsDrug'], ohdsi[DRUGS_D_MESH_KEYED[substance['recordUI']][2]]))
                else:
                    print "WARNING: no RxNorm or IMEDS equivalent to the MeSH drug %s (%s) belonging to the pharmacologic action mapping %s" % (substance['recordUI'], substance['recordName'], elt[DRUG_MESH])
        else:
            print "INFO:  MeSH drug %s (%s) does not appear in the pharmacologic action mapping (not a grouping?)" % (elt[DRUG_MESH], elt[DRUG_PREFERRED_TERM])
    else:
        print "WARNING: no MeSH CUI for UMLS drug %s" % elt[DRUG_UMLS_CUI]

    # Now to HOIs - there are groupings in the data file as indicated
    # by pipe delimitted text strings.

    # For now, treat the MeSH mapping as necessary because its unique
    # for every record where it is found.
    # TODO: determine if this is the best approach!
    if elt[HOI_MESH] != "":
        if len(elt[HOI_MESH].split("|")) > 1:
            print "ERROR: more than one MeSH hoi CUI (%s). This case is not yet handled by this program" % elt[HOI_MESH]
        else:
            tplL.append((poc[currentAnnotationBody], ohdsi['MeshHoi'], mesh[elt[HOI_MESH]]))

        if MESH_D_SV.has_key(elt[HOI_MESH]):
            tplL.append((poc[currentAnnotationBody], ohdsi['ImedsHoi'], ohdsi[MESH_D_SV[elt[HOI_MESH]]]))
        else:
            print "ERROR: no OHDSI/IMEDS equivalent to the MeSH HOI %s" % (elt[HOI_MESH])

        # add the SNOMED and MedDRA effects to a collection in the body
        if elt[HOI_SNOMED] != "" or elt[HOI_MEDDRA] != "":
            collectionHead = URIRef(u"urn:uuid:%s" % uuid.uuid4())
            tplL.append((poc[currentAnnotationBody], ohdsi['adeEffects'], collectionHead))

            if elt[HOI_SNOMED] != "":
                snomedUIs = elt[HOI_SNOMED].split("|")
                for ui in snomedUIs:
                    tplL.append((collectionHead, ohdsi['adeEffect'], snomed[ui]))
                    if SNOMED_D_SV.has_key(ui):
                        tplL.append((collectionHead, ohdsi['ImedsHoi'], ohdsi[SNOMED_D_SV[ui]]))
                    else:
                        print "WARNING: no IMEDS equivalent to the SNOMED HOI %s (%s)" % (ui, elt[HOI_PREFERRED_TERM])

            if elt[HOI_MEDDRA] != "":
                meddraUIs = elt[HOI_MEDDRA].split("|")
                for ui in meddraUIs:
                    tplL.append((collectionHead, ohdsi['adeEffect'], meddra[ui]))
                    if MEDDRA_D_SV.has_key(ui):
                        tplL.append((collectionHead, ohdsi['ImedsHoi'], ohdsi[MEDDRA_D_SV[ui]]))
                    else:
                        print "WARNING: no IMEDS equivalent to the MedDRA HOI %s (%s)" % (ui, elt[HOI_PREFERRED_TERM])
    else:
        print "WARNING: No MeSH mapping for the HOI concept so the UMLS UI will be the only one provided in this body. TODO: determine if it would be better to use SNOMED or MedDRA as the required concept (or if some other approach is needed)"
        
    s = ""
    for t in tplL:
        s += unicode.encode(" ".join((t[0].n3(), t[1].n3(), t[2].n3(), u".\n")), 'utf-8', 'replace')
    f.write(s)


f.close
graph.close()
