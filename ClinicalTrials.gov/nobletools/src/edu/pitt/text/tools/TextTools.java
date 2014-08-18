package edu.pitt.text.tools;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.lang.reflect.Array;
import java.net.URL;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Formatter;
import java.util.HashMap;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.StringTokenizer;

import edu.pitt.terminology.util.Sender;


/**
 * This class provides several convinience methods
 * for text processing
 * @author tseytlin
 *
 */
public class TextTools {
	public static final String DEFAULT_TEXT_TOOLS_URL = "http://slidetutor.upmc.edu/term/servlet/TextToolsServlet";
	public static final int NO_VALUE = Integer.MIN_VALUE;
	private static final String separator = "\t";
	private static Map<String,String> plurals;
	private static Map<Character,String> urlEscapeCodeMap;
	private static Map<Character,String> xmlEscapeCodeMap;
	private static Map<String,String> stopWords,prepostionWords,commonWords;
	private Sender sender;
	
	//	 load values into map
	/*
	static {
		// load in all processing resources
        plurals = loadResource("/resources/PluralTable.lst");
        stopWords = loadResource("/resources/StopWords.lst");
	}
	*/
	
	/**
	 * get plural table
	 * @return
	 */
	private static Map<String,String> getPluralTable(){
		if(plurals == null)
			plurals = loadResource("/resources/PluralTable.lst");
		return plurals;
	}
	
	/**
	 * get list of stop words
	 * @return
	 */
	public static Set<String> getStopWords(){
		if(stopWords == null){
			stopWords = loadResource("/resources/StopWords.lst");
		}
		return stopWords.keySet();
	}
	
	
	/**
	 * get stop words table
	 * @return
	 */
	public static Set<String> getPrepostitionWords(){
		if(prepostionWords == null)
			prepostionWords = loadResource("/resources/PrepositionWords.lst");
		return prepostionWords.keySet();
	}
	
	/**
	 * get a list of common words
	 * @return
	 */
	public static Set<String> getCommonWords(){
		if(commonWords == null){
			commonWords = new HashMap<String, String>();
			for(String w: loadResource("/resources/CommonWords.lst").keySet()){
				commonWords.put(normalize(w),"");
			}
		}
		return commonWords.keySet();
	}
	
	
	/**
	 * Read a list with this name and put its content into a list object
	 */	
	private static Map<String,String> loadResource(String name){
		Map<String,String> list = new LinkedHashMap<String,String>();
		try{
			InputStream in = null;
			File f = new File(name);
			if(f.exists()){
				in = new FileInputStream(f);
			}else if(name.startsWith("http://")){
				in = (new URL(name)).openStream();
			}else{
				in = TextTools.class.getResourceAsStream(name);
			}
			if(in == null){
				System.err.println("ERROR: Could not load resource: "+name);
				return list;
			}	
			BufferedReader reader = new BufferedReader(new InputStreamReader(in));
			for(String line = reader.readLine();line != null;line=reader.readLine()){
				String t = line.trim();
				// skip blank lines and lines that start with #
				if(t.length() > 0 && !t.startsWith("#")){
					String [] suffixes = line.trim().split(separator);
					if(suffixes.length >= 2)
						list.put(suffixes[1].trim(),suffixes[0].trim());
					else
						list.put(suffixes[0].trim(),null);
				}
			}
			reader.close();
			in.close();
		}catch(IOException ex){
			ex.printStackTrace();
		}
		return list;
	}
	
	/**
	 * TextTools located on a server (forward to some implementation)
	 * @param remote servlet
	 */
	public TextTools(URL servlet){
		sender = new Sender(servlet);
	}
	
	/**
	 * TextTools located on a server (forward to some implementation)
	 * @param remote servlet
	 */
	public TextTools(){
		try{
			sender = new Sender(new URL(DEFAULT_TEXT_TOOLS_URL));
		}catch(Exception ex){
			ex.printStackTrace();
		}
	}
	
	
	/**
	 * Determine if word is plural
	 */
	public static boolean isPlural(String word){
		//iterate over keys
		for(Iterator i=getPluralTable().keySet().iterator();i.hasNext();){
			String pluralSuffix	= (String) i.next();
			if(word.endsWith(pluralSuffix)){	
				return true;
			}
		}
		return false;
	}
	
	/**
	 * Determine if word is a stop word
	 */
	public static boolean isStopWord(String word){
		//check table
		getStopWords();
		if(stopWords.containsKey(word.trim()))
			return true;
		return false;
	}
	
	/**
	 * Determine if word is a stop word
	 */
	public static boolean isPrepositionWord(String word){
		//check table
		getPrepostitionWords();
		if(prepostionWords.containsKey(word.trim()))
			return true;
		return false;
	}
	

	/**
	 * Determine if word is in the top 1000 common english words
	 */
	public static boolean isCommonWord(String word){
		//check table
		getCommonWords();
		if(commonWords.containsKey(normalize(word.trim())))
			return true;
		return false;
	}
	
