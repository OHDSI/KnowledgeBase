package edu.pitt.ontology.protege;

import java.beans.PropertyChangeListener;
import java.beans.PropertyChangeSupport;
import java.io.File;
import java.io.OutputStream;
import java.net.URI;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Properties;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.w3c.dom.Document;
import org.w3c.dom.Element;

import edu.pitt.ontology.DefaultRepository;
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
import edu.pitt.ontology.protege.concepts.ConceptRegistry;
import edu.pitt.terminology.Terminology;
import edu.pitt.terminology.lexicon.Concept;
import edu.pitt.terminology.lexicon.Relation;
import edu.pitt.terminology.lexicon.Source;
import edu.pitt.terminology.util.TerminologyException;
import edu.stanford.smi.protege.exception.OntologyLoadException;
import edu.stanford.smi.protege.model.KnowledgeBase;
import edu.stanford.smi.protege.model.KnowledgeBaseFactory;
import edu.stanford.smi.protege.model.Project;
import edu.stanford.smi.protege.util.MessageError;
import edu.stanford.smi.protege.util.PropertyList;
import edu.stanford.smi.protegex.owl.ProtegeOWL;
import edu.stanford.smi.protegex.owl.database.OWLDatabaseKnowledgeBaseFactory;
import edu.stanford.smi.protegex.owl.database.OWLDatabaseModel;
import edu.stanford.smi.protegex.owl.jena.JenaOWLModel;
import edu.stanford.smi.protegex.owl.jena.creator.NewOwlProjectCreator;
import edu.stanford.smi.protegex.owl.model.OWLIndividual;
import edu.stanford.smi.protegex.owl.model.OWLModel;
import edu.stanford.smi.protegex.owl.model.OWLNamedClass;
import edu.stanford.smi.protegex.owl.model.OWLOntology;
import edu.stanford.smi.protegex.owl.model.RDFProperty;
import edu.stanford.smi.protegex.owl.model.RDFResource;
import edu.stanford.smi.protegex.owl.model.RDFSClass;
import edu.stanford.smi.protegex.owl.model.impl.OWLUtil;
import edu.stanford.smi.protegex.owl.model.project.SettingsMap;
import edu.stanford.smi.protegex.owl.model.util.ImportHelper;
import edu.stanford.smi.protegex.owl.repository.Repository;
import edu.stanford.smi.protegex.owl.repository.RepositoryManager;
import edu.stanford.smi.protegex.owl.repository.factory.RepositoryFactory;
import edu.stanford.smi.protegex.owl.repository.impl.DatabaseRepository;
import edu.stanford.smi.protegex.owl.repository.impl.LocalFileRepository;
import edu.stanford.smi.protegex.owl.repository.impl.LocalFolderRepository;

public class POntology extends PResource implements IOntology, Terminology {
	protected OWLModel model;
	private String [] prefix;
	private Relation [] relations;
	private List<IOntology> imported;
	private IRepository repository;
	private PropertyChangeSupport pcs = new PropertyChangeSupport(this);
	
	
	public POntology(Properties meta){
		super(meta);
		setOntology(this);
	}
	
	/**
	 * create an instance of ontology with given URI
	 * @param uri
	 */
	public POntology(OWLModel model){
		this(model.getDefaultOWLOntology(),model);
	}
	
	/**
	 * create an instance of ontology with given URI
	 * @param uri
	 */
	POntology(OWLOntology ont, OWLModel model){
		super(ont);
		this.model = model;
		setOntology(this);
		
		// initialize properties
		if(info == null)
			info = new Properties();
		info.put("uri",getURI());
		info.put("location",getLocation());
	}
	
	
	/**
	 * add listener to listen to misc ontology events
	 * @param listener
	 */
	public void addPropertyChangeListener(PropertyChangeListener listener){
		pcs.addPropertyChangeListener(listener);
	}
	
	
	/**
	 * remove listener to listen to misc ontology events
	 * @param listener
	 */
	public void removePropertyChangeListener(PropertyChangeListener listener){
		pcs.removePropertyChangeListener(listener);
	}
	
		
	/**
	 * load ontology from file
	 * @param uri
	 * @return
	 */
	public static POntology loadOntology(URI uri) throws IOntologyException{
		POntology ont = null;
		if(uri.toString().endsWith(".pprj")){
			ArrayList errors = new ArrayList();
			Project project = Project.loadProjectFromURI(uri,errors);
			if(!errors.isEmpty()){
				throw new IOntologyException("Problem loading PPRJ file "+uri,getException(errors));
			}
			ont =  new POntology((OWLModel) project.getKnowledgeBase());
		}else {
			try{
				ont = new POntology(ProtegeOWL.createJenaOWLModelFromURI(""+uri));
			}catch(Exception ex){
				throw new IOntologyException("Problem loading OWL file "+uri,ex);
			}
		}
		
		// set some meta data
		if(ont != null){
			ont.getResourceProperties().setProperty("location",""+uri);
			ont.getResourceProperties().setProperty("uri",""+uri);
		}
		return ont;
	}
	
	/**
	 * lazy load ontology from URI
	 * @param uri
	 * @return
	 */
	public static POntology loadOntology(String uri) throws IOntologyException{
		Properties p = new Properties();
		p.setProperty("location",uri);
		p.setProperty("uri",uri);
		return new POntology(p);
	}
	
