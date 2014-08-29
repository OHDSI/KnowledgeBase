package edu.pitt.terminology.lexicon;

import java.io.Serializable;

import org.w3c.dom.Document;
import org.w3c.dom.Element;

import edu.pitt.terminology.util.TerminologyException;

/**
 * Wrapps definition
 * @author tseytlin
 */
public class Definition implements Serializable{
	private static final long serialVersionUID = 1234567890L;
	private Source source;
	private String definition,language;
	private boolean preferred;
	
	public Definition(){};
	
	/**
	 * Create new definition
	 * @param txt
	 */
	public Definition(String txt){
		this.definition = txt;
	}
	
	
	/**
	 * @return the definition
	 */
	public String getDefinition() {
		return definition;
	}
	/**
	 * @param definition the definition to set
	 */
	public void setDefinition(String definition) {
		this.definition = definition;
	}
	/**
	 * @return the source
	 */
	public Source getSource() {
		return source;
	}
	/**
	 * @param source the source to set
	 */
	public void setSource(Source source) {
		this.source = source;
	}
	
	/**
	 * Make it readable
	 */
	public String toString(){
		return definition;
	}

	/**
	 * @return the preferred
	 */
	public boolean isPreferred() {
		return preferred;
	}

	/**
	 * @param preferred the preferred to set
	 */
	public void setPreferred(boolean preferred) {
		this.preferred = preferred;
	}

	/**
	 * @return the language
	 */
	public String getLanguage() {
		return language;
	}

	/**
	 * @param language the language to set
	 */
	public void setLanguage(String language) {
		this.language = language;
	}
	
	/**
	 * get instance of definition class
	 * @param text
	 * @return
	 */
	public static Definition getDefinition(String text){
		return new Definition(text);
	}
	
	/**
	 * get instance of definition class
	 * @param text
	 * @return
	 */
	public static Definition [] getDefinitions(String [] text){
		if(text == null)
			return new Definition [0];
		Definition [] d = new Definition [text.length];
		for(int i=0;i<d.length;i++)
			d[i] = new Definition(text[i]);
		return d;
	}

	public int hashCode() {
		return toString().hashCode();
	}

	public boolean equals(Object obj) {
		return toString().equals(obj.toString());
	}
	
	/**
	 * convert to DOM element
	 * @param doc
	 * @return
	 */
	public Element toElement(Document doc) throws TerminologyException {
		Element root = doc.createElement("Definition");
		if(source != null)
			root.setAttribute("source",source.getName());
		if(isPreferred())
			root.setAttribute("preferred",""+isPreferred());
		if(language != null)
			root.setAttribute("language",language);
		root.setTextContent(definition);
		return root;
	}
	/**
	 * convert from DOM element
	 * @param element
	 * @throws TerminologyException
	 */
	public void fromElement(Element element) throws TerminologyException{
		if(element.getTagName().equals("Definition")){
			String s  = element.getAttribute("source");
			language = element.getAttribute("language");
			definition = element.getTextContent().trim();
			preferred = Boolean.parseBoolean(element.getAttribute("preferred"));
			if(s != null && s.length() > 0)
				source = Source.getSource(s);
		}
	}
}
