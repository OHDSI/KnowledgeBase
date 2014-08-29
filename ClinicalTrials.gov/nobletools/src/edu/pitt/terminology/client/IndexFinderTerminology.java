package edu.pitt.terminology.client;

import java.beans.PropertyChangeListener;
import java.beans.PropertyChangeSupport;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.Serializable;
import java.net.URI;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.ListIterator;
import java.util.Map;
import java.util.Properties;
import java.util.Set;
import java.util.TreeMap;
import java.util.TreeSet;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.w3c.dom.Document;
import org.w3c.dom.Element;

import edu.pitt.info.extract.model.util.XMLUtils;
import edu.pitt.ontology.IClass;
import edu.pitt.ontology.IOntology;
import edu.pitt.ontology.IOntologyException;
import edu.pitt.ontology.IResourceIterator;
import edu.pitt.terminology.AbstractTerminology;
import edu.pitt.terminology.lexicon.Annotation;
import edu.pitt.terminology.lexicon.Concept;
import edu.pitt.terminology.lexicon.Definition;
import edu.pitt.terminology.lexicon.Relation;
import edu.pitt.terminology.lexicon.SemanticType;
import edu.pitt.terminology.lexicon.Source;
import edu.pitt.terminology.lexicon.Term;
import edu.pitt.terminology.util.CacheMap;
import edu.pitt.terminology.util.MemoryManager;
import edu.pitt.terminology.util.JDBMMap;
import edu.pitt.terminology.util.TerminologyException;
import edu.pitt.text.tools.TextTools;


/**
 * Implementation of Terminology using IndexFinder algorithm
 * @author Eugene Tseytlin (University of Pittsburgh)
 */

public class IndexFinderTerminology extends AbstractTerminology {
	// names of property events to monitor progress
	public static final int CACHE_LIMIT = 10000;
	public static final String LOADING_MESSAGE  = "INDEX_FINDER_MESSAGE";
	public static final String LOADING_PROGRESS = "INDEX_FINDER_PROGRESS";
	public static final String LOADING_TOTAL    = "INDEX_FINDER_TOTAL";
	// names of search methods
	public static final String BEST_MATCH = "best-match";
	public static final String ALL_MATCH = "all-match";
	public static final String PRECISE_MATCH= "precise-match";
	public static final String PARTIAL_MATCH= "partial-match";
	public static final String NONOVERLAP_MATCH = "nonoverlap-match";
	public static final String CUSTOM_MATCH = "custom-match";
	
	public static final String TERM_SUFFIX = ".term";
	public static final String TERM_FILE = "terms";
	public static final String CONCEPT_FILE = "concepts";
	public static final String INFO_FILE = "info.txt";
	public static final String SEARCH_PROPERTIES = "search.properties";
	public static final String TEMP_WORD_DIR = "tempWordTable";
	
	private File location;
	private String name;
	protected Map<String,Set<String>> wordMap;
	protected Map<String,WordStat> wordStatMap;
	protected Map<String,Set<String>> termMap;
	protected Map<String,String> regexMap;
	protected Map<String,Concept.Content> conceptMap;
	protected Map<String,String> infoMap;
	protected Map<String,Source> sourceMap;
	protected Map<String,String> rootMap;
	//protected Map<Integer,String> stringMap;
	private CacheMap<String,Concept []> cache;
	// print rough size and time
	//private final boolean DEBUG = false;
	
	// setting parameters
	/*
	 * stripDigits 			- do not consider digits in text for lookup  (false)
	 * stemWords   			- do porter stemming of terms for storing and lookup (true)
	 * ignoreSmallWords		- do not lookup one-letter words (true)
	 * selectBestCandidate	- if multiple matches for the same term, returned the highest scored one (false)
	 * ignoreCommonWords	- do not lookup 100 most frequent English words (false)
	 * scoreConcepts		- perform scoring for best candidate concept for a match (false)
	 * ignoreUsedWords		- do not lookup on a word in text if it is already part of another matched term (false)
	 * 						  If true, there is a big speedup, but there is a potential to miss some matches.
	 * subsumptionMode		- If true, the narrowest concept Ex: 'deep margin', subsumes broader concepts: 'deep' and 'margin' (true)
	 * overlapMode			- If true, concepts are allowed to overlap and share words: 
	 * orderedMode			- If true, an order of words in text has to reflect the synonym term (false)
	 * contiguousMode		- If true, words in a term must be next to eachother within (wordWindowSize) (false)
	 * partialMode			- If true, text will match if more then 50% of the synonym words are in text (false)
	 * 
	 * windowSize			- Both a maximum number of words that can form a matched term AND a gap between words to make a match (disabled) 
	 * wordWindowSize		- How far words can be apart to be apart as part of a term 
	 */
	
	private boolean stripDigits,crashing,stemWords = true,ignoreSmallWords = true,selectBestCandidate = false, checkProblemWords = true;;
	private boolean ignoreCommonWords,scoreConcepts = false,ignoreAcronyms,useTempWordFolder,ignoreUsedWords = true;
	private boolean subsumptionMode = true,overlapMode=true, orderedMode, contiguousMode,partialMode; 
	private int windowSize = -1;
	private int wordWindowSize = 1;
	private double partialMatchThreshold = 0.5;
	private String defaultSearchMethod = BEST_MATCH;
	
	
	
	
	private static File dir;
	private Set<Source> filteredSources;
	private Set<SemanticType> filteredSemanticTypes;
	private Set<String> filteredLanguages;
	private PropertyChangeSupport pcs = new PropertyChangeSupport(this);
	private boolean cachingEnabled = true, truncateURI;
	private int maxTermsPerWord,totalTermsPerWord;
	
	public boolean isCachingEnabled() {
		return cachingEnabled;
	}

	public void setCachingEnabled(boolean b) {
		this.cachingEnabled = b;
	}

	// init default persistence directory
	static{
		setPersistenceDirectory(new File(System.getProperty("user.home"),".terminologies"));
	}

	/**
	 * set directory where persistence files should be saved
	 * @param f
	 */
	public static void setPersistenceDirectory(File f){
		dir = f;
	}
	
	/**
	 * set directory where persistence files should be saved
	 * @param f
	 */
	public static File getPersistenceDirectory(){
		if(dir != null && !dir.exists())
			dir.mkdirs();
		return dir;
	}
	
	
	/**
	 * represents several word stats
	 * @author tseytlin
	 */
	public static class WordStat implements Serializable {
		public int termCount;
		public boolean isTerm;
	}
	
	
	/**
	 * initialize empty in-memory terminology that has to be
	 * filled up manual using Terminology.addConcept()
	 */
	public IndexFinderTerminology(){
		init();
	}
	
	/**
	 * initialize with in memory maps
	 */
	private void init(){
		wordMap = new HashMap<String,Set<String>>();
		wordStatMap = new HashMap<String, WordStat>();
		termMap = new HashMap<String,Set<String>>();
		regexMap = new HashMap<String,String>();
		conceptMap = new HashMap<String,Concept.Content>();
		infoMap = new HashMap<String,String>();
		sourceMap = new HashMap<String,Source>();
		rootMap = new HashMap<String,String>();
		//stringMap = new HashMap<Integer, String>();
		cache = new CacheMap<String, Concept []>(CacheMap.FREQUENCY);
		cache.setSizeLimit(CACHE_LIMIT);		
	}
	
	/**
	 * initialize a named terminology that either has already been 
	 * persisted on disk, or will be persisted on disk
	 */
	public IndexFinderTerminology(String name) throws IOException{
		load(name,true);
	}
	
	protected void finalize() throws Throwable {
		dispose();
	}

	/**
	 * add property change listener to subscribe to progress messages
	 * @param l
	 */
	public void addPropertyChangeListener(PropertyChangeListener l){
		pcs.addPropertyChangeListener(l);
	}
	
	/**
	 * add property change listener to subscribe to progress messages
	 * @param l
	 */
	public void removePropertyChangeListener(PropertyChangeListener l){
		pcs.removePropertyChangeListener(l);
	}
	
	/**
	 * load persitent tables
	 */
	public void load(String name) throws IOException{
		load(name,false);
	}
	/**
	 * load persitent tables
	 */
	public void load(String name,boolean readonly) throws IOException{
		if(name.endsWith(TERM_SUFFIX))
			name = name.substring(0,name.length()-TERM_SUFFIX.length());
		this.name = name;
		
		// setup location
		if(name.contains(File.separator))
			location = new File(name+TERM_SUFFIX);
		else
			location = new File(getPersistenceDirectory(),name+TERM_SUFFIX);
		
		// create a directory
		if(!location.exists())
			location.mkdirs();
		
		// split into two seperate 
		//String termFile = location.getAbsolutePath()+File.separator+TERM_FILE;
		//String conceptFile = location.getAbsolutePath()+File.separator+CONCEPT_FILE;
		String prefix = location.getAbsolutePath()+File.separator+"table";
				
		wordMap = new JDBMMap<String,Set<String>>(prefix,"wordMap",readonly);
		termMap = new JDBMMap<String,Set<String>>(prefix,"termMap",readonly);
		regexMap = new JDBMMap<String,String>(prefix,"regexMap",readonly);
		wordStatMap = new JDBMMap<String,WordStat>(prefix,"wordStatMap",readonly);
		//stringMap =  new JDBMMap<Integer,String>(termFile,"stringMap");
		
		conceptMap = new JDBMMap<String,Concept.Content>(prefix,"conceptMap",readonly);
		infoMap = new JDBMMap<String,String>(prefix,"infoMap",readonly);
		sourceMap = new JDBMMap<String,Source>(prefix,"sourceMap",readonly);
		rootMap = new JDBMMap<String,String>(prefix,"rootMap",readonly);

		cache = new CacheMap<String, Concept []>(CacheMap.FREQUENCY);
		cache.setSizeLimit(CACHE_LIMIT);
		
		
		// load default values
		if(infoMap.containsKey("stem.words"))
			stemWords = Boolean.parseBoolean(infoMap.get("stem.words"));
		if(infoMap.containsKey("strip.digits"))
			stripDigits = Boolean.parseBoolean(infoMap.get("strip.digits"));
		if(infoMap.containsKey("ignore.small.words"))
			ignoreSmallWords = Boolean.parseBoolean(infoMap.get("ignore.small.words"));
		
		
		// load optional search options
		File sp = new File(location,SEARCH_PROPERTIES);
		if(sp.exists()){
			// pull this file
			Properties p = new Properties();
			FileReader r = new FileReader(sp);
			p.load(r);
			r.close();
			
			// lookup default search method
			setSearchProperties(p);
		}
		
	}
	
	/**
	 * save meta information
	 * @param f
	 */
	private void saveSearchProperteis(){
		try{
			FileWriter w = new FileWriter(new File(location,SEARCH_PROPERTIES));
			getSearchProperties().store(w,"Optional Search Options");
			w.close();
		}catch(Exception ex){
			ex.printStackTrace();
		}
	}
	
