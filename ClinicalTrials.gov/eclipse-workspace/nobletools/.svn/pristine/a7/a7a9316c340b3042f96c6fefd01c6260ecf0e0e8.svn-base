package edu.pitt.ontology.bioportal;

import static edu.pitt.ontology.bioportal.BioPortalHelper.COMMENTS;
import static edu.pitt.ontology.bioportal.BioPortalHelper.LABELS;
import static edu.pitt.ontology.bioportal.BioPortalHelper.PROPERTIES;
import static edu.pitt.ontology.bioportal.BioPortalHelper.VERSIONS;

import java.net.URI;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.HashSet;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Properties;
import java.util.Set;

import edu.pitt.ontology.ILogicExpression;
import edu.pitt.ontology.IOntology;
import edu.pitt.ontology.IOntologyError;
import edu.pitt.ontology.IProperty;
import edu.pitt.ontology.IResource;
import edu.pitt.ontology.LogicExpression;

/**
 * basic BioPortal resource
 * @author Eugene Tseytlin
 *
 */
public class BResource implements IResource {
	protected Properties properties = new Properties();
	protected BOntology ontology;
	protected String resourceType;
	
	/**
	 * set ontology
	 * @param ontology
	 */
	public void setOntology(BOntology ontology) {
		this.ontology = ontology;
	}

	/**
	 * get a type of this resource
	 * @return
	 */
	public String getResourceType(){
		return resourceType;
	}
	
	/**
	 * get list of strings from the properties
	 * @param s
	 * @return
	 */
	protected Set<String> getList(String key){
		/*
		Set<String> list = null;
		Object obj = properties.get(key);
		if(obj == null){
			list = new LinkedHashSet<String>();
			properties.put(key,list);
		}else if(obj instanceof Set){
			list = (Set<String>) obj;
		}else {
			list = new LinkedHashSet<String>();
			list.add(obj.toString());
			properties.put(key,list);
		}
		*/
		HashSet<String> list = (HashSet<String>) properties.get(key);
		if(list == null){
			list = new LinkedHashSet<String>();
			properties.put(key,list);
		}
		return list;
	}
	
	/**
	 * get list of strings from the properties
	 * @param s
	 * @return
	 */
	protected List getObjectList(Object key){
		// maybe there is an object, but not a list
		List list = null;
		Object obj = properties.get(""+key);
		if(obj == null){
			list = new ArrayList();
			properties.put(""+key,list);
		}else if(obj instanceof List){
			list = (List) obj;
		}else if(obj instanceof Collection){
			list = new ArrayList((Collection)obj);
		}else{
			list = Collections.singletonList(obj);
		}
		return list;
	}
	
	public void addComment(String comment) {
		getList(COMMENTS).add(comment);
	}

	public void addLabel(String label) {
		getList(LABELS).add(label);
	}

	public void addPropertyValue(IProperty prop, Object value) {
		// add prop -value
		List list = getObjectList(prop);
		if(!list.contains(value))
			list.add(value);
		// add property to list of all properties
		list = getObjectList(BioPortalHelper.PROPERTIES);
		if(!list.contains(prop))
			list.add(prop);
	}

	public void addVersion(String version) {
		getList(VERSIONS).add(version);
	}

	public void delete() {
		throw new IOntologyError("Read-Only Ontology");
	}

	public void dispose() {
		String loc = getLocation();
		properties.clear();
		properties.setProperty("location", loc);
	}

	
	public String[] getComments() {
		return getList(COMMENTS).toArray(new String [0]);
	}

	public String getDescription() {
		Set<String> str = getList(COMMENTS);
		return (str.size()>0)?str.iterator().next():"";
	}

	public String[] getLabels() {
		return getList(LABELS).toArray(new String[0]);
	}

	public ILogicExpression getLogicExpression() {
		return new LogicExpression(this);
	}

	public String getName() {
		return properties.getProperty("name","");
	}

	public String getNameSpace() {
		return properties.getProperty("namespace","");
	}

	public IOntology getOntology() {
		return ontology;
	}

	public String getPrefix() {
		return  properties.getProperty("prefix","");
	}