	/**
	 * Given a word tries to extract its singular form and returns it
	 */	
	public static String convertToSingularForm(String word){
		// strip posessive
		if(word.endsWith("'s")){
			return word.substring(0,(word.length()-2));
		}
		
		//iterate over keys
		for(Iterator i=getPluralTable().keySet().iterator();i.hasNext();){
			String pluralSuffix	= (String) i.next();
			if(word.endsWith(pluralSuffix)){	
				String singularSuffix = (String) getPluralTable().get(pluralSuffix);
				int end = word.length() - pluralSuffix.length();
				return word.substring(0,end)+singularSuffix;
			}
		}
		return word;
	}
	
	/**
	 * stem input word (find root)
	 * Uses Porter stemmer algorithm
	 * @param input word 
	 * @return word root (lowercase)
	 * NOTE: this method doesn't check that input string is a single word.
	 */
	public static String stem(String word){
		if(word == null || word.length() == 0)
			return "";
		Stemmer s = new Stemmer();
		s.add(word.toLowerCase());
		s.stem();
		return s.getResultString();
	}
	
	/**
	 * split text into words.
	 * replace all non-word characters and possesives from query w/ single space
	 * tokenize words by space and add non-empty ones
	 * @param query
	 * @return
	 */
	public static String [] getWords(String query){
		// replace all non-word characters and possesives from query w/ single space
		//String text = query.replaceAll("('s\\b|\\W+|\\s+)"," ");
		List<String> list = new ArrayList<String>();
		// tokenize words by space and add non-empty ones
		StringTokenizer t = new StringTokenizer(query," -_\\/|\t\n<>()[]");
		while(t.hasMoreTokens()){
			String s =t.nextToken();
			if(s.length() > 0){
				while(s.endsWith(".") || s.endsWith(",") || s.endsWith("!") || s.endsWith("?") || s.endsWith(";") || s.endsWith(":"))
					s = s.substring(0,s.length()-1);
				list.add(s);
			}
		}
		return (String[]) list.toArray(new String[0]);
	}
	
	
	
	/**
	 * break a given text into a set of ngrams
	 * Ex: input: "quick brown fox jumped" w/ n = 3 will return
	 *  quick brown fox, brown fox jumped, quick brown, brown fox, fox jumped
	 *  quick, brown, fox, jumped
	 * @param input text
	 * @param ngram limit 
	 * @return
	 */
	public static String [] getNGrams(String text, int n){
		List<String> result = new ArrayList<String>();
		String [] words = getWords(text);
		
		// decrement by number of n in ngram
		for(int e = n; e > 0; e--){
			// w/ given ngram size, get all combinations
			for(int s = 0; s <= words.length - e; s++){ 
				// inner loop to construct the actual ngram
				StringBuffer b = new StringBuffer();
				for(int i=s;i<s+e; i++){
					b.append(words[i]+" ");
				}
				result.add(b.toString().trim());
			}
		}
		
		return result.toArray(new String [0]);
	}
	
	
	/**
	 * This method gets a text file (HTML too) from input stream 
	 * from given map
	 * @param InputStream text input
	 * @return String that was produced
	 * @throws IOException if something is wrong
	 * WARNING!!! if you use this to read HTML text and want to put it somewhere
	 * you should delete newlines
	 */
	public static String getText(InputStream in) throws IOException {
		StringBuffer strBuf = new StringBuffer();
		BufferedReader buf = new BufferedReader(new InputStreamReader(in));
		try {
			for (String line = buf.readLine(); line != null; line = buf.readLine()) {
				strBuf.append(line.trim() + "\n");
			}
		} catch (IOException ex) {
			throw ex;
		} finally {
			buf.close();
		}
		return strBuf.toString();
	}
	
	
	/**
	 * strip diacritics from the string Ex; Protégé -> Protege
	 * a faster solution, that avoids weird non-ascii chars in your code
	 * shamelessly copy/pasted from
	 * http://www.rgagnon.com/javadetails/java-0456.html
	 */
	public static String stripDiacritics(String s) {
		final String PLAIN_ASCII =
				 "AaEeIiOoUu" // grave
				+ "AaEeIiOoUuYy" // acute
				+ "AaEeIiOoUuYy" // circumflex
				+ "AaOoNn" // tilde
				+ "AaEeIiOoUuYy" // umlaut
				+ "Aa" // ring
				+ "Cc" // cedilla
				+ "OoUu"; // double acute;
		final String UNICODE = 
				"\u00C0\u00E0\u00C8\u00E8\u00CC\u00EC\u00D2\u00F2\u00D9\u00F9"
				+ "\u00C1\u00E1\u00C9\u00E9\u00CD\u00ED\u00D3\u00F3\u00DA\u00FA\u00DD\u00FD"
				+ "\u00C2\u00E2\u00CA\u00EA\u00CE\u00EE\u00D4\u00F4\u00DB\u00FB\u0176\u0177"
				+ "\u00C3\u00E3\u00D5\u00F5\u00D1\u00F1"
				+ "\u00C4\u00E4\u00CB\u00EB\u00CF\u00EF\u00D6\u00F6\u00DC\u00FC\u0178\u00FF" + "\u00C5\u00E5"
				+ "\u00C7\u00E7" + "\u0150\u0151\u0170\u0171";
		
		if (s == null)
			return null;
		
		StringBuilder sb = new StringBuilder();
		for (int i = 0; i < s.length(); i++) {
			char c = s.charAt(i);
			int pos = UNICODE.indexOf(c);
			if (pos > -1) {
				sb.append(PLAIN_ASCII.charAt(pos));
			} else {
				sb.append(c);
			}
		}
		return sb.toString();
	}
	
