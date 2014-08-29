package edu.pitt.ontology.owl;

import java.net.URI;
import java.util.ArrayList;
import java.util.Collection;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Properties;
import java.util.Set;

import org.semanticweb.owlapi.model.*;
import org.semanticweb.owlapi.reasoner.OWLReasoner;
import org.semanticweb.owlapi.util.OWLEntityRemover;
import org.semanticweb.owlapi.util.OWLEntityRenamer;
import edu.pitt.ontology.IClass;
import edu.pitt.ontology.IInstance;
import edu.pitt.ontology.ILogicExpression;
import edu.pitt.ontology.IOntologyError;
import edu.pitt.ontology.IProperty;
import edu.pitt.ontology.IResource;
import edu.pitt.ontology.LogicExpression;



public class OResource implements IResource{
	private OOntology ontology;
	protected OWLObject obj;
	protected Properties info;
	
	
	protected OResource(OWLObject obj){
		this.obj = obj;
	}
	protected OResource(OWLObject obj,OOntology ont){
		this.obj = obj;
		this.ontology = ont;
	}
	
	public void setOntology(OOntology ont){
		ontology = ont;
	}
	
	public String getFormat() {
		OWLOntology o = getOWLOntology();
		if(o != null)
			return o.getOWLOntologyManager().getOntologyFormat(o).toString();
		return null;
	}

	public String getLocation() {
		return getIRI().toString();
	}
	public int compareTo(IResource o) {
		return getURI().compareTo(o.getURI());
	}

	public String getDescription() {
		return getComments().length > 0?getComments()[0]:null;
	}

	public void setDescription(String text) {
		addComment(text);
	}

	public String getName() {
		return getIRI().getFragment();
	}

	public String toString(){
		return getName();
	}

	public void dispose() {
		obj = null;
		info = null;
		ontology = null;
	}

	public String getVersion() {
		String [] v = getAnnotations(getOWLDataFactory().getOWLVersionInfo()).toArray(new String [0]);
		return v.length > 0?v[0]:null;
	}
	public URI getURI() {
		return getIRI().toURI();
	}

	public String getNameSpace() {
		return getIRI().getNamespace();
	}

	public String getPrefix() {
		PrefixManager pm = ((OOntology)getOntology()).getPrefixManager(); 
		Map<String,String> map = pm.getPrefixName2PrefixMap();
		for(String prefix: map.keySet()){
			if(getNameSpace().equals(map.get(prefix)))
				return prefix;
		}
		return ":";
	}

	public IProperty[] getProperties() {
		OWLEntity e = asOWLEntity();
		if(e != null){
			Set<IProperty> list = new LinkedHashSet<IProperty>();
			for(OWLAnnotation a: e.getAnnotations(getDefiningOntology())){
				list.add((IProperty)convertOWLObject(a.getProperty()));
			}
			return list.toArray(new IProperty [0]);
		}
		return new IProperty [0];
	}

	public Object getPropertyValue(IProperty prop) {
		Object [] a = getPropertyValues(prop);
		return a.length > 0?a[0]:new Object [0];
	}

	public Object[] getPropertyValues(IProperty prop) {
		OWLEntity e = asOWLEntity();
		if(e != null){
			Set list = new LinkedHashSet();
			for(OWLAnnotation a: e.getAnnotations(getDefiningOntology(),(OWLAnnotationProperty)convertOntologyObject(prop))){
				list.add(convertOWLObject(a.getValue()));
			}
			return list.toArray();
		}
		return new Object [0];
	}

	public void addPropertyValue(IProperty prop, Object value) {
		if(prop.isAnnotationProperty()){
			addAxiom(getAnnotationAxiom((OWLAnnotationProperty)convertOntologyObject(prop),(OWLAnnotationValue)convertOntologyObject(value)));
		}else
			throw new IOntologyError("Not implemented for "+getClass().getName());
	}