	public IProperty[] getProperties() {
		List<IProperty> list = new ArrayList<IProperty>();
		for(Object key: getObjectList(PROPERTIES)){
			list.add(ontology.getProperty(""+key));
		}
		return list.toArray(new IProperty [0]);
	}

	public Object getPropertyValue(IProperty prop) {
		Object [] obj = getPropertyValues(prop);
		return (obj.length > 0)?obj[0]:null;
	}

	public Object[] getPropertyValues(IProperty prop) {
		BProperty bp = (BProperty) prop;
		if(properties.containsKey(prop.getName()))
			return getObjectList(prop).toArray();
		else if(properties.containsKey(bp.getOrignalName()))
			return getObjectList(bp.getOrignalName()).toArray();
		return new Object [0];
	}

	public URI getURI() {
		
		Object u = properties.get("uri");
		try{
		if(u == null){
			u = URI.create(ontology.getNameSpace()+getName());
		}else if(!(u instanceof URI))
			u = URI.create(""+u);
		return (URI) u;
		}catch (Exception ex ){
			System.err.println(u);
			return null;
		}
	}

	public String getVersion() {
		Set<String> str = getList(VERSIONS);
		return (str.size()>0)?str.iterator().next():"";
	}

	public boolean hasPropetyValue(IProperty p, Object value) {
		if(properties.containsKey(p.getName())){
			return getObjectList(p).contains(value);
		}
		return false;
	}

	public boolean isSystem() {
		return Boolean.parseBoolean(properties.getProperty("isSystem","false"));
	}

	public void removeComment(String comment) {
		getList(COMMENTS).remove(comment);
	}

	public void removeLabel(String label) {
		getList(LABELS).remove(label);
	}

	public void removePropertyValue(IProperty prop, Object value) {
		if(properties.containsKey(prop.getName())){
			List list = getObjectList(prop);
			list.remove(value);
			if(list.isEmpty())
				removePropertyValues(prop);
		}
	}
	public void removePropertyValues(IProperty prop) {
		if(properties.containsKey(prop.getName())){
			properties.remove(prop.getName());
		}
		getObjectList(BioPortalHelper.PROPERTIES).remove(prop);

	}
	public void removePropertyValues() {
		for(IProperty p: getProperties())
			removePropertyValues(p);
		properties.remove(BioPortalHelper.PROPERTIES);
	}

	public void removeVersion(String version) {
		getList(VERSIONS).remove(version);
	}

	public void setDescription(String text) {
		List<String> c = new ArrayList<String>(getList(COMMENTS));
		if(c.size()> 0 &&  text.equals(c.get(0)))
			c.set(0,text);
		else
			c.add(0,text);
		properties.put(COMMENTS,new LinkedHashSet<String>(c));
	}

	public void setName(String name) {
		properties.setProperty("name",name);
	}

	public void setPropertyValue(IProperty prop, Object value) {
		List list = getObjectList(prop);
		if(!list.contains(value)){
			// check if functional
			if(prop.isFunctional())
				list.clear();
			list.add(value);
		}
		list = getObjectList(BioPortalHelper.PROPERTIES);
		if(!list.contains(prop))
			list.add(prop);
	}

	public void setPropertyValues(IProperty prop, Object[] values) {
		List list = getObjectList(prop);
		list.clear();
		Collections.addAll(list,values);
		list = getObjectList(BioPortalHelper.PROPERTIES);
		if(!list.contains(prop))
			list.add(prop);
	}

	public String getFormat() {
		return properties.getProperty("format","");
	}

	public String getLocation() {
		return properties.getProperty("location","");
	}

	public int compareTo(IResource r) {
		return getURI().compareTo(r.getURI());
	}
	
	public String getId(){
		return properties.getProperty("id","");
	}
	
	public String toString(){
		return getName();
	}
	
	public boolean equals(Object obj){
		if(obj instanceof BResource){
			return getURI().equals(((BResource)obj).getURI());
		}
		return false;
	}
	
	public int hashCode(){
		return getURI().hashCode();
	}
	/**
	 * get metadata information
	 * @return
	 */
	public Properties getResourceProperties(){
		return properties;
	}
}
