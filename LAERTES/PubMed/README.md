OHDSI KB - Source - PubMed using MeSH tags


The scripts in this folder retrieve MEDLINE records for indexed
literature reporting adverse drug events and store the data for
further processing. The program implements the method described in:

Avillach P, Dufour JC, Diallo G, Salvo F, Joubert M, Thiessard F, Mougin F, Trifirò G, Fourrier-Réglat A, Pariente A, Fieschi M. Design and val     idation of an automated method to detect known adverse drug reactions in MEDLINE: a contribution from the EU-ADR project. J Am Med Inform Assoc. 2013 May 1;20(3):446-52. doi: 10.1136/amiajnl-2012-001083. Epub 2012 Nov 29. PubMed PMID: 23195749; PubMed Central PMCID: PMC3628051.

The process works as follows:

1) The MEDLINE database is loaded into a postgres DBMS using the code from https://github.com/OHDSI/MedlineXmlToDatabase 

2) The MEDLINE database is queried using the script
   queryDrugHOIAssociations.psql for drugs and drug classes associated
   with specific adverse events according to MeSH tags. See the header
   of that script for USAGE.

3) The tab-delimitted output of Step 2 is is processed by
   pmSearch2rdf.py to convert the results to an RDF Open Data
   Annotation graph. Because some of the drug - HOI associations use
   drug classes rather than individual substances, the pharmacologic
   substance mappings provided by MeSH
   (http://www.nlm.nih.gov/mesh/pa_abt.html) are used (see
   terminology-mappings/MeSHPharmocologicActionToSubstances/README)

4) The RDF graph is loaded into an endpoint and script
   writeLoadablePubMedMeSHCounts.py generates "tinyurls" for queries
   against the RDF dataset to support the "drill down" use case

5) See Schema/postgresql/README.md for how the results of the above
   process get loaded into the LAERTES database

See also:

- PubMed-MeSH-ER-diagram.dia : a diagram of the RDF data model editable using Dia (see PubMed-MeSH-ER-diagram.png for an exported version)

TODOs (9/9/2014):

- clean up the folder to remove unecessary data files 

- develop an Ant workflow for the entire process 


------------------------------------------------------------

LOADING THE RDF DATA INTO VIRTUOSO:

-- FIRST TIME ONLY
$ INSERT INTO DB.DBA.load_list (ll_file,ll_graph) values('<PATH TO drug-hoi-pubmed-mesh.rdf>', 'http://purl.org/net/nlprepository/ohdsi-pubmed-mesh-poc/');
-- MAKE SURE THAT THE PATH WHERE THE DATA FILE RESIDES IS IN THE DirsAllowed list of virtuoso.ini 
-- END OF FIRST TIME ONLY

$ select * from DB.DBA.load_list

------------------------------------------------------------
ll_file                                                                           ll_graph                                                                          ll_state    ll_started           ll_done              ll_host     ll_work_time  ll_error
VARCHAR NOT NULL                                                                  VARCHAR                                                                           INTEGER     TIMESTAMP            TIMESTAMP            INTEGER     INTEGER     VARCHAR
_______________________________________________________________________________

/home/rdb20/OHDSI/KnowledgeBase/PubMed/drug-hoi-pubmed-mesh.rdf                   http://purl.org/net/nlprepository/ohdsi-pubmed-mesh-poc/                          2           2014.9.9 7:22.2 0    2014.9.9 7:23.18 0   0           NULL        NULL
------------------------------------------------------------

-- IF LL_STATE = 0 THEN THE DATASET IS READY TO LOAD

$ rdf_loader_run();

-- ELSE, CLEAR THE GRAPH AND THE SET LL_STATE TO 0

$ SPARQL CLEAR GRAPH http://purl.org/net/nlprepository/ohdsi-pubmed-mesh-poc/ ;
$ UPDATE DB.DBA.load_list SET ll_state = 0 WHERE ll_graph = 'http://purl.org/net/nlprepository/ohdsi-pubmed-mesh-poc/';
$ rdf_loader_run();

