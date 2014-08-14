package edu.pitt.ontology.protege;

import java.awt.Dimension;
import java.beans.PropertyChangeListener;
import java.beans.PropertyChangeSupport;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.URI;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Properties;

import javax.swing.JFrame;

import edu.pitt.ontology.IClass;
import edu.pitt.ontology.IOntology;
import edu.pitt.ontology.IOntologyException;
import edu.pitt.ontology.IReasoner;
import edu.pitt.ontology.IRepository;
import edu.pitt.ontology.IResource;
import edu.pitt.terminology.RemoteTerminology;
import edu.pitt.terminology.Terminology;
import edu.pitt.terminology.client.IndexFinderTerminology;
import edu.pitt.terminology.client.LexEVSRestTerminology;
import edu.pitt.terminology.util.TerminologyException;
import edu.stanford.smi.protege.ui.ProjectManager;
import edu.stanford.smi.protege.util.ComponentFactory;
import edu.stanford.smi.protegex.owl.ProtegeOWL;


public class ProtegeRepository implements IRepository {
	public static final String ADDED_EVENT = "ADDED";
	public static final String REMOVED_EVENT = "REMOVED";
	
	private final String ONTOLOGY_PREFIX_DEFAULT = "ontology_";
	private final String CONFIGURATION = "configuration";
	private final String REPOSITORY = "global.repository";
	private Map<String, Map> repository;
	private List ontologies;
	private List terminologies;
	private File directory; //,configurationFile;
	private PropertyChangeSupport pcs = new PropertyChangeSupport(this);
	
	private String ontologyPrefix = ONTOLOGY_PREFIX_DEFAULT;
	
	
	public String getOntologyPrefix() {
		return ontologyPrefix;
	}

	public void setOntologyPrefix(String ontologyPrefix) {
		this.ontologyPrefix = ontologyPrefix;
	}

	/**
	 * instanciate protege repository  with config file
	 * @param config
	 *
	public ProtegeRepository(String config) throws IOntologyException{
		readConfig(config);
		setupGlobalRepository();
		System.out.println(repository);
	}
	*/
	/**
	 * instanciate protege repository  with database connection
	 * @param config
	 */
	public ProtegeRepository(String driver,String url, String user, String pass, String table, String dir) throws IOntologyException{
		readConfig(driver,url,user,pass,table,dir);
		setupGlobalRepository();
	}
	
	
	
	
	/**
	 * save global repository file
	 */
	private void setupGlobalRepository(){
		// set custom plugin folder
		try{
			System.setProperty("protege.dir",directory.getAbsolutePath());
		}catch(Exception ex){
			// do nothing on security exception, not such a bid deal anyway
		}
		// create plugin folder
		File plugin = new File(directory,"plugins");
		if(!plugin.exists())
			plugin.mkdirs();
		
		// create OWL plugin folder
		File owl = new File(plugin,"edu.stanford.smi.protegex.owl");
		if(!owl.exists())
			owl.mkdir();
	
		// set plugin folder
		ProtegeOWL.setPluginFolder(owl);
		
		Map conf = repository.get(CONFIGURATION);
		StringBuffer buf = new StringBuffer("database:");
		buf.append(conf.get("driver")+",");
		buf.append(conf.get("url")+",");
		buf.append(conf.get("username")+",");
		buf.append(conf.get("password")+",");
		IOntology [] ont = getOntologies();
		for(int i=0;i<ont.length;i++){
			Map map = repository.get(""+ont[i].getURI());
			if(map != null && "database".equals(map.get("format"))){
				buf.append(map.get("location")+",");
			}
		}
		try{
			File f = new File(owl,REPOSITORY);
			BufferedWriter writer = new BufferedWriter(new FileWriter(f));
			writer.write(buf.substring(0,buf.length()-1)+"\n");
			writer.close();
		}catch(IOException ex){
			ex.printStackTrace();
		}
		
		// put a dependency .owl file
		File protege_dc = new File(owl,"protege-dc.owl");
		if(!protege_dc.exists()){
			try{
				InputStream is = getClass().getResourceAsStream("/resources/protege-dc.owl");
				if(is != null){
					BufferedWriter writer = new BufferedWriter(new FileWriter(protege_dc));
					BufferedReader reader = new BufferedReader(new InputStreamReader(is));
					for(String line = reader.readLine();line != null; line=reader.readLine()){
						writer.write(line+"\n");
					}
					reader.close();
					writer.close();
					is.close();
				}
			}catch(IOException ex){
				ex.printStackTrace();
			}
		}
	}
	
