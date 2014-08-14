package edu.pitt.ontology.protege;

import java.util.Iterator;

import edu.pitt.ontology.DefaultResourceIterator;
import edu.pitt.ontology.IOntology;
import edu.pitt.ontology.IResource;

public class PResourceIterator extends DefaultResourceIterator {
	private POntology ont;
	public PResourceIterator(Iterator it, IOntology ont){
		super(it);
		this.ont = (POntology) ont;
	}
	
	public Object next(){
		Object obj = null;
		do{
			obj = ont.convertGetValue(super.next());
			count --; // super.next() increments it, we need to decrement it
		}while(obj instanceof IResource && ((IResource)obj).isSystem());
		count ++;
		return obj;
	}
}
