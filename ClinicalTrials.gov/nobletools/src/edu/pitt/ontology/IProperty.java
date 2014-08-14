package edu.pitt.ontology;

/**
 * This class describes propery construct
 * @author tseytlin
 */
public interface IProperty extends IResource {
	// property constants
	public static final int OBJECT = 0;
	public static final int DATATYPE = 1;
	public static final int ANNOTATION_OBJECT = 2;
	public static final int ANNOTATION_DATATYPE = 3;
	
	
	// a set of predefined RDFS/OWL properties
	public static final String RDFS_IS_DEFINED_BY = "rdfs:isDefinedBy";
	public static final String RDFS_SEE_ALSO = "rdfs:seeAlso";	
	public static final String RDFS_LABEL = "rdfs:label";
	public static final String RDFS_COMMENT = "rdfs:comment";
	public static final String OWL_VERSION_INFO = "owl:versionInfo";
	public static final String OWL_PRIOR_VERSION = "owl:priorVersion";
	public static final String OWL_BACKWARD_COMPATIBLE_WITH = "owl:backwardCompatibleWith";
	public static final String OWL_INCOMPATIBLE_WITH = "owl:incompatibleWith";
	public static final String OWL_DEPRECATED_CLASS = "owl:DeprecatedClass";
	public static final String OWL_DEPRECATED_PROPERTY = "owl:DeprecatedProperty";
	public static final String OWL_SAME_AS = "owl:sameAs";
	public static final String OWL_DIFFERENT_FROM = "owl:differentFrom";
	public static final String OWL_ALL_DIFFERENT = "owl:AllDifferent";

	// dublin core constants
	public static final String DC_CONTRIBUTOR = "http://purl.org/dc/elements/1.1/contributor";
	public static final String DC_COVERAGE = "http://purl.org/dc/elements/1.1/coverage";
	public static final String DC_CREATOR = "http://purl.org/dc/elements/1.1/creator";
	public static final String DC_DATE = "http://purl.org/dc/elements/1.1/date";
	public static final String DC_DESCRIPTION = "http://purl.org/dc/elements/1.1/description";
	public static final String DC_FORMAT = "http://purl.org/dc/elements/1.1/format";
	public static final String DC_IDENTIFIER = "http://purl.org/dc/elements/1.1/identifier";
	public static final String DC_LANGUAGE = "http://purl.org/dc/elements/1.1/language";
	public static final String DC_PUBLISHER = "http://purl.org/dc/elements/1.1/publisher";
	public static final String DC_RELATION = "http://purl.org/dc/elements/1.1/relation";
	public static final String DC_RIGHTS = "http://purl.org/dc/elements/1.1/rights";
	public static final String DC_SOURCE = "http://purl.org/dc/elements/1.1/source";
	public static final String DC_SUBJECT = "http://purl.org/dc/elements/1.1/subject";
	public static final String DC_TITLE = "http://purl.org/dc/elements/1.1/title";
	public static final String DC_TYPE = "http://purl.org/dc/elements/1.1/type";
	
	
	
	

	/**
	 * create sub property of this property
	 * @param name
	 * @return
	 */
	public IProperty createSubProperty(String name);
	
	
	/**
	 * get property type
	 * OBJECT, DATATYPE, ANNOTATION_OBJECT, ANNOTATION_DATATYPE
	 * @return
	 */
	public int getPropertyType();
	
	
	/**
	 * is property a datatype property
	 * @return
	 */
	public boolean isDatatypeProperty();
	
	/**
	 * is property an object property
	 * @return
	 */
	public boolean isObjectProperty();
	
	/**
	 * is property an annotation property
	 * @return
	 */
	public boolean isAnnotationProperty();
	
	
	/**
	 * get domain of some property
	 * @param prop
	 * @return
	 */
	public IClass [] getDomain();
	
	
	/**
	 * get range of some property
	 * @param prop
	 * @return
	 */
	public Object [] getRange();
	
	
	/**
	 * set domain of some property
	 * @param prop
	 * @return
	 */
	public void setDomain(IResource [] domain);
	
	
	/**
	 * set range of some property
	 * @param prop
	 * @return
	 */
	public void setRange(Object [] range);
	
	/**
	 * check if given property is an inverse of this
	 * @param p
	 * @return
	 */
	public boolean isInverseOf(IProperty p);
	
	/**
	 * is property transitive
	 * @return
	 */
	public boolean isTransitive();
	
	/**
	 * is property functional
	 * @return
	 */
	public boolean isFunctional();
	
	/**
	 * is property symmetrical
	 * @return
	 */
	public boolean isSymmetric();
	
	/**
	 * get sub properties
	 * @return
	 */
	public IProperty [] getSubProperties();
	
	/**
	 * get super properties
	 * @return
	 */
	public IProperty [] getSuperProperties();
	
	/**
	 * get sub properties
	 * @return
	 */
	public IProperty [] getDirectSubProperties();
	
	/**
	 * get super properties
	 * @return
	 */
	public IProperty [] getDirectSuperProperties();
	
	/**
	 * get inverse property
	 * @return
	 */
	public IProperty getInverseProperty();
	
	/**
	 * set inverse property
	 * @return
	 */
	public void setInverseProperty(IProperty p);
	
	
	/**
	 * add direct super property
	 * @param p
	 */
	public void addSuperProperty(IProperty p);
	
	/**
	 * add direct super property
	 * @param p
	 */
	public void addSubProperty(IProperty p);
	
	/**
	 * remove super property
	 * @param p
	 */
	public void removeSuperProperty(IProperty p);
	
	/**
	 * remove super property
	 * @param p
	 */
	public void removeSubProperty(IProperty p);
	
	
	/**
	 * set property transitive flag
	 */
	public void setTransitive(boolean b);
	
	/**
	 * set property functional flag
	 */
	public void  setFunctional(boolean b);
	
	/**
	 * set property symmetrical flag
	 */
	public void setSymmetric(boolean b);
	
}
