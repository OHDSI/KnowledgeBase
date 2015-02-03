"""

:author: Jeremy Jao
09.04.2014

This is a class that will process MRCONSO.rff from the UMLS datasets:

http://www.nlm.nih.gov/pubs/factsheets/umlsmeta.html

http://www.nlm.nih.gov/research/umls/knowledge_sources/metathesaurus/release/abbreviations.html

To get the UMLS datasets, you must have a UMLS account then download it.

Usually this is designed to process MRCONSO.RRF

Important MRCONSO assumptions (http://www.ncbi.nlm.nih.gov/books/NBK9685/):
- Pipe delimited
- Indexes
    - 0: UMLS CUI
    - 1: Language of term
    - 11: Knowledgebase
    - 12: Type of term within Knowledgebase (Preferred term, etc.)
    - 13: Ontology's CUI
    - 14: String term of the Ontology

Then it will take the UMLS CUI's Preferred English term's CUIs:
- name
- SNOMED
- MESH
- MEDDRA
- RxNorm

This is done in a dict: (SNOMED, MESH, MEDDRA, RXNORM) tuple

I will make the code to be as extensible as possible.

"""
import cPickle as pickle

inp = '/home/rdb20/UMLS/2014AB/META/MRCONSO.RRF'

class UMLS_CUIs:
    
    cui = {'SNOMEDCT_US':1, 'MSH':2, 'MDR':3, 'RXNORM':4}
    """
    This is the global dictionary of the location in the structure to get
    a the structure's CUIs from different databases
    """
    
    
    def __init__(self):
        """Initializes the class to create the UMLS dictionary of preferred terms
        """
        self.structure = {}

    def process(self, location):
        """
        Processes the file given. This was designed to process MRCONSO.rff
        on English terms and only return SNOMED, MESH, MEDDRA, and RXNORM CUIs
        
        :param location: location of MRCONSO.rff
        """
        with open(location, 'r') as fil:
            
            for line in fil:
                split = line.split('|')
                umls_cui, language, kb, term_type, kb_cui, kb_name = self.__getConcepts(split)
                self.__addCUI(umls_cui, language, kb, term_type, kb_cui, kb_name)
                
                
    def __getConcepts(self, split):
        """
        Gets the Concepts from MRCONSO.RRF
        
        Creates a multi-return of:
        - UMLS CUI as umls_cui
        - Language of the Term as language
        - Knowledgebase as kb
        - term type (preferred term as PT, synonym as SY etc.) as term_type
        - Knowledgebase CUI as kb_cui
        - Name of Term as kb_name
        
        :param split: a list of a line from MRCONSO.rff that was pre-split from a previous method
        """
        umls_cui = split[0].strip()
        language = split[1].strip()
        kb = split[11].strip()
        term_type = split[12].strip()
        kb_cui = split[13].strip()
        kb_name = split[14].strip()
        return umls_cui, language, kb, term_type, kb_cui, kb_name
    
    def __addCUI(self, umls_cui, language, kb, term_type, kb_cui, kb_name):
        """
        Adds the UMLS CUIs to the UMLS python structure
        
        The CUIs will be added if and only if the UMLS entity is English
        and a preferred term. SNOMED and MESH are assumed to all be active
        since I didnt' have any conflicts with many CUIs for them.
        
        For now, for every different kb CUI, I add it to itself pipe delimited.
        So for UMLS CUIs with multiple SNOMED CUIs -> cui1|cui2... etc.
        
        :param umls_cui: the UMLS CUI
        :param language: language of the UMLS entity (ENG etc.)
        :param kb: Type of knowledgebase UMLS is pointing to
        :param term_type: type of term given (PT etc.)
        :param kb_cui: the type of cui from the knowledgebase given
        :param kb_name: the string of the term
        """
        self.__initializeEntityIfNotPresent(umls_cui)
        
        #print term_type
        #print language
        #print kb_cui
        #print ''
        #if term_type == 'PT' and language == 'ENG' and kb in self.cui:
        if language == 'ENG' and ((kb in ('RXNORM', 'MSH')) or term_type in ('PT', 'MH', 'SCD','MIN')) and kb in self.cui:
            #if self.structure[umls_cui][self.cui[kb]] is not None:
                #print umls_cui + ' ' + kb + ' '
                #print 'old: ' + self.structure[umls_cui][self.cui[kb]]
                #print 'new: ' + kb_cui
                #self.structure[umls_cui][0] += '|' + kb_name
                #self.structure[umls_cui][self.cui[kb]] += '|' + kb_cui
                #print ''
            #else:
                #self.structure[umls_cui][self.cui[kb]] = kb_cui
            if self.structure[umls_cui][0] == None:
                self.structure[umls_cui][0] = kb_name
            if kb_cui not in self.structure[umls_cui][self.cui[kb]]:
                self.structure[umls_cui][self.cui[kb]].append(kb_cui)
                
    def __inStructure(self, umls_cui):
        """
        This will check whether the UMLS CUI is in the structure
        
        :param umls_cui: the UMLS CUI being fed into the structure
        :return: a boolean if the CUI being fed is in the UMLS dic structure
        """
        return (umls_cui in self.structure)
    
    def __initializeEntityIfNotPresent(self, umls_cui):
        """
        Puts an empty entity into the UMLS dictionary structure if not
        present in the structure as the UMLS CUI as a string and 
        5 tuples (currently) of strings. They will be initialized as None
        and added as the file processes MRCONSO.RRF
        
        It is not expected that this will be full per entity
        
        Structure -> struc[cui] = (
                                    preferred name,
                                    SNOMED CUI,
                                    MESH CUI,
                                    MEDDRA CUI,
                                    RXNORM CUI
                                  )
        :param umls_cui: the key of the UMLS structure
        :param kb_name: the preferred UMLS entity's name
        """
        if not (self.__inStructure(umls_cui)):
            self.structure[umls_cui] = [None, [], [], [], []]
            
    def getName(self, umls_cui):
        """
        :param umls_cui: The UMLS CUI being retrieved
        :return: The name of the Concept's CUI if present, else None
        """
        if self.__inStructure(umls_cui):
            return self.structure[umls_cui][0]
        return None
        
    def getSnomedct_usCui(self, umls_cui):
        """
        :param umls_cui: The UMLS CUI being retrieved
        :return: The SNOMEDCT_US CUI if present, else None
        """
        if self.__inStructure(umls_cui):
            return self.listToPipe(self.structure[umls_cui][1])
            #return self.structure[umls_cui][1]
        return None
        
    def getMeshCui(self, umls_cui):
        """
        :umls_cui: The UMLS CUI being retrieved
        :return: The MeSH CUI if present
        """
        if self.__inStructure(umls_cui):
            return self.listToPipe(self.structure[umls_cui][2])
            #return self.structure[umls_cui][2]
        return None
        
    def getMeddraCui(self, umls_cui):
        """
        :param umls_cui: The UMLS CUI being retrieved
        :return: The MedDRA CUI if present
        """
        if self.__inStructure(umls_cui):
            return self.listToPipe(self.structure[umls_cui][3])
            #return self.structure[umls_cui][3]
        return None
        
    def getRxnormCui(self, umls_cui):
        """
        :param umls_cui: The UMLS CUI being retrieved
        :return: the RxNorm CUI if present
        """
        if self.__inStructure(umls_cui):
            return self.listToPipe(self.structure[umls_cui][4])
            #return self.structure[umls_cui][4]
        return None

    def listToPipe(self, lis):
        start = True
        string = None
        for li in lis:
            if start:
                start = False
                string = li
            else:
                string += '|' + li
                
        return string

def main():
    """
    Will be serializing the UMLS python dictionary if main is run
    as a cPickle
    """
    umls_cuis = UMLS_CUIs()
    umls_cuis.process(inp)
    testCUI = 'C0013604'
    
    print umls_cuis.getName(testCUI)
    print umls_cuis.getMeshCui(testCUI)
    print umls_cuis.getRxnormCui(testCUI)
    print umls_cuis.getSnomedct_usCui(testCUI)
    print umls_cuis.getMeddraCui(testCUI)
    
    testCUI = 'C0055447'
    print umls_cuis.getName(testCUI)
    print umls_cuis.getMeshCui(testCUI)
    print umls_cuis.getRxnormCui(testCUI)
    print umls_cuis.getSnomedct_usCui(testCUI)
    print umls_cuis.getMeddraCui(testCUI)
    
    pickle.dump(umls_cuis, open('umlsStructure.cPickle', 'wb'))

if __name__ == '__main__':
    main()
