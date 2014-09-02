package edu.pitt.terminology.lexicon;
import java.io.PrintStream;
import java.io.Serializable;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Properties;
import java.util.Set;

import org.w3c.dom.Document;
import org.w3c.dom.Element;

import edu.pitt.info.extract.model.util.XMLUtils;
import edu.pitt.ontology.IClass;
import edu.pitt.ontology.IOntology;
import edu.pitt.terminology.Terminology;
import edu.pitt.terminology.util.TerminologyException;
import edu.pitt.text.tools.TextTools;

/**
 * This class discribes a concept
 * @author Eugene Tseytlin (University of Pittsburgh)
 */
public class Concept implements  Serializable, Comparable<Concept> {
	private static final long serialVersionUID = 1234567890L;
	private boolean initialized;
	private String code, name = "unknown", definition = "", text, searchString;
	private Definition [] definitions = new Definition[0];
	private Source [] sources = new Source[0];
	private SemanticType [] semanticTypes = new SemanticType[0];
	private String [] synonyms = new String [0];
	private Term [] terms = new Term [0];
	private Term preferredTerm;
	private Relation [] relations = null;
	private Map<Source,String> codes;
	private Map<String,Set<String>> relationMap;
	private transient Map<Relation,Concept []> relatedConcepts;
	private Properties properties;
	private int offset;
	private int [] refs;
	private transient Terminology terminology;
	private transient IClass cls;
	private Annotation [] annotations;
	private String [] matchedTerm;
	private transient Content content;
	private double score;

	
	/**
	 * simple object that represents concept content
	 * @author tseytlin
	 */
	public static class Content implements Serializable {
		private static final long serialVersionUID = 1234567890L;
		public transient Concept concept;
		public String code, name;
		public List<Definition> definitions;
		public List<Source> sources;
		public List<SemanticType> semanticTypes;
		public List<String> synonyms;
		public List<Term> terms;
		public Map<String,String> codeMap;
		public Map<String,Set<String>> relationMap;
	}
	
	/**
	 * get concept from storage object
	 * @param c
	 */
	public Concept(Content c){
		code = c.code;
		name = c.name;
		if(c.definitions != null){
			definitions = new Definition [c.definitions.size()];
			for(int i=0;i<definitions.length;i++){
				definitions[i] = c.definitions.get(i);
			}
		}
		if(c.sources != null){
			sources = new Source [c.sources.size()];
			for(int i=0;i<sources.length;i++)
				sources[i] = c.sources.get(i);
		}
		if(c.synonyms != null){
			synonyms = c.synonyms.toArray(new String [0]);
		}
		if(c.semanticTypes != null){
			semanticTypes = new SemanticType [c.semanticTypes.size()];
			for(int i=0;i<semanticTypes.length;i++){
			semanticTypes[i] = c.semanticTypes.get(i);
			}
		}
		if(c.relationMap != null){
			relationMap = c.relationMap;
		}
		if(c.codeMap != null){
			for(String key: c.codeMap.keySet()){
				addCode(c.codeMap.get(key),Source.getSource(key));
			}
		}
		if(c.terms != null){
			terms = new Term [c.terms.size()];
			for(int i=0;i<c.terms.size();i++){
				terms[i] = c.terms.get(i);
			}
		}
	}
	
	/**
	 * get content object
	 * @return
	 */
	public Content getContent(){
		if(content == null){
			Content c = new Content();
			c.name = name;
			c.code = code;
			c.synonyms = new ArrayList<String>();
			Collections.addAll(c.synonyms,synonyms);
			c.relationMap = relationMap;
			if(definitions != null){
				c.definitions = new ArrayList<Definition>();
				Collections.addAll(c.definitions,definitions);
			}
			if(sources != null){
				c.sources = new ArrayList<Source>();
				Collections.addAll(c.sources,sources);
			}
			if(semanticTypes != null){
				c.semanticTypes = new ArrayList<SemanticType> ();
				Collections.addAll(c.semanticTypes,semanticTypes);
			}
			if(codes != null){
				c.codeMap = new HashMap<String, String>();
				for(Source key: codes.keySet()){
					c.codeMap.put(key.getName(),codes.get(key));
				}
			}
			if(terms != null){
				// do best possible job to map terms
				c.terms = new ArrayList<Term>();
				Collections.addAll(c.terms,terms);
			}
			
			c.concept = this;
			content = c;
		}
		return content;
	}
	
	
	/**
	 * simple object that represents concept content
	 * @author tseytlin
	 *
	public static class Content implements Serializable {
		private static final long serialVersionUID = 1234567890L;
		public transient Concept concept;
		public String code, name;
		public String [] definitions, sources, semanticTypes, synonyms,termForms, termLanguages,termSources,semanticTypeCodes, definitionSources;
		public Map<String,String> codeMap;
		public Map<String,Set<String>> relationMap;
	}*/
	
