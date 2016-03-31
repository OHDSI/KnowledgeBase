The Comparative Toxicogenomics Database (CTD)

Overview

“A collaboration between safety researchers at Pfizer and the research
team at the Comparative Toxicogenomics Database (CTD) to text mine and
manually review a collection of 88,629 articles relating over 1,200
pharmaceutical drugs to their potential involvement in cardiovascular,
neurological, renal and hepatic toxicity. In 1 year, CTD biocurators
curated 254,173 toxicogenomic interactions (152,173 chemical-disease,
58,572 chemical-gene, 5,345 gene-disease and 38,083 phenotype
interactions). All chemical-gene-disease interactions are fully
integrated with public CTD, and phenotype interactions can be
downloaded.” - http://www.ncbi.nlm.nih.gov/pubmed/?term=24288140



INSTRUCTIONS:
(1) Go to http://ctdbase.org
(2) Click on "Download", then on "Data Files" from the dropdown
    menu.
(3) Scroll down to "Chemical-disease associations".
(4) Click on and download "CTD_chemicals.tsv.gz".
(5) Extract the file "CTD_chemicals.tsv" to the "CTD" folder within LAERTES.
(6) Run this script as "python CTD2rdf.py".
(7) This script currently takes longer than 10 minutes to run, but
    will produce the file "chemical-disease-ctd.nt" upon completion.


"CTD_chemicals.tsv" contains the following fields:
(1) ChemicalName
(2) ChemicalID (MeSH identifier)
(3) CasRN (CAS Registry Number, if available)
(4) DiseaseName
(5) DiseaseID (MeSH or OMIM identifier) 
(6) DirectEvidence ('|'-delimited list)
(7) InferenceGeneSymbol
(8) InferenceScore
(9) OmimIDs ('|'-delimited list)
(10) PubMedIDs ('|'-delimited list

NOTE: These fields apply to the December 2015 CTD data release.


------------------------------------------------------------

LOADING THE RDF DATA INTO VIRTUOSO:

-- FIRST TIME ONLY
$ INSERT INTO DB.DBA.load_list (ll_file,ll_graph) values('<PATH TO THE RDF DATA FOR CTD>', 'http://purl.org/net/nlprepository/ohdsi-ctd-chem-disease-poc');
-- MAKE SURE THAT THE PATH WHERE THE DATA FILE RESIDES IS IN THE DirsAllowed list of virtuoso.ini 
-- END OF FIRST TIME ONLY

$ select * from DB.DBA.load_list

------------------------------------------------------------
ll_file                                                                           ll_graph                                                                          ll_state    ll_started           ll_done              ll_host     ll_work_time  ll_error
VARCHAR NOT NULL                                                                  VARCHAR                                                                           INTEGER     TIMESTAMP            TIMESTAMP            INTEGER     INTEGER     VARCHAR
_______________________________________________________________________________

/home/rdb20/OHDSI-code/KnowledgeBase/LAERTES/CTD/chemical-disease-ctd.nt          http://purl.org/net/nlprepository/ohdsi-ctd-chem-disease-poc                      0           NULL                 NULL                 NULL        NULL        NULL
------------------------------------------------------------

-- IF LL_STATE = 0 THEN THE DATASET IS READY TO LOAD

$ rdf_loader_run();

-- ELSE, CLEAR THE GRAPH AND THE SET LL_STATE TO 0

$ SPARQL CLEAR GRAPH 'http://purl.org/net/nlprepository/ohdsi-ctd-chem-disease-poc' ;
$ UPDATE DB.DBA.load_list SET ll_state = 0 WHERE ll_graph = 'http://purl.org/net/nlprepository/ohdsi-ctd-chem-disease-poc';
$ rdf_loader_run();


