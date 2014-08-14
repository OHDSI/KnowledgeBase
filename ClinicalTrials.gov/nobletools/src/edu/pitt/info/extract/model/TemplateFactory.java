package edu.pitt.info.extract.model;

import static edu.pitt.info.extract.model.util.SlideTutorOntologyHelper.ANATOMY_ONTOLOGY_URI;
import static edu.pitt.info.extract.model.util.SlideTutorOntologyHelper.LOCATIONS;
import static edu.pitt.info.extract.model.util.SlideTutorOntologyHelper.MODIFIERS;
import static edu.pitt.info.extract.model.util.SlideTutorOntologyHelper.VALUES;
import static edu.pitt.info.extract.model.util.SlideTutorOntologyHelper.getFeature;
import static edu.pitt.info.extract.model.util.SlideTutorOntologyHelper.getPotentialTemplateAttributes;
import static edu.pitt.info.extract.model.util.SlideTutorOntologyHelper.isAnatomicLocation;
import static edu.pitt.info.extract.model.util.SlideTutorOntologyHelper.isAttributeCategory;
import static edu.pitt.info.extract.model.util.SlideTutorOntologyHelper.isDisease;
import static edu.pitt.info.extract.model.util.SlideTutorOntologyHelper.isFeature;
import static edu.pitt.info.extract.model.util.SlideTutorOntologyHelper.isHeader;
import static edu.pitt.info.extract.model.util.SlideTutorOntologyHelper.isLocation;
import static edu.pitt.info.extract.model.util.SlideTutorOntologyHelper.isModifier;
import static edu.pitt.info.extract.model.util.SlideTutorOntologyHelper.isNumber;
import static edu.pitt.info.extract.model.util.SlideTutorOntologyHelper.isWorksheet;

import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.transform.TransformerException;

import org.w3c.dom.Document;
import org.w3c.dom.Element;

import edu.pitt.info.extract.model.util.XMLUtils;
import edu.pitt.ontology.IClass;
import edu.pitt.ontology.IOntology;
import edu.pitt.ontology.IRestriction;
import edu.pitt.ontology.protege.POntology;
import edu.pitt.ontology.protege.concepts.ConceptRegistry;
import edu.pitt.terminology.CompositTerminology;
import edu.pitt.terminology.Terminology;
import edu.pitt.terminology.client.IndexFinderTerminology;
import edu.pitt.terminology.lexicon.Concept;
import edu.pitt.terminology.lexicon.Source;
import edu.pitt.terminology.util.TerminologyException;
import edu.pitt.text.tools.TextTools;

/**
 * create Templates for information extraction from various sources
 * @author tseytlin
 */
public class TemplateFactory {
	private Map<String,Template> templates;
	private static TemplateFactory instance;
	private TemplateFactory(){}
	public static TemplateFactory getInstance(){
		if(instance == null)
			instance = new TemplateFactory();
		return instance;
	}
	
	/**
	 * get a map of templates
	 */
	public Map<String,Template> getTemplateMap(){
		if(templates == null)
			templates = new HashMap<String, Template>();
		return templates;
	}
	
	/**
	 * get template based on name
	 */
	public Template getTemplate(String name){
		return getTemplateMap().get(name);
	}
	
	/**
	 * get all template based on name
	 */
	public List<Template> getTemplates(){
		if(getTemplateMap().values() instanceof List)
			return (List)getTemplateMap().values();
		return new ArrayList<Template>(getTemplateMap().values());
	}
	
	/**
	 * import templates from url
	 * looks at URL to figure out how to import it
	 * @param url
	 */
	public void importTemplates(String url) throws Exception {
		// is this a known SlideTutor ontology?
		if(url.matches("http://.*/curriculum/owl/.*\\.owl(#.+)?")){
			addSlideTutorTemplates(url);
		// is this an existing terminology?
		}else if(url.endsWith(IndexFinderTerminology.TERM_SUFFIX) && new File(url).exists()){
			addTerminologyTemplate(url);
		}else if(new File(IndexFinderTerminology.getPersistenceDirectory(),url+IndexFinderTerminology.TERM_SUFFIX).exists()){
			addTerminologyTemplate(url);
		}
	}
	