	/**
	 * get concept from storage object
	 * @param c
	 *
	public Concept(Content c){
		code = c.code;
		name = c.name;
		if(c.definitions != null){
			definitions = new Definition [c.definitions.length];
			for(int i=0;i<definitions.length;i++){
				Definition d = Definition.getDefinition(c.definitions[i]);
				if(c.definitionSources != null)
					d.setSource(Source.getSource(c.definitionSources[i]));
				definitions[i] = d;
			}
		}
		if(c.sources != null){
			sources = new Source [c.sources.length];
			for(int i=0;i<sources.length;i++)
				sources[i] = Source.getSource(c.sources[i]);
		}
		if(c.synonyms != null){
			synonyms = c.synonyms;
		}
		if(c.semanticTypes != null){
			semanticTypes = new SemanticType [c.semanticTypes.length];
			for(int i=0;i<semanticTypes.length;i++){
				SemanticType sm = SemanticType.getSemanticType(c.semanticTypes[i]);
				if(c.semanticTypeCodes != null)
					sm.setCode(c.semanticTypeCodes[i]);
				semanticTypes[i] = sm;
			}
		}
		if(c.relationMap != null){
			relationMap = c.relationMap;
		}
		if(c.codeMap != null){
			for(String key: c.codeMap.keySet()){
				addCode(c.codeMap.get(key),Source.getSource(key));
			}
		}
		if(c.termForms != null){
			for(int i=0;i<c.termForms.length;i++){
				String txt = c.synonyms[i];
				String fm = c.termForms[i];
				String sr = c.termSources[i];
				String ln = c.termLanguages[i];
				// if we have a valid value, then add term
				if(fm != null && ln != null && sr != null){
					Term t = new Term(txt);
					t.setLanguage(ln);
					t.setForm(fm);
					t.setSource(Source.getSource(sr));
					addTerm(t);
				}
			}
		}
	}
	*/
	/**
	 * get content object
	 * @return
	 *
	public Content getContent(){
		if(content == null){
			Content c = new Content();
			c.name = name;
			c.code = code;
			c.synonyms = synonyms;
			c.relationMap = relationMap;
			if(definitions != null){
				c.definitions = new String [definitions.length];
				c.definitionSources = new String [definitions.length];
				for(int i=0;i<c.definitions.length;i++){
					c.definitions[i] = definitions[i].getDefinition();
					c.definitionSources[i] = (definitions[i].getSource() != null)?definitions[i].getSource().getName():"";
				}
			}
			if(sources != null){
				c.sources = new String [sources.length];
				for(int i=0;i<c.sources.length;i++)
					c.sources[i] = sources[i].getName();
			}
			if(semanticTypes != null){
				c.semanticTypes = new String [semanticTypes.length];
				c.semanticTypeCodes = new String [semanticTypes.length];
				for(int i=0;i<c.semanticTypes.length;i++){
					c.semanticTypes[i] = semanticTypes[i].getName();
					c.semanticTypeCodes[i] = ""+semanticTypes[i].getCode();
				}
			}
			if(codes != null){
				c.codeMap = new HashMap<String, String>();
				for(Source key: codes.keySet()){
					c.codeMap.put(key.getName(),codes.get(key));
				}
			}
			if(terms != null){
				// do best possible job to map terms
				c.termLanguages = new String [synonyms.length];
				c.termForms = new String [synonyms.length];
				c.termSources = new String [synonyms.length];
				for(int i=0;i<synonyms.length;i++){
					for(Term t : terms){
						// if term matches a synonym, then save it
						if(t.getText().equals(synonyms[i])){
							c.termLanguages[i] = ""+t.getLanguage();
							c.termForms[i] = ""+t.getForm();
							c.termSources[i] = (t.getSource() !=null)?t.getSource().getName():"";
						}
					}
				}
			}
			
			c.concept = this;
			content = c;
		}
		return content;
	}
	*/
	
	/**
	 * Constract a concept. CUI being the sole required argument
	 * @param code
	 */
	public Concept(String code){
		this.code = code;
		this.name = code;
		addSynonym(name);
	}
	
