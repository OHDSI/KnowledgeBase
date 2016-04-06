 /*-------------------------------------------------------------------------*
 | Program:      Conditions and their Children                              |
 | Purpose:      This program pre-processes for every conditions what       |
 |               what descendant concepts as associated to that in the      |
 |				 OMOP Vocabulary.                                           |
 | Author(s):    Erica Voss                                                 |
 |                                                                          |
 | Version:      1.0                                                        |
 | Last revised: 09FEB16                                                  |
 *-------------------------------------------------------------------------*/

 /*ASSUMPTIONS*/
 /*
 1)  You have the right copy of the CDM Vocabulary available.
 */

\echo 'Starting Script'

SELECT DISTINCT HOI AS CONDITION_CONCEPT_ID, SNOMED_HOI AS CONDITION_CONCEPT_NAME, EVIDENCE_TYPE 
INTO #CONDITIONS
FROM DRUG_HOI_EVIDENCE e
	JOIN DRUG_HOI_RELATIONSHIP r
		ON r.ID = e.DRUG_HOI_RELATIONSHIP
ORDER BY HOI, SNOMED_HOI;

CREATE INDEX IDX_CONDITIONS_CONDITION_CONCEPT_ID ON #CONDITIONS (CONDITION_CONCEPT_ID);

SELECT DISTINCT *
INTO LU_CONDITIONS_CHILDREN /*this is slow running*/
FROM (
	SELECT CONDITION_CONCEPT_ID, CONDITION_CONCEPT_NAME, c1.CONCEPT_ID, c1.CONCEPT_NAME
	FROM #CONDITIONS c
		JOIN CONCEPT_ANCESTOR ca
			ON ca.ANCESTOR_CONCEPT_ID = c.CONDITION_CONCEPT_ID
		JOIN CONCEPT c1
			ON c1.CONCEPT_ID = ca.DESCENDANT_CONCEPT_ID
			AND c1.VOCABULARY_ID = 'SNOMED'
			AND c1.INVALID_REASON IS NULL
	UNION 
	/*This allows things go up in the Vocab*/
	SELECT c1.CONCEPT_ID AS CONDITION_CONCEPT_ID, c1.CONCEPT_NAME AS CONDITION_CONCEPT_NAME, CONDITION_CONCEPT_ID AS CONCEPT_ID, CONDITION_CONCEPT_NAME AS CONCEPT_NAME
	FROM #CONDITIONS c
		JOIN CONCEPT_ANCESTOR ca
			ON ca.DESCENDANT_CONCEPT_ID = c.CONDITION_CONCEPT_ID
		JOIN CONCEPT c1
			ON c1.CONCEPT_ID = ca.ANCESTOR_CONCEPT_ID
			AND c1.VOCABULARY_ID = 'SNOMED'
			AND c1.INVALID_REASON IS NULL
) z;

/*This has been added because it is known MeSH lands at 4340942 but that doesn't link in with other liver injury terms*/
INSERT INTO LU_CONDITIONS_CHILDREN (CONDITION_CONCEPT_ID, CONDITION_CONCEPT_NAME, CONCEPT_ID, CONCEPT_NAME) VALUES (4026032,'Acute hepatic failure',4340942,'Drug-induced hepatitis');
/*Adding this link because some of the evidence gets associated to the measurement which has no links anywhere*/
INSERT INTO LU_CONDITIONS_CHILDREN (CONDITION_CONCEPT_ID, CONDITION_CONCEPT_NAME, CONCEPT_ID, CONCEPT_NAME) VALUES (314664,'Prolonged QT interval',4008859,'Prolonged QT interval');

CREATE INDEX IDX_CONDITIONS_CHILDREN_CONDITION_CONCEPT_ID ON LU_CONDITIONS_CHILDREN (CONCEPT_ID);

---- !!!! UNCOMMENT THESE PERMISSIONS FOR RELEASE !!!! 
-- ALTER TABLE LU_CONDITIONS_CHILDREN  OWNER TO rich;
-- GRANT ALL ON TABLE LU_CONDITIONS_CHILDREN  TO public;
-- GRANT ALL ON TABLE LU_CONDITIONS_CHILDREN  TO ohdsi;
-- GRANT ALL ON TABLE LU_CONDITIONS_CHILDREN  TO administrator;
-- GRANT ALL ON TABLE LU_CONDITIONS_CHILDREN  TO developer;

---- !!!! UNCOMMENT THESE PERMISSIONS FOR DEVELOPMENT !!!! 
ALTER TABLE LU_CONDITIONS_CHILDREN  OWNER TO rdb20;

COMMIT;
