package edu.pitt.terminology.lexicon;

import java.io.Serializable;

import org.w3c.dom.Document;
import org.w3c.dom.Element;

import edu.pitt.terminology.util.TerminologyException;

/**
 * Describes relationship between 2 concepts
 * @author tseytlin
 */
public class Relation  implements  Serializable{
	private static final long serialVersionUID = 1234567890L;
	// some predefined relationships
	public static Relation BROADER = new Relation("Broader");
	public static Relation NARROWER = new Relation("Narrower");
	public static Relation SIMILAR = new Relation("Similar");
	
	
	private String name,code;
	private boolean inverse;
	

	/**
	 * Relation is inverse.
	 * false - if Concept that returns this relation is a source of it
	 * true  - if Concept that returns this relation is a target of it
	 * @return the inverse
	 */
	public boolean isInverse() {
		return inverse;
	}

	/**
	 * @param inverse the inverse to set
	 */
	public void setInverse(boolean inverse) {
		this.inverse = inverse;
	}

	
	
	/**
	 * Create new realtion
	 * @param name
	 * @param code
	 */
	public Relation(String name){
		this(name,name);
	}
	

	/**
	 * Create new realtion
	 * @param name
	 * @param code
	 */
	public Relation(String name, String code){
		this.name = name;
		this.code = code;
	}
	
	
	/**
	 * @return the code
	 */
	public String getCode() {
		return code;
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
	 * String representation
	 */
	public String toString(){
		return name;
	}
		
	/**
	 * get instance of definition class
	 * @param text
	 * @return
	 */
	public static Relation getRelation(String text){
		return new Relation(text);
	}
	
	/**
	 * get instance of definition class
	 * @param text
	 * @return
	 */
	public static Relation [] getRelations(String [] text){
		if(text == null)
			return new Relation [0];
		Relation [] d = new Relation [text.length];
		for(int i=0;i<d.length;i++)
			d[i] = new Relation(text[i]);
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
		Element root = doc.createElement("Source");
		root.setAttribute("name",getName());
		root.setAttribute("code",getCode());
		root.setAttribute("inverse",""+isInverse());
		
		return root;
	}
	/**
	 * convert from DOM element
	 * @param element
	 * @throws TerminologyException
	 */
	public void fromElement(Element element) throws TerminologyException{
		if(element.getTagName().equals("Source")){
			setName(element.getAttribute("name"));
			setCode(element.getAttribute("code"));
			setInverse(Boolean.parseBoolean(element.getAttribute("inverse")));
		}
	}
}