	/**
	 * Constract a concept with CUI and preferred name 
	 * @param code
	 * @param name
	 */
	public Concept(String code, String name){
		this.code = code;
		this.name = name;
		addSynonym(name);
	}

	/**
	 * Constract concept from another concept (copy)
	 * @param c
	 */
	public Concept(Concept c){
		c.copyTo(this);
	}
	
	
	/**
	 * create new concept from a class
	 * @param cls
	 */
	public Concept(IClass cls){
		this.cls = cls;
		
		// figure out name
		String name = cls.getName();
		int i = name.indexOf(":");
		if(i > -1)
			name = name.substring(i+1);
		name =  name.replaceAll("_"," ").toLowerCase();
		
		// assign code and name
		this.code = ""+cls.getURI();
		this.name = name;
		
		IOntology ontology = cls.getOntology();
		setDefinitions(getDefinitions(cls));
		setSources(new Source[] {new Source(ontology.getName(),ontology.getDescription(),""+ontology.getURI())});
		Set<String> labels = new LinkedHashSet<String>();
		labels.add(name);
		Collections.addAll(labels,cls.getLabels());
		setSynonyms(labels.toArray(new String [0]));
		if(ontology instanceof Terminology)
			setTerminology((Terminology)ontology);
		setInitialized(true);
	}
	
	
	/**
	 * get concept definitions
	 * @return
	 */
	private Definition [] getDefinitions(IClass cls){
		String [] com = cls.getComments();
		Definition [] d = new Definition[com.length];
		for(int i=0;i<d.length;i++)
			d[i] = new Definition(com[i]);
		return d;
	}
	
	
	/**
	 * get concept class
	 * @return
	 */
	public IClass getConceptClass(){
		return cls;
	}
	
	/**
	 * Concept object is only required to contain a CUI
	 * the rest of the information can be requested from the
	 * server on demand. This method must be invoked to request that
	 * information 
	 */
	public void initialize() throws TerminologyException{
		if(terminology != null){
			Concept c = terminology.lookupConcept(code);
			if(c != null)
				c.copyTo(this);
			initialized = true;
		}
	}
	
	
	/**
	 * Copy content of this concept to target concept
	 * @param c
	 */
	private void copyTo(Concept c){
		c.setCode(getCode());
		c.setTerminology(getTerminology());
		c.setName(getName());
		c.setText(getText());
		c.setOffset(getOffset());
		c.setDefinitions(getDefinitions());
		c.setSources(getSources());
		c.setProperties(getProperties());
		c.setSemanticTypes(getSemanticTypes());
		c.setRelations(getRelations());
		c.setSynonyms(getSynonyms());
		c.setTerms(terms);
		c.setAnnotations(getAnnotations());
		c.setMatchedTerm(getMatchedTerm());
		c.setSearchString(getSearchString());
		Map map = getCodes();
		if(map != null)
			for(Object n: map.keySet())
				c.addCode((String)map.get(n),(Source)n);
	}
	
	
	/**
	 * get a copy of this dataset
	 */
	public Concept clone(){
		Concept c = new Concept(getContent());
		c.setMatchedTerm(getMatchedTerm());
		c.setSearchString(getSearchString());
		c.setScore(getScore());
		return c;
	}
	
	
	/**
	 * Pick some definition from the set of definitions (if available)
	 * @return
	 */
	public String getDefinition(){
		if(definition == null || definition.length() == 0){
			if(definitions != null){
				// search for preferred definition
				// if none, found last one is used
				for(int i=0;i<definitions.length;i++){
					definition = definitions[i].getDefinition();
					if(definitions[i].isPreferred())
						break;
				}
			}
		}
		return definition;
	}
	
	/**
	 * score is a level of confidence from 0 to 1.0 that a terminology MAY
	 * assign to a discovered concept, not all terminologies may assigne scores.
	 * @return value from 0 to 1.0
	 */
	public double getScore() {
		return score;
	}

	/**
	 * score is a level of confidence from 0 to 1.0 that a terminology MAY
	 * assign to a discovered concept, not all terminologies may assigne scores.
	 * @return
	 */
	public void setScore(double score) {
		this.score = score;
	}

	
	/**
	 * Name should be returned as a string representation
	 */
	public String toString(){
		//return name;
		return code;
	}
	
	/**
	 * Get Concept Unique Identifier
	 * @return the code
	 */
	public String getCode() {
		return code;
	}
	
