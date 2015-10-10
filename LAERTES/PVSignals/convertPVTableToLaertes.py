# convertPVTableToLaertes.py
#
# Ad hoc script to take a data file of AERS counts and PV signals and
# create a file that can be loaded into the Laertes evidence base

import csv

# TODO - generated using the data provided by OpenFDA but apparently, multiple reports are not easy to return e.g., https://api.fda.gov/drug/event.json?search=safetyreportid:%228493487-2%22+safetyreportid:%2210046047%22
LINKOUT_TMPL = ""
    
infS = "/home/rdb20/Downloads/PharmacovigilanceSignal-downloads/faers_standard_drug_outcome_statistics.backup"
outfS = "/home/rdb20/OHDSI-code/KnowledgeBase/LAERTES/PVSignals/drug-hoi-pharmacovigilance-signal-data.tsv"


# prr and AERS_COUNTS are used for the Proportional reporting ration and counts of AERS reports respectively
(drug_concept_id,outcome_concept_id,snomed_outcome_concept_id,case_count,prr,prr_95_percent_upper_confidence_limit,prr_95_percent_lower_confidence_limit,ror,ror_95_percent_upper_confidence_limit,ror_95_percent_lower_confidence_limit) = range(0,10)

inf = open(infS, "r")
outf = open(outfS, "w")

## note the format of the evidence out file
#outf.writeline("\t".join(['id', 'evidence_type', 'modality', 'evidence_source_code_id', 'statistic value', 'evidence_linkout', 'statistic_type'])

# get rid of the first 25 lines...
l = inf.readline()
while l.find("COPY faers_standard_drug_outcome_statistics (drug_concept_id, outcome_concept_id, snomed_outcome_concept_id, case_count, prr, prr_95_percent_upper_confidence_limit, prr_95_percent_lower_confidence_limit, ror, ror_95_percent_upper_confidence_limit, ror_95_percent_lower_confidence_limit) FROM stdin;") == -1:
    l = inf.readline()

l = inf.readline()
while l:
    s = l.strip()
    if s == "\.":
        break

    vals = s.split("\t")
    key = "%s-%s" % (vals[drug_concept_id],vals[outcome_concept_id]) # Note the key is in MedDRA because the snomed mappings tend to need revision which happens at load time
    outf.write("\t".join([key,'aers_report_count','positive','5',vals[case_count],"",'COUNT','\n']))
    outf.write("\t".join([key,'aers_report_prr','positive','5',vals[prr],"",'AERS_PRR','\n']))
    # TODO: add the other data that is available (but this affects the webapi)

    l = inf.readline()
    
inf.close()
outf.close()