	public void setPropertyValue(IProperty prop, Object value) {
		if(prop.isAnnotationProperty()){
			removePropertyValues(prop);
			addPropertyValue(prop, value);
		}else
			throw new IOntologyError("Not implemented for "+getClass().getName());
	}

	public void setPropertyValues(IProperty prop, Object[] values) {
		if(prop.isAnnotationProperty()){
			removePropertyValues(prop);
			for(Object o: values){
				addPropertyValue(prop,o);
			}
		}else
			throw new IOntologyError("Not implemented for "+getClass().getName());
	}
	
	public void removePropertyValues(IProperty prop) {
		OWLEntity e = asOWLEntity();
		if(e != null){
			for(OWLAnnotation a: e.getAnnotations(getDefiningOntology())){
				if(prop.equals(convertOWLObject(a.getProperty()))){
					removeAxiom(getAnnotationAxiom(a.getProperty(),a.getValue()));
				}
				
			}
		}
	}
	public void removePropertyValue(IProperty prop, Object value) {
		if(prop.isAnnotationProperty()){
			removeAxiom(getAnnotationAxiom((OWLAnnotationProperty)convertOntologyObject(prop),(OWLAnnotationValue)convertOntologyObject(value)));
		}
	}
	
	public void removePropertyValues() {
		OWLEntity e = asOWLEntity();
		if(e != null){
			for(OWLAnnotation a: e.getAnnotations(getDefiningOntology())){
				removeAxiom(getAnnotationAxiom(a.getProperty(),a.getValue()));
			}
		}
	}
	
	public boolean hasPropetyValue(IProperty p, Object value) {
		OWLEntity e = asOWLEntity();
		if(e != null){
			for(OWLAnnotation a: e.getAnnotations(getDefiningOntology())){
				if(p.equals(convertOWLObject(a.getProperty())) && 
				   value.equals(convertOWLObject(a.getValue()))){
					return true;
				}
			}
		}
		return false;
	}

	public void addLabel(String label) {
		List<String> labels = getAnnotations(getOWLDataFactory().getRDFSLabel());
		if(!labels.contains(label)){
			addAnnotation(getOWLDataFactory().getRDFSLabel(),label);
		}
	}

	public void addComment(String comment) {
		List<String> labels = getAnnotations(getOWLDataFactory().getRDFSComment());
		if(!labels.contains(comment)){
			addAnnotation(getOWLDataFactory().getRDFSComment(),comment);
		}
	}

	public void removeLabel(String label) {
		List<String> labels = getAnnotations(getOWLDataFactory().getRDFSLabel());
		if(labels.contains(label)){
			removeAnnotation(getOWLDataFactory().getRDFSLabel(),label);
		}
		
	}
	public void removeComment(String comment) {
		List<String> labels = getAnnotations(getOWLDataFactory().getRDFSComment());
		if(labels.contains(comment)){
			removeAnnotation(getOWLDataFactory().getRDFSComment(),comment);
		}
	}

	public void addVersion(String version) {
		List<String> labels = getAnnotations(getOWLDataFactory().getOWLVersionInfo());
		if(!labels.contains(version)){
			addAnnotation(getOWLDataFactory().getOWLVersionInfo(),version);
		}
	}
	public void removeVersion(String version) {
		List<String> labels = getAnnotations(getOWLDataFactory().getOWLVersionInfo());
		if(labels.contains(version)){
			removeAnnotation(getOWLDataFactory().getOWLVersionInfo(),version);
		}
	}

	public String[] getLabels() {
		return getAnnotations(getOWLDataFactory().getRDFSLabel()).toArray(new String [0]);
	}

