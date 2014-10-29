-- EXAMPLE QUERIES AGAINST THE RELATIONAL DATABASE FOR LAERTES:

-- A general query showing how to bridge all tables
SELECT `drug`,`HOI`,`evidence_type`,`evidence_count`,`evidence_linkout`,evidence_sources.title, evidence_sources.description
FROM `drug_HOI_evidence`, evidence_sources
WHERE evidence_source_code_id = evidence_sources.id


-- Get back all evidence for 'Lisinopril' and 'Uterine leiomyoma' using standard vocab codes
SELECT *
FROM drug_hoi_evidences  
WHERE 
drug = 1308216 AND
hoi = 36617553;


-- Get back all evidence for 'amoxacillin' and 'Pruritis' using
-- standard vocab codes. Returns the following linkout that can be put
-- into the browser to retrieve an OA representation of the data in
-- the product label:
-- http://dbmi-icode-01.dbmi.pitt.edu/l/index.php?id=i9b  
SELECT *
FROM drug_hoi_evidences  
WHERE 
drug = 19123591 AND
hoi = 37320197;


------------------------------------------------------------ 
-- Queries below this line need to get ported but first the
-- Evidence_sources table needs to be revised to tag each evidence
-- source with a type such as literature, labeling,
-- pharmacovigilance_signal_spontaneous_reporting,
-- pharmacovigilance_signal_EHR
------------------------------------------------------------
-- Count literature evidence for 'metronidazole' and 'renal failure'
SELECT COUNT("drug_HOI_evidence".evidence_type)
FROM "drug_HOI_evidence"
WHERE 
drug = 1707164 AND
"HOI" = 37019318 AND
evidence_type LIKE 'literature%'


-- Count case report evidence for 'metronidazole' and 'renal failure'
SELECT COUNT(evidence_type)
FROM "drug_HOI_evidence"
WHERE 
drug = 1707164 AND
"HOI" = 37019318 AND 
evidence_type = 'literature_case_report'


-- get the target URIs for product label evidence for Simvastatin and Upper respiratory tract infection
SELECT evidence_targets.uri
FROM "drug_HOI_evidence", evidence_targets
WHERE 
"drug_HOI_evidence".drug = 1539403 AND
"drug_HOI_evidence"."HOI" = 36110715 AND
"drug_HOI_evidence".evidence_type = 'product_label' AND
evidence_targets.id = "drug_HOI_evidence".evidence_target_id

