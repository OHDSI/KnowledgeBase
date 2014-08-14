package edu.pitt.ontology.owl;

import java.util.LinkedHashSet;
import java.util.Set;

import org.semanticweb.owlapi.model.IRI;
import org.semanticweb.owlapi.model.OWLAnnotationProperty;
import org.semanticweb.owlapi.model.OWLDataFactory;

import edu.pitt.ontology.IClass;
import edu.pitt.ontology.IOntologyError;
import edu.pitt.ontology.IProperty;
import edu.pitt.ontology.IResource;

/**
 * represents annotation property
 * @author tseytlin
 *
 */
public class OAnnotation extends OResource implements IProperty {
	private OWLAnnotationProperty annotation;
	
	protected OAnnotation(OWLAnnotationProperty obj, OOntology ont) {
		super(obj, ont);
		annotation = obj;
	}

	public OWLAnnotationProperty getOWLAnnotationProperty(){
		return annotation;
	}

	
	public IProperty createSubProperty(String name) {
		OWLDataFactory dataFactory = getOWLDataFactory();
		OWLAnnotationProperty ch = dataFactory.getOWLAnnotationProperty(IRI.create(getNameSpace()+name));
		addAxiom(getOWLDataFactory().getOWLSubAnnotationPropertyOfAxiom(ch,annotation));
		return (IProperty) convertOWLObject(ch);
	}

	public int getPropertyType() {
		return IProperty.ANNOTATION_DATATYPE;
	}

	public boolean isDatatypeProperty() {
		return false;
	}

	public boolean isObjectProperty() {
		return false;
	}

	public boolean isAnnotationProperty() {
		return true;
	}

	public IClass[] getDomain() {
		return new IClass [0];
	}

	public Object[] getRange() {
		return new Object [0];
	}

	public void setDomain(IResource[] domain) {
		throw new IOntologyError("Not implemented");
	}

	public void setRange(Object[] range) {
		throw new IOntologyError("Not implemented");
	}

	public boolean isInverseOf(IProperty p) {
		return false;
	}

	public boolean isTransitive() {
		return false;
	}

	public boolean isFunctional() {
		return false;
	}

	public boolean isSymmetric() {
		return false;
	}

	public IProperty[] getSubProperties() {
		Set<IProperty> list = new LinkedHashSet<IProperty>();
		return getSubProperties(this, list).toArray(new IProperty [0]);
	}

	public IProperty[] getSuperProperties() {
		Set<IProperty> list = new LinkedHashSet<IProperty>();
		return getSuperProperties(this, list).toArray(new IProperty [0]);
	}

	private Set<IProperty> getSubProperties(IProperty p, Set<IProperty> list){
		for(IProperty c: p.getDirectSubProperties()){
			list.add(c);
			getSubProperties(c,list);
		}
		return list;
	}
	
	private Set<IProperty> getSuperProperties(IProperty p, Set<IProperty> list){
		for(IProperty c: p.getDirectSuperProperties()){
			list.add(c);
			getSuperProperties(c,list);
		}
		return list;
	}
	
	
	public IProperty[] getDirectSubProperties() {
		return getProperties(annotation.getSubProperties(getDefiningOntologies()));
	}

	public IProperty[] getDirectSuperProperties() {
		return getProperties(annotation.getSuperProperties(getDefiningOntologies()));
	}

	public IProperty getInverseProperty() {
		return null;
	}

	public void setInverseProperty(IProperty p) {
		throw new IOntologyError("Not implemented");
	}

	public void addSuperProperty(IProperty p) {
		if(!p.isAnnotationProperty())
			throw new IOntologyError("Can't add non-annotation superproperty");
		OWLAnnotationProperty ch = (OWLAnnotationProperty) convertOntologyObject(p);
		addAxiom(getOWLDataFactory().getOWLSubAnnotationPropertyOfAxiom(annotation,ch));
	}

	public void addSubProperty(IProperty p) {
		if(!p.isAnnotationProperty())
			throw new IOntologyError("Can't add non-annotation subproperty");
		OWLAnnotationProperty ch = (OWLAnnotationProperty) convertOntologyObject(p);
		addAxiom(getOWLDataFactory().getOWLSubAnnotationPropertyOfAxiom(ch,annotation));
	}

	public void removeSuperProperty(IProperty p) {
		if(!p.isAnnotationProperty())
			throw new IOntologyError("Can't remove non-annotation superproperty");
		OWLAnnotationProperty ch = (OWLAnnotationProperty) convertOntologyObject(p);
		removeAxiom(getOWLDataFactory().getOWLSubAnnotationPropertyOfAxiom(annotation,ch));
	}

	public void removeSubProperty(IProperty p) {
		if(!p.isAnnotationProperty())
			throw new IOntologyError("Can't remove non-annotation subproperty");
		OWLAnnotationProperty ch = (OWLAnnotationProperty) convertOntologyObject(p);
		removeAxiom(getOWLDataFactory().getOWLSubAnnotationPropertyOfAxiom(ch,annotation));
	}
	
	public void setTransitive(boolean b) {
		throw new IOntologyError("Not implemented");
	}

	public void setFunctional(boolean b) {
		throw new IOntologyError("Not implemented");
	}

	public void setSymmetric(boolean b) {
		throw new IOntologyError("Not implemented");
	}

}