	/**
	 * get properties map with search options
	 * @return
	 */
	public Properties getSearchProperties(){
		Properties p = new Properties();
		p.setProperty("default.search.method",defaultSearchMethod);
		p.setProperty("ignore.small.words",""+ignoreSmallWords);
		p.setProperty("source.filter",toString(getFilterSources()));
		p.setProperty("language.filter",toString(getFilterLanguages()));
		p.setProperty("semantic.type.filter",toString(getFilterSemanticType()));
		p.setProperty("ignore.common.words",""+isIgnoreCommonWords());
		p.setProperty("ignore.acronyms",""+isIgnoreAcronyms());
		p.setProperty("select.best.candidate",""+isSelectBestCandidate());
		p.setProperty("window.size",""+getWindowSize());
		p.setProperty("enable.search.cache",""+cachingEnabled);
		p.setProperty("ignore.used.words",""+ignoreUsedWords);
		p.setProperty("subsumption.mode",""+subsumptionMode);
		p.setProperty("overlap.mode",""+overlapMode);
		p.setProperty("contiguous.mode",""+contiguousMode);
		p.setProperty("ordered.mode",""+orderedMode);
		p.setProperty("partial.mode",""+partialMode);
		p.setProperty("partial.mode",""+partialMode);
		p.setProperty("stem.words",""+stemWords);
		p.setProperty("ignore.digitss",""+stripDigits);
		p.setProperty("partial.match.theshold",""+partialMatchThreshold);
		return p;
	}
	
	
	/**
	 * set search properties
	 * @param p
	 */
	public void setSearchProperties(Properties p){
		// load default values
		if(p.containsKey("stem.words"))
			stemWords = Boolean.parseBoolean(p.getProperty("stem.words"));
		if(p.containsKey("ignore.digits"))
			stripDigits = Boolean.parseBoolean(p.getProperty("ignore.digits"));
		if(p.containsKey("ignore.small.words"))
			ignoreSmallWords = Boolean.parseBoolean(p.getProperty("ignore.small.words"));
		
		// lookup default search method
		if(p.containsKey("default.search.method")){
			defaultSearchMethod = BEST_MATCH;
			String s = p.getProperty("default.search.method",BEST_MATCH);
			for(String m: getSearchMethods()){
				if(s.equals(m)){
					defaultSearchMethod = s;
					break;
				}	
			}
		}
		
		// lookup small words
		if(p.containsKey("ignore.small.words"))
			ignoreSmallWords = Boolean.parseBoolean(p.getProperty("ignore.small.words"));
		if(p.containsKey("ignore.common.words"))
			ignoreCommonWords = Boolean.parseBoolean(p.getProperty("ignore.common.words"));
		if(p.containsKey("ignore.digits"))
			stripDigits = Boolean.parseBoolean(p.getProperty("ignore.digits"));
		if(p.containsKey("ignore.acronyms"))
			ignoreAcronyms = Boolean.parseBoolean(p.getProperty("ignore.acronyms"));
		if(p.containsKey("select.best.candidate"))
			selectBestCandidate = Boolean.parseBoolean(p.getProperty("select.best.candidate"));
		if(p.containsKey("window.size")){
			try{
				windowSize = Integer.parseInt(p.getProperty("window.size"));
			}catch(Exception ex){}
		}
		if(p.containsKey("ignore.used.words"))
			ignoreUsedWords = Boolean.parseBoolean(p.getProperty("ignore.used.words"));
		if(p.containsKey("subsumption.mode"))
			subsumptionMode = Boolean.parseBoolean(p.getProperty("subsumption.mode"));
		if(p.containsKey("overlap.mode"))
			overlapMode = Boolean.parseBoolean(p.getProperty("overlap.mode"));
		if(p.containsKey("contiguous.mode"))
			contiguousMode = Boolean.parseBoolean(p.getProperty("contiguous.mode"));
		if(p.containsKey("ordered.mode"))
			orderedMode = Boolean.parseBoolean(p.getProperty("ordered.mode"));
		if(p.containsKey("partial.mode"))
			partialMode = Boolean.parseBoolean(p.getProperty("partial.mode"));
		if(p.containsKey("enable.search.cache"))
			cachingEnabled = Boolean.parseBoolean(p.getProperty("enable.search.cache"));
		if(p.containsKey("partial.match.theshold"))
			partialMatchThreshold = Double.parseDouble(p.getProperty("partial.match.theshold"));
		
		// language filter
		String v = p.getProperty("language.filter");
		if(v != null && v.length() > 0){
			ArrayList<String> val = new ArrayList<String>();
			String sep = (v.indexOf(';') > -1)?";":",";
			for(String s: v.split(sep))
				val.add(s.trim());
			setFilterLanguages(val.toArray(new String [0]));
		}
		
		// source filter
		v = p.getProperty("source.filter");
		if(v != null && v.length() > 0){
			ArrayList<Source> val = new ArrayList<Source>();
			String sep = (v.indexOf(';') > -1)?";":",";
			for(String s: v.split(sep))
				val.add(Source.getSource(s.trim()));
			setFilterSources(val.toArray(new Source [0]));
		}
		
		// semantic type filter
		v = p.getProperty("semantic.type.filter");
		if(v != null && v.length() > 0){
			ArrayList<SemanticType> val = new ArrayList<SemanticType>();
			String sep = (v.indexOf(';') > -1)?";":",";
			for(String s: v.split(sep))
				val.add(SemanticType.getSemanticType(s.trim()));
			setFilterSemanticType(val.toArray(new SemanticType [0]));
		}
	
		
	}
	
	
	private String toString(Object [] list){
		StringBuffer b = new StringBuffer();
		for(Object o: list){
			b.append(o+";"); 
		}
		return (b.length()>1)?b.substring(0,b.length()-1):"";
	}
	
	/**
	 * save meta information
	 * @param f
	 */
	private void saveMetaInfo(File f){
		try{
			BufferedWriter writer = new BufferedWriter(new FileWriter(f));
			writer.write("name:\t\t"+getName()+"\n");
			writer.write("uri:\t\t"+getURI()+"\n");
			writer.write("version:\t"+getVersion()+"\n");
			writer.write("location:\t"+getLocation()+"\n");
			if(infoMap.containsKey("languages"))
				writer.write("languages:\t"+infoMap.get("languages")+"\n");
			writer.write("description:\t"+getDescription()+"\n");
			if(infoMap.containsKey("semantic.types"))
				writer.write("semantic types:\t"+infoMap.get("semantic.types")+"\n");
			if(infoMap.containsKey("word.count"))
				writer.write("word count:\t"+infoMap.get("word.count")+"\n");
			if(infoMap.containsKey("term.count"))
				writer.write("term count:\t"+infoMap.get("term.count")+"\n");
			if(infoMap.containsKey("concept.count"))
				writer.write("concept count:\t"+infoMap.get("concept.count")+"\n");
			writer.write("configuration:\t");
			writer.write("stem.words="+stemWords+", ");
			writer.write("strip.digits="+stripDigits+", ");
			writer.write("ignore.small.words="+ignoreSmallWords+"\n");
			writer.write("\nsources:\n\n");
			for(String name: new TreeSet<String>(sourceMap.keySet())){
				writer.write(name+": "+sourceMap.get(name).getDescription()+"\n");
			}
			
			
			writer.close();
		}catch(Exception ex){
			ex.printStackTrace();
		}
		
		// save info in map
		infoMap.put("strip.digits",""+stripDigits);
		infoMap.put("stem.words",""+stemWords);
		infoMap.put("ignore.small.words",""+ignoreSmallWords);
	}
	
	

	
	
	/**
	 * get the entire set of concept codes
	 * @return
	 */
	public Set<String> getAllConcepts(){
		return conceptMap.keySet();
	}
	
	/**
	 * get all available concept objects in terminology. Only sensible for small terminologies
	 * @return
	 */
	public Collection<Concept> getConcepts()  throws TerminologyException{
		List<Concept> list = new ArrayList<Concept>();
		for(Concept.Content c: conceptMap.values()){
			list.add(convertConcept(c));
		}
		return list;
	}
	
	/**
	 * reload tables to save space
	 */
	public void crash(){
		if(crashing)
			return;
		crashing = true;
		// save current content 
		pcs.firePropertyChange(LOADING_MESSAGE,null,"Running low on memory.Saving work and crashing ...");
		save();
		System.exit(1);
		crashing = false;
	}
	
	
	/**
	 * load index finder tables from an IOntology object
	 * @param ontology
	 * @throws IOException
	 * @throws TerminologyException 
	 */
	public void loadOntology(IOntology ontology) throws IOException, TerminologyException, IOntologyException {
		loadOntology(ontology,null);
	}
	
	/**
	 * load index finder tables from an IOntology object
	 * @param ontology
	 * @throws IOException
	 * @throws TerminologyException 
	 */
	public void loadOntology(IOntology ontology, String name) throws IOException, TerminologyException, IOntologyException {
		loadOntology(ontology,name,false,false);
	}
	
	/**
	 * load index finder tables from an IOntology object
	 * @param ontology
	 * @throws IOException
	 * @throws TerminologyException 
	 */
	public void loadOntology(IOntology ontology, String name, boolean inmemory,boolean truncateURI) throws IOException, TerminologyException, IOntologyException {
		this.name = (name != null)?name:ontology.getName();
		this.truncateURI = truncateURI;
		
		// clear tables
		if(inmemory)
			init();
		else
			load(this.name);
		
		// check if already loaded
		if("done".equals(infoMap.get("status")))
			return;
		
		
		// handle memory nightmare (save when you reach 90%)
		MemoryManager.setMemoryThreshold(new Runnable(){
			public void run() {
				crash();
			}
		},0.95);
		
		// load classes for the very first time
		pcs.firePropertyChange(LOADING_MESSAGE,null,"Loading Ontology "+ontology.getName()+" from "+ontology.getLocation()+" ...");
		ontology.load();
		
		// save meta information
		infoMap.put("name",ontology.getName());
		infoMap.put("descripion",ontology.getDescription());
		infoMap.put("version",ontology.getVersion());
		infoMap.put("uri",ontology.getURI().toASCIIString());
		Source src = Source.getSource(ontology.getName());
		src.setDescription(ontology.getDescription());
		sourceMap.put(ontology.getName(),src);
		
		// get all classes
		pcs.firePropertyChange(LOADING_MESSAGE,null,"Iterating Over Ontology Classes ...");
		pcs.firePropertyChange(LOADING_TOTAL,null,0);
		IResourceIterator it = ontology.getAllClasses();
		int i = 0;
		int offset = 0;
		if(infoMap.containsKey("offset"))
			offset = Integer.parseInt(infoMap.get("offset"));
		while(it.hasNext()){
			i++;
			// skip if we have an offset left over from previous load
			//if(i< offset)
			//	continue;
			
			IClass cls = (IClass)it.next();
			String code = getCode(cls);
			if(conceptMap.containsKey(code))
				continue;
			
			Concept concept = cls.getConcept();
			concept.setCode(code);
			
			// fix sources
			for(Source sr: concept.getSources())
				sr.setCode(getCode(sr.getCode()));
			
			// add relations to concept
			for(IClass c: cls.getDirectSuperClasses()){
				concept.addRelatedConcept(Relation.BROADER,getCode(c));
			}
			
			// add relations to concept
			for(IClass c: cls.getDirectSubClasses()){
				concept.addRelatedConcept(Relation.NARROWER,getCode(c));
			}
						
			// add concept
			addConcept(concept);
			
			// commit ever so often
			if((i % 3000) == 0){
				pcs.firePropertyChange(LOADING_PROGRESS,null,i);
				//save();
			}
			infoMap.put("offset",""+i);
		}
		for(IClass r: ontology.getRootClasses())
			rootMap.put(getCode(r),"");
		save();
		infoMap.put("status","done");
	}

