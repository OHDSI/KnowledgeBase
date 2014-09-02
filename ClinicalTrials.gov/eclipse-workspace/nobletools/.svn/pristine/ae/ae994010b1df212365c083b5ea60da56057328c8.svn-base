package edu.pitt.info.extract.model;

import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.ListIterator;
import java.util.Map;
import java.util.Set;
import java.util.TreeSet;

import org.w3c.dom.Document;
import org.w3c.dom.Element;

import edu.pitt.info.extract.model.util.XMLUtils;
import edu.pitt.terminology.Terminology;
import edu.pitt.terminology.lexicon.Concept;
import edu.pitt.terminology.util.PathHelper;
import edu.pitt.terminology.util.TerminologyException;


/**
 * this class represents a single piece of information
 * and its possible values that need to be extracted from text
 * @author tseytlin
 *
 */
public class TemplateItem implements Comparable {
	public static final String TYPE_DIAGNOSIS = "diagnosis";
	public static final String TYPE_FINDING   = "finding";
	public static final String TYPE_ORGAN   = "organ";
	public static final String TYPE_ATTRIBUTE   = "attribute";
	public static final String TYPE_MODIFIER   = "modifier";
	public static final String TYPE_ATTRIBUTE_VALUE   = "attribute-value";
	public static final String TYPE_NUMERIC_VALUE   = "numeric-value";
	public static final String TYPE_TEXTC_VALUE   = "text-value";
	
	public static final String DOMAIN_SELF = "self";
	public static final String DOMAIN_ATTRIBUTE = "attribute";
	public static final String DOMAIN_VALUE = "value";
	public static final String DOMAIN_BOOLEAN = "boolean";
	
	private String type,valueDomain = DOMAIN_BOOLEAN;
	private Concept concept;
	private Template template;
	private Map<TemplateItem,Set<TemplateItem>> attributeValues;
	private TemplateItem feature;
	private Set<TemplateItem> modifiers;
	private Set<TemplateItem> values;
	private Set<TemplateItem> units;
	
	/**
	 * get template item name
	 * @return
	 */
	public String getName(){
		return concept.getName();
	}
	
	/**
	 * get a type of template item
	 * @return
	 */
	public String getType(){
		return type;
	}
	
	public void setType(String type) {
		this.type = type;
	}

	public String getValueDomain() {
		return valueDomain;
	}

	public void setValueDomain(String valueDomain) {
		this.valueDomain = valueDomain;
	}

	/**
	 * get template item definition
	 * @return
	 */
	public String getDescription(){
		return concept.getDefinition();
	}

	/**
	 * get a concept object representing this template iterm
	 * @return
	 */
	public Concept getConcept() {
		return concept;
	}

	/**
	 * set a concept object representing this template iterm
	 * @return
	 */
	public void setConcept(Concept concept) {
		this.concept = concept;
	}
	
	/**
	 * get a set of attributes associated with this template item
	 * @return
	 */
	public Set<TemplateItem> getAttributes(){
		return getAttributeValues().keySet();
	}

	
	/**
	 * get a feature that is associated with an attribute 
	 * @return
	 */
	public TemplateItem getFeature() {
		return (feature != null)?feature:this;
	}

	/**
	 * set a feature associated with an attribute
	 * @param feature
	 */
	public void setFeature(TemplateItem feature) {
		this.feature = feature;
	}

	/**
	 * get a mapping between attributes and its associated set of values
	 * @return
	 */
	public Map<TemplateItem, Set<TemplateItem>> getAttributeValues() {
		if(attributeValues == null)
			attributeValues = new HashMap<TemplateItem, Set<TemplateItem>>();
		return attributeValues;
	}
	
	
	/**
	 * get attribute values associated with a given attribute
	 * @param attribute
	 * @return
	 */
	public Set<TemplateItem> getAttributeValues(TemplateItem attribute){
		Set<TemplateItem> list = getAttributeValues().get(attribute);
		return (list != null)?list:Collections.EMPTY_SET;
	}
	
	/**
	 * add a new attribute value to 
	 * @param attribute
	 * @param value
	 */
	public void addAttributeValue(TemplateItem attribute, TemplateItem value){
		Set<TemplateItem> list = getAttributeValues().get(attribute);
		if(list == null){
			list = new TreeSet<TemplateItem>();
			getAttributeValues().put(attribute,list);
		}
		list.add(value);
	}
	
	/**
	 * add a new attribute value to 
	 * @param attribute
	 * @param value
	 */
	public void removeAttributeValue(TemplateItem attribute, TemplateItem value){
		Set<TemplateItem> list = getAttributeValues().get(attribute);
		if(list != null){
			list.remove(value);
		}
	}

