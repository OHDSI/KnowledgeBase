The Comparative Toxicogenomics Database (CTD)

OVERVIEW

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

------------------------------------------------------------
DATA CITATION:
Curated chemical–disease data were retrieved from the Comparative Toxicogenomics Database (CTD), MDI Biological Laboratory, Salisbury Cove, Maine, and NC State University, Raleigh, North Carolina. World Wide Web (URL: http://ctdbase.org/). [March, 2016]

------------------------------------------------------------
LEGAL NOTICES:
Legal Notices
The Comparative Toxicogenomics DatabaseTM (CTDTM) is provided to enhance knowledge and encourage progress in the scientific community. It is to be used only for research and educational purposes. Medical treatment decisions should not be made based on the information in CTD.

Any reproduction or use for commercial purpose is prohibited without the prior express written permission of the MDI Biological Laboratory and NC State University.

This data and software are provided “as is”, “where is” and without any express or implied warranties, including, but not limited to, any implied warranties of merchantability and/or fitness for a particular purpose, or any warranties that use will not infringe any third party patents, copyrights, trademarks or other rights. In no event shall the MDI Biological Laboratory nor NC State University, nor their agents, employers or representatives be liable for any direct, indirect, incidental, special, exemplary, or consequential damages however caused and on any theory of liability, whether in contract, strict liability, or tort (including negligence or otherwise) arising in any way or form out of the use of this data or software, even if advised of the possibility of such damage.

THE COMPARATIVE TOXICOGENOMICS DATABASE and CTD are trademarks of the MDI Biological Laboratory and NC State University. All rights reserved.

Copyright 2002-2012 MDI Biological Laboratory. All rights reserved.

Copyright 2012-2016 MDI Biological Laboratory & NC State University. All rights reserved.

Additional Terms of Data Use
Use of CTD data is subject to the following additional terms:

All forms of publication (e.g., web sites, research papers, databases, software applications, etc.) that use or rely on CTD data must cite CTD. Please follow our citation guidelines.
All electronic or online applications must include hyperlinks from contexts that use CTD data to the applicable CTD data pages. Please refer to our linking instructions.
You must notify CTD and describe your use of our data.
For quality control purposes, you must provide CTD with periodic access to your publication of our data.
NLM Terms
Data from the U.S. National Library of Medicine (NLM) are provided pursuant to the following terms:

NLM represents that its data were formulated with a reasonable standard of care. Except for this representation, NLM makes no representation or warranties, expressed or implied. This includes, but is not limited to, any implied warranty of merchantability or fitness for a particular purpose, with respect to the NLM data, and NLM specifically disclaims any such warranties and representations.

NLM databases are produced by a U.S. Government agency and as such are not protected by US copyright laws. Use of the databases outside the United States may be governed by applicable foreign copyright laws.

All complete or parts of NLM-derived records that are redistributed or retransmitted must be identified as being derived from NLM databases. Examples are: “From MEDLINE®/PubMed®, a database of the U.S. National Library of Medicine.” and “MeSH Headings from MEDLINE®/PubMed®, a database of the U.S. National Library of Medicine.”

Some material in the NLM databases derives from copyrighted publications. Publishers and/or authors often claim copyright on the abstracts in MEDLINE®/PubMed®. Refer to the publication data appearing in the citations, as well as to the copyright notices appearing in the original publications, all of which are hereby incorporated by reference. Users of the NLM databases are solely responsible for compliance with fair use guidelines and applicable copyright restrictions. Users should consult legal counsel before using NLM-produced records to be certain that their plans are in compliance with appropriate laws.

CAS Registry Number
CAS Registry Number is a Registered Trademark of the American Chemical Society.

------------------------------------------------------------
INSTRUCTIONS TO RETRIEVE THE DATA:

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
INSTRUCTIONS FOR LOADING THE DATA

The process works as follows:

1. The tab-delimitted CTD_chemicals.tsv is processed by
   CTD2rdf.py to convert the results to an RDF Open Data
   Annotation graph. Please see the NOTES below.

   NOTE: The data file has a one to many mapping between
   chemical-disease pair and both Pubmed IDs and OMIM IDs. The OA
   graph creates a single OA for each chemical-disease-PubMedID or
   chemical-disease-OMIM id triple.


   NOTE: if the output has to be transferred to a remote location, the
   following approach is recommended (set up .ssh/config if using public/private keys): 

   $ rsync -e ssh -av --progress --partial chemical-disease-ctd.nt  user@remote-server:<destination folder>/chemical-disease-ctd.nt


4. The RDF graph is loaded into an endpoint and script
   writeLoadableCTDcounts.py generates "tinyurls" for queries
   against the RDF dataset to support the "drill down" use case. The
   script is ran like this to produce the a file with both counts and
   linkouts that is loaded into the LAERTES evidence table:

   $ python writeLoadableCTDcounts.py > drug-hoi-counts-with-linkouts-CTD-March<some date>.tsv

NOTE: The output of writeLoadableCTDcounts.py includes data that
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


