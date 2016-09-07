# pmSearch2rdf.py
#
# Convert the result of a pubmed drug-HOI evidence search to Open Data Annotation
#
# Author: Richard D Boyce, PhD
# 2014/2015
#

import sys
sys.path = sys.path + ['.']
reload(sys)
sys.setdefaultencoding('utf8')

import re, codecs, uuid, datetime
import json
from rdflib import Graph, Literal, Namespace, URIRef, RDF, RDFS
from lxml import etree
from lxml.etree import XMLParser, parse

import mysql.connector as msql # for mysql connection to Semmeddb
import psycopg2 # for postgres connection to Medline

## The result of the query in queryDrugHOIAssociations.psql
#SEARCH_RESULTS = "drug-hoi-associations-from-mesh-September-2016.tsv"
SEARCH_RESULTS = "drug-hoi-associations-from-mesh-September-2016-55831-to-end.tsv"

## Set up the db connection to the MEDLINE DB. This is used to collect
## a bit more data and metadata on the MEDLINE entries
DB_CONNECTION_INFO="db-connection.conf"
f = open(DB_CONNECTION_INFO,'r')
(db,user,pword,host,port) = f.readline().strip().split("\t")
f.close()
try:
    conn=psycopg2.connect(database=db, user=user, password=pword, host=host, port=port)
except Exception as e:
    print "ERROR: Unable to connect to database %s (user:%s) on host %s (port: %s). Check that the data in db-connection.conf is correct and that there is not barrier related to the network connection. Error: %s" % (db,user,host,port,e)
cur = conn.cursor()

## Set up the db connection to the SEMMEDDB DB. This is used to filter
## evidence items to be more specific than the drug class concepts
## that MeSH often uses for tags.
SEMMEDDB_CONNECTION_INFO="db-connection-SEMMEDDB.conf"
f = open(SEMMEDDB_CONNECTION_INFO,'r')
(db,user,pword,host,port) = f.readline().strip().split("\t")
f.close()
try:
    smdb_conn=msql.connect(database=db, user=user, password=pword, host=host, port=port)
except Exception as e:
    print "ERROR: Unable to connect to database %s (user:%s) on host %s (port: %s). Check that the data in db-connection-SEMMEDDB.conf is correct and that there is not barrier related to the network connection. Error: %s" % (db,user,host,port,e)
smdb_cur = smdb_conn.cursor()


# TERMINOLOGY MAPPING FILES 
## NOTE: the drug concepts are mapped directly to RxNorm here but the
##       HOIs are retained as MeSH and then mapped using the Standard
##       Vocabu lary at load time by the code in
##       Schema/postgres/mergeCountsFromIntegratedSources.py based on
##       config information present in
##       Schema/postgres/integratedSources.conf
RXNORM_TO_MESH = "../terminology-mappings/RxNorm-to-MeSH/mesh-to-rxnorm-standard-vocab-v5.csv"
MESH_TO_STANDARD_VOCAB = "../terminology-mappings/StandardVocabToMeSH/mesh-to-standard-vocab-v5.txt"
MESH_PHARMACOLOGIC_ACTION_MAPPINGS = "../terminology-mappings/MeSHPharmocologicActionToSubstances/pa2016.xml"

# OUTPUT DATA FILE
OUTPUT_FILE = "drug-hoi-pubmed-mesh.nt"

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
f = open(RXNORM_TO_MESH,"r")
buf = f.read()
f.close()
l = buf.split("\n")
for elt in l[1:]:
    if elt.strip() == "":
        break

    try:
        (mesh,pt,rxcui,concept_name,ohdsiID,conceptClassId) = [x.strip() for x in elt.split("|")]
    except ValueError:        
        print "ERROR: terminology mapping record appears incomplete. Skipping: %s" % elt
        continue
    
    if DRUGS_D.get(mesh): # add a synonymn
        DRUGS_D[mesh][1].append(pt)
    else: # create a new record
        DRUGS_D[mesh] = (rxcui, [pt], ohdsiID)

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

# ################################################################################

# Load the results of applying the Avillach et al method for
# identifying drug-ADR associations in MEDLINE using MeSH headings
# TODO: consider using an iterator for this
(PMID, ADR_DRUG_LABEL, ADR_DRUG_UI, ADR_HOI_LABEL, ADR_HOI_UI, PUB_TYPE, PUB_TYPE_UI) = range(0,7)
f = open(SEARCH_RESULTS,'r')
buf = f.read()
f.close()
recL = [x.strip().split("\t") for x in buf.strip().split("\n")]

