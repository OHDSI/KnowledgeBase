package edu.pitt.ontology.protege.concepts;

import edu.pitt.ontology.IClass;
import edu.pitt.ontology.IOntology;
import edu.pitt.ontology.IProperty;
import edu.pitt.ontology.bioportal.BioPortalHelper;
import edu.pitt.terminology.lexicon.Concept;
import edu.pitt.terminology.lexicon.SemanticType;
import edu.pitt.terminology.lexicon.Source;

public class BioPortalConcept extends Concept {
	public BioPortalConcept(IClass cls) {
		super(cls);
		
		// not lets do NCI Thesaurus specifics
		IOntology ont = cls.getOntology();
		
		// do code
		IProperty code_p = ont.getProperty(BioPortalHelper.CODE);
		if(code_p != null){
			for(Object val : cls.getPropertyValues(code_p)){
				addCode(val.toString(),new Source(val.toString()));
			}
		}
		
		// do sem type
		IProperty sem_p = ont.getProperty(BioPortalHelper.SEMANTIC_TYPE);
		if(sem_p != null){
			Object [] val = cls.getPropertyValues(sem_p);
			SemanticType [] types = new SemanticType [val.length];
			for(int i=0;i<val.length;i++){
				types[i] = new SemanticType(val[i].toString());
			}
			setSemanticTypes(types);
		}
	}
}
