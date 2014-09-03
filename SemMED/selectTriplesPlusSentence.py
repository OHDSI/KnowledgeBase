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
        #allObjects = open('allObjectTypes.txt', 'w')
        #query = """
    #SELECT CONCEPT1, PREDICATE, CONCEPT2, SENTENCE_ID, PMID, TYPE, NUMBER, SENTENCE
    #FROM 
    #...TODO: 
    #Q1) all rows from PREDICATION_ARGUMENT with a given predication id
    #Q2) SENTENCE_PREDICATION will give the sentence id that can be used for the table.

    #you probably do not want to inner join from predication to PREDICATION_ARGUMENT....

    #CONCEPT_SEMTYPE_ID

    #"""

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
        - medd|Medical Device
        - drdd|Drug Delivery Device
        
        Objects (goal is to get health outcomes):
        - bpoc|Body Part, Organ, or Organ Component
        - cgab|Congenital Abnormality
        - clna|Clinical Attribute
        - comd|Cell or Molecular Dysfunction
        - dysn|Disease or Syndrome
        - enzy|Enzyme
        - fndg|Finding
        - ftcn|Functional Concept
        - gngm|Gene or Genome
        - horm|Hormone
        - humn|Human
        - imft|Immunologic Factor
        - mobd|Mental or behavioral dysfunction
        - menp|Mental Process
        - nnon|Nucleic Acid, Nucleoside, etc.
        - patf|Pathologic Function
        - orgf|Organism Function
        - sosy|Sign or Symptom
        - vita|Vitamin
        
        PREDICATES:
        
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
        
        - PREDISPOSES
        - NEG_PREDISPOSES
        
        - TREATS
        - NEG_TREATS
        
        - INHIBITS
        - NEG_INHIBITS
        
        - DISRUPTS
        - NEG_DISRUPTS
        
        - STIMULATES
        - NEG_STIMULATES
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
                    OR
                        s_type='medd'
                    OR
                        s_type='drdd'
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
                    OR
                        predicate='PREDISPOSES'
                    OR
                        predicate='NEG_PREDISPOSES'
                    OR
                        predicate='TREATS'
                    OR
                        predicate='NEG_TREATS'
                    OR
                        predicate='INHIBITS'
                    OR
                        predicate='NEG_INHIBITS'
                    OR
                        predicate='DISRUPTS'
                    OR
                        predicate='NEG_DISRUPTS'
                    OR
                        predicate='STIMULATES'
                    OR
                        predicate='NEG_STIMULATES'
                )
                AND
                (
                        o_type='bpoc'
                    OR
                        o_type='cgab'
                    OR
                        o_type='clna'
                    OR
                        o_type='comd'
                    OR
                        o_type='dysn'
                    OR
                        o_type='enzy'
                    OR
                        o_type='fndg'
                    OR
                        o_type='ftcn'
                    OR
                        o_type='gngm'
                    OR
                        o_type='horm'
                    OR
                        o_type='humn'
                    OR
                        o_type='imft'
                    OR
                        o_type='mobd'
                    OR
                        o_type='menp'
                    OR
                        o_type='nnon'
                    OR
                        o_type='patf'
                    OR
                        o_type='orgf'
                    OR
                        o_type='sosy'
                    OR
                        o_type='vita'
                );
                """
        
        #otherquery = """
                
                #SELECT DISTINCT
                    #o_type
                #FROM
                    #PREDICATION_AGGREGATE
                #WHERE
                #(
                        #s_type='clnd'
                    #OR
                        #s_type='phsu'
                    #OR
                        #s_type='orch'
                    #OR
                        #s_type='medd'
                    #OR
                        #s_type='drdd'
                #)
                #AND
                #(
                        #predicate='CAUSES'
                    #OR
                        #predicate='NEG_CAUSES'
                    #OR
                        #predicate='AFFECTS'
                    #OR
                        #predicate='NEG_AFFECTS'
                    #OR
                        #predicate='ASSOCIATED_WITH'
                    #OR
                        #predicate='NEG_ASSOCIATED_WITH'
                    #OR
                        #predicate='COMPLICATES'
                    #OR
                        #predicate='NEG_COMPLICATES'
                    #OR
                        #predicate='DISRUPTS'
                    #OR
                        #predicate='NEG_DISRUPTS'
                    #OR
                        #predicate='PREDISPOSES'
                    #OR
                        #predicate='NEG_PREDISPOSES'
                    #OR
                        #predicate='TREATS'
                    #OR
                        #predicate='NEG_TREATS'
                    #OR
                        #predicate='INHIBITS'
                    #OR
                        #predicate='NEG_INHIBITS'
                    #OR
                        #predicate='DISRUPTS'
                    #OR
                        #predicate='NEG_DISRUPTS'
                    #OR
                        #predicate='STIMULATES'
                    #OR
                        #predicate='NEG_STIMULATES'
                #)
                #ORDER BY o_type
                #"""
        
        dic = makeSemanticDict('SRDEF.txt')
        pprint.pprint(dic, fil)
        
        fil.write("query:\n" + query + "\n")
        cursor.execute(query)

        for predicate in cursor:
            pprint.pprint(predicate, fil)
            #allObjects.write(dic[predicate[0]] + " -> " + predicate[0] + "\n")
            fil.write("\n")
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
