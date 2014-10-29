In folder Vojtech-huser on github are some new files
https://github.com/OHDSI/KnowledgeBase/tree/master/ClinicalTrials.gov/vojtech-huser
 
 
 
file01 is raw input data that we start with (too big to email, not attached)
 
file02 is a not so great summary file (HOI is missing, there is one row per trial)  (it has 3000 rows) (attached)
Description: cid:image001.png@01CFB1F1.8224D3C0
 
 
file03- better detailed import file B (was attached but bounced back so only on github) (sorry for 13mb file but github is terrible for fetching a single file…)
_cid = _concept_id
Example below:
Description: cid:image002.png@01CFB1F3.1DCDF580
 
File 03 is missing quite key counts parameter. For many HOIs – the ADE (serious and other (there are 2 tables)) table lists 0 counts. But the 0 is, is in fact, negative evidence and is also important.
 
File 03 is produced mainly to “practice the NLP further pipeline” and provide yet another example of import into the emerging, early release of the KB.
