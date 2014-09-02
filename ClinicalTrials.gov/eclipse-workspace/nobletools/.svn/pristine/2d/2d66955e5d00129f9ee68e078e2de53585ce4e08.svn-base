package edu.pitt.ontology;

import java.net.URI;
import java.util.Properties;

import edu.pitt.terminology.util.Describable;
/**
 * This class describes a generic resource that is part of ontology
 * @author tseytlin
 */
public interface IResource extends Describable, Comparable<IResource> {
	/**
	 * get description
	 */
	public String getDescription();
	
	/**
	 * set description
	 * @param text
	 */
	public void setDescription(String text);
	
	/**
	 * get name of this resource
	 * @return
	 */
	public String getName();
	
	/**
	 * called when this resource is no longer required. Implementations should clear any 
	 * associated resources 
	 */
	public void dispose();
	
	/**
	 * get version of this resource
	 * @return
	 */
	public String getVersion();
	
	
	/**
	 * get URI of this resource
	 * @return
	 */
	public URI getURI();
	
	/**
	 * get namespace
	 * @return
	 */
	public String getNameSpace();
	
	/**
	 * get prefix for this resource (shortcut for a namespace) 
	 * @return
	 */
	public String getPrefix();
	
	/**
	 * get all properties associated with this resource
	 * @return list of properties
	 */
	public IProperty [] getProperties();
	
	
	/**
	 * get a single value of the given properties
	 * @return list of properties
	 */
	public Object getPropertyValue(IProperty prop);
	
	/**
	 * get values of the given properties
	 * @return list of properties
	 */
	public Object [] getPropertyValues(IProperty prop);
	
	
	/**
	 * add single value of the given properties
	 * @return list of properties
	 */
	public void addPropertyValue(IProperty prop, Object value);
	
	/**
	 * set single value of the given properties
	 * @return list of properties
	 */
	public void setPropertyValue(IProperty prop, Object value);
	
	/**
	 * get values of the given properties
	 * @return list of properties
	 */
	public void setPropertyValues(IProperty prop, Object [] values);
	
	/**
	 * remove all property values from resource for given property
	 * @param prop
	 */
	public void removePropertyValues(IProperty prop);
	
	/**
	 * remove all property values from resource for given property
	 * @param prop
	 */
	public void removePropertyValue(IProperty prop, Object value);
	
	/**
	 * remove all property values from resource
	 * @param prop
	 */
	public void removePropertyValues();
	
	
	/**
	 * has propety value
	 * @return
	 */
	public boolean hasPropetyValue(IProperty p, Object value);

	
	/**
	 * add label
	 * @param string
	 */
	public void addLabel(String label);
	
	
	/**
	 * add comment
	 * @param string
	 */
	public void addComment(String comment);
	
	
	/**
	 * add label
	 * @param string
	 */
	public void removeLabel(String label);
	
	
	/**
	 * add comment
	 * @param string
	 */
	public void removeComment(String comment);
	
	/**
	 * add version
	 * @param string
	 */
	public void addVersion(String version);
	
	
	/**
	 * remove version
	 * @param string
	 */
	public void removeVersion(String version);
	/**
	 * get labels
	 * @return
	 */
	public String [] getLabels();
	
	
	/**
	 * get labels
	 * @return
	 */
	public String [] getComments();
	
	
	/**
	 * is this a system resource
	 * @return
	 */
	public boolean isSystem();
	
	/**
	 * get an Ontology that is associated with this resource
	 * @return
	 */
	public IOntology getOntology();
	
	/**
	 * remove this resource
	 */
	public void delete();
	
	
	/**
	 * set name of a resource (fragment part of a URL)
	 * @param name
	 */
	public void setName(String name);
	
	/**
	 * get logic expression that represents this resource
	 * usually this is an empty expression with this as its parameter
	 * if resource is LogicClass, then it might do something interesting
	 * @return
	 */
	public ILogicExpression getLogicExpression();
	
	
	/**
	 * get misc properties that are associated with this resource
	 * @return
	 */
	public Properties getResourceProperties();
}
