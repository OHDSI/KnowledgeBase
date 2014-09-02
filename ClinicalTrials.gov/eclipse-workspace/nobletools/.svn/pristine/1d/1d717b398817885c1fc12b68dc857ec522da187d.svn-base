package edu.pitt.terminology.client;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.net.URI;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

import javax.swing.Timer;

import edu.pitt.terminology.AbstractTerminology;
import edu.pitt.terminology.Terminology;
import edu.pitt.terminology.lexicon.Concept;
import edu.pitt.terminology.lexicon.Definition;
import edu.pitt.terminology.lexicon.Relation;
import edu.pitt.terminology.lexicon.SemanticType;
import edu.pitt.terminology.lexicon.Source;
import edu.pitt.terminology.lexicon.Term;
import edu.pitt.terminology.util.TerminologyException;
import edu.pitt.text.tools.TextTools;


/**
 * connect to UMLS compatible RRF database schema
 * @author tseytlin
 *
 */
public class UMLSTerminology extends AbstractTerminology {
	public static final String SEARCH_EXACT = "exactMatch";
	public static final String SEARCH_STARTS_WITH = "startsWith";
	public static final String SEARCH_ENDS_WITH = "endsWith";
	public static final String SEARCH_CONTAINS = "contains";
	public static final String SEARCH_BEST = "bestMatch";
	public static final String SEARCH_NGRAM = "ngramMatch";
	
	private String lang = "ENG";
	private String driver,url,user,pass;
	private Connection conn;
	private Source [] sources, filterSources;
	
	/**
	 * connect to new URML instance
	 * @param driver
	 * @param url
	 * @param user
	 * @param pass
	 */
	public UMLSTerminology(String driver,String url,String user, String pass){
		this.driver = driver;
		this.url = url;
		this.user = user;
		this.pass = pass;
	}
	
	
	/**
	 * get connection to the database
	 * @return
	 * @throws Exception
	 */
	private Connection getConnection() throws Exception{
		if(conn == null){
    		Class.forName(driver).newInstance();
			conn = DriverManager.getConnection(url,user,pass);
			// add timer to disconnect after an hour
			Timer t = new Timer(60*60*1000,new ActionListener(){
				public void actionPerformed(ActionEvent e) {
					if(conn != null){
						try{
							conn.close();
						}catch(SQLException ex){
							
						}
						conn = null;
					}
				}
				
			});
			t.setRepeats(false);
			t.start();
		}
    	return conn;
	}
	
	
	protected Concept convertConcept(Object obj) {
		//NOOP
		return null;
	}

	public Source[] getFilterSources() {
		return filterSources;
	}

	public Concept[] getRelatedConcepts(Concept c, Relation r) throws TerminologyException {
		// TODO Auto-generated method stub
		return null;
	}

	public Map getRelatedConcepts(Concept c) throws TerminologyException {
		// TODO Auto-generated method stub
		return null;
	}

	
	/**
	 * set default language (english is default), null is everything
	 * @param l
	 */
	public void setLanguage(String l){
		lang = l;
	}
	
	public String getLanguage(){
		return lang;
	}
	
	public Source[] getSources() {
		if(sources == null){
			try{
				Connection con = getConnection();
				
				Set<Source> srcs = new HashSet<Source>();
				
				// lookup main concept info
				PreparedStatement st = con.prepareStatement("SELECT * FROM mrsab");
				ResultSet result =  st.executeQuery();
				while(result.next()){
					String src  = result.getString("rsab");
					String text = result.getString("son");
					
					Source source = Source.getSource(src);
					source.setDescription(text);
					
					srcs.add(source);

				}
				result.close();
				st.close();
				
				sources = srcs.toArray(new Source [0]);
			}catch(Exception ex){
				ex.printStackTrace();
			}
			
		}
		return sources;
	}

