OHDSI KB - Source - PubMed using MeSH tags


The scripts in this folder retrieve MEDLINE records for indexed
literature reporting adverse drug events and store the data for
further processing. The program implements the method described in:

Avillach P, Dufour JC, Diallo G, Salvo F, Joubert M, Thiessard F, Mougin F, Trifirò G, Fourrier-Réglat A, Pariente A, Fieschi M. Design and val     idation of an automated method to detect known adverse drug reactions in MEDLINE: a contribution from the EU-ADR project. J Am Med Inform Assoc. 2013 May 1;20(3):446-52. doi: 10.1136/amiajnl-2012-001083. Epub 2012 Nov 29. PubMed PMID: 23195749; PubMed Central PMCID: PMC3628051.

The process works as follows:

1. The MEDLINE database is loaded into a postgres DBMS using the code from https://github.com/OHDSI/MedlineXmlToDatabase 

2. The MEDLINE database is queried using the script
   queryDrugHOIAssociations.psql for drugs and drug classes associated
   with specific adverse events according to MeSH tags. See the header
   of that script for USAGE.

3. The tab-delimitted output of Step 2 is is processed by
   pmSearch2rdf.py to convert the results to an RDF Open Data
   Annotation graph. Please see the NOTES below.

4. The RDF graph is loaded into an endpoint and script
   writeLoadablePubMedMeSHCounts.py generates "tinyurls" for queries
   against the RDF dataset to support the "drill down" use case. 

NOTE: The output of writeLoadablePubMedMeSHCounts.py includes data that
      needs to be loaded into the database for the URL shortener
      (harryjrc_linx). This output may be too large for a single load so
      it has to be split into file sizes smaller than 1G. You also
      have to make sure that both the mysql server and client have the
      max_allowed_packet=999M

### To split the INSERT query into files that can be loaded in mysql
$ split -l 400000 insertShortURLs-ALL.txt insertShortURLs

# this creates files like insertShortURLsaa, insertShortURLsab, insertShortURLsac etc.
# These each need an SQL INSERT clause as the first line and a semi-colon at the end
# For all files:
$ sed -i '1s/^/INSERT INTO lil_urls VALUES \n/' insertShortURLsaa
# For all but the last file:
$ sed -i "\$s/,$/;/" insertShortURLsaa
# For the last file
$ sed -i "\$s/$/;/" insertShortURLsac
# Now you have to start the mysql client like this:
$ mysql --max_allowed_packet=999M -u <user> -p --local-infile
# select the database and the source each file


5. See Schema/postgresql/README.md for how the results of the above
   process get loaded into the LAERTES database

NOTES: 

- Because some of the drug - HOI associations use drug classes rather
than individual substances, we use the pharmacologic substance
mappings provided by MeSH (http://www.nlm.nih.gov/mesh/pa_abt.html) to
create a collection of the MeSH, OHDSI/IMEDS Standard Vocab, and
RxNorm, drug entities assigned to each grouping (see
terminology-mappings/MeSHPharmocologicActionToSubstances/README). This
grouping data is not complete so review the log output of the script
for drug entities that could not be mapped. For example, the group
D006146 (Guanidines) and this does not appear in the pharmacologic
action mapping but is assigned an adverse effect in MEDLINE record
<http://www.ncbi.nlm.nih.gov/pubmed/7446541?report=xml&format=text>. Also,
not all drug entities that MeSH lists in a grouping can be mapped to
the Standard Vocabulary or RxNorm. Please see the log output of the
script for specific cases.

- Though relatively infrequent, there are some MEDLINE records that
have more than one publication type assigned (e.g.,
http://www.ncbi.nlm.nih.gov/pubmed/8977519). For now, all of the
publication types are added to the target graph using the
http://purl.org/net/ohdsi#MeshStudyType predicate. 

- This implementation of the Avillach et al method allows adverse drug
effects reported in animals (recognizable by the presence in the
MEDELINE MeSH qualifier record of the "veterinary" QualifierName)to be
included in the results. The query or RDF output could be modified in
the future to address this. For now, it appears that the Standard
Vocabulary has removed HOIs that are specific to animals (e.g., Dog
Diseases (D004283)) so, the records might not make it into the LAERTES
evidence base. 

SEE ALSO:

- PubMed-MeSH-ER-diagram.dia : a diagram of the RDF data model editable using Dia (see PubMed-MeSH-ER-diagram.png for an exported version)

TODOs (1/10/2015):

- Develop a policy for handling non-human adverse effects

- Develop a policy for dealing with the MeSH pharmacologic action groupings

- Port the method for generating 'tinyurls' to use a more efficient technique that just appends rows to the main 'tinyurl' table

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

