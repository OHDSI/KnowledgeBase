package edu.pitt.ontology.protege;

import java.lang.reflect.Array;
import java.net.URI;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Properties;
import java.util.Set;

import edu.pitt.ontology.IClass;
import edu.pitt.ontology.ILogicExpression;
import edu.pitt.ontology.IOntology;
import edu.pitt.ontology.IOntologyError;
import edu.pitt.ontology.IProperty;
import edu.pitt.ontology.IResource;
import edu.pitt.ontology.IRestriction;
import edu.pitt.ontology.LogicExpression;
import edu.stanford.smi.protegex.owl.model.OWLIndividual;
import edu.stanford.smi.protegex.owl.model.OWLIntersectionClass;
import edu.stanford.smi.protegex.owl.model.OWLLogicalClass;
import edu.stanford.smi.protegex.owl.model.OWLModel;
import edu.stanford.smi.protegex.owl.model.OWLProperty;
import edu.stanford.smi.protegex.owl.model.OWLRestriction;
import edu.stanford.smi.protegex.owl.model.OWLUnionClass;
import edu.stanford.smi.protegex.owl.model.RDFProperty;
import edu.stanford.smi.protegex.owl.model.RDFResource;
import edu.stanford.smi.protegex.owl.model.RDFSClass;
import edu.stanford.smi.protegex.owl.model.RDFSLiteral;
import edu.stanford.smi.protegex.owl.model.impl.DefaultRDFSLiteral;


public class PResource implements IResource {
	private URI uri;
	protected Properties info;
	protected RDFResource resource;
	protected POntology ontology;
	
	
	/**
	 * create new resource
	 * @param r
	 */
	public PResource(Properties info){
		this.info = info;
	}
	
	/**
	 * create new resource
	 * @param r
	 */
	public PResource(RDFResource r){
		this(r,null);
	}

	/**
	 * create new resource
	 * @param r
	 */
	public PResource(RDFResource r, IOntology o){
		this.resource = r;
		this.ontology = (POntology) o;
	}
	
	
	public void addComment(String comment) {
		if(resource == null && ontology != null)
			ontology.checkModel();
		resource.addComment(comment);
	}

	public void addLabel(String label) {
		if(resource == null && ontology != null)
			ontology.checkModel();
		
		resource.addLabel(label,null);
	}
	
	
	/**
	 * add label
	 * @param string
	 */
	public void removeLabel(String label){
		if(resource == null && ontology != null)
			ontology.checkModel();
		
		resource.removeLabel(label,null);
	}
	
	
	/**
	 * add comment
	 * @param string
	 */
	public void removeComment(String comment){
		if(resource == null && ontology != null)
			ontology.checkModel();
		
		resource.removeComment(comment);
	}

	
	/**
	 * add version
	 * @param string
	 */
	public void addVersion(String version){
		if(resource == null && ontology != null)
			ontology.checkModel();
		
		resource.addVersionInfo(version);
	}
	
	
	/**
	 * remove version
	 * @param string
	 */
	public void removeVersion(String version){
		if(resource == null && ontology != null)
			ontology.checkModel();
		
		resource.removeVersionInfo(version);
	}
	
	/**
	 * remove this resource
	 */
	public void delete(){
		if(resource == null && ontology != null)
			ontology.checkModel();
		//deleteReferences(resource);
		resource.delete();
	}
	
	/**
	 * delete references to resource
	 * @param res
	 *
	private void deleteReferences(RDFResource res){
		for(Iterator i=res.getOWLModel().listReferences(res,50);i.hasNext();){
			Tuple t = (Tuple) i.next();
			RDFResource r = t.getSubject();
			System.out.println("rem "+res+" "+r);
			if(r.isAnonymous()){
				deleteReferences(r);
				if(r instanceof OWLNAryLogicalClass && res instanceof RDFSClass){
					((OWLNAryLogicalClass)r).removeOperand((RDFSClass)res);
				}else{
					r.delete();
				}
			}
		}
	}
	*/
	
	
	public String[] getComments() {
		if(resource == null && ontology != null)
			ontology.checkModel();
		if(resource != null)
			return listToString(resource.getComments());
		return new String[0];
	}

