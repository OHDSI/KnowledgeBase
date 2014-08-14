package edu.pitt.terminology;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.Map;

import org.w3c.dom.Document;
import org.w3c.dom.Element;

import edu.pitt.terminology.lexicon.Concept;
import edu.pitt.terminology.lexicon.Relation;
import edu.pitt.terminology.lexicon.Source;
import edu.pitt.terminology.util.TerminologyException;

/**
 * This class performs basic terminology lookup
 * @author Eugene Tseytlin (University of Pittsburgh)
 */
public abstract class AbstractTerminology implements Terminology{

	/**
	 * Return list of all sources in this terminology
	 * @return
	 */
	public abstract Source [] getSources();
	
	
	/**
	 * get list of sources that match some criteria
	 * '*' or 'all' means all sources
	 * Ex: NCI,SNOMED,MEDLINE will find relevant source objects in given order
	 * @param match
	 * @return
	 */
	public Source [] getSources(String matchtext){
		Source [] src = getSources();
		if(src == null ||  matchtext.equals("*") || matchtext.equalsIgnoreCase("all"))
			return src;
		// iterate over sources
		ArrayList list = new ArrayList();
		String [] match = matchtext.split(",");
		for(int j=0;j<match.length;j++){
			for(int i=0;i<src.length;i++){
				if(src[i].getName().matches(".*"+match[j]+".*") || 
				   (src[i].getCode() != null && src[i].getCode().equals(match[j])))
					list.add(src[i]);
			}
		}
		return (Source []) list.toArray(new Source [0]);
	}
	
	
	/**
	 * Get source filter. When terminology is used only use stuff from given sources.
	 * The order of sources in Source [] array, should also determine precedence
	 * @param srcs
	 * NOTE: functionality of this call is limmited by underlying implementation
	 * of Terminology
	 */
	public abstract Source [] getFilterSources();
	
	
	/**
	 * Set source filter. When terminology is used only use stuff from given sources.
	 * The order of sources in Source [] array, should also determine precedence
	 * @param srcs
	 * NOTE: functionality of this call is limmited by underlying implementation
	 * of Terminology
	 */
	public abstract void setFilterSources(Source [] srcs);
	
	
	/**
	 * Return a list of concepts that can be mapped to the input string. 
	 * The list is flat. The input string may contain several concepts.
	 * Each Concept object contains a reference to the text that concept 
	 * was mapped to as well as offset within an input string
	 * @param text to be mapped to concepts
	 * @return List of Concept objects
	 */
	public abstract Concept[] search(String text) throws TerminologyException;

	
	/**
	 * HARD CODED TO IGNORE METHOD ARGUMENT AND DO BEST MATCH SEARCH
	 */
	public Concept[] search(String text, String method) throws TerminologyException {
		return search(text);
	}
	
	
	/**
	 * HARD CODED TO RETURN "best_match" search method
	 * @return 
	 */
	public String [] getSearchMethods(){
		return new String[] {"best_match"};
	}
	
	
	/**
	 * Lookup concept information if unique identifier is available
	 * @param CUI
	 * @return Concept object
	 */
	public abstract Concept lookupConcept(String cui) throws TerminologyException;
	
	
	/**
	 * Convert concept representation of some other API to Conept
	 * @param obj
	 * @return
	 */
	protected abstract Concept convertConcept(Object obj);
	
	/**
	 * Get concepts related to parameter concept based on some relationship
	 * @param concept
	 * @param relation
	 * @return related concepts
	 */
	public abstract Concept [] getRelatedConcepts(Concept c, Relation r) throws TerminologyException;
	
	/**
	 * Get all concepts related to parameter concept
	 * @param concept 
	 * @return Map where relation is a key and list of related concepts is a value
	 */
	public abstract Map getRelatedConcepts(Concept c) throws TerminologyException;
	
	
	/**
	 * Get all supported relations between concepts
	 */
	public Relation[] getRelations() throws TerminologyException {
		throw new TerminologyException("Not implemented");
	}

	/**
	 * Get all relations for specific concept, one actually needs to explore
	 * a concept graph (if available) to determine those
	 */
	public Relation[] getRelations(Concept c) throws TerminologyException {
		throw new TerminologyException("Not implemented");
	}
	
	/**
	 * Get all supported languages
	 */
	public String [] getLanguages() {
		return new String [] {"ENG"};
	}
	
	
	/**
	 * get all root concepts. This makes sence if Terminology is in fact ontology
	 * that has heirchichal structure
	 * @return
	 */
	public Concept[] getRootConcepts() throws TerminologyException {
		throw new TerminologyException("Not implemented");
	}
	
	/**
	 * add new concept to the terminology
	 * @param c
	 */
	public boolean addConcept(Concept c) throws TerminologyException{
		throw new TerminologyException("Not implemented");
	}
	
	/**
	 * update concept information
	 * @param c
	 */
	public boolean updateConcept(Concept c) throws TerminologyException{
		throw new TerminologyException("Not implemented");
	}
	
	/**
	 * remove existing concept
	 * @param c
	 */
	public boolean removeConcept(Concept c) throws TerminologyException{
		throw new TerminologyException("Not implemented");
	}
	
	
	/**
	 * get all available concept objects in terminology. Only sensible for small terminologies
	 * @return
	 */
	public Collection<Concept> getConcepts()  throws TerminologyException{
		throw new TerminologyException("Not implemented");
	}
	
	/**
	 * convert Template to XML DOM object representation
	 * @return
	 */
	public Element toElement(Document doc)  throws TerminologyException{
		Element root = doc.createElement("Terminology");
		
		root.setAttribute("name",getName());
		root.setAttribute("version",getVersion());
		root.setAttribute("location",getLocation());
		root.setAttribute("format",getFormat());
		root.setAttribute("uri",""+getURI());
		
		Element desc = doc.createElement("Description");
		desc.setTextContent(getDescription());
		root.appendChild(desc);
		
		Element sources = doc.createElement("Sources");
		root.appendChild(sources);
		for(Source c: getSources()){
			sources.appendChild(c.toElement(doc));
		}
		
		Element relations = doc.createElement("Relations");
		root.appendChild(relations);
		for(Relation c: getRelations()){
			relations.appendChild(c.toElement(doc));
		}
		
		Element langs = doc.createElement("Languages");
		String s = Arrays.toString(getLanguages());
		langs.setTextContent(s.substring(1,s.length()-1));
		root.appendChild(langs);
		
		
		Element roots = doc.createElement("Roots");
		s = Arrays.toString(getRootConcepts());
		roots.setTextContent(s.substring(1,s.length()-1));
		root.appendChild(roots);
		
		
		Element concepts = doc.createElement("Concepts");
		root.appendChild(concepts);
		for(Concept c: getConcepts()){
			concepts.appendChild(c.toElement(doc));
		}
		
		return root;
	}
	
	/**
	 * convert Template to XML DOM object representation
	 * @return
	 */
	public void fromElement(Element element) throws TerminologyException{
		throw new TerminologyException("Not implemented");
	}
}
