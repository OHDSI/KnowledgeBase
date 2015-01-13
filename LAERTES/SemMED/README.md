OHDSI KB - Source - PubMed via SemMedDB (http://skr3.nlm.nih.gov/)
======


Background: The Semantic Knowledge Representation project conducts
basic research in symbolic natural language processing based on the
UMLS knowledge sources. A core resource is the SemRep program, which
extracts semantic predications from text. SemRep was originally
developed for biomedical research. A general methodology is being
developed for extending its domain, currently to influenza epidemic
preparedness, health promotion, and health effects of climate change.

The scripts in this folder 1) retrieve STATEMENTS from MEDLINE records
that might report adverse drug events, or that such events DO NOT
occur, and 2) store the data for further processing. 

The process works as follows:

1. The MEDLINE database is loaded into a postgres DBMS using the code from https://github.com/OHDSI/MedlineXmlToDatabase 

2. The SemMedDB database is loaded into a MySql DBMS following the
instructions for that resource.

3. The python script selectTriplesPlusSentence.py is used to get our final tab-delimited output:
[semmedTriplesPlusSentence.tsv](https://github.com/OHDSI/KnowledgeBase/blob/master/SemMED/semmedTriplesPlusSentence.tsv). This outputs the Drug CUIs, HOI CUIs, their positions in the sentence, the confidence score of the selection, sentence itself, and location of the sentence within the Pubmed source. Please see below for an explanation of the columns output by the script. 

4. 

######Problems:
- There is a one-to-many mapping between UMLS and SNOMED+MEDDRA so what I did is I put the CUIs with that mapping pipe-delimited inside each column.

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