	public String getDescription() {
		if(resource != null){
			Collection c = resource.getComments();
			return (c != null && c.size() > 0)?""+c.iterator().next():"";
		}else if(info != null){
			return ""+info.get("description");
		}
		return null;
	}

	public String[] getLabels() {
		// don't bother to load resource just for labels
		//if(resource == null && ontology != null)
		//	ontology.checkModel();
		if(resource != null){
			return listToString(resource.getLabels());
		}
		return new String [0];
		
	}
	
	/**
	 * convert list to string
	 * @param list
	 * @return
	 */
	private String [] listToString(Collection list){
		if(list != null && !list.isEmpty()){
			String [] str = new String [list.size()];
			int i= 0;
			for(Object obj : list){
				if(obj instanceof RDFSLiteral){
					str[i++] = ((RDFSLiteral) obj).getString();
				}else{
					str[i++] = ""+obj;
				}
			}
			return str;
		}
		return new String [0];
	}
	

	/*
	public String getName() {
		if(resource != null)
			return resource.getName();
		else if(info != null)
			return ""+info.get("name");
		return null;
	}*/
	
	public String getName() {
		if(resource != null && isAnonymous()){
			try{
				String t =  resource.getBrowserText();
				return (t != null)?t:resource.getName();
			}catch(Exception ex){
				System.err.println("ERROR: corrupted resources "+resource.getName()+" can't get BrowserText!");
				return resource.getName();
			}
		}
		String f = getURI().getFragment();
		// if there is no fragment, then we have a URI like http://purl.org/dc/elements/1.1/creator
		if(f == null){
			String s = ""+getURI();
			int i =  s.lastIndexOf("/");
			if(i > -1)
				return s.substring(i+1);
			return s;
		}
		return f;
	}

	
	public void setName(String name){
		if(resource != null){
			resource = (RDFResource) resource.rename(getNameSpace()+name);
			uri = null;
		}
	}
	
	public String getNameSpace() {
		//return resource.getNamespace();
		String uri = ""+getURI();
		int i = uri.lastIndexOf("#");
		return ((i > -1)?uri.substring(0,i):uri)+"#";
	}
	
	public boolean isAnonymous(){
		if(resource == null && ontology != null)
			ontology.checkModel();
		
		return resource.isAnonymous();
	}
	
	public String getPrefix() {
		if(resource == null && ontology != null)
			ontology.checkModel();
		
		String p = (resource != null)?resource.getNamespacePrefix():"";
		return (p == null || p.length() == 0)?"":p+":";
	}

	public IProperty[] getProperties() {
		if(resource == null && ontology != null)
			ontology.checkModel();
		
		List<IProperty> props = new ArrayList<IProperty>();
		//DIFFERENCE BETWEEN 3.3.1 and 3.4
		Collection list = resource.getRDFProperties();
		//Collection list = resource.getPossibleRDFProperties();
		for(Object o: list){
			if(!((RDFProperty)o).isSystem())// && 
				//resource.getPropertyValue((RDFProperty)o,true) != null)
				props.add(new PProperty((RDFProperty)o,getOntology()));
		}
		return (IProperty []) props.toArray(new IProperty [0]);
	}

	public Object getPropertyValue(IProperty prop) {
		if(resource == null && ontology != null)
			ontology.checkModel();
		
		// if property is null, well nothing to be done
		if(prop == null)
			return null;
		
		RDFProperty p = (RDFProperty) ((PProperty)prop).getResource();
		Object value = resource.getPropertyValue(p,true);
		
		// if there are implied values then replace the real ones
		// if implied are defaults
		if(value == null || value instanceof Number){
			if(value == null || ((Number)value).intValue() == 0){
				Collection col = resource.getHasValuesOnTypes(p);
				if(!col.isEmpty()){
					value = col.iterator().next();
				}
			}
		}
		// convert value
		return convertGetValue(value);
	}