	/**
	 * create new ontology
	 * @param uri of this ontology
	 * @param dir dir where project/owl file should be created
	 * @return
	 * @throws IOntologyException
	 */
	public static POntology createOntology(URI path, File dir) throws IOntologyException {
		try{
			// new way to create ontology to fix xml:base issue
			Collection errors = new ArrayList();
		    NewOwlProjectCreator creator = new NewOwlProjectCreator();
		    creator.setOntologyName(""+path);
		    creator.create(errors);
		    if(!errors.isEmpty())
		    	throw new IOntologyError(""+errors);
		    OWLModel model = creator.getOwlModel();
			//OWLModel model = ProtegeOWL.createJenaOWLModel();
			
			// setup default namespace
			model.getNamespaceManager().setDefaultNamespace(path+"#");
			OWLUtil.renameOntology(model,model.getDefaultOWLOntology(),""+path);
			
			// derive file names
			String name = PUtils.getName(path);
			String filePath = ""+(new File(dir,name)).toURI();
			name = PUtils.getOntologyName(path);
			
			// set project save path
			model.getProject().setProjectFilePath((new File(dir,name+".pprj")).getAbsolutePath());
			model.getOWLProject().getSettingsMap().setString("owl_file_name",filePath);
			return new POntology(model);
		}catch(Exception ex){
			throw new IOntologyException("problem creating new ontology "+path,ex);
		}
	}
	
	/**
	 * create new ontology
	 * @param uri of this ontology
	 * @param dir dir where project/owl file should be created
	 * @return
	 * @throws IOntologyException
	 */
	public static POntology createOntology(URI path) throws IOntologyException {
		try{
			
			// new way to create ontology so that xml:base is setup propertly
			Collection errors = new ArrayList();
		    NewOwlProjectCreator creator = new NewOwlProjectCreator();
		    creator.setOntologyName(""+path);
		    creator.create(errors);
		    if(!errors.isEmpty())
		    	throw new IOntologyError(""+errors);
		    OWLModel model = creator.getOwlModel();
			//OWLModel model = ProtegeOWL.createJenaOWLModel();
			
			// setup default namespace
			model.getNamespaceManager().setDefaultNamespace(path+"#");
			OWLUtil.renameOntology(model,model.getDefaultOWLOntology(),""+path);
			
			/*
			for (Iterator it = model.getOWLOntologies().iterator(); it.hasNext();) {
				OWLOntology ont = (OWLOntology) it.next();
				System.out.println(ont);
			}
			*/
			
			return new POntology(model);
		}catch(Exception ex){
			throw new IOntologyException("problem creating new ontology "+path,ex);
		}
	}
	
	
	/**
	 * set file location for this ontology to be saved to 
	 * @param dir - this is a directory where ontology path will be saved
	 * Ex: http://www.ontologies.com/ontologies/examples/A.owl will be saved at
	 * <dir>/ontologies/examples/A.owl
	 */
	public void setFilePath(File dir){
		URI uri = getURI();
		if(!(""+uri).startsWith("http://"))
			return;
		
		// get name and path
		String name = PUtils.getOntologyName(uri);
		String path = uri.getPath();
		path = path.substring(0,path.lastIndexOf(name));
		
		// create directory
		File f = new File(dir,path.replace('/',File.separatorChar));
		if(!f.exists())
			f.mkdirs();
		String filePath = ""+(new File(f,getName())).toURI();
		
		// set project save path
		if(model != null){
			model.getProject().setProjectFilePath((new File(f,name+".pprj")).getAbsolutePath());
			model.getOWLProject().getSettingsMap().setString("owl_file_name",filePath);
			
			// add repository from potential import ontologies
			Repository rep = RepositoryFactory.getInstance().createOntRepository(model,""+f.toURI());
			if (rep != null) {
				model.getRepositoryManager().addProjectRepository(rep);
	        }
			
			// this should be here
			info.setProperty("location",filePath);
		}else if(info != null){
			info.setProperty("project.file.path",(new File(f,name+".pprj")).getAbsolutePath());
			info.setProperty("owl.file.path",filePath);
		}
		
		
	}
	
	/**
	 * set file location for this ontology to be saved to 
	 * @param dir - this is a directory where ontology path will be saved
	 */
	public void setFileLocation(File dir){
		URI uri = getURI();
		if(!(""+uri).startsWith("http://"))
			return;
		
		// get name and path
		String name = PUtils.getOntologyName(uri);
				
		// create directory
		File f = dir;
		if(!f.exists())
			f.mkdirs();
		String filePath = ""+(new File(f,getName())).toURI();
		
		// set project save path
		if(model != null){
			model.getProject().setProjectFilePath((new File(f,name+".pprj")).getAbsolutePath());
			model.getOWLProject().getSettingsMap().setString("owl_file_name",filePath);
			
			// add repository from potential import ontologies
			Repository rep = RepositoryFactory.getInstance().createOntRepository(model,""+f.toURI());
			if (rep != null) {
				model.getRepositoryManager().addProjectRepository(rep);
	        }
			
			// this should be here
			info.setProperty("location",filePath);
		}else if(info != null){
			info.setProperty("project.file.path",(new File(f,name+".pprj")).getAbsolutePath());
			info.setProperty("owl.file.path",filePath);
		}
		
		
	}
	
	
	
	/**
	 * load ontology from file
	 * @param uri
	 * @return
	 */
	public static POntology loadOntology(File uri) throws IOntologyException{
		// check if this is an pprj file
		if(uri.getName().endsWith(".pprj")){
			ArrayList errors = new ArrayList();
			Project project = Project.loadProjectFromFile(uri.getAbsolutePath(),errors);
			if(!errors.isEmpty()){
				throw new IOntologyException("Could not open "+uri,getException(errors));
			}
			return new POntology((OWLModel) project.getKnowledgeBase());
		}
		return loadOntology(uri.toURI());
	}

	/**
	 * is ontology loaded into memory
	 * @return true or false
	 */
	public boolean isLoaded(){
		return model != null;
	}
	
	/**
	 * is project modified
	 */
	public boolean isModified(){
		return (model != null)?model.hasChanged():false;
	}
	
