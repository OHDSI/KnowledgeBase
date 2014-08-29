package edu.pitt.ontology.bioportal;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.MalformedURLException;
import java.net.SocketTimeoutException;
import java.net.URL;
import java.net.URLConnection;
import java.sql.Timestamp;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Properties;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.parsers.SAXParserFactory;

import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.xml.sax.InputSource;
import org.xml.sax.SAXException;
import org.xml.sax.SAXNotRecognizedException;
import org.xml.sax.SAXNotSupportedException;
import org.xml.sax.XMLReader;
import org.xml.sax.helpers.DefaultHandler;

/**
 * varies helper methods
 * 
 * @author tseytlin
 * 
 */
public class BioPortalHelper {
	public static final String BIOPORTAL_URL = "http://bioportal.bioontology.org/ontologies/";
	public static final String ONTOLOGIES = "/ontologies/";
	public static final String GET_VERSIONS = "versions/";
	public static final String CONCEPTS = "/concepts/";
	public static final String ROOT = "/root";
	public static final String ALL = "/all";
	public static final String SEARCH = "search/";
	public static final String EMAIL = "email=example@example.org";
	public static final int MAX_READ_ATTEMPTS = 100 ;
	public static final long RECOVERY_TIME_IN_MILLISECONDS = 30000 ; // 30 second intervals
	public static final Properties RELATIONSHIPS = new Properties();
	public static final int MAX_SEARCH_HITS = 10;
	public static final String ONTOLOGY_LOAD_EVENT = "Loading Ontology";
	
	// special ontology properties
	public static final String SUB_CLASS = "SubClass";
	public static final String SUPER_CLASS = "SuperClass";
	public static final String PART_OF = "isPartOf";
	public static final String HAS_PART = "hasPart";
	public static final String TYPE = "Type";
	public static final String DISJOINT_CLASS = "DisjointClass";
	public static final String EQUIVALENT_CLASS = "EquivalentClass";
	public static final String INSTANCES = "Instances";
	public static final String PROPERTIES = "Properties";
	
	public static final String CHILD_COUNT = "ChildCount";
	public static final String INSTANCE_COUNT = "InstanceCount";
	public static final String NAME      = "name";
	
	public static final String TYPE_CLASS = "Class";
	public static final String TYPE_PROPERTY = "Property";
	public static final String TYPE_INSTANCE = "Instance";
	
	// ontology relation maps
	public static final String LABELS     = "Labels";
	public static final String COMMENTS   = "Comments";
	public static final String CODE       = "code";
	public static final String SEMANTIC_TYPE  = "SemanticType";
	public static final String VERSIONS = "Versions";
	
	// search
	public static final String ONTOLOGYIDS = "/?ontologyids=";
	public static final String PREF_METHOD = "&is";
	public static final String EXACT_MATCH  = "exactmatch";
	public static final String CONTAINS_MATCH  = "containsmatch";
	public static final String PROPERTIES_MATCH  = "propertiesmatch";
	public static final String CONTAINS  = "contains";

