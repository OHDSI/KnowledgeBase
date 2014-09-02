package edu.pitt.terminology.lexicon;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;

import javax.swing.tree.TreePath;

/**
 * describes a class path
 * @author tseytlin
 *
 */
public class ConceptPath extends ArrayList<Concept>{
	public ConceptPath(){
		super();
	}
	public ConceptPath(Collection<Concept> c){
		super(c);
	}
	public ConceptPath(Concept c){
		super(Collections.singletonList(c));
	}
	public TreePath toTreePath(){
		return new TreePath(toArray(new Concept [0]));
	}
	public String toString(){
		String s = super.toString();
		s = s.substring(1,s.length()-1);
		return s.replaceAll(","," ->");
	}
}