	/**
	 * make sure model is loaded
	 *
	 */
	void checkModel(){
		try{
			load();
		}catch(IOntologyException ex){
			throw new IOntologyError("Problem loading ontology "+getURI(),ex);
		}
	}
	
	/**
	 * create new class
	 */
	public IClass createClass(String name) {
		checkModel();
		return new PClass(model.createOWLNamedClass(name),this);
	}
	
	
	/**
	 * create a class that represents this expression
	 * @param cls
	 */
	public IClass createClass(ILogicExpression exp){
		checkModel();
		return new PClass((RDFSClass)convertSetValue(exp),this);
	}
	
	
	/**
	 * create new restriction
	 */
	public IRestriction createRestriction(int type) {
		checkModel();
		switch(type){
			case(IRestriction.ALL_VALUES_FROM):
				return new PRestriction(model.createOWLAllValuesFrom(),this);
			case(IRestriction.SOME_VALUES_FROM):
				return new PRestriction(model.createOWLSomeValuesFrom(),this);
			case(IRestriction.HAS_VALUE):
				return new PRestriction(model.createOWLHasValue(),this);
			case(IRestriction.CARDINALITY):
				return new PRestriction(model.createOWLCardinality(),this);
			case(IRestriction.MAX_CARDINALITY):
				return new PRestriction(model.createOWLMaxCardinality(),this);
			case(IRestriction.MIN_CARDINALITY):
				return new PRestriction(model.createOWLMinCardinality(),this);
		}
		return null;
	}

	

	public IProperty createProperty(String name, int type) {
		checkModel();
		switch(type){
			case(IProperty.OBJECT):
				return new PProperty(model.createOWLObjectProperty(name),this);
			case(IProperty.DATATYPE):
				return new PProperty(model.createOWLDatatypeProperty(name),this);
			case(IProperty.ANNOTATION_OBJECT):
				return new PProperty(model.createAnnotationOWLObjectProperty(name),this);
			case(IProperty.ANNOTATION_DATATYPE):
				return new PProperty(model.createAnnotationOWLDatatypeProperty(name),this);
		}
		return null;
	}

	public IResourceIterator getAllClasses() {
		checkModel();
		return new PResourceIterator(model.listOWLNamedClasses(),this);
	}

	public IResourceIterator getAllProperties() {
		checkModel();
		return new PResourceIterator(model.listRDFProperties(),this);
	}

	public IResourceIterator getAllResources() {
		checkModel();
		return new PResourceIterator(model.getRDFResources().iterator(),this);
	}
	
	
	/**
	 * get descriptor for repository factory
	 * @param map
	 * @return
	 */
	private String getDescriptor(SettingsMap map){
		if(map.getString("driver") != null){
			String s = ",";
			String driver = map.getString("driver");
			String url    = map.getString("url");
			String user   = map.getString("username");
			String pass   = map.getString("password");
			String table  = map.getString("table");
			return "database:"+driver+s+url+s+user+s+pass+s+table;
		}else if(map.getString("owl_file_name") != null){
			return map.getString("owl_file_name");
		}
		return "";
	}
	
	/**
	 * get descriptor for repository factory
	 * @param map
	 * @return
	 */
	private Map<String,String> parseDescriptor(String descriptor){
		Map<String,String> map = new HashMap<String,String>();
		if(descriptor.startsWith("database:")){
			descriptor = descriptor.substring("database:".length());
			String [] fields = descriptor.split(",");
			if(fields.length >= 5){
				map.put("driver",fields[0]);
				map.put("url",fields[1]);
				map.put("username",fields[2]);
				map.put("password",fields[3]);
				map.put("table",fields[4]);
			}
		} else {
			map.put("filename",descriptor);
		}
		return map;
	}
	
	
	public void addImportedOntology(IOntology o) throws IOntologyException {
		try{
			load();
			// load ontology
			o.load();
			//model.getDefaultOWLOntology().addImports((OWLOntology)((POntology)o).getResource());
			ImportHelper importHelper = new ImportHelper((JenaOWLModel) model);
			// get repository from import ontology
			OWLModel imodel = ((POntology)o).getModel();
			//Repository rep = imodel.getRepositoryManager().getRepository(o.getURI());
			String path = getDescriptor(imodel.getOWLProject().getSettingsMap());
			// I am tired, for some reason this property may be reset and 
			// instead of full path URI it stores file name, well in this case
			// lets return location instead
			if(!path.contains("/"))
				path = o.getLocation();
			Repository rep = RepositoryFactory.getInstance().createOntRepository(imodel,path);
			if (rep != null) {
				model.getRepositoryManager().addProjectRepository(rep);
	        }
			
			/*
			for(Repository r : model.getRepositoryManager().getAllRepositories()){
				System.out.println(r.getRepositoryDescriptor()+" : "+r.getOntologies()); 
			}
			*/		
			
			// create custom prefix
			model.getNamespaceManager().setPrefix(o.getNameSpace(),PUtils.createOntologyPrefix(o.getURI()));
			
			// import ontologies
			importHelper.addImport(o.getURI());
			importHelper.importOntologies();
			 
			// don't know what is the function of this???
			//model.getNamespaceManager().setPrefix(ProtegeNames.NS, ProtegeNames.PROTEGE_PREFIX);
			if(imported == null)
				imported = new ArrayList<IOntology>();
			imported.add(o);
			
			// set prefix somewhere????
			prefix = null;
		}catch(Exception ex){
			throw new IOntologyException("failed to import "+o.getURI(),ex);
		}	
	}
	
	public String getName() {
		return PUtils.getName(getURI());
	}
	