	/**
	 * The normalized string is a version of the original string in lower case, 
	 * without punctuation, genitive markers, or stop words, diacritics, ligatures, 
	 * with each word in it's uninflected (citation) form, the words sorted in alphabetical 
	 * order, and normalize non-ASCII Unicode characters to ASCII by mapping punctuation 
	 * and symbols to ASCII, mapping Unicode to ASCII, stripping diacritics, spliting ligatures, 
	 * and stripping non-ASCII Unicode characrters.
	 * 1. q0: map Uniocde symbols and punctuation to ASCII
   	 * 2. g: remove genitives,
   	 * 3. rs: then remove parenthetc pluralforms of (s), (es), (ies), (S), (ES), and (IES),
   	 * 4. o: then replace punctuation with spaces,
   	 * 5. t: then remove stop words,
   	 * 6. l: then lowercase,
   	 * 7. B: then uninflect each word,
   	 * 8. Ct: then get citation form for each base form,
   	 * 9. q7: then Unicode Core Norm
     *     * map Uniocde symbols and punctuation to ASCII
     *     * map Unicode to ASCII
     *     * split ligatures
     *     * strip diacritics 
     * 10. q8: then strip or map non-ASCII Unicode characters,
     * 11. w: and finally sort the words in alphabetic order. 
	 * @param original text
	 * @return normalized string
	 */
	public static String normalize(String text){
		return normalize(text,false);
	}
	
	/**
	 * The normalized string is a version of the original string in lower case, 
	 * without punctuation, genitive markers, or stop words, diacritics, ligatures, 
	 * with each word in it's uninflected (citation) form, the words sorted in alphabetical 
	 * order, and normalize non-ASCII Unicode characters to ASCII by mapping punctuation 
	 * and symbols to ASCII, mapping Unicode to ASCII, stripping diacritics, spliting ligatures, 
	 * and stripping non-ASCII Unicode characrters.
	 * 1. q0: map Uniocde symbols and punctuation to ASCII
   	 * 2. g: remove genitives,
   	 * 3. rs: then remove parenthetc pluralforms of (s), (es), (ies), (S), (ES), and (IES),
   	 * 4. o: then replace punctuation with spaces,
   	 * 5. t: then remove stop words,
   	 * 6. l: then lowercase,
   	 * 7. B: then uninflect each word,
   	 * 8. Ct: then get citation form for each base form,
   	 * 9. q7: then Unicode Core Norm
     *     * map Uniocde symbols and punctuation to ASCII
     *     * map Unicode to ASCII
     *     * split ligatures
     *     * strip diacritics 
     * 10. q8: then strip or map non-ASCII Unicode characters,
     * 11. w: and finally sort the words in alphabetic order. 
	 * @param original text
	 * @return normalized string
	 */
	public static String normalize(String text, boolean stem, boolean digits){
		return normalize(text, stem, digits,true);
	}
	
	
	/**
	 * The normalized string is a version of the original string in lower case, 
	 * without punctuation, genitive markers, or stop words, diacritics, ligatures, 
	 * with each word in it's uninflected (citation) form, the words sorted in alphabetical 
	 * order, and normalize non-ASCII Unicode characters to ASCII by mapping punctuation 
	 * and symbols to ASCII, mapping Unicode to ASCII, stripping diacritics, spliting ligatures, 
	 * and stripping non-ASCII Unicode characrters.
	 * 1. q0: map Uniocde symbols and punctuation to ASCII
   	 * 2. g: remove genitives,
   	 * 3. rs: then remove parenthetc pluralforms of (s), (es), (ies), (S), (ES), and (IES),
   	 * 4. o: then replace punctuation with spaces,
   	 * 5. t: then remove stop words,
   	 * 6. l: then lowercase,
   	 * 7. B: then uninflect each word,
   	 * 8. Ct: then get citation form for each base form,
   	 * 9. q7: then Unicode Core Norm
     *     * map Uniocde symbols and punctuation to ASCII
     *     * map Unicode to ASCII
     *     * split ligatures
     *     * strip diacritics 
     * 10. q8: then strip or map non-ASCII Unicode characters,
     * 11. w: and finally sort the words in alphabetic order. 
	 * @param original text
	 * @return normalized string
	 */
	public static String normalize(String text, boolean stem, boolean digits,boolean stopWords){
		List<String> words = normalizeWords(text, stem, digits,stopWords);
				
		// sort words alphabeticly
		Collections.sort(words);
			
		// convert words to single string
		StringBuffer buf = new StringBuffer();
		for(String s: words)
			buf.append(s+" ");
		return buf.toString().trim();
	}
	