	public String[] getComments() {
		return getAnnotations(getOWLDataFactory().getRDFSComment()).toArray(new String [0]);
	}
	
	
	/**
	 * get annotations associated with a given entry
	 * @param prop
	 * @return
	 */
	private List<String> getAnnotations(OWLAnnotationProperty prop){
		List<String> list = new ArrayList<String>();
		OWLEntity entity = asOWLEntity();
		if(entity != null){
			for(OWLAnnotation a: entity.getAnnotations(getDefiningOntology(),prop)){
				list.add((String)convertOWLObject(a.getValue()));
		    }
		}else if(obj instanceof OWLOntology){
			for(OWLAnnotation a: getOWLOntology().getAnnotations()){
				if(a.getProperty().equals(prop))
					list.add((String)convertOWLObject(a.getValue()));
		    }
		}
		return list;
	}
	
	
	/**
	 * get defining ontology for this attribute
	 * @return
	 */
	protected OWLOntology getDefiningOntology(){
		OWLEntity e = asOWLEntity();
		OWLOntology o = null;
		if(e != null){
			OWLOntologyManager man = getOWLOntologyManager();
			String s = getNameSpace();
			if(s.endsWith("#"))
				s = s.substring(0,s.length()-1);
			o =  man.getOntology(IRI.create(s));
		}
		return o != null?o:getOWLOntology();
	}
	
	protected Set<OWLOntology> getDefiningOntologies(){
		return getOWLOntologyManager().getOntologies();
	}

	
	public boolean isSystem() {
		OWLEntity o = asOWLEntity();
		return (o != null)?o.isBuiltIn():false;
	}

	public OOntology getOntology() {
		return ontology;
	}

	public void delete() {
		if(obj instanceof OWLEntity){
			OWLEntityRemover remover = getOWLEntityRemover();
			((OWLEntity)obj).accept(remover);
			getOWLOntologyManager().applyChanges(remover.getChanges());
	        remover.reset();
		}
	}

	public void setName(String name) {
		if(obj instanceof OWLEntity){
			OWLEntityRenamer renamer = getOWLEntityRenamer();
			IRI newIRI = IRI.create(getNameSpace()+name);
			List<OWLOntologyChange> changes = renamer.changeIRI((OWLEntity)obj,newIRI);
			getOWLOntologyManager().applyChanges(changes);
	 	}
	}
	public ILogicExpression getLogicExpression() {
		return new LogicExpression(this);
	}

	public Properties getResourceProperties() {
		if(info == null)
			info = new Properties();
		return info;
	}

	protected OWLObject getOWLObject(){
		return obj;
	}
	protected IRI getIRI(){
		if(obj instanceof OWLOntology)
			return ((OWLOntology)obj).getOntologyID().getOntologyIRI();
		else if(obj instanceof OWLNamedObject)
			return ((OWLNamedObject)obj).getIRI();
		return null;
	}
	protected OWLEntity asOWLEntity(){
		if(obj instanceof OWLEntity)
			return (OWLEntity) obj;
		return null;
	}

	
	private void addAnnotation(OWLAnnotationProperty prop,String str){
		OWLDataFactory df = getOWLDataFactory();
		addAxiom(getAnnotationAxiom(prop, df.getOWLLiteral(str)));
	}
	
	private void removeAnnotation(OWLAnnotationProperty prop,String str){
		OWLDataFactory df = getOWLDataFactory();
		removeAxiom(getAnnotationAxiom(prop, df.getOWLLiteral(str)));
	}
	
	/**
	 * get annotation axiom
	 * @param prop
	 * @param val
	 * @return
	 */
	private OWLAxiom getAnnotationAxiom(OWLAnnotationProperty prop,OWLAnnotationValue val){
		OWLDataFactory df = getOWLDataFactory();
		OWLAnnotation commentAnno = df.getOWLAnnotation(prop,val);
		return df.getOWLAnnotationAssertionAxiom(getIRI(),commentAnno);
	}
	