	private String getCode(IClass cls){
		return getCode(""+cls.getURI());
	}
	private String getCode(String uri){
		if(truncateURI){
			int x = uri.lastIndexOf('/');
			return (x > -1)?uri.substring(x+1):uri;
		}
		return uri;
	}
	
	
	
	
	/**
	 * load from RRF files (Rich Release Files)
	 * This is a common distribution method for UMLS and NCI Meta
	 * @param directory that contains MRCONSO.RRF, MRDEF.RRF, MRSTY.RRF etc...
	 * by default uses ALL sources, but only for English language
	 */
	public void loadRRF(File dir) throws FileNotFoundException, IOException, TerminologyException {
		Map<String,List<String>> params = new HashMap<String, List<String>>();
		params.put("languages",Arrays.asList("ENG"));
		loadRRF(dir,params);
	}
	
	
	/**
	 * load from RRF files (Rich Release Files)
	 * This is a common distribution method for UMLS and NCI Meta
	 * @param directory that contains MRCONSO.RRF, MRDEF.RRF, MRSTY.RRF etc...
	 * @param Map<String,List<String>> filter property object, where some properties are:
	 * name - change ontology name
	 * languages - only include languages in a given list languages
	 * sources - only include concepts from a given list of sources
	 * semanticTypes - filter result by a list of semantic types attached
	 * hierarchySources - only include hierarhy information from a list of sources
	 */
	public void loadRRF(File dir, Map<String,List<String>> params) throws FileNotFoundException, IOException, TerminologyException {
		long time = System.currentTimeMillis();
		
		// get known params
		String name = (params.containsKey("name") && !params.get("name").isEmpty())?params.get("name").get(0):null; 
		List<String> filterLang = params.get("languages");
		List<String> filterSources = params.get("sources");
		List<String> filterSemTypes = params.get("semanticTypes");
		List<String> relationSources = params.get("hierarchySources");
		if(relationSources == null)
			relationSources = filterSources;
		else if(relationSources.size() == 1 && "*".equals(relationSources.get(0)))
			relationSources = null;
		
		
		// load tables 
		//load(dir.getName());
		load((name != null)?name:dir.getName());
		
		// check if already loaded
		if("done".equals(infoMap.get("status")))
			return;
		
		// handle memory nightmare (save when you reach 90%)
		MemoryManager.setMemoryThreshold(new Runnable(){
			public void run() {
				crash();
			}
		},0.95);
		
		// try to extract the name from the directory
		int i=0,offset = 0;
		infoMap.put("name",dir.getName());
		Pattern pt = Pattern.compile("([a-zA-Z\\s_]+)[_\\-\\s]+([\\d_]+[A-Z]?)");
		Matcher mt = pt.matcher(dir.getName());
		if(mt.matches()){
			infoMap.put("name",mt.group(1));
			infoMap.put("version",mt.group(2));
		}
		
		// fill out some more info
		if(filterLang != null){
			String s = filterLang.toString();
			infoMap.put("languages",s.substring(1,s.length()-1));
		}
		
		// fill out some more info
		if(filterSemTypes != null){
			String s = filterSemTypes.toString();
			infoMap.put("semantic.types",s.substring(1,s.length()-1));
		}

		// fill out some more info
		if(filterSources != null){
			String s = filterSources.toString();
			infoMap.put("sources",s.substring(1,s.length()-1));
		}
		
		if(infoMap.containsKey("total.terms.per.word"))
			totalTermsPerWord = Integer.parseInt(infoMap.get("total.terms.per.word"));
		if(infoMap.containsKey("max.terms.per.word"))
			maxTermsPerWord = Integer.parseInt(infoMap.get("max.terms.per.word"));
		
		
		// first read in meta information
		Map<String,Integer> rowCount = new HashMap<String, Integer>();
		for(String f: Arrays.asList("MRSAB.RRF","MRCONSO.RRF","MRDEF.RRF","MRSTY.RRF","MRREL.RRF")){
			rowCount.put(f,Integer.MAX_VALUE);
		}
		
		BufferedReader r = null;
		if(new File(dir,"MRFILES.RRF").exists()){
			r = new BufferedReader(new FileReader(new File(dir,"MRFILES.RRF")));
			for(String line = r.readLine(); line != null; line = r.readLine()){
				// parse each line ref: http://www.ncbi.nlm.nih.gov/books/NBK9685/
				String [] fields = line.split("\\|");
				rowCount.put(fields[0].trim(),Integer.parseInt(fields[4]));
			}
			r.close();
		}
		
		// read in source information
		offset = 0;
		String RRFile = "MRSAB.RRF";
		if(infoMap.containsKey(RRFile)){
			offset = Integer.parseInt(infoMap.get(RRFile));
		}
		if(!new File(dir,RRFile).exists()){
			pcs.firePropertyChange(LOADING_MESSAGE,null,"RRF file "+(new File(dir,RRFile).getAbsolutePath()+" does not exist, sipping .."));
			offset = Integer.MAX_VALUE;
		}
		// if offset is smaller then total, read file
		if(offset < rowCount.get(RRFile)){
			i = 0;
			pcs.firePropertyChange(LOADING_MESSAGE,null,"Loading "+RRFile+" file ...");
			r = new BufferedReader(new FileReader(new File(dir,RRFile)));
			for(String line = r.readLine(); line != null; line = r.readLine()){
				if(i < offset){
					i++;
					continue;
				}
				//http://www.ncbi.nlm.nih.gov/books/NBK9685/table/ch03.T.source_information_file__mrsabrrf/?report=objectonly
				String [] fields = line.split("\\|");
				Source src = new Source(fields[3].trim());
				src.setDescription(fields[4]); // fields.length-1
				if(filterSources != null && filterSources.contains(src.getName())){
					sourceMap.put(src.getName(),src);
				}
				i++;
				infoMap.put(RRFile,""+i);
			}
			r.close();
		}else{
			pcs.firePropertyChange(LOADING_MESSAGE,null,"Skipping "+RRFile+" file ...");
		}
			
		
		// save meta information
		pcs.firePropertyChange(LOADING_MESSAGE,null,"Saving Meta Information ...");
		((JDBMMap) infoMap).commit();
		((JDBMMap) sourceMap).commit();
		
		// lets first build a map of concepts using existing concept map
		useTempWordFolder = true;
		String prefNameSource = null;
		offset = 0;
		RRFile = "MRCONSO.RRF";
		if(!new File(dir,RRFile).exists())
			throw new TerminologyException("RRF file "+(new File(dir,RRFile).getAbsolutePath()+" does not exist!"));
		
		if(infoMap.containsKey(RRFile)){
			offset = Integer.parseInt(infoMap.get(RRFile));
		}
		// if offset is smaller then total, read file
		if(offset < rowCount.get(RRFile)){
			i = 0;
			pcs.firePropertyChange(LOADING_MESSAGE,null,"Loading "+RRFile+" file ...");
			pcs.firePropertyChange(LOADING_TOTAL,null,rowCount.get(RRFile));
			r = new BufferedReader(new FileReader(new File(dir,RRFile)));
			Concept previousConcept = null;
			//boolean crash = false;
			for(String line = r.readLine(); line != null; line = r.readLine()){
				if(i < offset){
					i++;
					continue;
				}
				// parse each line ref: http://www.ncbi.nlm.nih.gov/books/NBK9685/table/ch03.T.concept_names_and_sources_file__m/?report=objectonly
				String [] fields = line.split("\\|");
				if(fields.length >= 14 ){
					String cui = fields[0].trim();
					String ts =  fields[2].trim();
					String src  = fields[11].trim();
					String text = fields[14].trim();
					String lang = fields[1].trim();
					String form = fields[12].trim();
					String code = fields[13].trim();
					String pref = fields[6].trim();
					String sup  = fields[16].trim();
					
					Source source = Source.getSource(src);
					
					// display progress bar
					if((i % 10000) == 0){
						pcs.firePropertyChange(LOADING_PROGRESS,null,i);
						((JDBMMap) infoMap).commit();
						((JDBMMap) termMap).commit();
						((JDBMMap) regexMap).commit();
						((JDBMMap) conceptMap).commit();
						/*if(i > 0 && i % 500000 == 0){
							crash = true;
						}*/
					}
					i++;
					
					// filter out by language
					if(filterLang != null && !filterLang.contains(lang))
						continue;
					
					// filter out by source
					if(filterSources != null && !filterSources.contains(src)){
						if(!(code.startsWith("V-") && filterSources.contains(code.substring(2))))
							continue;
					}
					
					// honor suppress flag
					if("O".equals(sup))
						continue;
					
					// get concept from map
					Concept c = convertConcept(conceptMap.get(cui));
					if(c == null){
						// if concept is not in map, see if previous is it
						if(previousConcept != null && previousConcept.getCode().equals(cui)){
							c = previousConcept;
						}else{
							c = new Concept(cui,text);
							prefNameSource = null;
						}
					}
					
					// create a term
					Term term = new Term(text);
					term.setForm(form);
					term.setLanguage(lang);
					term.setSource(source);
					if("y".equalsIgnoreCase(pref) && "P".equalsIgnoreCase(ts))
						term.setPreferred(true);
					
					// add to concept
					c.addSynonym(text);
					c.addSource(source);
					c.addTerm(term);
					c.addCode(code, source);
					
					// set preferred name for the first time
					if(term.isPreferred()){
						// if prefered name source is not set OR
						// we have filtering and the new source offset is less then old source offset (which means higher priority)
						if(prefNameSource == null || (filterSources != null && filterSources.indexOf(src) < filterSources.indexOf(prefNameSource))){
							c.setName(text);
							prefNameSource = src;
							
						}
					}
					term = null;
					
					// now see if we pretty much got the entire concept and should put it in
					if(previousConcept != null && !previousConcept.getCode().equals(cui)){
						addConcept(previousConcept);
						infoMap.put("max.terms.per.word",""+maxTermsPerWord);
						infoMap.put("total.terms.per.word",""+totalTermsPerWord);
						/*if(crash)
							crash();*/
					}
					previousConcept = c;
				}
				infoMap.put(RRFile,""+i);
			
			}
			// save last one
			if(previousConcept != null)
				addConcept(previousConcept);
			r.close();
		}else{
			pcs.firePropertyChange(LOADING_MESSAGE,null,"Skipping "+RRFile+" file ...");
		}
		
		// commit info terms and regex
		pcs.firePropertyChange(LOADING_MESSAGE,null,"Saving Term Information ...");
		((JDBMMap) infoMap).commit();
		((JDBMMap) termMap).commit();
		((JDBMMap) regexMap).commit();
		((JDBMMap) conceptMap).commit();
		
		// now do temp word dir
		File tempDir = new File(location,TEMP_WORD_DIR);
		if(useTempWordFolder && tempDir.exists()){
			useTempWordFolder = false;
			File [] files = tempDir.listFiles();
			offset = 0;
			RRFile = TEMP_WORD_DIR;
			if(infoMap.containsKey(RRFile)){
				offset = Integer.parseInt(infoMap.get(RRFile));
			}
			// if offset is smaller then total, read file
			if(offset < files.length){
				pcs.firePropertyChange(LOADING_MESSAGE,null,"Loading temporary word files ...");
				pcs.firePropertyChange(LOADING_TOTAL,null,files.length);
				i = 0;
				for(File f: files){
					if(i < offset){
						i++;
						continue;
					}
					// display progress bar
					if((i % (files.length/100)) == 0){
						pcs.firePropertyChange(LOADING_PROGRESS,null,i);
					}
					i++;
					
					//load file content
					String word = f.getName();
					Set<String> terms = new HashSet<String>();
					BufferedReader rd = new BufferedReader(new FileReader(f));
					for(String l = rd.readLine();l != null; l = rd.readLine()){
						terms.add(l.trim());
					}
					rd.close();
					
					// set words
					setWordTerms(word,terms);
					infoMap.put(RRFile,""+i);
				}
			}else{
				pcs.firePropertyChange(LOADING_MESSAGE,null,"Skipping "+RRFile+" file ...");
			}
		}
		
		// save some meta information
		infoMap.put("word.count",""+wordMap.size());
		infoMap.put("term.count",""+termMap.size());
		infoMap.put("concept.count",""+conceptMap.size());
		infoMap.put("average.terms.per.word",""+totalTermsPerWord/wordMap.size());
		infoMap.put("max.terms.per.word",""+maxTermsPerWord);
		
		// good time to save term info
		pcs.firePropertyChange(LOADING_MESSAGE,null,"Saving Word Information ...");
		((JDBMMap) infoMap).commit();
		((JDBMMap) wordMap).commit();
		((JDBMMap) wordStatMap).commit();
		
		// lets go over definitions
		offset = 0;
		RRFile = "MRDEF.RRF";
		if(infoMap.containsKey(RRFile)){
			offset = Integer.parseInt(infoMap.get(RRFile));
		}
		
		if(!new File(dir,RRFile).exists()){
			pcs.firePropertyChange(LOADING_MESSAGE,null,"RRF file "+(new File(dir,RRFile).getAbsolutePath()+" does not exist, sipping .."));
			offset = Integer.MAX_VALUE;
		}
			
		// if offset is smaller then total, read file
		if(offset < rowCount.get(RRFile)){
			i = 0;
			pcs.firePropertyChange(LOADING_MESSAGE,null,"Loading "+RRFile+" file ...");
			pcs.firePropertyChange(LOADING_TOTAL,null,rowCount.get(RRFile));
			r = new BufferedReader(new FileReader(new File(dir,RRFile)));
			for(String line = r.readLine(); line != null; line = r.readLine()){
				if(i < offset){
					i++;
					continue;
				}
				// parse each line ref: http://www.ncbi.nlm.nih.gov/books/NBK9685/table/ch03.T.definitions_file__mrdefrrf/?report=objectonly
				String [] fields = line.split("\\|");
				if(fields.length >= 5 ){
					String cui = fields[0].trim();
					String src = fields[4].trim();
					String text = fields[5].trim();
					
					Definition d = Definition.getDefinition(text);
					d.setSource(Source.getSource(src));
					
					// get concept from map
					Concept c = convertConcept(conceptMap.get(cui));
					if(c != null){
						c.addDefinition(d);
						// replace with new concept
						conceptMap.put(cui,c.getContent());
					}
					if((i % 10000) == 0)
						pcs.firePropertyChange(LOADING_PROGRESS,null,i);
				}
				i++;
				infoMap.put(RRFile,""+i);
			}
			r.close();
		}else{
			pcs.firePropertyChange(LOADING_MESSAGE,null,"Skipping "+RRFile+" file ...");
		}
		
		// go over semantic types
		offset = 0;
		RRFile = "MRSTY.RRF";
		if(infoMap.containsKey(RRFile)){
			offset = Integer.parseInt(infoMap.get(RRFile));
		}
		if(!new File(dir,RRFile).exists()){
			pcs.firePropertyChange(LOADING_MESSAGE,null,"RRF file "+(new File(dir,RRFile).getAbsolutePath()+" does not exist, sipping .."));
			offset = Integer.MAX_VALUE;
		}
		// if offset is smaller then total, read file
		if(offset < rowCount.get(RRFile)){
			i=0;
			pcs.firePropertyChange(LOADING_MESSAGE,null,"Loading "+RRFile+" file ...");
			pcs.firePropertyChange(LOADING_TOTAL,null,rowCount.get(RRFile));
			r = new BufferedReader(new FileReader(new File(dir,RRFile)));
			for(String line = r.readLine(); line != null; line = r.readLine()){
				if(i < offset){
					i++;
					continue;
				}
				// parse each line ref: http://www.ncbi.nlm.nih.gov/books/NBK9685/table/ch03.T.definitions_file__mrdefrrf/?report=objectonly
				String [] fields = line.split("\\|");
				if(fields.length >= 3 ){
					String cui = fields[0].trim();
					String tui = fields[1].trim();
					String text = fields[3].trim();
					
					// get concept from map
					Concept c = convertConcept(conceptMap.get(cui));
					if(c != null){
						// filter out by source
						if(filterSemTypes != null && !filterSemTypes.contains(text)){
							removeConcept(c);
						}else{
							c.addSemanticType(new SemanticType(text,tui));
							// replace with new concept
							conceptMap.put(cui,c.getContent());
						}
					}
				}
				if((i % 10000) == 0)
					pcs.firePropertyChange(LOADING_PROGRESS,null,i);
				i++;
				infoMap.put(RRFile,""+i);
			}
			r.close();
		}else{
			pcs.firePropertyChange(LOADING_MESSAGE,null,"Skipping "+RRFile+" file ...");
		}
		
		//process relationships?
		offset = 0;
		RRFile = "MRREL.RRF";
		if(infoMap.containsKey(RRFile)){
			offset = Integer.parseInt(infoMap.get(RRFile));
		}
		if(!new File(dir,RRFile).exists()){
			pcs.firePropertyChange(LOADING_MESSAGE,null,"RRF file "+(new File(dir,RRFile).getAbsolutePath()+" does not exist, sipping .."));
			offset = Integer.MAX_VALUE;
		}
		// if offset is smaller then total, read file
		if(offset < rowCount.get(RRFile)){
			i=0;
			pcs.firePropertyChange(LOADING_MESSAGE,null,"Loading "+RRFile+" file ...");
			pcs.firePropertyChange(LOADING_TOTAL,null,rowCount.get(RRFile));
			r = new BufferedReader(new FileReader(new File(dir,RRFile)));
			List<String> filterRelations = Arrays.asList("RB","RN","PAR","CHD");
			//Concept previousConcept = null;
			for(String line = r.readLine(); line != null; line = r.readLine()){
				if(i < offset){
					i++;
					continue;
				}
				// parse each line ref: http://www.ncbi.nlm.nih.gov/books/NBK9685/table/ch03.T.definitions_file__mrdefrrf/?report=objectonly
				String [] fields = line.split("\\|");
				if(fields.length >= 5 ){
					String cui1 = fields[0].trim();
					String cui2 = fields[4].trim();
					String rel = fields[3].trim();
					String src = fields[10].trim();
					
					// filter by known source if
					if(relationSources != null && !relationSources.contains(src))
						continue;
					
					// filter by known relationship
					if(filterRelations.contains(rel) && !cui1.equals(cui2)){
						Relation re = null;
						if("RB".equals(rel) || "PAR".equals(rel))
							re = Relation.BROADER;
						else if("RN".equals(rel) || "CHD".equals(rel))
							re = Relation.NARROWER;
						
						// get concept from map
						Concept c = convertConcept(conceptMap.get(cui1));
						if(c != null && re != null){
							c.addRelatedConcept(re,cui2);
							// replace with new concept
							conceptMap.put(cui1,c.getContent());
						}
					}	
				}
				if((i % 10000) == 0)
					pcs.firePropertyChange(LOADING_PROGRESS,null,i);
				i++;
				infoMap.put(RRFile,""+i);
			}
			r.close();
		}else{
			pcs.firePropertyChange(LOADING_MESSAGE,null,"Skipping "+RRFile+" file ...");
		}
		
		
		// try to create root table, by going over all concepts
		offset = 0;
		i = 0;
		RRFile = "ROOTS";
		if(infoMap.containsKey(RRFile)){
			offset = Integer.parseInt(infoMap.get(RRFile));
		}
		if(offset < conceptMap.size()){
			pcs.firePropertyChange(LOADING_MESSAGE,null,"Finding Root Concepts ...");
			for(String key : conceptMap.keySet()){
				if(i < offset){
					i++;
					continue;
				}
				Concept.Content c = conceptMap.get(key);
				//anything that doesn't have brader concepts AND is from SRC terminology
				if(c.relationMap != null && c.relationMap.containsKey(Relation.NARROWER) && !c.relationMap.containsKey(Relation.BROADER)){
					// is it a source?
					boolean issource = false;
					for(Source s: c.sources)
						if(s.getName().equals("SRC"))
							issource = true;
					if(issource)
						rootMap.put(c.code,"");
				}
				if((i % 100000) == 0)
					pcs.firePropertyChange(LOADING_PROGRESS,null,i);
				i++;
				infoMap.put(RRFile,""+i);
			}
		}else{
			pcs.firePropertyChange(LOADING_MESSAGE,null,"Skipping Root Inference ...");
		}
		
		// last save
		pcs.firePropertyChange(LOADING_MESSAGE,null,"Saving Concept Information ...");
		infoMap.put("status","done");
		save();
		
		// remove temp word files 
		if(tempDir.exists()){
			pcs.firePropertyChange(LOADING_MESSAGE,null,"Deleting Temporary Files ...");
			for(File f: tempDir.listFiles()){
				f.delete();
			}
			tempDir.delete();
		}
		pcs.firePropertyChange(LOADING_MESSAGE,null,"Total Load Time: "+(System.currentTimeMillis()-time)/60000.0+" minutes");
	}
	
	
	/**
	 * load terms file
	 * @param file
	 * @throws Exception
	 */
	public void loadText(File file,String name) throws Exception {
		// load tables
		name = (name != null)?name:file.getName();
		
		// strip suffix
		if(name.endsWith(".txt"))
			name = name.substring(0,name.length()-".txt".length());
		this.name = name;
		load(name);
	
		// check if already loaded
		if("done".equals(infoMap.get("status")))
			return;			
				
		// handle memory nightmare (save when you reach 90%)
		MemoryManager.setMemoryThreshold(new Runnable(){
			public void run() {
				crash();
			}
		},0.95);
		
		// load classes for the very first time
		pcs.firePropertyChange(LOADING_MESSAGE,null,"Loading Text from "+file.getAbsolutePath()+" ...");
		
		// save meta information
		infoMap.put("name",name);
		infoMap.put("location",file.getAbsolutePath());
		infoMap.put("stem.words",""+stemWords);
		
		BufferedReader reader = new BufferedReader(new FileReader(file));
		Concept c = new Concept("_");
		List<String> synonyms = new ArrayList<String>();
		int code = 0;
		for(String line=reader.readLine();line != null; line=reader.readLine()){
			line = line.trim();
			
			// junk is a concept delimeter
			if(line.length() == 0 || line.matches("_+") || line.matches("\\d+")){
				// add previous concept
				if(c != null && synonyms != null && synonyms.size() > 0){
					c.setName(synonyms.get(0));
					c.setCode(""+(++code));
					c.setSynonyms(synonyms.toArray(new String [0]));
					addConcept(c);
				}
				// start new concept
				c = new Concept("_");
				synonyms = new ArrayList<String>();
			}else{
				synonyms.add(line);
			}
		}
		reader.close();
		
		// handle last concept
		if(c != null && synonyms != null && synonyms.size() > 0){
			c.setName(synonyms.get(0));
			c.setCode(""+(++code));
			c.setSynonyms(synonyms.toArray(new String [0]));
			addConcept(c);
		}
		
		// save terminology
		pcs.firePropertyChange(LOADING_MESSAGE,null,"Saving Concept Information ...");
		infoMap.put("status","done");
		save();
		
	}
	
	
	/**
	 * returns true if this terminology doesn't contain any terms
	 * @return
	 */
	public boolean isEmpty(){
		return wordMap.isEmpty();
	}
	
	
	/**
	 * get all concept objects in the entire terminology
	 * @return
	 *
	public Collection<Concept> getAllConcepts(){
		return conceptMap.values();
	}
	*/
	
