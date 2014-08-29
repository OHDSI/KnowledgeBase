package edu.pitt.ontology.owl;


import java.beans.PropertyChangeListener;
import java.beans.PropertyChangeSupport;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.OutputStream;
import java.net.ProtocolException;
import java.net.URI;
import java.net.URISyntaxException;
import java.net.URL;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.coode.owlapi.obo.parser.OBOOntologyFormat;
import org.coode.owlapi.turtle.TurtleOntologyFormat;
import org.semanticweb.owlapi.io.OWLXMLOntologyFormat;
import org.semanticweb.owlapi.io.RDFOntologyFormat;
import org.semanticweb.owlapi.io.RDFXMLOntologyFormat;
import org.semanticweb.owlapi.model.OWLEntity;
import org.semanticweb.owlapi.util.OWLEntityRenamer;
import org.semanticweb.owlapi.apibinding.OWLManager;
import org.semanticweb.owlapi.model.AddImport;
import org.semanticweb.owlapi.model.IRI;
import org.semanticweb.owlapi.model.OWLClass;
import org.semanticweb.owlapi.model.OWLDataFactory;
import org.semanticweb.owlapi.model.OWLDataProperty;
import org.semanticweb.owlapi.model.OWLDataPropertyAssertionAxiom;
import org.semanticweb.owlapi.model.OWLImportsDeclaration;
import org.semanticweb.owlapi.model.OWLObjectProperty;
import org.semanticweb.owlapi.model.OWLOntology;
import org.semanticweb.owlapi.model.OWLOntologyCreationException;
import org.semanticweb.owlapi.model.OWLOntologyFormat;
import org.semanticweb.owlapi.model.OWLOntologyManager;
import org.semanticweb.owlapi.model.OWLOntologyStorageException;
import org.semanticweb.owlapi.model.PrefixManager;
import org.semanticweb.owlapi.model.RemoveImport;
import org.semanticweb.owlapi.reasoner.OWLReasoner;
import org.semanticweb.owlapi.reasoner.structural.StructuralReasonerFactory;
import org.semanticweb.owlapi.util.OWLEntityRemover;
import org.semanticweb.owlapi.util.SimpleIRIMapper;

import edu.pitt.ontology.IClass;
import edu.pitt.ontology.IInstance;
import edu.pitt.ontology.ILogicExpression;
import edu.pitt.ontology.IOntology;
import edu.pitt.ontology.IOntologyError;
import edu.pitt.ontology.IOntologyException;
import edu.pitt.ontology.IProperty;
import edu.pitt.ontology.IQuery;
import edu.pitt.ontology.IQueryResults;
import edu.pitt.ontology.IRepository;
import edu.pitt.ontology.IResource;
import edu.pitt.ontology.IResourceIterator;
import edu.pitt.ontology.IRestriction;
import edu.pitt.ontology.LogicExpression;
import edu.pitt.ontology.protege.PProperty;
import edu.pitt.ontology.protege.concepts.ConceptRegistry;
import edu.pitt.terminology.lexicon.Concept;

/**
 * OWL Ontology implementation
 * @author tseytlin
 *
 */
public class OOntology extends OResource implements IOntology{
	private PropertyChangeSupport pcs = new PropertyChangeSupport(this);
	private OWLOntologyManager manager;
	private OWLOntology ontology;
	private OWLDataFactory data;
	private OWLReasoner reasoner;
	private OWLEntityRemover remover;
	private OWLEntityRenamer renamer;
	private IRepository repository;
	private PrefixManager prefixManager;
	private boolean modified;
	private String location;
	private IRI locationIRI;
	
	
	/**
	 * create new ow
	 * @param ont
	 */
	private OOntology(OWLOntology ont){
		super(ont);
		manager = ont.getOWLOntologyManager();
		ontology = ont;
		data = manager.getOWLDataFactory();
		setOntology(this);
		prefixManager = manager.getOntologyFormat(ontology).asPrefixOWLOntologyFormat();
	}
	
	
	public OOntology(String location){
		super(null);
		this.location = location;
	}
	
	
	/**
	 * get prefix manager 
	 * @return
	 */
	PrefixManager getPrefixManager(){
		return prefixManager;
	}
	
	private void lazyLoad(){
		try {
			load();
		} catch (IOntologyException e) {
			throw new IOntologyError("Unable to load ontology "+location,e);
		}
	}
	
	
	public void load() throws IOntologyException {
		if(!isLoaded() && location != null){
			try{
				manager = OWLManager.createOWLOntologyManager();
				File f = new File(location);
				// this is file
				if(f.exists()){
					ontology = manager.loadOntologyFromOntologyDocument(f);
				// this is URL	
				}else if(location.matches("[a-zA-Z]+://(.*)")){
					ontology = manager.loadOntologyFromOntologyDocument(IRI.create(location));
				}
				obj = ontology;
				data = manager.getOWLDataFactory();
				setOntology(this);
				prefixManager = manager.getOntologyFormat(ontology).asPrefixOWLOntologyFormat();
				
			} catch (OWLOntologyCreationException e) {
				throw new IOntologyException("Unable to create ontology "+location,e);
			}
		}
	}
	