	/**
	 * create a template from terminology where each root is a template item
	 * @param url
	 */
	private void addTerminologyTemplate(String url) throws Exception {
		Terminology terminology = new IndexFinderTerminology(url);
		
		// setup template
		Template template = new Template();
		template.setName(terminology.getName()+" Template");
		template.setDescription(terminology.getDescription());
		template.setTerminology(terminology);
		template.getFilters().add(new DocumentFilter("(?s)^BACKGROUND:$.*^$",true));
		
		for(Concept c: terminology.getRootConcepts()){
			TemplateItem item = new TemplateItem();
			/*			
			{
				//TODO: this is a hack for BRAF, let it stay for now?
				public List<ItemInstance> process(AnnotatedDocument doc) throws TerminologyException {
					// do not include concepts from BACKGROUND section and below
					List<ItemInstance> items =  super.process(doc);
					int s = doc.getText().indexOf("\nBACKGROUND:\n");
					if(s > -1){
						List<ItemInstance> items2 = new ArrayList<ItemInstance>();
						for(ItemInstance i: items){
							if(i.getAnnotations().get(0).getEndPosition() < s)
								items2.add(i);
						}
						return items2;
					}
					return items;
				}
				
			};
			*/
			item.setTemplate(template);
			item.setConcept(c);
			item.setType(TemplateItem.TYPE_FINDING);
			item.setValueDomain(TemplateItem.DOMAIN_SELF);
			template.getTemplateItems().add(item);
		}
		getTemplateMap().put(template.getName(),template);
		
	}


	public static class SlideTutorConcept extends Concept {
		public SlideTutorConcept(IClass cls) {
			super(cls);
			if(isWorksheet(cls))
				setName(cls.getName());
		}
	}
	
	/**
	 * create a template object from SlideTutor ontology
	 * @param url
	 * @return
	 */
	private void addSlideTutorTemplates(String url) throws Exception {
		IOntology ont = POntology.loadOntology(url);
		ConceptRegistry.REGISTRY.put(url,SlideTutorConcept.class.getName());
		
		// create in-memory terminology from this ontology
		IndexFinderTerminology term = new IndexFinderTerminology();
		term.loadOntology(ont,null,true,true);
		term.setScoreConcepts(false);
		term.setSelectBestCandidate(false);
		term.setCachingEnabled(false);
		
		IndexFinderTerminology aterm = new IndexFinderTerminology();
		aterm.loadOntology(POntology.loadOntology(ANATOMY_ONTOLOGY_URI),null,true,true);
		aterm.setCachingEnabled(false);
		
		// add a terminology to it
		CompositTerminology terminology = new CompositTerminology();
		terminology.addTerminology(term);
		terminology.addTerminology(aterm);
		
		
		// go over templates
		for(IClass template: ont.getClass("TEMPLATES").getDirectSubClasses()){
			// get orders
			final Map<String,Integer> conceptOrder = new HashMap<String,Integer>();
			for(Object o: template.getPropertyValues(ont.getProperty("order"))){
				String [] p = o.toString().split(":");
				if(p.length == 2){
					conceptOrder.put(p[0].trim(),new Integer(p[1].trim()));
				}
			}
			// get triggers
			//TODO:
			
			// get template contents
			List<IClass> templateContent = new ArrayList<IClass>();
			for(IRestriction r: template.getRestrictions(ont.getProperty("hasPrognostic"))){
				IClass c = (IClass) r.getParameter().getOperand();
				templateContent.add(c);
			}
			
			// sort them in order
			Collections.sort(templateContent,new Comparator<IClass>() {
				public int compare(IClass o1, IClass o2) {
					if(conceptOrder.containsKey(o1.getName()) && conceptOrder.containsKey(o2.getName())){
						return conceptOrder.get(o1.getName()).compareTo(conceptOrder.get(o2.getName()));
					}
					return o1.compareTo(o2);
				}
			});
			
			// setup template
			Template temp = new Template();
			temp.setName(TextTools.getCapitalizedWords(template.getName()));
			temp.setDescription(template.getDescription());
			temp.setTerminology(terminology);
			
			for(IClass c: templateContent){
				TemplateItem t = convertSlideTutorClass(c,temp);
				temp.getTemplateItems().add(t);
			}
			getTemplateMap().put(template.getName(),temp);
		}
	}