	public IOntology[] getImportedOntologies() {
		if(imported == null){
			checkModel();
			imported = new ArrayList<IOntology>();
			OWLOntology defaultont = (OWLOntology) resource;
			Collection list = defaultont.getImportResources();
			for(Object o: list){
				if(o instanceof RDFResource){
					//TODO: maybe there is some tripplestore trick that I can use
					// and avoid loading imported ontology again
					RDFResource on = (RDFResource) o;
					PResource ont = new PResource(on);
					Repository r = model.getRepositoryManager().getRepository(ont.getURI());
					//TODO We check this because sometimes r is null. We dont understand this completely,
					//just circumventing this for now.
					if(r==null)
						continue;
					URI uri = ont.getURI();
					String location = r.getOntologyLocationDescription(uri);
					Properties map = new Properties();
					map.put("name",PUtils.getName(uri));
					map.put("version",ont.getVersion());
					map.put("description",ont.getDescription());
					map.put("uri",""+uri);
					if(r instanceof LocalFileRepository || r instanceof LocalFolderRepository){
						map.put("location",(new File(location)).toURI());
						map.put("format","file");
					}else if(r instanceof DatabaseRepository){
						Pattern pt = Pattern.compile("Table (.*) of the .*");
						Matcher mt = pt.matcher(location);
						String table = (mt.matches())?mt.group(1).trim():location;
						DatabaseRepository dr = (DatabaseRepository)r;
						map.put("format","database");
						map.put("driver",dr.getDriver());
						map.put("url",dr.getUrl());
						map.put("username",dr.getUser());
						map.put("password",dr.getPassword());
						map.put("location",table);
					//}else if(r instanceof HTTPRepository){
					}else{
						map.put("location",uri);
						map.put("format","url");
					}
					
					// add non loaded ontology
					imported.add(new POntology(map));
					
					/*
					// now lets try to play tripple store trick
					OWLModel owlModel = on.getOWLModel();
						
					// will it work?????
					TripleStoreModel tsm = owlModel.getTripleStoreModel();
				    TripleStore tripleStore = tsm.getHomeTripleStore(on);
		            tsm.setActiveTripleStore(tripleStore);
		            tsm.updateEditableResourceState();
				    
				    POntology ontology = new POntology(on,owlModel);
					ontology.setResourceProperties(map);
					
					
					//System.out.println(map);
					imported.add(ontology);
					*/
			
				}else{
					System.err.println("ERROR: WTF not recognized import: "+o.getClass().getSimpleName());
				}
			}
		}
		return imported.toArray(new IOntology [0]);
	}


	public void removeImportedOntology(IOntology o) {
		checkModel();
		((OWLOntology)resource).removeImports(""+o.getURI());
		model.flushCache();
		//TODO: do I need to reload???
		if(imported != null)
			imported.remove(o);
	}

	public IResourceIterator getMatchingResources(IProperty p, Object value) {
		//TODO: weird behavior
		checkModel();
		Collection c = model.getMatchingResources((RDFProperty)convertSetValue(p),""+value,-1);
		return new PResourceIterator(c.iterator(),this);
	}

	
	/**
	 * get resource whose name matches (contains) string
	 * @param string
	 * @return
	 */
	public IResourceIterator getMatchingResources(String str){
		checkModel();
		return new PResourceIterator(model.getResourceNameMatches("*"+str+"*",-1).iterator(),this);
	}
	
