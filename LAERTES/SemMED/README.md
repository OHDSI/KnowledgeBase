OHDSI KB - Source - PubMed via SemMedDB (http://skr3.nlm.nih.gov/)
======

The [Semantic MEDLINE Database](http://skr3.nlm.nih.gov/SemMedDB/) is
a repository of semantic predications (subject-predicate-object
triples) extracted by SemRep, a semantic interpreter of biomedical
text. 

Please cite the following paper in any publications or presentations of work that uses the data:

Kilicoglu H, Rosemblat G, Fiszman M, Rindflesch TC. Constructing a semantic predication gold standard from the biomedical literature. BMC Bioinformatics. 2011 Dec 20;12:486. doi: 10.1186/1471-2105-12-486. PubMed PMID: 22185221; PubMed Central PMCID: PMC3281188. 

Also, please note the following use requirements:

Use of Semantic Knowledge Representation (SKR) Resources

    * Redistribution of SKR resources in source or binary form must include this list of conditions in the documentation and other materials provided with the distribution.
    
    * In any publication or distribution of all or any portion of an SKR resource (1) you must attribute the source of the tools as the resource name with the release number and date; (2) you must clearly annotate within the source code, any modification made to the resource; and (3) any subsequent distribution of program, tool, or material based on the resource, must be accomplished within the context of an open source set of terms and conditions such as the GNU General License.
    
    * Bugs, questions, and issues relating to an SKR resource should be directed to the most recent of the chain of entities that may have modified and re-distributed this resource.
    
    * You shall not assert any proprietary rights to any portion of an SKR resource, nor represent it or any part thereof to anyone as other than a United States Government product.
    
    * The name of the U.S. Department of Health and Human Services, National Institutes of Health, National Library of Medicine, and Lister Hill National Center for Biomedical Communications may not be used to endorse or promote products derived from any SKR resource without specific prior written permission.
    
    * Neither the United States Government, U.S. Department of Health and Human Services, National Institutes of Health, National Library of Medicine, Lister Hill National Center for Biomedical Communications, nor any of its agencies, contractors, subcontractors or employees of the United States Government make any warranties, expressed or implied, with respect to any SKR resource, and, furthermore, assume no liability for any party's use, or the results of such use, of any part of these tools.

These terms and conditions are in effect as long as the user retains any part of any SKR resource. 


------------------------------------------------------------
The scripts in this folder use the Semantic MEDLINE Database and
a local implementation of PubMed/MEDLINE to:

1) retrieve STATEMENTS from MEDLINE records that might report adverse
drug events, or that such events DO NOT occur,

2) store the data for further processing

3) convert the data into Open Annotation Data RDF 

The process works as follows:

1. The MEDLINE database is loaded into a postgres DBMS using the code
from https://github.com/OHDSI/MedlineXmlToDatabase

2. The SemMedDB database is loaded into a MySql DBMS following the
instructions for that resource.

