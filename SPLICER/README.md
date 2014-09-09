OHDSI KB Source : SPLICER - Adverse Drug Events from FDA Structured Product Labels (SPLs)

Convert SPLICER output to RDF to support the OHDSI KB use cases.

- splicer2rdf.py : Accepts as input a tab delimitted file containing adverse drug events extracted from FDA SPLs by SPLICER and produces as output a ntriples file that representes the SPLICER data using the Open Annotation Data (OA) schema

- ADR-ER-diagram.dia : an editable diagram of the OA model for SPLICER ADE records (see ADR-ER-diagram.png for a static version)

------------------------------------------------------------

LOADING THE RDF DATA INTO VIRTUOSO:

-- FIRST TIME ONLY
$ INSERT INTO DB.DBA.load_list (ll_file,ll_graph) values('<PATH TO drug-hoi-splicer.n3>', 'http://purl.org/net/nlprepository/ohdsi-adr-splicer-poc');
-- MAKE SURE THAT THE PATH WHERE THE DATA FILE RESIDES IS IN THE DirsAllowed list of virtuoso.ini 
-- END OF FIRST TIME ONLY

$ select * from DB.DBA.load_list

------------------------------------------------------------
ll_file                                                                           ll_graph                                                                          ll_state    ll_started           ll_done              ll_host     ll_work_time  ll_error
VARCHAR NOT NULL                                                                  VARCHAR                                                                           INTEGER     TIMESTAMP            TIMESTAMP            INTEGER     INTEGER     VARCHAR
_______________________________________________________________________________

/home/rdb20/OHDSI/KnowledgeBase/SPLICER/drug-hoi-splicer.n3                   http://purl.org/net/nlprepository/ohdsi-adr-splicer-poc                          2           2014.9.9 7:22.2 0    2014.9.9 7:23.18 0   0           NULL        NULL
------------------------------------------------------------

-- IF LL_STATE = 0 THEN THE DATASET IS READY TO LOAD

$ rdf_loader_run();

-- ELSE, CLEAR THE GRAPH AND THE SET LL_STATE TO 0

$ SPARQL CLEAR GRAPH 'http://purl.org/net/nlprepository/ohdsi-adr-splicer-poc' ;
$ UPDATE DB.DBA.load_list SET ll_state = 0 WHERE ll_graph = 'http://purl.org/net/nlprepository/ohdsi-adr-splicer-poc';
$ rdf_loader_run();

