# convertPVTableToLaertes.py
#
# Ad hoc script to take a data file of AERS counts and PV signals and
# create a file that can be loaded into the Laertes evidence base

import csv

linkouts = {
'aers_ebgm': 'http://www.ncbi.nlm.nih.gov/pubmed/22422992',
'aers_eb05': 'http://www.ncbi.nlm.nih.gov/pubmed/22422992',
'aers_report_count': 'http://www.ncbi.nlm.nih.gov/pubmed/22422992',
'aers_prr': 'http://www.ncbi.nlm.nih.gov/pubmed/22422992',
}
    
infS = "/home/rdb20/Downloads/PharmacovigilanceSignal-downloads/AERS_W_MEDDRA_ATC_MAPPED_TO_OMOP_VOCAB_V03.txt"
outfS = "/home/rdb20/OHDSI-code/KnowledgeBase/LAERTES/PVSignals/drug-hoi-pharmacovigilance-signal-data.tsv"


# prr and AERS_COUNTS are used for the Proportional reporting ration and counts of AERS reports respectively
(stitch_id,umls_id,pvalue,drug_mean,drug_sd,bg_mean,bg_sd,drug_num,bg_num,t_statistic,df,drug_cutoff,ind_cutoff,prr,t_denorm_gtr0,t_dnorm_gtr0,e_score_de,chisq,chisq_pvalue,rr,chemical,AERS_COUNTS,CONDITION_CONCEPT_ID,CONDITION_CONCEPT_NAME,INGREDIENT_CONCEPT_ID,INGREDIENT_CONCEPT_NAME,MAPPING_TYPE) = range(0,27)

inf = open(infS, "r")
outf = open(outfS, "w")

## note the format of the evidence out file
#outf.writeline("\t".join(['id', 'evidence_type', 'modality', 'evidence_source_code_id', 'statistic value', 'evidence_linkout', 'statistic_type'])

l = inf.readline()
while l:
    s = l.strip()
    if s == "":
        break

    vals = s.split("\t")
    key = "%s-%s" % (vals[INGREDIENT_CONCEPT_ID],vals[CONDITION_CONCEPT_ID])
    outf.write("\t".join([key,'aers_report_count','positive','5',vals[AERS_COUNTS],linkouts['aers_report_count'],'COUNT','\n']))
    outf.write("\t".join([key,'aers_prr','positive','5',vals[prr],linkouts['aers_prr'],'AERS_PRR','\n']))

    l = inf.readline()
    
inf.close()
outf.close()