3. The python script (use Python 3 to run!) selectTriplesPlusSentence.py is used to get our
final tab-delimited output:
[semmedTriplesPlusSentence.tsv](https://github.com/OHDSI/KnowledgeBase/blob/master/SemMED/semmedTriplesPlusSentence.tsv). This
outputs the Drug CUIs, HOI CUIs, their positions in the sentence, the
confidence score of the selection, sentence itself, and location of
the sentence within the Pubmed source. Please see below for an
explanation of the columns output by the script.

4. semMed2rdf.py is ran over the output file
semmedTriplesPlusSentence.tsv to produce an Open Annotation Data graph
drug-hoi-pubmed-semmeddb.nt.

5. The graph is loaded onto a Virtuoso endpoint (see below) and
queried for drug-HOI counts stratified by positive and negative
modality evidence support. The script writeLoadableSemMedCounts.py
generates "tinyurls" for queries against the RDF dataset to support
the "drill down" use case.

------------------------------------------------------------
LOADING THE RDF DATA INTO VIRTUOSO:
------------------------------------------------------------
```
-- FIRST TIME ONLY
$ INSERT INTO DB.DBA.load_list (ll_file,ll_graph) values('<PATH TO drug-hoi-pubmed-semmeddb.nt>', 'http://purl.org/net/nlprepository/ohdsi-pubmed-semmed-poc/');
-- MAKE SURE THAT THE PATH WHERE THE DATA FILE RESIDES IS IN THE DirsAllowed list of virtuoso.ini 
-- END OF FIRST TIME ONLY

$ select * from DB.DBA.load_list

------------------------------------------------------------
ll_file                                                                           ll_graph                                                                          ll_state    ll_started           ll_done              ll_host     ll_work_time  ll_error
VARCHAR NOT NULL                                                                  VARCHAR                                                                           INTEGER     TIMESTAMP            TIMESTAMP            INTEGER     INTEGER     VARCHAR
_______________________________________________________________________________

/home/rdb20/OHDSI/KnowledgeBase/LAERTES/SemMED/drug-hoi-pubmed-semmeddb.nt        http://purl.org/net/nlprepository/ohdsi-pubmed-semmed-poc/                        0           NULL                 NULL                 NULL        NULL        NULL
------------------------------------------------------------

-- IF LL_STATE = 0 THEN THE DATASET IS READY TO LOAD

$ rdf_loader_run();

-- ELSE, CLEAR THE GRAPH AND THE SET LL_STATE TO 0

$ SPARQL CLEAR GRAPH http://purl.org/net/nlprepository/ohdsi-pubmed-semmed-poc/ ;
$ UPDATE DB.DBA.load_list SET ll_state = 0 WHERE ll_graph = 'http://purl.org/net/nlprepository/ohdsi-pubmed-semmed-poc/';
$ rdf_loader_run();
```

######Problems:
- There is a one-to-many mapping between UMLS and SNOMED+MEDDRA. CUIs with this kind of mapping are listed (pipe-delimited) inside each column.

######Explanation of the columns output by selectTriplesPlusSentence.py:
- pmid: the PMID
- predicate: the predicate used to associate the subject and object
- predicate start index: first predicate's character's location in the sentence
- predicate end index: last predicate's character's location in the sentence
- Drug UMLS CUI: UMLS CUI of the subject (drug)
- drug RxNorm: RxNorm drug CUI
- drug MeSH: MeSH drug CUI
- drug Preferred Term: name of the drug from SEMMED
- drug UMLS entity type: name of the drug's UMLS Entity Type
- drug start index: drug's first character's location in the sentence
- drug end index: drug's last character's location in the sentence
- drug distance: The distance of the subject mention (counted in noun phrases) from the predicate mention (0 for certain indicator types, such as NOM)
- drug max distance: The number of potential arguments (in noun phrases) from the predicate mention in the direction of the subject mention (0 for certain indicator types, such as NOM)
- drug max score: (note should not have max in the header...)
- HOI UMLS CUI: Health Outcome of Interest UMLS CUI
- HOI SNOMED: Health Outcome of Interest SNOMED CUI
- HOI MedDRA: Health Outcome of Interest MedDRA CUI
- HOI MeSH: Health Outcome of Interest MeSH CUI
- HOI Preferred Term: name of the HOI from SEMMED
- HOI entity type: name of the HOI's UMLS Entity type
- HOI start index: HOI's first character's location in the sentence
- HOI end index: HOI's last character's location in the sentence
- HOI distance: The distance of the subject mention (counted in noun phrases) from the predicate mention (0 for certain indicator types, such as NOM)
- HOI max distance: The number of potential arguments (in noun phrases) from the predicate mention in the direction of the subject mention (0 for certain indicator types, such as NOM)
- HOI max score: (note should not have max in the header...)
- sentence: the actual sentence of the finding
- sentence location: number that represents the location of the sentence found from its source from PM
- sentence type: sentence was extracted from this type


####Info retrieved...
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


### [selectTriplesPlusSentence.py](https://github.com/OHDSI/KnowledgeBase/blob/master/SemMED/selectTriplesPlusSentence.py)


Selects concept triples with the sentences from which they were derived. 
The output semmedTriplesPlusSentence.tsv has a way to perhaps create a way
to make a simple drilldown and summary case usage.

Prerequisites:

The UMLS CUI to RxNorm, MeSH, SNOMED, and MedDRA Conversion was done with 
UMLS_CUIs.py class which takes the TRIADS data from Dr. Boyce's server, 
process it into its own class (well documented), processed, and then 
pickled using cPickle (in its main). This had to be done in this way 
because it would be impossible otherwise to get the the CUIs as far as 
I was concerned.

File prerequisites:
- UMLS_CUIs.py (python UMLS_CUIs.py)
- umlsStructure.cPickle - UMLS_CUIs class postprocessed file created
  from above python class file
- can only be run on Dr. Boyce's server

Steps that the program does:

1. Query the SemMED DB from the OHDSI dev server
2. open the UMLS_CUIs pickle
3. writes the results via this in [semmedTriplesPlusSentence.tsv](https://github.com/OHDSI/KnowledgeBase/blob/master/SemMED/semmedTriplesPlusSentence.tsv) tab-delimited    

Take Note:
- SEMMED supplies the UMLS CUI
- I used the UMLS CUI to get the RxNorm, MeSH, MedDRA, and SNOMED CUIs
- However, as of right now, there is a one-to-many mapping between UMLS and SNOMED+MEDDRA

so what I did is I put the CUIs with that mapping pipe-delimited inside each column.
