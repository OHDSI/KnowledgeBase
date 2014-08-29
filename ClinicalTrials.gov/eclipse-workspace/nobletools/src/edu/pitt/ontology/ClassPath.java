package edu.pitt.ontology;

import java.util.ArrayList;
import java.util.Collection;

import javax.swing.tree.TreePath;

/**
 * describes a class path
 * @author tseytlin
 *
 */
public class ClassPath extends ArrayList<IClass>{
	public ClassPath(){
		super();
	}
	public ClassPath(Collection<IClass> c){
		super(c);
	}
	public TreePath toTreePath(){
		return new TreePath(toArray(new IClass [0]));
	}
	public String toString(){
		String s = super.toString();
		s = s.substring(1,s.length()-1);
		return s.replaceAll(","," ->");
	}
}
