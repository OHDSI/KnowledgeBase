package edu.pitt.ontology.bioportal;

import static edu.pitt.ontology.bioportal.BioPortalHelper.ONTOLOGIES;
import static edu.pitt.ontology.bioportal.BioPortalHelper.openURL;
import static edu.pitt.ontology.bioportal.BioPortalHelper.parseXML;

import java.beans.PropertyChangeListener;
import java.beans.PropertyChangeSupport;
import java.io.OutputStream;
import java.net.MalformedURLException;
import java.net.URI;
import java.net.URL;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.SortedSet;
import java.util.TreeSet;

import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.NodeList;

import edu.pitt.ontology.IClass;
import edu.pitt.ontology.IOntology;
import edu.pitt.ontology.IOntologyError;
import edu.pitt.ontology.IOntologyException;
import edu.pitt.ontology.IReasoner;
import edu.pitt.ontology.IRepository;
import edu.pitt.ontology.IResource;
import edu.pitt.terminology.Terminology;
import edu.pitt.terminology.lexicon.Concept;

/**
 * provides view into BioPortal Repository
 * @author Eugene Tseytlin
 *
 */
public class BioPortalRepository implements IRepository {
	public static final String DEFAULT_BIOPORTAL_URL = "http://rest.bioontology.org/bioportal/";
	public static final String BIOPORTAL_STAGING_SERVER_URL = "http://stagerest.bioontology.org/bioportal/";
	public static final String DEFAULT_BIOPORTAL_API_KEY = "6ebc962a-e7ae-40e4-af41-472224ef81aa";
	
	private URL bioPortalURL;
	private String bioPortalAPIKey;
	private Map<String,BOntology> ontologyMap;
	private IOntology [] ontologies;
	private PropertyChangeSupport pcs = new PropertyChangeSupport(this);
	
	/**
	 * @param args
	 */
	public static void main(String[] args) {
		BioPortalRepository repository = new BioPortalRepository();
		System.out.println("--");
		for(IOntology o: repository.getOntologies())
			System.out.println(o+" "+o.getResourceProperties().getProperty("id"));
		System.out.println("--");
		IOntology [] onts = repository.getOntologies("NCI_Thesaurus");
		if(onts.length > 0){
			IOntology ont = onts[0];
			System.out.println(ont.getRoot()+" : "+Arrays.toString(ont.getRootClasses()));
			IClass [] clses = new IClass [] { ont.getClass("Melanoma") };
			for(IClass cls :clses){
				System.out.println(cls+" "+cls.getLocation());
				Concept c = cls.getConcept();
				c.printInfo(System.out);
			}
		}
	}
	
	
	/**
	 * creat new bioportal repository
	 */
	public BioPortalRepository(URL url){
		bioPortalURL = url;
		bioPortalAPIKey = "apikey="+DEFAULT_BIOPORTAL_API_KEY;
	}
	
	/**
	 * creat new bioportal repository
	 */
	public BioPortalRepository(URL url, String apiKey){
		bioPortalURL = url;
		bioPortalAPIKey = "apikey="+apiKey;
	}
	
	
	/**
	 * creat new bioportal repository
	 */
	public BioPortalRepository(){
		try{
			bioPortalURL = new URL(DEFAULT_BIOPORTAL_URL);
		}catch(MalformedURLException ex){
			ex.printStackTrace();
		}
		bioPortalAPIKey = "apikey="+DEFAULT_BIOPORTAL_API_KEY;
	}
	
	public URL getURL(){
		return bioPortalURL;
	}
	
	public String getAPIKey(){
		return bioPortalAPIKey;
	}
	
	/**
	 * fetch all ontologies from URL
	 */
	private Map<String,BOntology> fetchOntologies(){
		// init map
		ontologyMap = new LinkedHashMap<String,BOntology>();
		
		// get document
		Document doc = parseXML(openURL(getURL()+ONTOLOGIES+"?"+getAPIKey()));
		if(doc != null){
			// since ontologyBean are not nested we can simple
			// get their list
			NodeList list = doc.getDocumentElement().getElementsByTagName("ontologyBean");
			for(int i=0;i<list.getLength();i++){
				BOntology ont = new BOntology(this,(Element)list.item(i));
				ontologyMap.put(ont.getName(),ont);
				ontologyMap.put(""+ont.getURI(),ont);
			}
		}
		return ontologyMap;
	}
	
	public void addOntology(IOntology ontology) {
		throw new IOntologyError("BioPortal Repository is read-only");
	}
	
