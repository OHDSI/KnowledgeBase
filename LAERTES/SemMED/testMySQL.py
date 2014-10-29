import mysql.connector as sql
import connectSEMMED as db

c = sql.connect(**db.details())
#c = sql.connect(**connection)

c.close()