	/**
	 * The normalized string is a version of the original string in lower case, 
	 * without punctuation, genitive markers, or stop words, diacritics, ligatures, 
	 * with each word in it's uninflected (citation) form, the words sorted in alphabetical 
	 * order, and normalize non-ASCII Unicode characters to ASCII by mapping punctuation 
	 * and symbols to ASCII, mapping Unicode to ASCII, stripping diacritics, spliting ligatures, 
	 * and stripping non-ASCII Unicode characrters.
	 * 1. q0: map Uniocde symbols and punctuation to ASCII
   	 * 2. g: remove genitives,
   	 * 3. rs: then remove parenthetc pluralforms of (s), (es), (ies), (S), (ES), and (IES),
   	 * 4. o: then replace punctuation with spaces,
   	 * 5. t: then remove stop words,
   	 * 6. l: then lowercase,
   	 * 7. B: then uninflect each word,
   	 * 8. Ct: then get citation form for each base form,
   	 * 9. q7: then Unicode Core Norm
     *     * map Uniocde symbols and punctuation to ASCII
     *     * map Unicode to ASCII
     *     * split ligatures
     *     * strip diacritics 
     * 10. q8: then strip or map non-ASCII Unicode characters,
     * 11. w: and finally sort the words in alphabetic order. 
	 * @param original text
	 * @return normalized string
	 */
	public static String normalize(String text, boolean stem){
		return normalize(text,stem,true);
	}
	
	
	/**
	 * perform normalization of a string @see normalize, but return unsorted list of words 
	 * @param text
	 * @param stem
	 * @return
	 */
	public static List<String> normalizeWords(String text, boolean stem){
		return normalizeWords(text, stem,true);
	}
	
	
	/**
	 * perform normalization of a string @see normalize, but return unsorted list of words 
	 * @param text
	 * @param stem -stem words
	 * @param strip - strip digits
	 * @return
	 */
	public static List<String> normalizeWords(String text, boolean stem, boolean stripDigits){
		return normalizeWords(text, stem, stripDigits,true);
	}
	
	/**
	 * perform normalization of a string @see normalize, but return unsorted list of words 
	 * @param text
	 * @param stem -stem words
	 * @param strip - strip digits
	 * @return
	 */
	public static List<String> normalizeWords(String text, boolean stem, boolean stripDigits, boolean stripStopWords){
		text = text.trim();
		
		// map to ascii (unicode nomralization)
		text = stripDiacritics(text);
		
		// then lowercase,
		text = text.toLowerCase();
		
		// remove genetives ('s and s')
		text = text.replaceAll("\\b([a-z]+)'s?","$1");
		
		//then remove parenthetc pluralforms of (s), (es), (ies), (S), (ES), and (IES),
		text = text.replaceAll("\\(i?e?s\\)","");
		
		// then replace punctuation with spaces, (and other non word characters)
		//text = text.replaceAll(" ?\\W ?"," ");
		
		// replace punctuations, yet preserve period in float numbers and a dash, since there are
		// useful concepts that have a dash in them Ex: in-situ
		//text = text.replaceAll("\\s?[^\\w\\.]\\s?"," ").replaceAll("([a-zA-Z ])\\.([a-zA-Z ])","$1 $2");
		
		// have only single space between words
		//text = text.replaceAll("\\s+"," ");
		
		// find floating digits and replace . with _
		text = text.replaceAll("(\\d+)\\.(\\d+)","$1_$2").replaceAll("\\.(\\d+)","_$1");
		
		// then replace punctuation with spaces, (and other non word characters)
		text = text.replaceAll("\\s*\\W\\s*"," ");
		
		// now replace all inserted _ back with periods under same conditions as before
		text = text.replaceAll("(\\d+)_(\\d+)","$1.$2").replaceAll("_(\\d+)",".$1");
						
		// split into words
		String [] swords = text.split("\\s+");
		List<String> words = new ArrayList<String>(Arrays.asList(swords));
		
		// then remove stop words and numbers
		if(stripStopWords){
			for(int i=0;i<swords.length;i++){
				if(isStopWord(swords[i]) || (stripDigits && swords[i].matches("\\d+")))
					words.remove(swords[i]);
			}
		}
		
		//and stem other words
		if(stem){
			for(int i=0;i<words.size();i++){
				words.set(i,stem(words.get(i)));
			}
		}
		return words;
	}
	
	/**
	 * represents a tuple of hashtable and list
	 *
	public static class NormalizedWordsContainer {
		public Map<String,String> normalizedWordsMap;
		public List<String> normalizedWordsList;
		
	}
	*/
	