	public void clear(){
		// clear tables
		wordMap.clear();
		wordStatMap.clear();
		termMap.clear();
		regexMap.clear();
		conceptMap.clear();
		infoMap.clear();
		sourceMap.clear();
		rootMap.clear();
				
	}
	
	/**
	 * clear cache
	 */
	public void clearCache(){
		cache.clear();
	}
	
	/**
	 * save all information to disc
	 */
	public void save(){
		if(wordMap instanceof JDBMMap){
			pcs.firePropertyChange(LOADING_PROGRESS,null,"Saving Index Finder Tables ...");
			saveMetaInfo(new File(location,INFO_FILE));
			saveSearchProperteis();
			
			//commit
			((JDBMMap) wordMap).commit();
			((JDBMMap) wordStatMap).commit();
			((JDBMMap) termMap).commit();
			((JDBMMap) conceptMap).commit();
			((JDBMMap) regexMap).commit();
			((JDBMMap) infoMap).commit();
			((JDBMMap) sourceMap).commit();
			((JDBMMap) rootMap).commit();
			
			//defrag
			((JDBMMap) wordMap).compact();
			((JDBMMap) wordStatMap).compact();
			((JDBMMap) termMap).compact();
			((JDBMMap) conceptMap).compact();
			((JDBMMap) regexMap).compact();
			((JDBMMap) infoMap).compact();
			((JDBMMap) sourceMap).compact();
			((JDBMMap) rootMap).compact();
			
			//((JDBMMap) stringMap).commit();
		}
	}
	