	/**
	 * read config file
	 * @param path
	 * @return
	 * @throws IOntologyException
	 *
	private void readConfig(String config) throws IOntologyException{
		try{
			configurationFile = new File(config); 
			directory = configurationFile.getParentFile();
			BufferedReader reader = new BufferedReader(new FileReader(configurationFile));
			Pattern pt = Pattern.compile("\\[(.*)\\]");
			Map map = null;
			repository = new LinkedHashMap<String,Map>();
			ontologies = new ArrayList();
			terminologies = new ArrayList();
			// iterate through config file
			for(String line =reader.readLine();line != null;line = reader.readLine()){
				// trim line and skip blanks
				line = line.trim();
				if(line.length() == 0 || line.startsWith("#"))
					continue;
				
				// check headings
				Matcher mt = pt.matcher(line);
				if(mt.matches()){
					String name = mt.group(1).trim();
					map = new HashMap();
					map.put("name",name);
					repository.put(name,map);
				}else {
					// parse kev/value pairs
					int i = line.indexOf("=");
					if(i > 0 && i<line.length()-1){
						String key = line.substring(0,i).trim();
						String val = line.substring(i+1).trim();
						
						// put into config
						map.put(key,val);
					}
				}
			}
			reader.close();
			
			// do some post processing on the config
			for(Object key : new ArrayList(repository.keySet())){
				map = (Map) repository.get(key);
				if(key.equals(CONFIGURATION)){
					String s = ""+map.get("directory");
					map.put("directory",(s.length() > 0)?new File(s):directory);
				}else if(map.get("type").equals(IRepository.TYPE_ONTOLOGY) ||
						map.get("type").equals(IRepository.TYPE_SYSTEM_ONTOLOGY)){
					// take care of ontology
					if((""+map.get("format")).equals(IRepository.FORMAT_FILE)){
						map.put("location",(new File(directory,""+map.get("location"))).toURI());
					}else if((""+map.get("format")).equals(IRepository.FORMAT_DATABASE)){
						map.putAll((Map)repository.get(CONFIGURATION));
					}
					map.put("uri",URI.create(""+map.get("uri")));
					IOntology ont = new POntology(createProperties(map));
					ont.setRepository(this);
					map.put("object",ont);
					ontologies.add(map.get("object"));
					repository.put(""+map.get("uri"),map);
				}else if(map.get("type").equals(IRepository.TYPE_TERMINOLOGY)){
					if((""+map.get("format")).equals("evs")){
						map.put("object",new LexEVSTerminology(""+map.get("location")));
						terminologies.add(map.get("object"));
						repository.put(""+map.get("uri"),map);
					}else if((""+map.get("format")).equalsIgnoreCase("HTTP")){
						map.put("object",new RemoteTerminology(URI.create(""+map.get("location")).toURL()));
						terminologies.add(map.get("object"));
						repository.put(""+map.get("uri"),map);
					}
				}
			}
			
			// now parse each individual resource
		}catch(Exception ex){
			//ex.printStackTrace();
			throw new IOntologyException("Could not initialize protege repository from config file "+config,ex);
		}
	}
	*/
	
	/**
	 * if repository table doesn't exist, create and repopulate it
	 * 
	 */
	private void createRepositoryTable(Connection conn,String table) throws SQLException{
		//boolean need2create = true;
		/*
		ResultSet result = null;
		Statement st = null;
		try{
			st = conn.createStatement();
			result = st.executeQuery("SELECT * FROM "+table);
			// if there is something in table, then it exists
			// hence no need to create it
			if(result.next())
				need2create = false;
		}catch(Exception ex){
			
		}finally{
			if(st != null)
				st.close();
			if(result != null)
				result.close();
		}
		
		// if doesn't exist, quit
		if(!need2create)
			return false;
		*/
		// create table if doesn't exist
        Statement st = conn.createStatement();
        st.execute( "CREATE TABLE IF NOT EXISTS  "+table+" ("+
	        	    "id  INT(10) unsigned NOT NULL AUTO_INCREMENT,"+
	        		"uri VARCHAR(512) NOT NULL,"+
	        		"name VARCHAR(45) NOT NULL,"+
	        		"type VARCHAR(45) NOT NULL,"+
	        		"location VARCHAR(1024) NOT NULL,"+
	        		"format VARCHAR(45) NOT NULL,"+
	        		"description VARCHAR(1024) DEFAULT NULL,"+
	        		"version VARCHAR(45) DEFAULT NULL,"+
	        		"PRIMARY KEY (id))");
        st.close();
        //return need2create;
    }
	
