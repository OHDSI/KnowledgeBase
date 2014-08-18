package edu.pitt.ontology;

import java.beans.PropertyChangeListener;
import java.io.OutputStream;
import java.net.URI;

import edu.pitt.terminology.Terminology;



/**
 * This class describes a repository that contains 
 * ontologies and terminologies
 * @author tseytlin
 *
 */
public interface IRepository {
	public static final int OWL_FORMAT = 0;
	public static final String FORMAT_FILE = "file";
	public static final String FORMAT_DATABASE = "database";
	public static final String TYPE_ONTOLOGY = "ontology";
	public static final String TYPE_SYSTEM_ONTOLOGY = "systemOntology";
	public static final String TYPE_TERMINOLOGY = "terminology";

	/**
	 * add property change listener
	 * @param listener
	 */
	public void addPropertyChangeListener(PropertyChangeListener listener);
	
	
	/**
	 * add property change listener
	 * @param listener
	 */
	public void removePropertyChangeListener(PropertyChangeListener listener);
	
	
	/**
	 * add given ontology to repository registry
	 * @param ontology
	 */
	public void addOntology(IOntology ontology);
	
	
	/**
	 * remove given ontology to repository registry
	 * @param ontology
	 */
	public void removeOntology(IOntology ontology);
	
	
	/**
	 * add given terminology to repository registry
	 * @param terminology
	 */
	public void addTerminology(Terminology terminology);
	
	
	/**
	 * remove given terminology to repository registry
	 * @param terminology
	 */
	public void removeTerminology(Terminology terminology);
	
	
	/**
	 * create new ontology with given URI
	 * does NOT save it in database
	 * @param path
	 * @return
	 */
	public IOntology createOntology(URI path) throws IOntologyException;


	/**
	 * convinience method
	 * get resource from one of the loaded ontologies
	 * @param path - input uri
	 * @return resource or null if resource was not found
	 */
	public IResource getResource(URI path);
	
	/**
	 * get ontologies that are loaded in repository
	 * @return
	 */
	public IOntology [] getOntologies();
	
	
	/**
	 * get ontologies that are loaded in repository
	 * @return
	 */
	public IOntology [] getOntologies(String name);
	
	
	/**
	 * get specific ontology if path is known
	 * @param URI path 
	 * @return Ontology
	 */
	public IOntology getOntology(URI name);
	
	
	/**
	 * get specific ontology if path is known
	 * @param URI path 
	 * @return Ontology
	 */
	public IOntology getOntology(URI name, String version);

	
	/**
	 * get available version fo a given ontology
	 * @param ont
	 * @return
	 */
	public String [] getVersions(IOntology ont);

	
	
	/**
	 * is specific ontology available if path is known
	 * @param URI path or name
	 * @return Ontology
	 */
	public boolean hasOntology(String name);
	
	
	/**
	 * get a list of available terminologies
	 * @return
	 */
	public Terminology [] getTerminologies();
	
	
	/**
	 * get a specific  terminologies
	 * @return
	 */
	public Terminology getTerminology(String path);
	
	
	/**
	 * import ontology into repository, puts it into database
	 * @param file location 
	 * @return ontology object
	 */
	public IOntology importOntology(URI path) throws IOntologyException;
	
	/**
	 * import ontology into repository, puts it into database
	 * @param file location 
	 */
	public void importOntology(IOntology ont) throws IOntologyException;
	
	
	/**
	 * export ontology from repository
	 */
	public void exportOntology(IOntology iOntology, int format, OutputStream out) throws IOntologyException;
	
	
	/**
	 * get reasoner that can handle this ontology
	 * you can configure the type of reasoner by 
	 * specifying reasoner class and optional URL
	 * in System.getProperties()
	 * reasoner.class and reasoner.url
	 * @return null if no reasoner is available
	 */
	public IReasoner getReasoner(IOntology ontology);
	
	
	/**
	 * get name of this repository
	 * @return
	 */
	public String getName();
	
	
	/**
	 * get description of repository
	 * @return
	 */
	public String getDescription();
}
