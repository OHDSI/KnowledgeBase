package edu.pitt.ontology.owl;

import java.util.Collection;

import edu.pitt.ontology.DefaultResourceIterator;
import edu.pitt.ontology.IResource;


public class OResourceIterator extends DefaultResourceIterator{
	private OOntology ont;
	
	
	public OResourceIterator(Collection list ,OOntology ont){
		super(list.iterator());
		this.ont =  ont;
	}
	
	public Object next(){
		Object obj = null;
		do{
			obj = ont.convertOntologyObject(super.next());
			count --; // super.next() increments it, we need to decrement it
		}while(obj instanceof IResource && ((IResource)obj).isSystem());
		count ++;
		return obj;
	}

}