	/**
	 * perform normalization of a string @see normalize, but return unsorted list of words 
	 * @param text
	 * @param stem -stem words
	 * @param strip - strip digits
	 * @return Map<String,String> normalized word for its original form
	 *
	public static NormalizedWordsContainer getNormalizedWordMap(String text, boolean stem, boolean stripDigits, boolean stripStopWords){
		NormalizedWordsContainer c = new NormalizedWordsContainer();
		c.normalizedWordsMap = new LinkedHashMap<String, String>();
		c.normalizedWordsList = new ArrayList<String>();
		for(String w: getWords(text)){
			List<String> ws = normalizeWords(w, stem, stripDigits);
			if(!ws.isEmpty() && !c.normalizedWordsMap.containsKey(ws.get(0)))
				c.normalizedWordsMap.put(ws.get(0),w);
			c.normalizedWordsList.addAll(ws);
		}
		return c;
	}
	*/
	
	
	/**
     * Compute Levenshtein (edit) distance
     * copy/paste from http://www.merriampark.com/ld.htm
	 *
	public static int distance (String s, String t) {
		int d[][]; // matrix
		int n; // length of s
		int m; // length of t
		int i; // iterates through s
		int j; // iterates through t
		char s_i; // ith character of s
		char t_j; // jth character of t
		int cost; // cost

	    // Step 1
	    n = s.length();
	    m = t.length();
	    if (n == 0){
	      return m;
	    }
	    if (m == 0) {
	      return n;
	    }
	    
	    d = new int[n+1][m+1];

	    // Step 2
	    for (i = 0; i <= n; i++) {
	    	d[i][0] = i;
	    }

	    for (j = 0; j <= m; j++) {
	    	d[0][j] = j;
	    }

	    // Step 3
	    for (i = 1; i <= n; i++) {
	    	s_i = s.charAt (i - 1);

	    	// Step 4
	    	for (j = 1; j <= m; j++) {
	    		t_j = t.charAt (j - 1);

		        // Step 5
		        if (s_i == t_j) {
		          cost = 0;
		        }
		        else {
		          cost = 1;
		        }

		        // Step 6
		        d[i][j] = Math.min(Math.min(d[i-1][j]+1, d[i][j-1]+1),d[i-1][j-1] + cost);

	      }
	    }
	    // Step 7
	    return d[n][m];
	}
	*/


	/**
	 * compute levenshtein (edit) distance between two strings
	 * http://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#Java
	 * @param str1
	 * @param str2
	 * @return
	 */
	public static int getLevenshteinDistance(CharSequence str1, CharSequence str2) {
		int[][] distance = new int[str1.length() + 1][str2.length() + 1];

		for (int i = 0; i <= str1.length(); i++)
			distance[i][0] = i;
		for (int j = 0; j <= str2.length(); j++)
			distance[0][j] = j;

		for (int i = 1; i <= str1.length(); i++)
			for (int j = 1; j <= str2.length(); j++)
				distance[i][j] = Math.min(Math.min(distance[i - 1][j] + 1, distance[i][j - 1] + 1),
						distance[i - 1][j - 1] + ((str1.charAt(i - 1) == str2.charAt(j - 1)) ? 0 : 1));

		return distance[str1.length()][str2.length()];
	}

	
	/**
	 * compute fuzzy equals /similarity (minimal levenshtein (edit) distance
	 * this class tries to detect similarity by computing edit distance, but 
	 * only as the last resourt. First it checks for nulls, string lengths,
	 * regular equals, makes sure that the first letters of each word are the
	 * same. Only then it attempts to compute the distance and compares it to 
	 * a threshold that is relative to string size
	 * @param s1
	 * @param s2
	 * @return
	 */
	public static boolean similar(String s1, String s2){
		// check for null
		if(s1 == null && s2 == null)
			return true;
		if(s1 == null || s2 == null)
			return false;
		
		// check sizes (no point to compare if size difference is huge)
		if(Math.abs(s1.length() - s2.length()) > 3)
			return false;
		
		// do normal equals first
		if(s1.equalsIgnoreCase(s2))
			return true;
		
		
		// don't do this for really small words
		if(s1.length() <= 4 || s2.length() <= 4)
			return false;
		
		
		// now break into words
		String [] w1 = s1.split("[\\s_]");
		String [] w2 = s2.split("[\\s_]");
		
		// if number of words is different, then false
		if(w1.length != w2.length)
			return false;
		
		// check first letters of each word
		for(int i=0;i<w1.length;i++){
			// if first letters don't match then not similar enough
			if(w1[i].charAt(0) != w2[i].charAt(0))
				return false;
		}
		
		// figure out the minimum edit distance
		int n = (s1.length() < 7)?1:(s1.length() >= 20)?3:2; 
		
		// now comput levenshtein distances
		return getLevenshteinDistance(s1.toLowerCase(),s2.toLowerCase()) <= n;
	}
	
	
	public static Map<Character,String> getURLEscapeCode(){
		if(urlEscapeCodeMap == null){
			urlEscapeCodeMap = new HashMap<Character, String>();
			urlEscapeCodeMap.put(' ',"%20");
			urlEscapeCodeMap.put('<',"%3C");
			urlEscapeCodeMap.put('>',"%3E");
			urlEscapeCodeMap.put('#',"%23");
			urlEscapeCodeMap.put('%',"%25");
			urlEscapeCodeMap.put('{',"%7B");
			urlEscapeCodeMap.put('}',"%7D");
			urlEscapeCodeMap.put('|',"%7C");
			urlEscapeCodeMap.put('\\',"%5C");
			urlEscapeCodeMap.put('^',"%5E");
			urlEscapeCodeMap.put('~',"%7E");
			urlEscapeCodeMap.put('[',"%5B");
			urlEscapeCodeMap.put(']',"%5D");
			urlEscapeCodeMap.put('`',"%60");
			urlEscapeCodeMap.put(';',"%3B");
			urlEscapeCodeMap.put('/',"%2F");
			urlEscapeCodeMap.put('?',"%3F");
			urlEscapeCodeMap.put(':',"%3A");
			urlEscapeCodeMap.put('@',"%40");
			urlEscapeCodeMap.put('=',"%3D");
			urlEscapeCodeMap.put('&',"%26");
			urlEscapeCodeMap.put('$',"%24");
		}
		return urlEscapeCodeMap;
	}
	