	private static String getCode(String uri, boolean truncate){
		if(truncate){
			int x = uri.lastIndexOf('/');
			return (x > -1)?uri.substring(x+1):uri;
		}
		return uri;
	}
	/**
	 * create a template item from a given class
	 * @param c
	 * @return
	 */
	private static TemplateItem convertSlideTutorClass(IClass c, Template template) {
		IOntology ont = c.getOntology();
		TemplateItem item = new TemplateItem();
		item.setTemplate(template);
		item.setConcept(c.getConcept());
		item.getConcept().setCode(getCode(item.getConcept().getCode(),true));
		item.setValueDomain(TemplateItem.DOMAIN_BOOLEAN);
		
		// figure out type
		if(isFeature(c)){
			item.setType(TemplateItem.TYPE_FINDING);
		}else if(isAttributeCategory(c)){
			item.setType(TemplateItem.TYPE_ATTRIBUTE);
		}else if(isLocation(c)){
			item.setType(TemplateItem.TYPE_ATTRIBUTE_VALUE);
		}else if(isNumber(c)){
			item.setType(TemplateItem.TYPE_NUMERIC_VALUE);
		}else if(isModifier(c)){
			item.setType(TemplateItem.TYPE_MODIFIER);
		}else if(isDisease(c)){
			item.setType(TemplateItem.TYPE_DIAGNOSIS);
			item.setValueDomain(TemplateItem.DOMAIN_SELF);
		}
		
		// if feature process attributes
		if(isFeature(c)){
			IClass feature = getFeature(c);	
			
			if(!feature.equals(c)){
				item.setFeature(convertSlideTutorClass(feature,template));
				
				// if feature is a child of value then, it is a fully specified feature attr/value, and
				// we just need a feature
				if(isOfParent(c,VALUES))
					item = item.getFeature();
				
				// if we have a more general feature specified, then 
				
			}
			
			// process potential attributes
			for(IClass attribute: getPotentialTemplateAttributes(c)){
				// if used attribute, skip
				//if(!usedAttributes.contains(attribute))
				//	continue;
				
				TemplateItem a = convertSlideTutorClass(attribute,template);
				// handle numbers
				if(isNumber(attribute)){
					item.getValues().add(a);
					item.setValueDomain(TemplateItem.DOMAIN_VALUE);
				// handle units
				}else if(isOfParent(attribute,"UNITS")){
					item.getUnits().add(a);
				// handle locations
				}else if(isLocation(attribute)){
					TemplateItem l = convertSlideTutorClass(ont.getClass(LOCATIONS), template);
					item.addAttributeValue(l,a);
				// handle attributes with categories and modifiers
				}else if(isModifier(attribute)){
					if(!attribute.hasSubClass(c))
						item.setValueDomain(TemplateItem.DOMAIN_ATTRIBUTE);
					for(IClass  acat : attribute.getDirectSuperClasses()){
						if(isAttributeCategory(acat) && !acat.equals(ont.getClass(MODIFIERS))){
							TemplateItem l = convertSlideTutorClass(acat, template);
							item.addAttributeValue(l, a);
						}else{
							item.addModifier(a);
						}
					}
				}else{
					//System.err.println(attribute);
				}
			}
			
			// do something special for worksheet?
			if(isWorksheet(c)){
				item.setValueDomain(TemplateItem.DOMAIN_SELF);
			}else if(isHeader(c)){
				item.setValueDomain(TemplateItem.DOMAIN_SELF);
			} 
			
			// anatomic location?	
			if(isAnatomicLocation(c)){
				item.setType(TemplateItem.TYPE_ORGAN);
				String code = getCode((String) c.getPropertyValue(ont.getProperty("code")),true);
				if(code != null){
					String cd = (code.indexOf("#") > -1)?code.substring(0,code.lastIndexOf("#")):code;
					String nm = (cd.indexOf("/") > -1)?cd.substring(cd.lastIndexOf("/")+1):cd;
					Source src = new Source(nm, "", cd);
					try {
						template.getTerminology().lookupConcept(item.getConcept().getCode()).addCode(code,src);
					} catch (TerminologyException e) {
						e.printStackTrace();
					}
					item.getConcept().addCode(code,src);
					
				}
				
			}
		}else if(isDisease(c)){
			//NOOP
		}
		
		
		return item;
	}
	
