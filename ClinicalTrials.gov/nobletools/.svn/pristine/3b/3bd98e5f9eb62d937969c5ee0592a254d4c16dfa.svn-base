package edu.pitt.ontology;


/**
 * This class describes an ontology instance
 * @author tseytlin
 *
 */
public interface IInstance extends IResource {
	
	/**
	 * add a direct type to this instance
	 * @param cls
	 */
	public void addType(IClass cls);
	
	/**
	 * remove a type from this instance
	 * @param cls
	 */
	public void removeType(IClass cls);		
	
	/**
	 * get all types of a given instance
	 * @param cls
	 * @return
	 */
	public IClass [] getTypes();
	
	/**
	 * get direct types of a given instance
	 * @param inst
	 * @return
	 */
	public IClass [] getDirectTypes();
	
	/**
	 * Is given instance has a type of cls
	 * @param inst
	 * @param cls
	 * @return
	 */
	public boolean hasType(IClass cls);
	
}
