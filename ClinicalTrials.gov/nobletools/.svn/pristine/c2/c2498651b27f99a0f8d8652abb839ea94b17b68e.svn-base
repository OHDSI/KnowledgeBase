package edu.pitt.terminology.client;

import java.beans.PropertyChangeListener;
import java.beans.PropertyChangeSupport;
import java.io.File;
import java.io.IOException;
import java.io.OutputStream;
import java.net.URI;
import java.util.HashMap;
import java.util.Map;

import edu.pitt.ontology.IOntology;
import edu.pitt.ontology.IOntologyException;
import edu.pitt.ontology.IReasoner;
import edu.pitt.ontology.IRepository;
import edu.pitt.ontology.IResource;
import edu.pitt.terminology.Terminology;

public class IndexFinderRepository implements IRepository {
	private PropertyChangeSupport pcs = new PropertyChangeSupport(this);
	private Map<String,Terminology> terminologies;
	
	public void addPropertyChangeListener(PropertyChangeListener listener) {
		pcs.addPropertyChangeListener(listener);
	}

	public void removePropertyChangeListener(PropertyChangeListener listener) {
		pcs.removePropertyChangeListener(listener);
	}

	public void addOntology(IOntology ontology) {
		// TODO Auto-generated method stub

	}

	public void removeOntology(IOntology ontology) {
		// TODO Auto-generated method stub

	}

	public void addTerminology(Terminology terminology) {
		// TODO Auto-generated method stub

	}

	public void removeTerminology(Terminology terminology) {
		// TODO Auto-generated method stub

	}

	public IOntology createOntology(URI path) throws IOntologyException {
		// TODO Auto-generated method stub
		return null;
	}

	public IResource getResource(URI path) {
		// TODO Auto-generated method stub
		return null;
	}

	public IOntology[] getOntologies() {
		return new IOntology [0];
	}

	public IOntology[] getOntologies(String name) {
		// TODO Auto-generated method stub
		return null;
	}

	public IOntology getOntology(URI name) {
		// TODO Auto-generated method stub
		return null;
	}

	public IOntology getOntology(URI name, String version) {
		// TODO Auto-generated method stub
		return null;
	}

	public String[] getVersions(IOntology ont) {
		// TODO Auto-generated method stub
		return null;
	}

	public boolean hasOntology(String name) {
		// TODO Auto-generated method stub
		return false;
	}

	public Terminology[] getTerminologies() {
		if(terminologies == null){
			terminologies = new HashMap<String, Terminology>();
			
			File dir = IndexFinderTerminology.getPersistenceDirectory();
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

	public IOntology importOntology(URI path) throws IOntologyException {
		// TODO Auto-generated method stub
		return null;
	}

	public void importOntology(IOntology ont) throws IOntologyException {
		// TODO Auto-generated method stub

	}

	public void exportOntology(IOntology iOntology, int format, OutputStream out) throws IOntologyException {
		// TODO Auto-generated method stub

	}

	public IReasoner getReasoner(IOntology ontology) {
		return null;
	}

	public String getName() {
		return "IndexFinder Repository";
	}

	public String getDescription() {
		return "Repository of Terminologies stored in IndexFinder tables";
	}

}