	/**
	 * get concept entry for a cui
	 */
	public Concept lookupConcept(String cui) throws TerminologyException {
		try{
			Connection con = getConnection();
			
			// get list of terms
			Set<String> synonyms = new HashSet<String>();
			Set<Source> sources = new HashSet<Source>();
			Set<Term> terms = new HashSet<Term>();
			Set<SemanticType> semanticTypes = new LinkedHashSet<SemanticType>();
			Set<Definition> definitions = new LinkedHashSet<Definition>();
			Map<String, Source> codes = new HashMap<String,Source>();
			Term preferred = null;
			
			// lookup main concept info
			PreparedStatement st = con.prepareStatement("SELECT * FROM mrconso WHERE cui = ? "+((lang != null)?" AND lat = ?":""));
			st.setString(1,cui);
			if(lang != null)
				st.setString(2,lang);
			ResultSet result =  st.executeQuery();
			while(result.next()){
				String src  = result.getString("sab");
				String text = result.getString("str");
				String lang = result.getString("lat");
				String form = result.getString("tty");
				String code = result.getString("code");
				String pref = result.getString("ispref");
				Source source = Source.getSource(src);
				
				Term term = new Term(text);
				term.setForm(form);
				term.setLanguage(lang);
				term.setSource(source);
				if("y".equalsIgnoreCase(pref))
					term.setPreferred(true);
				
				synonyms.add(text);
				sources.add(source);
				terms.add(term);
				codes.put(code,source);
				
				if(preferred == null && term.isPreferred())
					preferred = term;
			}
			result.close();
			st.close();
			
			// if no terms, then no cod
			if(terms.isEmpty())
				return null;
			
			
			// lookup definitions
			st = con.prepareStatement("SELECT * FROM mrdef WHERE cui = ?");
			st.setString(1,cui);
			result =  st.executeQuery();
			while(result.next()){
				String src  = result.getString("sab");
				String text = result.getString("def");
				
				Definition d = Definition.getDefinition(text);
				d.setSource(Source.getSource(src));
				
				definitions.add(d);
			}
			result.close();
			st.close();
			
			
			// lookup semantic type
			st = con.prepareStatement("SELECT * FROM mrsty WHERE cui = ?");
			st.setString(1,cui);
			result =  st.executeQuery();
			while(result.next()){
				String text  = result.getString("sty");
				semanticTypes.add(SemanticType.getSemanticType(text));
			}
			result.close();
			st.close();
			
			// change ter
			if(preferred == null)
				preferred = terms.iterator().next();
			
			// stup concept
			Concept c = new Concept(cui);
			c.setTerminology(this);
			if(preferred != null)
				c.setName(preferred.getText());
			c.setSemanticTypes(semanticTypes.toArray(new SemanticType [0]));
			c.setSynonyms(synonyms.toArray(new String [0]));
			c.setSources(sources.toArray(new Source [0]));
			c.setTerms(terms.toArray(new Term [0]));
			c.setDefinitions(definitions.toArray(new Definition [0]));
			for(String code: codes.keySet())
				c.addCode(code,codes.get(code));
			c.setInitialized(true);
			
			return c;
			
		}catch(Exception ex){
			throw new TerminologyException("Error: Problem with lookup of "+cui,ex);
		}
	}

	public Concept[] search(String text) throws TerminologyException {
		return search(text,SEARCH_NGRAM);
	}
	
	public String[] getSearchMethods() {
		return new String [] {SEARCH_EXACT,SEARCH_BEST,SEARCH_STARTS_WITH,SEARCH_ENDS_WITH,SEARCH_CONTAINS,SEARCH_NGRAM};
	}

	
	/**
	 * is ngram used elsewhere
	 * @param list
	 * @param str
	 * @return
	 */
	private boolean isUsed(String text, List<String> list, String ng){
		int st = text.indexOf(ng);
		int en = st+ng.length();
		
		// go over a list of used ngrams
		for(String str: list){
			int s = text.indexOf(str);
			int e = s+str.length();
			
			// start of ngram in equestion is less then end of used ngram
			// or end o
			if(!(st > e || en < s))
				return true;
			
		}
		return false;
	}
	
