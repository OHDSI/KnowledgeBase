 /*-------------------------------------------------------------------------*
 | Program:      CONDITION UNIVERSE				            |
 | Purpose:      This program pre-processes ingredients that contain        | 
 |               enough evidence to be part of the LAERTES UNIVERSE         |
 | Author(s):    Erica Voss                                                 |
 |                                                                          |
 | Version:      2.0                                                        |
 | Last revised: 4/4/2016                                                  |
 *-------------------------------------------------------------------------*/

  /*ASSUMPTIONS*/
 /*
 1)  You have the right copy of the CDM Vocabulary available.
 */

-- NOTE: For now, CTD evidence is counted as MEDLINE when it also includes OMIM

 \echo 'Starting Script'


 /*Get evidence table conditions*/
/*-----------------------------*/
\echo 'Find Conditions & Supports'

SELECT DISTINCT HOI AS CONDITION_CONCEPT_ID, SNOMED_HOI AS CONDITION_CONCEPT_NAME, EVIDENCE_TYPE, SUPPORTS 
INTO TEMP TABLE TEMP_CONDITIONS_SUPPORTS
FROM DRUG_HOI_EVIDENCE e
	JOIN DRUG_HOI_RELATIONSHIP r
		ON r.ID = e.DRUG_HOI_RELATIONSHIP
ORDER BY HOI, SNOMED_HOI;

\echo 'Find Conditions'

SELECT DISTINCT HOI AS CONDITION_CONCEPT_ID, SNOMED_HOI AS CONDITION_CONCEPT_NAME, EVIDENCE_TYPE 
INTO TEMP TABLE TEMP_CONDITIONS
FROM DRUG_HOI_EVIDENCE e
	JOIN DRUG_HOI_RELATIONSHIP r
		ON r.ID = e.DRUG_HOI_RELATIONSHIP
ORDER BY HOI, SNOMED_HOI;

CREATE INDEX IDX_CONDITIONS_CONDITION_CONCEPT_ID ON TEMP_CONDITIONS (CONDITION_CONCEPT_ID);

/*for every concept, gets children in the Vocabulary, use this as a lookup*/
/*-----------------------------*/

\echo 'Generate Children Lookup'

SELECT DISTINCT *
INTO TEMP TABLE TEMP_CONDITIONS_CHILDREN /*this is slow running*/
FROM (
	SELECT CONDITION_CONCEPT_ID, CONDITION_CONCEPT_NAME, c1.CONCEPT_ID, c1.CONCEPT_NAME
	FROM TEMP_CONDITIONS c
		JOIN CONCEPT_ANCESTOR ca
			ON ca.ANCESTOR_CONCEPT_ID = c.CONDITION_CONCEPT_ID
		JOIN CONCEPT c1
			ON c1.CONCEPT_ID = ca.DESCENDANT_CONCEPT_ID
			AND c1.VOCABULARY_ID = 'SNOMED'
			AND c1.INVALID_REASON IS NULL
	UNION 
	/*This allows things go up in the Vocab*/
	SELECT c1.CONCEPT_ID AS CONDITION_CONCEPT_ID, c1.CONCEPT_NAME AS CONDITION_CONCEPT_NAME, CONDITION_CONCEPT_ID AS CONCEPT_ID, CONDITION_CONCEPT_NAME AS CONCEPT_NAME
	FROM TEMP_CONDITIONS c
		JOIN CONCEPT_ANCESTOR ca
			ON ca.DESCENDANT_CONCEPT_ID = c.CONDITION_CONCEPT_ID
		JOIN CONCEPT c1
			ON c1.CONCEPT_ID = ca.ANCESTOR_CONCEPT_ID
			AND c1.VOCABULARY_ID = 'SNOMED'
			AND c1.INVALID_REASON IS NULL
) z;

/*This has been added because it is known MeSH lands at 4340942 but that doesn't link in with other liver injury terms*/
INSERT INTO TEMP_CONDITIONS_CHILDREN (CONDITION_CONCEPT_ID, CONDITION_CONCEPT_NAME, CONCEPT_ID, CONCEPT_NAME) VALUES (4026032,'Acute hepatic failure',4340942,'Drug-induced hepatitis');
/*Adding this link because some of the evidence gets associated to the measurement which has no links to the QT prolongation condition*/
INSERT INTO TEMP_CONDITIONS_CHILDREN (CONDITION_CONCEPT_ID, CONDITION_CONCEPT_NAME, CONCEPT_ID, CONCEPT_NAME) VALUES (314664,'Prolonged QT interval',4008859,'Prolonged QT interval');

