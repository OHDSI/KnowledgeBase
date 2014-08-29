package edu.pitt.ontology.bioportal;

import static edu.pitt.ontology.bioportal.BioPortalHelper.CHILD_COUNT;
import static edu.pitt.ontology.bioportal.BioPortalHelper.CODE;
import static edu.pitt.ontology.bioportal.BioPortalHelper.CONCEPTS;
import static edu.pitt.ontology.bioportal.BioPortalHelper.DISJOINT_CLASS;
import static edu.pitt.ontology.bioportal.BioPortalHelper.EQUIVALENT_CLASS;
import static edu.pitt.ontology.bioportal.BioPortalHelper.PROPERTIES;
import static edu.pitt.ontology.bioportal.BioPortalHelper.RELATIONSHIPS;
import static edu.pitt.ontology.bioportal.BioPortalHelper.SEMANTIC_TYPE;
import static edu.pitt.ontology.bioportal.BioPortalHelper.SUB_CLASS;
import static edu.pitt.ontology.bioportal.BioPortalHelper.SUPER_CLASS;
import static edu.pitt.ontology.bioportal.BioPortalHelper.TYPE_CLASS;
import static edu.pitt.ontology.bioportal.BioPortalHelper.deriveName;
import static edu.pitt.ontology.bioportal.BioPortalHelper.filterURL;
import static edu.pitt.ontology.bioportal.BioPortalHelper.getElementByTagName;
import static edu.pitt.ontology.bioportal.BioPortalHelper.getElementsByTagName;
import static edu.pitt.ontology.bioportal.BioPortalHelper.isReservedProperty;
import static edu.pitt.ontology.bioportal.BioPortalHelper.openURL;
import static edu.pitt.ontology.bioportal.BioPortalHelper.parseXML;

import java.io.InputStream;
import java.net.URL;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Set;

import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.NodeList;

import edu.pitt.ontology.IClass;
import edu.pitt.ontology.IInstance;
import edu.pitt.ontology.ILogicExpression;
import edu.pitt.ontology.IOntologyError;
import edu.pitt.ontology.IProperty;
import edu.pitt.ontology.IRestriction;
import edu.pitt.ontology.LogicExpression;
import edu.pitt.terminology.lexicon.Concept;
import edu.pitt.terminology.lexicon.SemanticType;
import edu.pitt.terminology.lexicon.Source;

/**
 * this represents a bioportal class
 * @author Eugene Tseytlin
 *
 */
public class BClass extends BResource implements IClass {
	private boolean loaded;
	private Concept concept;
	private Set<IClass> superClasses,subClasses;
	
	/**
	 * create new class if id is not known
	 * @param ont
	 * @param id
	 */
	public BClass(BOntology ont, String id){
		super();
		setOntology(ont);
		properties.setProperty("id",id);
		
		// setup url
		URL url = ((BioPortalRepository)ont.getRepository()).getURL();
		properties.setProperty("location",url+CONCEPTS+ont.getId()+"/"+getId());
		properties.setProperty("uri",getNameSpace()+getName());
	}

	
	
