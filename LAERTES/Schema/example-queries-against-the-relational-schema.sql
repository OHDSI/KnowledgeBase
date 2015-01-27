-- EXAMPLE QUERIES AGAINST THE RELATIONAL DATABASE FOR LAERTES:

-- A general query showing how to bridge all tables
SELECT drug_hoi_relationship.drug, drug_hoi_relationship.hoi, drug_HOI_evidence.evidence_type, drug_HOI_evidence.statistic_value, drug_HOI_evidence.statistic_type, drug_HOI_evidence.evidence_linkout, evidence_sources.title, evidence_sources.description
FROM drug_hoi_relationship, drug_HOI_evidence, evidence_sources
WHERE drug_hoi_relationship.id = drug_HOI_evidence.drug_hoi_relationship AND
      drug_HOI_evidence.evidence_source_code_id = evidence_sources.id
LIMIT 10;


-- Get back all evidence for 'Lisinopril' and 'Uterine leiomyoma' using standard vocab codes
SELECT *
FROM drug_hoi_evidence_view  
WHERE 
drug = 1308216 AND
hoi = 36617553;


-- Get back all evidence for 'amoxacillin' and 'Pruritis' using
-- standard vocab codes. Returns the following linkout that can be put
-- into the browser to retrieve an OA representation of the data in
-- the product label:
-- http://dbmi-icode-01.dbmi.pitt.edu/l/index.php?id=i9b  
SELECT *
FROM drug_hoi_evidence_view  
WHERE 
drug = 19123591 AND
hoi = 37320197;

-- get the target URIs for product label evidence for Simvastatin and Upper respiratory tract infection
-- TODO: change the evidence_types to hold literature, product label, pharmacovigilance, EHR. Right now it just repeats the 'title' in the evidence_sources table
SELECT *
FROM drug_hoi_evidence_view  
WHERE 
drug = 1539403 AND
hoi = 36110715 AND
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
-- Originally from Christian Reich in reply to the forum
-- http://forums.ohdsi.org/t/laertes-pre-load-queries-hoi-from-x-to-snomed-rxnorm-bd-to-cd/180
-- Some modifications to bring in additional evidence sources
--
-- Here is the query that will do the following:

--     Stratify by ingredient only
--     Stratify by ingredient and HOI
--     Stratify by ingredient and clinical drug
--     Give the full detail (all ingredients, drugs, HOI and the numbers)

-- and create one summary report for each of them. The numbers are:

--     ct_count - clinical trial count. The details are listed for ingredients and HOIs, not for clinical drugs. The summary is provided as a total.
--     case_count - care report count. Same as above.
--     other_count - other mesh based count. Same as above.
--     splicer_count - count in splicer. The details are listed for clinical drugs and HOIs. The summary is provided as a total.
--     eb05 - ebgm confidence interval. The details are listed for ingredients and HOIs. The summary provides an average.
--     ebgm - empirical Bayes geometric mean of the EARS report. Same as above.
--     aers_report_count - absolute number of AERS reports. The summary is provided as a total.


select
  report_name,
  case 
    when lag(ingredient_id) over (partition by ingredient_id order by report_order, clinical_drug_id, hoi_id) = ingredient_id then null
    else ingredient_id
  end as ingredient_id, 
  case 
    when lag(ingredient_id) over (partition by ingredient_id order by report_order, clinical_drug_id, hoi_id) = ingredient_id then null
    else ingredient
  end as ingredient,
  case 
    when lag(clinical_drug_id) over (partition by ingredient_id, clinical_drug_id order by report_order, hoi_id) = clinical_drug_id then null
    else clinical_drug_id
  end as clinical_drug_id, 
  case 
    when lag(clinical_drug_id) over (partition by ingredient_id, clinical_drug_id order by report_order, hoi_id) = clinical_drug_id then null
    else clinical_drug
  end as clinical_drug,
  hoi_id, hoi, ct_count, case_count, other_count, splicer_count, eu_spc_count, eb05, ebgm, aers_report_count
