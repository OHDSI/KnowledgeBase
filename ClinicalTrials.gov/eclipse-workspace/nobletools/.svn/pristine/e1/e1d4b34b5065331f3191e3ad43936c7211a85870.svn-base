package edu.pitt.ontology;

import java.beans.PropertyChangeListener;
import java.io.OutputStream;
import java.net.URI;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

import edu.pitt.terminology.Terminology;

public class DefaultRepository implements IRepository {
	private Map<URI,IOntology> ontologies = new LinkedHashMap<URI, IOntology>();
	private Map<String,Terminology> terminologies = new LinkedHashMap<String, Terminology>();
	
	public void addOntology(IOntology ontology) {
		ontologies.put(ontology.getURI(),ontology);
	}

	public void addPropertyChangeListener(PropertyChangeListener listener) {}

	public void addTerminology(Terminology terminology) {
		terminologies.put(terminology.getName(),terminology);
	}

	public IOntology createOntology(URI path) throws IOntologyException {
		throw new IOntologyException("Operation Not Support");
	}

	public void exportOntology(IOntology ont, int format, OutputStream out) throws IOntologyException {
		ont.write(out,format);
	}

	public String getDescription() {
		return "In Memory Ontology Repository";
	}

	public String getName() {
		return "Default Repository";
	}

	public IOntology[] getOntologies() {
		return ontologies.values().toArray(new IOntology [0]);
	}

	public IOntology[] getOntologies(String name) {
		List<IOntology> list = new ArrayList<IOntology>();
		for(URI key: ontologies.keySet()){
			if(key.toString().contains(name)){
				list.add(ontologies.get(key));
			}
		}
		return list.toArray(new IOntology [0]);
	}

	public IOntology getOntology(URI name) {
		return ontologies.get(name);
	}

	public IReasoner getReasoner(IOntology ontology) {
		return null;
	}

	/**
	 * convinience method
	 * get resource from one of the loaded ontologies
	 * @param path - input uri
	 * @return resource or null if resource was not found
	 */
	public IResource getResource(URI path){
		String uri = ""+path;
		int i = uri.lastIndexOf("#");
		uri = (i > -1)?uri.substring(0,i):uri;
		// get ontology
		IOntology ont = getOntology(URI.create(uri));
		
		// if ontology is all you want, fine Girish
		if(i == -1)
			return ont;
		// 
		if(ont != null){
			return ont.getResource(""+path);
		}
		return null;
	}
	

	public Terminology[] getTerminologies() {
		return terminologies.values().toArray(new Terminology [0]);
	}

	public Terminology getTerminology(String path) {
		return terminologies.get(path);
	}

	public boolean hasOntology(String name) {
		return getOntologies(name).length > 0;
	}

	public IOntology importOntology(URI path) throws IOntologyException {
		throw new IOntologyException("Operation Not Support");
	}

	public void importOntology(IOntology ont) throws IOntologyException {
		throw new IOntologyException("Operation Not Support");
	}

	public void removeOntology(IOntology ontology) {
		ontologies.remove(ontology.getURI());
	}

	public void removePropertyChangeListener(PropertyChangeListener listener) {
	}

	public void removeTerminology(Terminology terminology) {
		terminologies.remove(terminology.getName());

	}

	public IOntology getOntology(URI name, String version) {
		return getOntology(name);
	}

	public String[] getVersions(IOntology ont) {
		return (ont != null)?new String [] {ont.getVersion()}:new String [0];
	}

}
