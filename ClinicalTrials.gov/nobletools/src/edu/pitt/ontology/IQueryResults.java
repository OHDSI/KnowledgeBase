package edu.pitt.ontology;

import java.util.Iterator;
import java.util.Map;

public interface IQueryResults extends Iterator {

	/**
	 * get list of variables that were returned
	 * @return
	 */
	public String [] getVariables();
	
	/**
	 * get next row
	 * @return
	 */
	public Map next();
}