from (
  select distinct
    1 as report_order,
    'Stratified by ingredient' as report_name,
    dv1.drug as ingredient_id, 
    dv1.rxnorm_drug as ingredient, 
    cast(null as integer) as clinical_drug_id, 
    cast(null as varchar(1)) as clinical_drug, 
    cast(null as integer) as hoi_id, 
    cast(null as varchar(1)) as hoi, 
    sum(dv1.medline_mesh_clin_trial_count) over (partition by dv1.drug) as ct_count, -- Ingredient-based
    sum(dv1.medline_mesh_case_report_count) over (partition by dv1.drug) as case_count, -- Ingredient-based
    sum(dv1.medline_mesh_other_count) over (partition by dv1.drug) as other_count, -- Ingredient-based
    sum(dv2.spl_splicer_count) over (partition by dv1.drug) as splicer_count, -- Drug-based
    sum(dv1.spl_eu_spc_count) over (partition by dv1.drug) as eu_spc_count, -- Ingredient-based
    avg(dv1.aers_eb05) over (partition by dv1.drug) as eb05, -- Ingredient-based
    avg(dv1.aers_ebgm) over (partition by dv1.drug) as ebgm, -- Ingredient-based
    sum(dv1.aers_report_count) over (partition by dv1.drug) as aers_report_count-- Ingredient-based
  from drug_hoi_evidence_view dv1, drug_hoi_evidence_view dv2, concept_ancestor ca, concept ing, concept drg
  where dv1.hoi = dv2.hoi 
  and dv1.drug = ca.ancestor_concept_id and dv1.drug=ing.concept_id and ing.concept_class_id='Ingredient'
  and dv2.drug = ca.descendant_concept_id and dv2.drug=drg.concept_id and drg.concept_class_id like '%Drug'
union
  select distinct
    2 as report_order,
    'Stratified by ingredient and HOI' as report_name,
    dv1.drug as ingredient_id, 
    dv1.rxnorm_drug as ingredient, 
    cast(null as integer) as clinical_drug_id, 
    cast(null as varchar(1)) as clinical_drug, 
    dv1.hoi as hoi_id, 
    dv1.snomed_hoi as hoi,
    sum(dv1.medline_mesh_clin_trial_count) over (partition by dv1.drug, dv1.hoi) as ct_count, -- Ingredient-based
    sum(dv1.medline_mesh_case_report_count) over (partition by dv1.drug, dv1.hoi) as case_count, -- Ingredient-based
    sum(dv1.medline_mesh_other_count) over (partition by dv1.drug, dv1.hoi) as other_count, -- Ingredient-based
    sum(dv2.spl_splicer_count) over (partition by dv1.drug, dv1.hoi) as splicer_count, -- Drug-based
    sum(dv1.spl_eu_spc_count) over (partition by dv1.drug, dv1.hoi) as eu_spc_count, -- Ingredient-based
    avg(dv1.aers_eb05) over (partition by dv1.drug, dv1.hoi) as eb05, -- Ingredient-based
    avg(dv1.aers_ebgm) over (partition by dv1.drug, dv1.hoi) as ebgm, -- Ingredient-based
    sum(dv1.aers_report_count) over (partition by dv1.drug, dv1.hoi) as aers_report_count-- Ingredient-based
  from drug_hoi_evidence_view dv1, drug_hoi_evidence_view dv2, concept_ancestor ca, concept ing, concept drg
  where dv1.hoi = dv2.hoi 
  and dv1.drug = ca.ancestor_concept_id and dv1.drug=ing.concept_id and ing.concept_class_id='Ingredient'
  and dv2.drug = ca.descendant_concept_id and dv2.drug=drg.concept_id and drg.concept_class_id like '%Drug'
union
  select distinct
    3 as report_order,
    'Stratified by ingredient and clinical drug' as report_name,
    dv1.drug as ingredient_id, 
    dv1.rxnorm_drug as ingredient, 
    dv2.drug as clinical_drug_id, 
    dv2.rxnorm_drug as clinical_drug, 
    cast(null as integer) as hoi_id, 
    cast(null as varchar(1)) as hoi, 
    sum(dv1.medline_mesh_clin_trial_count) over (partition by dv1.drug, dv2.drug) as ct_count, -- Ingredient-based
    sum(dv1.medline_mesh_case_report_count) over (partition by dv1.drug, dv2.drug) as case_count, -- Ingredient-based
    sum(dv1.medline_mesh_other_count) over (partition by dv1.drug, dv2.drug) as other_count, -- Ingredient-based
    sum(dv2.spl_splicer_count) over (partition by dv1.drug, dv2.drug) as splicer_count, -- Drug-based
    sum(dv1.spl_eu_spc_count) over (partition by dv1.drug, dv2.drug) as eu_spc_count, -- Ingredient-based
    avg(dv1.aers_eb05) over (partition by dv1.drug, dv2.drug) as eb05, -- Ingredient-based
    avg(dv1.aers_ebgm) over (partition by dv1.drug, dv2.drug) as ebgm, -- Ingredient-based
    sum(dv1.aers_report_count) over (partition by dv1.drug, dv2.drug) as aers_report_count-- Ingredient-based
  from drug_hoi_evidence_view dv1, drug_hoi_evidence_view dv2, concept_ancestor ca, concept ing, concept drg
  where dv1.hoi = dv2.hoi 
  and dv1.drug = ca.ancestor_concept_id and dv1.drug=ing.concept_id and ing.concept_class_id='Ingredient'
  and dv2.drug = ca.descendant_concept_id and dv2.drug=drg.concept_id and drg.concept_class_id like '%Drug'
union
  select
    4 as report_order,
    'Full detail: ingredient, clinical drug, HOI' as report_name,
    dv1.drug as ingredient_id, 
    dv1.rxnorm_drug as ingredient, 
    dv2.drug as clinical_drug_id, 
    dv2.rxnorm_drug as clinical_drug, 
    dv1.hoi as hoi_id, 
    dv1.snomed_hoi as hoi, 
    dv1.medline_mesh_clin_trial_count as ct_count, -- Ingredient-based
    dv1.medline_mesh_case_report_count as case_count, -- Ingredient-based
    dv1.medline_mesh_other_count as other_count, -- Ingredient-based
    dv2.spl_splicer_count as splicer_count, -- Drug-based
    dv1.spl_eu_spc_count as eu_spc_count, -- Ingredient-based
    dv1.aers_eb05 as eb05, -- Ingredient-based
    dv1.aers_ebgm as ebgm, -- Ingredient-based
    dv1.aers_report_count as aers_report_count-- Ingredient-based
  from drug_hoi_evidence_view dv1, drug_hoi_evidence_view dv2, concept_ancestor ca, concept ing, concept drg
  where dv1.hoi = dv2.hoi 
  and dv1.drug = ca.ancestor_concept_id and dv1.drug=ing.concept_id and ing.concept_class_id='Ingredient'
  and dv2.drug = ca.descendant_concept_id and dv2.drug=drg.concept_id and drg.concept_class_id like '%Drug'
) d
order by d.ingredient_id, report_order, d.clinical_drug_id, d.hoi_id
limit 1000;



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



