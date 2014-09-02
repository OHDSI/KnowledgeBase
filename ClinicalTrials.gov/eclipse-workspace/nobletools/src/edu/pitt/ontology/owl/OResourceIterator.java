package edu.pitt.ontology.owl;

import java.util.Collection;
import java.util.Collections;
import java.util.Iterator;

import org.semanticweb.owlapi.model.OWLEntity;
import org.semanticweb.owlapi.model.OWLObject;

import edu.pitt.ontology.DefaultResourceIterator;
import edu.pitt.ontology.IOntology;
import edu.pitt.ontology.IResource;
import edu.pitt.ontology.IResourceIterator;


public class OResourceIterator extends DefaultResourceIterator{
	private OOntology ont;
	
	
	public OResourceIterator(Collection list ,OOntology ont){
		super(list.iterator());
		this.ont =  ont;
	}
	
	public Object next(){
		Object obj = null;
		do{
			obj = ont.convertOWLObject((OWLEntity)super.next());
			count --; // super.next() increments it, we need to decrement it
		}while(obj instanceof IResource && ((IResource)obj).isSystem());
		count ++;
		return obj;
	}

}
