
#filter a set of NCTs to parse in part 2


rm(ct.full2)

ct.full2 <- read.csv('c:/w/w/d/ohdsi/search_result-all-05-29-2014/ctg-all-2014-05-29.csv',as.is=T)
ct <- ct.full2
ct$'Start.Date2' <- as.Date(paste('1-',ct$Start.Date,sep=''),'%d-%b %y')
table(ct$Start.Date2)
ct$'Last.Verified2' <- as.Date(paste('1-',ct$Last.Verified,sep=''),'%d-%b %y')
ct$'Completion.Date2' <- as.Date(paste('1-',ct$Completion.Date,sep=''),'%d-%b %y')
ct$'Primary.Completion.Date2' <- as.Date(paste('1-',ct$Primary.Completion.Date,sep=''),'%d-%b %y')
ct$'First.Received2' <- as.Date(as.Date(ct$First.Received,'%d %b %y'))


ctfinal <-  subset(ct,Study.Results=='Has Results')
#12685
ctfinal <-  subset(ctfinal,Study.Types=='Interventional')
#11886
table(ct$Interventions)

#ctfinal <-  subset(ctfinal,substr(Interventions,1,5) %in% c("Drug:", "Biolo"))
ctfinal <-  subset(ctfinal,substr(Interventions,1,5) %in% c("Drug:"))
nrow(ctfinal)

#8837

table(ctfinal$Interventions)
table(ctfinal$Phases)
#rm(cttemp)
ctfinal <-  subset(ctfinal,Phases %in% c("Phase 4","Phase 3"))
#5416
ctfinal <-  subset(ctfinal,Enrollment>99)
#3816



nrow(ctfinal)
ctfinal$searchURL <- sprintf('http://www.clinicaltrials.gov/ct2/show/%s?resultsxml=true',as.character(ctfinal$NCT.Number))
#View(ctsubset)
str(ctfinal)







#--extra code






#skip----------------------
str(ct.full2)
#correctly has 21473 trials
tail(ct.full2$NCT.Number)


#parse the dates into nice format
ct <- ct.full2
ct$Start.Date[2]
ct$Start.Date2[2]
str(ct)

ct$First.Received[2]
ct$Start.Date2[2]
ct$First.Received2[2]


#date must have day in it, otherwise the function is confused
# this does not work      as.Date(ct$Start.Date[1:10],'%B %Y')  generates NA
#ct$Start.Date[1:10]
#add day as always 1 and ad it to the detection
#as.Date(paste('1-',ct$Start.Date[1:10],sep=''),'%d-%b-%y')


as.matrix(table(as.Date(paste('1-',ct$Start.Date,sep=''),'%d-%b-%y')))
#no NA, good !


#fix the date in the dataframe DID NOT WORK

ct$'Start.Date2' <- as.Date(paste('1-',ct$Start.Date,sep=''),'%d-%b %y')
table(ct$Start.Date2)
ct$'Last.Verified2' <- as.Date(paste('1-',ct$Last.Verified,sep=''),'%d-%b %y')
ct$'Completion.Date2' <- as.Date(paste('1-',ct$Completion.Date,sep=''),'%d-%b %y')
ct$'Primary.Completion.Date2' <- as.Date(paste('1-',ct$Primary.Completion.Date,sep=''),'%d-%b %y')
ct$'First.Received2' <- as.Date(as.Date(ct$First.Received,'%d %b %y'))


#table(as.Date(ct$First.Received,'%d-%b-%y'))
#no NA in first received, good !
str(ct)

#DO NOT DO THAT ! takes for ever !!!
#vvsave3(ct,'0102-ct-dates-cleaned')

#all data from ct.gov are in R, dates are beautified


#restrict trials by completion date being present
nrow(ct)
nrow(subset(ct,!is.na(Completion.Date2)))
nrow(subset(ct,!is.na(Completion.Date)))
names(ct)
#View(subset(ct,is.na(Completion.Date2)       ,select=c('Completion.Date','NCT.Number','Completion.Date2')))


nrow(subset(ct,is.na(Completion.Date2)))
#2070

#CONDITION A
nrow(subset(ct,is.na(Primary.Completion.Date2)))
#3023

nrow(subset(ct,is.na(Primary.Completion.Date2)&is.na(Completion.Date2)))
#723   !!!!

#CONDITION B
nrow(subset(ct,is.na(Start.Date2)))
#389 no start date

nrow(subset(ct,!is.na(Primary.Completion.Date2)))
#18938

nrow(subset(ct,!is.na(Primary.Completion.Date2) & !is.na(Start.Date2)  ))
#18891

nrow(ct)

nrow(subset(ct,!is.na(Primary.Completion.Date2) & !is.na(Start.Date2) & Primary.Completion.Date2 >= '2006-01-01'))
#17618

