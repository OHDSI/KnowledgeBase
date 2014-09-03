"""
selectTriplesPlusSentence.py

Jeremy Jao and Rich Boyce
09.2.2014

Selects concept triples with the sentences from which they were derived.
TODO: filter this down to triples with:
- subject being a pharm entity semantic type 
- object being a Pathologic Function, Sign or Symptom, Disease or Syndrome, Finding
- predicate CAUSES, ASSOCIATED_WITH, COMPLICATES, DISRUPTS, PREDISPOSES - and the negated versions of these

"""

import mysql.connector as sql
import connectSEMMED as db
import pprint

cnx = sql.connect(**db.details())
cursor = cnx.cursor()

def main():
    with open('listOfResults.txt', 'w') as fil:
        """        
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
        
        - DISRUPTS
        - NEG_DISRUPTS

        TODO: Consider the following to help untangle confounding by indication and known risk factors
        - PREDISPOSES
        - NEG_PREDISPOSES
        
        - TREATS
        - NEG_TREATS
        """

        query = """
                
                SELECT 
                    PREDICATION_AGGREGATE.PMID,
                    s_cui,
                    s_name,
                    s_type,
                    predicate,
                    o_cui,
                    o_name,
                    o_type,
                    SENTENCE,
                    TYPE
                FROM
                    PREDICATION_AGGREGATE, 
                    SENTENCE
                WHERE
                (
                        SID = SENTENCE_ID
                    AND
                        PREDICATION_AGGREGATE.PMID=SENTENCE.PMID
                )
                AND
                (
                        s_type='clnd'
                    OR
                        s_type='phsu'
                    OR
                        s_type='orch'
                )
                AND
                (
                        predicate='CAUSES'
                    OR
                        predicate='NEG_CAUSES'
                    OR
                        predicate='AFFECTS'
                    OR
                        predicate='NEG_AFFECTS'
                    OR
                        predicate='ASSOCIATED_WITH'
                    OR
                        predicate='NEG_ASSOCIATED_WITH'
                    OR
                        predicate='COMPLICATES'
                    OR
                        predicate='NEG_COMPLICATES'
                    OR
                        predicate='DISRUPTS'
                    OR
                        predicate='NEG_DISRUPTS'
                )
                AND
                (                      
                        o_type='cgab'
                    OR
                        o_type='dysn'
                    OR
                        o_type='mobd'
                    OR
                        o_type='patf'
                );
                """
             
        dic = makeSemanticDict('SRDEF.txt')
        pprint.pprint(dic, fil)
        
        fil.write("query:\n" + query + "\n")
        cursor.execute(query)

        for predicate in cursor:
            pprint.pprint(predicate, fil)
            #allObjects.write(dic[predicate[0]] + " -> " + predicate[0] + "\n")
            fil.write("\n")

            ## TODO: write in this format 
# TSV with header: pmid, predicate, drug CUI, drug RxNorm, drug MeSH, drug Preferred Term, drug UMLS entity type (long), HOI CUI, HOI SNOMED, HOI MedDRA, HOI MeSH, HOI Preferred Term, HOI UMLS entity type (long), sentence, sentence type, 
# 
            
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