	/**
	 * create bclass from the element
	 * @param ont
	 * @param e
	 */
	BClass(BOntology ont, Element e){
		super();
		setOntology(ont);
		load(e);
	}
	
	
	/**
	 * load class content
	 * @param element
	 */
	public void load(Element element){
		// pull in all class data
		NodeList list = element.getChildNodes();
		List<Element> relations = null;
		List<Element> synonyms = null;
		List<Element> definitions = null;
		
		for(int i=0;i<list.getLength();i++){
			if(list.item(i) instanceof Element){
				Element e = (Element) list.item(i);
				String text = e.getTextContent();
				if(e.getTagName().equals("relations")){
					relations = getElementsByTagName(e,"entry");
				}else if(e.getTagName().equals("synonyms")){
					synonyms = getElementsByTagName(e,"string");
				}else if(e.getTagName().equals("definitions")){
					definitions = getElementsByTagName(e,"string");
				}else if(text != null && text.trim().length() > 0){
					//String key = RELATIONSHIPS.getProperty(e.getTagName(),e.getTagName());
					properties.put(e.getTagName(),text.trim());
				}
			}
		}
		// now set some common elements in standard way
		if(properties.containsKey("label")){
			String name = (String) properties.get("label");
			addLabel(name);
			setName(deriveName(name));
		}
		
		// now set type
		if(properties.containsKey("type")){
			resourceType = properties.getProperty("type");
		}
		
		// add synonyms
		if(synonyms != null){
			for(Element e: synonyms){
				addLabel(e.getTextContent());
			}
		}
		// add definitions
		if(definitions != null){
			for(Element e: definitions){
				addComment(e.getTextContent());
			}
		}
				
		// set locations
		BOntology ont = (BOntology) getOntology();
		URL url = ((BioPortalRepository)ont.getRepository()).getURL();
		properties.setProperty("location",filterURL(url+CONCEPTS+ont.getId()+"/"+getId()));
		properties.setProperty("uri",getNameSpace()+getName());
		
		// don't bother if in quick mode
		/*
		if(quick){
			// register class if class
			if(TYPE_CLASS.equalsIgnoreCase(getResourceType()))
				ont.registerClass(this);
			return;
		}*/
		
		
		// explore relations
		if(relations != null){
			for(Element e: relations){
				NodeList l = e.getChildNodes();
				String key = null;
				Object value = null;
				for(int i=0;i<l.getLength();i++){
					if(l.item(i) instanceof Element){
						Element c = (Element) l.item(i);
						if("string".equals(c.getTagName()) && key == null){
							key = c.getTextContent().trim();
						}else if("list".equals(c.getTagName())){
							NodeList l2 = c.getChildNodes();
							Set<String> content = new LinkedHashSet<String>();
							for(int j=0;j<l2.getLength();j++){
								if(l2.item(j) instanceof Element){
									Element e2= (Element) l2.item(j);
									if("classBean".equals(e2.getTagName())){
										BClass cls = new BClass(ontology,e2);
										content.add(cls.getName());
									}else if("string".equals(e2.getTagName()) || "int".equals(e2.getTagName())){
										content.add(e2.getTextContent());
									}else if("instanceBean".equals(e2.getTagName())){
										//TODO: handle instanceos
									}
								}
							}
							value = content;
						}else if(c.getTextContent() != null){
							// else just value
							value = c.getTextContent().trim();
						}
					}
				}
				
				// set key value
				if(key != null){
					// translate keys to some standards
					String key2 = RELATIONSHIPS.getProperty(key.toLowerCase());
					key = (key2 != null)?key2:key;
					if(value instanceof Collection){
						getList(key).addAll((Collection)value);
					}else if(value != null){
						properties.put(key,value);
					}
				}
			}
		}
		
		
		// create properties objects
		List<String> props = new ArrayList<String>();
		for(Object key: properties.keySet()){
			if(!isReservedProperty(key)){
				ont.createProperty(""+key,IProperty.ANNOTATION_DATATYPE);
				props.add(""+key);
			}
		}
		properties.put(PROPERTIES,props);
		
		// only consider it loaded when relations were available
		if(relations != null && !relations.isEmpty())
			loaded = true;
		
		// cleanup?, Please clean up...
		element = null;
		list = null;
		relations = null;
		synonyms = null;
		definitions = null;
			
		// register class if class
		if(TYPE_CLASS.equalsIgnoreCase(getResourceType()))
			ont.registerClass(this);
		
	}
	
	public void load(){
		// if not loaded 
		if(!isLoaded()){
			InputStream in = openURL(getLocation()+"?"+((BioPortalRepository)getOntology().getRepository()).getAPIKey());
			if(in != null){
				Document doc = parseXML(in);
				if(doc != null){
					load(getElementByTagName(
							doc.getDocumentElement(),"classBean"));
					// this is definately loaded
					loaded = true;
				}
			}
		}
	}
	