	/**
	 * check if running mysql
	 * @param config
	 * @return
	 */
	private boolean isMySQL(Map config){
		return (""+config.get("driver")).indexOf("mysql") > -1;
	}
	
	
	/**
	 * scan repository table
	 * @param conn
	 * @param table
	 * @throws SQLException
	 */
	private void populateRepositoryTable(Connection conn, String table) throws SQLException {
		// check if running mysql
		if(isMySQL(repository.get(CONFIGURATION))){
			// create table if doesn't exist
	        Statement st = conn.createStatement();
	        ResultSet result = st.executeQuery("SHOW TABLES");
	        List<String> tables = new ArrayList<String>();
	        while(result.next()){
	        	String t = result.getString(1);
	        	if(!t.equals(table))
	        		tables.add(t);
	        }
	        result.close();
	        st.close();
	        
	        // if there are table figure out if they are in correct format
	        for(String tb : tables){
	        	String uri = null;
	        	try{
	        		st = conn.createStatement();
	        		result = st.executeQuery("SELECT frame,short_value FROM "+tb+
	        								 " WHERE frame LIKE '%www.w3.org%Ontology'");
	        		if(result.next()){
	        			uri = result.getString("short_value");
	        		}
	        		result.close();
	        		st.close();
	        	}catch(Exception ex){
	        		//ex.printStackTrace();
	        	}
	        	
	        	// if URI is not NULL then we have an ontology table
	        	if(uri != null){
	        		String version="", desciption="";
	        		st = conn.createStatement();
	        		result = st.executeQuery("SELECT frame,slot,short_value,long_value FROM "+tb+
	        				" WHERE frame='"+uri+"' AND slot NOT LIKE '%OWL-ONTOLOGY-PREFIXES'");
	        		while(result.next()){
	        			String slot = result.getString("slot");
	        			String val =  result.getString("short_value");
	        			if(val == null)
        					val = result.getString("long_value");
	        			// if we see comment
	        			if(slot.endsWith("#comment")){
	        				desciption = val;
	        			// if we see version
	        			}else if(slot.endsWith("#versionInfo")){
	        				version = val;
	        			}
	        		}
	        		result.close();
	        		st.close();
	        		
	        		
	        		// now insert an Entry
	        		Map map = new HashMap();
	        		map.put("name",PUtils.getName(URI.create(uri)));
	        		map.put("uri",uri);
	        		map.put("version",version);
	        		map.put("description",desciption);
	        		map.put("type","ontology");
	        		map.put("format","database");
	        		map.put("location",tb);
	        		 
	        		insertEntry(conn,table,map);
	        	}
	        }
		}
	}
	
	/**
	 * scan repository table
	 * @param conn
	 * @param table
	 * @throws SQLException
	 */
	private void scanRepositoryTable(Connection conn, String table) throws SQLException {
		//	read data from table
        Statement st = conn.createStatement();
		ResultSet result = st.executeQuery("SELECT * FROM "+table);
		ResultSetMetaData meta = result.getMetaData();
		while(result.next()){
			Map map = new HashMap();
			for(int i=1;i<=meta.getColumnCount();i++){
				String name = meta.getColumnName(i);
				if(meta.getColumnClassName(i).contains("String"))
					map.put(name,result.getString(name));
				else if(name.equals("id"))
					map.put(name,new Integer(result.getInt(name)));
			}
			repository.put(""+map.get("uri"),map);
		}
		st.close();
		result.close();
		
		debugPrintRepositoryTable();
	
	}
	
