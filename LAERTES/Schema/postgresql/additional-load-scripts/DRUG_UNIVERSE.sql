 /*-------------------------------------------------------------------------*
 | Program:      DRUG UNIVERSE					            |
 | Purpose:      This program pre-processes ingredients that contain        | 
 |		 enough evidence to be part of the LAERTES UNIVERSE         |
 | Author(s):    Erica Voss                                                 |
 |                                                                          |
 | Version:      2.0                                                        |
 | Last revised: April 4, 2016                                              |
 *-------------------------------------------------------------------------*/

  /*ASSUMPTIONS*/
 /*
 1)  You have the right copy of the CDM Vocabulary available.
 */

-- NOTE: For now, CTD evidence is counted as MEDLINE when it also includes OMIM

\echo 'Starting Script'

/*Get drugs down to ingredients*/
/*-----------------------------*/
\echo 'Mapping Ingredients'

SELECT r.HOI AS CONDITION_CONCEPT_ID, r.SNOMED_HOI AS CONDITION_CONCEPT_NAME,
	r.DRUG AS DRUG_CONCEPT_ID, r.RXNORM_DRUG AS DRUG_CONCEPT_NAME,  
	c.CONCEPT_ID AS INGREDIENT_ID, c.CONCEPT_NAME AS INGREDIENT_NAME,
	CASE WHEN c.CONCEPT_ID IS NULL THEN 0 ELSE 1 END INGREDIENT_EXISTS, 
	c2.CONCEPT_ID AS CLINICAL_DRUG_ID,c2.CONCEPT_NAME AS CLINICAL_DRUG_NAME,
	CASE WHEN c2.CONCEPT_ID IS NULL THEN 0 ELSE 1 END CLINICAL_DRUG_EXISTS, 
	e.EVIDENCE_TYPE, e.SUPPORTS, e.EVIDENCE_SOURCE_CODE_ID, e.STATISTIC_VALUE, e.EVIDENCE_LINKOUT, e.STATISTIC_TYPE
INTO TEMP TABLE TEMP_INGREDIENTS
FROM DRUG_HOI_EVIDENCE e
	JOIN DRUG_HOI_RELATIONSHIP r
		ON r.ID = e.DRUG_HOI_RELATIONSHIP
	/*ROLL DOWN TO INGREDIENTS*/
	LEFT OUTER JOIN CONCEPT_ANCESTOR ca
		ON ca.DESCENDANT_CONCEPT_ID = r.DRUG
		AND ca.ANCESTOR_CONCEPT_ID IN (
			SELECT DISTINCT CONCEPT_ID
			FROM CONCEPT
			WHERE VOCABULARY_ID = 'RxNorm'
			AND CONCEPT_CLASS_ID = 'Ingredient'
			AND INVALID_REASON IS NULL
		)
	LEFT OUTER JOIN CONCEPT c
		ON c.CONCEPT_ID = ca.ANCESTOR_CONCEPT_ID
	/*ROLL UP TO CLINICAL DRUG*/
	LEFT OUTER JOIN CONCEPT_ANCESTOR ca2
		ON ca2.DESCENDANT_CONCEPT_ID = r.DRUG
		AND ca2.ANCESTOR_CONCEPT_ID IN (
			SELECT DISTINCT CONCEPT_ID
			FROM CONCEPT
			WHERE VOCABULARY_ID = 'RxNorm'
			AND CONCEPT_CLASS_ID = 'Clinical Drug'
			AND INVALID_REASON IS NULL
		)
	LEFT OUTER JOIN CONCEPT c2
		ON c2.CONCEPT_ID = ca2.ANCESTOR_CONCEPT_ID;

CREATE INDEX IDX_INGREDIENTS_INGREDIENT_ID ON TEMP_INGREDIENTS (INGREDIENT_ID);
CREATE INDEX IDX_INGREDIENTS_HOI ON TEMP_INGREDIENTS (CONDITION_CONCEPT_ID);

/*For NULL safety, cut out records without an ingredient available*/
/*-----------------------------*/
\echo 'Trimming Records'

SELECT DISTINCT INGREDIENT_ID, INGREDIENT_NAME, EVIDENCE_TYPE
INTO TEMP TABLE TEMP_DRUGS
FROM TEMP_INGREDIENTS
WHERE INGREDIENT_EXISTS = 1
ORDER BY INGREDIENT_ID, INGREDIENT_NAME;

/*Define drug universe has an ingredient that has records in spontaneous reprots, medline, and a product label*/
/*-----------------------------*/
\echo 'Drop old table'

DROP TABLE IF EXISTS DRUG_UNIVERSE;

\echo 'Create table'

CREATE TABLE DRUG_UNIVERSE (
  INGREDIENT_CONCEPT_ID   integer,
  INGREDIENT_CONCEPT_NAME character varying(255)
);


\echo 'Generate Universe'

INSERT INTO DRUG_UNIVERSE (INGREDIENT_CONCEPT_ID, INGREDIENT_CONCEPT_NAME)
SELECT DISTINCT INGREDIENT_ID, INGREDIENT_NAME
FROM TEMP_DRUGS
WHERE INGREDIENT_ID IN (
	SELECT DISTINCT INGREDIENT_ID
	FROM TEMP_DRUGS
	WHERE EVIDENCE_TYPE IN (
		'aers_report_prr','aers_report_count'
	)
)
AND INGREDIENT_ID IN (
	SELECT DISTINCT INGREDIENT_ID
	FROM TEMP_DRUGS
	WHERE EVIDENCE_TYPE IN (
		'MEDLINE_MeSH_ClinTrial','MEDLINE_MeSH_CR','MEDLINE_MeSH_Other','MEDLINE_SemMedDB_ClinTrial','MEDLINE_SemMedDB_CR','MEDLINE_SemMedDB_Other'
	)
)
AND INGREDIENT_ID IN (
	SELECT DISTINCT INGREDIENT_ID
	FROM TEMP_DRUGS
	WHERE EVIDENCE_TYPE IN (
		'SPL_EU_SPC','SPL_SPLICER_ADR'
	)
);
/*Currently not including CTD_ChemicalDisease in evidence requirement*/

CREATE INDEX IDX_DRUG_UNIVERSE_INGREDIENT_ID ON DRUG_UNIVERSE (INGREDIENT_CONCEPT_ID);
ALTER TABLE DRUG_UNIVERSE CLUSTER ON IDX_DRUG_UNIVERSE_INGREDIENT_ID;

\echo 'Alter statements'

---- !!!! UNCOMMENT THESE PERMISSIONS FOR RELEASE !!!! 
-- ALTER TABLE DRUG_UNIVERSE  OWNER TO rich;
-- GRANT ALL ON TABLE DRUG_UNIVERSE  TO public;
-- GRANT ALL ON TABLE DRUG_UNIVERSE  TO ohdsi;
-- GRANT ALL ON TABLE DRUG_UNIVERSE  TO administrator;
-- GRANT ALL ON TABLE DRUG_UNIVERSE  TO developer;

---- !!!! UNCOMMENT THESE PERMISSIONS FOR DEVELOPMENT !!!! 
ALTER TABLE DRUG_UNIVERSE  OWNER TO rdb20;

COMMIT;