	public static Map<Character,String> getHTMLEscapeCode(){
		if(xmlEscapeCodeMap == null){
			xmlEscapeCodeMap = new HashMap<Character, String>();
			xmlEscapeCodeMap.put('"',"&quot;");
			xmlEscapeCodeMap.put('\'',"&apos;");
			xmlEscapeCodeMap.put('<',"&lt;");
			xmlEscapeCodeMap.put('>',"&gt;");
			xmlEscapeCodeMap.put('&'," &amp;");
		}
		return xmlEscapeCodeMap;
	}
	
	/**
	 * URL escape filter
	 * @param s
	 * @return
	 */
	public static String escapeURL(String s){
		StringBuffer str = new StringBuffer();
		Map<Character,String> m = getURLEscapeCode();
		for(char x: s.toCharArray()){
			if(m.containsKey(x))
				str.append(m.get(x));
			else
				str.append(x);
		}
		return str.toString();
	}
	
	/**
	 * URL escape filter
	 * @param s
	 * @return
	 */
	public static String escapeHTML(String s){
		StringBuffer str = new StringBuffer();
		Map<Character,String> m = getHTMLEscapeCode();
		for(char x: s.toCharArray()){
			if(m.containsKey(x))
				str.append(m.get(x));
			else
				str.append(x);
		}
		return str.toString();
	}
	
	/**
	 * add a value to an array and return a new array
	 * @param old array
	 * @param val value to add
	 * @return concatanated arrays
	 */
	public static <T> T[] addAll(T[] a, T b){
		Class cls = null;
		if(a.length > 0)
			cls = a[0].getClass();
		else if(b != null)
			cls = b.getClass();
		else
			cls = Object.class;
		T[] c = (T []) Array.newInstance(cls,a.length+1);
		System.arraycopy(a, 0, c, 0,a.length);
		c[c.length-1] = b;
		return c;
	}
	
	/**
	 * add a value to an array and return a new array
	 * @param old array
	 * @param val value to add
	 * @return concatanated arrays
	 */
	public static <T> T[] addAll(T[] a, T[] b){
		Class cls = null;
		if(a.length > 0)
			cls = a[0].getClass();
		else if(b.length > 0)
			cls = b[0].getClass();
		else
			cls = Object.class;
		T[] c = (T []) Array.newInstance(cls,a.length+b.length);
		System.arraycopy(a, 0, c, 0,a.length);
		System.arraycopy(b, 0, c, a.length, b.length);
		return c;
	}
	
	/**
	 * get character count for a given string
	 * @param text
	 * @param test
	 * @return
	 */
	public static int charCount(String text, char test ){
		int count = 0;
		for(char x: text.toCharArray()){
			if(x == test)
				count++;
		}
		return count;
	}
	
	
	/**
	 * for each character in the target strings sets case in the source string
	 * @param source - string to change case
	 * @param target - example string to take character case info from
	 * @return result string that has case that resembles target string
	 * NOTE: if target string is shorter then source string, then the remainder of
	 * the source string will use the case of the last character of the target string
	 */
	public static String copyCharacterCase(String source, String target){
		StringBuffer str = new StringBuffer();
		char [] s = source.toCharArray();
		char [] t = target.toCharArray();
		int i=0;
		boolean toUpper = false,toLower = false;
		// copy case
		for(i=0;i<s.length && i<t.length;i++){
			toUpper = Character.isUpperCase(s[i]);
			toLower = Character.isLowerCase(s[i]);
			String tt = ""+t[i];
			str.append((toUpper)?tt.toUpperCase():(toLower)?tt.toLowerCase():tt);
		}
		// finish the string
		for(int j=i;j<t.length;j++){
			String tt = ""+t[j];
			str.append((toUpper)?tt.toUpperCase():(toLower)?tt.toLowerCase():tt);
		}
		
		return str.toString();
	}
	
	
	/**
	 * This function attempts to convert vaires types of input into numerical
	 * equivalent
	 */
	public static double parseDecimalValue(String text) {
		double value = 0;
		if(text == null)
			return value;
		
		// check if this is a float
		if (text.matches("\\d+\\.\\d+")) {
			// try to parse regular number
			try {
				value = Double.parseDouble(text);
			} catch (Exception ex) {
				ex.printStackTrace();
			}
		} else {
			value = parseIntegerValue(text);
		}
		return value;
	}