	private void debugPrintRepositoryTable(){
		//for(Object k : repository.keySet())
		//	System.out.println(k+"\n"+repository.get(k)+"\n");
	}
	
	/**
	 * get database driver
	 * @return
	 */
	public String getDatabaseDriver(){
		Object s = (repository != null && repository.containsKey(CONFIGURATION))?repository.get(CONFIGURATION).get("driver"):null;
		return (s != null)?s.toString():null;
	}
	
	/**
	 * get database driver
	 * @return
	 */
	public String getDatabaseURL(){
		Object s = (repository != null && repository.containsKey(CONFIGURATION))?repository.get(CONFIGURATION).get("url"):null;
		return (s != null)?s.toString():null;
	}
	
	/**
	 * get database driver
	 * @return
	 */
	public String getDatabaseUsername(){
		Object s = (repository != null && repository.containsKey(CONFIGURATION))?repository.get(CONFIGURATION).get("username"):null;
		return (s != null)?s.toString():null;
	}
	
	/**
	 * get database driver
	 * @return
	 */
	public String getDatabasePassword(){
		Object s = (repository != null && repository.containsKey(CONFIGURATION))?repository.get(CONFIGURATION).get("password"):null;
		return (s != null)?s.toString():null;
	}
	
	/**
	 * get database driver
	 * @return
	 */
	public String getDatabaseRepositoryTable(){
		Object s = (repository != null && repository.containsKey(CONFIGURATION))?repository.get(CONFIGURATION).get("repository"):null;
		return (s != null)?s.toString():null;
	}
	
	
	/**
	 * get database driver
	 * @return
	 */
	public String getDatabaseRepositoryDirectory(){
		Object s = (repository != null && repository.containsKey(CONFIGURATION))?repository.get(CONFIGURATION).get("directory"):null;
		return (s != null)?s.toString():null;
	}
	
	/**
	 * read config file
	 * @param path
	 * @return
	 * @throws IOntologyException
	 */
	private void readConfig(String driver,String url, String user, String pass, String table, String dir) throws IOntologyException{
		try{
			directory = new File(dir);
			repository = new LinkedHashMap<String,Map>();
			ontologies = new ArrayList();
			terminologies = new ArrayList();
			
			// create dir if doesn't exists
			if(!directory.exists()){
				directory.mkdirs();
			}
			
			// setup configuration object
			Map map = new HashMap();
			map.put("driver",driver);
			map.put("url",url);
			map.put("username",user);
			map.put("password",pass);
			map.put("repository",table);
			map.put("directory",directory);
			repository.put(CONFIGURATION,map);
			
			// read in ontology data from table
			Class.forName(driver).newInstance();
	        Connection conn = DriverManager.getConnection(url,user, pass);
			
	        // create table if doesn't exist
	        //if(createRepositoryTable(conn,table)){
	        	//populate table
			//	populateRepositoryTable(conn, table);
	        //}
	        createRepositoryTable(conn, table);
	        
			// read data from table
	        scanRepositoryTable(conn, table);
	        
	        if(repository.keySet().size() <= 1){
	        	populateRepositoryTable(conn, table);
	        	scanRepositoryTable(conn, table);
	        }
			
			// close connection
			conn.close();
			
			// do some post processing on the config
			for(Object key : new ArrayList(repository.keySet())){
				map = (Map) repository.get(key);
				if(key.equals(CONFIGURATION)){
					// don't do anything for configuration
				}else if((""+map.get("type")).equals(IRepository.TYPE_ONTOLOGY) ||
						map.get("type").equals(IRepository.TYPE_SYSTEM_ONTOLOGY)){
					// take care of ontology
					if((""+map.get("format")).equals(IRepository.FORMAT_FILE)){
						String location = ""+map.get("location");
						URI u = null;
						// if NOT (URL or absolute path), then use default location for location
						if(!(location.contains("/") || location.contains(File.separator)))
							u  = (new File(dir,location)).toURI();
						else
							u = URI.create(location);
						map.put("location",u);
					}else if((""+map.get("format")).equals(IRepository.FORMAT_DATABASE)){
						map.putAll((Map)repository.get(CONFIGURATION));
					}
					map.put("uri",URI.create(""+map.get("uri")));
					IOntology ont = new POntology(createProperties(map));
					ont.setRepository(this);
					map.put("object",ont);
					ontologies.add(map.get("object"));
					repository.put(""+map.get("uri"),map);
				}else if((""+map.get("type")).equals(IRepository.TYPE_TERMINOLOGY)){
					if((""+map.get("format")).equalsIgnoreCase("EVS")){
						map.put("object",new LexEVSRestTerminology(""+map.get("location")));
						terminologies.add(map.get("object"));
						repository.put(""+map.get("uri"),map);
					}else if((""+map.get("format")).equalsIgnoreCase("HTTP")){
						map.put("object",new RemoteTerminology(URI.create(""+map.get("location")).toURL()));
						terminologies.add(map.get("object"));
						repository.put(""+map.get("uri"),map);
					}
				}
			}
			
			//System.out.println(repository);
			
			// now parse each individual resource
		}catch(Exception ex){
			throw new IOntologyException("Could not connect to Protege Database Repository "+url,ex);
			//ex.printStackTrace();
		}
	}
	