	public IQueryResults executeQuery(IQuery query) {
		checkModel();
		if(query.getLanguage() == IQuery.SPARQL){
			try{
				return new PQueryResults(model.executeSPARQLQuery(query.getQuery()));
			}catch(Exception ex){
				ex.printStackTrace();
			}
		}
		return null;
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
	

	public IProperty getProperty(String name) {
		checkModel();
		RDFProperty c = model.getRDFProperty(getResourceName(name));
		return (c != null)?new PProperty(c,this):null;
	}
	
	/**
	 * create prefixes 
	 * @return
	 */
	private String [] createPrefixes(){
		//NOTE: Protege 3.4 in its infinite wizdom seems to 
		//got rid of prefixes, hence we need to use URIs now
		List<String> list = new ArrayList<String>();
		createPrefixes(model.getDefaultOWLOntology(),list);
		return (String []) list.toArray(new String [0]);
	}
	
	/**
	 * create prefix list
	 * @param ont
	 * @param list
	 */
	private void createPrefixes(OWLOntology ont,List<String> list){
		list.add(ont.getURI()+"#");
		for(Object o : ont.getImportResources())
			if(o instanceof OWLOntology)
				createPrefixes((OWLOntology) o,list);
	}
	
	
	/**
	 * get appropriate owl resource
	 * @param name
	 * @return
	 */
	private String getResourceName(String name){
		// if this is valid name without prefix
		if(name.matches("[a-zA-Z0-9_\\-\\.]+")){
			// init prefixes
			if(prefix == null)
				prefix = createPrefixes();
			
			//check all prefixes
			for(int i=0;i<prefix.length;i++){
				if(model.getRDFResource(prefix[i]+name) != null){
					return prefix[i]+name;
				}
			}
			return name;
		// check if resource name is URI		
		//}else if(name.startsWith(getNameSpace().substring(0,5))){
		}else if(name.startsWith("http://")){	
			return model.getResourceNameForURI(name);
		}
		// else return unmodified name
		return name;
	}
	
	
	public IClass getClass(String name) {
		checkModel();
		try{
			OWLNamedClass c = model.getOWLNamedClass(getResourceName(name));
			return (c != null)?new PClass(c,this):null;
		}catch(Exception ex){
			System.err.println("WARNING: POntology.getClass("+name+") "+ex.getClass().getSimpleName()+": "+ex.getMessage());
		}
		// problem occured ClassCastException or whatever
		return null;
	}

	/**
	 * get specific instance
	 * @param name
	 * @return
	 */
	public IInstance getInstance(String name){
		checkModel();
		OWLIndividual c = model.getOWLIndividual(getResourceName(name));
		return (c != null)?new PInstance(c,this):null;
	}

	public IResource getResource(String name) {
		checkModel();
		RDFResource c = model.getRDFResource(getResourceName(name));
		return (c != null)?(IResource)convertGetValue(c):null;
	}
	


	/**
	 * get root classes (children of OWL:Thing)
	 */
	public IClass[] getRootClasses() {
		checkModel();
		return getClasses(model.getOWLThingClass().getSubclasses(false));
	}

	/**
	 * get one and only OWL system root class
	 * OWLThing
	 * @return
	 */
	public IClass getRoot(){
		checkModel();
		return new PClass(model.getOWLThingClass(),this);
	}
	
	
	public boolean hasResource(String path) {
		return getResource(path) != null;
	}

	public void write(OutputStream out, int format) throws IOntologyException {
		load();
		String lang = null;
		switch(format){
			case(RDF_FORMAT): lang = "RDF/XML"; break;
			case(OWL_FORMAT): 	 lang = "RDF/XML-ABBREV"; break;
			case(NTRIPLE_FORMAT):lang = "N-TRIPLE"; break;
			case(TURTLE_FORMAT): lang = "TURTLE"; break;
		}
		try{
			JenaOWLModel.saveModel(out,model.getOntModel(),lang,getNameSpace(),""+getURI());
			//model.getOntModel().write(out,lang,""+getURI());
		}catch(Exception ex){
			throw new IOntologyException("Problem writing protege",ex);
		}
	}
	
	
	/*
	public void read(InputStream in, int format) throws IOntologyException {
		load();
		String lang = null;
		switch(format){
			case(RDF_FORMAT): lang = "RDF/XML"; break;
			case(OWL_FORMAT): 	 lang = "RDF/XML-ABBREV"; break;
			case(NTRIPLE_FORMAT):lang = "N-TRIPLE"; break;
			case(TURTLE_FORMAT): lang = "TURTLE"; break;
		}
		try{
			//JenaOWLModel.saveModel(out,Protege2Jena.createOntModel(model),lang,getNameSpace());
			//JenaOWLModel.saveModel(out,Protege2Jena.createOntModel(model),lang,getNameSpace(),""+getURI());
			model.getOntModel().read(in,lang,null);
			model.resetJenaModel();
		}catch(Exception ex){
			throw new IOntologyException("Problem reading ontology",ex);
		}
	}
	*/

	/**
	 * persist ontology data
	 */
	public void flush() {
		if(model != null)
			model.flushCache();
	}
	
	/**
	 * persist ontology data
	 */
	public void save() throws IOntologyException {
		load();
		model.flushCache();
		ArrayList list = new ArrayList();
		model.getProject().save(list);
		if(!list.isEmpty()){
			throw new IOntologyException("Problem saving "+getURI(),getException(list));
		}
		pcs.firePropertyChange(ONTOLOGY_SAVED_EVENT,null,null);
	}
			
	/**
	 * Return list of all sources in this terminology
	 * @return
	 */
	public Source [] getSources(){
		return new Source [] { new Source(getName(),getDescription(),""+getURI())};
	}
	
	
	/**
	 * get list of sources that match some criteria
	 * '*' or 'all' means all sources
	 * Ex: NCI,SNOMED,MEDLINE will find relevant source objects in given order
	 * @param match
	 * @return
	 */
	public Source [] getSources(String matchtext){
		return getSources();
	}
	
	
	/**
	 * get list of sources that are used as a filter
	 * @return
	 */
	public Source [] getFilterSources(){
		return null;
	}
	
	
	/**
	 * Set source filter. When terminology is used only use stuff from given sources.
	 * The order of sources in Source [] array, should also determine precedence
	 * @param srcs
	 * NOTE: functionality of this call is limmited by underlying implementation
	 * of Terminology
	 */
	public void setFilterSources(Source [] srcs){
		//noop
	}
	
	
	/**
	 * Return a list of concepts that can be mapped to the input string. 
	 * The list is flat. The input string may contain several concepts.
	 * Each Concept object contains a reference to the text that concept 
	 * was mapped to as well as offset within an input string
	 * @param text to be mapped to concepts
	 * @return List of Concept objects
	 */
	public Concept[] search(String text) throws TerminologyException{
		IResourceIterator it = getMatchingResources("*"+text.replaceAll("\\W","_"));
		List<Concept> concepts = new ArrayList<Concept>();
		while(it.hasNext()){
			Object obj = it.next();
			if(obj instanceof IClass){
				concepts.add(((IClass)obj).getConcept());
			}
		}
		return (Concept []) concepts.toArray(new Concept[0]);
	}

	
	/**
	 * Return a list of concepts that can be mapped to the input string. 
	 * The list is flat. The input string may contain several concepts.
	 * Each Concept object contains a reference to the text that concept 
	 * was mapped to as well as offset within an input string
	 * @param text to be mapped to concepts
	 * @param method - search method, use getSearchMethods to see available 
	 * search methods
	 * @return List of Concept objects
	 */
	public Concept[] search(String text, String method) throws TerminologyException{
		if(method.equalsIgnoreCase("contains"))
			return search(text+"*");
		return search(text);			
	}
	
	
	/**
	 * return supported search methods for this terminology
	 * @return
	 */
	public String [] getSearchMethods(){
		return new String [] {"contains","endsWith"};
	}
	
	
	/**
	 * get array of concepts from array of classes
	 * @param clss
	 * @return
	 */
	private Concept [] getConcepts(IClass [] clss){
		Concept [] c = new Concept [clss.length];
		for(int i=0;i<c.length;i++)
			c[i] = clss[i].getConcept();
		return c;
	}
	
	/**
	 * Lookup concept information if unique identifier is available
	 * @param CUI
	 * @return Concept object
	 */
	public Concept lookupConcept(String cui) throws TerminologyException {
		IClass c = getClass(cui);
		return (c != null)?c.getConcept():null;
	}
	
	

	/**
	 * Get concepts related to parameter concept based on some relationship
	 * @param concept
	 * @param relation
	 * @return related concepts
	 */
	public Concept [] getRelatedConcepts(Concept c, Relation r) throws TerminologyException{
		return (Concept []) c.getRelatedConcepts().get(r);
	}
	
	/**
	 * Get all concepts related to parameter concept
	 * @param concept 
	 * @return Map where relation is a key and list of related concepts is a value
	 */
	public Map getRelatedConcepts(Concept c) throws TerminologyException{
		Map<Relation,Concept[]> map = new HashMap<Relation,Concept[]>();
		Relation [] r = getRelations();
		IClass cls = getClass(c.getCode());
		if(cls != null){
			map.put(r[0],getConcepts(cls.getDirectSuperClasses()));
			map.put(r[1],getConcepts(cls.getDirectSubClasses()));
			map.put(r[2],getConcepts(cls.getDisjointClasses()));
		}
		return map;
	}
	
	
	/**
	 * Get all supported relations between concepts
	 */
	public Relation[] getRelations() throws TerminologyException{
		if(relations == null){
			relations = new Relation [3];
			relations[0] = Relation.BROADER;
			relations[1] = Relation.NARROWER;
			relations[2] = new Relation("DisjointWith");
		}
		return relations;
	}

	/**
	 * Get all relations for specific concept, one actually needs to explore
	 * a concept graph (if available) to determine those
	 */
	public Relation[] getRelations(Concept c) throws TerminologyException{
		return relations;
	}
	
	/**
	 * Get all supported languages
	 */
	public String [] getLanguages(){
		return new String [] {"ENG"};
	}
	
	
	/**
	 * get all root concepts. This makes sence if Terminology is in fact ontology
	 * that has heirchichal structure
	 * @return
	 */
	public Concept[] getRootConcepts() throws TerminologyException{
		IClass [] cls = getRootClasses();
		Concept [] roots = new Concept[cls.length];
		for(int i=0;i<roots.length;i++)
			roots[i] = cls[i].getConcept();
		return roots;
	}

	
	/**
	 * 
	 */
	public String toString(){
		return getName();
	}

	
	/**
	 * @return the model
	 */
	public OWLModel getModel() {
		return model;
	}
	
	/**
	 * get all properties
	 */
	public IProperty[] getProperties() {
		checkModel();
		List<IProperty> props = new ArrayList<IProperty>();
		Collection list = model.getRDFProperties();
		for(Object o: list){
			if(!((RDFProperty)o).isSystem())
				props.add(new PProperty((RDFProperty)o,getOntology()));
		}
		return props.toArray(new IProperty [0]);
	}
	
	/**
	 * reload ontology
	 */
	public void reload() throws IOntologyException{
		dispose();
		load();
	}

	
	/**
	 * unload ontology
	 */
	public void dispose(){
		super.dispose();
		if(model != null){
			model.dispose();
			model = null;
		}	
	}
	
	/**
	 * delete ontology data
	 */
	public void delete(){
		// remove project file
		try{
			Map map = new HashMap();
			
			if(model != null){
				// get project file
				File pfile = model.getProject().getProjectFile();
				
				// copy settings
				SettingsMap settings = model.getOWLProject().getSettingsMap();
			
				for(Iterator i=settings.listKeys();i.hasNext();){
					String key = ""+i.next();
					map.put(key,settings.getString(key));
				}
				
				// dispose of object and file etc.
				model.getProject().dispose();
				
				// remove project file
				pfile.delete();
			}else{
				map.putAll(getResourceProperties());
				map.put("table",map.get("location"));
				map.put("owl_file_name",map.get("location"));
			}
			
			
			// get OWL file or database table 
			if(map.containsKey("driver")){
				// if in database
				String driver = ""+map.get("driver");
				String url    = ""+map.get("url");
				String user   = ""+map.get("username");
				String pass   = ""+map.get("password");
				String table  = ""+map.get("table");
				
				// remove data, but first dispose
				Class.forName(driver).newInstance();
		        Connection conn = DriverManager.getConnection(url, user, pass);
				Statement st = conn.createStatement();
				st.execute("DROP TABLE "+table);
				st.close();
				conn.close();
				
			}else if(map.containsKey("owl_file_name")){
				File ofile = new File(""+map.get("owl_file_name"));
				ofile.delete();
			}
			
		}catch(Exception ex){
			throw new IOntologyError("Problem removing ontology "+getName(),ex);
		}
	}
	
	
	public static class MyOWLDatabaseKnowledgeBaseFactory extends OWLDatabaseKnowledgeBaseFactory {
		public KnowledgeBase createKnowledgeBase(Collection errors) {
			OWLDatabaseModel owlModel = new OWLDatabaseModel(this){
				public URI loadImportedAssertions(URI ontologyName) throws OntologyLoadException {
					RepositoryManager rm = getRepositoryManager();
					for(Repository r: rm.getGlobalRepositories()){
						if(r instanceof DatabaseRepository)
							rm.addProjectRepository(0, r);
					}
					return super.loadImportedAssertions(ontologyName);
				}
			};
			return owlModel;
		 }
		public String getProjectFilePath() {
			return null;
		}
	}
	
	
	/**
	 * load this ontology into memory 
	 * this method loads OWL model into memory, if not already loaded
	 * if OWL model was already loaded, then this method is NOOP
	 */
	public void load() throws IOntologyException{
		if(isLoaded())
			return;
		
		long time = System.currentTimeMillis();
		ArrayList errors = new ArrayList();
		Map info = getResourceProperties();
		if(info.containsKey("driver") || "database".equals(info.get("format"))){
			URI path = getURI();
			
			// load new KB
			KnowledgeBaseFactory factory = new MyOWLDatabaseKnowledgeBaseFactory();
			Project project = Project.createBuildProject(factory, errors);
			if(!errors.isEmpty())
				throw new IOntologyException(""+errors);
			loadNewSources(project, factory);
			
			// load data
			project.createDomainKnowledgeBase(factory, errors, true);
	        if(!errors.isEmpty())
				throw new IOntologyException(""+errors);
	            
	    	model = (OWLModel) project.getKnowledgeBase();       
			
	        // make sure it is named correctly
	        model.getNamespaceManager().setDefaultNamespace(path+"#");
			OWLUtil.renameOntology(model,model.getDefaultOWLOntology(),""+path);
	 	}else{
			// load regular ontology
			String u = ""+info.get("location");
			File f = new File(u);
			URI path = (f.exists())?f.toURI():URI.create(u);
			
			// check URI path, if doesn't exist simply use URI as location
			if("file".equals(path.getScheme()) && !(new File(path)).exists())
				path = getURI();
			
			if(path.toString().endsWith(".pprj")){
				Project project = Project.loadProjectFromURI(path,errors);
				if(!errors.isEmpty()){
					throw new IOntologyException("Problem loading PPRJ file "+path+"\n",getException(errors));
				}
				model = (OWLModel) project.getKnowledgeBase();
			}else {
				try{
					model = ProtegeOWL.createJenaOWLModelFromURI(""+path);
				}catch(Exception ex){
					throw new IOntologyException("Problem loading OWL file "+path,ex);
				}
			}
			
			// set saved location if available
			if(info.containsKey("project.file.path"))
				model.getProject().setProjectFilePath(""+info.get("project.file.path"));
			if(info.containsKey("owl.file.path")){
				model.getOWLProject().getSettingsMap().setString("owl_file_name",""+info.get("owl.file.path"));
				info.put("location",info.get("owl.file.path"));
			}
			
		}
		resource = model.getDefaultOWLOntology();
		setOntology(this);
		// reset some of generic map values (in case they don't sync)
		// cause ones you load it, this is the true values
		if(info != null){
			info.put("name",getName());
			info.put("description",getDescription());
			info.put("version",getVersion());
			info.put("uri",getURI());
		}
		System.out.println(getName()+" load time is "+(System.currentTimeMillis()-time)+" ms");
		pcs.firePropertyChange(ONTOLOGY_LOADED_EVENT,null,null);
	}
	
	/**
	 * get list of errors
	 * @param errors
	 * @return
	 */
	private static Throwable getException(Collection errors){
		for(Object o: errors){
			if(o instanceof MessageError){
				return ((MessageError) o).getException();
			}
		}
		return null;
	}
	
	/**
	 * persist ontology to database (if not in one already)
	 */
	public void saveToDatabase(Map params) throws IOntologyException {
		load();
		if(info == null)
			info = new Properties();
		info.putAll(params);
		saveToDatabase();
	}
	/**
	 * get repository ontology belongs to (if available)
	 * @return
	 */
	public IRepository getRepository(){
		// if repository is empty, create empty repository
		if(repository == null){
			repository = new DefaultRepository();
			repository.addOntology(this);
		}
		return repository;
	}
	
	/**
	 * set repository ontology belongs to (if available)
	 * @return
	 */
	public void setRepository(IRepository r){
		repository = r;
	}	
	
	
	
	/**
	 * persist ontology to database (if not in one already)
	 */
	public void saveToDatabase() throws IOntologyException {
		load();
		// don't do anything if project is already in the database
		if(model instanceof OWLDatabaseModel)
			return;
		
		String prefix="";
		if(getRepository() instanceof ProtegeRepository){
			prefix = ((ProtegeRepository)getRepository()).getOntologyPrefix();
		}
	
		Project currentProject = model.getProject();
		KnowledgeBaseFactory factory = new OWLDatabaseKnowledgeBaseFactory();
        
        // load new source information
        loadNewSources(currentProject, factory);
        
        // check completeness
        if (currentProject.hasCompleteSources()) {
        	ArrayList errors = new ArrayList();
            currentProject.setIsReadonly(false);
            currentProject.save(errors);
            if(!errors.isEmpty())
            	throw new IOntologyException("problem saving "+getURI(),getException(errors));       
        }
        
        // save included projects
        /*
		IOntology [] onts = getImportedOntologies();
		for(int i=0;i<onts.length;i++){
			POntology o = (POntology) onts[i];
			o.load();
			
			//set database params
			o.getResourceProperties().put("driver",info.get("driver"));
			o.getResourceProperties().put("url",info.get("url"));
			o.getResourceProperties().put("username",info.get("username"));
			o.getResourceProperties().put("password",info.get("password"));
			o.getResourceProperties().put("location",prefix+PUtils.getOntologyName(o.getURI()).replaceAll("\\W","_"));
			
			// save database
			o.saveToDatabase();
		}
		*/
		
	}
	
	// return true if sources are complete and 'ok' was pressed
	// copy/pasted from Protege code
    private void loadNewSources(Project project, KnowledgeBaseFactory factory) {
        PropertyList sources = project.getSources();
        File   dir = (File) info.get("directory");
        
        // send a flag to url
        String driver = ""+info.get("driver");
        String url = ""+info.get("url");
        if(driver.contains("mysql") && !url.contains("relaxAutoCommit")){
        	url += ((url.lastIndexOf("?") > -1)?"&":"?")+"relaxAutoCommit=true";
        }
        
        // set project file
        File f = new File(dir,PUtils.getOntologyName(getURI())+".pprj");
        project.setProjectURI(f.toURI());
        
        // setup drivers
        OWLDatabaseKnowledgeBaseFactory.setDriver(sources,driver);
        OWLDatabaseKnowledgeBaseFactory.setURL(sources,url);
        OWLDatabaseKnowledgeBaseFactory.setTablename(sources,""+info.get("location"));
        OWLDatabaseKnowledgeBaseFactory.setUsername(sources,""+info.get("username"));
        OWLDatabaseKnowledgeBaseFactory.setPassword(sources,""+info.get("password"));
        
        sources.setString(KnowledgeBaseFactory.FACTORY_CLASS_NAME, factory.getClass().getName());
        
       
        
        //TODO: handle includes !!!
        Iterator i = Collections.EMPTY_LIST.iterator();//editor.getIncludedProjects().iterator();
        while (i.hasNext()) {
        	URI uri = (URI) i.next();
            project.includeProject(uri, false, null);
        }
    }
    
    /*
    private boolean prepareToSave(KnowledgeBaseFactory oldFactory, KnowledgeBaseFactory newFactory) {
        // Log.enter(this, "prepareToSave", oldFactory, newFactory);
        boolean succeeded = true;
        if (newFactory != null && newFactory != oldFactory && oldFactory instanceof KnowledgeBaseFactory2) {
            KnowledgeBaseFactory2 oldFactory2 = (KnowledgeBaseFactory2) oldFactory;
            Collection errors = new ArrayList();
            KnowledgeBase kb = model;
            oldFactory2.prepareToSaveInFormat(kb, newFactory, errors);
            succeeded = errors.isEmpty();
        }
        return succeeded;
    }
    */
    
    /**
	 * create logic expression 
	 * @param type
	 * @param obj if Array or Collection, fill multiple params
	 * @return
	 */
	public ILogicExpression createLogicExpression(int type, Object param){
		if(param instanceof Collection)
			return new LogicExpression(type,(Collection) param);
		else if(param instanceof Object [])
			return new LogicExpression(type,(Object []) param);
		else
			return new LogicExpression(type,param);
	}
	
	/**
	 * create logic expression 
	 * @param type
	 * @param obj if Array or Collection, fill multiple params
	 * @return
	 */
	public ILogicExpression createLogicExpression(){
		return new LogicExpression(ILogicExpression.EMPTY);
	}
	
	
	/**
	 * add new concept to the terminology
	 * @param c
	 */
	public boolean addConcept(Concept c) throws TerminologyException{
		throw new TerminologyException("Not implemented");
	}
	
	/**
	 * update concept information
	 * @param c
	 */
	public boolean updateConcept(Concept c) throws TerminologyException{
		throw new TerminologyException("Not implemented");
	}
	
	/**
	 * remove existing concept
	 * @param c
	 */
	public boolean removeConcept(Concept c) throws TerminologyException{
		throw new TerminologyException("Not implemented");
	}
	
	/**
	 * get location
	 * @return
	 */
	public String getFormat(){
		Object l = getResourceProperties().get("format");
		if(l != null)
			return ""+l;
		
		// else query project
		if(model != null){
			SettingsMap map = model.getOWLProject().getSettingsMap();
			if(map.getString("table") != null){
				return "database";
			}else if(map.getString("owl_file_name") != null){
				return "file";
			}
		}
		return "";
	}
	
	
	/**
	 * get location
	 * @return
	 */
	public String getLocation(){
		Object l = getResourceProperties().get("location");
		if(l != null)
			return ""+l;
		
		// else query project
		if(model != null){
			SettingsMap map = model.getOWLProject().getSettingsMap();
			if(map.getString("table") != null){
				return map.getString("table");
			}else if(map.getString("owl_file_name") != null){
				return map.getString("owl_file_name");
			}
		}
		return "";
	}
	
	/**
	 * get all available version of this ontolgy
	 * the first entry is the current version, entries after that are previous versions
	 * If given IRepository supports multiple versions of ontologies, you can append this version
	 * number to ontology URL to get the desired version
	 * Example: IRepository.getOntology("http://wwww.ontologies.com/TestOntology.owl#1.1")
	 * @return list of version
	 */
	public String getVersion(){
		String s = super.getVersion();
		return (s != null)?s:"1.0";
	}
	
	/**
	 * get all available concept objects in terminology. Only sensible for small terminologies
	 * @return
	 */
	public Collection<Concept> getConcepts()  throws TerminologyException{
		List<Concept> concepts = new ArrayList<Concept>();
		for(IResourceIterator it = getAllClasses();it.hasNext();){
			Object r = it.next();
			if(r instanceof IClass){
				concepts.add(((IClass)r).getConcept());
			}
		}
		return concepts;
	}
	
	/**
	 * convert Template to XML DOM object representation
	 * @return
	 */
	public Element toElement(Document doc)  throws TerminologyException{
		Element root = doc.createElement("Terminology");
		
		root.setAttribute("name",getName());
		root.setAttribute("version",getVersion());
		root.setAttribute("location",getLocation());
		root.setAttribute("format",getFormat());
		root.setAttribute("uri",""+getURI());
		
		Element desc = doc.createElement("Description");
		desc.setTextContent(getDescription());
		root.appendChild(desc);
		
		Element sources = doc.createElement("Sources");
		root.appendChild(sources);
		for(Source c: getSources()){
			sources.appendChild(c.toElement(doc));
		}
		
		Element relations = doc.createElement("Relations");
		root.appendChild(relations);
		for(Relation c: getRelations()){
			relations.appendChild(c.toElement(doc));
		}
		
		Element concepts = doc.createElement("Concepts");
		root.appendChild(concepts);
		for(Concept c: getConcepts()){
			concepts.appendChild(c.toElement(doc));
		}
		
		return root;
	}
	
	/**
	 * convert Template to XML DOM object representation
	 * @return
	 */
	public void fromElement(Element element) throws TerminologyException{
		throw new TerminologyException("Not implemented");
	}
	
}