	public void dispose(){
		if(wordMap instanceof JDBMMap){
			((JDBMMap) wordMap).dispose();
			((JDBMMap) wordStatMap).dispose();
			((JDBMMap) termMap).dispose();
			((JDBMMap) conceptMap).dispose();
			((JDBMMap) regexMap).dispose();
			((JDBMMap) infoMap).dispose();
			((JDBMMap) sourceMap).dispose();
			((JDBMMap) rootMap).dispose();
		}
	}
	
	/**
	 * ignore digits in concept names for matching
	 * default is false
	 * @param b
	 */
	public void setIgnoreDigits(boolean b){
		stripDigits = b;
	}
	
	/**
	 * use porter stemmer to stem words during search
	 * default is true
	 * @param stemWords
	 */
	public void setStemWords(boolean stemWords) {
		this.stemWords = stemWords;
	}

	
	/**
	 * ignore one letter words to avoid parsing common junk
	 * default is true
	 * @param stemWords
	 */

	public void setIgnoreSmallWords(boolean ignoreSmallWords) {
		this.ignoreSmallWords = ignoreSmallWords;
	}



	/**
	 * add concept to terminology
	 */
	public boolean addConcept(Concept c) throws TerminologyException {
		// don't go into classes that we already visited
		if(conceptMap.containsKey(c.getCode()))
			return true;
		
		// check if read only
		if(conceptMap instanceof JDBMMap && ((JDBMMap)conceptMap).isReadOnly()){
			dispose();
			try {
				load(name,false);
			} catch (IOException e) {
				throw new TerminologyException("Unable to gain write access to data tables",e);
			}
		}
		
		
		// get list of terms
		Set<String> terms = getTerms(c);
		for(String term: terms){
			// check if term is a regular expression
			if(isRegExp(term)){
				regexMap.put("\\b("+term.substring(1,term.length()-1)+")\\b",c.getCode());
			}else{
				// insert concept concept into a set
				Set<String> codeList = new HashSet<String>();
				codeList.add(c.getCode());
				// add concept codes thate were already in a set
				if(termMap.containsKey(term)){
					codeList.addAll(termMap.get(term));
				}
				// insert the set
				termMap.put(term,codeList);
				
				// insert words
				for(String word: TextTools.getWords(term)){
					setWordTerms(word,terms);	
				}
			}
			
		}
		conceptMap.put(c.getCode(),c.getContent());
		return true;
	}
	
	/**
	 * add concept as a root
	 * @param code
	 */
	public boolean addRoot(String code){
		if(conceptMap.containsKey(code)){
			rootMap.put(code,"");	
			return true;
		}
		return false;
	}
	
	/**
	 * only return terms where given word occures
	 * @param workd
	 * @param terms
	 * @return
	 */
	private Set<String> filterTerms(String word, Set<String> terms){
		Set<String> result = new HashSet<String>();
		for(String t: terms){
			if(t.contains(word))
				result.add(t);
		}
		return result;
	}
	
	public boolean removeConcept(Concept c) throws TerminologyException {
		// find concept terms
		if(conceptMap.containsKey(c.getCode()))
			c = convertConcept(conceptMap.get(c.getCode()));
		Set<String> terms = getTerms(c);
		// remove all terms and words
		for(String term: terms){
			termMap.remove(term);
			//remove from words
			for(String word: TextTools.getWords(term)){
				Set<String> list = getWordTerms(word);
				if(list != null){
					list.remove(term);
					// if the only entry, remove the word as well
					if(list.isEmpty())
						wordMap.remove(word);	
				}
			}
		}
		return true;
	}

	public boolean updateConcept(Concept c) throws TerminologyException {
		removeConcept(c);
		addConcept(c);
		return true;
	}

	/**
	 * Get Search Methods supported by this terminology 
	 * Values are
	 * 
	 * best-match : subsumption of concepts, overlap of concepts
	 * all-match  : overlap of concepts
	 * precise-match: subsumption of concepts, overlap of concepts, contiguity of term
	 * nonoverlap-match: subsumption of concepts
	 * partial-match: partial term match, overlap of concepts
	 * custom-match: use flags to tweak search 
	 */
	public String[] getSearchMethods() {
		return new String [] {BEST_MATCH,ALL_MATCH,PRECISE_MATCH,NONOVERLAP_MATCH,PARTIAL_MATCH,CUSTOM_MATCH};
	}
	
	/**
	 * try to find the best possible match for given query
	 */
	public Concept[] search(String text) throws TerminologyException {
		return search(text,defaultSearchMethod);
	}
	
	/**
	 * setup search method
	 * @param metho
	 */
	private void setupSearch(String method){
		if(BEST_MATCH.equals(method)){
			subsumptionMode = true;
			overlapMode = true;
			contiguousMode = true;
			orderedMode = false;
			partialMode = false;
			wordWindowSize = 3;
		}else if(ALL_MATCH.equals(method)){
			subsumptionMode = false;
			overlapMode = true;
			contiguousMode = false;
			orderedMode = false;
			partialMode = false;
			ignoreUsedWords = false;
		}else if(PRECISE_MATCH.equals(method)){
			subsumptionMode = true;
			overlapMode = true;
			contiguousMode = true;
			orderedMode = false;
			partialMode = false;
			wordWindowSize = 1;
		}else if(NONOVERLAP_MATCH.equals(method)){
			subsumptionMode = true;
			overlapMode = false;
			contiguousMode = false;
			orderedMode = false;
			partialMode = false;
		}else if(PARTIAL_MATCH.equals(method)){
			subsumptionMode = false;
			overlapMode = false;
			contiguousMode = false;
			orderedMode = false;
			partialMode = true;
		}
	}
	
	/**
	 * represents a tuple of hashtable and list
	 */
	private static class NormalizedWordsContainer {
		public Map<String,String> normalizedWordsMap;
		public List<String> normalizedWordsList;
		
	}
	
	/**
	 * perform normalization of a string @see normalize, but return unsorted list of words 
	 * @param text
	 * @param stem -stem words
	 * @param strip - strip digits
	 * @return Map<String,String> normalized word for its original form
	 */
	private NormalizedWordsContainer getNormalizedWordMap(String text, boolean stem, boolean stripDigits, boolean stripStopWords){
		NormalizedWordsContainer c = new NormalizedWordsContainer();
		c.normalizedWordsMap = new LinkedHashMap<String, String>();
		c.normalizedWordsList = new ArrayList<String>();
		for(String w: TextTools.getWords(text)){
			List<String> ws = TextTools.normalizeWords(w, stem, stripDigits);
			if(!ws.isEmpty() && !c.normalizedWordsMap.containsKey(ws.get(0)))
				c.normalizedWordsMap.put(ws.get(0),w);
			c.normalizedWordsList.addAll(ws);
		}
		return c;
	}
	