	/**
	 * get annotation value as java object
	 * @param val
	 * @return
	 */
	protected Object convertOWLObject(OWLObject val){
		if(val == null)
			return null;
		
		if(val instanceof OWLLiteral){
			OWLLiteral l = (OWLLiteral) val;
			if(l.isInteger())
				return l.parseInteger();
			if(l.isBoolean())
				return l.parseBoolean();
			if(l.isDouble())
				return l.parseDouble();
			if(l.isFloat())
				return l.parseFloat();
			//if(l.getDatatype().equals(OWL2Datatype.XSD_DATE_TIME))
			//	return l.
			return l.getLiteral();
		}else if (val instanceof OWLClass){
			return new OClass((OWLClass)val,getOntology());
		}else if (val instanceof OWLIndividual){
			return new OInstance((OWLIndividual)val,getOntology());
		}else if (val instanceof OWLAnnotationProperty){
			return new OAnnotation((OWLAnnotationProperty)val,getOntology());
		}else if (val instanceof OWLPropertyExpression){
			return new OProperty((OWLPropertyExpression)val,getOntology());
		}else if (val instanceof OWLDataRange){
			OWLDataRange l = (OWLDataRange) val;
			if(l.isDatatype()){
				if(l.asOWLDatatype().isBoolean()){
					return Boolean.FALSE;
				}else if(l.asOWLDatatype().isInteger()){
					return new Integer(0);
				}else if(l.asOWLDatatype().isDouble()){
					return new Double(0);
				}else if(l.asOWLDatatype().isFloat()){
					return new Float(0);
				}else{
					return new String("string");
				}
			}
		}else if(val instanceof OWLNaryBooleanClassExpression){
			LogicExpression exp = new LogicExpression(LogicExpression.EMPTY);
			if(val instanceof OWLObjectIntersectionOf || val instanceof OWLDataIntersectionOf)
				exp.setExpressionType(ILogicExpression.AND);
			else if(val instanceof OWLObjectUnionOf || val instanceof OWLDataUnionOf)
				exp.setExpressionType(ILogicExpression.OR);
			for(OWLClassExpression e: ((OWLNaryBooleanClassExpression)val).getOperands()){
				exp.add(convertOWLObject(e));
			}
			return exp;
		}else if(val instanceof OWLObjectComplementOf){
			LogicExpression exp = new LogicExpression(LogicExpression.NOT);
			exp.add(convertOWLObject(((OWLObjectComplementOf) val).getOperand()));
			return exp;
		}else if(val instanceof OWLRestriction){
			return new ORestriction((OWLRestriction)val,getOntology());
		}
		
		return null;
	}
	
