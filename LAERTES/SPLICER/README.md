OHDSI KB Source : SPLICER - Adverse Drug Events from FDA Structured Product Labels (SPLs)

NOTE: See LICENSE for important information on legal requirements on the use
of this data.

Convert SPLICER output to RDF to support the OHDSI KB use cases.

- splicer2rdf.py : Accepts as input a tab delimitted file containing
  adverse drug events extracted from FDA SPLs by SPLICER and produces
  as output an ntriples file that represents the SPLICER data using
  the Open Annotation Data (OA) schema
  (http://www.openannotation.org/spec/core/)

NOTE: an editable diagram of the OA model for SPLICER ADE records can
be found in [Schema/OpenAnnotationSchemaERDiagrams/](https://github.com/OHDSI/KnowledgeBase/tree/master/Schema/OpenAnnotationSchemaERDiagrams}

NOTE: The output of this script is too large to load into virtuoso
through the web interface. See below for instructions on loading the
dataset using isql-vt

- writeLoadableSPLICERcounts.py : Once the RDF output of the
splicer2rdf.py script is loaded into a virtuoso endpoint, a query in the
following form is ran at the endpoint (see
RDF-count-and-drill-down-queries.sparql or the comments in writeLoadableSPLICERcounts.py): 

SELECT count(distinct ?an) ?drug ?hoi
...

This query gives the counts for records present in SPLs processed by
SPLICER for all drugs and HOIs present in the database. This data is
saved into a tab delimitted file (most recently
test-query-of-counts-09102014.csv) that is loaded by
writeLoadableSPLICERcounts.py. The script then generates a file (most
recently drug-hoi-counts-with-linkouts-SPLICER-09102014.tsv) that can
be loaded into the relational Schema table 'drug_hoi_evidence'. An
example record:

drug_hoi_relationship	evidence_type	modality	evidence_source_code_id	statistic_value	evidence_linkout	statistic_type
40184727-35809076       SPL_SPLICER     positive        2       7       http://dbmi-icode-01.dbmi.pitt.edu/l/index.php?id=0     COUNT

The data in this file can then be used in the LAERTES evidence base.

NOTE: The output of writeLoadableSPLICERcounts.py includes data that
      needs to be loaded into the database for the URL shortener
      (harryjrc_linx). This output is too large for a single load so
      it has to be split into file sizes smaller than 1G. You also
      have to make sure that both the mysql server and client have the
      max_allowed_packet=999M

### To split the INSERT query into files that can be loaded in mysql
$ split -l 400000 insertShortURLs-ALL.txt insertShortURLs-ALL

# this creates files like insertShortURLsaa, insertShortURLsab, insertShortURLsac etc.
# These each need an SQL INSERT clause as the first line and a semi-colon at the end
# For all files:
$ sed -i '1s/^/INSERT INTO lil_urls VALUES \n/' insertShortURLsaa
# For all but the last file:
$ sed -i "\$s/,$/;/" insertShortURLsaa
# For the last file
sed -i "\$s/$/;/" insertShortURLsac
# Now you have to start the mysql client like this:
$ mysql --max_allowed_packet=999M -u <user> -p --local-infile
# select the database and the source each file


------------------------------------------------------------

LOADING THE RDF DATA INTO VIRTUOSO:

-- FIRST TIME ONLY
-- MAKE SURE THAT THE PATH WHERE THE DATA FILE RESIDES IS IN THE DirsAllowed LIST OF virtuoso.ini AND RESTART VIRTUOSO
$ INSERT INTO DB.DBA.load_list (ll_file,ll_graph) values('<PATH TO drug-hoi-splicer.n3>', 'http://purl.org/net/nlprepository/ohdsi-adr-splicer-poc');
-- END OF FIRST TIME ONLY

$ select * from DB.DBA.load_list
-- IF LL_STATE = 0 THEN THE DATASET IS READY TO LOAD

$ rdf_loader_run();

-- ELSE, CLEAR THE GRAPH AND THE SET LL_STATE TO 0

$ SPARQL CLEAR GRAPH 'http://purl.org/net/nlprepository/ohdsi-adr-splicer-poc' ;
$ UPDATE DB.DBA.load_list SET ll_state = 0 WHERE ll_graph = 'http://purl.org/net/nlprepository/ohdsi-adr-splicer-poc';
$ rdf_loader_run();