	public static final String [] RESERVED_PROPERTIES = 
		new String [] { SUB_CLASS, SUPER_CLASS, DISJOINT_CLASS, EQUIVALENT_CLASS, INSTANCES, INSTANCE_COUNT, CHILD_COUNT,
						LABELS,COMMENTS,VERSIONS,"uri",NAME,TYPE,PROPERTIES,"label","type"};
	
	
	// set default relationship map
	static {
		RELATIONSHIPS.put("hassubclass",SUB_CLASS);
		RELATIONSHIPS.put("hassubtype",SUB_CLASS);
		RELATIONSHIPS.put("has_subtype",SUB_CLASS);
		RELATIONSHIPS.put("subclass",SUB_CLASS);
		RELATIONSHIPS.put(":direct-subclasses",SUB_CLASS);
		RELATIONSHIPS.put("[r]is_a",SUB_CLASS);
		
		RELATIONSHIPS.put("rdfs:subclassof",SUPER_CLASS);
		RELATIONSHIPS.put("superclass",SUPER_CLASS);
		RELATIONSHIPS.put(":direct-superclasses",SUPER_CLASS);
		RELATIONSHIPS.put("is_a",SUPER_CLASS);
		RELATIONSHIPS.put("rb",SUPER_CLASS);
		
		RELATIONSHIPS.put("[r]part_of",HAS_PART);
		RELATIONSHIPS.put("part_of",PART_OF);
		
		RELATIONSHIPS.put("owl:equivalentclass",EQUIVALENT_CLASS);
		RELATIONSHIPS.put("equivalentclass",EQUIVALENT_CLASS);
		RELATIONSHIPS.put("disjointwith",DISJOINT_CLASS);
		RELATIONSHIPS.put("disjoint_from",DISJOINT_CLASS);
		RELATIONSHIPS.put("owl:disjointwith",DISJOINT_CLASS);
		
		RELATIONSHIPS.put("type",TYPE);
		RELATIONSHIPS.put("rdf:type",TYPE);
		RELATIONSHIPS.put("rdftype",TYPE);
		RELATIONSHIPS.put(":direct-type",TYPE);
		
		RELATIONSHIPS.put("label",LABELS);
		RELATIONSHIPS.put("labels",LABELS);
		RELATIONSHIPS.put("rdfs:label",LABELS);
		RELATIONSHIPS.put("synonym",LABELS);
		RELATIONSHIPS.put("synonym_of",LABELS);
		RELATIONSHIPS.put("synonym_name",LABELS);
		RELATIONSHIPS.put("synonyms",LABELS);
		RELATIONSHIPS.put("related synonym",LABELS);
		RELATIONSHIPS.put("full_syn",LABELS);
		RELATIONSHIPS.put("bp_synonym",LABELS);
		RELATIONSHIPS.put("sy",LABELS);
		RELATIONSHIPS.put("textualpresentation",LABELS);
		RELATIONSHIPS.put("preferred_name",LABELS);
		
		RELATIONSHIPS.put("definition",COMMENTS);
		RELATIONSHIPS.put("alt_definition",COMMENTS);
		RELATIONSHIPS.put("description",COMMENTS);
		RELATIONSHIPS.put("rdfs:comment",COMMENTS);
		RELATIONSHIPS.put("comments",COMMENTS);
		
		RELATIONSHIPS.put("code",CODE);
		RELATIONSHIPS.put("id",CODE);
		RELATIONSHIPS.put("umls_cui",CODE);
		RELATIONSHIPS.put("nci_meta_cui",CODE);
		
		RELATIONSHIPS.put("semantic_type",SEMANTIC_TYPE);
	}
	
	
	/**
	 * is reserved property
	 * @param key
	 * @return
	 */
	public static boolean isReservedProperty(Object key){
		for(String s: RESERVED_PROPERTIES){
			if(s.equals(key)){
				return true;
			}
		}
		return false;
	}
	
	
	
	/**
	 * fetch all ontologies from URL
	 */
	public static void processRequest(String url, DefaultHandler handler){
		// fix url
		// TODO: do full URL sanity replacement
		url = url.replaceAll(" ","%20");
		
		// start reading in the list of ontologies
		InputStream is = null ;
		XMLReader parser = null;
		
		try {
			parser = SAXParserFactory.newInstance().newSAXParser().getXMLReader();
		} catch (SAXException e1) {
			e1.printStackTrace();
		} catch (ParserConfigurationException e1) {
			e1.printStackTrace();
		}

		boolean isReading = true;
		int readAttempt = 0;
		while (isReading && readAttempt < BioPortalHelper.MAX_READ_ATTEMPTS) {
			try {
				parser.setFeature("http://xml.org/sax/features/validation",	false);
				parser.setContentHandler(handler);
				parser.setErrorHandler(handler);
				is = getInputStream(url);
				InputSource input = new InputSource(is);
				input.setEncoding("ISO-8859-1");
				parser.parse(input);
				isReading = false ;
			} catch (SAXNotRecognizedException e) {
				BioPortalHelper.warn("SAXNotRecognizedException " + url+ "]\n" + e.getMessage());
				readAttempt++;
			} catch (SAXNotSupportedException e) {
				BioPortalHelper.warn("SAXNotSupportedException [" + url+ "]\n" + e.getMessage());
				readAttempt++;
			} catch (IOException e) {
				BioPortalHelper.warn("IOException [" + url + "]\n"+ e.getMessage());
				readAttempt++;
				e.printStackTrace();
			} catch (SAXException e) {
				BioPortalHelper.warn("SAXException [" + url + "]\n"+ e.getMessage());
				readAttempt++;
			} finally {
				if(is != null){
					try{
						is.close();
					}catch(Exception ex){}
				}
			}
			if (isReading) {
				try {
					BioPortalHelper.warn("Try again in " + readAttempt * BioPortalHelper.RECOVERY_TIME_IN_MILLISECONDS + " ms") ;
					Thread.sleep(readAttempt * BioPortalHelper.RECOVERY_TIME_IN_MILLISECONDS) ;
				} catch (InterruptedException e) {
					e.printStackTrace();
					break ;
				}
			}
			
		}
	}

	/**
	 * extract name from URI
	 * @param name
	 * @return
	 */
	public static String getName(String name){
		// if we got a uri as a code
		int i = name.lastIndexOf("#");
		if(i > -1)
			name = name.substring(i+1);
		return name;
	}
	
	/**
	 * get input stream from URL
	 * @param urlAsString
	 * @return
	 */
	public static InputStream getInputStream(String u) throws MalformedURLException, IOException {
		URL url = new URL(u);
		// 3 attempts to establish connection
		for(int i=0;i<3;i++){
			try{
				URLConnection con = url.openConnection();
				con.setConnectTimeout(3000);
				con.setDoOutput(true);
				con.setUseCaches(false);
				return con.getInputStream();
			}catch(SocketTimeoutException ex){
				System.err.println("timed out");
			}
		}
		return null;
	}