	private IRI inferIRI(String loc) {
		if(loc.matches("[a-zA-Z]+://(.*)"))
			return IRI.create(loc);
		File f = new File(location);
		// this is file
		if(f.exists()){
			try {
				String url = null;
				Pattern p = Pattern.compile("(ontologyIRI|xml:base)=\"(.*?)\"");
				BufferedReader r = new BufferedReader(new FileReader(f));
				for(String l = r.readLine(); l != null; l = r.readLine()){
					Matcher m = p.matcher(l);
					if(m.find()){
						url = m.group(2);
						break; 
					}
				}
				r.close();
				return IRI.create(url);
			} catch (FileNotFoundException e) {
				throw new IOntologyError("Error reading ontology from "+location,e);
			} catch (IOException e) {
				throw new IOntologyError("Error reading ontology from "+location,e);
			}
		}
		return null;
	}

	/**
	 * load ontology from file
	 * 
	 * @param file
	 * @throws Exception
	 */
	public static OOntology loadOntology(File file) throws IOntologyException {
		OWLOntologyManager manager = OWLManager.createOWLOntologyManager();
		try{
			return new OOntology(manager.loadOntologyFromOntologyDocument(file));
		} catch (OWLOntologyCreationException e) {
			throw new IOntologyException("Unable to create ontology "+file,e);
		}
	}
	
	
	/**
	 * create new ontology with this URI
	 * @param uri
	 * @return
	 * @throws Exception
	 */
	public static OOntology createOntology(URI uri) throws IOntologyException {
		OWLOntologyManager manager = OWLManager.createOWLOntologyManager();
		//manager.addOntologyStorer(new OWLXMLOntologyStorer());
		try{
			return new OOntology(manager.createOntology(IRI.create(uri)));
		} catch (OWLOntologyCreationException e) {
			throw new IOntologyException("Unable to create ontology "+uri,e);
		}
	}
	
	/**
	 * load ontology from uri
	 * 
	 * @param file
	 * @throws Exception
	 */
	public static OOntology loadOntology(URL file) throws IOntologyException {
		OWLOntologyManager manager = OWLManager.createOWLOntologyManager();
		try {
			return new OOntology(manager.loadOntologyFromOntologyDocument(IRI.create(file)));
		} catch (OWLOntologyCreationException e) {
			throw new IOntologyException("Unable to create ontology "+file,e);
		} catch (URISyntaxException e) {
			throw new IOntologyException("Unable to create ontology "+file,e);
		}
	}
	
	public void addPropertyChangeListener(PropertyChangeListener listener) {
		pcs.addPropertyChangeListener(listener);
	}
	public void removePropertyChangeListener(PropertyChangeListener listener) {
		pcs.removePropertyChangeListener(listener);
	}
	
	public void addImportedOntology(IOntology o) throws IOntologyException {
		lazyLoad();
		IRI toImport=IRI.create(o.getURI());
		OWLImportsDeclaration importDeclaraton = getOWLDataFactory().getOWLImportsDeclaration(toImport);
		getOWLOntologyManager().applyChange(new AddImport(getOWLOntology(),importDeclaraton));
		
	}
	public void removeImportedOntology(IOntology o) {
		lazyLoad();
		IRI toImport=IRI.create(o.getURI());
		OWLImportsDeclaration importDeclaraton = getOWLDataFactory().getOWLImportsDeclaration(toImport);
		getOWLOntologyManager().applyChange(new RemoveImport(getOWLOntology(),importDeclaraton));
	}
	public IOntology[] getImportedOntologies() {
		lazyLoad();
		List<IOntology> io = new ArrayList<IOntology>();
		for(OWLOntology o: ontology.getImports()){
			io.add(new OOntology(o));
		}
		return io.toArray(new IOntology [0]);
	}
	public IRepository getRepository() {
		return repository;
	}
	public void setRepository(IRepository r) {
		repository = r;
	}
	