	/**
	 * Get Concept Unique Identifier
	 * @return the code
	 * @see setCUI()
	 */
	public void setCode(String code) {
		this.code = code;
	}
	
	/**
	 * @return the definitions
	 */
	public Definition [] getDefinitions() {
		return (definitions != null)?definitions: new Definition [0];
	}

	/**
	 * @param definitions the definitions to set
	 */
	public void setDefinitions(Definition [] definitions) {
		this.definitions = definitions;
	}
	
	/**
	 * add synonym
	 * @param synonym
	 */
	public void addDefinition(Definition def){
		setDefinitions(TextTools.addAll(getDefinitions(),def));
	}

	/**
	 * @return the name
	 */
	public String getName() {
		return name;
	}

	/**
	 * @param name the name to set
	 */
	public void setName(String name) {
		this.name = name;
	}

	/**
	 * @return the properties
	 */
	public Properties getProperties() {
		if(properties == null)
			properties = new Properties();
		return properties;
	}

	/**
	 * @param properties the properties to set
	 */
	public void setProperties(Properties p) {
		Properties prop = getProperties();
		prop.putAll(p);
		/*
		for(Iterator i=p.keySet().iterator();i.hasNext();){
			String key = (String) i.next();
			prop.setProperty(key,p.getProperty(key));
		}
		*/
	}


	/**
	 * @return the sources
	 */
	public Source [] getSources() {
		return (sources != null)?sources:new Source [0];
	}

	/**
	 * @param sources the sources to set
	 */
	public void setSources(Source [] sources) {
		this.sources = sources;
	}

	/**
	 * add synonym
	 * @param synonym
	 */
	public void addSource(Source src){
		// check if it is there already
		for(Source s: getSources())
			if(s.equals(src))
				return;
		setSources(TextTools.addAll(getSources(),src));
	}
	
	/**
	 * @return the synonyms
	 */
	public String [] getSynonyms() {
		return (synonyms != null)?synonyms:new String [0];
	}

	/**
	 * @param synonyms the synonyms to set
	 */
	public void setSynonyms(String [] synonyms) {
		this.synonyms = synonyms;
	}

	/**
	 * add synonym
	 * @param synonym
	 */
	public void addSynonym(String synonym){
		// check if it is there already
		for(String s: getSynonyms())
			if(s.equals(synonym))
				return;
		setSynonyms(TextTools.addAll(getSynonyms(),synonym));
	}
	
	/**
	 * @return the initialized
	 */
	public boolean isInitialized() {
		return initialized;
	}
	
	
	/**
	 * If concept is extracted from some text, then 
	 * start position is the offset of the exact string 
	 * that the concept covers in the phrase/sentance/doc
	 * @return the offset
	 */
	public int getOffset() {
		return offset;
	}

	/**
	 * @param offset the offset to set
	 */
	public void setOffset(int offset) {
		this.offset = offset;
	}

	/**
	 * If concept is extracted from some text, then 
	 * text is the exact string that the concept covers.
	 * @return the text
	 */
	public String getText() {
		if(text == null){
			if(searchString != null){
				// try to find what matches what
				matchText(searchString);
			}else
				text = name;
		}
		return text;
	}

	
	/**
	 * remove weird chars from string
	 * @param str
	 * @return
	 */
	private String filter(String str){
		// lowercase
		String str2 = str.toLowerCase();
		
		// get rid of non-word chars
		str2 = str2.replaceAll("\\W"," ");
		
		// strip posesive
		str2 = str2.replaceAll("'s\\b","  ");
		
		// get rid of stop words
		// replace with something not intellegible
		// that won't match to anything
		// if word is all uppoer case, it could be useful though
		if(TextTools.isStopWord(str2) && !str.matches("[A-Z]+"))
			str2 = "@#$%&";
		
		return str2.trim();
	}
	