# Start building the open annotation data graph
annotationSetCntr = 1
annotationItemCntr = 1
annotationBodyCntr = 1
annotationEvidenceCntr = 1

annotatedCache = {} # indexes annotation ids by pmid
abstractCache = {} # cache for abstract text
pubTypeCache = {} # used because some PMIDs have multiple publication type assignments TODO: determine pub types should be assigned to a Collection under the target's graph 
drugHoiPMIDCache = {} # used to avoid duplicating PMID - drug  - HOI combos for PMIDs that have multiple publication type assignments TODO: determine if a more robust source query is needed
mshPharmIdToUMLSCache = {} # Used to store mappings from MeSH pharmacological grouping IDs to a list of UMLS MetaThesaurus CUIs for the drug concepts that belong in that group
mshSubstOfInterestLCache = {} # used to avoid repeated calls to Semmeddb to identify specific drugs mentioned in a title or abstract
pmidToCuiCache = {} # stores all CUIs mentioned in the s_cui or o_cui columns of semmeddb.PREDICATION_AGGREGATE for a given PMID

currentAnnotation = annotationItemCntr

currentAnnotSet = 'ohdsi-pubmed-mesh-annotation-set-%s' % annotationSetCntr 
annotationSetCntr += 1
graph.add((poc[currentAnnotSet], RDF.type, oa["DataAnnotation"])) # TODO: find out what is being used for collections in OA
graph.add((poc[currentAnnotSet], oa["annotatedAt"], Literal(datetime.date.today())))
graph.add((poc[currentAnnotSet], oa["annotatedBy"], URIRef(u"http://www.pitt.edu/~rdb20/triads-lab.xml#TRIADS")))

f = codecs.open(OUTPUT_FILE,"w","utf8")
s = graph.serialize(format="n3",encoding="utf8", errors="replace")
f.write(s)