	/**
	 * dispose of resources
	 */
	public void dispose(){
		super.dispose();
		superClasses = subClasses = null;
		loaded = false;
		concept = null;
	}
	
	public void addDisjointClass(IClass a) {
		throw new IOntologyError("Operation Not Supported");
	}

	public void addEquivalentClass(IClass a) {
		throw new IOntologyError("Operation Not Supported");	}

	public void addEquivalentRestriction(IRestriction restriction) {
		throw new IOntologyError("Operation Not Supported");
	}

	public void addNecessaryRestriction(IRestriction restriction) {
		throw new IOntologyError("Operation Not Supported");
	}

	public void addSubClass(IClass child) {
		throw new IOntologyError("Operation Not Supported");
	}

	public void addSuperClass(IClass parent) {
		throw new IOntologyError("Operation Not Supported");
	}

	public IInstance createInstance(String name) {
		throw new IOntologyError("Operation Not Supported");
	}

	public IInstance createInstance() {
		throw new IOntologyError("Operation Not Supported");
	}

	public IClass createSubClass(String name) {
		throw new IOntologyError("Operation Not Supported");
	}

	public boolean evaluate(Object obj) {
		if(obj instanceof IClass){
			IClass c2 = (IClass) obj;
			return equals(c2) || hasSubClass(c2);
		}else if(obj instanceof IInstance){
			IInstance i2 = (IInstance) obj;
			return i2.hasType(this);
		}
		return false;
	}

	public Concept getConcept() {
		//return  new Concept(getId(),getName());
		if(concept == null){
			load();
			concept = new Concept(this);
			
			// add codes
			if(properties.containsKey(CODE)){
				Object val = properties.get(CODE);
				int i = 0;
				if(val instanceof Collection){
					for(Object o :(Collection) val)
						concept.addCode(""+o,new Source("SOURCE"+(i++)));
				}else
					concept.addCode(""+val,new Source("SOURCE"+i));
			}
			
			// add semantic types
			if(properties.containsKey(SEMANTIC_TYPE)){
				Object val = properties.get(SEMANTIC_TYPE);
				List<SemanticType> sems = new ArrayList<SemanticType>();
				if(val instanceof Collection){
					for(Object o :(Collection) val)
						sems.add(new SemanticType(""+o));
				}else
					sems.add(new SemanticType(""+val));
				concept.setSemanticTypes(sems.toArray(new SemanticType [0]));
			}
			
			
		}
		return concept;
	}

	public IInstance[] getDirectInstances() {
		return new IInstance [0];
	}

	public ILogicExpression getDirectNecessaryRestrictions() {
		return getOntology().createLogicExpression();
	}

	public boolean isLeaf(){
		String str = properties.getProperty(CHILD_COUNT,"0");
		return Integer.parseInt(str) == 0;
	}
	
	/**
	 * load list of classes
	 * @param key
	 * @return
	 */
	private Set<IClass> getClassList(String key){
		//load content
		load();
		
		// load list of classes
		Set<IClass> list = new LinkedHashSet<IClass>();
		for(String s: getList(key)){
			IClass c = ontology.getClass(s);
			if(c != null)
				list.add(c);
		}
		return list;
	}
	
	/**
	 * get direct sub classes
	 */
	public IClass[] getDirectSubClasses() {
		// get direct subclasses
		IClass [] subs =  getClassList(SUB_CLASS).toArray(new IClass [0]);
		// if not leaf, but children are not available
		// load content :)
		if(!isLeaf() && subs.length == 0){
			loaded = false;
			subs = getClassList(SUB_CLASS).toArray(new IClass [0]);
		}
		return subs;
	}
	
	public String [] getLabels(){
		load();
		return super.getLabels();
	}
	