	public IClass createClass(String name) {
		return getRoot().createSubClass(name);
	}
	public IClass createClass(ILogicExpression exp) {
		return (IClass)convertOWLObject((OWLClass)convertOntologyObject(exp));
	}
	public IProperty createProperty(String name, int type) {
		IRI iri = getIRI(name);
		switch(type){
			case(IProperty.OBJECT):
				return getTopObjectProperty().createSubProperty(name);
			case(IProperty.DATATYPE):
				return getTopDatatProperty().createSubProperty(name);
			case(IProperty.ANNOTATION_OBJECT):
			case(IProperty.ANNOTATION_DATATYPE):
			case(IProperty.ANNOTATION):
				return (IProperty) convertOWLObject(data.getOWLAnnotationProperty(iri));
		}
		return null;
	}
	public ILogicExpression createLogicExpression(int type, Object param) {
		if(param instanceof Collection)
			return new LogicExpression(type,(Collection) param);
		else if(param instanceof Object [])
			return new LogicExpression(type,(Object []) param);
		else
			return new LogicExpression(type,param);
	}
	public ILogicExpression createLogicExpression() {
		return new LogicExpression(ILogicExpression.EMPTY);
	}
	public IRestriction createRestriction(int type) {
		return new ORestriction(type, getOntology());
	}

	public IQueryResults executeQuery(IQuery iQuery) {
		throw new IOntologyError("Not implemented yet");
	}
	
	public IResourceIterator getMatchingResources(IProperty p, Object value) {
		throw new IOntologyError("Not implemented yet");
	}
	
	public IResourceIterator getMatchingResources(String regex) {
		lazyLoad();
		List<OWLEntity> list = new ArrayList<OWLEntity>();
		for(OWLEntity e: ontology.getSignature(true)){
			Pattern p = Pattern.compile(regex);
			Matcher m = p.matcher(e.getIRI().toString());
			if(m.find()){
				list.add(e);
			}
		}
		return  new OResourceIterator(list,this);
	}
	
	
	public IResource getResource(String name) {
		IRI iri = getIRI(name);
		if(ontology.containsClassInSignature(iri,true)){
			return (IClass) convertOWLObject(data.getOWLClass(iri));
		}else if(ontology.containsIndividualInSignature(iri,true)){
			return (IInstance) convertOWLObject(data.getOWLNamedIndividual(iri));
		}else if(ontology.containsAnnotationPropertyInSignature(iri,true)){
			return (IProperty) convertOWLObject(data.getOWLAnnotationProperty(iri));
		}else if(ontology.containsDataPropertyInSignature(iri,true)){
			return (IProperty) convertOWLObject(data.getOWLDataProperty(iri));
		}else if(ontology.containsObjectPropertyInSignature(iri,true)){
			return (IProperty) convertOWLObject(data.getOWLObjectProperty(iri));
		}
		return null;
	}
	public IClass getClass(String name) {
		IRI iri = getIRI(name);
		if(ontology.containsClassInSignature(iri,true))
			return (IClass) convertOWLObject(data.getOWLClass(iri));
		return null;
	}
	public IInstance getInstance(String name) {
		IRI iri = getIRI(name);
		if(ontology.containsIndividualInSignature(iri,true))
			return (IInstance) convertOWLObject(data.getOWLNamedIndividual(iri));
		return null;
	}
	public IProperty getProperty(String name) {
		IRI iri = getIRI(name);
		if(ontology.containsAnnotationPropertyInSignature(iri,true)){
			return (IProperty) convertOWLObject(data.getOWLAnnotationProperty(iri));
		}else if(ontology.containsDataPropertyInSignature(iri,true)){
			return (IProperty) convertOWLObject(data.getOWLDataProperty(iri));
		}else if(ontology.containsObjectPropertyInSignature(iri,true)){
			return (IProperty) convertOWLObject(data.getOWLObjectProperty(iri));
		}
		return null;
	}
	public boolean hasResource(String path) {
		return ontology.containsEntityInSignature(getIRI(path),true);
	}
	public IClass[] getRootClasses() {
		return getRoot().getDirectSubClasses();
	}
	public IClass getRoot() {
		return (IClass) convertOWLObject(data.getOWLThing());
	}
	public IClass getThing() {
		return (IClass) convertOWLObject(data.getOWLThing());
	}
	public IClass getNothing() {
		return (IClass) convertOWLObject(data.getOWLNothing());
	}
	public IProperty getTopObjectProperty() {
		return (IProperty) convertOWLObject(data.getOWLTopObjectProperty());
	}
	public IProperty getTopDatatProperty() {
		return (IProperty) convertOWLObject(data.getOWLTopDataProperty());
	}
	public IResourceIterator getAllResources() {
		return  new OResourceIterator(ontology.getSignature(true),this);
	}
	public IResourceIterator getAllProperties() {
		List list = new ArrayList();
		list.addAll(ontology.getDataPropertiesInSignature(true));
		list.addAll(ontology.getObjectPropertiesInSignature(true));
		list.addAll(ontology.getAnnotationPropertiesInSignature());
		return new OResourceIterator(list,this);
		
	}
	public IResourceIterator getAllClasses() {
		return new OResourceIterator(ontology.getClassesInSignature(true),this);
	}
	public boolean isLoaded() {
		return ontology != null;
	}

	public void reload() throws IOntologyException {
		dispose();
		load();
		
	}
	public void flush() {}
	
