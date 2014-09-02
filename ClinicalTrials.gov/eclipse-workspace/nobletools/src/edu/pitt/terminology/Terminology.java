package edu.pitt.terminology;

import java.util.Collection;
import java.util.Map;

import org.w3c.dom.Document;
import org.w3c.dom.Element;

import edu.pitt.terminology.lexicon.Concept;
import edu.pitt.terminology.lexicon.Relation;
import edu.pitt.terminology.lexicon.Source;
import edu.pitt.terminology.util.Describable;
import edu.pitt.terminology.util.TerminologyException;


/**
 * This class performs basic terminology lookup
 * @author Eugene Tseytlin (University of Pittsburgh)
 */
public interface Terminology extends Describable {

	/**
	 * add new concept to the terminology
	 * @param c
	 */
	public boolean addConcept(Concept c) throws TerminologyException;
	
	/**
	 * update concept information
	 * @param c
	 */
	public boolean updateConcept(Concept c) throws TerminologyException;
	
	/**
	 * remove existing concept
	 * @param c
	 */
	public boolean removeConcept(Concept c) throws TerminologyException;
	
	
	/**
	 * Return list of all sources in this terminology
	 * @return
	 */
	public Source [] getSources();
	
	
	/**
	 * get list of sources that match some criteria
	 * '*' or 'all' means all sources
	 * Ex: NCI,SNOMED,MEDLINE will find relevant source objects in given order
	 * @param match
	 * @return
	 */
	public Source [] getSources(String matchtext);
	
	
	/**
	 * get list of sources that are used as a filter
	 * @return
	 */
	public Source [] getFilterSources();
	
	
	/**
	 * Set source filter. When terminology is used only use stuff from given sources.
	 * The order of sources in Source [] array, should also determine precedence
	 * @param srcs
	 * NOTE: functionality of this call is limmited by underlying implementation
	 * of Terminology
	 */
	public void setFilterSources(Source [] srcs);
	
	
	/**
	 * Return a list of concepts that can be mapped to the input string. 
	 * The list is flat. The input string may contain several concepts.
	 * Each Concept object contains a reference to the text that concept 
	 * was mapped to as well as offset within an input string
	 * @param text to be mapped to concepts
	 * @return List of Concept objects
	 */
	public Concept[] search(String text) throws TerminologyException;

	
	/**
	 * Return a list of concepts that can be mapped to the input string. 
	 * The list is flat. The input string may contain several concepts.
	 * Each Concept object contains a reference to the text that concept 
	 * was mapped to as well as offset within an input string
	 * @param text to be mapped to concepts
	 * @param method - search method, use getSearchMethods to see available 
	 * search methods
	 * @return List of Concept objects
	 */
	public Concept[] search(String text, String method) throws TerminologyException;
	
	
	/**
	 * return supported search methods for this terminology
	 * @return
	 */
	public String [] getSearchMethods();
	
	
	/**
	 * Lookup concept information if unique identifier is available
	 * @param CUI
	 * @return Concept object
	 */
	public Concept lookupConcept(String cui) throws TerminologyException;
	
	

	/**
	 * Get concepts related to parameter concept based on some relationship
	 * @param concept
	 * @param relation
	 * @return related concepts
	 */
	public Concept [] getRelatedConcepts(Concept c, Relation r) throws TerminologyException;
	
	/**
	 * Get all concepts related to parameter concept
	 * @param concept 
	 * @return Map where relation is a key and list of related concepts is a value
	 */
	public Map getRelatedConcepts(Concept c) throws TerminologyException;
	
	
	/**
	 * Get all supported relations between concepts
	 */
	public Relation[] getRelations() throws TerminologyException ;

	/**
	 * Get all relations for specific concept, one actually needs to explore
	 * a concept graph (if available) to determine those
	 */
	public Relation[] getRelations(Concept c) throws TerminologyException ;
	
	/**
	 * Get all supported languages
	 */
	public String [] getLanguages();
	
	
	/**
	 * get all root concepts. This makes sense if Terminology is in fact ontology
	 * that has heirchichal structure
	 * @return
	 */
	public Concept[] getRootConcepts() throws TerminologyException;
	
	
	/**
	 * convert Terminology to XML DOM object representation
	 * @return
	 */
	public Element toElement(Document doc) throws TerminologyException;
	
	/**
	 * initialize terminology from XML DOM object representation
	 * @param element
	 */
	public void fromElement(Element element) throws TerminologyException;
	
	/**
	 * get all available concept objects in terminology. Only sensible for small terminologies
	 * @return
	 */
	public Collection<Concept> getConcepts() throws TerminologyException;
}
