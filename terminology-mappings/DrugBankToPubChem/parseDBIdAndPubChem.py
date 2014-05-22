'''
Created 05/22/2014

@authors: Rich Boyce and Yifan Ning

@summary: parse PubChem substance and compound ids and drugbank_id from drugbank.xml
          output terms: Drugbank URI, PubChem substance, PubChem compound
          output file: Drugbank-PubChem.txt
'''

import xml.etree.ElementTree as ET
import os, sys

DRUGBANK_XML = "drugbank.xml"

NS = "{http://drugbank.ca}" 


dict_pubchem_dbid = {}

'''
data structure of drugbank.xml
	
<drug>...
 <drugbank-id>...
 <name>...</name>
  <external-identifier>
    <resource>PubChem Compound</resource>
    <identifier>...</identifier>
  </external-identifier>
  <external-identifier>
    <resource>PubChem Substance</resource>
    <identifier>...</identifier>
  </external-identifier>

'''

#print out mappings drugbankid to drugbankid,drugbankName,pubchemSubstanceId,pubchemCompoundId
def parseDbIdAndPubChem(root):
    for drug in root.iter(tag=NS + "drug"):
        subId = drug.find(NS + "drugbank-id")
        
        if subId == None:
            continue
        else:
            drugbankid = unicode(subId.text)
            drugbankName = unicode(drug.find(NS + "name").text)   

            pubchemSubstanceId = ""
            pubchemCompoundId = ""
            for exIdens in drug.iter(NS + "external-identifiers"):
                for exIden in exIdens.iter(NS + "external-identifier"):

                    resource = exIden.find(NS + "resource")
                    if resource == None:
                        continue

                    if resource.text == "PubChem Substance":
                        childIdenti = exIden.find(NS + "identifier") 
                        if childIdenti == None:
                            continue
                        else:
                            pubchemSubstanceId = unicode(childIdenti.text)

                    if resource.text == "PubChem Compound":
                        childIdenti = exIden.find(NS + "identifier") 
                        if childIdenti == None:
                            continue
                        else:
                            pubchemCompoundId = unicode(childIdenti.text)

            dict_pubchem_dbid[drugbankid] = (drugbankid,drugbankName,pubchemSubstanceId,pubchemCompoundId)
            output = "\t".join(dict_pubchem_dbid[drugbankid])
            print output.encode('utf-8').strip()

                           
tree = ET.parse(DRUGBANK_XML)
root = tree.getroot()

output = "drugbankid\tdrugbankName\tpubchemSubstanceId\tpubchemCompoundId"
print output.encode('utf-8').strip()

parseDbIdAndPubChem(root)

# for drugbankid,l in dict_pubchem_dbid.iteritems():
#     output = "drugbankid\tdrugbankName\tpubchemSubstanceId\tpubchemCompoundId"
#     print output.encode('utf-8').strip()

#     output = "\t".join(l)
#     print output.encode('utf-8').strip()