	/**
	 * convert Ontology object back to OWL-API
	 * @param val
	 * @return
	 */
	protected Object convertOntologyObject(Object val){
		if(val == null)
			return null;
		
		OWLDataFactory df = getOWLDataFactory();
		// Ontology Objects
		if(val instanceof OClass)
			return ((OClass) val).getOWLClass();
		if(val instanceof OInstance)
			return ((OInstance) val).getOWLIndividual();
		if(val instanceof OAnnotation)
			return ((OAnnotation) val).getOWLAnnotationProperty();
		if(val instanceof OProperty)
			return ((OProperty) val).getOWLProperty();
		
		// data types
		if(val instanceof String)
			return df.getOWLLiteral((String) val);
		if(val instanceof Double)
			return df.getOWLLiteral((Double) val);
		if(val instanceof Float)
			return df.getOWLLiteral((Float) val);
		if(val instanceof Integer )
			return df.getOWLLiteral((Integer) val);
		if(val instanceof Boolean )
			return df.getOWLLiteral((Boolean) val);
		if(val instanceof ILogicExpression){
			ILogicExpression exp = (ILogicExpression) val;
			if(exp.isEmpty())
				return null;
			Object obj = convertOntologyObject(exp.get(0));
			switch(exp.getExpressionType()){
			case ILogicExpression.EMPTY:
				return obj;
			case ILogicExpression.NOT:
				if(obj instanceof OWLLiteral)
					return df.getOWLDataComplementOf(((OWLLiteral)obj).getDatatype());
				else if(obj instanceof OWLClassExpression )
					return df.getOWLObjectComplementOf((OWLClassExpression)obj);
			case ILogicExpression.AND:
				if(obj instanceof OWLLiteral){
					Set<OWLDataRange> dataRanges = new LinkedHashSet<OWLDataRange>();
					for(Object o: exp){
						dataRanges.add(((OWLLiteral)convertOntologyObject(o)).getDatatype());
					}
					return df.getOWLDataIntersectionOf(dataRanges);
				}else if(obj instanceof OWLClassExpression ){
					Set<OWLClassExpression> dataRanges = new LinkedHashSet<OWLClassExpression>();
					for(Object o: exp){
						dataRanges.add((OWLClassExpression)convertOntologyObject(o));
					}
					return df.getOWLObjectIntersectionOf(dataRanges);
				}
			case ILogicExpression.OR:
				if(obj instanceof OWLLiteral){
					Set<OWLDataRange> dataRanges = new LinkedHashSet<OWLDataRange>();
					for(Object o: exp){
						dataRanges.add(((OWLLiteral)convertOntologyObject(o)).getDatatype());
					}
					return df.getOWLDataUnionOf(dataRanges);
				}else if(obj instanceof OWLClassExpression ){
					Set<OWLClassExpression> dataRanges = new LinkedHashSet<OWLClassExpression>();
					for(Object o: exp){
						dataRanges.add((OWLClassExpression)convertOntologyObject(o));
					}
					return df.getOWLObjectUnionOf(dataRanges);
				}
			}
		}
		return null;
	}
	
	
	/**
	 * method to get super/sub direct/all classes
	 * @param parent
	 * @param direct
	 * @return
	 */
	protected IClass [] getClasses(Collection<OWLClass> list){
		Set<IClass> c = new LinkedHashSet<IClass>();
		for(OWLClass child: list){
			if(!(child.isAnonymous() || child.isBottomEntity()))
				c.add((IClass) convertOWLObject(child));
		}
		return (IClass []) c.toArray(new IClass [0]);
	}
	
	protected IProperty [] getProperties(Collection list){
		List<IProperty> props = new ArrayList<IProperty>();
		for(Object p: list){
			if(p instanceof OWLEntity){
				OWLEntity e = (OWLEntity) p;
				if(!e.isBottomEntity() && !e.isTopEntity())
					props.add((IProperty)convertOWLObject(e));
			}
		}
		return props.toArray(new IProperty [0]);
	}
	
	/**
	 * method to get super/sub direct/all classes
	 * @param parent
	 * @param direct
	 * @return
	 */
	protected IInstance [] getInstances(Collection<OWLNamedIndividual> list){
		Set<IInstance> c = new LinkedHashSet<IInstance>();
		for(OWLNamedIndividual child: list){
			if(!(child.isAnonymous() || child.isBottomEntity()))
				c.add((IInstance) convertOWLObject(child));
		}
		return (IInstance []) c.toArray(new IInstance [0]);
	}
	
	protected void addAxiom(OWLAxiom ax){
		getOWLOntologyManager().addAxiom(getOWLOntology(),ax);
	}
	
	protected void removeAxiom(OWLAxiom ax){
		getOWLOntologyManager().removeAxiom(getOWLOntology(),ax);
	}

	protected OWLOntology getOWLOntology(){
		return getOntology().getOWLOntology();
	}
	
	protected OWLDataFactory getOWLDataFactory(){
		return getOntology().getOWLDataFactory();
	}
	
	protected OWLOntologyManager getOWLOntologyManager(){
		return getOntology().getOWLOntologyManager();
	}
	
	protected OWLReasoner getOWLReasoner(){
		return getOntology().getOWLReasoner();
	}
	protected OWLEntityRemover getOWLEntityRemover(){
		return getOntology().getOWLEntityRemover();
	}
	protected OWLEntityRenamer getOWLEntityRenamer(){
		return getOntology().getOWLEntityRenamer();
	}
}
