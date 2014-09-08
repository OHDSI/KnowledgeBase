"""
selectTriplesPlusSentence.py

Jeremy Jao and Rich Boyce
09.2.2014

Selects concept triples with the sentences from which they were derived. 
The output semmedTriplesPlusSentence.tsv has a way to perhaps create a way
to make a simple drilldown and summary case usage.

Prerequisites:

The UMLS CUI to RxNorm, MeSH, SNOMED, and MedDRA Conversion was done with 
UMLS_CUIs.py class which takes the TRIADS data from Dr. Boyce's server, 
process it into its own class (well documented), processed, and then 
pickled using cPickle (in its main). This had to be done because

-File prerequisites:
    - UMLS_CUIs.py (python UMLS_CUIs.py)
    - umlsStructure.cPickle - UMLS_CUIs class postprocessed file created
    from above python class file
    - can only be run on Dr. Boyce's server

Steps that the program does:

1. Query the SemMED DB from the OHDSI dev server
2. open the UMLS_CUIs pickle
3. writes the results via this in a TSV:
['pmid', 'predicate', 'drug UMLS CUI', 'drug RxNorm', 'drug MeSH', 'drug Preferred Term', 'drug UMLS entity type', 'HOI UMLS CUI', 'HOI SNOMED', 'HOI MedDRA', 'HOI MeSH', 'HOI Preferred Term', 'HOI UMLS entity type', 'sentence', 'sentence location', 'sentence type']
- explanation of columns:
    - pmid: the PMID
    - predicate: the predicate used to associate the subject and object
    - Drug UMLS CUI: UMLS CUI of the subject (drug)
    - drug RxNorm: RxNorm drug CUI
    - drug MeSH: MeSH drug CUI
    - drug Preferred Term: name of the drug from SEMMED
    - drug UMLS entity type: name of the drug's UMLS Entity Type
    - HOI UMLS CUI: Health Outcome of Interest UMLS CUI
    - HOI SNOMED: Health Outcome of Interest SNOMED CUI
    - HOI MedDRA: Health Outcome of Interest MedDRA CUI
    - HOI MeSH: Health Outcome of Interest MeSH CUI
    - HOI Preferred Term: name of the HOI from SEMMED
    - HOI entity type: name of the HOI's UMLS Entity type
    - sentence: the actual sentence of the finding
    - sentence location: number that represents the location of the sentence found from its source from PM
    - sentence type: sentence was extracted from this type
    
Take Note:
- SEMMED supplies the UMLS CUI
- I used the UMLS CUI to get the RxNorm, MeSH, MedDRA, and SNOMED CUIs
- However, as of right now, there is a one-to-many mapping between UMLS and SNOMED+MEDDRA
so what I did is I put the CUIs with that mapping pipe-delimited inside each column.


"""

import mysql.connector as sql
import connectSEMMED as db
import pprint
import cPickle as pickle
import csv
from UMLS_CUIs import UMLS_CUIs

cnx = sql.connect(**db.details())
cursor = cnx.cursor()

