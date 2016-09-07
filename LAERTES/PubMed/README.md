OHDSI KB - Source - PubMed using MeSH tags


The scripts in this folder retrieve MEDLINE records for indexed
literature reporting adverse drug events and store the data for
further processing. The program implements a modified version of the
method described in:

Avillach P, Dufour JC, Diallo G, Salvo F, Joubert M, Thiessard F, Mougin F, Trifirò G, Fourrier-Réglat A, Pariente A, Fieschi M. Design and val     idation of an automated method to detect known adverse drug reactions in MEDLINE: a contribution from the EU-ADR project. J Am Med Inform Assoc. 2013 May 1;20(3):446-52. doi: 10.1136/amiajnl-2012-00
1083. Epub 2012 Nov 29. PubMed PMID: 23195749; PubMed Central PMCID: PMC3628051.

Please note the following licensing information:  

''
NLM represents that its data were formulated with a reasonable standard of care. Except for this representation, NLM makes no representation or warranties, expressed or implied. This includes, but is not limited to, any implied warranty of merchantability or fitness for a particular purpose, with respect to the NLM data, and NLM specifically disclaims any such warranties and representations.
''

''
NLM data are produced by a U.S. Government agency and include works of the United States Government that are not protected by U.S. copyright law but may be protected by non-US copyright law, as well as abstracts originating from publications that may be protected by U.S. copyright law.  
''

''
NLM assumes no responsibility or liability associated with use of copyrighted material, including transmitting, reproducing, redistributing, or making commercial use of the data. NLM does not provide legal advice regarding copyright, fair use, or other aspects of intellectual property rights. Persons contemplating any type of transmission or reproduction of copyrighted material such as abstracts are advised to consult legal counsel.
''

------------------------------------------------------------

The process works as follows:

1. The MEDLINE database is loaded into a postgres DBMS using the code from https://github.com/OHDSI/MedlineXmlToDatabase (this can come from updates from the NLM FTP server, e.g., via  ncftpget -R -v -u anonymous -p <user> ftp.nlm.nih.gov <target folder> /nlmdata/.medlease/gz/)


2. The MEDLINE database is queried using the script
   queryDrugHOIAssociations.psql for drugs and drug classes associated
   with specific adverse events according to MeSH tags. See the header
   of that script for USAGE.

3. The tab-delimitted output of Step 2 is is processed by
   pmSearch2rdf.py to convert the results to an RDF Open Data
   Annotation graph. Please see the NOTES below.

   NOTE: The main modification to the original method reported by
   Avillach et al is to integrate Semmeddb named entity recognition to
   address MeSH pharmacologic entities that represent groups of
   drugs. MeSH pharmacologic entities that represent groups of drugs
   are used quite a bit by MEDLINE. Semmeddb is used to identify any
   specific drugs in a grouping that are mentioned in the pubmed title
   or abstract.  Drug - HOI evidence provided in an OA graph where the
   drug is in 'adeAgents' is limited to only those specific
   drugs. Collections under 'adeAgentsUnfiltered' hold the drugs
   within a pharmacologic grouping that were not found in the title or
   abstract. The negative control use case appears to benefit from the
   much less specific (and often just incorrect) approach of including
   inferring the drug-HOI associations apply to all drugs within a
   pharmacologic grouping.

   NOTE: There are all kinds of duplication that occurs in the output
   file mentioned above. Take the following example:

17766   Adrenergic beta-Antagonists     D000319 Arrhythmias, Cardiac    D001145 Journal Article D016428
17766   Adrenergic beta-Antagonists     D000319 Diarrhea        D003967 Journal Article D016428
17766   Adrenergic beta-Antagonists     D000319 Heart Failure   D006333 Journal Article D016428
17766   Adrenergic beta-Antagonists     D000319 Hypoglycemia    D007003 Journal Article D016428
17766   Adrenergic beta-Antagonists     D000319 Hypotension     D007022 Journal Article D016428
17766   Adrenergic beta-Antagonists     D000319 Muscle Cramp    D009120 Journal Article D016428
17766   Adrenergic beta-Antagonists     D000319 Skin Diseases   D012871 Journal Article D016428
17766   Practolol       D011217 Arrhythmias, Cardiac    D001145 Journal Article D016428
17766   Practolol       D011217 Diarrhea        D003967 Journal Article D016428
17766   Practolol       D011217 Heart Failure   D006333 Journal Article D016428
17766   Practolol       D011217 Hypoglycemia    D007003 Journal Article D016428
17766   Practolol       D011217 Hypotension     D007022 Journal Article D016428
17766   Practolol       D011217 Muscle Cramp    D009120 Journal Article D016428
17766   Practolol       D011217 Skin Diseases   D012871 Journal Article D016428

   In this case, the MEDLINE record was tagged with both a drug
   grouping and an individual drug causing duplication. The OA
   generation script attempts to remove duplication and create only
   one OA body for each PMID-drug-HOI triple.

   Another kind of duplication is shown in this example:

311     Enflurane       D004737 Jaundice        D007565 Case Reports    D002363
311     Enflurane       D004737 Jaundice        D007565 Journal Article D016428
311     Methyl Ethers   D008738 Jaundice        D007565 Case Reports    D002363
311     Methyl Ethers   D008738 Jaundice        D007565 Journal Article D016428

   In this case, a single OA target will be created with multiple
   objects assigned to http://purl.org/net/ohdsi#MeshStudyType (one
   for case reports and one for journal articles (mapped to
   'Other')). A single OA body for Enflurane is created. Then, the
   Methyl Esters group is checked for individual drugs. Because none
   are found, no additional body is created.

   Yet another example:

658     Adrenergic beta-Agonists        D000318 Depression      D003863 Journal Article D016428
658     Adrenergic beta-Agonists        D000318 Depression      D003863 Case Reports    D002363
658     Adrenergic beta-Agonists        D000318 Hallucinations  D006212 Journal Article D016428
658     Adrenergic beta-Agonists        D000318 Hallucinations  D006212 Case Reports    D002363
658     Albuterol       D000420 Depression      D003863 Journal Article D016428
658     Albuterol       D000420 Depression      D003863 Case Reports    D002363
658     Albuterol       D000420 Hallucinations  D006212 Journal Article D016428
658     Albuterol       D000420 Hallucinations  D006212 Case Reports    D002363
658     Isoxsuprine     D007556 Depression      D003863 Journal Article D016428
658     Isoxsuprine     D007556 Depression      D003863 Case Reports    D002363
658     Isoxsuprine     D007556 Hallucinations  D006212 Journal Article D016428
658     Isoxsuprine     D007556 Hallucinations  D006212 Case Reports    D002363
658     Phenethylamines D010627 Depression      D003863 Journal Article D016428
658     Phenethylamines D010627 Depression      D003863 Case Reports    D002363
658     Phenethylamines D010627 Hallucinations  D006212 Journal Article D016428
658     Phenethylamines D010627 Hallucinations  D006212 Case Reports    D002363

   In this case, a single target is created with two objects assigned
   to http://purl.org/net/ohdsi#MeshStudyType. Two bodies are created
   for the Adrenergic beta-Agonists.The MeSH pharmacologic grouping
   file contains the drug group and so Semmedb is checked for mentions
   involving specific drugs within the group. None are found. Then,
   two bodies are created for Albuterol and Isoxsuprine. No body is
   created for Phenethylamines because the MeSH pharmacologic grouping
   file does not list the group

   It is worth looking at one more example:

5066    Amantadine      D000547 Basal Ganglia Diseases  D001480 Clinical Trial  D016430
5066    Amantadine      D000547 Basal Ganglia Diseases  D001480 Comparative Study       D003160
5066    Amantadine      D000547 Basal Ganglia Diseases  D001480 Journal Article D016428
5066    Antipsychotic Agents    D014150 Basal Ganglia Diseases  D001480 Clinical Trial  D016430
5066    Antipsychotic Agents    D014150 Basal Ganglia Diseases  D001480 Comparative Study       D003160
5066    Antipsychotic Agents    D014150 Basal Ganglia Diseases  D001480 Journal Article D016428
5066    Benztropine     D001590 Basal Ganglia Diseases  D001480 Clinical Trial  D016430
5066    Benztropine     D001590 Basal Ganglia Diseases  D001480 Comparative Study       D003160
5066    Benztropine     D001590 Basal Ganglia Diseases  D001480 Journal Article D016428

   In this case, a single OA target is created with two objects
   assigned to http://purl.org/net/ohdsi#MeshStudyType (the
   Comparative Study and Journal Article are both mapped to
   "Other"). A single body is created for Amantadine. A single body is
   created for the Antipsychotic Agents.The MeSH pharmacologic
   grouping file contains the drug group and so Semmedb is checked for
   mentions involving specific drugs within the group. None are
   found. A single body is created for Benztropine.


   Yet another example:

17766   Adrenergic beta-Antagonists     D000319 Arrhythmias, Cardiac    D001145 Journal Article D016428
17766   Adrenergic beta-Antagonists     D000319 Diarrhea        D003967 Journal Article D016428
17766   Adrenergic beta-Antagonists     D000319 Heart Failure   D006333 Journal Article D016428
17766   Adrenergic beta-Antagonists     D000319 Hypoglycemia    D007003 Journal Article D016428
17766   Adrenergic beta-Antagonists     D000319 Hypotension     D007022 Journal Article D016428
17766   Adrenergic beta-Antagonists     D000319 Muscle Cramp    D009120 Journal Article D016428
17766   Adrenergic beta-Antagonists     D000319 Skin Diseases   D012871 Journal Article D016428
17766   Practolol       D011217 Arrhythmias, Cardiac    D001145 Journal Article D016428
17766   Practolol       D011217 Diarrhea        D003967 Journal Article D016428
17766   Practolol       D011217 Heart Failure   D006333 Journal Article D016428
17766   Practolol       D011217 Hypoglycemia    D007003 Journal Article D016428
17766   Practolol       D011217 Hypotension     D007022 Journal Article D016428
17766   Practolol       D011217 Muscle Cramp    D009120 Journal Article D016428
17766   Practolol       D011217 Skin Diseases   D012871 Journal Article D016428

   A single target is created with only on value assigned to
   http://purl.org/net/ohdsi#MeshStudyType. The MeSH pharmacologic
   grouping file contains the drug group Adrenergic beta-Antagonists
   and so Semmedb is checked for mentions involving specific
   drugs. Practolol is found within the abstract so a body is created
   for each Adrenergic beta-Antagonists - HOI association and each
   body has a http://purl.org/net/ohdsi#adeAgents predicate with three
   resources, one each for the practolol identifier in rxnorm, OHDSI,
   and MeSH. This sums up to 7 bodies. No additional OA bodies are
   created for the Practol records shown above because that
   information is already captured by the bodies for Adrenergic
   beta-Antagonists.

   A final example:

17162   Adrenergic beta-Antagonists     D000319 Asthma  D001249 Journal Article D016428
17162   Adrenergic beta-Antagonists     D000319 Hypercalcemia   D006934 Journal Article D016428
17162   Adrenergic beta-Antagonists     D000319 Hyperglycemia   D006943 Journal Article D016428
17162   Adrenergic beta-Antagonists     D000319 Hypoglycemia    D007003 Journal Article D016428
17162   Adrenergic beta-Antagonists     D000319 Kidney Failure, Chronic D007676 Journal Article D016428
17162   Adrenergic beta-Antagonists     D000319 Nephrotic Syndrome      D009404 Journal Article D016428
17162   Adrenergic beta-Antagonists     D000319 Neurasthenia    D009440 Journal Article D016428
17162   Adrenergic beta-Antagonists     D000319 Placental Insufficiency D010927 Journal Article D016428
17162   Adrenergic beta-Antagonists     D000319 Vomiting        D014839 Journal Article D016428
17162   Practolol       D011217 Asthma  D001249 Journal Article D016428
17162   Practolol       D011217 Hypercalcemia   D006934 Journal Article D016428
17162   Practolol       D011217 Hyperglycemia   D006943 Journal Article D016428
17162   Practolol       D011217 Hypoglycemia    D007003 Journal Article D016428
17162   Practolol       D011217 Kidney Failure, Chronic D007676 Journal Article D016428
17162   Practolol       D011217 Nephrotic Syndrome      D009404 Journal Article D016428
17162   Practolol       D011217 Neurasthenia    D009440 Journal Article D016428
17162   Practolol       D011217 Placental Insufficiency D010927 Journal Article D016428
17162   Practolol       D011217 Vomiting        D014839 Journal Article D016428
17162   Propranolol     D011433 Asthma  D001249 Journal Article D016428
17162   Propranolol     D011433 Hypercalcemia   D006934 Journal Article D016428
17162   Propranolol     D011433 Hyperglycemia   D006943 Journal Article D016428
17162   Propranolol     D011433 Hypoglycemia    D007003 Journal Article D016428
17162   Propranolol     D011433 Kidney Failure, Chronic D007676 Journal Article D016428
17162   Propranolol     D011433 Nephrotic Syndrome      D009404 Journal Article D016428
17162   Propranolol     D011433 Neurasthenia    D009440 Journal Article D016428
17162   Propranolol     D011433 Placental Insufficiency D010927 Journal Article D016428
17162   Propranolol     D011433 Vomiting        D014839 Journal Article D016428

   A single target and 27 bodies are created. This happens because
   none of the individual drugs MeSH assignes to Adrenergic
   beta-Antagonists is found in the title or abstract and so the 9
   HOIs are repeated for the group and then practolol and propranolol.
   

   NOTE: if the output has to be transferred to a remote location, the
   following approach is recommended (set up .ssh/config if using public/private keys): 

   $ rsync -e ssh -av --progress --partial drug-hoi-pubmed-mesh.nt  user@remote-server:<destination folder>/drug-hoi-pubmed-mesh.nt


4. The RDF graph is loaded into an endpoint and script
   writeLoadablePubMedMeSHCounts.py generates "tinyurls" for queries
   against the RDF dataset to support the "drill down" use case. The
   script is ran like this to produce the a file with both counts and
   linkouts that is loaded into the LAERTES evidence table:

   $ python writeLoadablePubMedMeSHCounts.py > drug-hoi-counts-with-linkouts-PUBMED-<some date>.tsv

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

TODOs (3/2016):

- Develop a policy for handling non-human adverse effects

- Port the method for generating 'tinyurls' to use a more efficient technique that just appends rows to the main 'tinyurl' table

- develop an Ant workflow for the entire process 


------------------------------------------------------------

LOADING THE RDF DATA INTO VIRTUOSO:

-- FIRST TIME ONLY
$ INSERT INTO DB.DBA.load_list (ll_file,ll_graph) values('<PATH TO THE RDF DATA FOR PUBMED>', 'http://purl.org/net/nlprepository/ohdsi-pubmed-mesh-poc');
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

$ SPARQL CLEAR GRAPH 'http://purl.org/net/nlprepository/ohdsi-pubmed-mesh-poc' ;
$ UPDATE DB.DBA.load_list SET ll_state = 0 WHERE ll_graph = 'http://purl.org/net/nlprepository/ohdsi-pubmed-mesh-poc';
$ rdf_loader_run();