for elt in recL[0:1000]: # Debugging
#for elt in recL: # Full run
    ## For now, only process papers tagged as for humans
    ## TODO: expand the evidence types to include non-human studies 
    try:
        print "INFO: Testing if study %s is tagged as involving humans" % elt[PMID]
        cur.execute("""select descriptorname from medcit_meshheadinglist_meshheading where pmid = %s and descriptorname = 'Humans'""" % elt[PMID])
    except Exception as e:
        print "ERROR: test if study tagged as involving humans failed. Error string: %s" % e
        sys.exit(1)

    rows = cur.fetchall()
    if len(rows) == 0:
        print "WARNING: PMID %s not tagged as involving humans. Skipping this record." % elt[PMID]
        continue 

    # get abstract if not already cached
    # TODO: retrieve the title too
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

        curType = elt[PUB_TYPE]
        if curType in ['Meta-Analysis','Comparative Study','Multicenter Study','Journal Article']:
            curType = "other (publication type)"
        
        if curType not in pubTypeL:
            print "INFO: MEDLINE record %s has more than one pub type assigned" % elt[PMID]
            pubTypeCache[elt[PMID]].append(elt[PUB_TYPE])
            if curType == "Clinical Trial": 
                tplL.append((currentAnnotTargetUuid, ohdsi["MeshStudyType"], Literal("clinical trial (publication type)")))
            elif curType == "Case Reports": 
                tplL.append((currentAnnotTargetUuid, ohdsi["MeshStudyType"], Literal("case reports (publication type)")))
            else: 
                tplL.append((currentAnnotTargetUuid, ohdsi["MeshStudyType"], Literal("other (publication type)")))
    else:
        currentAnnotation = annotationItemCntr
        annotatedCache[elt[PMID]] = currentAnnotation
        annotationItemCntr += 1
        createNewTarget = True
    
    currentAnnotItem = "ohdsi-pubmed-mesh-annotation-item-%s" % currentAnnotation

    if createNewTarget:
        tplL.append((poc[currentAnnotSet], aoOld["item"], poc[currentAnnotItem])) # TODO: find out what is being used for items of collections in OA
        tplL.append((poc[currentAnnotItem], RDF.type, oa["DataAnnotation"])) 
        tplL.append((poc[currentAnnotItem], RDF.type, ohdsi["PubMedDrugHOIAnnotation"])) # TODO: should be a subclass of oa:DataAnnotation
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
        curType = elt[PUB_TYPE]
        if curType in ['Meta-Analysis','Comparative Study','Multicenter Study','Journal Article']:
            curType = "other (publication type)"
            
        pubTypeCache[elt[PMID]] = [curType]
        if curType == "Clinical Trial": 
            tplL.append((currentAnnotTargetUuid, ohdsi["MeshStudyType"], Literal("clinical trial (publication type)")))
        elif curType == "Case Reports": 
            tplL.append((currentAnnotTargetUuid, ohdsi["MeshStudyType"], Literal("case reports (publication type)")))
        else:
            tplL.append((currentAnnotTargetUuid, ohdsi["MeshStudyType"], Literal("other (publication type)")))


        # add the text quote selector but just put the abstract in an oa:exact
        # TODO: add the title to oa:exact when there is no abstract (or concatenate both)
        textConstraintUuid = URIRef("urn:uuid:%s" % uuid.uuid4())
        tplL.append((currentAnnotTargetUuid, oa["hasSelector"], textConstraintUuid))         
        tplL.append((textConstraintUuid, RDF.type, oa["TextQuoteSelector"]))
        abstractTxt = unicode(abstractCache[elt[PMID]], 'utf-8', 'replace')
        tplL.append((textConstraintUuid, oa["exact"], Literal(abstractTxt)))
        
    s = u""
    for t in tplL:
        s += unicode.encode(u" ".join((t[0].n3(), t[1].n3(), t[2].n3(), u".\n")), 'utf-8', 'replace')
    f.write(s)
    

    # Specify the bodies of the annotation - for this type each
    # body contains the MESH drug and condition as a semantic tag
    print "INFO: working on the body for %s" % elt
    
    # to begin with, avoid duplicating PMID - drug  - HOI combos for PMIDs that have multiple publication type assignments
    concat = "%s-%s-%s" % (elt[PMID], elt[ADR_DRUG_UI], elt[ADR_HOI_UI])
    if drugHoiPMIDCache.has_key(concat):
        print "INFO: skipping generation of a new body graph because the PMID, drug, and HOI (%s) have already been processed. Probably a MEDLINE record with multiple pub type assignments" % concat
        continue
    else:
        drugHoiPMIDCache[concat] = None

    currentAnnotationBody = "ohdsi-pubmed-mesh-annotation-annotation-body-%s" % annotationBodyCntr
    annotationBodyCntr += 1

    tplL = []  # Clearing out the Target data tuple
    tplL.append((poc[currentAnnotItem], oa["hasBody"], poc[currentAnnotationBody]))
    tplL.append((poc[currentAnnotationBody], RDFS.label, Literal("Drug-HOI tag for PMID %s" % elt[PMID])))
    tplL.append((poc[currentAnnotationBody], RDF.type, ohdsi["OHDSIMeshTags"])) # TODO: this is not yet formalized in a public ontology but should be
    tplL.append((poc[currentAnnotationBody], RDF.type, oa["SemanticTag"])) 
    tplL.append((poc[currentAnnotationBody], dcterms["description"], Literal("Drug-HOI body from MEDLINE PMID %s using MESH drug %s (%s) and HOI %s (%s)" % (elt[PMID], elt[ADR_DRUG_LABEL], elt[ADR_DRUG_UI], elt[ADR_HOI_LABEL], elt[ADR_HOI_UI]))))

    ### INCLUDE THE MESH TAGS FROM THE RECORD AS PREFERRED TERMS AS
    ### WELL AS DATA FROM THE DRUG AND HOI QUERY
    tplL.append((poc[currentAnnotationBody], ohdsi['MeshDrug'], mesh[elt[ADR_DRUG_UI]])) 

    if DRUGS_D.has_key(elt[ADR_DRUG_UI]): # an individual drug
        tplL.append((poc[currentAnnotationBody], ohdsi['RxnormDrug'], rxnorm[DRUGS_D[elt[ADR_DRUG_UI]][0]]))
        tplL.append((poc[currentAnnotationBody], ohdsi['ImedsDrug'], ohdsi[DRUGS_D[elt[ADR_DRUG_UI]][2]]))

    elif elt[ADR_DRUG_UI] in pharmActionMaptD.keys(): # a drug group
        (descriptorName, substancesL) =  (pharmActionMaptD[elt[ADR_DRUG_UI]]['descriptorName'], pharmActionMaptD[elt[ADR_DRUG_UI]]['substancesL'])
        print "INFO: The MeSH drug %s might be a grouping (%s). Attempting to expand to the %d individual drugs mapped in the MeSH pharmacologic action mapping that are mentioned in the title and/or abstract" % (elt[ADR_DRUG_UI], descriptorName, len(substancesL))

        # First see if any of the drugs in the group are mentioned specifically in the title or abstract. 
        mshSubstOfInterestL = []
        if mshSubstOfInterestLCache.has_key(elt[PMID] + elt[ADR_DRUG_UI]):
            mshSubstOfInterestL = mshSubstOfInterestLCache[elt[PMID] + elt[ADR_DRUG_UI]]
            print "INFO: pulled %s individual Semmeddb drug mentions for PMID %s from cache" % (len(mshSubstOfInterestL), elt[PMID])
        else:
            ## query UMLS for the MeSH identifiers for the substances and chemicals
            cuiRsltL = []
            if mshPharmIdToUMLSCache.has_key(descriptorName):
                cuiRsltL = mshPharmIdToUMLSCache[descriptorName]
                print "INFO: No need to query UMLS, using UMLS MetaThesaurus results from cache"
            else:
                # It is most efficient, given the indices on semmeddb, to
                # query UMLS first for all relevant substance CUIs, then pass
                # that in a query to semmedb
                mshIdSet = set([x['recordUI'] for x in substancesL])
                q = """
SELECT DISTINCT CUI,SDUI FROM umls.MRCONSO WHERE SDUI IN ('%s') AND SAB = 'MSH'
            """ % "','".join(list(mshIdSet))
                print q
        
                smdb_cur.execute(q)
                cuiRsltL = []
                for rslt in smdb_cur:
                    cuiRsltL.append((rslt[0],rslt[1]))        
                mshPharmIdToUMLSCache[descriptorName] = cuiRsltL

            if len(cuiRsltL) == 0:
                print "ERROR: very strange that none of the drug concepts in the MeSH pharmacological grouping is able to map to any UMLS MetaThesaurus CUI: %s -- %s" % (descriptorName,mshIdSet)
            else:
                # query Semmeddb to get the CUIs for tagged pharmacologic
                # substances and organic chemicals. NOTE: the IN clause is
                # limited by the MySQL max_allowed_packet configuration
                # variable so set it to be large (e.g., several megabytes)
                print "INFO: checking Semmeddb to see if the title or abstract of PMID %s mentions any of the %s individual drugs" % (elt[PMID], len(cuiRsltL))

                # 1. Get the CUIs associated with the PMID in semmeddb
                pmidCuis = pmidToCuiCache.get(elt[PMID])
                if pmidCuis == None:
                    q = """
 SELECT * 
 FROM 
 (
 SELECT s_cui AS out_cui FROM semmeddb.PREDICATION_AGGREGATE WHERE PMID = '%s'
 UNION
 SELECT o_cui AS out_cui FROM semmeddb.PREDICATION_AGGREGATE WHERE PMID = '%s'
 ) c_union
""" % (elt[PMID], elt[PMID])

                    print q 

                    smdb_cur.execute(q)
                    pmidCuis = fetchall() # all results (even null ones) need to be retrieved to prevent  "Unread result found" when the curser is used in a later iteraction 

                if pmidCuis != None:
                    pmidToCuiCache[elt[PMID]] = pmidCuis
                    print "INFO: Found individual Semmeddb drug mentions for PMID -- pmidCuis: %s" % ",".join(pmidCuis)
                    # 2. get the MESH identifiers for the returned CUIs that are in the MESH Pharm group cuiRsltL
                    mshSubstOfInterestL = [x[1] for x in filter(lambda x: x[0] in pmidCuis, cuiRsltL)]
                    mshSubstOfInterestLCache[elt[PMID] + elt[ADR_DRUG_UI]] = mshSubstOfInterestL
                
        # add each specific substance found in the title or abstract to a 'adeAgents' collection in the body
        if len(mshSubstOfInterestL) > 0:
            # first check for duplication, it happens a bunch
            keepers = []
            for substanceMshUI in mshSubstOfInterestL:
                concat = "%s-%s-%s" % (elt[PMID], substanceMshUI, elt[ADR_HOI_UI])
                if drugHoiPMIDCache.has_key(concat):
                    print "INFO: skipping addition of a PMID, drug, and HOI (%s) that have already been processed (probably duplication of pharmacologic entity mapping because of drug groupings)." % concat
                    continue
                else:
                    drugHoiPMIDCache[concat] = None
                    keepers.append(substanceMshUI)

            if len(keepers) > 0:
                collectionHead = URIRef(u"urn:uuid:%s" % uuid.uuid4()) # TODO: give this URI a type
                tplL.append((poc[currentAnnotationBody], ohdsi['adeAgents'], collectionHead))

                for substanceMshUI in keepers:
                    tplL.append((collectionHead, ohdsi['MeshDrug'], mesh[substanceMshUI]))
                    if DRUGS_D.has_key(substanceMshUI):
                        tplL.append((collectionHead, ohdsi['RxnormDrug'], rxnorm[DRUGS_D[substanceMshUI][0]]))
                        tplL.append((collectionHead, ohdsi['ImedsDrug'], ohdsi[DRUGS_D[substanceMshUI][2]]))
                    else:
                        print "WARNING: no RxNorm or IMEDS equivalent to the MeSH drug %s belonging to the pharmacologic action mapping %s" % (substanceMshUI, elt[ADR_DRUG_UI])
            else:
                print "INFO: none of the individual drugs in the drug group %s (%s) were identified in the abstract. The drug group MeSH CUI will be noted in the body of this OA annotation and all members of the group will be linked to a list under adeAgentsUnfiltered" % (elt[ADR_DRUG_UI], descriptorName)

        # Now, add the rest of the entities in the pharmacologic group to an 'adeAgentsUnfiltered' collection which is useful for two reasons, 1) SemMedDB is a few months behind the current MEDLINE (so, more recent titles and abstracts will not benefit from the processing steps above), and 2)although noisy for inferring positive drug-HOI associaions, having all drugss in a class is helpful for inferring negative controls.
        keepers = [] # NOTE: we deliberately do not add those triples that have been added to the 'adeAgents' collection to the 'adeAgentsUnfiltered' collection
        if pmidCuis != None:
            substOfInterestL = [x[1] for x in filter(lambda x: x[0] not in pmidCuis, cuiRsltL)] # the drug concepts NOT mentioned in the abstract
        else:
            substOfInterestL = [x[1] for x in cuiRsltL] # the MESH identifiers all drugs in the MESH pharm grouping
            
        for substanceMshUI in substOfInterestL:          
            concat = "%s-%s-%s" % (elt[PMID], substanceMshUI, elt[ADR_HOI_UI])
            if drugHoiPMIDCache.has_key(concat):
                print "INFO: skipping addition of a PMID, drug, and HOI (%s) that have already been processed (probably duplication of pharmacologic entity mapping because of drug groupings)." % concat
                continue
            else:
                drugHoiPMIDCache[concat] = None
                keepers.append(substanceMshUI)

        if len(keepers) > 0:
            collectionHead = URIRef(u"urn:uuid:%s" % uuid.uuid4()) # TODO: give this URI a type
            tplL.append((poc[currentAnnotationBody], ohdsi['adeAgentsUnfiltered'], collectionHead))
            for substanceMshUI in keepers:
                tplL.append((collectionHead, ohdsi['MeshDrug'], mesh[substanceMshUI]))
                if DRUGS_D.has_key(substanceMshUI):
                    tplL.append((collectionHead, ohdsi['RxnormDrug'], rxnorm[DRUGS_D[substanceMshUI][0]]))
                    tplL.append((collectionHead, ohdsi['ImedsDrug'], ohdsi[DRUGS_D[substanceMshUI][2]]))
                else:
                    print "WARNING: no RxNorm or IMEDS equivalent to the MeSH drug %s belonging to the pharmacologic action mapping %s" % (substanceMshUI, elt[ADR_DRUG_UI])
                        
    else:
        print "ERROR: no RxNorm equivalent to the MeSH drug %s (%s) and this does not appear in the pharmacologic action mapping (not a grouping?), skipping" % (elt[ADR_DRUG_UI], elt[ADR_DRUG_LABEL])
        continue

    if MESH_D_SV.has_key(elt[ADR_HOI_UI]):
        tplL.append((poc[currentAnnotationBody], ohdsi['ImedsHoi'], ohdsi[MESH_D_SV[elt[ADR_HOI_UI]]]))
        tplL.append((poc[currentAnnotationBody], ohdsi['MeshHoi'], mesh[elt[ADR_HOI_UI]]))
    else:
        print "ERROR: no OHDSI/IMEDS equivalent to the MeSH HOI %s, skipping" % (elt[ADR_DRUG_UI])
        continue
 
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
conn.close()
smdb_conn.close()