	public String [] getComments(){
		load();
		return super.getComments();
	}
	

	public IClass [] getDirectSuperClasses() {
		//return getClassList(SUPER_CLASS).toArray(new IClass [0]);
		
		// get direct subclasses
		IClass [] subs =  getClassList(SUPER_CLASS).toArray(new IClass [0]);
		// if not leaf, but children are not available
		// load content :)
		if(subs.length == 0){
			loaded = false;
			subs = getClassList(SUPER_CLASS).toArray(new IClass [0]);
		}
		return subs;
	}

	public IClass[] getDisjointClasses() {
		return getClassList(DISJOINT_CLASS).toArray(new IClass [0]);
	}

	public IClass[] getEquivalentClasses() {
		return getClassList(EQUIVALENT_CLASS).toArray(new IClass [0]);
	}

	public ILogicExpression getEquivalentRestrictions() {
		return new LogicExpression(ILogicExpression.EMPTY);
	}

	public IInstance[] getInstances() {
		// TODO Auto-generated method stub
		return new IInstance [0];
	}

	public ILogicExpression getNecessaryRestrictions() {
		return new LogicExpression(ILogicExpression.EMPTY);
	}

	public IRestriction[] getRestrictions(IProperty p) {
		return new IRestriction [0];
	}

	/**
	 * get all subclasses
	 */
	public IClass[] getSubClasses() {
		if(subClasses == null){
			subClasses = new LinkedHashSet<IClass>();
			for(IClass c: getDirectSubClasses()){
				subClasses.add(c);
				Collections.addAll(subClasses,c.getSubClasses());
			}
		}
		return subClasses.toArray(new IClass [0]);
	}

	public IClass[] getSuperClasses() {
		if(superClasses == null){
			superClasses = new LinkedHashSet<IClass>();
			for(IClass c: getDirectSuperClasses()){
				superClasses.add(c);
				Collections.addAll(superClasses,c.getSuperClasses());
			}
		}
		return superClasses.toArray(new IClass [0]);
	}

	public boolean hasSubClass(IClass child) {
		getSubClasses();
		return subClasses.contains(child);
	}

	public boolean hasSuperClass(IClass parent) {
		getSuperClasses();
		return superClasses.contains(parent);
	}
	
	/**
	 * is child a sub class of parent
	 * @param child
	 * @return
	 */
	public boolean hasEquivalentClass(IClass child){
		return getClassList(EQUIVALENT_CLASS).contains(child);
	}
	
	
	/**
	 * is parent a direct super class of child
	 * @param parent
	 * @return
	 */
	public boolean hasDirectSuperClass(IClass parent){
		return getClassList(SUPER_CLASS).contains(parent);
	}
	
	
	/**
	 * is child a direct sub class of parent
	 * @param child
	 * @return
	 */
	public boolean hasDirectSubClass(IClass child){
		return getClassList(SUB_CLASS).contains(child);
	}

	public boolean isAnonymous() {
		return false;
	}

	public boolean hasDisjointClass(IClass a) {
		return getClassList(DISJOINT_CLASS).contains(a);
	}

	public void removeDisjointClass(IClass a) {
		throw new IOntologyError("Operation Not Supported");

	}

	public void removeEquivalentClass(IClass a) {
		throw new IOntologyError("Operation Not Supported");

	}

	public void removeEquivalentRestriction(IRestriction restriction) {
		throw new IOntologyError("Operation Not Supported");

	}

	public void removeNecessaryRestriction(IRestriction restriction) {
		throw new IOntologyError("Operation Not Supported");

	}

	public void removeSubClass(IClass child) {
		throw new IOntologyError("Operation Not Supported");
	}

	public void removeSuperClass(IClass parent) {
		throw new IOntologyError("Operation Not Supported");

	}

	public String getNameSpace(){
		return getOntology().getNameSpace();
	}
	
	public boolean isLoaded(){
		return loaded;
	}
}