	public Object[] getPropertyValues(IProperty prop) {
		if(resource == null && ontology != null)
			ontology.checkModel();
		
		// if property is null, well nothing to be done
		if(prop == null)
			return new Object [0];
		
		RDFProperty p = (RDFProperty) ((PProperty)prop).getResource();
		List list = new ArrayList();
		Collection own = (prop.isFunctional())?
						Collections.singletonList(resource.getPropertyValue(p,true)):
						resource.getPropertyValues(p,true);
		Collection impl = resource.getHasValuesOnTypes(p);
		
		// if own is composed of a default number 0.0
		// and there are implied values, then we can ignore it
		if(own.size() == 1){
			Object val = own.iterator().next();
			if(!(val instanceof Number && ((Number)val).intValue() == 0 && !impl.isEmpty())){
				list.addAll(own);
			}
		}else{
			// get own properties
			list.addAll(own);
		}
				
		// get "implied" properties
		if(list.isEmpty() || !prop.isFunctional())
			list.addAll(impl); 
		return convertGetValues(list);
		//return convertGetValues(resource.getOwnSlotValues(p));
	}

	public URI getURI() {
		if(uri == null){
			if(resource != null){
				uri = URI.create(resource.getURI());
			}else if(info != null){
				return URI.create(""+info.get("uri"));
			}
		}
		return uri;
	}

	public String getVersion() {
		if(resource != null){
			Collection c = resource.getVersionInfo();
			return (c != null && c.size() > 0)?""+c.iterator().next():"";
		}else if(info != null)
			return ""+info.get("version");
		return null;
	}

	public boolean hasPropetyValue(IProperty prop, Object value) {
		if(resource == null && ontology != null)
			ontology.checkModel();
		
		RDFProperty p = (RDFProperty) ((PProperty)prop).getResource();
		return resource.hasPropertyValue(p,convertSetValue(value),true);
	}

	public void removePropertyValues(IProperty prop) {
		if(resource == null && ontology != null)
			ontology.checkModel();
		
		RDFProperty p = (RDFProperty) ((PProperty)prop).getResource();
		for(Object o: resource.getPropertyValues(p))
			resource.removePropertyValue(p,o);
	}

	
	public void removePropertyValue(IProperty prop, Object value) {
		if(resource == null && ontology != null)
			ontology.checkModel();
		
		// if property is null, well nothing to be done
		if(prop == null)
			return;
		
		RDFProperty p = (RDFProperty) convertSetValue(prop);
		resource.removePropertyValue(p,convertSetValue(value));
	}

	
	/**
	 * remove all property values from resource
	 * @param prop
	 */
	public void removePropertyValues(){
		if(resource == null && ontology != null)
			ontology.checkModel();
			
		for(Object o: resource.getPossibleRDFProperties()){
			RDFProperty p = (RDFProperty) o;
			for(Object v: resource.getPropertyValues(p)){
				resource.removePropertyValue(p,v);
			}
		}
	}
	
	
	/**
	 * where there is equals, there is hashCode
	 */
	public int hashCode() {
		return getURI().hashCode();
	}
	
	public boolean equals(Object obj) {
		if(obj == null)
			return false;
		if(obj instanceof PResource){
			return getURI().equals(((PResource)obj).getURI());
			//return resource.equalsStructurally(((PResource)obj).getResource());
		}else
			return super.equals(obj);
	}