	/**
	 * parse integer value
	 * @param longAsString
	 * @return
	 */
	public static Long parseLong(String longAsString) {
		Long result = null;
		longAsString = longAsString.replaceAll("^\\s*", "").replaceAll("\\s*$","");
		long longValue = Long.parseLong(longAsString);
		result = new Long(longValue);
		return result;
	}

	/**
	 * parse timestamp
	 * @param timeStampString
	 * @return
	 */
	public static Timestamp parseTimeStamp(String timeStampString) {
		Timestamp result = null;
		try {
			SimpleDateFormat format = new SimpleDateFormat(
					"yyyy-MM-dd HH:mm:ss.S");
			Date parsed = format.parse(timeStampString);
			result = new Timestamp(parsed.getTime());
		} catch (ParseException pe) {
			System.out.println("ERROR: Cannot parse \"" + timeStampString
					+ "\"");
		} catch (Exception x) {
			x.printStackTrace();
		}
		return result;
	}

	
	/**
	 * get string from input stream
	 * @param is
	 * @param charEncoding
	 * @return
	 */
	public static String getString(final InputStream is, final String charEncoding) {
		try {
			final ByteArrayOutputStream out = new ByteArrayOutputStream();
			final byte ba[] = new byte[8192];
			int read = is.read(ba);
			while (read > -1) {
				out.write(ba, 0, read);
				read = is.read(ba);
			}
			return out.toString(charEncoding);
		} catch (final Exception e) {
			e.printStackTrace();
			return null;
		} finally {
			try {
				if (is != null) {
					is.close();
				}
			} catch (final Exception e) {
				e.printStackTrace();
			}
		}
	}

	/**
	 * generate tabs
	 * @param level
	 * @return
	 */
	public static String generateTabsOfLength(int level) {
		StringBuffer sb = new StringBuffer();
		for (int idx = 0; idx < level; idx++) {
			sb.append("\t");
		}
		return sb.toString();
	}
	
	/**
	 * create ontology friendly class name
	 * @param name
	 * @return
	 */
	public static String deriveName(String name){
		return name.replaceAll("\\s*\\(.+\\)\\s*","").replaceAll("\\W","_").replaceAll("_+","_");
	}
	
	
	
	/**
	 * print out a warning
	 * @param str
	 */
	public static void warn(String str){
		System.err.println(str);
	}
	
	/**
	 * print out a fatal error message
	 * @param str
	 */
	public static void fatal(String str){
		System.err.println("ERROR: "+str);
	}
	
	
	/**
	 * open stream from URL
	 * @param url
	 * @return null if invalid url
	 */
	public static InputStream openURL(String url){
		try{
			return new URL(filterURL(url)).openStream();
		}catch(Exception ex){
			//COULD NOT OPEN
		}
		return null;
	}
	
	/**
	 * replace some things to make URLs that work
	 * @param url
	 * @return
	 */
	public static String filterURL(String url){
		String h = "http://";
		// remove header
		if(url.startsWith(h))
			url = url.substring(h.length());
		// replace spaces and double slashes
		return h+url.replaceAll("/{2,}","/").replaceAll("\\s","%20");
	}
	
	/**
	 * parse XML document
	 * @param in
	 * @return
	 * @throws IOException
	 */
	public static Document parseXML(InputStream in) {
		if(in == null)
			return null;
		
		Document document = null;
		DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
		//factory.setValidating(true);
		//factory.setNamespaceAware(true);

		try {
			DocumentBuilder builder = factory.newDocumentBuilder();
			//builder.setErrorHandler(new XmlErrorHandler());
			//builder.setEntityResolver(new XmlEntityResolver());
			document = builder.parse(in);
			
			// close input stream
			in.close();
		}catch(Exception ex){
			//throw new IOException(ex.getMessage());
			return null;
		}
		return document;
	}
	
	/**
	 * get single element by tag name
	 * @param element
	 * @param tag
	 * @return
	 */
	public static Element getElementByTagName(Element element, String tag){
		NodeList list = element.getElementsByTagName(tag);
		for(int i=0;i<list.getLength();i++){
			Node node = list.item(i);
			if(node instanceof Element){
				return (Element) node;
			}
		}
		return null;
	}
	
	/**
	 * get single element by tag name
	 * @param element
	 * @param tag
	 * @return
	 */
	public static List<Element> getElementsByTagName(Element element, String tag){
		List<Element> elements = new ArrayList<Element>();
		NodeList list = element.getChildNodes();
		for(int i=0;i<list.getLength();i++){
			if(list.item(i) instanceof Element){
				Element e = (Element) list.item(i);
				if(e.getTagName().equals(tag)){
					elements.add(e);
				}
			}
		}
		return elements;
	}
}