	/**
	 * create properties
	 * @param map
	 * @return
	 */
	private Properties createProperties(Map map){
		Properties p = new Properties();
		p.putAll(map);
		return p;
	}
	
	/**
	 * update entry
	 * @param map
	 */
	private void removeEntry(Connection conn,String table, int id) throws SQLException{
		Statement st = conn.createStatement();
		st.executeUpdate("DELETE FROM "+table+" WHERE id="+id);
		st.close();
	}
	
	
	/**
	 * update entry
	 * @param map
	 */
	private void updateEntry(Connection conn, String table,Map map) throws SQLException{
		String [] keys = new String [] {"name","uri","type","location","format","description","version"};
		//create statement
		String sql = "UPDATE "+table+" SET name=?, uri=?, type=?, location=?, format=?, description=?, version=? WHERE id="+map.get("id");
		PreparedStatement st = conn.prepareStatement(""+sql);
		//iterate over specific keys to update
		for(int i=0;i<keys.length;i++){
			st.setString(i+1,""+map.get(keys[i]));
		}
		st.executeUpdate();
		st.close();
	}
	
	/**
	 * update entry
	 * @param map
	 */
	private void insertEntry(Connection conn, String table, Map map) throws SQLException{
		String [] keys = new String [] {"name","uri","type","location","format","description","version"};
		
		StringBuffer sql = new StringBuffer("INSERT INTO "+table+" (");
		//add which values you wish to add
		for(int i=0;i<keys.length;i++){
			sql.append(" "+keys[i]+((i<keys.length-1)?",":""));
		}
		sql.append(") VALUES (?,?,?,?,?,?,?)");
		PreparedStatement st = conn.prepareStatement(""+sql);
		// add values
		for(int i=0;i<keys.length;i++){
			st.setString(i+1,""+map.get(keys[i]));
		}
		
		st.executeUpdate();
		st.close();
		
		// get the last inserted entry
		Statement st1 = conn.createStatement();
		ResultSet result = st1.executeQuery("SELECT MAX(id) FROM "+table);
		if(result.next()){
			int i = result.getInt(1);
			map.put("id",new Integer(i));
		}
		result.close();
		st1.close();
	}
	
	/**
	 * save DB config
	 *
	 */
	private void writeDBConfig(int [] ids){
		try{
			Map config = repository.get(CONFIGURATION);
			String driver = ""+config.get("driver");
			String url = ""+config.get("url");
			String user = ""+config.get("username");
			String pass = ""+config.get("password");
			String table = ""+config.get("repository");
			
			// read in ontology data from table
			Class.forName(driver).newInstance();
	        Connection conn = DriverManager.getConnection(url,user, pass);
			
	        // remove entries that are marked for removal
	        if(ids != null && ids.length > 0){
	        	for(int i=0;i<ids.length;i++)
	        		removeEntry(conn,table,ids[i]);
	        }
	        
			// iterate over keys in repository
			for(String key : new ArrayList<String>(repository.keySet())){
				Map map = (Map) repository.get(key);
				// skip configuration key and but not URI keys
				//&& !key.startsWith("http://")
				if(!key.equals(CONFIGURATION)){
					//System.out.println("updating "+key+" "+map);
					// we need to do an update
					if( map.get("id") != null){
						updateEntry(conn,table,map);
					}else{
						insertEntry(conn,table,map);
					}
				}
			}
			
			conn.close();
		}catch(Exception ex){
			ex.printStackTrace();
		}
	}
	
