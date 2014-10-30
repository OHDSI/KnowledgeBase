-- EXAMPLE QUERIES AGAINST THE RELATIONAL DATABASE FOR LAERTES:

-- A general query showing how to bridge all tables
SELECT drug_hoi_relationship.drug, drug_hoi_relationship.hoi, drug_HOI_evidence.evidence_type, drug_HOI_evidence.statistic_value, drug_HOI_evidence.statistic_type, drug_HOI_evidence.evidence_linkout, evidence_sources.title, evidence_sources.description
FROM drug_hoi_relationship, drug_HOI_evidence, evidence_sources
WHERE drug_hoi_relationship.id = drug_HOI_evidence.drug_hoi_relationship AND
      drug_HOI_evidence.evidence_source_code_id = evidence_sources.id
LIMIT 10;


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

-- get the target URIs for product label evidence for Simvastatin and Upper respiratory tract infection
-- TODO: change the evidence_types to hold literature, product label, pharmacovigilance, EHR. Right now it just repeats the 'title' in the evidence_sources table
SELECT evidence_targets.uri
FROM drug_HOI_evidence, evidence_targets
WHERE 
drug_HOI_evidence.drug = 1539403 AND
drug_HOI_evidence.HOI = 36110715 AND
drug_HOI_evidence.evidence_type in ('SPL_SPLICER','SPL_EU_SPC') AND
evidence_targets.id = drug_HOI_evidence.evidence_target_id

-- locate some drug-HOI pairs that have evidence from both product labeling sources using the main drug_HOI_evidence table
SELECT *
FROM drug_HOI_evidence A INNER JOIN drug_HOI_evidence B ON A.drug_hoi_relationship = B.drug_hoi_relationship
WHERE A.evidence_type = 'SPL_EU_SPC' AND
      B.evidence_type = 'SPL_SPLICER'
LIMIT 10

-- locate some drug-HOI pairs that have evidence from both product labeling sources using the pivot table (i.e., the view drug_hoi_evidences)
SELECT id, drug, rxnorm_drug, hoi, meddra_hoi, aers_eb05, aers_ebgm, 
       aers_report_count, spl_eu_spc_count, spl_splicer_count, aers_eb05_link, 
       aers_ebgm_link, aers_report_link, spl_eu_spc_link, spl_splicer_link
FROM drug_hoi_evidences
WHERE   (spl_splicer_link IS NOT NULL) AND 	
	(spl_eu_spc_link IS NOT NULL)

-- dump the count data from SPLICER, EU SPC, and FAERS from the pivot table 
SELECT id, drug, rxnorm_drug, hoi, meddra_hoi, aers_eb05, aers_ebgm, 
       aers_report_count, spl_eu_spc_count, spl_splicer_count, aers_eb05_link, 
       aers_ebgm_link, aers_report_link, spl_eu_spc_link, spl_splicer_link
FROM drug_hoi_evidences
WHERE   (spl_splicer_link IS NOT NULL) OR 	
	(spl_eu_spc_link IS NOT NULL) OR
	(aers_report_link IS NOT NULL);

------------------------------------------------------------ 
-- Queries below this line need to get ported but first the
-- Evidence_sources table needs to be revised to tag each evidence
-- source with a type such as literature, labeling,
-- pharmacovigilance_signal_spontaneous_reporting,
-- pharmacovigilance_signal_EHR
------------------------------------------------------------


---- TODO: port after PubMed and SemMedDB are loaded
-- Count literature evidence for 'metronidazole' and 'renal failure'
-- SELECT COUNT("drug_HOI_evidence".evidence_type)
-- FROM "drug_HOI_evidence"
-- WHERE 
-- drug = 1707164 AND
-- "HOI" = 37019318 AND
-- evidence_type LIKE 'literature%'


-- Count case report evidence for 'metronidazole' and 'renal failure'
---- TODO: port after PubMed and SemMedDB are loaded
-- SELECT COUNT(evidence_type)
-- FROM "drug_HOI_evidence"
-- WHERE 
-- drug = 1707164 AND
-- "HOI" = 37019318 AND 
-- evidence_type = 'literature_case_report'



