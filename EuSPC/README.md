European Union Adverse Drug Reactions from Summary of Product Characteristics (EU SPC) Database Import 
=============================================================================================

This table of adverse events from the EU SPCs as downloaded from
[PROTECT](http://www.imi-protect.eu/adverseDrugReactions.shtml)

### Convert EU SPC data to RDF to support the OHDSI KB use cases

- euSPC2rdf.py : Accepts as input a tab delimitted file containing
  adverse drug events extracted from EU SPCs by
  [PROTECT](http://www.imi-protect.eu/adverseDrugReactions.shtml) and
  produces as output a ntriples file that represents the data using
  the Open Annotation Data (OA) schema

NOTE: an editable diagram of the OA model for EU SPC ADE records can
be found in
[Schema/OpenAnnotationSchemaERDiagrams/](https://github.com/OHDSI/KnowledgeBase/tree/master/Schema/OpenAnnotationSchemaERDiagrams}

NOTE: The output of this script is too large to load into virtuoso
through the web interface. See below for instructions on loading the
dataset using isql-vt

### Generating the table of EU SPC data:

The scripts in this folder add RxCUIs and MeSH CUIs to the EU SPC drug
list. In most cases, there was a simple string match between an entry
in the 'substance' column with an RxNorm or MeSH preferred
term. However, there are many cases of combination products, and a few
things that were unable to be mapped. The combination products were
manually mapped where possibly using the Bioportal's ontology search.

The final dataset with the RxCUIs and MeSH CUIs is in
[FinalRepository_DLP30Jun2012_withCUIs_v2.csv](https://github.com/OHDSI/KnowledgeBase/blob/master/EuSPC/data/FinalRepository_DLP30Jun2012_withCUIs_v2.csv).

1. `cd scripts`
2. `python processEuSPCToAddRxNormAndMeSH.py`
3. `python3 getMissingMappings.py ../data/FinalRepository_DLP30Jun2012_withCUIs_v2.csv ../data/missing`

### Processing the EU SPC Drug Listing

The **euspc-drug-listing** holds drug names for single ingredient drugs
listed in the adverse event table. This was created by:

1. `cat FinalRepository_DLP30Jun2012.csv| cut -f3 | sort | uniq > euspc-drug-listing.txt`
2. within emacs:
`replace-regexp  ".*, .*^J" -> ""`


## Subfolders
1. [json-rxcui](https://github.com/OHDSI/KnowledgeBase/tree/master/EuSPC/json-rxcui)
	- Contains the raw output from the [TRIADs drug named entity recognition program](https://swat-4-med-safety.googlecode.com/svn/trunk/u-of-pitt-SPL-drug-NER) used to input one of the big files.
2. [data/missing](https://github.com/OHDSI/KnowledgeBase/tree/master/EuSPC/data/missing)
	- contains the missing CUIs from the second run of [processEuSPCToAddRxNormAndMeSH.py](https://github.com/OHDSI/KnowledgeBase/blob/master/EuSPC/processEuSPCToAddRxNormAndMeSH.py)
3. [backup/missingCUIs](https://github.com/OHDSI/KnowledgeBase/tree/master/EuSPC/backup/missingCUIs)
	- A backup folder containing the output missing CUIs from the first run of [processEuSPCToAddRxNormAndMeSH.py](https://github.com/OHDSI/KnowledgeBase/blob/d2af5e16c2b6f05d59664b93457f90f90da83dea/EuSPC/processEuSPCToAddRxNormAndMeSH.py) using the first [getMissingMappings.py](https://github.com/OHDSI/KnowledgeBase/blob/d933222eca84247c7dcbcc03d203141fb3d98198/EuSPC/getMissingMappings.py) from commit [90f0a68842428c222b9606c05d2d5f129cee7ca4](https://github.com/OHDSI/KnowledgeBase/commit/90f0a68842428c222b9606c05d2d5f129cee7ca4)
	- Also contains the missing CUIs from the first run manually searched in [Bioportal](http://bioportal.bioontology.org/search?opt=advanced)
4. [scripts](https://github.com/OHDSI/KnowledgeBase/tree/master/EuSPC/scripts)
	- location of the scripts file to run
5. [data](https://github.com/OHDSI/KnowledgeBase/tree/master/EuSPC/data)
	- location of the scripts output files


------------------------------------------------------------

LOADING THE RDF DATA INTO VIRTUOSO:

-- FIRST TIME ONLY 
-- MAKE SURE THAT THE PATH WHERE THE DATA FILE RESIDES IS IN THE DirsAllowed LIST OF virtuoso.ini AND RESTART VIRTUOSO
$ INSERT INTO DB.DBA.load_list (ll_file,ll_graph) values('<path to drug-hoi-eu-spc.nt>', 'http://purl.org/net/nlprepository/ohdsi-adr-eu-spc-poc');
-- END OF FIRST TIME ONLY

$ select * from DB.DBA.load_list
-- IF LL_STATE = 0 THEN THE DATASET IS READY TO LOAD

$ rdf_loader_run();

-- ELSE, CLEAR THE GRAPH AND THE SET LL_STATE TO 0

$ SPARQL CLEAR GRAPH 'http://purl.org/net/nlprepository/ohdsi-adr-eu-spc-poc' ;
$ UPDATE DB.DBA.load_list SET ll_state = 0 WHERE ll_graph = 'http://purl.org/net/nlprepository/ohdsi-adr-eu-spc-poc';
$ rdf_loader_run();
