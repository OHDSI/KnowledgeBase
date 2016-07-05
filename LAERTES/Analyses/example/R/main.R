#  *-------------------------------------------------------------------------*/
#   SETUP
#  *-------------------------------------------------------------------------*/
library(DatabaseConnector)
library(SqlRender)

#  *-------------------------------------------------------------------------*/
#   CONNECTION DETAILS
#  *-------------------------------------------------------------------------*/
laertes = list (
  dbms = "postgresql",
  user = "YOUR_USER_NAME",
  password = "YOUR_PWD",
  server = "laertes.ohdsi.org/vocabularyv5",
  port = 5432,
  schema = "public"
)


genConnPG = function(dbms, user, password, server, port, schema){
  connectionDetails <- createConnectionDetails(dbms=dbms, user=user, password=password, server=server, port=port, schema=schema)
  conn <- connect(connectionDetails)
  return(conn)
}

#  *-------------------------------------------------------------------------*/
#   PULL LAERTES SPLS
#  *-------------------------------------------------------------------------*/

## Grabbing from PostGres but should pull from local LAERTES copy
summarizeEvidence <- function(db){
  conn <- genConnPG(dbms=laertes$dbms, user=laertes$user, password=laertes$password, server=laertes$server, port=laertes$port, schema=laertes$schema)
  sql <- readSql("sql/LAERTES_pullSPLs.sql")
  evidence <- querySql(conn=conn,sql)
  dbDisconnect(conn)
  return(evidence)
}
LAERTES_EVIDENCE <- summarizeEvidence(db)

#  *-------------------------------------------------------------------------*/
#   Post File
#  *-------------------------------------------------------------------------*/
postFile <- function(db){
  conn <- genConnPG(dbms=laertes$dbms, user=laertes$user, password=laertes$password, server=laertes$server, port=laertes$port, schema=laertes$schema)
  TEST_EXAMPLE <- read.csv("files/TEST_EXAMPLE.txt",header=TRUE, sep="\t")
  sql <-paste("DROP TABLE IF EXISTS TEST_EXAMPLE;",sep='')
  executeSql(conn,sql)
  insertTable(conn,"TEST_EXAMPLE",TEST_EXAMPLE)
  results <- querySql(conn, "SELECT * FROM TEST_EXAMPLE")
  sql <-paste("DROP TABLE IF EXISTS TEST_EXAMPLE;",sep='')
  executeSql(conn,sql)
  dbDisconnect(conn)
  return(results)
}
result <- postFile(db)
View(result)
