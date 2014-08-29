package edu.pitt.ontology.owl;

import java.beans.PropertyChangeListener;
import java.beans.PropertyChangeSupport;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.net.MalformedURLException;
import java.net.URI;
import java.net.URL;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

import edu.pitt.ontology.IOntology;
import edu.pitt.ontology.IOntologyException;
import edu.pitt.ontology.IReasoner;
import edu.pitt.ontology.IRepository;
import edu.pitt.ontology.IResource;
import edu.pitt.terminology.Terminology;
import edu.pitt.terminology.client.IndexFinderTerminology;

public class ORepository implements IRepository{
	private static final String DEFAULT_TERMINOLOGY_LOCATION = ".terminologies";
	private static final String DEFAULT_ONTOLOGY_LOCATION = ".ontologies";
	
	private File ontologyDirectory = new File(System.getProperty("user.home")+File.separator+DEFAULT_ONTOLOGY_LOCATION);
	private File terminologyDirectory = new File(System.getProperty("user.home")+File.separator+DEFAULT_TERMINOLOGY_LOCATION);

	
	private PropertyChangeSupport pcs = new PropertyChangeSupport(this);
	private Map<URI,IOntology> ontologies = new LinkedHashMap<URI, IOntology>();
	private Map<String,Terminology> terminologies = new LinkedHashMap<String, Terminology>();
	
	
	
	public void addOntology(IOntology ontology) {
		ontologies.put(ontology.getURI(),ontology);
	}

	public void addPropertyChangeListener(PropertyChangeListener listener) {
		pcs.addPropertyChangeListener(listener);
	}

	public void addTerminology(Terminology terminology) {
		terminologies.put(terminology.getName(),terminology);
	}

	public IOntology createOntology(URI path) throws IOntologyException {
		return OOntology.createOntology(path);
	}

	public void exportOntology(IOntology ont, int format, OutputStream out) throws IOntologyException {
		ont.write(out,format);
	}

	public String getDescription() {
		return "OWL Ontology and NOBLE Terminology Repository.";
	}

	public String getName() {
		return "OWL Ontology Repository";
	}

	public IOntology[] getOntologies() {
		if(ontologies == null){
			ontologies = new HashMap<URI, IOntology>();
			File dir = ontologyDirectory;
			if(!dir.exists())
				dir.mkdirs();
			for(File f: dir.listFiles()){
				String sf = IndexFinderTerminology.TERM_SUFFIX;
				if(f.getName().endsWith(sf)){
					addOntology(new OOntology(f.getAbsolutePath()));
				}
			}
			
		}
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

	public IReasoner getReasoner(IOntology ont) {
		if(ont instanceof OOntology){
			return new OReasoner((OOntology)ont);
		}
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
		if(terminologies == null){
			terminologies = new HashMap<String, Terminology>();
			File dir = terminologyDirectory;
			if(!dir.exists())
				dir.mkdirs();
			for(File f: dir.listFiles()){
				String sf = IndexFinderTerminology.TERM_SUFFIX;
				if(f.getName().endsWith(sf)){
					Terminology t;
					try {
						t = new IndexFinderTerminology(f.getName().substring(0,f.getName().length()-sf.length()));
						terminologies.put(t.getName(),t);
					} catch (UnsupportedOperationException e){
						System.err.println("Corrupted termonology detected at "+f.getAbsolutePath()+". skipping ...");
					} catch (IOException e) {
						e.printStackTrace();
					}
				}
			}
			
		}
		return terminologies.values().toArray(new Terminology [0]);
	}

	public Terminology getTerminology(String path) {
		getTerminologies();
		return terminologies.get(path);
	}

	public boolean hasOntology(String name) {
		return getOntologies(name).length > 0;
	}

	public IOntology importOntology(URI path) throws IOntologyException {
		URL url = null;
		try {
			url = path.toURL();
		} catch (MalformedURLException e) {
			throw new IOntologyException("Invalid URI supplied: "+path,e);
		}
		IOntology ont = OOntology.loadOntology(url);
		importOntology(ont);
		return getOntology(ont.getURI());
		
	}

	public void importOntology(IOntology ont) throws IOntologyException {
		File file = new File(ontologyDirectory,ont.getName());
		try {
			ont.write(new FileOutputStream(file),IOntology.OWL_FORMAT);
		} catch (FileNotFoundException e) {
			throw new IOntologyException("Unable to save file in the local cache at "+file.getAbsolutePath(),e);
		}
		// reload from cache
		ont.dispose();
		ont = OOntology.loadOntology(file);
		addOntology(ont);
	}

	public void removeOntology(IOntology ontology) {
		ontologies.remove(ontology.getURI());
	}

	public void removePropertyChangeListener(PropertyChangeListener listener) {
		pcs.removePropertyChangeListener(listener);
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
