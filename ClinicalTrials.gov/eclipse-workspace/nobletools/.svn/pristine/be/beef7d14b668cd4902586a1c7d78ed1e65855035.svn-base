package edu.pitt.terminology.lexicon;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

import edu.pitt.text.tools.TextTools;

/**
 * concept annotation
 * @author tseytlin
 */
public class Annotation implements Serializable, Comparable<Annotation>{
	private static final long serialVersionUID = 1234567890L;
	private String text, searchString;
	private int offset;
	private transient Concept concept;
	
	public Concept getConcept() {
		return concept;
	}
	public void setConcept(Concept concept) {
		this.concept = concept;
	}
	public String getText() {
		return text;
	}
	public void setText(String text) {
		this.text = text;
	}
	public String getSearchString() {
		return searchString;
	}
	public void setSearchString(String searchString) {
		this.searchString = searchString;
	}
	public int getOffset() {
		return offset;
	}
	public void updateOffset(int o){
		offset += o;
	}
	public int getLength(){
		return text.length();
	}
	public int getStartPosition(){
		return offset;
	}
	public int getEndPosition(){
		return offset+text.length();
	}
	public void setOffset(int offset) {
		this.offset = offset;
	}
	public String toString(){
		return text+"/"+offset;
	}
	public int hashCode() {
		return toString().hashCode();
	}

	public boolean equals(Object obj) {
		if(obj instanceof Annotation){
			if(offset != ((Annotation)obj).offset)
				return false;
		}else{
			return false;
		}
		return toString().equals(obj.toString());
	}
	
	
	public int compareTo(Annotation a) {
		int d = getOffset() - a.getOffset();
		if(d == 0)
			return getLength() - a.getLength();
		return d;
	}
	
	
	/**
	 * if annotation is already known, this method adds annotation properly to a concept
	 * @param c
	 * @param text
	 * @param offset
	 */
	public static void addAnnotation(Concept c, String txt, int offset){
		// add matched text
		c.addMatchedTerm(txt);
		
		// add annotation
		Annotation a = new Annotation();
		a.setText(txt);
		a.setConcept(c);
		a.setOffset(offset);
		c.addAnnotation(a);
		
		// add matched text
		int offs = Integer.MAX_VALUE;
		StringBuffer b = new StringBuffer();
		for(Annotation an: c.getAnnotations()){
			if(an.getOffset() < offs)
				offs = an.getOffset();
			b.append(an.getText()+" ");
		}
		c.setOffset(offs);
		c.setText(b.toString().trim());
	}
	
	/**
	 * Get a list of contiguous concept annotations from a given concept
	 * Essentially converts a single concepts that annotates multiple related words to text
	 * to potentially multiple instances of a concept in text
	 * @param c
	 * @return
	 */
	public static List<Annotation> getAnnotations(Concept c){
		String text = c.getSearchString();
		List<Annotation> list = new ArrayList<Annotation>();
		try{
			int st = -1,en = -1;
			Set<String> usedWords = new HashSet<String>();
			for(Annotation a: c.getAnnotations()){
				String w = TextTools.normalize(a.getText(),true);
				// this word was encountered before, saved previous annoation
				if(usedWords.contains(w)){
					Annotation an = new Annotation();
					an.setSearchString(text);
					an.setConcept(c);
					an.setOffset(st);
					an.setText(text.substring(st,en));
					list.add(an);
					usedWords.clear();
					st = -1;
				}
				
				// start w/ first annotation
				if(st < 0)
					st = a.getStartPosition();
				// remember end position
				en = a.getEndPosition();
				
				usedWords.add(w);
			}
			// finish last annotation
			if(st >= 0 && en >= 0){
				Annotation an = new Annotation();
				an.setSearchString(text);
				an.setConcept(c);
				an.setOffset(st);
				an.setText(text.substring(st,en));
				list.add(an);
			}
		}catch(Exception ex){
			System.err.println("match: "+c.getMatchedTerm()+" | name: "+c.getName()+" | code: "+c.getCode());
			System.err.println("annotations: "+Arrays.toString(c.getAnnotations()));
			System.err.println("search: "+c.getSearchString()+"\n");
			System.err.println("error: "+ex.getMessage()+"\n");
	
		}
		return list;
	}
	
}
