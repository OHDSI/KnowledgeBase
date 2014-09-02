package edu.pitt.ontology.owl;


import java.beans.PropertyChangeListener;
import java.beans.PropertyChangeSupport;
import java.io.File;
import java.io.OutputStream;
import java.net.URL;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.List;
import java.util.Map;

import org.semanticweb.owlapi.apibinding.OWLManager;
import org.semanticweb.owlapi.model.IRI;
import org.semanticweb.owlapi.model.OWLClass;
import org.semanticweb.owlapi.model.OWLDataFactory;
import org.semanticweb.owlapi.model.OWLOntology;
import org.semanticweb.owlapi.model.OWLOntologyFormat;
import org.semanticweb.owlapi.model.OWLOntologyManager;
import org.semanticweb.owlapi.model.OWLOntologyStorageException;
import org.semanticweb.owlapi.model.PrefixManager;
import org.semanticweb.owlapi.reasoner.OWLReasoner;
import org.semanticweb.owlapi.reasoner.structural.StructuralReasonerFactory;
import org.semanticweb.owlapi.util.OWLEntityRemover;
import org.semanticweb.owlapi.util.OWLEntityRenamer;

import edu.pitt.ontology.IClass;
import edu.pitt.ontology.IInstance;
import edu.pitt.ontology.ILogicExpression;
import edu.pitt.ontology.IOntology;
import edu.pitt.ontology.IOntologyException;
import edu.pitt.ontology.IProperty;
import edu.pitt.ontology.IQuery;
import edu.pitt.ontology.IQueryResults;
import edu.pitt.ontology.IRepository;
import edu.pitt.ontology.IResource;
import edu.pitt.ontology.IResourceIterator;
import edu.pitt.ontology.IRestriction;
import edu.pitt.ontology.LogicExpression;
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
	private ORepository repository;
	private PrefixManager prefixManager;
	private boolean modified;
	
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
	
	/**
	 * get prefix manager 
	 * @return
	 */
	PrefixManager getPrefixManager(){
		return prefixManager;
	}

	/**
	 * load ontology from file
	 * 
	 * @param file
	 * @throws Exception
	 */
	public static OOntology loadOntology(File file) throws Exception {
		OWLOntologyManager manager = OWLManager.createOWLOntologyManager();
		return new OOntology(manager.loadOntologyFromOntologyDocument(file));
	}
	
	
	/**
	 * load ontology from uri
	 * 
	 * @param file
	 * @throws Exception
	 */
	public static OOntology loadOntology(URL file) throws Exception {
		OWLOntologyManager manager = OWLManager.createOWLOntologyManager();
		return new OOntology(manager.loadOntologyFromOntologyDocument(IRI.create(file)));
	}
	
	public void addPropertyChangeListener(PropertyChangeListener listener) {
		pcs.addPropertyChangeListener(listener);
	}
	public void removePropertyChangeListener(PropertyChangeListener listener) {
		pcs.removePropertyChangeListener(listener);
	}
	
	@Override
	public void addImportedOntology(IOntology o) throws IOntologyException {
		// TODO Auto-generated method stub
		
	}
	@Override
	public void removeImportedOntology(IOntology o) {
		// TODO Auto-generated method stub
		
	}
	public IOntology[] getImportedOntologies() {
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
		repository = (ORepository) r;
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
				return (IProperty) convertOWLObject(data.getOWLObjectProperty(iri));
			case(IProperty.DATATYPE):
				return (IProperty) convertOWLObject(data.getOWLDataProperty(iri));
			case(IProperty.ANNOTATION_OBJECT):
			case(IProperty.ANNOTATION_DATATYPE):
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
	@Override
	public IRestriction createRestriction(int type) {
		//TODO: create empty restrictions
		/*switch(type){
		case(IRestriction.ALL_VALUES_FROM):
			return (IRestriction) convertOWLObject(data.getOWLObjectAllValuesFrom(property, classExpression));
			return new ORestriction(model.createOWLAllValuesFrom(),this);
		case(IRestriction.SOME_VALUES_FROM):
			return new ORestriction(model.createOWLSomeValuesFrom(),this);
		case(IRestriction.HAS_VALUE):
			return new ORestriction(model.createOWLHasValue(),this);
		case(IRestriction.CARDINALITY):
			return new ORestriction(model.createOWLCardinality(),this);
		case(IRestriction.MAX_CARDINALITY):
			return new ORestriction(model.createOWLMaxCardinality(),this);
		case(IRestriction.MIN_CARDINALITY):
			return new ORestriction(model.createOWLMinCardinality(),this);
	}*/
	return null;
	}
	@Override
	public IQueryResults executeQuery(IQuery iQuery) {
		// TODO Auto-generated method stub
		return null;
	}
	@Override
	public IResourceIterator getMatchingResources(IProperty p, Object value) {
		// TODO Auto-generated method stub
		return null;
	}
	@Override
	public IResourceIterator getMatchingResources(String regex) {
		// TODO Auto-generated method stub
		return null;
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
	public void load() throws IOntologyException {
	}
	
	public void reload() throws IOntologyException {
		dispose();
		load();
		
	}
	public void flush() {
		//TODO:
	}
	
	public String getNameSpace(){
		return getIRI().toString()+"#";
	}
	public void save() throws IOntologyException {
		modified = false;
		try {
			manager.saveOntology(ontology, getIRI());
		} catch (OWLOntologyStorageException e) {
			throw new IOntologyException("Unable to save ontology "+getIRI(),e);
		}
	}
	
	public void write(OutputStream out, int format) throws IOntologyException {
		//TODO: handle other format
		OWLOntologyFormat ontologyFormat = manager.getOntologyFormat(ontology);
		try {
			manager.saveOntology(ontology, ontologyFormat, out);
		} catch (OWLOntologyStorageException e) {
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
		return data;
	}
	
	protected OWLOntologyManager getOWLOntologyManager(){
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
	
	
	/**
	 * convert name of resource to IRI
	 * @param name
	 * @return
	 */
	protected IRI getIRI(String name){
		if(name == null)
			return null;
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