	/**
	 * get number of chars
	 * @param str
	 * @param test
	 * @return
	 */
	private int charCount(String str, char test){
		int n = 0;
		char [] a = str.toCharArray();
		for(int i=0;i<a.length;i++)
			if(a[i] == test)
				n++;
		return n;
	}
	
	
	/**
	 * match text, setup text and offset
	 * @param query
	 * @return
	 */
	private void matchText(String query){
		//long time = System.currentTimeMillis();
		String [] words = TextTools.getWords(query);
		String [] fwords = new String [words.length];
		String [] swords = new String [words.length];
		String [] pwords = new String [words.length];
		// convert words to singular strip possessive etc
		for(int i=0;i<fwords.length;i++){
			fwords[i] = filter(words[i]);
			swords[i] = TextTools.stem(fwords[i]);
			pwords[i] = TextTools.convertToSingularForm(fwords[i]);
		}
				
		//	(?i) case insentetive
		int hits = 0;
		refs = new int [words.length];
		String [] terms = synonyms;
		
		// if we know which synonym matched, then use it,
		//String name = getName();
		if(matchedTerm != null){
			terms = getMatchedTerms();		
			//name = matchedTerm;
		}
		// go over all available tersm
		for(int i=0;i<terms.length;i++){
			if(isRegExp(terms[i]))
				continue;
			
			String synonym = filter(terms[i]);
			for(int j=0;j<fwords.length;j++){
				if(fwords[j].length() == 0)
					continue;
				// check original word, then stem, then singular
				if( synonym.matches(".*\\b"+fwords[j]+"\\b.*") ||
				    (swords[j].length() > 3 && synonym.matches(".*\\b"+swords[j]+".*")) ||
				    synonym.matches(".*\\b"+pwords[j]+"\\b.*")){
					if(refs[j] == 0)
						hits ++;
					refs[j]++;
				}
			}
		}
		
		
		// lets do gap analysis, if we have multi-word concept
		// then most words should be withing some window of eachother
		// if there is a lone word somewhere far it is probably an outlier
		//System.out.println("map of -"+query+"-"+Arrays.toString(getWordMap()));
		/*if(hits > 1 && hits > charCount(name,' ')+1){
			final int WINDOW_SIZE = 3;
			int windowCount = -1, wordPosition = -1;
			for(int i=0;i<refs.length;i++){
				// if window count is greater then threshold
				// then last word was an outlier and should be
				// "deleted" from word map
				if(windowCount >= WINDOW_SIZE && wordPosition > -1 ){
					refs[wordPosition] = 0;
				}
				
				
				// once we hit a word, start counting the window
				if(refs[i] > 0){
					// remember position, if we exceeded max window
					// or has not started counting, else ignore pos
					if(windowCount < 0 || windowCount > WINDOW_SIZE){
						wordPosition = i;
					}else{
						wordPosition = -1;
					}
					windowCount =  0;
				}else if(windowCount >= 0){
					// if we initialized window, then increment it
					windowCount ++;
				}
			}
			// clear potential outlier to the right
			if(wordPosition > -1){
				refs[wordPosition] = 0;
			}
			//System.out.println(query+Arrays.toString(getWordMap()));
		}*/
		
		
		// analyze found words
		// get bounds
		int i=0,j=refs.length-1;
		while(i<=j ){
			if(refs[i]==0)
				i++;
			if(refs[j]==0)
				j--;
			if(i >= refs.length || (refs[i]  > 0 && refs[j] > 0))
				break;
		}
		
		// rebuild the string
		if(i<= j){
			// calculate offset to start search for words
			// to avoid finding short words in other words before them
			int sti,eni,k;
			for(sti=0,k=0;k<i;sti+=words[k].length(),k++);
			for(eni=0,k=0;k<j;eni+=words[k].length(),k++);
			
			// now calculate the offset
			int st = query.indexOf(words[i],sti);
			int en = query.indexOf(words[j],eni)+words[j].length();
			//System.out.println((System.currentTimeMillis()-time));
			
			// set member vars
			try{
				text   = query.substring(st,en);
				offset = st;
			}catch(Exception ex){
				text = query;
			}
			
			//System.out.println(text+" "+sti+" "+st+" "+en+" "+Arrays.toString(getWordMap()));
		}
		//System.out.println("time="+(System.currentTimeMillis()-time));
	}
	
	/**
	 * get an array of hit words in matched text (from getText())
	 * @return
	 */
	public int [] getWordMap(){
		// try to get word map in the unique case, where we have text, but not map
		// most likely cause is that this concept came from regexp
		if(refs == null && searchString != null && text != null){
			String [] words = TextTools.getWords(searchString);
			refs = new int [words.length];
			
			boolean span = false;
			for(int i=0;i< words.length;i++){
				if(text.startsWith(words[i]))
					span = true;
				if(span)
					refs[i] = 1;
				if(text.endsWith(words[i]))
					span = false;
			}
			
			
		}
		return (refs != null)?refs:new int [0];
	}
	
	
	/**
	 * @param text the text to set
	 */
	public void setText(String text) {
		this.text = text;
	}