	/**
	 * try to find the best possible match for given query
	 */
	public Concept[] search(String text,String method) throws TerminologyException {
		if(text == null)
			return new Concept[0];
		
		// setup flags
		setupSearch(method);
		
		// do cache
		Concept [] r = null;
		if(cachingEnabled){
			r = cache.get(text);
			if(r != null)
				return r;
		}
		
		// split text into words (don't strip digits)
		NormalizedWordsContainer nwc = getNormalizedWordMap(text,stemWords, stripDigits,true);
		List<String> words = nwc.normalizedWordsList;
		Map<String,String> normWords = nwc.normalizedWordsMap;
		//List<String> words = TextTools.normalizeWords(text,stemWords,stripDigits);
		Set<String> resultTerms = new LinkedHashSet<String>();
		//Map<String,String> normWords = getNormalizeWordMap(text,words);
		Map<Concept,Concept> result = new TreeMap<Concept,Concept>(new Comparator<Concept>() {
			public int compare(Concept o1, Concept o2) {
				if(o2.getCode().equals(o1.getCode()))
					return 0;
				int n = (int)(1000 * (o2.getScore()-o1.getScore()));
				if(n == 0)
					return o2.getCode().compareTo(o1.getCode());
				return n;
			}
		});
			
		// sort if possible
		Collection<String> swords = words;
		if(ignoreUsedWords){
			swords = new TreeSet<String>(new Comparator<String>() {
				public int compare(String o1, String o2) {
					if(wordStatMap.containsKey(o1) && wordStatMap.containsKey(o2)){
						if( wordStatMap.get(o1).termCount == wordStatMap.get(o2).termCount){
							return o1.compareTo(o2);
						}
						return wordStatMap.get(o1).termCount-wordStatMap.get(o2).termCount;
					}
					if(wordStatMap.containsKey(o1))
						return -1;
					return 1;
				}
			});
			swords.addAll(words);
		}else{
			swords = new LinkedHashSet<String>(words);
		}
		

		// search regexp
		for(Concept c: searchRegExp(text)){
			if(!isFilteredOut(c)){
				c.setScore(1.0);
				result.put(c,c);
			}
		}
		
		// for each word
		Set<String> usedWords = new HashSet<String>();
		int count = 0;
		for(String word : swords){
			count ++;
			
			// filter out junk
			if(ignoreSmallWords && word.length() <= 1)
				continue;
			
			// filter out common words
			if(ignoreCommonWords && TextTools.isCommonWord(word))
				continue;
			
			// if word is already in list of used words
			// save time and go on this time, but re-added for
			// later use in case the word is repeated later on
			if(ignoreUsedWords && usedWords.contains(word)){
				continue;
			}
			
			//Arrays.asList(TextTools.getWords(text))
			List<String> textWords = getTextWords(words,count);
			for(String term: getBestTerms(textWords,usedWords,word)){
				resultTerms.add(term);
				if(ignoreUsedWords)
					usedWords.addAll(getUsedWords(textWords,term));
			}
			
		}
		
		// create result list
		//time = System.currentTimeMillis();
		for(String term: resultTerms){
			Set<String> codes = termMap.get(term);
			
			// Derive original looking term
			String oterm = getOriginalTerm(text, term, normWords);
						
			// create 
			List<Concept> termConcepts = new ArrayList<Concept>();
			double score = getDefaultScore(term,oterm,resultTerms);
			for(String code: codes){
				Concept c = convertConcept(code);
				if(c != null){
					c.setInitialized(true);
				}else{
					c = new Concept(code,term);
				}
				// clone
				c = c.clone();
				c.setTerminology(this);
				c.setMatchedTerm(oterm);
				c.setSearchString(text);
				
				if(ignoreAcronyms && isAcronym(c))
					continue;
			
				scoreConcept(c,term,score);
				
				// filter out really bad ones
				if(!scoreConcepts || c.getScore() >= 0.5)
					termConcepts.add(c);
			}
			// add to results
			for(Concept c: getBestCandidates(termConcepts)){
				if(!isFilteredOut(c)){
					// if we have multipe annotations, deal with it better
					if(result.containsKey(c)){
						Concept oc = result.get(c);
						for(String ot: c.getMatchedTerms())
							oc.addMatchedTerm(ot);
						for(Annotation a: c.getAnnotations())
							oc.addAnnotation(a);
					}else
						result.put(c,c);
				}
			}
		}

		// get best candidates
		r =  result.keySet().toArray(new Concept[0]);
		if(cachingEnabled)
			cache.put(text,r);
		return r;
	}
	
	
	private boolean isAcronym(Concept c) {
		for(Term t: c.getTerms()){
			if(("ACR".equals(t.getForm()) || t.getForm().endsWith("AB")) && t.getText().equalsIgnoreCase(c.getMatchedTerm()))
				return true;
		}
		return false;
	}

	/**
	 * optionally limit to a sublist of words
	 * @param words
	 * @return
	 */
	private List<String> getTextWords(List<String> words,int count) {
		// currently there is a bug, so can't use window size with used words
		if(ignoreUsedWords)
			return words;
		// decrement to compensate
		count --;
		if(windowSize > 0 && words.size() > windowSize && count < words.size()){
			int end = (count+windowSize)<words.size()?count+windowSize:words.size();
			return words.subList(count,end);
		}
		return words;
	}

	
	/**
	 * set the maximum size a single term can take, to limit the search for very long input
	 * default is 0, which means no limit
	 * @param n
	 */
	public void setWindowSize(int n){
		windowSize = n;
	}
	
	/**
	 * get original string
	 * @param text
	 * @param term
	 * @param map
	 * @return
	 */
	private String getOriginalTerm(String text, String term, Map<String,String> map){
		StringBuffer ot = new StringBuffer();
		final String txt = text.toLowerCase();
		Set<String> words = new TreeSet<String>(new Comparator<String>() {
			public int compare(String o1, String o2) {
				if(o1.length() > 3)
					o1 = o1.substring(0,o1.length()-1);
				if(o2.length() > 3)
					o2 = o2.substring(0,o2.length()-1);
				int x = txt.indexOf(o1) - txt.indexOf(o2);
				if(x == 0)
					return o1.compareTo(o2);
				return x;
			}
		});
		Collections.addAll(words, term.split(" "));
		for(String s: words){
			String w = map.get(s);
			if(w == null)
				w = s;
			ot.append(w+" ");
		}
		String oterm = ot.toString().trim();
		return oterm;
	}
	
	/**
	 * get normalization  word map
	 * @param text
	 * @param nwords
	 * @return
	 *
	private Map<String,String> getNormalizeWordMap(String text, List<String> nwords){
		String [] owords = TextTools.getWords(text);
		Map<String,String> map = new LinkedHashMap<String, String>();
		for(int i=0,j=0;i<owords.length && j<nwords.size();i++){
			if(normalizeWordMatch(nwords.get(j),owords[i])){
				map.put(nwords.get(j),owords[i]);
				j++;
			}
		}
		return map;
	}
	*/
	
	/**
	 * does normalized version of this word matches to original
	 * @param norm
	 * @param orig
	 * @return
	 *
	public static boolean normalizeWordMatch(String norm, String orig){
		// if normalized version is greater then 3 characters
		// check if the original starts with most of it
		//TOOO: when added >= instead of >, caused word MAY to match to Finding :(
		orig = orig.toLowerCase();
		if(norm.length() >= 3)
			return orig.startsWith(norm.substring(0,norm.length()-1));
		return orig.startsWith(norm);
	}
	*/
	
	
	
	private double getDefaultScore(String term, String oterm, Set<String> resultTerms){
		if(!scoreConcepts)
			return 0.0;
		
		// assign default weight
		double weight = 1.0;
		
		// if this term is subsumed by another term, then make it 0.5
		String [] wterm = term.split(" ");
		double maxCount = 0;
		for(String t: resultTerms){
			int n = TextTools.charCount(t,' ')+1;
			if(maxCount <  n)
				maxCount = n;
			if(!t.equals(term)){
				boolean subsumed  = true;
				for(String w: wterm){
					if(!t.contains(w)){
						subsumed = false;
						break;
					}
				}
				// if word is subsumed, make smaller weight
				if(subsumed){
					weight = 0.5;
				}
			}
		}
		
		// add word count ratio
		weight += 0.2*wterm.length/maxCount;
		
		// penilize common words
		if(TextTools.isCommonWord(term.replaceAll("\\p{Punct}","")))
			weight -= 0.5;
		
		return weight;
	}
	
	private void scoreConcept(Concept c, String normalizedTerm, double weight){
		if(!scoreConcepts)
			return;
		
		// set original text
		String originalTerm = c.getMatchedTerm();
		
		// now look at concept itself if it can be weighted further
		double count = 0;
		for(String s: c.getSynonyms()){
			s = s.toLowerCase();
			
			// check if there is an exact match
			if(s.equalsIgnoreCase(originalTerm)){
				count ++;
				weight += 0.2*1/count;
			}
			
			// check if there is a proposition match, but not structure of
			try{
				if(!s.startsWith("structure of ") && s.matches("(?i).*\\s+(of|at|in|from)\\s+"+originalTerm+".*")){
					weight -= 0.5;
					break;
				}
			}catch(Exception ex){
				// since we are using an original term inside regex, we can have an issue with some characters
				// that will be misinterpreted, hence just ignore the whole test
			}

			// check if it is part of some device
			if(s.contains(","+originalTerm.toLowerCase()+",")){
				weight -= 0.5;
				break;
			}
		}
		// check if we have a normalized match only
		if(count == 0 && TextTools.charCount(normalizedTerm,' ') == 0){
			for(String s: c.getSynonyms()){
				// check if there is only a stemmed matched
				if(TextTools.stem(s).equalsIgnoreCase(normalizedTerm)){
					weight -= 0.5;
					break;
				}
			}
		}
		
		// add small points for more sources
		weight += c.getSources().length*0.01;
		// add some points if exact match to preferred name
		if(c.getName().equalsIgnoreCase(originalTerm))
			weight += 0.1;
		
		
		c.setScore(weight);
	}
	
	
	/**
	 * get best candidates for all concepts that match a single term
	 * @param text
	 * @param concepts
	 * @return
	 */
	private List<Concept> getBestCandidates(List<Concept> concepts){
		// do default
		if(concepts.isEmpty() || !scoreConcepts)
			return concepts;
		// for empty and list of 1, easy to handle
		if(selectBestCandidate){
			// handle another type of default
			if(concepts.size() == 1){
				if(concepts.get(0).getScore() >= 0.5)
					return concepts;
				else
					return Collections.EMPTY_LIST;
			}
			// now find best
			Concept best = null;
			for(Concept c: concepts){
				if(best == null || best.getScore() < c.getScore())
					best = c;
			}
			return Collections.singletonList(best);
		}
		return concepts;
	}
	
	
	
	/**
	 * get all terms associated with a word
	 * @param word
	 * @return
	 */
	private Set<String> getWordTerms(String word){
		return wordMap.get(word);
	}
	
	
	/**
	 * add entry to word table
	 * @param word
	 * @param terms
	 */
	private void setWordTerms(String word,Set<String> terms){
		// filter terms to only include those that contain a given word
		Set<String> termList = filterTerms(word,terms);
		
		// if in temp word folder mode, save in temp directory instead of map
		if(useTempWordFolder && location != null && location.exists()){
			File d = new File(location,TEMP_WORD_DIR);
			if(!d.exists())
				d.mkdirs();
			File f = new File(d,word);
			try {
				BufferedWriter w = new BufferedWriter(new FileWriter(f,true));
				for(String t: termList){
					w.write(t+"\n");
				}
				w.close();
			} catch (IOException e) {
				pcs.firePropertyChange(LOADING_MESSAGE,null,"Warning: failed to create file \""+f.getAbsolutePath()+"\", reason: "+e.getMessage());
			}
		// else do the normal save to MAP	
		}else{
			if(wordMap.containsKey(word)){
				termList.addAll(getWordTerms(word));
			}
			try{
				wordMap.put(word,termList);
				if(wordMap instanceof JDBMMap)
					((JDBMMap) wordMap).commit();
				
			}catch(IllegalArgumentException e ){
				wordMap.put(word,new HashSet<String>(Collections.singleton(word)));
				pcs.firePropertyChange(LOADING_MESSAGE,null,"Warning: failed to insert word \""+word+"\", reason: "+e.getMessage());
				
			}
			// if word already existed, subtract previous value from the total
			if(wordStatMap.containsKey(word))
				totalTermsPerWord -= wordStatMap.get(word).termCount;
			
			WordStat ws = new WordStat();
			ws.termCount = termList.size();
			ws.isTerm = termList.contains(word);
			wordStatMap.put(word,ws);
			totalTermsPerWord += termList.size();
			if(termList.size() > maxTermsPerWord)
				maxTermsPerWord = termList.size();
			
		}
	}
	
