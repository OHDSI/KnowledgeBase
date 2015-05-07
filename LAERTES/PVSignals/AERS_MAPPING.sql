/********
AUTHOR:  ERICA VOSS
DATE:  06-MAY-2015
********/

USE UMLS;

WITH CTE_SNOMED_CUI_LU AS (
	SELECT CUI, MAX(CODE) AS CODE
	FROM MRCONSO m
	WHERE SAB = 'SNOMEDCT_US'
	AND TTY = 'PT'
	AND LAT = 'ENG'
	GROUP BY CUI
),
CTE_CUI_SNOMED_LU AS (
	SELECT l.*, c.concept_id AS CONDITION_CONCEPT_ID, c.CONCEPT_NAME AS CONDITION_CONCEPT_NAME
	FROM CTE_SNOMED_CUI_LU l
		JOIN [OMOP_Vocabulary_v5.0_20150403].dbo.CONCEPT c
			ON c.CONCEPT_CODE = l.CODE
			AND c.INVALID_REASON IS NULL
			AND c.VOCABULARY_ID = 'SNOMED'
),
CTE_TRIM_CUI_MEDDRA AS (
	SELECT CUI, MAX(MEDDRA) AS MEDDRA
	FROM scratch.dbo.CUI_MEDDRA_LU
	GROUP BY CUI
),
CTE_CUI_MEDDRA_LU AS (
	SELECT *
	FROM (
		SELECT l.CUI, l.MEDDRA, c.*,
			c.concept_id AS MEDDRA_CONCEPT_ID, c.concept_name AS MEDDRA_CONCEPT_NAME, 
			c2.concept_id AS SNOMED_CONCEPT_ID, c2.concept_name AS SNOMED_CONCEPT_NAME, 
			ROW_NUMBER() OVER(PARTITION BY l.CUI, l.MEDDRA ORDER BY l.CUI, l.MEDDRA, ca.min_levels_of_separation, ca.max_levels_of_separation, c.CONCEPT_ID, c2.CONCEPT_ID) AS ROW_NUM
		FROM CTE_TRIM_CUI_MEDDRA l
			JOIN [OMOP_Vocabulary_v5.0_20150403].dbo.CONCEPT c
				ON c.CONCEPT_CODE = l.MEDDRA
				AND DOMAIN_ID = 'Condition'
				AND c.concept_class_id = 'PT'
			JOIN [OMOP_Vocabulary_v5.0_20150403].dbo.concept_ancestor ca
				ON ca.ancestor_concept_id = c.concept_id
			JOIN [OMOP_Vocabulary_v5.0_20150403].dbo.CONCEPT c2
				ON c2.concept_id = ca.descendant_concept_id
				AND c2.vocabulary_id = 'SNOMED'
				AND c2.CONCEPT_CLASS_ID = 'Clinical Finding'
				AND c2.INVALID_REASON IS NULL
	) z
	WHERE z.ROW_NUM = 1
),
CTE_ICD9_CUI_LU AS (
	SELECT CUI, MAX(CODE) AS CODE
	FROM MRCONSO m
	WHERE SAB = 'ICD9CM'
	AND TTY IN ( 'PT', 'HT' )
	AND LAT = 'ENG'
	GROUP BY CUI
),
CTE_CUI_ICD9_LU AS (
	SELECT l.*, c.concept_id AS CONDITION_CONCEPT_ID, c.CONCEPT_NAME AS CONDITION_CONCEPT_NAME
	FROM CTE_ICD9_CUI_LU l
		JOIN [OMOP_Vocabulary_v5.0_20150403].dbo.CONCEPT c
			ON c.CONCEPT_CODE = l.CODE
			AND c.INVALID_REASON IS NULL
			AND c.VOCABULARY_ID = 'ICD9CM'
),
CTE_ICD9_SNOMED_PREP AS (
	SELECT c.CONCEPT_ID AS ICD9_CONCEPT_ID, c.concept_name AS ICD9_CONCEPT_NAME, c2.concept_id AS SNOMED_CONCEPT_ID, c2.concept_name AS SNOMED_CONCEPT_NAME
	FROM [OMOP_Vocabulary_v5.0_20150403].dbo.CONCEPT c
		JOIN [OMOP_Vocabulary_v5.0_20150403].dbo.CONCEPT_RELATIONSHIP cr
			ON cr.CONCEPT_ID_1 = c.CONCEPT_ID
			AND cr.INVALID_REASON IS NULL
		JOIN [OMOP_Vocabulary_v5.0_20150403].dbo.CONCEPT c2
			ON c2.CONCEPT_ID = cr.CONCEPT_ID_2
			AND c2.INVALID_REASON IS NULL
			AND c2.VOCABULARY_ID = 'SNOMED'
	WHERE c.vocabulary_id = 'ICD9CM'
	AND c.invalid_reason IS NULL
),
CTE_ICD9_MULTI AS (
	SELECT ICD9_CONCEPT_ID, COUNT(*) AS MESH_COUNT
	FROM CTE_ICD9_SNOMED_PREP
	GROUP BY ICD9_CONCEPT_ID
	HAVING COUNT(*) > 1
),
CTE_ICD9_SNOMED_LU AS (
	SELECT t.*
	FROM CTE_ICD9_SNOMED_PREP t
		LEFT OUTER JOIN CTE_ICD9_MULTI m
			ON m.ICD9_CONCEPT_ID = t.ICD9_CONCEPT_ID
	WHERE m.ICD9_CONCEPT_ID IS NULL
),
CTE_DRUGS AS (
	SELECT DISTINCT c.CONCEPT_CODE AS ATC_CONCEPT, c2.CONCEPT_ID AS INGREDIENT_CONCEPT_ID, c2.CONCEPT_NAME AS INGREDIENT_CONCEPT_NAME
	FROM [OMOP_Vocabulary_v5.0_20150403].dbo.CONCEPT c
		JOIN [OMOP_Vocabulary_v5.0_20150403].dbo.CONCEPT_RELATIONSHIP cr
			ON cr.CONCEPT_ID_1 = c.CONCEPT_ID
			AND cr.INVALID_REASON IS NULL
		JOIN [OMOP_Vocabulary_v5.0_20150403].dbo.CONCEPT c2
			ON c2.CONCEPT_ID = cr.CONCEPT_ID_2
			AND c2.INVALID_REASON IS NULL
			AND c2.VOCABULARY_ID = 'RxNorm'
			AND c2.CONCEPT_CLASS_ID = 'Ingredient'
	WHERE c.vocabulary_id = 'ATC'
	AND c.invalid_reason IS NULL
), 
CTE_MAP AS (
	SELECT a.*, 
		CASE 
			WHEN l.CONDITION_CONCEPT_ID IS NOT NULL THEN l.CONDITION_CONCEPT_ID
			WHEN l.CONDITION_CONCEPT_ID IS NULL		THEN ml.SNOMED_CONCEPT_ID 
			--WHEN ml.SNOMED_CONCEPT_ID  IS NULL		THEN s.SNOMED_CONCEPT_ID
			ELSE l.CONDITION_CONCEPT_ID 
		END	AS CONDITION_CONCEPT_ID, 
		CASE 
			WHEN l.CONDITION_CONCEPT_NAME IS NOT NULL	THEN l.CONDITION_CONCEPT_NAME
			WHEN l.CONDITION_CONCEPT_NAME IS NULL		THEN ml.SNOMED_CONCEPT_NAME 
			--WHEN l.CONDITION_CONCEPT_NAME IS NULL		THEN s.SNOMED_CONCEPT_NAME
			ELSE l.CONDITION_CONCEPT_NAME 
		END	AS CONDITION_CONCEPT_NAME,
		CASE 
			WHEN l.CONDITION_CONCEPT_NAME IS NOT NULL	THEN 'CUI to SNOMED'
			WHEN l.CONDITION_CONCEPT_NAME IS NULL		THEN 'CUI to MEDDRA'
			--WHEN l.CONDITION_CONCEPT_NAME IS NULL		THEN 'CUI to ICD'
			ELSE l.CONDITION_CONCEPT_NAME 
		END	AS MAPPING_TYPE,
		d.INGREDIENT_CONCEPT_ID, d.INGREDIENT_CONCEPT_NAME
	FROM [Scratch].[dbo].[EV311_AERS] a
		LEFT OUTER JOIN CTE_CUI_SNOMED_LU l
			ON a.umls_id = l.CUI
		LEFT OUTER JOIN CTE_DRUGS d
			ON d.ATC_CONCEPT = a.source_id
		--LEFT OUTER JOIN CTE_ICD9_CUI_LU mc
		--	ON mc.CUI = a.UMLS_ID
		--LEFT OUTER JOIN CTE_CUI_ICD9_LU i
		--	ON i.CUI = a.umls_id
		--LEFT OUTER JOIN CTE_ICD9_SNOMED_LU s
		--	ON s.ICD9_CONCEPT_ID = i.CONDITION_CONCEPT_ID
		LEFT OUTER JOIN CTE_CUI_MEDDRA_LU ml
			ON ml.CUI = a.umls_id
), 
CTE_FULL_MAP AS (
SELECT DISTINCT m.stitch_id, m.umls_id, m.pvalue, m.drug_mean, m.drug_sd, m.bg_mean, m.bg_sd, m.drug_num,
	m.bg_num, m.t_statistic, m.df, m.drug_cutoff, m.ind_cutoff, m.prr, m.t_denorm_gtr0, m.t_dnorm_gtr0, m.e_score_de, 
	m.chisq, m.chisq_pvalue, m.rr, m.chemical, c.AERS_COUNTS, m.CONDITION_CONCEPT_ID, m.CONDITION_CONCEPT_NAME, 
	m.INGREDIENT_CONCEPT_ID, m.INGREDIENT_CONCEPT_NAME, m.MAPPING_TYPE
FROM CTE_MAP m
	LEFT OUTER JOIN [Scratch].[dbo].EV311_AERS_COUNTS c
		ON c.STITCH_ID = m.stitch_id
		AND c.UMLS_ID = m.umls_id 
)
SELECT *
FROM CTE_FULL_MAP fm
ORDER BY umls_id, stitch_id