	/**
	 * get a set of modifiers
	 * @return
	 */
	public Set<TemplateItem> getModifiers() {
		if(modifiers == null)
			modifiers = new TreeSet<TemplateItem>();
		return modifiers;
	}
	
	/**
	 * add a modifier
	 * @param mod
	 */
	public void addModifier(TemplateItem mod){
		getModifiers().add(mod);
	}

	
	/**
	 * get a set of available values
	 * @return
	 */
	public Set<TemplateItem> getValues() {
		if(values == null)
			values = new TreeSet<TemplateItem>();
		return values;
	}

	/**
	 * get a set of available units per value
	 * @return
	 */
	public Set<TemplateItem> getUnits() {
		if(units == null)
			units = new TreeSet<TemplateItem>();
		return units;
	}

	/**
	 * get a list of templates that include this item
	 * @return
	 */
	public Template getTemplate() {
		return template;
	}

	/**
	 * add template to a list
	 * @param template
	 */
	public void setTemplate(Template template) {
		this.template = template;
	}
	
	/**
	 * compare to other template item
	 */
	public int compareTo(Object o) {
		return getConcept().compareTo(((TemplateItem)o).getConcept());
	}
	
	public String toString(){
		String md = "";
		String at = "";
		String vl = "";
		String un = "";
		if(!getModifiers().isEmpty())
			md = ""+ getModifiers();
		if(!getAttributeValues().isEmpty())
			at = ""+ getAttributeValues();
		if(!getValues().isEmpty())
			vl = ""+ getValues();
		if(!getUnits().isEmpty())
			un = ""+ getUnits();
		return (md+" "+getName()+" "+at+" "+vl+" "+un).trim();
	}
	
	
	public boolean equals(Object o){
		return getConcept().equals(((TemplateItem)o).getConcept());
	}

	public int hashCode() {
		return getConcept().hashCode();
	}
	
	
	/**
	 * get terminology
	 * @return
	 */
	public Terminology getTerminology(){
		if(template != null)
			return template.getTerminology();
		return null;
	}
	
	
	/**
	 * get path helper
	 * @return
	 */
	public PathHelper getPathHelper(){
		if(template != null)
			return template.getPathHelper();
		return null;
	}
	

	/**
	 * extract instances from the document that fit this template
	 * @param doc
	 * @return
	 */
	public List<ItemInstance> process(AnnotatedDocument doc) throws TerminologyException{
		List<ItemInstance> items = new ArrayList<ItemInstance>();
		PathHelper paths = getPathHelper();
		// first pass
		for(Concept c: doc.getConcepts()){
			if(paths.hasAncestor(c,getConcept())){
				ItemInstance item = new ItemInstance(this,c);
				item.process(doc);
				addInstance(paths, items, item);
			}else if(concept.getCodes() != null && !concept.getCodes().isEmpty() && c.getSources().length > 0){
				// what if there is a linkage code
				String code = concept.getCode(c.getSources()[0]);
				if(code != null){
					Concept cc = (code.equals(c.getSources()[0].getName()))?c.getTerminology().getRootConcepts()[0]:c.getTerminology().lookupConcept(code);
					if(cc != null){
						if(paths.hasAncestor(c,cc)){
							ItemInstance item = new ItemInstance(this,c);
							item.process(doc);
							addInstance(paths, items, item);
						}
					}
				}
			}
		}
		
		// second pass, if nothing was found and there is a more general feature available
		if(items.isEmpty() && feature != null){
			for(Concept c: doc.getConcepts()){
				if(paths.hasAncestor(c,getFeature().getConcept())){
					// process this template with feature concept
					ItemInstance item = new ItemInstance(this,c);
					item.process(doc);
					
					// process a feature template with feature concept
					ItemInstance fitem = new ItemInstance(getFeature(),c);
					fitem.process(doc);
					
					// if feature instance has attributes detected that this instance
					// does not, it belongs to a sibling attribute and should not be 
					// added as a found template item
					List<ItemInstance> l1 = item.getComponentInstances();
					List<ItemInstance> l2 = fitem.getComponentInstances();
					if(l1.size() == l2.size() && l1.containsAll(l2))
						addInstance(paths, items, item);
					
					// we found a secondary match based on a feature, if it doesn't contains
					// attributes or modifiers, they are probably wrong and belong to 
					// other template match, hence don't include it
					//if(!item.getAttributeValues().isEmpty() || !item.getModifiers().isEmpty())
					//	addInstance(paths, items, item);
				}
			}
		}
		
		
		return items;
	}