# View(subset(
#             ct
#             ,!is.na(Primary.Completion.Date2) & !is.na(Start.Date2) & Primary.Completion.Date2 >= '2006-01-01'
#             ,select=c('Primary.Completion.Date2')))
#the time condition is working fine



table(ct$Study.Results)


































#part 2

#parse the data

install.packages("XML")
require(XML)
#--ohdsi

rm(ctdata)
i=1
ctdata=data.frame(NCT.Number=ctsubset$NCT.Number,stringsAsFactors=FALSE)
str(ctdata)
ctdata<-data.frame(NCT.Number=c('NCT01148511','NCT01810042','NCT00674323','NCT00473642'))
i=1



save.image('nicePointB.RData')

ctdata<-ctfinal
all<-data.frame()
#--loop
for (i in 1:nrow(ctdata)) {
  #for (i in 1:100) { 
  nct=as.character(ctdata$NCT.Number[i])
  nct
  url=sprintf('http://ClinicalTrials.gov/show/%s?resultsxml=true',nct)
  url
  xml = xmlTreeParse(url,useInternalNode=TRUE)
  #    xml
  #all
  
  #(ns <- getNodeSet(xml, '/clinical_study/clinical_results/reported_events'))
  #(ns <- getNodeSet(xml, '/clinical_study/clinical_results/reported_events/serious_events/category_list'))
  #ns[[2]]
  
  (ns <- getNodeSet(xml, '/clinical_study/clinical_results/reported_events/serious_events/category_list/category/event_list/event/sub_title'))
  
  #fix(ns) #does not work
  df <- xmlToDataFrame(nodes=ns)
  df
  #(ns <- getNodeSet(xml, '/clinical_study/clinical_results/reported_events/serious_events/category_list/category'))
  #df <- xmlToDataFrame(nodes=ns)
  nrow(df)
  if (nrow(df)>0)
  {
   df$NCT<-nct
   df$type<-'S'
   df
   all<-rbind(all,df)
   
  }
  (ctdata[i,'S_event_cnt']=nrow(df))
  
  
  
  
  
  #other
  (ns <- getNodeSet(xml, '/clinical_study/clinical_results/reported_events/other_events/category_list/category/event_list/event/sub_title'))
  df <- xmlToDataFrame(nodes=ns)
  #df
  nrow(df)
  if (nrow(df)>0)
  {df$NCT<-nct
   df$type<-'O'
   all<-rbind(df,all)
   
  }
  (ctdata[i,'O_event_cnt']=nrow(df))
  
  
  #(ns <- getNodeSet(xml, '/clinical_study/clinical_results/reported_events/serious_events/category_list/category/event'))
  #df <- xmlToDataFrame(nodes=ns)
  
  
  #(ns2 <- getNodeSet(xml, '/clinical_study/clinical_results/reported_events/serious_events/category_list/category/event_list/event/sub_title'))
  #df2 <- xmlToDataFrame(nodes=ns2)
  
  
  (ns <- getNodeSet(xml, '/clinical_study/enrollment')) 
  (ctdata[i,'enrollment_type']=paste(sapply(ns, function(x) { xmlAttrs(x) }),collapse="|"))
  
  #cat('.')
  
  
  (ctdata[i,'msh_condition']=paste(sapply(getNodeSet(xml, '//condition_browse/mesh_term'), function(x) { xmlValue(x) }),collapse='|'))
  (ctdata[i,'msh_intervention']=paste(sapply(getNodeSet(xml, '//intervention_browse/mesh_term'), function(x) { xmlValue(x) }),collapse='|'))
  
  print(paste(i,' '))
}

#all
#write.table(all, "clipboard", sep="\t", row.names=FALSE)


#end of big loop------------------------------------




write.csv(all,file="A-all-v011.csv",row.names=FALSE,quote=TRUE)
write.csv(ctdata,file="B-ctdata-v011.csv",row.names=FALSE,quote=TRUE)

str(ctdata)

ctdata$searchURL <- sprintf('http://www.clinicaltrials.gov/ct2/show/%s?resultsxml=true',as.character(ctdata$NCT.Number))
ctdata.min<-subset(ctdata, select=c(NCT.Number,Enrollment,enrollment_type,Phases,msh_condition,msh_intervention,searchURL))


ctdata3  <- merge(all,ctdata.min,by.x="NCT",by.y="NCT.Number",all.x=T,all.y=F,sort=F)
#ctdata3$searchURL <- sprintf('http://www.clinicaltrials.gov/ct2/show/%s?resultsxml=true',as.character(ctdata3$NCT))

write.csv(ctdata3,file="C-ctdata3-v011.csv",row.names=FALSE,quote=TRUE)