#### SCRATCH
#cuiRsltStr = "','".join([x[0] for x in cuiRsltL]) # UMLS CUIs for the individual drugs in the pharm grouping mentioned as having some drug-HOI association
# ...                
#                 q = """
#  SELECT * 
#  FROM 
#  (
#  SELECT s_cui AS out_cui FROM semmeddb.PRED_AGGR_TO_MRCONSO WHERE PMID = '%s' AND s_SDUI IN ('%s')
#  UNION
#  SELECT o_cui AS out_cui FROM semmeddb.PRED_AGGR_TO_MRCONSO WHERE PMID = '%s' AND o_SDUI IN ('%s')
#  ) c_union
# """ % (elt[PMID], "','".join(list(mshIdSet)), elt[PMID], "','".join(list(mshIdSet)))
#                 print q                
                
#                 q = """
#  SELECT * 
#  FROM 
#  (
#  SELECT s_cui AS out_cui FROM semmeddb.PREDICATION_AGGREGATE INNER JOIN umls.MRCONSO ON semmeddb.PREDICATION_AGGREGATE.s_cui = umls.MRCONSO.CUI WHERE PMID = '%s' AND umls.MRCONSO.SDUI IN ('%s')
#  UNION
#  SELECT o_cui AS out_cui FROM semmeddb.PREDICATION_AGGREGATE INNER JOIN umls.MRCONSO ON semmeddb.PREDICATION_AGGREGATE.o_cui = umls.MRCONSO.CUI WHERE PMID = '%s' AND umls.MRCONSO.SDUI IN ('%s')
#  ) c_union
# """ % (elt[PMID], "','".join(list(mshIdSet)), elt[PMID], "','".join(list(mshIdSet)))
#                 print q
#                 q = """
#  SELECT * 
#  FROM 
#  (
#  SELECT s_cui AS out_cui FROM semmeddb.PREDICATION_AGGREGATE WHERE PMID = '%s' AND s_cui IN (
#      SELECT DISTINCT CUI FROM umls.MRCONSO WHERE SDUI IN ('%s') AND SAB = 'MSH')
#  UNION
#  SELECT o_cui AS out_cui FROM semmeddb.PREDICATION_AGGREGATE WHERE PMID = '%s' AND o_cui IN (
#      SELECT DISTINCT CUI FROM umls.MRCONSO WHERE SDUI IN ('%s') AND SAB = 'MSH')
#  ) c_union
# """ % (elt[PMID], "','".join(list(mshIdSet)), elt[PMID], "','".join(list(mshIdSet)))
#                 print q
#                 q = """
# SELECT * 
# FROM 
# (
# SELECT s_cui AS out_cui FROM semmeddb.PREDICATION_AGGREGATE WHERE PMID = '%s' AND s_cui IN ('%s')
# UNION
# SELECT o_cui AS out_cui FROM semmeddb.PREDICATION_AGGREGATE WHERE PMID = '%s' AND o_cui IN ('%s')
# ) c_union
# """ % (elt[PMID], cuiRsltStr, elt[PMID], cuiRsltStr)
#                 print q  
                # smdb_cur.execute(q)
                # substOfInterestL = []
                # for rslt in smdb_cur:
                #     substOfInterestL.append(rslt[0])
                # mshSubstOfInterestL = [x[1] for x in filter(lambda x: x[0] in substOfInterestL, cuiRsltL)]

                # if len(mshSubstOfInterestL) > 0:
                #     print "INFO: caching %s specific substances mentioned in the abstract for %s: %s " % (len(mshSubstOfInterestL),elt[PMID],mshSubstOfInterestL)
                #     mshSubstOfInterestLCache[elt[PMID] + elt[ADR_DRUG_UI]] = mshSubstOfInterestL
