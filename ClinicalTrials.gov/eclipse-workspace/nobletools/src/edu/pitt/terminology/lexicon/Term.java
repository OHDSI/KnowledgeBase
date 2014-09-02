package edu.pitt.terminology.lexicon;

import java.io.Serializable;

import org.w3c.dom.Document;
import org.w3c.dom.Element;

import edu.pitt.terminology.util.TerminologyException;

/**
 * This class describes a term. A string representation of a Concept
 * @author tseytlin
 */
public class Term implements Serializable{
	private static final long serialVersionUID = 1234567890L;
	private String text, language,form;
	private boolean preferred;
	private Source source;
	
	/**
	 * create new term
	 * @param txt
	 */
	public Term(String txt){
		this.text = txt;
	}
	
	/**
	 * @return the form
	 */
	public String getForm() {
		return form;
	}
	/**
	 * @param form the form to set
	 */
	public void setForm(String form) {
		this.form = form;
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
	 * @return the text
	 */
	public String getText() {
		return text;
	}
	/**
	 * @param text the text to set
	 */
	public void setText(String text) {
		this.text = text;
	}
	
	/**
	 * text representation
	 */
	public String toString(){
		return text;
	}
	
	/**
	 * get instance of definition class
	 * @param text
	 * @return
	 */
	public static Term getTerm(String text){
		return new Term(text);
	}
	
	/**
	 * get instance of definition class
	 * @param text
	 * @return
	 */
	public static Term [] getTerms(String [] text){
		if(text == null)
			return new Term [0];
		Term [] d = new Term [text.length];
		for(int i=0;i<d.length;i++)
			d[i] = new Term(text[i]);
		return d;
	}
	
	public int hashCode() {
		return toString().hashCode();
	}

	public boolean equals(Object obj) {
		return toString().equals(obj.toString());
	}
	
	public boolean isAcronym() {
		return "ACR".equals(getForm());
	}
	public boolean isAbbreviation(){
		return form != null && form.endsWith("AB");
	}
	public boolean isRegularExpression(){
		return "RegEx".equals(form);
	}
	
	/**
	 * convert to DOM element
	 * @param doc
	 * @return
	 */
	public Element toElement(Document doc) throws TerminologyException {
		Element root = doc.createElement("Term");
		if(source != null)
			root.setAttribute("source",source.getName());
		if(isPreferred())
			root.setAttribute("preferred",""+isPreferred());
		if(language != null)
			root.setAttribute("language",language);
		if(form != null)
			root.setAttribute("form",form);
		root.setTextContent(text);
		return root;
	}
	/**
	 * convert from DOM element
	 * @param element
	 * @throws TerminologyException
	 */
	public void fromElement(Element element) throws TerminologyException{
		if(element.getTagName().equals("Term")){
			String s = element.getAttribute("source");
			if(s != null && s.length() > 0)
				source = Source.getSource(s);
			form = element.getAttribute("form");
			language = element.getAttribute("language");
			preferred = Boolean.parseBoolean(element.getAttribute("preferred"));
			text = element.getTextContent().trim();
		}
	}
}
