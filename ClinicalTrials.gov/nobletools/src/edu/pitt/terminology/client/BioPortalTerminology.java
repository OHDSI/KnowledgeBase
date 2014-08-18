package edu.pitt.terminology.client;

import static edu.pitt.ontology.bioportal.BioPortalHelper.EXACT_MATCH;
import static edu.pitt.ontology.bioportal.BioPortalHelper.MAX_SEARCH_HITS;
import static edu.pitt.ontology.bioportal.BioPortalHelper.PROPERTIES_MATCH;
import static edu.pitt.ontology.bioportal.BioPortalHelper.SEARCH;
import static edu.pitt.ontology.bioportal.BioPortalHelper.getElementByTagName;
import static edu.pitt.ontology.bioportal.BioPortalHelper.getElementsByTagName;
import static edu.pitt.ontology.bioportal.BioPortalHelper.openURL;
import static edu.pitt.ontology.bioportal.BioPortalHelper.parseXML;

import java.net.URI;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.w3c.dom.Document;
import org.w3c.dom.Element;

import edu.pitt.ontology.IClass;
import edu.pitt.ontology.IOntology;
import edu.pitt.ontology.IResource;
import edu.pitt.ontology.bioportal.BClass;
import edu.pitt.ontology.bioportal.BOntology;
import edu.pitt.ontology.bioportal.BioPortalHelper;
import edu.pitt.ontology.bioportal.BioPortalRepository;
import edu.pitt.terminology.AbstractTerminology;
import edu.pitt.terminology.lexicon.Concept;
import edu.pitt.terminology.lexicon.Relation;
import edu.pitt.terminology.lexicon.Source;
import edu.pitt.terminology.util.TerminologyException;

public class BioPortalTerminology extends AbstractTerminology {
	private BOntology ontology;
	private BioPortalRepository repository = new BioPortalRepository();

	public BioPortalTerminology(){
		super();
	}
	
	public BioPortalTerminology(BOntology ontology){
		super();
		this.ontology = ontology;
	}
	
	
	public void setOntology(BOntology ontology) {
		this.ontology = ontology;
	}

	public void setOntology(String name) {
		// repository.getOntology("NCI_Thesaurus");
		IOntology [] ont = repository.getOntologies(name);
		if(ont.length > 0)
			setOntology((BOntology) ont[0]);
	}

	/**
	 * converts IClass to Concept
	 */
	protected Concept convertConcept(Object obj) {
		if (obj instanceof IClass)
			return ((IClass)obj).getConcept();
		else
			return null;
	}

	public Source[] getFilterSources() {
		return getSources();
	}

	public Concept[] getRelatedConcepts(Concept c, Relation r) throws TerminologyException {
		IClass cls = c.getConceptClass();
		if(r == Relation.BROADER){
			//IClass cls = ontology.getClass(c.getCode());
			if(cls != null){
				return convertConcepts(cls.getDirectSuperClasses());
			}
		}else if(r == Relation.NARROWER){
			//IClass cls = ontology.getClass(c.getCode());
			if(cls != null){
				return convertConcepts(cls.getDirectSubClasses());
			}
		}else if(r == Relation.SIMILAR){
			//IClass cls = ontology.getClass(c.getCode());
			if(cls != null){
				List<IClass> clses = new ArrayList<IClass>();
				for(IClass eq: cls.getEquivalentClasses()){
					if(!eq.isAnonymous()){
						clses.add(eq);
					}
				}
				return convertConcepts(clses);
			}
		}
		return new Concept [0];
		
		
		
		/*
		String n = c.getName().replaceAll(" ", "_");
		IClass cls = ontology.createClass(n);

		IClass[] clsResult = null;
		try {
			// get parents
			if (r.equals(Relation.BROADER))
				clsResult = cls.getDirectSuperClasses();
			// get children
			else if (r.equals(Relation.NARROWER))
				clsResult = cls.getDirectSubClasses();

		} catch (Exception ex) {
			throw new TerminologyException(ex.getMessage());
		}

		if (clsResult != null) {
			ArrayList<Concept> concepts = new ArrayList<Concept>();
			for (int i = 0; i < clsResult.length; i++) {
				concepts.add(convertConcept(clsResult[i]));
			}
			return concepts.toArray(new Concept[] {});
		} else
			return null;
		*/	
	}

	private Concept [] convertConcepts(IClass [] clses){
		Concept [] concepts = new Concept[clses.length];
		for(int i=0;i<concepts.length;i++)
			concepts[i] = clses[i].getConcept();
		return concepts;
	}
	
	private Concept [] convertConcepts(Collection<IClass> clses){
		Concept [] concepts = new Concept[clses.size()];
		int i=0;
		for(IClass cls: clses)
			concepts[i++] = cls.getConcept();
		return concepts;
	}
	
	
	public Map getRelatedConcepts(Concept c) throws TerminologyException {
		Map<Relation,List<Concept>> map = new HashMap<Relation,List<Concept>>();
		map.put(Relation.BROADER,Arrays.asList(getRelatedConcepts(c,Relation.BROADER)));
		map.put(Relation.NARROWER,Arrays.asList(getRelatedConcepts(c,Relation.NARROWER)));
		map.put(Relation.SIMILAR,Arrays.asList(getRelatedConcepts(c,Relation.SIMILAR)));
		return map;
	}

	/**
	 * get all ontologies in bioportal
	 */
	public Source[] getSources() {
		return iOntologiesToSource(repository.getOntologies());
	}

	public Concept lookupConcept(String cui) throws TerminologyException {
		if(ontology == null)
			return null;
		IResource cls = ontology.getResource(cui);
		return (cls != null && cls instanceof IClass)?((IClass)cls).getConcept():null;
	}