	// add item to a list in a clever way
	private void addInstance(PathHelper paths, List<ItemInstance> items, ItemInstance i){
		if(items.isEmpty()){
			items.add(i);
		}else{
			boolean filed = false;
			for(ListIterator<ItemInstance> it=items.listIterator();it.hasNext();){
				ItemInstance o = it.next();
				// if new item is identical then just merge annotations
				if(i.getConcept().equals(o.getConcept())){
					o.merge(i);
					filed = true;
					break;
				// if new item is more specific, then add it and remove the general	
				}else if(paths.hasAncestor(i.getConcept(),o.getConcept())){
					it.remove();
					i.merge(o);
					it.add(i);
					filed = true;
					break;
				// in other case just merge
				}else if(paths.hasAncestor(o.getConcept(),i.getConcept())){
					o.merge(i);
					filed = true;
					break;
				}
			}
			// if noting has been done, must be sibling, then merge
			if(!filed)
				items.add(i);
		}
		
	}
	
	/**
	 * convert Template to XML DOM object representation
	 * @return
	 */
	public Element toElement(Document doc){
		Element root = doc.createElement("TemplateItem");
		root.setAttribute("name",getName());
		root.setAttribute("type",getType());
		root.setAttribute("value.domain",getValueDomain());
		root.setAttribute("concept",getConcept().getCode());
		
		if(feature != null){
			Element f = doc.createElement("Feature");
			f.appendChild(feature.toElement(doc));
			root.appendChild(f);
		}
		
		if(!getModifiers().isEmpty()){
			Element f = doc.createElement("Modifiers");
			for(TemplateItem m: getModifiers())
				f.appendChild(m.toElement(doc));
			root.appendChild(f);
		}
	
		if(!getAttributeValues().isEmpty()){
			for(TemplateItem attr: getAttributeValues().keySet()){
				Element av = doc.createElement("AttributeValues");
				Element a = doc.createElement("Attribute");
				a.appendChild(attr.toElement(doc));
				av.appendChild(a);
				
				Element v = doc.createElement("Values");
				for(TemplateItem va: getAttributeValues().get(attr))
					v.appendChild(va.toElement(doc));
				av.appendChild(v);
				root.appendChild(av);
			}
		}
		
		
		if(!getValues().isEmpty()){
			Element f = doc.createElement("Values");
			for(TemplateItem m: getValues())
				f.appendChild(m.toElement(doc));
			root.appendChild(f);
		}
		
		if(!getUnits().isEmpty()){
			Element f = doc.createElement("Units");
			for(TemplateItem m: getUnits())
				f.appendChild(m.toElement(doc));
			root.appendChild(f);
		}
		
		return root;
	}
	

	/**
	 * initialize template from XML DOM object representation
	 * @param element
	 */
	public void fromElement(Element element) throws Exception{
		concept = getTemplate().getTerminology().lookupConcept(element.getAttribute("concept"));
		type = element.getAttribute("type");
		valueDomain = element.getAttribute("value.domain");
		
		Element f = XMLUtils.getElementByTagName(element,"Feature");
		if(f != null){
			TemplateItem item = new TemplateItem();
			item.setTemplate(getTemplate());
			item.fromElement(XMLUtils.getElementByTagName(f,"TemplateItem"));
			setFeature(item);
		}
		Element m = XMLUtils.getElementByTagName(element,"Modifiers");
		if(m != null){
			for(Element e: XMLUtils.getElementsByTagName(m,"TemplateItem")){
				TemplateItem item = new TemplateItem();
				item.setTemplate(getTemplate());
				item.fromElement(e);
				getModifiers().add(item);
			}
		}
		Element v = XMLUtils.getElementByTagName(element,"Values");
		if(v != null){
			for(Element e: XMLUtils.getElementsByTagName(v,"TemplateItem")){
				TemplateItem item = new TemplateItem();
				item.setTemplate(getTemplate());
				item.fromElement(e);
				getValues().add(item);
			}
		}
		Element u = XMLUtils.getElementByTagName(element,"Units");
		if(u != null){
			for(Element e: XMLUtils.getElementsByTagName(u,"TemplateItem")){
				TemplateItem item = new TemplateItem();
				item.setTemplate(getTemplate());
				item.fromElement(e);
				getUnits().add(item);
			}
		}
		for(Element av : XMLUtils.getElementsByTagName(element,"AttributeValues")){
			Element at = XMLUtils.getElementByTagName(av,"Attribute");
			Element vl = XMLUtils.getElementByTagName(av,"Values");
			
			TemplateItem attr = new TemplateItem();
			attr.setTemplate(getTemplate());
			attr.fromElement(XMLUtils.getElementByTagName(at,"TemplateItem"));
		
			for(Element e: XMLUtils.getElementsByTagName(vl,"TemplateItem")){
				TemplateItem item = new TemplateItem();
				item.setTemplate(getTemplate());
				item.fromElement(e);
				addAttributeValue(attr,item);
			}
		}
	}
}
