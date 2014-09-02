package edu.pitt.ontology.owl;

import java.util.ArrayList;
import java.util.List;

import org.semanticweb.owlapi.model.*;
import org.semanticweb.owlapi.reasoner.NodeSet;

import edu.pitt.ontology.IClass;
import edu.pitt.ontology.IOntologyError;
import edu.pitt.ontology.IProperty;
import edu.pitt.ontology.IResource;

public class OProperty extends OResource implements IProperty {
	private OWLPropertyExpression property;
	
	protected OProperty(OWLPropertyExpression obj,OOntology ont) {
		super(obj,ont);
		property = obj;
	}

	public OWLProperty getOWLProperty(){
		return (OWLProperty) property;
	}
	
	OWLDataProperty asOWLDataProperty(){
		return (OWLDataProperty)property;
	}
	OWLObjectProperty asOWLObjectProperty(){
		return (OWLObjectProperty)property;
	}
	
	public IProperty createSubProperty(String name) {
		OWLDataFactory dataFactory = getOWLDataFactory();
		if(isDatatypeProperty()){
			OWLDataProperty ch = dataFactory.getOWLDataProperty(IRI.create(getOntology().getNameSpace()+name));
			addAxiom(getOWLDataFactory().getOWLSubDataPropertyOfAxiom(ch,asOWLDataProperty()));
			return (IProperty) convertOWLObject(ch);
		}else{
			OWLObjectProperty ch = dataFactory.getOWLObjectProperty(IRI.create(getOntology().getNameSpace()+name));
			addAxiom(getOWLDataFactory().getOWLSubObjectPropertyOfAxiom(ch,asOWLObjectProperty()));
			return (IProperty) convertOWLObject(ch);
		}
		
	}

	public int getPropertyType() {
		return isDatatypeProperty()?IProperty.DATATYPE:IProperty.OBJECT;
	}

	public boolean isDatatypeProperty() {
		return getOWLProperty().isOWLDataProperty();
	}

	public boolean isObjectProperty() {
		return getOWLProperty().isOWLObjectProperty();
	}

	public boolean isAnnotationProperty() {
		return false;
	}

	public IClass[] getDomain() {
		if(isObjectProperty()){
			NodeSet<OWLClass> sub = getOWLReasoner().getObjectPropertyDomains(asOWLObjectProperty(),false);
			return getClasses(sub.getFlattened());
		}else{
			NodeSet<OWLClass> sub = getOWLReasoner().getDataPropertyDomains(asOWLDataProperty(),false);
			return getClasses(sub.getFlattened());
		}
	}

	public Object[] getRange() {
		if(isObjectProperty()){
			NodeSet<OWLClass> sub = getOWLReasoner().getObjectPropertyRanges(asOWLObjectProperty(),false);
			return getClasses(sub.getFlattened());
		}else{
			List lst = new ArrayList();
			for(OWLDataRange r: asOWLDataProperty().getRanges(getDefiningOntologies())){
				lst.add(convertOWLObject(r));
			}
			return lst.toArray();
		}
	}

	public void setDomain(IResource[] domain) {
		if(isObjectProperty()){
			for(OWLClass c: getOWLReasoner().getObjectPropertyDomains(asOWLObjectProperty(),false).getFlattened())
				removeAxiom(getOWLDataFactory().getOWLObjectPropertyDomainAxiom(asOWLObjectProperty(),c));
			for(IResource r: domain)
				addAxiom(getOWLDataFactory().getOWLObjectPropertyDomainAxiom(asOWLObjectProperty(),(OWLClassExpression)convertOntologyObject(r)));
		}else{
			for(OWLClass c: getOWLReasoner().getDataPropertyDomains(asOWLDataProperty(),false).getFlattened())
				removeAxiom(getOWLDataFactory().getOWLDataPropertyDomainAxiom(asOWLDataProperty(),c));
			for(IResource r: domain)
				addAxiom(getOWLDataFactory().getOWLDataPropertyDomainAxiom(asOWLDataProperty(),(OWLClassExpression)convertOntologyObject(r)));
		}

	}

