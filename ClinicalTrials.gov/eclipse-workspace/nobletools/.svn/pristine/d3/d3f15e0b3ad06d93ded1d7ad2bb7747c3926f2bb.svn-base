package edu.pitt.ontology.protege.concepts;

import java.util.ArrayList;
import java.util.List;

import edu.pitt.ontology.IClass;
import edu.pitt.ontology.IOntology;
import edu.pitt.ontology.IProperty;
import edu.pitt.terminology.lexicon.Concept;
import edu.pitt.terminology.lexicon.Definition;
import edu.pitt.terminology.lexicon.Source;

public class FMAConcept extends Concept {
	public FMAConcept(IClass cls) {
		super(cls);
		
		// not lets do NCI Thesaurus specifics
		IOntology ont = cls.getOntology();
		
		// do codes
		IProperty code_p = ont.getProperty("FMAID");
		if(code_p != null){
			Object [] val = cls.getPropertyValues(code_p);
			if(val.length > 0)
				addCode(val[0].toString(),new Source("FMA"));
		}
		IProperty umls_p = ont.getProperty("UMLS_ID");
		if(umls_p != null){
			Object [] val = cls.getPropertyValues(umls_p);
			if(val.length > 0)
				addCode(val[0].toString(),new Source("UMLS"));
		}
		
		// do definitions
		List<Definition> deflist = new ArrayList<Definition>();
		IProperty def_p = ont.getProperty("definition");
		if(def_p != null){
			for(Object val : cls.getPropertyValues(def_p)){
				Definition d = new Definition(val.toString());
				deflist.add(d);
			}
		}
		setDefinitions(deflist.toArray(new Definition [0]));
		
	}
}