	/**
	 * @return the terminology
	 */
	public Terminology getTerminology() {
		return terminology;
	}

	/**
	 * @param terminology the terminology to set
	 */
	public void setTerminology(Terminology terminology) {
		this.terminology = terminology;
	}


	/**
	 * @return the symanticTypes
	 */
	public SemanticType [] getSemanticTypes() {
		return semanticTypes != null?semanticTypes: new SemanticType [0];
	}

	/**
	 * @param symanticTypes the symanticTypes to set
	 */
	public void setSemanticTypes(SemanticType[] semanticTypes) {
		this.semanticTypes = semanticTypes;
	}
	
	/**
	 * @param symanticTypes the symanticTypes to set
	 */
	public void addSemanticType(SemanticType semanticType) {
		// check if it is there already
		for(SemanticType s: getSemanticTypes())
			if(s.equals(semanticType))
				return;
		setSemanticTypes(TextTools.addAll(getSemanticTypes(),semanticType));
	}
	
	
	/**
	 * add related concept
	 * @param r - relationship in question
	 * @param code - code of the related concept
	 */
	public void addRelatedConcept(Relation r, String code){
		if(relationMap == null)
			relationMap = new HashMap<String, Set<String>>();
		Set<String> list = relationMap.get(r.getName());
		if(list == null){
			list = new LinkedHashSet<String>();
			relationMap.put(r.getName(),list);
		}
		list.add(code);
	}
	
	/**
	 * print info
	 * @param stream
	 */
	public void printInfo(PrintStream out){
		out.println(getName()+" ("+getCode()+")\t"+Arrays.toString(getSemanticTypes()));
		out.println("\tdefinition:\t"+getDefinition());
		out.println("\tsynonyms:\t"+Arrays.toString(getSynonyms()));
		out.println("\tsources:\t"+Arrays.toString(getSources()));	
		//if(relations != null)
		//	out.println("\trelations:\t"+Arrays.toString(relations));	
	}

	/**
	 * @return the parentConcepts
	 */
	public Concept[] getParentConcepts() throws TerminologyException {
		return getRelatedConcepts(Relation.BROADER);
	}

	/**
	 * @return the parentConcepts
	 */
	public Concept[] getChildrenConcepts() throws TerminologyException {
		return getRelatedConcepts(Relation.NARROWER);
	}

	/**
	 * @return the relations
	 */
	public Relation[] getRelations() {
		try{
			if(relations == null && terminology != null)
				relations = terminology.getRelations(this);
		}catch(TerminologyException ex){
			relations = new Relation [0];
		}
		return relations;
	}

	/**
	 * @param relations the relations to set
	 */
	public void setRelations(Relation[] relations) {
		this.relations = relations;
	}

	/**
	 * @return the relatedConcepts
	 */
	public Concept [] getRelatedConcepts(Relation relation) throws TerminologyException {
		return (getRelatedConcepts().containsKey(relation))?getRelatedConcepts().get(relation):new Concept [0];
	}

	/**
	 * @return the relatedConcepts
	 */
	public Map<Relation,Concept []>  getRelatedConcepts() throws TerminologyException {
		// if there was a privous request, get cache
		if(relatedConcepts == null){
			relatedConcepts = new HashMap<Relation,Concept []>();
		
			// see if this information is available locally
			if(terminology != null)
				relatedConcepts.putAll(terminology.getRelatedConcepts(this));
			
		}
		return relatedConcepts;
	}
	
	/**
	 * get relation map that is associated with this concept 
	 * @return
	 */
	
	public Map<String,Set<String>> getRelationMap(){
		return relationMap;
	}
	
	/**
	 * @param initialized the initialized to set
	 */
	public void setInitialized(boolean initialized) {
		this.initialized = initialized;
	}
	
	
	/**
	 * get preferred term
	 * @return
	 */
	public Term getPreferredTerm(){
		// get preferred term from terms
		if(preferredTerm == null){
			if(terms != null){
				for(int i=0;i<terms.length;i++){
					if(terms[i].isPreferred()){
						preferredTerm = terms[i];
						break;
					}
				}
			}
		}
		// if preferred term is still null, make one up
		if(preferredTerm == null)
			preferredTerm = new Term(getName());
		return preferredTerm;
	}