	/**
	 * do concept search
	 */
	public Concept[] search(String text, String method) throws TerminologyException {
		// to do best, simple first do exact match, then contains with
		if(SEARCH_BEST.contains(method)){
			Concept [] result = search(text,SEARCH_EXACT);
			return (result.length > 0)?result: search(text,SEARCH_CONTAINS);
		}else if(SEARCH_NGRAM.contains(method)){
			// get ngrams from the text
			String [] ngrams = TextTools.getNGrams(text,4);
			// reconstuct search term
			StringBuffer b = new StringBuffer();
			for(String s: TextTools.getWords(text))
				b.append(s+" ");
			String stext = b.toString().trim();
			
			
			// iterate over ngrams, the order is assumed to be
			// from largest to smallest
			List<String> usedNgrams = new ArrayList<String>();
			List<Concept> conceptList = new ArrayList<Concept>();
			for(String ng : ngrams){
				// check if part of this ngram was used
				if(isUsed(stext,usedNgrams,ng))
					continue;
				
				// do exact search on a ngram
				Concept [] r = search(ng,SEARCH_EXACT);
				if(r.length > 0){
					Collections.addAll(conceptList,r);
					usedNgrams.add(ng);
				}
			}
			
			return conceptList.toArray(new Concept [0]);
		// else do normal search	
		}else{
			try{
				List<Concept> conceptList = new ArrayList<Concept>();
				Connection con = getConnection();
				
				// by default exact match
				String condition = " str = '"+text+"'";
				if(SEARCH_CONTAINS.equals(method)){
					condition = " str LIKE '%"+text+"%'";
				}else if(SEARCH_STARTS_WITH.equals(method)){
					condition = " str LIKE '"+text+"%'";
				}else if(SEARCH_ENDS_WITH.equals(method)){
					condition = " str LIKE '%"+text+"'";
				}else if(text.length() > 3) {
					// default case is SEARCH_EXACT_MATCH
					// exect match that is case insencitive
					String a = ""+text.charAt(0);
					String b = text.substring(1,4);
					
					// this attempts to speedup the search
					StringBuffer bf = new StringBuffer("((");
					bf.append("str LIKE '"+a.toUpperCase()+b.toLowerCase()+"%' OR ");
					bf.append("str LIKE '"+(a+b).toLowerCase()+"%' OR ");
					bf.append("str LIKE '"+(a+b).toUpperCase()+"%')");
					bf.append(" AND UPPER(str) = '"+text.toUpperCase()+"')");
					
					condition = bf.toString();
				}
				
				// filter by sources
				String filter = "";
				if(filterSources != null && filterSources.length > 0){
					StringBuffer b = new StringBuffer(" AND sab IN (");
					for(Source s: filterSources){
						b.append("'"+s.getName()+"', ");
					}
					filter = b.substring(0,b.length()-2)+")";
				}
				
				// lookup main concept info
				Statement st = con.createStatement();
				ResultSet result =  st.executeQuery("SELECT DISTINCT cui, str FROM mrconso WHERE "+condition+filter);
				while(result.next()){
					String cui  = result.getString("cui");
					String str = result.getString("str");
					
					Concept c = new Concept(cui,str);
					c.setTerminology(this);
					c.setSearchString(text);
					
					if(!conceptList.contains(c))
						conceptList.add(c);
				}
				result.close();
				st.close();
				
				
				return conceptList.toArray(new Concept [0]);
			}catch(Exception ex){
				throw new TerminologyException("Error: UMLS search failed on "+text,ex);
			}
		}
		//return new Concept [0];
	}


	public void setFilterSources(Source[] srcs) {
		filterSources = srcs;
	}

	public String getDescription() {
		return "UMLS or compatible terminology distribution deployed in Rich Release Format (RRF)";
	}

	public String getFormat() {
		return "RRF";
	}

	public String getLocation() {
		return url;
	}

	public String getName() {
		return "UMLS Terminology";
	}

	public URI getURI() {
		return URI.create(getLocation());
	}

	public String getVersion() {
		return "1.0";
	}

	/**
	 * @param args
	 */
	public static void main(String[] args) throws Exception {
		Terminology term = new UMLSTerminology("oracle.jdbc.driver.OracleDriver",
				"jdbc:oracle:thin:@lnx01.dbmi.pitt.edu:1521:dbmi01", "umls","dbmi09umls");
		
		// lookup concept
		Concept melanoma = term.lookupConcept("C0025202");
		melanoma.printInfo(System.out);
		term.setFilterSources(term.getSources("NCI"));
		System.out.println("--");
		// do search
		long time = System.currentTimeMillis();
		for(String text: new String [] {"blue tumor"}){
			System.out.println("searching for: "+text);
			for(Concept c: term.search(text)){
				System.out.println(c.getCode()+" "+c.getName());
				c.initialize();
				c.printInfo(System.out);
				System.out.println(c.getCodes());
			}
		}
		System.out.println(System.currentTimeMillis()-time);
	}

}