	/**
	 * get all used words from this term
	 * @param term
	 * @return
	 */
	private List<String> getUsedWords(List<String> words, String term){
		// if not ignore used words and in overlap mode, return
		if(!ignoreUsedWords && overlapMode)
			return Collections.EMPTY_LIST;
				
		List<String> termWords = new ArrayList<String>();
		Collections.addAll(termWords,TextTools.getWords(term));
		List<String> usedWords = new ArrayList<String>();
		// remove words that are involved in term
		if(overlapMode){
			for(String w: termWords){
				usedWords.add(w);
			}
		}else{
			boolean span = false;
			for(String w: words){
				// if text word is inside terms, then
				if(termWords.contains(w)){
					usedWords.add(w);
					termWords.remove(w);
					span = true;
				}
				if(termWords.isEmpty())
					break;
				if(span)
					usedWords.add(w);
			}
		}
		return usedWords;
	}
	
	
	/**
	 * search through regular expressions
	 * @param text
	 * @return
	 */
	private Collection<Concept> searchRegExp(String term){
		List<Concept> result = null;
		term = new String(term);
		// iterate over expression
		for(String re: regexMap.keySet()){
			// match regexp from file to
			Pattern p = Pattern.compile(re,Pattern.CASE_INSENSITIVE);
			Matcher m = p.matcher( term );
			while ( m.find() ){
				if(result == null)
					result = new ArrayList<Concept>();
				
				String cls_str = regexMap.get(re);
				String txt = m.group(1);    // THIS BETTER BE THERE,
				//System.out.println(cls_str+" "+txt+" for re: "+re);	
				// create concept from class
				Concept c = convertConcept(conceptMap.get(cls_str));
				c = c.clone();
				c.setSearchString(term);
				Annotation.addAnnotation(c, txt,m.start());
				
				// check if results already have similar entry
				// if new entry is better replace the old one
				for(ListIterator<Concept> it = result.listIterator();it.hasNext();){
					Concept b = it.next();
					
					// get offsets of concepts
					int st = c.getOffset();
					int en = c.getOffset()+c.getText().length();
					
					int stb = b.getOffset();
					int enb = b.getOffset()+b.getText().length();
					
					// if concept b (previous concept) is within concept c (new concept)
					if(st <=  stb && enb <= en)
						it.remove();
					
				}
				
				// add concept to result
				result.add(c);
				
				// this is bad, cause this fucks up next match
				// that can potentially overlap, use case ex: \\d vs \\d.\\d
				//term = term.replaceAll(txt,"");
			}
		}
						
		return (result != null)?result:Collections.EMPTY_LIST;
	}
	
	/**
	 * get best term that spans most words
	 * @param words in search string
	 * @param word in question
	 * @return
	 */
	private Collection<String> getBestTerms(List<String> words, Set<String> usedWords, String word){
		// get list of terms that have a given word associated with it
		Set<String> terms = getWordTerms(word);
		if(terms == null || words.isEmpty())
			return Collections.EMPTY_LIST;
		
		// best-match vs all-match
		// in best-match terms that are subsumed by others are excluded 
		List<String> best = new ArrayList<String>();
		int bestCount = 0;
		for(String term: terms){
			// check if term should not be used 
			//if(isFilteredOut(term))
			//	continue;
			
			boolean all = true;
			int hits = 0;
			String [] twords  = TextTools.getWords(term);
			
			// if at least one word not in list of words, don't have a mach
			for(String tword : twords ){
				// if term word doesn't occur in text, then NO match
				if(!words.contains(tword)){
					all = false;
					if(!partialMode)
						break;
				}else{
					// if not in overlap mode,then make sure that this term word is not used already
					if(!overlapMode){
						if(usedWords.contains(tword)){
							all = false;
							hits --;
							if(!partialMode)
								break;
						}
					}
					hits++;	
				}
			}
			
			// do partial match
			if(partialMode && !all && hits > 0){
				//all = hits >= twords.length/2.0;
				all = ((double)hits/twords.length) >= partialMatchThreshold;
			}
			
			// optionally inforce term contiguity in text
			if(all && contiguousMode && twords.length > 1){
				TreeSet<Integer> offs = new TreeSet<Integer>();
				for(String w: twords){
					for(int i=0;i<words.size();i++){
						if(words.get(i).equals(w))
							offs.add(i);
					}
					
				}
				// count gaps between words
				int gaps = 0,p = -1;
				for(int i: offs){
					//if current - previous is more then 1, increase the gap
					if(p > -1 && i-p > wordWindowSize){
						gaps++;
					}
					p = i;
				}
				// now look at gaps
				if(gaps > offs.size()-twords.length){
					all = false;
				}	
			}
			
			
			// optionally inforce term order in text
			if(all && orderedMode && twords.length > 1){
				// if we are here, lets find the original synonym that matched this normalized term
				try {
					boolean ordered = false;
					for(String  code: termMap.get(term)){
						for(String s: lookupConcept(code).getSynonyms()){
							List<String> nwords = TextTools.normalizeWords(s, stemWords);
							//compare with term
							boolean eq = true;
							if(twords.length == nwords.size()){
								eq = nwords.containsAll(Arrays.asList(twords));
							}else{
								eq = false;
							}
							// if equal
							if(eq){
								// we found our term that matches matched term in normalized form
								List<Integer> offs = new ArrayList<Integer>();
								for(String w: nwords){
									for(int i=0;i<words.size();i++){
										if(words.get(i).equals(w))
											offs.add(i);
									}
								}
								// count gaps between words
								int gaps = 0,p = -1;
								for(int i: offs){
									//if current - previous is less then previous
									if(p > -1 && i < p){
										gaps++;
									}
									p = i;
								}
								// now look at gaps, if it is ordered then, stop looking
								if(gaps <= offs.size()-twords.length){
									ordered = true;
									break;
								}
							}
						}
					}
					// reset all variable, if not ordered
					all = ordered;
				}catch (Exception e) {
					//IF we fuck up, OH well, it is not a big deal anyway
				}
			}

			
			
			
			// if all words match
			if(all){
				// if best-match mode, then keep the best term only
				if(subsumptionMode){
					// select the narrowest best
					if(twords.length > bestCount){
						best = new ArrayList<String>();
						best.add(term);
						bestCount = twords.length;
					}else if(twords.length == bestCount){
						best.add(term);
					}
				// else use all-matches mode and keep all of them
				}else{
					best.add(term);
				}
			}	
		}
		return best;
	}
	
	/**
	 * should the concept be filtered out based on some filtering technique
	 * @param c
	 * @return
	 */
	private boolean isFilteredOut(Concept c) {
		boolean filteredOut = false;
		
		// do not filter anything if filtered sources are not set
		if(filteredSources != null && !filteredSources.isEmpty()){
			filteredOut = true;
			Source [] src = c.getSources();
			if(src != null){
				for(Source s: src){
					// if at least one source is contained 
					// in filter list, then do not filter it out
					if(filteredSources.contains(s)){
						filteredOut = false;
						break;
					}
				}
			}else{
				// if we have no sources set,
				// well, meybe we should use this concept
				filteredOut =  false;
			}
			// if we can't find concept or it doesn't have and sources difined
			// discard it (filter out)
			if(filteredOut)
				return true;
		}
		
		// do not filter anything if filtered semantic types are not set
		if(filteredSemanticTypes != null && !filteredSemanticTypes.isEmpty()){
			filteredOut = true;
			SemanticType [] src = c.getSemanticTypes();
			if(src != null){
				for(SemanticType s: src){
					// if at least one source is contained 
					// in filter list, then do not filter it out
					if(filteredSemanticTypes.contains(s)){
						filteredOut = false;
						break;
					}
				}
			}else{
				// if we have no semantic types set,
				// well, meybe we should use this concept
				filteredOut = false;
			}
			// if we can't find concept or it doesn't have and semantic types difined
			// discard it (filter out)
			if(filteredOut)
				return true;
		}
		// keep concept , if everything else is cool
		
		// if we have a match of a small word that is a common word
		// then check exact case, we don't want to match abbreviations
		// by mistake 
		if(checkProblemWords){
			String term = c.getMatchedTerm();
			if(term != null && term.length() < 5 && TextTools.isCommonWord(term)){
				boolean exactMatch = false;
				for(String s: c.getSynonyms()){
					if(s.equals(term)){
						exactMatch = true;
						break;
					}
				}
				if(!exactMatch)
					return true;
			}
			
		}
		
		
		return filteredOut;
			
	}



	/**
	 * get list of normalized terms from from the class
	 * @param name
	 * @return
	 */
	protected Set<String> getTerms(Concept cls){
		return getTerms(cls,stemWords);
	}
	
	/**
	 * get list of normalized terms from from the class
	 * @param name
	 * @return
	 */
	protected Set<String> getTerms(Concept cls, boolean stem){
		if(cls == null)
			return Collections.EMPTY_SET;
		
		String name = cls.getName();
		
		/*
		// no longer applies to Concept object
		// was originally written with IClass in mind
		// strip prefix (if available)
		int i = name.indexOf(":");
		if(i > -1){
			name = name.substring(i+1);
		}
		// now replace all underscores with spaces
		name =  name.toLowerCase().replaceAll("_"," ");
		*/
		Pattern pt = Pattern.compile("(.*)[\\(\\[].*[\\)\\]]");
		Set<String> terms = new HashSet<String>();
		terms.add(TextTools.normalize(name,stem,stripDigits));
		for(String str: cls.getSynonyms()){
			if(isRegExp(str))
				terms.add(str);
			else{
				// strip categories 
				Matcher m = pt.matcher(str);
				if(m.matches())
					str = m.group(1).trim();
				terms.add(TextTools.normalize(str,stem,stripDigits));
			}
		}
		return terms;
	}

	/**
	 * check if string is a regular expression
	 * @param s
	 * @return
	 */
	protected boolean isRegExp(String s){
		return s != null && s.startsWith("/") && s.endsWith("/");
	}
	
	
	/**
	 * get all root concepts. This makes sence if Terminology is in fact ontology
	 * that has heirchichal structure
	 * @return
	 */
	public Concept[] getRootConcepts() throws TerminologyException {
		List<Concept> roots = new ArrayList<Concept>();
		for(String code: rootMap.keySet()){
			Concept c = lookupConcept(code);
			if(c != null)
				roots.add(c);
		}
		return roots.toArray(new Concept [0]);
	}
	