	/**
	 * read config file
	 * @param path
	 * @return
	 * @throws IOntologyException
	 *
	private void writeConfig(int [] ids){
		// do database thing
		if(configurationFile == null){
			writeDBConfig(ids);
			return;
		}
		// do file based thing
		try{
			List filter = Arrays.asList(new String [] {"driver","url","username","password","object"});
			BufferedWriter writer = new BufferedWriter(new FileWriter(configurationFile));
			for(Object key : new ArrayList(repository.keySet())){
				// skip uri keys
				if(!(""+key).contains("/")){
					Map map = (Map) repository.get(key);
					//write it out
					writer.write("["+key+"]"+"\n");
					for(Object o: map.keySet()){
						//filter out some keys
						if(key.equals(CONFIGURATION) || !filter.contains(o)){
							String val = ""+map.get(o);
							if(o.equals("location") && map.get("type").equals("ontology")){
								int i=val.lastIndexOf("/");
								val = (i > -1)?val.substring(i+1):val;
							}
							writer.write(o+" = "+val+"\n");
						}
					}
					writer.write("\n");
				}
			}
			writer.close();
		}catch(Exception ex){
			ex.printStackTrace();
		}
	}
	
	*/
	/**
	 * create new ontology
	 */
	public IOntology createOntology(URI path)  throws IOntologyException {
		IOntology ont =  POntology.createOntology(path, directory);
		ont.setRepository(this);
		return ont;
	}

	
	public Terminology createTerminology() throws TerminologyException {
		return new IndexFinderTerminology();
	}
	
	
	
	public void exportOntology(IOntology ont, int format, OutputStream out) throws IOntologyException{
		ont.write(out,format);
	}

	public IOntology[] getOntologies() {
		return (IOntology []) ontologies.toArray(new IOntology[0]);
	}

	/**
	 * get ontologies that are loaded in repository
	 * @return
	 */
	public IOntology [] getOntologies(String name){
		ArrayList<IOntology> onts = new ArrayList<IOntology>();
		for(IOntology o : getOntologies()){
			if(o.getURI().toString().contains(name)){
				onts.add(o);
			}
		}
		return onts.toArray(new IOntology [0]);
	}
	
	
	public IOntology getOntology(URI path) {
		Map map = (Map) repository.get(""+path);
		if(map != null){
			return (IOntology) map.get("object");
		}
		return null;
	}
	
	/**
	 * get a specific  terminologies
	 * @return
	 */
	public Terminology getTerminology(String path){
		Map map = (Map) repository.get(path);
		if(map != null){
			return (Terminology) map.get("object");
		}
		return null;
		
	}
	
	
	/**
	 * get specific ontology if path is known
	 * @param URI path or name
	 * @return Ontology
	 */
	public boolean hasOntology(String name){
		return repository.containsKey(name);
	}
	

	public Terminology [] getTerminologies() {
		return 	(Terminology []) terminologies.toArray(new Terminology[0]);
	}

	/**
	 * add property change listener
	 * @param listener
	 */
	public void addPropertyChangeListener(PropertyChangeListener listener){
		pcs.addPropertyChangeListener(listener);
	}
	
	
	/**
	 * add property change listener
	 * @param listener
	 */
	public void removePropertyChangeListener(PropertyChangeListener listener){
		pcs.removePropertyChangeListener(listener);
	}
	
	/**
	 * add ontology to repository
	 * @param ont
	 */
	public void removeOntology(IOntology o){
		if(o == null)
			return;
		
		int [] ids = null;
		
		// get sql id if in database mode
		Map map = repository.get(""+o.getURI());
		Integer id = (Integer) map.get("id");
		if(id != null){
			ids = new int [] {id.intValue()};
		}
		
		// remove from registry
		//repository.remove(o.getName());
		repository.remove(""+o.getURI());
		ontologies.remove(o);
			
		// notify of change
		pcs.firePropertyChange(REMOVED_EVENT,null,o.getURI());
		
		// write configuration
		writeDBConfig(ids);
	}
	