	/**
	 * check if this entry is a feature
	 * @return
	 */
	public static boolean isOfParent(IClass cls,String parent){
		if(cls == null)
			return false;
		IOntology o = cls.getOntology();
		IClass p = o.getClass(parent);
		return cls.equals(p) || cls.hasSuperClass(p);
	}
	
	
	/**
	 * export template
	 * @param t
	 * @param out
	 * @throws IOException
	 * @throws ParserConfigurationException 
	 * @throws TransformerException 
	 */
	public void exportTemplate(Template t, OutputStream out) throws Exception{
		// initialize document and root
		DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
		Document doc = factory.newDocumentBuilder().newDocument();
		
		// create DOM object
		doc.appendChild(t.toElement(doc));
		
		// write out XML
		XMLUtils.writeXML(doc, out);
	}
	

	/**
	 * export template
	 * @param t
	 * @param out
	 * @throws IOException
	 */
	public Template importTemplate(InputStream in) throws Exception{
		Document document = XMLUtils.parseXML(in);
		
		//print out some useful info
		Element element = document.getDocumentElement();
		if(element.getTagName().equals("Template")){
			Template temp = new Template();
			temp.fromElement(element);
			getTemplateMap().put(temp.getName(),temp);
			return temp;
		}
		return null;
	}
	
	
	/**
	 * @param args
	 *
	public static void main(String[] args) throws Exception {
		TemplateFactory tf = TemplateFactory.getInstance();
		tf.importTemplates("http://slidetutor.upmc.edu/curriculum/owl/skin/PITT/Melanocytic.owl");
		// print out template information
		for(Template t: tf.getTemplates()){
			System.out.println("---| "+t.getName()+" |---");
			for(TemplateItem i: t.getTemplateItems()){
				System.out.println("\t"+i);
			}
		}
		
		System.out.println("\n-----------------------------------------\n");
		
		// process sample report with one of the templates
		Template template = tf.getTemplate("invasive_lesion_template");
		
		// get sample document
		File f = new File("/home/tseytlin/Data/Reports/ReportProcessorInput/AP_201.txt");
		String text = TextTools.getText(new FileInputStream(f));
		AnnotatedDocument doc = new AnnotatedDocument();
		doc.setName(f.getName());
		doc.setText(text);
		
		
		
		// do a simple parsing of this document
		long time = System.currentTimeMillis();
		int offset = 0;
		for(String line: text.split("\n")){
			for(String phrase: line.split("[,\\:]")){
				for(Concept c: template.getTerminology().search(phrase,NobleCoderTerminology.BEST_MATCH)){
					for(Annotation a: Annotation.getAnnotations(c)){
						a.updateOffset(offset);
						doc.addAnnotation(a);
					}
					doc.addConcept(c);
				}
				offset += (line.length()+1);
			}
			offset++;
		}
		doc.sort();
		time = System.currentTimeMillis()-time;
		System.out.println(doc.getText());
		System.out.println("--------------");
		for(Annotation a: doc.getAnnotations()){
			System.out.println(a.getText()+" ... ("+a.getStartPosition()+","+a.getEndPosition()+ ") \t->\t"+a.getConcept().getName()+" ... "+a.getConcept().getCode());
		}
		System.out.println("\n----------------( "+time+" )-------------------\n");
		
		// now lets do information extraction
		if(template.isAppropriate(doc)){
			time = System.currentTimeMillis();
			List<ItemInstance> items = template.process(doc);
			time = System.currentTimeMillis()-time;
			for(ItemInstance i: items){
				System.out.println(i.getQuestion()+" : "+i.getAnswer());
			}
			System.out.println("\n----------------( "+time+" )-------------------\n");
		}
	}
	*/

}
