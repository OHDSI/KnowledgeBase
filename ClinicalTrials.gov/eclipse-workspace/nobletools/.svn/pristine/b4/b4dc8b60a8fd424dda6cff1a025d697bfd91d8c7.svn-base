package edu.pitt.ontology.protege.concepts;

import java.util.ArrayList;
import java.util.Collections;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import edu.pitt.ontology.IClass;
import edu.pitt.ontology.IOntology;
import edu.pitt.ontology.IProperty;
import edu.pitt.terminology.lexicon.Concept;
import edu.pitt.terminology.lexicon.Definition;
import edu.pitt.terminology.lexicon.SemanticType;
import edu.pitt.terminology.lexicon.Source;
import edu.pitt.terminology.lexicon.Term;

public class ThesaurusConcept extends Concept {
	public ThesaurusConcept(IClass cls){
		super(cls);
		
		// not lets do NCI Thesaurus specifics
		IOntology ont = cls.getOntology();
		
		// do preferred name
		IProperty pn_p = ont.getProperty("Preferred_Name");
		if(pn_p != null){
			Object [] val = cls.getPropertyValues(pn_p);
			if(val.length > 0)
				setName(val[0].toString());
		}
		
		// do synonyms
		IProperty syn_p = ont.getProperty("FULL_SYN");
		if(syn_p != null){
			List<Term> terms = new ArrayList<Term>();
			Set<String> syns = new LinkedHashSet<String>();
			Collections.addAll(syns,getSynonyms());
			for(Object val : cls.getPropertyValues(syn_p)){
				Pattern pt = Pattern.compile(".*<.*:term-name>(.*)</.*:term-name><.*:term-group>(.*)</.*:term-group><.*:term-source>(.*)</.*:term-source>.*");
				Matcher mt = pt.matcher(val.toString());
				if(mt.matches()){
					String text  = mt.group(1);
					String group = mt.group(2);
					String src   = mt.group(3);
					
					Term term = new Term(text);
					term.setForm(group);
					term.setSource(new Source(src));
					
					terms.add(term);
					syns.add(text);
				}
			}
			setTerms(terms.toArray(new Term [0]));
			setSynonyms(syns.toArray(new String [0]));
		}
				
		// do definitions
		List<Definition> deflist = new ArrayList<Definition>();
		IProperty def_p = ont.getProperty("DEFINITION");
		if(def_p != null){
			for(Object val : cls.getPropertyValues(def_p)){
				Pattern pt = Pattern.compile(".*<.*:def-definition>(.*)</.*:def-definition><.*:def-source>(.*)</.*:def-source>.*");
				Matcher mt = pt.matcher(val.toString());
				if(mt.matches()){
					String text  = mt.group(1);
					String src   = mt.group(2);
					
					Definition d = new Definition(text);
					d.setSource(new Source(src));
					deflist.add(d);
				}
			}
		}
		
		IProperty adef_p = ont.getProperty("ALT_DEFINITION");
		if(adef_p != null){
			for(Object val : cls.getPropertyValues(adef_p)){
				Pattern pt = Pattern.compile(".*<.*:def-definition>(.*)</.*:def-definition><.*:def-source>(.*)</.*:def-source>.*");
				Matcher mt = pt.matcher(val.toString());
				if(mt.matches()){
					String text  = mt.group(1);
					String src   = mt.group(2);
					
					Definition d = new Definition(text);
					d.setSource(new Source(src));
					deflist.add(d);
				}
			}
		}
		
		setDefinitions(deflist.toArray(new Definition [0]));
		
		// do semantic type
		IProperty sem_p = ont.getProperty("Semantic_Type");
		if(sem_p != null){
			Object [] val = cls.getPropertyValues(sem_p);
			SemanticType [] types = new SemanticType [val.length];
			for(int i=0;i<val.length;i++){
				types[i] = new SemanticType(val[i].toString());
			}
			setSemanticTypes(types);
		}
		
		// do codes
		IProperty code_p = ont.getProperty("code");
		if(code_p != null){
			Object [] val = cls.getPropertyValues(code_p);
			if(val.length > 0){
				addCode(val[0].toString(),new Source("NCI"));
			}
		}
		
		IProperty umls_p = ont.getProperty("UMLS_CUI");
		if(umls_p != null){
			Object [] val = cls.getPropertyValues(umls_p);
			if(val.length > 0){
				addCode(val[0].toString(),new Source("UMLS"));
			}
		}
		
		IProperty nci_p = ont.getProperty("NCI_META_CUI");
		if(nci_p != null){
			Object [] val = cls.getPropertyValues(nci_p);
			if(val.length > 0){
				addCode(val[0].toString(),new Source("NCI_META"));
			}
		}
	}
}
