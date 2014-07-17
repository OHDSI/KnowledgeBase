"""
Jeremy Jao
07.16.2014

Selects all predicates prints them out in bash
"""

import mysql.connector as sql
import connectSEMMED as db

cnx = sql.connect(**db.details())
cursor = cnx.cursor()

with open('allpredicates.txt', 'w') as fil:
	#fil.write('id,predicate,type' + '\n')
	
	
	
	query = ("SELECT Count(*) FROM PREDICATION")
	cursor.execute(query)
	
	for (count) in cursor:
		fil.write(str(count[0]) + ' entries' + '\n')

	query = ("SELECT DISTINCT predicate FROM PREDICATION")

	cursor.execute(query)

	for predicate in cursor:
		fil.write(predicate[0] + '\n')

cursor.close()
cnx.close()