	/**
	 * This function attempts to convert vaires types of input into numerical
	 * equivalent
	 */
	public static int parseIntegerValue(String text) {
		int value = 0;

		// try to parse roman numerals
		if (text.matches("[IiVvXx]+")) {
			boolean oneLess = false;
			for (int i = 0; i < text.length(); i++) {
				switch (text.charAt(i)) {
				case 'i':
				case 'I':
					value++;
					oneLess = true;
					break;
				case 'v':
				case 'V':
					value += ((oneLess) ? 3 : 5);
					oneLess = false;
					break;
				case 'x':
				case 'X':
					value += ((oneLess) ? 8 : 10);
					oneLess = false;
					break;
				}
			}

			return value;
		}
		// try to parse words
		if (text.matches("[a-zA-Z]+")) {
			if (text.equalsIgnoreCase("zero"))
				value = 0;
			else if (text.equalsIgnoreCase("one"))
				value = 1;
			else if (text.equalsIgnoreCase("two"))
				value = 2;
			else if (text.equalsIgnoreCase("three"))
				value = 3;
			else if (text.equalsIgnoreCase("four"))
				value = 4;
			else if (text.equalsIgnoreCase("five"))
				value = 5;
			else if (text.equalsIgnoreCase("six"))
				value = 6;
			else if (text.equalsIgnoreCase("seven"))
				value = 7;
			else if (text.equalsIgnoreCase("eight"))
				value = 8;
			else if (text.equalsIgnoreCase("nine"))
				value = 9;
			else if (text.equalsIgnoreCase("ten"))
				value = 10;
			else if (text.equalsIgnoreCase("eleven"))
				value = 11;
			else if (text.equalsIgnoreCase("twelve"))
				value = 12;
			else
				value = (int) NO_VALUE;

			return value;
		}

		// try to parse regular number
		try {
			value = Integer.parseInt(text);
		} catch (NumberFormatException ex) {
			// ex.printStackTrace();
			return (int) NO_VALUE;
		}
		return value;
	}
	


	/**
	 * is string a number
	 * 
	 * @param text
	 * @return
	 */
	public static boolean isNumber(String text) {
		return text.matches("\\d+(\\.\\d+)?");
	}

	/**
	 * pretty print number as integer or 2 precision float format numeric value
	 * as string
	 * 
	 * @return
	 */
	public static String toString(double numericValue) {
		Formatter f = new Formatter();
		if ((numericValue * 10) % 10 == 0)
			f.format("%d", (int) numericValue);
		else
			f.format("%.2f", numericValue);
		return "" + f.out();
	}

	/**
	 * get a string with each word being capitalized
	 * @param text
	 * @return
	 */
	public static String getCapitalizedWords(String text){
		StringBuffer b = new StringBuffer();
		for(String s: text.split("[\\s_]+")){
			if(s.length() > 2)
				b.append(Character.toUpperCase(s.charAt(0))+s.substring(1).toLowerCase()+" ");
			else
				b.append(s.toLowerCase()+" ");
		}
		return b.toString().trim();
	}
	
	
	/**
	 * parse CSV line (take care of double quotes)
	 * @param line
	 * @param delimeter
	 * @return
	 */
	public static List<String> parseCSVline(String line){
		return parseCSVline(line, ',');
	}
	