	/**
	 * add ontology to repository
	 * @param ont
	 */
	public void addOntology(IOntology o){
		POntology ont = (POntology) o;
		ont.setRepository(this);
		Map meta = ont.getResourceProperties();
		
		// remember old ids
		int [] ids = null;
		
		// get sql id if in database mode
		Map map = repository.get(""+o.getURI());
		if(map != null){
			Integer id = (Integer) map.get("id");
			if(id != null){
				ids = new int [] {id.intValue()};
			}
		}
		
		// setup a map
		map = new HashMap();
		map.put("type",IRepository.TYPE_ONTOLOGY);
		map.put("name",o.getName());
		map.put("uri",o.getURI());
		map.put("version",o.getVersion());
		map.put("description",o.getDescription());
		map.put("object",o);
		
		
		// check if database
		if(meta.containsKey("driver")){
			map.put("format","database");
			map.put("location",meta.get("location"));
		}else{
			map.put("format","file");
			String location = (String) meta.get("location");
			if(location == null)
				map.put("location",ont.getModel().getProject().getProjectURI());
			else
				map.put("location",location);
		}
		
		// map things to repository
		//repository.put(o.getName(),map);
		repository.put(""+o.getURI(),map);
		ontologies.add(o);
		pcs.firePropertyChange(ADDED_EVENT,null,o.getURI());
		
		//System.out.println(repository);
		//write configuration
		writeDBConfig(ids);
		setupGlobalRepository();
		
		debugPrintRepositoryTable();
	}
	
	
	/**
	 * add given terminology to repository registry
	 * @param terminology
	 */
	public void addTerminology(Terminology t){
		// remember old ids
		int [] ids = null;
		
		// get sql id if in database mode
		Map map = repository.get(t.getName());
		if(map != null){
			Integer id = (Integer) map.get("id");
			if(id != null){
				ids = new int [] {id.intValue()};
			}
		}
		
		// setup a map
		map = new HashMap();
		map.put("type",IRepository.TYPE_TERMINOLOGY);
		map.put("name",t.getName());
		map.put("uri",t.getURI());
		map.put("version",t.getVersion());
		map.put("description",t.getDescription());
		map.put("object",t);
		map.put("format",t.getFormat());
		map.put("location",t.getLocation());
		
		// map things to repository
		repository.put(t.getName(),map);
		repository.put(""+t.getURI(),map);
		terminologies.add(t);
		pcs.firePropertyChange(ADDED_EVENT,null,t.getName());
		
		//System.out.println(repository);
		//write configuration
		writeDBConfig(ids);
		setupGlobalRepository();
		
	}
	
	
	/**
	 * remove given terminology to repository registry
	 * @param terminology
	 */
	public void removeTerminology(Terminology t){
		int [] ids = null;
		
		// get sql id if in database mode
		Map map = repository.get(t.getName());
		Integer id = (Integer) map.get("id");
		if(id != null){
			ids = new int [] {id.intValue()};
		}
		
		// remove from registry
		repository.remove(t.getName());
		repository.remove(t.getURI());
		terminologies.remove(t);
		
		// notify of change
		pcs.firePropertyChange(REMOVED_EVENT,null,t.getName());
		
		// write configuration
		writeDBConfig(ids);
		
	}
	
	
	
	/**
	 * import ontology into database
	 */
	public IOntology importOntology(URI path) throws IOntologyException {
		POntology ont = null;
		// load ontology
		try{
			ont = POntology.loadOntology(path);
			importOntology(ont);
		}catch(Exception ex){
			throw new IOntologyException("problem loading "+path,ex);
		}
		return ont;
	}
	