	public void setDescription(String text) {
		resource.setComment(text);
	}

	
	public void setPropertyValue(IProperty prop, Object value) {
		if(resource == null && ontology != null)
			ontology.checkModel();
		
		// if property is null, well nothing to be done
		if(prop == null)
			return;
		
		RDFProperty p = (RDFProperty) ((PProperty)prop).getResource();
		resource.setPropertyValue(p,convertSetValue(value));
			
	}
	
	
	public void addPropertyValue(IProperty prop, Object value) {
		if(resource == null && ontology != null)
			ontology.checkModel();
		
		// if property is null, well nothing to be done
		if(prop == null)
			return;
		
		RDFProperty p = (RDFProperty) ((PProperty)prop).getResource();
		resource.addPropertyValue(p,convertSetValue(value));
			
	}
	

	public void setPropertyValues(IProperty prop, Object[] values) {
		if(resource == null && ontology != null)
			ontology.checkModel();
		
		// if property is null, well nothing to be done
		if(prop == null)
			return;
		
		RDFProperty p = (RDFProperty) ((PProperty)prop).getResource();
		resource.setPropertyValues(p,convertSetValues(values));
	}
	
	/**
	 * convert a set value from My API to Protege OWL API
	 * @param o
	 * @return
	 */
	protected Object convertSetValue(Object value){
		if(value == null)
			return null;
		
		if(value instanceof PResource){
			return ((PResource)value).getResource();
		}else if(value instanceof ILogicExpression){	
			OWLModel model = resource.getOWLModel();
			ILogicExpression exp = (ILogicExpression) value;
			Object obj = null;
			if(exp.isSingleton()){
				if(exp.getExpressionType() == ILogicExpression.NOT){
					try{
						obj = model.createOWLComplementClass(
								(RDFSClass)convertSetValue(exp.getOperand()));
					}catch(ClassCastException ex){
						throw new IOntologyError("Cannot complement "+exp.getOperand()+", because it is not a class",ex);
					}
				}else
					obj =  convertSetValue(exp.getOperand());
			}else if(exp.getExpressionType() == ILogicExpression.AND){
				OWLIntersectionClass ac = model.createOWLIntersectionClass();
				for(Object o: exp){
					ac.addOperand((RDFSClass)convertSetValue(o));
				}
				obj = ac;
			}else if(exp.getExpressionType() == ILogicExpression.OR){
				OWLUnionClass oc = model.createOWLUnionClass();
				for(Object o: exp){
					oc.addOperand((RDFSClass)convertSetValue(o));
				}
				obj = oc;
			}
			return obj;
		}else if(value instanceof Collection){
			//TODO:
			return DefaultRDFSLiteral.create(resource.getOWLModel(),""+value);
		}else
			return DefaultRDFSLiteral.create(resource.getOWLModel(),value);
	}
	
	/**
	 * convert value
	 * @param o
	 * @return
	 */
	protected Collection convertSetValues(Object [] value){
		List list = new ArrayList();
		for(int i=0;i<value.length;i++)
			list.add(convertSetValue(value[i]));
		return list;
	}
	
	
	/**
	 * convert get value from Protege OWL API to My API
	 * @param o
	 * @return
	 */
	protected Object convertGetValue(Object value){
		if(value instanceof RDFResource){
			if( value instanceof OWLIndividual){
				return new PInstance((OWLIndividual)value,getOntology());
			}else if( value instanceof OWLRestriction){
				return new PRestriction((OWLRestriction)value,getOntology());
			}else if( value instanceof OWLLogicalClass){
				//maybe class should be returned
				return (new PClass((RDFSClass)value,getOntology())).getLogicExpression();
			}else if( value instanceof RDFProperty){
				return new PProperty((RDFProperty)value,getOntology());
			}else if( value instanceof RDFSClass){
				return new PClass((RDFSClass)value,getOntology());
			}else{
				return new PResource((RDFResource)value,getOntology());
			}
		}else if( value instanceof RDFSLiteral){
			Object o = ((RDFSLiteral) value).getPlainValue();
			return (o != null)?o: ((RDFSLiteral) value).getString();
		}else {
			return value;
		}
	}
	
