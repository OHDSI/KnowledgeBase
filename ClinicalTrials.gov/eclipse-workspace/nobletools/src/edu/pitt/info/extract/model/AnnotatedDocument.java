package edu.pitt.info.extract.model;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

import edu.pitt.info.extract.model.util.SynopticReportDetector;
import edu.pitt.terminology.lexicon.Annotation;
import edu.pitt.terminology.lexicon.Concept;

/**
 * this class represents the original decument along with processed concept annotations
 * @author tseytlin
 *
 */
public class AnnotatedDocument {
	private String text,name;
	private List<Annotation> annotations;
	private List<Concept> concepts;
	private List<DocumentFilter> filters;
	private int [] synapticRange;
	private static SynopticReportDetector synopticDetector = new SynopticReportDetector();
	
	/**
	 * get original report text
	 * @return
	 */
	public String getText() {
		return text;
	}
	
	/**
	 * get filtered document 
	 * @return
	 */
	public String getFilteredDocument(){
		String filtered = getText();
		for(DocumentFilter filter : getFilters()){
			filtered = filter.filter(filtered);
		}
		return filtered;
	}
	
	/**
	 * set report text
	 * @param text
	 */
	public void setText(String text) {
		this.text = text;
		synapticRange = null;
	}
	public List<Annotation> getAnnotations() {
		if(annotations == null)
			annotations = new ArrayList<Annotation>();
		return annotations;
	}
	public void addAnnotation(Annotation a) {
		getAnnotations().add(a);
	}
	public String getName() {
		return name;
	}
	public void setName(String name) {
		this.name = name;
	}
	public List<Concept> getConcepts() {
		if(concepts == null)
			concepts = new ArrayList<Concept>();
		return concepts;
	}
	public void addConcept(Concept c){
		getConcepts().add(c);
	}
	
	public void sort(){
		Collections.sort(getAnnotations());
		Collections.sort(getConcepts());
	}
	
	public String toString(){
		return name;
	}

	
	public List<DocumentFilter> getFilters() {
		if(filters == null)
			filters = new ArrayList<DocumentFilter>();
		return filters;
	}
		
	public boolean hasSynopticSection(){
		if(synapticRange == null){
			synapticRange = synopticDetector.getSynopticReportRange(getText());
		}
		return synapticRange != null && synapticRange.length == 2 && synapticRange[0] > -1;
	}
	
	/**
	 * skip line if offset is within synaptic report range
	 * @param offset
	 * @param synRange
	 * @return
	 */
	public boolean isSynopticSection(int offset){
		if(hasSynopticSection())
			return synapticRange[0] <= offset && offset <= synapticRange[1];
		return false;
	} 

	/**
	 * skip line if offset is within synaptic report range
	 * @param offset
	 * @param synRange
	 * @return
	 */
	public String getSynopticSection(){
		if(hasSynopticSection())
			return getText().substring(synapticRange[0],synapticRange[1]);
		return "";
	} 

}