	/**
	 * import ontology into repository, puts it into database
	 * @param file location 
	 */
	public void importOntology(IOntology ont) throws IOntologyException{
		// load ontology
		try{
			// create name for table
			String name = PUtils.getOntologyName(ont.getURI()).replaceAll("\\W","_");
			
			// if ontology with a same name, but different URI exists, then change name
			IOntology [] same = getOntologies(name);;
			int count = 0;
			for(IOntology o: same){
				if(!o.getURI().equals(ont.getURI()) && o.getName().equals(ont.getName()))
					count ++;
			}
			if(count > 0)
				name += "_"+count;
			
			// set table location
			Map map = new HashMap((Map)repository.get(CONFIGURATION));
			map.put("location",ontologyPrefix+name);
			ont.setRepository(this);
			
			//System.out.println("importing "+ont.getURI()+" into "+name);
			
			// save to database if possible
			if(ont instanceof POntology)
				((POntology)ont).saveToDatabase(map);
			
			// add ontologies to a list
			addOntology(ont);
		
			// get list of ontologies
			IOntology [] importedOntologies = ont.getImportedOntologies();
			
			// dispose of current model to save memory
			ont.dispose();
			
			// add imported ontologies to database as well
			//the ontologies from database back
			for(IOntology o :importedOntologies){
				if(!hasOntology(""+o.getURI())){
					importOntology(o);
				}
			}
		}catch(Exception ex){
			ex.printStackTrace();
			throw new IOntologyException("problem importing "+ont.getURI(),ex);
		}
	}
	
	
	/**
	 * convinience method
	 * get resource from one of the loaded ontologies
	 * @param path - input uri
	 * @return resource or null if resource was not found
	 */
	public IResource getResource(URI path){
		String uri = ""+path;
		
		// handle two known ways to specify resource for a 
		int i = uri.lastIndexOf("#");
		if(i > -1){
			uri = uri.substring(0,i);
		}
		
		// get ontology
		IOntology ont = getOntology(URI.create(uri));
		
		// if ontology is all you want, fine Girish
		if(i == -1 && ont != null)
			return ont;
		
		// if ontology is null try again w/ a different convention
		if(ont == null){
			i = uri.lastIndexOf("/");
			if(i > -1){
				uri = uri.substring(0,i);
				
				// get ontology
				ont = getOntology(URI.create(uri));
			}
		}
		
		// now return resource
		if(ont != null)
			return ont.getResource(""+path);
		return null;
	}
	
	/**
	 * export ontology content to terminology
	 * @param ontology
	 * @param terminology
	 */
	public void exportOntology(IOntology ontology, Terminology terminology) throws TerminologyException{
		for(IClass cls: ontology.getRootClasses())
			addClass(cls,terminology);
		//if(terminology instanceof LuceneTerminology)
		//	((LuceneTerminology) terminology).commit();
	}	
	
	/**
	 * add single class to terminology
	 * @param cls
	 * @param term
	 */
	private void addClass(IClass cls, Terminology term) throws TerminologyException {
		if(term.addConcept(cls.getConcept()))
			for(IClass c: cls.getDirectSubClasses())
				addClass(c,term);
	}
	
	
	/**
	 * open protege editor with given ontology
	 */
	public JFrame openProtegeEditor(IOntology ont){
		// Construct the application's main frame.
		JFrame frame = ComponentFactory.createMainFrame();
		frame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
	
		// Find out if a filename was passed in on the command-line.
		ProjectManager.getProjectManager().setRootPane(frame.getRootPane());
		frame.setSize(new Dimension(1024,860));
		// show main frame
		frame.setVisible(true);

		// load project
		//get manager
		ProjectManager manager = ProjectManager.getProjectManager();
		// try to close existing project if it works then continue
		if (manager.closeProjectRequest()) {
			if(ont != null && ont instanceof POntology){
				try{
					ont.load();
					manager.setCurrentProject(((POntology)ont).getModel().getProject(),false);
				}catch(IOntologyException ex){
					ex.printStackTrace();
				}
			}
		}
		return frame;
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
		if(ont instanceof POntology){
			return new PReasoner((POntology)ont);
		}
		return null;
	}
	
	
	/**
	 * get name of this repository
	 * @return
	 */
	public String getName(){
		return "Protege Repository";
	}
	
	
	/**
	 * get description of repository
	 * @return
	 */
	public String getDescription(){
		return "";
	}

	public IOntology getOntology(URI name, String version) {
		return getOntology(name);
	}

	public String[] getVersions(IOntology ont) {
		return (ont != null)?new String [] {ont.getVersion()}:new String [0];
	}
}
