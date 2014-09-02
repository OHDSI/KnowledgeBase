package edu.pitt.terminology.lexicon;

import java.io.Serializable;

import org.w3c.dom.Document;
import org.w3c.dom.Element;

import edu.pitt.terminology.util.TerminologyException;

/**
 * This class describes a sematic type of a concept
 * @author tseytlin
 *
 */
public class SemanticType implements Serializable{
	private static final long serialVersionUID = 1234567890L;
	private String name, code;

	/**
	 * Create semantic type w/ name and code
	 * @param name
	 * @param code
	 */
	public SemanticType(String name){
		this(name,name);
	}
	
	/**
	 * Create semantic type w/ name and code
	 * @param name
	 * @param code
	 */
	public SemanticType(String name, String code){
		this.name = name;
		this.code = code;
	}
	
	/**
	 * @return the code
	 */
	public String getCode() {
		return (code != null)?code:name;
	}

	/**
	 * @param code the code to set
	 */
	public void setCode(String code) {
		this.code = code;
	}

	/**
	 * @return the name
	 */
	public String getName() {
		return name;
	}

	/**
	 * @param name the name to set
	 */
	public void setName(String name) {
		this.name = name;
	}
	
	/**
	 * string representation (name)
	 */
	public String toString(){
		return name;
	}
	
	/**
	 * get instance of definition class
	 * @param text
	 * @return
	 */
	public static SemanticType getSemanticType(String text){
		return new SemanticType(text);
	}
	
	/**
	 * get instance of definition class
	 * @param text
	 * @return
	 */
	public static SemanticType [] getSemanticTypes(String [] text){
		if(text == null)
			return new SemanticType [0];
		SemanticType [] d = new SemanticType [text.length];
		for(int i=0;i<d.length;i++)
			d[i] = new SemanticType(text[i]);
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
		Element e = doc.createElement("SemanticType");
		e.setAttribute("name",getName());
		e.setAttribute("code",getCode());
		return e;
	}
	
	/**
	 * convert from DOM element
	 * @param element
	 * @throws TerminologyException
	 */
	public void fromElement(Element element) throws TerminologyException{
		if(element.getTagName().equals("SemanticType")){
			setName(element.getAttribute("name"));
			setCode(element.getAttribute("code"));
		}
	}
}