	/**
	 * get related concepts map
	 */
	public Map getRelatedConcepts(Concept c) throws TerminologyException {
		// if we have a class, build the map from it, forget concept
		IClass cls = c.getConceptClass();
		if(cls != null){
			Map<Relation,Concept []> map = new HashMap<Relation,Concept []>();
			map.put(Relation.BROADER,getRelatedConcepts(c,Relation.BROADER));
			map.put(Relation.NARROWER,getRelatedConcepts(c,Relation.NARROWER));
			return map;
		// else see if there is a relation map attached to concept
		}else{
			Map<String,Set<String>> relationMap = c.getRelationMap();
			if(relationMap != null){
				Map<Relation,Concept []> map = new HashMap<Relation,Concept []>();
				for(String key: relationMap.keySet()){
					List<Concept> list = new ArrayList<Concept>();
					for(String cui: relationMap.get(key)){
						Concept con = lookupConcept(cui);
						if(con != null)
							list.add(con);
					}
					map.put(Relation.getRelation(key),list.toArray(new Concept [0]));
				}
				return map;
			}
		}
		// else return an empty map
		return Collections.EMPTY_MAP;
	}
	
	public Concept[] getRelatedConcepts(Concept c, Relation r) throws TerminologyException {
		// if we have a class already, use the ontology
		IClass cls = c.getConceptClass();
		if(cls != null){
			if(r == Relation.BROADER){
				return convertConcepts(cls.getDirectSuperClasses());
			}else if(r == Relation.NARROWER){
				return convertConcepts(cls.getDirectSubClasses());
			}else if(r == Relation.SIMILAR){
				List<IClass> clses = new ArrayList<IClass>();
				for(IClass eq: cls.getEquivalentClasses()){
					if(!eq.isAnonymous()){
						clses.add(eq);
					}
				}
				return convertConcepts(clses);
			}
		// if we don't have a class, use the concept map
		}else if(getRelatedConcepts(c).containsKey(r)){
			return (Concept []) getRelatedConcepts(c).get(r);
		}
		// else return empty list
		return new Concept [0];
	}
	
	private Concept [] convertConcepts(IClass [] clses){
		Concept [] concepts = new Concept[clses.length];
		for(int i=0;i<concepts.length;i++){
			concepts[i] = clses[i].getConcept();
			concepts[i].setCode(getCode(clses[i]));
		}
		return concepts;
	}
	
	private Concept [] convertConcepts(Collection<IClass> clses){
		Concept [] concepts = new Concept[clses.size()];
		int i=0;
		for(IClass cls: clses){
			concepts[i] = cls.getConcept();
			concepts[i].setCode(getCode(cls));
			i++;
		}
		return concepts;
	}
	

	protected Concept convertConcept(Object obj) {
		if(obj instanceof Concept)
			return (Concept) obj;
		if(obj instanceof Concept.Content){
			Concept.Content c = (Concept.Content)obj;
			return (c.concept == null)?new Concept(c):c.concept;
		}
		if(obj instanceof String || obj instanceof URI){
			try{
				return lookupConcept(""+obj);
			}catch(Exception ex){
				// should not generate one
			}
		}
		return null;
	}
	
	public Concept lookupConcept(String cui) throws TerminologyException {
		Concept c =  convertConcept(conceptMap.get(cui));
		if(c != null){
			c.setTerminology(this);
			c.setInitialized(true);
		}
		return c;
	}
	
	/**
	 * Get all supported relations between concepts
	 */
	public Relation[] getRelations() throws TerminologyException {
		return new Relation [] { Relation.BROADER, Relation.NARROWER, Relation.SIMILAR };
	}

	/**
	 * Get all relations for specific concept, one actually needs to explore
	 * a concept graph (if available) to determine those
	 */
	public Relation[] getRelations(Concept c) throws TerminologyException {
		return getRelations();
	}
	
	
	public Source[] getFilterSources() {
		return (filteredSources == null)?new Source [0]:filteredSources.toArray(new Source [0]);
	}
	
	public SemanticType[] getFilterSemanticType() {
		return (filteredSemanticTypes == null)?new SemanticType [0]:filteredSemanticTypes.toArray(new SemanticType [0]);
	}
	
	public String [] getFilterLanguages() {
		return (filteredLanguages == null)?new String [0]:filteredLanguages.toArray(new String [0]);
	}
	
	public Source[] getSources() {
		if(sourceMap != null && !sourceMap.isEmpty())
			return sourceMap.values().toArray(new Source [0]);
		return new Source[]{new Source(getName(),getDescription(),""+getURI())};
	}

	public void setFilterSources(Source[] srcs) {
		if(srcs == null)
			filteredSources = null;
		else{
			//if(filteredSources == null)
			filteredSources = new LinkedHashSet();
			Collections.addAll(filteredSources, srcs);
		}
	}

	public void setFilterSemanticType(SemanticType[] srcs) {
		if(srcs == null)
			filteredSemanticTypes = null;
		else{
		//if(filteredSemanticTypes == null)
			filteredSemanticTypes = new LinkedHashSet();
			Collections.addAll(filteredSemanticTypes, srcs);
		}
	}
	
	public void setFilterLanguages(String [] lang) {
		if(filteredLanguages == null)
			filteredLanguages = new LinkedHashSet();
		Collections.addAll(filteredLanguages, lang);
	}
	
	public void setSelectBestCandidate(boolean selectBestCandidate) {
		this.selectBestCandidate = selectBestCandidate;
		this.scoreConcepts = selectBestCandidate;
	}

	public void setDefaultSearchMethod(String s){
		this.defaultSearchMethod = s;
	}
	
	public String getDescription() {
		if(infoMap != null && infoMap.containsKey("description"))
			return infoMap.get("description");
		return "NobleCoder Terminlogy uses an IndexFinder-like algorithm to map text to concepts.";
	}

	public String getFormat() {
		return "index finder tables";
	}

	public String getLocation() {
		return (location != null)?location.getAbsolutePath():"memory";
	}

	public String getName() {
		if(name != null)
			return name;
		if(location != null)
			return location.getName();
		if(infoMap != null && infoMap.containsKey("name"))
			return infoMap.get("name");
		return "NobleCoder Terminology";
	}

	public URI getURI() {
		return URI.create("http://slidetutor.upmc.edu/curriculum/terminolgies/"+getName().replaceAll("\\W+","_"));
	}

	public String getVersion() {
		if(infoMap != null && infoMap.containsKey("version"))
			return infoMap.get("version");
		return "1.0";
	}

	public String toString(){
		return getName();
	}
	
	/**
	 * don't try to match common English words
	 * @param ignoreCommonWords
	 */
	public void setIgnoreCommonWords(boolean ignoreCommonWords) {
		this.ignoreCommonWords = ignoreCommonWords;
	}
	
	public double getPartialMatchThreshold() {
		return partialMatchThreshold;
	}

	public void setPartialMatchThreshold(double partialMatchThreshold) {
		this.partialMatchThreshold = partialMatchThreshold;
	}


	
	/**
	 * comput concept match score
	 * @param b
	 */
	public void setScoreConcepts(boolean b) {
		this.scoreConcepts = b;
	}

	public boolean isIgnoreDigits() {
		return stripDigits;
	}

	public boolean isIgnoreSmallWords() {
		return ignoreSmallWords;
	}

	public boolean isIgnoreCommonWords() {
		return ignoreCommonWords;
	}

	public boolean isSelectBestCandidate() {
		return selectBestCandidate;
	}

	public int getWindowSize() {
		return windowSize;
	}

	public String getDefaultSearchMethod() {
		return defaultSearchMethod;
	}
	public boolean isIgnoreAcronyms() {
		return ignoreAcronyms;
	}

	public void setIgnoreAcronyms(boolean ignoreAcronyms) {
		this.ignoreAcronyms = ignoreAcronyms;
	}
	public boolean isIgnoreUsedWords() {
		return ignoreUsedWords;
	}

	public void setIgnoreUsedWords(boolean ignoreUsedWords) {
		this.ignoreUsedWords = ignoreUsedWords;
	}

	public boolean isSubsumptionMode() {
		return subsumptionMode;
	}

	public void setSubsumptionMode(boolean subsumptionMode) {
		this.subsumptionMode = subsumptionMode;
	}

	public boolean isOverlapMode() {
		return overlapMode;
	}

	public void setOverlapMode(boolean overlapMode) {
		this.overlapMode = overlapMode;
	}

	public boolean isOrderedMode() {
		return orderedMode;
	}

	public void setOrderedMode(boolean orderedMode) {
		this.orderedMode = orderedMode;
	}

	public boolean isContiguousMode() {
		return contiguousMode;
	}

	public void setContiguousMode(boolean contiguousMode) {
		this.contiguousMode = contiguousMode;
	}

	public boolean isPartialMode() {
		return partialMode;
	}

	public void setPartialMode(boolean partialMode) {
		this.partialMode = partialMode;
	}
	
	
	/**
	 * convert Template to XML DOM object representation
	 * @return
	 */
	public Element toElement(Document doc)  throws TerminologyException{
		Element root = super.toElement(doc);
		Element options = doc.createElement("Options");
		Properties p = getSearchProperties();
		for(Object key: p.keySet()){
			Element opt = doc.createElement("Option");
			opt.setAttribute("name",""+key);
			opt.setAttribute("value",""+p.get(key));
			options.appendChild(opt);
		}
		root.appendChild(options);
		return root;
	}
	
	/**
	 * convert Template to XML DOM object representation
	 * @return
	 */
	public void fromElement(Element element) throws TerminologyException{
		name = element.getAttribute("name");
		String str = element.getAttribute("version");
		if(str.length() > 0)
			infoMap.put("version",str);
		str = element.getAttribute("uri");
		if(str.length() > 0)
			infoMap.put("uri",str);
		str = element.getAttribute("location");
		if(str.length() > 0)
			infoMap.put("location",str);
		
		// get child element
		for(Element e: XMLUtils.getChildElements(element)){
			if("Sources".equals(e.getTagName())){
				for(Element cc: XMLUtils.getElementsByTagName(e,"Source")){
					Source c = new Source("");
					c.fromElement(cc);
					sourceMap.put(c.getName(),c);
				}
			}else if("Relations".equals(e.getTagName())){
				//NOOP
			}else if("Languages".equals(e.getTagName())){
				infoMap.put("languages",e.getTextContent().trim());
			}else if("Roots".equals(e.getTagName())){
				for(String r: e.getTextContent().trim().split(",")){
					rootMap.put(r.trim(),"");
				}
			}else if("Description".equals(e.getTagName())){
				infoMap.put("description",e.getTextContent().trim());
			}else if("Concepts".equals(e.getTagName())){
				for(Element cc: XMLUtils.getElementsByTagName(e,"Concept")){
					Concept c = new Concept("");
					c.fromElement(cc);
					addConcept(c);
				}
			}else if("Options".equals(e.getTagName())){
				Properties p = new Properties();
				for(Element op: XMLUtils.getElementsByTagName(e,"Option")){
					p.setProperty(op.getAttribute("name"),op.getAttribute("value"));
				}
				setSearchProperties(p);
			}
		}
	}
}