def main():
    with open('semmedTriplesPlusSentence_v2.tsv', 'w') as fil:
        '''        
        List of subject/object types obtained from:
        https://raw.githubusercontent.com/mengjunxie/ae-lda/master/misc/SRDEF.txt
        
        Complete list of semantic types:
        http://semanticnetwork.nlm.nih.gov/SemGroups/Papers/2003-medinfo-atm.pdf
        
        List of drugs:
        http://www.nlm.nih.gov/research/umls/sourcereleasedocs/current/RXNORM/stats.html
        
        Subjects (goal is to get drug entities -> all RXNORM entities):
        - clnd|Clinical Drug
        - phsu|Pharmacologic Substance
        - orch|Organic Chemical
        
        Objects (goal is to get health outcomes):
        - cgab|Congenital Abnormality
        - dysn|Disease or Syndrome
        - mobd|Mental or behavioral dysfunction
        - patf|Pathologic Function
        
        PREDICATES: See Kilicoglu H, Rosemblat G, Fiszman M, Rindflesch TC. Constructing a semantic
predication gold standard from the biomedical literature. BMC Bioinformatics.
2011 Dec 20;12:486. doi: 10.1186/1471-2105-12-486. PubMed PMID: 22185221; PubMed 
Central PMCID: PMC3281188.
   
        - CAUSES
        - NEG_CAUSES
        
        - AFFECTS
        - NEG_AFFECTS
        
        - ASSOCIATED_WITH
        - NEG_ASSOCIATED_WITH
        
        - COMPLICATES
        - NEG_COMPLICATES
        
        - DISRUPTS
        - NEG_DISRUPTS

        TODO: Consider the following to help untangle confounding by indication and known risk factors
        - PREDISPOSES
        - NEG_PREDISPOSES
        
        - TREATS
        - NEG_TREATS
        '''

        query = """
                SELECT 
                    PREDICATION_AGGREGATE.PMID,
                    predicate,
                    s_cui,
                    s_name,
                    s_type,
                    o_cui,
                    o_name,
                    o_type,
                    SENTENCE,
                    NUMBER,
                    TYPE,
                    PREDICATE_START_INDEX,
                    PREDICATE_END_INDEX,
                    SUBJECT_START_INDEX,
                    SUBJECT_END_INDEX,
                    SUBJECT_DIST,
                    SUBJECT_MAXDIST,
                    SUBJECT_SCORE,
                    OBJECT_START_INDEX,
                    OBJECT_END_INDEX,
                    OBJECT_DIST,
                    OBJECT_MAXDIST,
                    OBJECT_SCORE

                FROM
                        PREDICATION_AGGREGATE
                    INNER JOIN
                        (SENTENCE NATURAL JOIN SENTENCE_PREDICATION)
                    ON
                            PREDICATION_AGGREGATE.SID=SENTENCE_ID
                        AND
                            PREDICATION_AGGREGATE.PNUMBER=PREDICATION_NUMBER
                        AND
                            PREDICATION_AGGREGATE.PID=PREDICATION_ID
                WHERE
                (
                    s_type in 
                    (
                        'clnd',
                        'phsu',
                        'orch'
                    )
                )
                AND
                (
                    predicate in 
                    (
                        'CAUSES',
                        'NEG_CAUSES',
                        'AFFECTS',
                        'NEG_AFFECTS',
                        'ASSOCIATED_WITH',
                        'NEG_ASSOCIATED_WITH',
                        'COMPLICATES',
                        'NEG_COMPLICATES',
                        'DISRUPTS',
                        'NEG_DISRUPTS'
                    )
                )
                AND
                (   
                    o_type in
                    (
                        'cgab',
                        'dysn',
                        'mobd',
                        'patf'
                    )
                )
                ;
        """

        srdefdic = makeSemanticDict('SRDEF.txt')
        #pprint.pprint(dic, fil)
        
        #fil.write("query:\n" + query + "\n")
        cursor.execute(query)
       
        tsv = csv.writer(fil, delimiter="\t")
        umlsCUIs = pickle.load(open('umlsStructure.cPickle', 'rb'))
        tsv.writerow(['pmid', 'predicate', 'predicate start index', 'predicate end index', 'drug UMLS CUI', 'drug RxNorm', 'drug MeSH','drug Preferred Term','drug UMLS entity type', 'drug start index', 'drug end index', 'drug distance', 'drug max distance', 'drug max score', 'HOI UMLS CUI', 'HOI SNOMED', 'HOI MedDRA', 'HOI MeSH', 'HOI Preferred Term', 'HOI UMLS entity type', 'HOI start index', 'HOI end index', 'HOI distance', 'HOI max distance', 'HOI score', 'sentence','sentence location', 'sentence type'])
        for predicate in cursor:
            tsv.writerow([predicate[0], predicate[1], predicate[11], predicate[12],predicate[2], umlsCUIs.getRxnormCui(predicate[2]), umlsCUIs.getMeshCui(predicate[2]), predicate[3], srdefdic[predicate[4]], predicate[13], predicate[14], predicate[15], predicate[16], predicate[17], predicate[5], umlsCUIs.getSnomedct_usCui(predicate[5]), umlsCUIs.getMeddraCui(predicate[5]), umlsCUIs.getMeshCui(predicate[5]), predicate[6], srdefdic[predicate[7]], predicate[18], predicate[19], predicate[20], predicate[21], predicate[22], predicate[8], predicate[9], predicate[10]])
        #allObjects.close()

def makeSemanticDict(inp):
    dic = {}
    with open(inp, 'r') as fil:
        for line in fil:
            split = line.split('|')
            dic[split[0].strip()] = split[1].strip()
    return dic

if __name__ == "__main__":
    main()
    cursor.close()
    cnx.close()
