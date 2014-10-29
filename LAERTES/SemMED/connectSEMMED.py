"""
Jeremy Jao
07.15.2014

This is the function that will give me a connection to SemMEDDB
This uses the Oracle-MySQL dev library:
http://dev.mysql.com/doc/connector-python/en/index.html

Interesting huh....

Usage (in another program...):

	import mysql.connector
	import connectSEMMED
	
	cn = mysql.connector.connect(**connectSEMMED.details())
	cn.close()

"""

def details():
	connection = {
		'user':'rich',
		'password':'Rich@123',
		'host':'54.210.37.230',
		'database':'semmed',
		'raise_on_warnings':True,
		'port':3306
	}
	return connection
