package edu.pitt.ontology.owl;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

import org.semanticweb.owlapi.model.OWLClass;
import org.semanticweb.owlapi.model.OWLDataProperty;
import org.semanticweb.owlapi.model.OWLDataPropertyExpression;
import org.semanticweb.owlapi.model.OWLIndividual;
import org.semanticweb.owlapi.model.OWLLiteral;
import org.semanticweb.owlapi.model.OWLNamedIndividual;
import org.semanticweb.owlapi.model.OWLObject;
import org.semanticweb.owlapi.model.OWLObjectPropertyExpression;
import org.semanticweb.owlapi.reasoner.NodeSet;

import edu.pitt.ontology.IClass;
import edu.pitt.ontology.IInstance;
import edu.pitt.ontology.IProperty;

public class OInstance extends OResource implements IInstance {
	private OWLIndividual individual;
	
	protected OInstance(OWLObject obj, OOntology ont) {
		super(obj,ont);
		individual = (OWLIndividual) obj;
	}


	public IProperty[] getProperties() {
		List<IProperty> props = new ArrayList<IProperty>();
		Collections.addAll(props,super.getProperties());
		for(OWLDataPropertyExpression e: getOWLIndividual().getDataPropertyValues(getDefiningOntology()).keySet()){
			props.add((IProperty)convertOWLObject(e));
		}
		for(OWLObjectPropertyExpression e: getOWLIndividual().getObjectPropertyValues(getDefiningOntology()).keySet()){
			props.add((IProperty)convertOWLObject(e));
		}
		return props.toArray(new IProperty [0]);
	}

	public Object getPropertyValue(IProperty prop) {
		Object [] o = getPropertyValues(prop);
		return o.length > 0?o[0]:null;
	}

	public Object[] getPropertyValues(IProperty prop) {
		if(prop.isAnnotationProperty())
			return super.getPropertyValues(prop);
		else if(prop.isDatatypeProperty()){
			List list = new ArrayList();
			for(OWLLiteral l: getOWLReasoner().getDataPropertyValues((OWLNamedIndividual)getOWLIndividual(),(OWLDataProperty)convertOntologyObject(prop))){
				list.add(convertOWLObject(l));
			}
			return list.toArray();
		}else if(prop.isObjectProperty()){
			List list = new ArrayList();
			for(OWLIndividual l: getOWLReasoner().getObjectPropertyValues((OWLNamedIndividual)getOWLIndividual(),
					(OWLObjectPropertyExpression)convertOntologyObject(prop)).getFlattened()){
				list.add(convertOWLObject(l));
			}
			return list.toArray();
		}
		return new Object [0];
	}

	@Override
	public void addPropertyValue(IProperty prop, Object value) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void setPropertyValue(IProperty prop, Object value) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void setPropertyValues(IProperty prop, Object[] values) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void removePropertyValues(IProperty prop) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void removePropertyValue(IProperty prop, Object value) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void removePropertyValues() {
		// TODO Auto-generated method stub
		
	}
	public boolean hasPropetyValue(IProperty p, Object value) {
		if(p.isAnnotationProperty())
			return super.hasPropetyValue(p, value);
		if(p.isDatatypeProperty())
			return getOWLIndividual().hasDataPropertyValue((OWLDataPropertyExpression)convertOntologyObject(p),
					(OWLLiteral)convertOntologyObject(value), getDefiningOntology());
		if(p.isObjectProperty())
			return getOWLIndividual().hasObjectPropertyValue((OWLObjectPropertyExpression)convertOntologyObject(p),
					(OWLIndividual)convertOntologyObject(value), getDefiningOntology());
		return false;
	}
	
	public void addType(IClass cls) {
		OWLClass pr = (OWLClass) convertOntologyObject(cls);
		addAxiom(getOWLDataFactory().getOWLClassAssertionAxiom(pr,individual));
	}
	
	public void removeType(IClass cls) {
		OWLClass pr = (OWLClass) convertOntologyObject(cls);
		removeAxiom(getOWLDataFactory().getOWLClassAssertionAxiom(pr,individual));
	}

	public IClass[] getTypes() {
		NodeSet<OWLClass> sub = getOWLReasoner().getTypes((OWLNamedIndividual)individual,false);
		return getClasses(sub.getFlattened());
	}

	public IClass[] getDirectTypes() {
		NodeSet<OWLClass> sub = getOWLReasoner().getTypes((OWLNamedIndividual)individual,true);
		return getClasses(sub.getFlattened());
	}

	public boolean hasType(IClass cls) {
		NodeSet<OWLClass> sub = getOWLReasoner().getTypes((OWLNamedIndividual)individual,false);
		//return hasClass(sub.getFlattened(),(OWLClass)convertOntologyObject(cls));
		//TODO:
		return false;
	}


	public OWLIndividual getOWLIndividual() {
		return individual;
	}

}
