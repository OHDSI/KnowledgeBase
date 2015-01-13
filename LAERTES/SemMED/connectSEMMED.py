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
DB_CONNECTION_INFO="db-connection-SemMedDB.conf"
## Set up the db connection
f = open(DB_CONNECTION_INFO,'r')
(db,user,pword,host,port) = f.readline().strip().split("\t")
f.close()


def details():
	connection = {
		'user':user,
		'password':pword,
		'host':host,
		'database':db,
		'raise_on_warnings':True,
		'port':port
	}
	return connection