	public void addPropertyChangeListener(PropertyChangeListener listener) {
		pcs.addPropertyChangeListener(listener);
	}
	
	public void addTerminology(Terminology terminology) {
		throw new IOntologyError("BioPortal Repository is read-only");
	}

	public IOntology createOntology(URI path) throws IOntologyException {
		throw new IOntologyError("BioPortal Repository is read-only");
	}

	public void exportOntology(IOntology ontology, int format, OutputStream out) throws IOntologyException {
		// TODO Auto-generated method stub

	}

	public IOntology[] getOntologies() {
		if(ontologyMap == null)
			ontologyMap = fetchOntologies();
		if(ontologies == null){
			SortedSet<BOntology> set = new TreeSet<BOntology>();
			set.addAll(ontologyMap.values());
			ontologies = set.toArray(new IOntology [0]);
		}
		return ontologies;
	}
	
	/**
	 * get ontologies that are loaded in repository
	 * @return
	 */
	public IOntology [] getOntologies(String name){
		if(ontologyMap == null)
			ontologyMap = fetchOntologies();
		ArrayList<IOntology> onts = new ArrayList<IOntology>();
		for(String str: ontologyMap.keySet()){
			if(str.contains(name)){
				onts.add(ontologyMap.get(str));
			}
		}
		return onts.toArray(new IOntology [0]);
	}
	

	public IOntology getOntology(URI u) {
		if(ontologyMap == null)
			ontologyMap = fetchOntologies();
		return ontologyMap.get(""+u);
	}

	public IResource getResource(URI path) {
		String uri = path.toASCIIString();
		int i = uri.lastIndexOf("#");
		uri = (i > -1)?uri.substring(0,i):uri;
		// get ontology
		IOntology ont = getOntology(URI.create(uri));
		// if ontology is all you want, fine Girish
		if(i == -1)
			return ont;
		// 

		if(ont != null){
			uri = path.toASCIIString();
			return ont.getResource(uri.substring(i+1));
		}
		return null;
	}

	public Terminology[] getTerminologies() {
		SortedSet<BOntology> set = new TreeSet<BOntology>();
		set.addAll(ontologyMap.values());
		return set.toArray(new Terminology [0]);
	}

	public Terminology getTerminology(String path) {
		if(ontologyMap == null)
			ontologyMap = fetchOntologies();
		return ontologyMap.get(path);
	}

	public boolean hasOntology(String name) {
		if(ontologyMap == null)
			ontologyMap = fetchOntologies();
		return ontologyMap.containsKey(name) || getOntologies(name).length > 0;
	}

	public IOntology importOntology(URI path) throws IOntologyException {
		throw new IOntologyError("BioPortal Repository is read-only");
	}

	public void importOntology(IOntology ont) throws IOntologyException {
		throw new IOntologyError("BioPortal Repository is read-only");
	}

	public void removeOntology(IOntology ontology) {
		throw new IOntologyError("BioPortal Repository is read-only");
	}

	public void removePropertyChangeListener(PropertyChangeListener listener) {
		pcs.removePropertyChangeListener(listener);
	}

	public void removeTerminology(Terminology terminology) {
		throw new IOntologyError("BioPortal Repository is read-only");
	}

	/**
	 * get reasoner that can handle this ontology
	 * you can configure the type of reasoner by 
	 * specifying reasoner class and optional URL
	 * in System.getProperties()
	 * reasoner.class and reasoner.url
	 * @return null if no reasoner is available
	 */
	public IReasoner getReasoner(IOntology ont){
		return null;
	}
		
	/**
	 * get name of this repository
	 * @return
	 */
	public String getName(){
		return "BioPortal Repository";
	}
	
	
	/**
	 * get description of repository
	 * @return
	 */
	public String getDescription(){
		return "Use BioPortal to access and share ontologies that are actively used in biomedical communities.";
	}
	

	/**
	 * get specific ontology version
	 */
	public IOntology getOntology(URI name, String version) {
		BOntology ont = (BOntology) getOntology(name);
		return (ont != null)?ont.getOntologyVersions().get(version):null;
	}

	
	/**
	 * get versions available for an ontology
	 */
	public String[] getVersions(IOntology ont) {
		if(ont instanceof BOntology){
			List<String> vers = new ArrayList<String>(((BOntology)ont).getOntologyVersions().keySet());
			return vers.toArray(new String [0]);
		}
		return (ont != null)?new String [] {ont.getVersion()}:new String [0];
	}
}
