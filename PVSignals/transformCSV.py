"""
:author: Jeremy Jao
09.09.2014

Transforms the example OMOP KB output to something that can reflect the 
PSQL.

Assumption that this is all pipe delimited!
"""

import csv


#TODO: These are sample linkouts...
linkouts = {

'aers_ebgm': 'http://www.ncbi.nlm.nih.gov/pmc/articles/PMC1884980/',
'aers_eb05': 'http://www.ncbi.nlm.nih.gov/pubmed/23657824',
'aers_report_count': 'https://open.fda.gov/drug/event/reference/'

}

inp = 'example output from OMOP KBv01.csv'
out = 'example_drug_HOI_evidence_input.csv'
out2 = 'example_drug_HOI_evidence_input_2.csv'
rel = 'example_drug_HOI_relationship_input.csv'
splicer = 'splicer.tsv'

def main():
    """
    reads example output from OMOP KBv01.csv
    outputs example_drug_HOI_evidence_input.csv for the drug_HOI_evidence table
    
    id serial, -- 'primary key',
    drug integer NOT NULL , -- 'OMOP/IMEDS Concept ID for the drug',
    RxNorm_Preferred_Term varchar(100),
    HOI integer NOT NULL , -- 'OMOP/IMEDS for the HOI',
    MedDRA_Preferred_Term varchar(100),
    evidence_type varchar(60) ,
    modality boolean,
    evidence_source_code_id integer ,
    statistic_value int NOT NULL, -- 'For literature-like (e.g., PubMed abstracts, product labeling) sources this holds the count of the number of items of the evidence type present in the evidence base from that source (several rules are used to derive the counts, see documentation on the knowledge-base wiki). From signal detection sources, the result of applying the algorithm indicated in the evidence_type column is shown.' ,
    evidence_linkout varchar(100) NOT NULL,
    statistic_type varchar(60) ,
    """
    infile = open(inp, 'r')
    
    next(infile) #skip header
    
    outfile = open(out, 'w')
    outfile2 = open(out2, 'w')
    splicerIn = open(splicer, 'r')
    relout = open(rel, 'w')
    
    #dict for the drug-HOI relationship entity
    drug_HOI = {}
    
    csvout = csv.writer(outfile, delimiter='|')
    csvout.writerow(['id', 'drug', 'RxNorm_Preferred_Term', 'HOI', 'MedDRA_Preferred_Term', 'evidence_type', 'modality', 'evidence_source_code_id', 'statistic value', 'evidence_linkout', 'statistic_type'])
    
    csvout2 = csv.writer(outfile2, delimiter='|')
    csvout2.writerow(['id', 'drug_HOI_relationship', 'evidence_type', 'modality', 'evidence_source_code_id', 'statistic value', 'evidence_linkout', 'statistic_type'])
    
    csvrel = csv.writer(relout, delimiter='|')
    csvrel.writerow(['id', 'drug', 'RxNorm_Preferred_term', 'HOI', 'MedDRA_Preferred_Term'])
    table_id = 1 #incrementing...
    for line in infile:
        row = line.split('|')
        drug_HOI_rel = str(row[0]) + '-' + str(row[2])
        
        if drug_HOI_rel not in drug_HOI:
            drug_HOI[drug_HOI_rel] = (row[0], row[1], row[2], row[3])
            csvrel.writerow([drug_HOI_rel, row[0], row[1], row[2], row[3]])
            
        csvout.writerow([table_id, row[0], row[1], row[2], row[3], 'aers_report_count', None, 5, row[4], linkouts['aers_report_count'], 'COUNT'])
        csvout2.writerow([table_id, drug_HOI_rel, 'aers_report_count', None, 5, row[4], linkouts['aers_report_count'], 'COUNT'])
        table_id += 1
        csvout.writerow([table_id, row[0], row[1], row[2], row[3], 'aers_ebgm', None, 5, row[5], linkouts['aers_ebgm'], 'AERS_EBGM'])
        csvout2.writerow([table_id, drug_HOI_rel, 'aers_ebgm', None, 5, row[5], linkouts['aers_ebgm'], 'AERS_EBGM'])
        table_id += 1
        csvout.writerow([table_id, row[0], row[1], row[2], row[3], 'aers_eb05', None, 5, row[6], linkouts['aers_eb05'], 'AERS_EB05'])
        csvout2.writerow([table_id, drug_HOI_rel, 'aers_eb05', None, 5, row[6], linkouts['aers_eb05'], 'AERS_EB05'])
        table_id += 1
        
    for line in splicerIn:
        row = line.split("\t")
        if 'NULL' in row[0]:
            continue
        csvout2.writerow((table_id, row[0], row[1], setBoolean(row[2]), row[3], row[4], row[5], row[6].strip()))
        table_id += 1
    infile.close()
    outfile.close()
    outfile2.close()
    relout.close()
    
def setBoolean(inp):
    if inp == 'positive':
        return 'true'
    if inp == 'negative':
        return 'false'
    return ''
if __name__ == '__main__':
    main()