	/**
	 * According to the Bioportal 2.0 docs there should be "exactmatch" and
	 * "contains" only.
	 */
	public Concept[] search(String text, String method) throws TerminologyException {
		return (ontology != null)?ontology.search(text, method):searchAll(text, method);
	}

	/**
	 * The search result should be light- not BClass, but Concept. We can create
	 * BClasses later if needed
	 */
	public Concept[] searchAll(String text, String method) throws TerminologyException {
	    /*
		* ontologyids=<ontologyid>,<ontologyid>… - limits the search to specific ontologies (default: all ontologies)
	    * isexactmatch=[1/0] – match the entire concept name (default: 0)
	    * includeproperties=[1/0] – include attributes in the search (default: 0)
	    * pagesize=<pagesize> - the number of results to display in a single request (default: all)
	    * pagenum=<pagenum> - the page number to display (pages are calculated using <total results>/<pagesize>) (default: 1)
	    * maxnumhits=<maxnumhits> - the maximum number of top matching results to return (default: 1000)
	    * subtreerootconceptid=<uri-encoded conceptid> - narrow the search to concepts residing in a sub-tree, 
	    *  where the "subtreerootconceptid" is the root node. This feature requires a SINGLE <ontologyid> passed in using the "onotlogyids" parameter. 
		*/
		
		// create a URL
		String url = repository.getURL()+SEARCH+text+"/";
		
		// is it exact match or not
		url += "&isexactmatch="+((method.equalsIgnoreCase(EXACT_MATCH))?1:0);
		
		// include attributess
		url += "&includeproperties="+((method.equalsIgnoreCase(PROPERTIES_MATCH))?1:0);
		
		// set number of results
		url += "&maxnumhits="+MAX_SEARCH_HITS;
		
		// required field
		url += "&"+repository.getAPIKey();
		
		Document doc = parseXML(openURL(url));
		if(doc != null){
			Element results = getElementByTagName(doc.getDocumentElement(),"searchResultList");
			List<Concept> list = new ArrayList<Concept>();
			if(results != null){
				// get concept name from each search bean, rest of info is useless for now
				for(Element e: getElementsByTagName(results,"searchBean")){
					Element o = getElementByTagName(e,"ontologyDisplayLabel");
					Element n = getElementByTagName(e,"conceptIdShort");
					if(n != null && o != null){
						// get ontology uri
						String oname = o.getTextContent().trim();
						String ouri = BioPortalHelper.BIOPORTAL_URL+BioPortalHelper.deriveName(oname);
						
						// get resource uri
						String name = n.getTextContent().trim();
						//String uri =  ouri+"#"+name;
						//IClass cls = (IClass) repository.getResource(URI.create(uri));
						
						//if(cls == null){
						IOntology ont = repository.getOntology(URI.create(ouri));
						if(ont != null){
							IClass cls = new BClass((BOntology)ont,name);
							cls.getConcept().setTerminology(this);
							cls.getConcept().setSearchString(text);
							list.add(cls.getConcept());
						}
						//}
						
						//if(cls != null)
						//	list.add(cls.getConcept());
					}
				}
			}
			return list.toArray(new Concept [0]);
		}
		return new Concept [0];
	}
	
	
	public Concept[] search(String text) throws TerminologyException {
		Concept [] result =  search(text, "exactmatch");
		for(Concept c: result)
			c.setTerminology(this);
		return result;
	}

	
	public String[] getSearchMethods() {
		return new String [] {BioPortalHelper.EXACT_MATCH,BioPortalHelper.CONTAINS_MATCH,BioPortalHelper.PROPERTIES_MATCH};
	}

	public void setFilterSources(Source[] srcs) {
		// NOOP
	}

	public String getDescription() {
		return ontology.getDescription();
	}

	public String getFormat() {
		return ontology.getFormat();
	}

	public String getLocation() {
		return ontology.getLocation();
	}

	public String getName() {
		return "BioPortal";
	}

	public URI getURI() {
		return URI.create(BioPortalRepository.DEFAULT_BIOPORTAL_URL);
	}

	public String getVersion() {
		return "2.0";
	}

	private Source[] iOntologiesToSource(IOntology[] iontologies) {
		Source[] sources = new Source[iontologies.length];

		for (int i = 0; i < iontologies.length; i++)
			sources[i] = new Source(iontologies[i].getName());

		return sources;
	}

	
	/**
	 * get all root concepts. This makes sence if Terminology is in fact ontology
	 * that has heirchichal structure
	 * @return
	 */
	public Concept[] getRootConcepts() throws TerminologyException {
		IClass [] clss = ontology.getRootClasses();
		Concept [] list = new Concept [clss.length];
		for(int i=0;i<list.length;i++)
			list[i] = clss[i].getConcept();
		return list;
	}
	
	public IOntology getOntology(){
		return ontology;
	}
	
	
	public static void main(String [] args) throws Exception{
		BioPortalTerminology term = new BioPortalTerminology();
		term.setOntology("NCI_Thesaurus");
		long time = System.currentTimeMillis();
		// ZFA_0001234 | C0025202
		System.out.println("--- lookup ---");
		Concept c = term.lookupConcept("C0025202");
		if(c != null){
			c.printInfo(System.out);
		}
		
		System.out.println("lookup time "+(System.currentTimeMillis()-time));
		
		System.out.println("--- search ---");
		
		time = System.currentTimeMillis();
		for(String text: Arrays.asList("melanoma","melanoma")){
			System.out.println("- "+text+" -");
			Concept [] cs = term.search(text);
			for(Concept i: cs){
				i.printInfo(System.out);
			}
			System.out.println("--");
		}
		System.out.println("lookup time "+(System.currentTimeMillis()-time));
	}
}