	/**
	 * parse CSV line (take care of double quotes)
	 * @param line
	 * @param delimeter
	 * @return
	 */
	public static List<String> parseCSVline(String line,char delim){
		List<String> fields = new ArrayList<String>();
		boolean inquotes = false;
		int st = 0;
		for(int i = 0;i<line.length();i++){
			// start/end quotes
			if(line.charAt(i) == '"'){
				inquotes ^= true;
			}
			// found delimeter (use it)
			if(!inquotes && line.charAt(i) == delim){
				String s = line.substring(st,i).trim();
				if(s.startsWith("\"") && s.endsWith("\""))
					s = s.substring(1,s.length()-1);
				fields.add(s.trim());
				st = i+1;
			}
		}
		// handle last field
		if(st < line.length()){
			String s = line.substring(st).trim();
			if(s.startsWith("\"") && s.endsWith("\""))
				s = s.substring(1,s.length()-1);
			fields.add(s.trim());
		}
		return fields;
	}
	
	
	/**
	 * Parse English sentences from a blurb of text. 
	 * Each sentence should be terminated by .! or ?
	 * Periods in digits and some acronyms should be skipped
	 * @param txt
	 * @return
	 */
	public static List<String> getSentences(String txt) {
		List<String> sentences =new ArrayList<String>();
		char [] tc = txt.toCharArray();
		int st = 0;
		for(int i=0;i<txt.length();i++){
			if(tc[i] == '.' || tc[i] == '!' || tc[i] == '?'){
				// get candidate sentence
				String s = txt.substring(st,i+1);
				
				// check if this period is a decimal point
				if(i+1 < tc.length && Character.isDigit(tc[i+1]))
					continue;
				
				// check if this period is some known abreviation
				if(s.matches(".* (vs)\\.") || s.matches(".* ([A-Z])\\.") || s.matches(".* (al)\\."))
					continue;
				
				// save sentence
				sentences.add(s);	
				
				// move start 
				st = i+1;
			}
		}
		// mop up in case you don't have a period at the end
		if(st<tc.length){
			sentences.add(txt.substring(st)+".");
		}
		
		return sentences;
	}
	
	/**
	 * determine if input line is a recognizable report section?
	 * @param line
	 * @return
	 */
	public static boolean isReportSection(String line){
		return line.matches("^\\[[A-Za-z \\-]*\\]$") || line.matches("^[A-Z \\-]*:$");
	}
	
	
	public static void main(String [] s) throws Exception{
		/*String s1 = "THIS is CLARK's LEVEL and LOTS of NEVI and maybe some MELANOMA, INVASIVE and IN-SITU, MELANOMA";
		long t3 = System.currentTimeMillis();
		List<String> words = normalizeWords(s1+" hello,world",true);
		t3 = System.currentTimeMillis()-t3;
		System.out.println(t3+" "+words);
		
		long time = System.currentTimeMillis();
		words = normalizeWords(s1,true);
		time = System.currentTimeMillis()-time;
		System.out.println(time+" "+words);
		long t2 = System.currentTimeMillis();
		NormalizedWordsContainer wordMap = getNormalizedWordMap(s1,true,true,true);
		t2 = System.currentTimeMillis()-t2;
		System.out.println(t2+" "+wordMap.normalizedWordsMap+"\n"+wordMap.normalizedWordsList);*/
		
		/*
		String str = "onè, Clark's Level";
		System.out.println(str+"-"+normalize(str));
		
		String a = "lympocytes";
		String b = "lymphocytic";
		System.out.println(distance(a,b)+", "+distance("ab","ab")+","+distance("bc","cb"));
		*/
		//TextTools tools = new TextTools(new URL("http://1upmc-opi-xip02:92/term/servlet/TextToolsServlet"));
		/*
		TextTools tools = new TextTools(new URL("http://slidetutor.upmc.edu/term/servlet/TextToolsServlet"));
		String str = "quick brown fox jumped on the lazy dog";
		long time = System.currentTimeMillis();
		Sentence sent = tools.parseSentence(str);
		System.out.println(sent.getTrimmedString()+" "+(System.currentTimeMillis()-time));
		
		for(Object l: sent.getLexicalElements()){
			LexicalElement le = (LexicalElement) l;
			System.out.println(le.getOriginalString()+" "+le.getPOSTagString());
		}
		time = System.currentTimeMillis();
		//sent = tools.tagSentence(sent);
		System.out.println("POS tagging "+(System.currentTimeMillis()-time));
		for(Object p: sent.getPhrases()){
		
			for(Object l: ((Phrase)p).getLexicalElements()){
				LexicalElement le = (LexicalElement) l;
				System.out.println(le.getOriginalString()+" "+le.getPOSTagString());
			}
		}
		*/
		/*
		String [] examples = new String [] {"neutrophils", "neutrophilic inflammatory infiltrate","lymphocytes", 
				"lymphocytic inflammatory infiltrate","isolated lymphocytes", "plasma cells","plasma cell inflammatory infiltrate"};
		//String [] examples = new String [] {"neutrophils", "neutrophilic","lymphocytes", 
		//		"lymphocytic","plasma cells","plasma cell"};
		
		for(String text: examples){
			System.out.println(text+"\n---");
			for(String word: getWords(text))
				System.out.println("\t"+stem(word));
		}
		*/
		/*
		System.out.println(getLevenshteinDistance("cytological atypia","cytologic atypia"));
		
		System.out.println(Arrays.toString(getNGrams("quick brown fox jumped over the lazy dog",4)));
		System.out.println(Arrays.toString(getNGrams("the lazy dog",4)));
		*/
		//System.out.println(copyCharacterCase("Hp", "fuckoff"));
		//System.out.println(copyCharacterCase("help", "fuckoff"));
	}
}
