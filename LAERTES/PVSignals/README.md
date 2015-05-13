Pharmacovigilance signals mined from the FAERS
====

Data from pharmacoviglance signals mined from FDA Adverse Event
Reporting System will also be included in the OHDSI KB. This folder
holds some data to test the best approach to loading the data into the
OHDSI Postgres DB drug_HOI_evidence table.

The signal data from AERS was generated from Columbia University
associating proportional reporting ratios (PRR) and signal counts for
specific drug-condition pairs.  

Please be sure to cite the following paper for any work you publish or
present that used AERS count or signal data:

N. P. Tatonetti, P. P. Ye, R. Daneshjou, R. B. Altman, Data-Driven Prediction of Drug Effects and Interactions. Sci Transl Med 4, 125ra31–125ra31 (2012).


Conditions were identified from a UMLS_ID and drugs come across form
the sources as a STITCH_ID and Columbia translated that into one or
many ATC codes.  We translated the UMLS_ID into a SNOMED OMOP
Vocabulary CONCEPT_ID and the ATC code into a RxNorm OMOP Vocabulary
CONCEPT_ID.
 
[CONDITIONS] Translation of UMLS_ID to SNOMED:
There were two path’s taken to get the UMLS_ID mapped to SNOMED.
 
Path 1

Sometimes the CUI given in UMLS_ID from the AERS signals had a direct
mapping in UMLS from CUI to US based English SNOMED Preferred Terms.
This was our primary mapping, 64% of the records in the AERS file used
a mapping that went directly from UMLS_ID to SNOMED.  In using the
UMLS CUI to SNOMED map, a small percentage (1%) of the CUIs mapped to
multiple SNOMED codes; in order to choose we just selected the
MAX(SNOMED_CODE).  Once we have the SNOMED code from UMLS, we can use
the Vocabulary to translate this SNOMED_CODE into an OMOP CONCEPT_ID.
A small percentage (2%) of the SNOMED_CODEs did not have a mapping in
the OMOP Vocabulary.
 
Path 2

For the CUIs did not find a mapping in Path 1, we tried to go through
MedDRA; CUI to MedDRA to SNOMED.  This was our secondary mapping and
an additional 7% of records in the AERS file.  In using the UMLS CUI
to MedDRA map, a small percentage (3%) of the CUIs mapped to multiple
MedDRA codes; in order to choose just selected the MAX(MEDDRA_CODE).
Using the OMOP Vocabulary we were able to create a mapping from MedDRA
Preferred Terms to SNOMED clinical findings, we choose the SNOMED term
that the OMOP Vocabulary deemed to be the “closest” in relationship.
 
With both paths, we were able to map 71% of the UMLS_IDs to
Conditions.  Laertes will exclude rows where a condition was not
mapped.
 
[DRUGS] Translation of STITCH_ID to ATC to RxNORM:

The raw AERs data does not come with codified drugs.  There are many
publicized processes for converting the free text given for a drug to
some type of codified drug vocabulary.  Columbia choose to map it to a
STITCH_ID from PubChem.  Columbia also provided a mapping from
STITCH_ID to an ATC code.  We used the ATC code to help us map into
the OMOP Vocabulary.  However there is an important note with the
STITCH_ID to ATC code mapping, in some cases there was not a one to
one mapping and a drug was mapped to several analogous drugs (this is
an important note for when summing up counts when rolling up in a drug
classification, it would be inappropriate for our current version of
AERS because you would end up with double counting).
 
We were able to map 95% of the AERs records to an RxNORM CONCEPT_ID in
the OMOP Vocabulary.


COLUMNS:


stitch_id
umls_id
pvalue
drug_mean
drug_sd
bg_mean
bg_sd
drug_num
bg_num
t_statistic
df
drug_cutoff
ind_cutoff
prr
t_denorm_gtr0
t_dnorm_gtr0
e_score_de
chisq
chisq_pvalue
rr
chemical
AERS_COUNTS
CONDITION_CONCEPT_ID
CONDITION_CONCEPT_NAME
INGREDIENT_CONCEPT_ID
INGREDIENT_CONCEPT_NAME
MAPPING_TYPE