	public void setRange(Object[] range) {
		if(isObjectProperty()){
			for(OWLClass c: getOWLReasoner().getObjectPropertyRanges(asOWLObjectProperty(),false).getFlattened())
				removeAxiom(getOWLDataFactory().getOWLObjectPropertyRangeAxiom(asOWLObjectProperty(),c));
			for(Object o: range)
				addAxiom(getOWLDataFactory().getOWLObjectPropertyRangeAxiom(asOWLObjectProperty(),(OWLClassExpression) convertOntologyObject(o)));
		}else{
			for(OWLDataRange r: asOWLDataProperty().getRanges(getDefiningOntologies()))
				removeAxiom(getOWLDataFactory().getOWLDataPropertyRangeAxiom(asOWLDataProperty(),((OWLLiteral)convertOntologyObject(r)).getDatatype()));
			for(Object o: range)
				addAxiom(getOWLDataFactory().getOWLDataPropertyRangeAxiom(asOWLDataProperty(),((OWLLiteral)convertOntologyObject(o)).getDatatype()));
		}
	}

	public boolean isInverseOf(IProperty p) {
		IProperty i = getInverseProperty();
		return (i != null)?i.equals(p):false;
	}

	public boolean isTransitive() {
		if(isObjectProperty())
			return asOWLObjectProperty().isTransitive(getDefiningOntologies());
		return false;
	}

	public boolean isFunctional() {
		return property.isFunctional(getDefiningOntology());
	}

	public boolean isSymmetric() {
		if(isObjectProperty())
			return asOWLObjectProperty().isSymmetric(getDefiningOntologies());
		return false;
	}

	public IProperty[] getSubProperties() {
		if(isDatatypeProperty()){
			return getProperties(getOWLReasoner().
					getSubDataProperties(asOWLDataProperty(),false).getFlattened());
		}else{
			return getProperties(getOWLReasoner().
					getSubObjectProperties(asOWLObjectProperty(),false).getFlattened());
		}
	}

	public IProperty[] getSuperProperties() {
		if(isDatatypeProperty()){
			return getProperties(getOWLReasoner().
					getSubDataProperties(asOWLDataProperty(),false).getFlattened());
		}else{
			return getProperties(getOWLReasoner().
					getSubObjectProperties(asOWLObjectProperty(),false).getFlattened());
		}
	}

	public IProperty[] getDirectSubProperties() {
		if(isDatatypeProperty()){
			return getProperties(getOWLReasoner().
					getSubDataProperties(asOWLDataProperty(),true).getFlattened());
		}else{
			return getProperties(getOWLReasoner().
					getSubObjectProperties(asOWLObjectProperty(),true).getFlattened());
		}
	}

	public IProperty[] getDirectSuperProperties() {
		if(isDatatypeProperty()){
			return getProperties(getOWLReasoner().
					getSuperDataProperties(asOWLDataProperty(),true).getFlattened());
		}else{
			return getProperties(getOWLReasoner().
					getSuperObjectProperties(asOWLObjectProperty(),true).getFlattened());
		}
	}

	public IProperty getInverseProperty() {
		if(isObjectProperty())
			return (IProperty) convertOWLObject(asOWLObjectProperty().getInverseProperty());
		return null;
	}

	public void setInverseProperty(IProperty p) {
		if(isObjectProperty() && p.isObjectProperty()){
			addAxiom(getOWLDataFactory().
					getOWLInverseObjectPropertiesAxiom(asOWLObjectProperty(),
							(OWLObjectProperty)convertOntologyObject(p)));
		}else{
			throw new IOntologyError("Can't set inverse property for non object properties");
		}
	}

