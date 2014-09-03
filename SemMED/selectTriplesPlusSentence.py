"""
selectTriplesPlusSentence.py

Jeremy Jao and Rich Boyce
09.2.2014

Selects concept triples with the sentences from which they were derived.
TODO: filter this down to triples with:
- subject being a pharm entity semantic type 
- object being a Pathologic Function, Sign or Symptom, Disease or Syndrome, Finding
- predicate CAUSES, ASSOCIATED_WITH, COMPLICATES, DISRUPTS, PREDISPOSES - and the negated versions of these

"""

import mysql.connector as sql
import connectSEMMED as db
import pprint

cnx = sql.connect(**db.details())
cursor = cnx.cursor()

with open('allpredicates.txt', 'w') as fil:

	#query = """
#SELECT CONCEPT1, PREDICATE, CONCEPT2, SENTENCE_ID, PMID, TYPE, NUMBER, SENTENCE
#FROM 
#...TODO: 
#Q1) all rows from PREDICATION_ARGUMENT with a given predication id
#Q2) SENTENCE_PREDICATION will give the sentence id that can be used for the table.

#you probably do not want to inner join from predication to PREDICATION_ARGUMENT....

#CONCEPT_SEMTYPE_ID

#"""
	query = """
			
			SELECT * 
			FROM PREDICATION_AGGREGATE inner join sentence 
			WHERE
			()
			
			
			LIMIT 100;
			
			"""

	cursor.execute(query)

	for predicate in cursor:
		pprint.pprint(predicate, fil)

cursor.close()
cnx.close()
