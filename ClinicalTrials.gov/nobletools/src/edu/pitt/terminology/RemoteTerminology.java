package edu.pitt.terminology;

import java.net.MalformedURLException;
import java.net.URI;
import java.net.URL;
import java.util.Map;
import java.util.Set;

import edu.pitt.terminology.lexicon.Concept;
import edu.pitt.terminology.lexicon.Relation;
import edu.pitt.terminology.lexicon.Source;
import edu.pitt.terminology.util.Parcel;
import edu.pitt.terminology.util.Sender;


/**
 * This class simply forwards all terminology requests to some
 * terminology EVS, CTS, LexBIG running on some given server
 * This class uses servlets to communicate
 * @author tseytlin
 */
public class RemoteTerminology extends AbstractTerminology {
	public static final String DEFAULT_SERVER = "http://slidetutor.upmc.edu/term/servlet/TerminologyServlet";
	private Sender sender;
	private Source [] filter;
	private String term;
	
	/**
	 * Terminology located on a server (forward to some implementation)
	 * @param remote servlet
	 */
	public RemoteTerminology(URL servlet){
		sender = new Sender(servlet);
	}
	
	/**
	 * Terminology located on a server (forward to some implementation)
	 * @param remote servlet
	 */
	public RemoteTerminology(){
		try {
			sender = new Sender(new URL(DEFAULT_SERVER));
		} catch (MalformedURLException e) {
			e.printStackTrace();
		}
	}
	
	/**
	 * get available terminologies
	 * @return
	 */
	public String [] getAvailableTerminologies(){
		Set terms = (Set) sender.sendObject(new Parcel("get_terminologies",null));
		return (String []) terms.toArray(new String [0]);
	}
	
	/**
	 * specify a particular terminology
	 * @param str
	 */
	public void setTerminology(String str){
		term = str;
	}
	
	
	/**
	 * filter parcel before sending
	 * @param p
	 * @return
	 */
	private Parcel filter(Parcel p){
		// set specific terminology
		if(p != null && term != null)
			p.getProperties().setProperty("term",term);
		
		return p;
	}
	
	/**
	 * This method is irrelevant in this context and hence not implemented	 
	 */
	protected Concept convertConcept(Object obj) {
		return null;
	}

	/**
	 * get related concepts
	 */
	public Concept[] getRelatedConcepts(Concept c, Relation r) {
		Concept [] result = (Concept []) sender.sendObject(filter(new Parcel("get_related_concepts",new Object[]{c,r})));
		for(Concept co: result)
			co.setTerminology(this);
		return result;
	}

	/**
	 * get related concepts
	 */
	public Map getRelatedConcepts(Concept c) {
		return (Map) sender.sendObject(filter(new Parcel("get_related_concept_map",c)));
	}
	
	
	/**
	 * Get list of sources that are supported by this terminology
	 */
	public Source[] getSources() {
		return (Source []) sender.sendObject(filter(new Parcel("get_sources",null)));
	}

	
	/**
	 * Set terminology sources
	 */
	public void setFilterSources(Source [] filter) {
		this.filter = filter;
		sender.sendObject(filter(new Parcel("set_sources",filter)));
	}
	
	/**
	 * get filter set from before
	 */
	public Source [] getFilterSources(){
		return filter;
	}
	
	/**
	 * lookup concept object based on CUI
	 */
	public Concept lookupConcept(String cui) {
		Concept c = (Concept) sender.sendObject(filter(new Parcel("lookup_concept",cui)));
		if(c == null)
			return null;
		c.setTerminology(this);
		return c;
	}

	
	/**
	 * Search terminology for concepts
	 */
	public Concept[] search(String text) {
		Concept [] result = (Concept []) sender.sendObject(filter(new Parcel("search",text)));
		if(result == null)
			return new Concept [0];
		for(Concept c: result){
			c.setTerminology(this);
		}
		return result;
	}

	
	/**
	 * get name of an item
	 * @return
	 */
	public String getName(){
		return "Remote Terminology";
	}
	
	/**
	 * get description of an item
	 * @return
	 */
	public String getDescription(){
		return "Forwards all terminology requests to a servlet";
	}
	
	public String toString(){
		return getName();
	}
	
	/**
	 * get version of an item
	 * @return
	 */
	public String getVersion(){
		return "1.0";
	}
	
	/**
	 * get URI of an item
	 * @return
	 */
	public URI getURI(){
		return URI.create(""+sender.getServletURL());
	}
	
	/**
	 * get format
	 * @return
	 */
	public String getFormat(){
		return "HTTP";
	}
	
	/**
	 * get location
	 * @return
	 */
	public String getLocation(){
		return ""+getURI();
	}
}