	public void addSuperProperty(IProperty p) {
		if(p.getPropertyType() != getPropertyType())
			throw new IOntologyError("Can't add super property of different type");
		if(isDatatypeProperty()){
			OWLDataProperty ch = (OWLDataProperty) convertOntologyObject(p);
			addAxiom(getOWLDataFactory().getOWLSubDataPropertyOfAxiom(asOWLDataProperty(),ch));
		}else{
			OWLObjectProperty ch = (OWLObjectProperty) convertOntologyObject(p);
			addAxiom(getOWLDataFactory().getOWLSubObjectPropertyOfAxiom(asOWLObjectProperty(),ch));
		}
	}

	public void addSubProperty(IProperty p) {
		if(p.getPropertyType() != getPropertyType())
			throw new IOntologyError("Can't add sub property of different type");
		if(isDatatypeProperty()){
			OWLDataProperty ch = (OWLDataProperty) convertOntologyObject(p);
			addAxiom(getOWLDataFactory().getOWLSubDataPropertyOfAxiom(ch,asOWLDataProperty()));
		}else{
			OWLObjectProperty ch = (OWLObjectProperty) convertOntologyObject(p);
			addAxiom(getOWLDataFactory().getOWLSubObjectPropertyOfAxiom(ch,asOWLObjectProperty()));
		}
	}

	public void removeSuperProperty(IProperty p) {
		if(p.getPropertyType() != getPropertyType())
			throw new IOntologyError("Can't add super property of different type");
		if(isDatatypeProperty()){
			OWLDataProperty ch = (OWLDataProperty) convertOntologyObject(p);
			removeAxiom(getOWLDataFactory().getOWLSubDataPropertyOfAxiom(asOWLDataProperty(),ch));
		}else{
			OWLObjectProperty ch = (OWLObjectProperty) convertOntologyObject(p);
			removeAxiom(getOWLDataFactory().getOWLSubObjectPropertyOfAxiom(asOWLObjectProperty(),ch));
		}
	}
	
	public void removeSubProperty(IProperty p) {
		if(p.getPropertyType() != getPropertyType())
			throw new IOntologyError("Can't add sub property of different type");
		if(isDatatypeProperty()){
			OWLDataProperty ch = (OWLDataProperty) convertOntologyObject(p);
			removeAxiom(getOWLDataFactory().getOWLSubDataPropertyOfAxiom(ch,asOWLDataProperty()));
		}else{
			OWLObjectProperty ch = (OWLObjectProperty) convertOntologyObject(p);
			removeAxiom(getOWLDataFactory().getOWLSubObjectPropertyOfAxiom(ch,asOWLObjectProperty()));
		}

	}

	public void setTransitive(boolean b) {
		if(isObjectProperty()){
			OWLAxiom a = getOWLDataFactory().getOWLTransitiveObjectPropertyAxiom(asOWLObjectProperty()); 
			if(b)
				addAxiom(a);
			else
				removeAxiom(a);
		}else{
			throw new IOntologyError("Can't set non-object property as transitive");
		}
	}

	public void setFunctional(boolean b) {
		if(isObjectProperty()){
			OWLAxiom a = getOWLDataFactory().getOWLFunctionalObjectPropertyAxiom(asOWLObjectProperty());
			if(b)
				addAxiom(a);
			else
				removeAxiom(a);
		}else{
			OWLAxiom a = getOWLDataFactory().getOWLFunctionalDataPropertyAxiom(asOWLDataProperty());
			if(b)
				addAxiom(a);
			else
				removeAxiom(a);
		}
	}

	public void setSymmetric(boolean b) {
		if(isObjectProperty()){
			OWLAxiom a = getOWLDataFactory().getOWLSymmetricObjectPropertyAxiom(asOWLObjectProperty());
			if(b)
				addAxiom(a);
			else
				removeAxiom(a);
		}else{
			throw new IOntologyError("Can't set non-object property as symmetric");
		}
	}

}