	/**
	 * convert value
	 * @param o
	 * @return
	 */
	protected Object [] convertGetValues(Collection values){
		/*
		Object [] list = new Object [values.size()];
		int i=0;
		for(Object o: values)
			list[i++] = convertGetValue(o);
		return list;
		*/
		ArrayList list = new ArrayList();
		boolean sameType = true;
		Class type = null;
		for(Object o: values){
			Object v = convertGetValue(o);
			if(v == null)
				continue;
			
			list.add(v);
			// find the type
			if(type == null)
				type = v.getClass();
			if(!type.equals(v.getClass()))
				sameType = false;
		}
		return (sameType && type != null)?
				list.toArray((Object [])Array.newInstance(type,0)):
				list.toArray();
	}
	

	/**
	 * is this a system resources
	 * @return
	 */
	public boolean isSystem(){
		return resource.isSystem();
	}
	
	/**
	 * method to get super/sub direct/all classes
	 * @param parent
	 * @param direct
	 * @return
	 */
	protected IClass [] getClasses(Collection list){
		Set<IClass> c = new LinkedHashSet<IClass>();
		for(Object o: list){
			if(o instanceof RDFSClass){
				RDFSClass cls = (RDFSClass)o;
				//System.out.println("get class "+cls.getBrowserText()+" "+cls.getClass().getName());
				if(!cls.isSystem() || cls.equals(cls.getOWLModel().getOWLThingClass())){
					c.add(new PClass(cls,getOntology()));
				}
			}
		}
		return (IClass []) c.toArray(new IClass [0]);
	}
	
	
	/**
	 * method to get super/sub direct/all classes
	 * @param parent
	 * @param direct
	 * @return
	 */
	protected IRestriction [] getRestriction(Collection list){
		IRestriction [] c = new IRestriction[list.size()];
		int i=0;
		for(Object o: list){
			c[i++] = new PRestriction((OWLRestriction)o,getOntology());
		}
		return c;
	}
	
	/**
	 * get list of properties
	 * @param list
	 * @return
	 */
	protected IProperty [] getProperties(Collection list){
		IProperty [] c = new IProperty[list.size()];
		int i=0;
		for(Object o: list){
			c[i++] = new PProperty((OWLProperty)o,getOntology());
		}
		return c;
	}
	
	
	
	/**
	 * get the resource
	 * @return
	 */
	public RDFResource getResource(){
		return resource;
	}	
	
	/**
	 * get the resource
	 * @return
	 */
	public void setResource(RDFResource r){
		resource = r;
	}
	
	public IOntology getOntology() {
		return ontology;
	}
	
	public void setOntology(IOntology o) {
		ontology = (POntology) o;
	}
	
	
	/**
	 * 
	 */
	public String toString(){
		//if(resource != null)
		//	return resource.getBrowserText();
		//else
		return getName();
	}

	/**
	 * @return the info
	 */
	public Properties getResourceProperties() {
		if(info == null)
			info = new Properties();
		return info;
	}
	
	
	/**
	 * @return the info
	 */
	public void setResourceProperties(Properties map) {
		info = map;
	}
	
	/**
	 * get logic expression that represents this resource
	 * usually this is an empty expression with this as its parameter
	 * if resource is LogicClass, then it might do something interesting
	 * @return
	 */
	public ILogicExpression getLogicExpression(){
		return new LogicExpression(this);
	}

	/**
	 * compare to other resource
	 */
	public int compareTo(IResource o) {
		return getURI().compareTo(o.getURI());
	}
	
	
	/**
	 * get format
	 * @return
	 */
	public String getFormat(){
		return "OWL";
	}
	
	/**
	 * get location
	 * @return
	 */
	public String getLocation(){
		return ""+getURI();
	}

	public void dispose() {
		resource = null;
	}
	
}