	public String getNameSpace(){
		return getIRI().toString()+"#";
	}
	public void save() throws IOntologyException {
		modified = false;
		try {
			manager.saveOntology(ontology, getIRI());
		} catch (OWLOntologyStorageException e) {
			if(e.getCause() instanceof ProtocolException)
				throw new IOntologyException("Unable to save ontology opened from URL "+getIRI()+". You should use IOntology.write() to save it as a file first.",e);
			throw new IOntologyException("Unable to save ontology "+getIRI(),e);
		}
	}
	
	public void write(OutputStream out, int format) throws IOntologyException {
		OWLOntologyFormat ontologyFormat = manager.getOntologyFormat(ontology);
		switch(format){
		case OWL_FORMAT:
			ontologyFormat = new OWLXMLOntologyFormat();break;
		case RDF_FORMAT:
			ontologyFormat = new RDFXMLOntologyFormat();break;
		case NTRIPLE_FORMAT:
			throw new IOntologyException("Unsupported export format");
		case OBO_FORMAT:
			ontologyFormat = new OBOOntologyFormat();break;
		case TURTLE_FORMAT:
			ontologyFormat = new TurtleOntologyFormat();break;
		}
		
		
		try {
			manager.saveOntology(ontology, ontologyFormat, out);
		} catch (OWLOntologyStorageException e) {
			if(e.getCause() instanceof ProtocolException)
				throw new IOntologyException("Unable to save ontology opened from URL "+getIRI()+". You should use IOntology.write() to save it as a file first.",e);
			throw new IOntologyException("Unable to save ontology "+getIRI(),e);
		}
		
	}
	public boolean isModified() {
		return modified;
	}
	
	protected OWLEntityRemover getOWLEntityRemover(){
		if(remover == null){ 
			remover = new OWLEntityRemover(manager,Collections.singleton(ontology));
		}
		return remover;
	}
	
	protected OWLEntityRenamer getOWLEntityRenamer(){
		if(renamer == null){ 
			renamer = new OWLEntityRenamer(manager,Collections.singleton(ontology));
		}
		return renamer;
	}
	
	protected OWLOntology getOWLOntology(){
		return ontology;
	}
	
	protected OWLDataFactory getOWLDataFactory(){
		lazyLoad();
		return data;
	}
	
	protected OWLOntologyManager getOWLOntologyManager(){
		lazyLoad();
		return manager;
	}
	
	protected OWLReasoner getOWLReasoner(){
		if(reasoner == null)
			reasoner = new StructuralReasonerFactory().createReasoner(ontology);
		return reasoner;
	}
	
	
	/**
	 * get appropriate concept for a given class
	 * @param cls
	 * @return
	 */
	public Concept getConcept(IClass cls){
		// lets see if we have any special concept handlers defined
		for(String pt: ConceptRegistry.REGISTRY.keySet()){
			// if regular expression or simple equals
			if((pt.matches("/.*/") && getURI().toString().matches(pt.substring(1,pt.length()-1))) ||
				pt.equals(getURI().toString())){
				String className = ConceptRegistry.REGISTRY.get(pt);
				try {
					Class c = Class.forName(className);
					return (Concept) c.getConstructors()[0].newInstance(cls);
				}catch(Exception ex){
					ex.printStackTrace();
					//NOOP, just do default
				}
			}
		}
		return new Concept(cls);
	}
	
	protected IRI getIRI(){
		if(!isLoaded()){
			if(locationIRI == null)
				locationIRI = inferIRI(location);
			return locationIRI;
		}
		return ontology.getOntologyID().getOntologyIRI();
	}
	
	

	/**
	 * convert name of resource to IRI
	 * @param name
	 * @return
	 */
	protected IRI getIRI(String name){
		if(name == null)
			return null;
		// lazy load ontology for most things
		lazyLoad();
		
		//full URI given
		if(name.indexOf("://") > -1)
			return IRI.create(name);
		//prefix given
		int of = name.indexOf(":"); 
		if( of > -1){
			String p = prefixManager.getPrefix(name.substring(0,of+1));
			return IRI.create(p+name.substring(of+1));
		}
		// just name is given
		Map<String,String> prefixes = prefixManager.getPrefixName2PrefixMap();
		for(String p: prefixes.keySet()){
			String val = prefixes.get(p);
			if(!p.equals(":") && lookupIRI(val)){
				IRI iri = getIRI(val+name);
				if(ontology.containsEntityInSignature(iri,true))
					return iri; 
			}
		}
		// use default
		return IRI.create(getNameSpace()+name);
	}
	
	private boolean lookupIRI(String val){
		final String [] generic = new String [] {"w3.org","protege.stanford.edu","purl.org","xsp.owl"};
		for(String s: generic){
			if(val.contains(s))
				return false;
		}
		return true;
	}
}
