# runUMLSSimilarity.py
# runs the Perl code for UMLS::Similarity from within Python so that the large concept pair file can be processed in small chun

import os,sys,subprocess

PERL_PATH="/usr/bin/perl"
UMLS_SIMILARITY_PATH="/home/rdb20/perl5/bin/umls-similarity.pl"
INFILE="data/umls-similarity-input.txt"
LINE_CHUNK=500
#START_FROM_BLOCK=1190 # use this if the process needs to restart at a certain block
START_FROM_BLOCK=2654 # use this if the process needs to restart at a certain block

PERL_COMMAND="%s %s --config ./umls-similarity-snomed-config.txt --infile /tmp/concept-block-for-umls-similarity.txt -measure wup >> ./output/snomed-concept-similarity-out.txt" % (PERL_PATH, UMLS_SIMILARITY_PATH)

##########
print "Using a data input line block size of %s to run the UMLS:Similarity program" % LINE_CHUNK
print "Deleting ./output/snomed-concept-similarity-out.txt if it exists"
try:
    os.remove("./output/snomed-concept-similarity-out.txt")
except OSError:
    pass

fIn = open(INFILE,"r")
outBuf = ""
blk_count = 0
ctr = 0
for line in iter(fIn):

    if ctr < LINE_CHUNK:
        outBuf += line
        ctr+=1
        continue
    
    elif ctr == LINE_CHUNK and blk_count < START_FROM_BLOCK:
        blk_count += 1
        print "Moving onto next block (%s)" % blk_count
        ctr = 0
        outBuf = ""
        continue
    
    elif ctr == LINE_CHUNK and blk_count >= START_FROM_BLOCK:
        fOut = open("/tmp/concept-block-for-umls-similarity.txt","w")
        fOut.write(outBuf)
        fOut.close()
        print "Wrote block %s" % blk_count
        subprocess.check_call(PERL_COMMAND, shell=True)
        print "Ran UMLS:Similarity on block %s" % blk_count
        blk_count += 1
        ctr = 0
        outBuf = ""

fIn.close()
