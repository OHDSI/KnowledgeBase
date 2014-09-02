package edu.pitt.ontology;

import edu.pitt.terminology.lexicon.Concept;

/**
 * This describes an ontology class
 * @author tseytlin
 *
 */
public interface IClass extends IResource {
	/**
	 * add subclass 
	 * @param parent
	 * @param child
	 */
	public void addSubClass(IClass child);
	
	/**
	 * add subclass 
	 * @param parent
	 * @param child
	 */
	public void addSuperClass(IClass parent);
	
	
	/**
	 * add disjoint 
	 * @param parent
	 * @param child
	 */
	public void addDisjointClass(IClass a);
	
	/**
	 * add disjoint 
	 * @param parent
	 * @param child
	 */
	public void addEquivalentClass(IClass a);
	
	
	/**
	 * create instance of this class
	 * @param name
	 * @return IInstance that was created
	 */
	public IInstance createInstance(String name);
	
	
	/**
	 * create instance of this class
	 * auto-generate instance name
	 * @return IInstance that was created
	 */
	public IInstance createInstance();
	
	
	/**
	 * create a class that is a child of this
	 * @param name
	 * @return
	 */
	public IClass createSubClass(String name);
	
	
	/**
	 * add necessary restriction to this class
	 * @param name
	 * @return IInstance that was created
	 */
	public void addNecessaryRestriction(IRestriction restriction);
	

	/**
	 * remove restriction to this class
	 * @param name
	 * @return IInstance that was created
	 */
	public void removeNecessaryRestriction(IRestriction restriction);
	
	/**
	 * add equivalent Necessary and Sufficient restriction to this class
	 * @param name
	 * @return IInstance that was created
	 */
	public void addEquivalentRestriction(IRestriction restriction);
	

	/**
	 * remove restriction to this class
	 * @param name
	 * @return IInstance that was created
	 */
	public void removeEquivalentRestriction(IRestriction restriction);
	
	
	/**
	 * remove subclass 
	 * @param parent
	 * @param child
	 */
	public void removeSubClass(IClass child);
	
	/**
	 * remove subclass 
	 * @param parent
	 * @param child
	 */
	public void removeSuperClass(IClass parent);
	
	
	/**
	 * remove disjoint 
	 * @param parent
	 * @param child
	 */
	public void removeDisjointClass(IClass a);
	
	

	/**
	 * remove equivalent 
	 * @param parent
	 * @param child
	 */
	public void removeEquivalentClass(IClass a);
	
	/**
	 * Get all parent classes of a given class
	 * @return parents
	 */
	public IClass [] getSuperClasses();

	
	/**
	 * Get all children classes of a given class
	 * @return parents
	 */
	public IClass [] getSubClasses();

	
	/**
	 * Get direct parent classes of a given class
	 * @return parents
	 */
	public IClass [] getDirectSuperClasses();

	
	/**
	 * Get direct children classes of a given class
	 * @return parents
	 */
	public IClass [] getDirectSubClasses();
	

	/**
	 * get all instances of a given class
	 * @return
	 */
	public IInstance [] getInstances();
	
	/**
	 * get direct instances of a given class
	 * @return
	 */
	public IInstance [] getDirectInstances();
	
	
	/**
	 * get all restrictions associated with a given class
	 * @return
	 */
	public ILogicExpression getEquivalentRestrictions();
	
	/**
	 * get dircect necessary  restrictions associated with a given class
	 * @return
	 */
	public ILogicExpression getDirectNecessaryRestrictions();
	
	/**
	 * get all restrictions on given property
	 * @return
	 */
	public IRestriction [] getRestrictions(IProperty p);
	
	
	/**
	 * get all necessary  restrictions associated with a given class
	 * including inferred restrictions
	 * @return
	 */
	public ILogicExpression getNecessaryRestrictions();
	
	
	/**
	 * is parent a super class of child
	 * @param parent
	 * @return
	 */
	public boolean hasSuperClass(IClass parent);
	
	
	/**
	 * is child a sub class of parent
	 * @param child
	 * @return
	 */
	public boolean hasSubClass(IClass child);
	
	
	/**
	 * is child a sub class of parent
	 * @param child
	 * @return
	 */
	public boolean hasEquivalentClass(IClass child);
	
	/**
	 * is parent a direct super class of child
	 * @param parent
	 * @return
	 */
	public boolean hasDirectSuperClass(IClass parent);
	
	
	/**
	 * is child a direct sub class of parent
	 * @param child
	 * @return
	 */
	public boolean hasDirectSubClass(IClass child);
	
	
	/**
	 * get disjoint classes of a given class
	 * @param a
	 * @return
	 */
	public IClass [] getDisjointClasses();
	
	
	/**
	 * get equivalent classes of a given class
	 * @param a
	 * @return
	 */
	public IClass [] getEquivalentClasses();
	
	/**
	 * are two classes disjoint
	 * @param a
	 * @param b
	 * @return
	 */
	public boolean hasDisjointClass(IClass a);
	
	
	/**
	 * is this class anonymous
	 * @return
	 */
	public boolean isAnonymous();


	/**
	 * if possible get a Concept object for a given class
	 * @return
	 */
	public Concept getConcept();
	
	
	/**
	 * evaluate if given object can satisfy this class
	 * if parameter is a Class, then return true if it is child or equivalent class
	 * if parameter is an Instance, then return true if this class is its Type
	 */
	public boolean evaluate(Object obj);
	
}