CREATE INDEX IDX_CONDITIONS_CHILDREN_CONDITION_CONCEPT_ID ON TEMP_CONDITIONS_CHILDREN (CONCEPT_ID);
ALTER TABLE TEMP_CONDITIONS_CHILDREN CLUSTER ON IDX_CONDITIONS_CHILDREN_CONDITION_CONCEPT_ID;

/*Define condition universe has an ingredient that has records in spontaneous reports, medline, and a product label*/
/*-----------------------------*/
--DROP TABLE IF EXISTS EV_CONDITION_UNIVERSE;

\echo 'Drop old table'

DROP TABLE IF EXISTS CONDITION_UNIVERSE;

\echo 'Create table'

CREATE TABLE CONDITION_UNIVERSE (
  CONDITION_CONCEPT_ID   integer,
  CONDITION_CONCEPT_NAME character varying(255)
);

\echo 'Generate Universe'

WITH CTE_TEST_EVIDENCE AS (
	SELECT DISTINCT c.CONDITION_CONCEPT_ID, c.CONDITION_CONCEPT_NAME, 
		MAX(CASE WHEN c1.CONDITION_CONCEPT_ID IS NULL THEN 0 ELSE 1 END) AS AERS_EVIDENCE, 
		MAX(CASE WHEN c2.CONDITION_CONCEPT_ID IS NULL THEN 0 ELSE 1 END) AS MEDLINE_EVIDENCE,
		MAX(CASE WHEN c3.CONDITION_CONCEPT_ID IS NULL THEN 0 ELSE 1 END) AS PL_EVIDENCE
	FROM TEMP_CONDITIONS_CHILDREN c
		LEFT OUTER JOIN EV_CONDITIONS c1
			ON c1.CONDITION_CONCEPT_ID = c.CONCEPT_ID
			AND c1.EVIDENCE_TYPE IN (
				'aers_report_prr','aers_report_count'
			)
		LEFT OUTER JOIN TEMP_CONDITIONS c2
			ON c2.CONDITION_CONCEPT_ID = c.CONCEPT_ID
			AND c2.EVIDENCE_TYPE IN (
				'MEDLINE_MeSH_ClinTrial','MEDLINE_MeSH_CR','MEDLINE_MeSH_Other','MEDLINE_SemMedDB_ClinTrial','MEDLINE_SemMedDB_CR','MEDLINE_SemMedDB_Other'
			)
		LEFT OUTER JOIN TEMP_CONDITIONS c3
			ON c3.CONDITION_CONCEPT_ID = c.CONCEPT_ID
			AND c3.EVIDENCE_TYPE IN (
				'SPL_EU_SPC','SPL_SPLICER_ADR'
			)
	GROUP BY c.CONDITION_CONCEPT_ID, c.CONDITION_CONCEPT_NAME
)
INSERT INTO CONDITION_UNIVERSE (CONDITION_CONCEPT_ID, CONDITION_CONCEPT_NAME)
SELECT DISTINCT CONDITION_CONCEPT_ID, CONDITION_CONCEPT_NAME
FROM CTE_TEST_EVIDENCE
WHERE AERS_EVIDENCE = 1
AND MEDLINE_EVIDENCE = 1
AND PL_EVIDENCE = 1
ORDER BY CONDITION_CONCEPT_ID;
/*Currently does not include 'CTD_ChemicalDisease', will include at a later time*/

CREATE INDEX IDX_CONDITION_UNIVERSE_CONDITION_CONCEPT_ID ON CONDITION_UNIVERSE (CONDITION_CONCEPT_ID);
ALTER TABLE CONDITION_UNIVERSE CLUSTER ON IDX_CONDITION_UNIVERSE_CONDITION_CONCEPT_ID;

\echo 'Alter statements'

---- !!!! UNCOMMENT THESE PERMISSIONS FOR RELEASE !!!! 
-- ALTER TABLE CONDITION_UNIVERSE  OWNER TO rich;
-- GRANT ALL ON TABLE CONDITION_UNIVERSE TO public;
-- GRANT ALL ON TABLE CONDITION_UNIVERSE  TO ohdsi;
-- GRANT ALL ON TABLE CONDITION_UNIVERSE  TO administrator;
-- GRANT ALL ON TABLE CONDITION_UNIVERSE  TO developer;

---- !!!! UNCOMMENT THESE PERMISSIONS FOR DEVELOPMENT !!!! 
ALTER TABLE adr_annotation
  OWNER TO rdb20;

