package edu.pitt.ontology.protege;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Date;
import java.util.List;

import edu.pitt.ontology.IClass;
import edu.pitt.ontology.IOntology;
import edu.pitt.ontology.IProperty;
import edu.pitt.ontology.IResource;
import edu.stanford.smi.protegex.owl.model.OWLClass;
import edu.stanford.smi.protegex.owl.model.OWLDataRange;
import edu.stanford.smi.protegex.owl.model.OWLObjectProperty;
import edu.stanford.smi.protegex.owl.model.OWLProperty;
import edu.stanford.smi.protegex.owl.model.RDFProperty;
import edu.stanford.smi.protegex.owl.model.RDFResource;
import edu.stanford.smi.protegex.owl.model.RDFSDatatype;

public class PProperty extends PResource implements IProperty {
	private RDFProperty prop;
	
	public PProperty(RDFProperty p, IOntology o){
		super(p,o);
		this.prop = p;
	}
	

	/**
	 * create sub property
	 */
	public IProperty createSubProperty(String name){
		return new PProperty((RDFProperty)prop.getOWLModel().createSubproperty(name,prop),getOntology());
	}
	
	/**
	 * get property type
	 * OBJECT, DATATYPE, ANNOTATION_OBJECT, ANNOTATION_DATATYPE
	 * @return
	 */
	public int getPropertyType(){
		if(isAnnotationProperty()){
			if(isObjectProperty())
				return ANNOTATION_OBJECT;
			else
				return ANNOTATION_DATATYPE;
		}else{
			if(isObjectProperty())
				return OBJECT;
			else
				return DATATYPE;
		}
	}
	
	/**
	 * is property a datatype property
	 * @return
	 */
	public boolean isDatatypeProperty(){
		if(prop instanceof OWLProperty)
			return !((OWLProperty)prop).isObjectProperty();
		return false;
	}
	
	/**
	 * is property an object property
	 * @return
	 */
	public boolean isObjectProperty(){
		if(prop instanceof OWLProperty)
			return ((OWLProperty)prop).isObjectProperty();
		return false;
	}
	
	/**
	 * is property an annotation property
	 * @return
	 */
	public boolean isAnnotationProperty(){
		return prop.isAnnotationProperty();
	}
	
	/**
	 * get domain 
	 */
	public IClass [] getDomain() {
		Collection list = prop.getDomains(false);
		IClass [] c = new IClass [list.size()];
		int i=0;
		for(Object o: list){
			c[i++] = new PClass((OWLClass)o,getOntology());
		}
		return c;
	}

	/**
	 * get range
	 */
	public Object[] getRange() {
		if(prop.hasDatatypeRange()){
			RDFResource range = prop.getRange();
			Object [] obj = new Object [1];
			if(range instanceof RDFSDatatype) {
				obj[0] = ((RDFSDatatype) range).getDefaultValue();
			}else if (range instanceof OWLDataRange) {
				obj[0] = ((OWLDataRange) range).getOneOfValues();
			}else
				obj = new Object[0];
			return obj;
		}else{
			Collection list = prop.getRanges(false);
			Object [] c = new Object [list.size()];
			int i=0;
			for(Object o: list){
				c[i++] = new PClass((OWLClass)o,getOntology());
			}
			return c;
		}
	}

	/**
	 * set domain
	 */
	public void setDomain(IResource[] domain) {
		prop.setDomains(getResources(domain));
	}
	
	/**
	 * convert datatype to resource
	 * @param o
	 * @return
	 */
	private RDFResource getDatatype(Object o){
		if(o instanceof Boolean){
			return prop.getOWLModel().getXSDboolean();
		}else if(o instanceof Float){
			return prop.getOWLModel().getXSDfloat();
		}else if(o instanceof Integer){
			return prop.getOWLModel().getXSDint();
		}else if(o instanceof String){
			return prop.getOWLModel().getXSDstring();
		}else if(o instanceof Date){
			return prop.getOWLModel().getXSDdateTime();
		}else if(o instanceof Collection){
			//TODO:
		}
		return null;
	}
	
	public void setRange(Object [] range) {
		if(prop.hasDatatypeRange()){
			if(range.length > 0){
				prop.setRange(getDatatype(range[0]));
			}
		}else{
			prop.setRanges(getResources((IResource[])range));
		}
	}
	
	/**
	 * get inverse property
	 * @return
	 */
	public IProperty getInverseProperty(){
		if(prop instanceof OWLProperty){
			OWLProperty p = (OWLProperty)prop.getInverseProperty();
			return (p != null)?new PProperty(p,getOntology()):null;
		}
		return null;
	}
	
	
	public boolean isFunctional() {
		return prop.isFunctional();
	}

	public boolean isInverseOf(IProperty p) {
		return getInverseProperty().equals(p);
	}

	public boolean isSymmetric() {
		return (prop instanceof OWLObjectProperty)?((OWLObjectProperty)prop).isSymmetric():false;
	}

	public boolean isTransitive() {
		return (prop instanceof OWLObjectProperty)?((OWLObjectProperty)prop).isTransitive():false;
	}
	
	
	
	/**
	 * get list of resources
	 * @param r
	 * @return
	 */
	private Collection getResources(IResource [] r){
		List list = new ArrayList();
		for(int i=0;i<r.length;i++)
			list.add(((PResource)r[i]).getResource());
		return list;
	}
	
	
	/**
	 * get sub properties
	 * @return
	 */
	public IProperty [] getSubProperties(){
		return getProperties(prop.getSubproperties(true));
	}
	
	/**
	 * get super properties
	 * @return
	 */
	public IProperty [] getSuperProperties(){
		return getProperties(prop.getSuperproperties(true));
	}
	
	/**
	 * get sub properties
	 * @return
	 */
	public IProperty [] getDirectSubProperties(){
		return getProperties(prop.getSubproperties(false));	
	}
	
	/**
	 * get super properties
	 * @return
	 */
	public IProperty [] getDirectSuperProperties(){
		return getProperties(prop.getSuperproperties(false));
	}
	
	/**
	 * set inverse property
	 * @return
	 */
	public void setInverseProperty(IProperty p){
		if(p != null)
			prop.setInverseProperty((RDFProperty)convertSetValue(p));
	}
	
	/**
	 * add direct super property
	 * @param p
	 */
	public void addSuperProperty(IProperty p){
		prop.addSuperproperty((RDFProperty)convertSetValue(p));
	}
	
	/**
	 * add direct super property
	 * @param p
	 */
	public void addSubProperty(IProperty p){
		p.addSuperProperty(this);
	}
	
	/**
	 * remove super property
	 * @param p
	 */
	public void removeSuperProperty(IProperty p){
		prop.removeSuperproperty((RDFProperty)convertSetValue(p));
	}
	
	/**
	 * remove super property
	 * @param p
	 */
	public void removeSubProperty(IProperty p){
		p.removeSuperProperty(this);
	}
	
	/**
	 * set property transitive flag
	 */
	public void setTransitive(boolean b){
		if(prop instanceof OWLObjectProperty)
			((OWLObjectProperty)prop).setTransitive(b);
	}
	
	/**
	 * set property functional flag
	 */
	public void  setFunctional(boolean b){
		prop.setFunctional(b);
	}
	
	/**
	 * set property symmetrical flag
	 */
	public void setSymmetric(boolean b){
		if(prop instanceof OWLObjectProperty)
			((OWLObjectProperty)prop).setSymmetric(b);
	}
}