	/**
	 * @return the terms
	 */
	public Term[] getTerms() {
		if(terms == null || terms.length == 0){
			Set<Term> termList = new LinkedHashSet<Term>();
			Term t = Term.getTerm(name);
			t.setPreferred(true);
			//t.setForm("PT");
			termList.add(t);
			for(String s: getSynonyms()){
				t = Term.getTerm(s);
				if(isRegExp(s)){
					t.setText(s.substring(1,s.length()-1));
					t.setForm("RegEx");
				}
				termList.add(t);
			}
			terms = termList.toArray(new Term [0]);
		}
		//return (terms != null)?terms:new Term [0];
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
	 * @param terms the terms to set
	 */
	public void setTerms(Term[] terms) {
		this.terms = terms;
	}
	
	/**
	 * add synonym
	 * @param synonym
	 */
	public void addTerm(Term term){
		setTerms(TextTools.addAll((terms != null)?terms:new Term [0],term));
		String t = term.getText();
		addSynonym(term.isRegularExpression()?"/"+t+"/":t);
	}
	
	/**
	 * add a code for some source
	 * @param code
	 * @param source
	 */
	public void addCode(String code, Source source){
		if(codes == null)
			codes = new HashMap<Source,String>();
		codes.put(source,code);
	}
	
	/**
	 * Return a code for a specific source
	 * if code is not found, return null
	 * @param source
	 * @return
	 */
	public String getCode(Source source){
		if(codes != null)
			return (String) codes.get(source);
		return null;
	}
	
	/**
	 * get mapping of codes from different sources
	 * @return
	 */
	public Map getCodes(){
		return codes;
	}

	/**
	 * if concept was searched, what was the original search query
	 * @return the searchQuery
	 */
	public String getSearchString() {
		return searchString;
	}

	/**
	 * @param searchQuery the searchQuery to set
	 */
	public void setSearchString(String searchQuery) {
		this.searchString = searchQuery;
	}
	
	/**
	 * is concept fully covered by search string
	 * @return
	 */
	public boolean isFullyCovered(){
		if(searchString != null){
			String ss = searchString.toLowerCase();
			for(String s: getSynonyms()){
				if(ss.contains(s))
					return true;
			}
			return false;
		}
		return true;
	}
	
	/**
	 * this class is a comparator that sorts Concepts based on length of
	 * text found in search string
	 * @author tseytlin
	 */
	public static class TextLengthComparator implements Comparator, Serializable{ 
		public int compare(Object o1, Object o2){
			if(o1 instanceof Concept && o2 instanceof Concept){
				String t1 = ((Concept)o1).getText();
				String t2 = ((Concept)o2).getText();
				t1 = (t1 == null)?"":t1; 
				t2 = (t2 == null)?"":t2;
				return t2.length() - t1.length();
			}
			return 0;	
		}
	};
	
	/**
	 * this class is a comparator that sorts Concepts based on name
	 * @author tseytlin
	 */
	public static class NameComparator implements Comparator, Serializable{ 
		public int compare(Object o1, Object o2){
			if(o1 instanceof Concept && o2 instanceof Concept){
				String t1 = ((Concept)o1).getName();
				String t2 = ((Concept)o2).getName();
				t1 = (t1 == null)?"":t1; 
				t2 = (t2 == null)?"":t2;
				return t1.compareTo(t2);
			}
			return 0;	
		}
	}

	public boolean equals(Object e) {
		if(e != null && e instanceof Concept)
			return getCode().equals(((Concept)e).getCode());
		return false;
	}

	public int hashCode() {
		return getCode().hashCode();
	};
	
	
	public String getMatchedTerm() {
		return (matchedTerm != null && matchedTerm.length > 0)?matchedTerm[0]:null;
	}
	public String [] getMatchedTerms() {
		return matchedTerm;
	}

	public void setMatchedTerm(String matchedTerm) {
		if(matchedTerm != null)
			this.matchedTerm = new String [] {matchedTerm};
	}
	public void addMatchedTerm(String matchedTerm) {
		if(this.matchedTerm == null){
			setMatchedTerm(matchedTerm);
		}else{
			this.matchedTerm = TextTools.addAll(this.matchedTerm,matchedTerm);
		}
	}
	
	/**
	 * set annotations
	 * @param a
	 */
	public void setAnnotations(Annotation [] a){
		annotations = a;
	}
	
	/**
	 * add annotation
	 * @param a
	 */
	public void addAnnotation(Annotation a){
		if(annotations == null){
			setAnnotations(new Annotation []{a});
		}else{
			// don't add annotation that is already there
			for(Annotation s: annotations){
				if(s.equals(a))
					return;
			}
			setAnnotations(TextTools.addAll(annotations,a));
		}
	}
	
	/**
	 * get annotations
	 * @return
	 */
	public Annotation [] getAnnotations(){
		if(annotations == null){
			if(searchString != null){
				// do our regular matching
				matchText(searchString);
				
				// go over words
				String [] words = TextTools.getWords(searchString);
				int [] wMap = getWordMap();
				if(words.length == wMap.length){
					List<Annotation> as = new ArrayList<Annotation>();
					int end = 0;
					for(int i=0;i<words.length;i++){
						if(wMap[i] > 0){
							int st = searchString.indexOf(words[i],end);
							Annotation a = new Annotation();
							a.setConcept(this);
							a.setText(words[i]);
							a.setOffset(st);
							a.setSearchString(searchString);
							as.add(a);
							end = a.getEndPosition()+1;
						}else
							end += words[i].length()+1;
					}
					annotations = as.toArray(new Annotation [0]);
				}else{
					Annotation a = new Annotation();
					a.setConcept(this);
					a.setText(getText());
					a.setOffset(getOffset());
					a.setSearchString(searchString);
					annotations = new Annotation [] {a};
				}
			}else{
				annotations = new Annotation [0];
			}
		}
		return annotations;
	}

	public int compareTo(Concept o) {
		return getName().compareTo(o.getName());
	}
	
	/**
	 * convert to DOM element
	 * @param doc
	 * @return
	 */
	public Element toElement(Document doc) throws TerminologyException {
		Element e = doc.createElement("Concept");
		e.setAttribute("name",getName());
		e.setAttribute("code",getCode());
		for(Definition d: getDefinitions()){
			e.appendChild(d.toElement(doc));
		}
		for(SemanticType st: getSemanticTypes()){
			e.appendChild(st.toElement(doc));
		}
		for(Source src: getSources()){
			Element sr = doc.createElement("Source");
			sr.setAttribute("name",src.getName());
			e.appendChild(sr);
		}
		for(Term t: getTerms()){
			e.appendChild(t.toElement(doc));
		}
		if(codes != null && !codes.isEmpty()){
			Element ce = doc.createElement("Codes");
			for(Source src: codes.keySet()){
				String cd = codes.get(src);
				Element cc = doc.createElement("Code");
				cc.setAttribute("source",src.getName());
				cc.setAttribute("code",cd);
				ce.appendChild(cc);
			}
			e.appendChild(ce);
		}
		if(relationMap != null && !relationMap.isEmpty()){
			Element ce = doc.createElement("Relations");
			for(String r: relationMap.keySet()){
				Set<String> codes = relationMap.get(r);
				Element cc = doc.createElement("Relation");
				cc.setAttribute("name",r);
				String t = ""+codes;
				cc.setTextContent(t.substring(1,t.length()-1));
				ce.appendChild(cc);
			}
			e.appendChild(ce);
		}
		
		
		return e;
	}
	/**
	 * convert from DOM element
	 * @param element
	 * @throws TerminologyException
	 */
	public void fromElement(Element e) throws TerminologyException{
		if(e.getTagName().equals("Concept")){
			setName(e.getAttribute("name"));
			setCode(e.getAttribute("code"));
			for(Element c: XMLUtils.getChildElements(e)){
				if("Term".equals(c.getTagName())){
					Term d = new Term("");
					d.fromElement(c);
					addTerm(d);
				}else if("Definition".equals(c.getTagName())){
					Definition d = new Definition();
					d.fromElement(c);
					addDefinition(d);
				}else if("Source".equals(c.getTagName())){
					Source d = new Source();
					d.fromElement(c);
					addSource(d);
				}else if("SemanticType".equals(c.getTagName())){
					SemanticType d = new SemanticType("");
					d.fromElement(c);
					addSemanticType(d);
				}else if("Relations".equals(c.getTagName())){
					for(Element r: XMLUtils.getElementsByTagName(c,"Relation")){
						Relation rl = Relation.getRelation(r.getAttribute("name"));
						for(String cd: r.getTextContent().trim().split(","))
							addRelatedConcept(rl, cd.trim());
					}
				}else if("Codes".equals(c.getTagName())){
					for(Element r: XMLUtils.getElementsByTagName(c,"Code")){
						Source sr = Source.getSource(r.getAttribute("source"));
						String cd = r.getAttribute("code");
						addCode(cd, sr);
					}
				}
			}
		}
	}
}
