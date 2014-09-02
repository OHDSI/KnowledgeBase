package edu.pitt.terminology.util;

import java.beans.PropertyChangeListener;
import java.beans.PropertyChangeSupport;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.Collection;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import edu.pitt.terminology.client.IndexFinderTerminology;
import edu.pitt.terminology.lexicon.Concept;
import edu.pitt.terminology.lexicon.Definition;
import edu.pitt.terminology.lexicon.Relation;
import edu.pitt.terminology.lexicon.SemanticType;
import edu.pitt.terminology.lexicon.Source;
import edu.pitt.terminology.lexicon.Term;

/**
 * import an OBO file to a collection of concept objects
 * @author tseytlin
 */
public class ConceptImporter {
	private PropertyChangeSupport pcs = new PropertyChangeSupport(this);
	private static ConceptImporter instance;
	
	/**
	 * get instance
	 * @return
	 */
	public static ConceptImporter getInstance(){
		if(instance == null)
			instance = new ConceptImporter();
		return instance;
	}
	
	public void addPropertyChangeListener(PropertyChangeListener l){
		pcs.addPropertyChangeListener(l);
	}
	public void removePropertyChangeListener(PropertyChangeListener l){
		pcs.removePropertyChangeListener(l);
	}
	
	/**
	 * add concept
	 * @param term
	 * @param c
	 * @throws TerminologyException
	 */
	private void addConcept(IndexFinderTerminology term, Concept c) throws TerminologyException{
		if(term == null || c == null)
			return;
		term.addConcept(c);
		// if not relations or no breader relations, then it is root
		if(c.getRelationMap() == null || !c.getRelationMap().containsKey(Relation.BROADER))
			term.addRoot(c.getCode());
	}
	
	/**
	 * add concept
	 * @param term
	 * @param c
	 * @throws TerminologyException
	 */
	private void addConcept(Map<String,Concept> list , Concept c) throws TerminologyException{
		if(c == null)
			return;
		list.put(c.getCode(),c);
		pcs.firePropertyChange("Concept Added",null,c.getName());
	}
	
	/**
	 * load OBO file into terminology
	 * @param file
	 * @throws IOException
	 */
	public void loadOBO(IndexFinderTerminology term, File file) throws IOException, TerminologyException {
		for(Concept c: loadOBO(file).values()){
			addConcept(term, c);
		}
	}
	
	/**
	 * load OBO file into terminology
	 * @param file
	 * @throws IOException
	 */
	public Map<String,Concept> loadOBO(File file) throws IOException, TerminologyException {
		Map<String,Concept> list = new LinkedHashMap<String,Concept>();
		String name = file.getName();
		if(name.endsWith(".obo"))
			name = name.substring(0,name.length()-4);
		Source src = Source.getSource(name);
		
		BufferedReader r = null;
		try{
			r = new BufferedReader(new FileReader(file));
			Concept c = null;
			Pattern p = Pattern.compile("\"(.*)\"\\s*([A-Z_]*)\\s*(.*)?\\[.*\\]");
			for(String l=r.readLine();l != null;l=r.readLine()){
				if("[Term]".equals(l.trim())){
					addConcept(list,c);
					c = new Concept("X");
					c.addSource(src);
				}else if(c != null){
					int i = l.indexOf(':');
					if(i > -1){
						String key = l.substring(0,i).trim();
						String val = l.substring(i+1).trim();
						
						// fill in values
						if("id".equals(key)){
							c.setCode(val);
						}else if("name".equals(key)){
							c.setSynonyms(new String [0]);
							c.setName(val);
							Term t = Term.getTerm(val);
							t.setPreferred(true);
							c.addTerm(t);
						}else if("namespace".equals(key)){
							c.addSemanticType(SemanticType.getSemanticType(val));
						}else if("def".equals(key)){
							Matcher m = p.matcher(val);
							if(m.matches())
								val = m.group(1);
							c.addDefinition(Definition.getDefinition(val));
						}else if(key != null && key.matches("(exact_|narrow_|broad_)?synonym")){
							Matcher m = p.matcher(val);
							String form = null;
							if(m.matches()){
								val = m.group(1);
								form = m.group(2);
							}
							Term t = Term.getTerm(val);
							if(form != null)
								t.setForm(form);
							c.addTerm(t);
						}else if("is_a".equals(key)){
							int j = val.indexOf("!");
							if(j > -1)
								val = val.substring(0,j).trim();
							c.addRelatedConcept(Relation.BROADER,val);
							Concept pr = list.get(val);
							if(pr != null)
								pr.addRelatedConcept(Relation.NARROWER,c.getCode());
						}else if("relationship".equals(key)){
							int j = val.indexOf("!");
							int k = val.indexOf(" ");
							if(k > -1){
								String rel = val.substring(0,k).trim();
								if(j > -1)
									val = val.substring(k,j).trim();
								c.addRelatedConcept(Relation.getRelation(rel),val);
							}
						}else if("is_obsolete".equals(key)){
							if(Boolean.parseBoolean(val)){
								c = null;
							}
						}else if("consider".equals(key)){
							// NOOP only relevant when term is obsolete
						}else if("comment".equals(key)){
							// NOOP only relevant when term is obsolete
						}else if("alt_id".equals(key)){
							c.addCode(val,Source.getSource(""));
						}else if("subset".equals(key)){
							// NOOP, don't know what to do with that
						}else if("xref".equals(key)){
							// NOOP, handle external references
						}
					}
				}else if(l.startsWith("default-namespace:")){
					src.setDescription(l.substring("default-namespace:".length()+1).trim());
				}
			}
			addConcept(list,c);
		}catch(IOException ex){
			throw ex;
		}catch(TerminologyException ex){
			throw ex;
		}finally{
			if(r != null)
				r.close();
		}
		return list;
	}
	
	/**
	 * @param args
	 */
	public static void main(String[] args) throws Exception {
		File dir = new File("/home/tseytlin/Data/Coropora/craft-1.0/ontologies");
		//File out = new File("/home/tseytlin/Data/Coropora/craft-1.0/terminologies");
		File out = new File("/home/tseytlin/Data/Coropora/CRAFT_ORF_update");
		//File out = new File("/home/tseytlin/Data/Coropora/CRAFT_RRF_update");
		for(File file: dir.listFiles()){
			if(file.getName().endsWith(".obo")){
				System.out.println("converting "+file.getName()+" ..");
				Collection<Concept> concepts = ConceptImporter.getInstance().loadOBO(file).values();
				//ConceptExporter.getInstances().exportRRF(concepts,out);
				ConceptExporter.getInstances().exportORF(concepts,out);
			}
		}

	}

}
