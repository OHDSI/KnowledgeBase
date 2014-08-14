package edu.pitt.terminology.util;

import java.net.URI;

/**
 * a class that has some description
 * @author tseytlin
 */
public interface Describable {
	/**
	 * get name of an item
	 * @return
	 */
	public String getName();
	
	/**
	 * get description of an item
	 * @return
	 */
	public String getDescription();
	
	/**
	 * get version of an item
	 * @return
	 */
	public String getVersion();
	
	/**
	 * get URI of an item
	 * @return
	 */
	public URI getURI();
	
	
	/**
	 * get format
	 * @return
	 */
	public String getFormat();
	
	
	/**
	 * get location
	 * @return
	 */
	public String getLocation();
}
