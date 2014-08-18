package edu.pitt.info.extract.model;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.Collections;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.ListIterator;
import java.util.Map;
import java.util.Set;
import java.util.TreeSet;

import edu.pitt.terminology.client.IndexFinderTerminology;
import edu.pitt.terminology.lexicon.Annotation;
import edu.pitt.terminology.lexicon.Concept;
import edu.pitt.terminology.util.TerminologyException;
import edu.pitt.text.tools.NegEx;
import edu.pitt.text.tools.TextTools;

/**
 * This class reperesents an identified instance of the TemplateItem.
 * It is essentially an "answer" to a template's "question"
 * @author tseytlin
 */
public class ItemInstance implements Comparable {
	private Concept concept;
	private TemplateItem templateItem;
	private ItemInstance feature;
	private Map<ItemInstance,Set<ItemInstance>> attributeValues;
	private Set<ItemInstance> modifiers;
	private Object value;
	private boolean absent;
	private ItemInstance unit;
	private List<Annotation> annotations;

	//private AnnotatedDocument document;
	
	/**
	 * initialise instance from template item and matched concept
	 * @param template item generating this instance
	 * @param concept representing the matched root/feature concept
	 */
	public ItemInstance(TemplateItem temp,Concept c){
		this.concept = c;
		this.templateItem = temp;
		Collections.addAll(getAnnotations(),c.getAnnotations());
	}
	
	/**
	 * get template item name
	 * @return
	 */
	public String getName(){
		return concept.getName();
	}

	
	
	public boolean isAbsent() {
		return absent;
	}

	public void setAbsent(boolean absent) {
		this.absent = absent;
	}

	/**
	 * get a list of annotations
	 * @return
	 */
	public List<Annotation> getAnnotations() {
		if(annotations == null)
			annotations = new ArrayList<Annotation>();
		return annotations;
	}
	/**
	 * get a type of template item
	 * @return
	 */
	public String getType(){
		return getTemplateItem().getType();
	}
	
	/**
	 * get template item definition
	 * @return
	 */
	public String getDescription(){
		String d = concept.getDefinition();
		if(d == null || d.length() == 0)
			d  = getTemplateItem().getDescription();
		return d;
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
	public Set<ItemInstance> getAttributes(){
		return getAttributeValues().keySet();
	}


	/**
	 * get a mapping between attributes and its associated set of values
	 * @return
	 */
	public Map<ItemInstance, Set<ItemInstance>> getAttributeValues() {
		if(attributeValues == null)
			attributeValues = new HashMap<ItemInstance, Set<ItemInstance>>();
		return attributeValues;
	}
	
	/**
	 * get attribute values associated with a given attribute
	 * @param attribute
	 * @return
	 */
	public Set<ItemInstance> getAttributeValues(ItemInstance attribute){
		Set<ItemInstance> list = getAttributeValues().get(attribute);
		return (list != null)?list:Collections.EMPTY_SET;
	}
	
	/**
	 * add a new attribute value to 
	 * @param attribute
	 * @param value
	 */
	public void addAttributeValue(ItemInstance attribute, ItemInstance value){
		Set<ItemInstance> list = getAttributeValues().get(attribute);
		if(list == null){
			list = new TreeSet<ItemInstance>();
			getAttributeValues().put(attribute,list);
		}
		list.add(value);
	}
	
	/**
	 * add a new attribute value to 
	 * @param attribute
	 * @param value
	 */
	public void removeAttributeValue(ItemInstance attribute, ItemInstance value){
		Set<ItemInstance> list = getAttributeValues().get(attribute);
		if(list != null){
			list.remove(value);
		}
	}

	/**
	 * get a set of modifiers
	 * @return
	 */
	public Set<ItemInstance> getModifiers() {
		if(modifiers == null)
			modifiers = new TreeSet<ItemInstance>();
		return modifiers;
	}
	
	/**
	 * add a modifier
	 * @param mod
	 */
	public void addModifier(ItemInstance mod){
		getModifiers().add(mod);
	}

	/**
	 * get all instances that were detected as part of this instance
	 * @return
	 */
	public List<ItemInstance> getComponentInstances(){
		List<ItemInstance> items = new ArrayList<ItemInstance>();
		if(getFeature() != null)
			items.add(getFeature());
		for(ItemInstance a: getAttributes())
			items.addAll(getAttributeValues().get(a));
		items.addAll(getModifiers());
		if(getUnit() != null)
			items.add(getUnit());
		
		return items;
	}
	
	/**
	 * get a set of available values
	 * @return
	 *
	public Set<TemplateItem> getValues() {
		if(values == null)
			values = new TreeSet<TemplateItem>();
		return values;
	}
	*/
	/**
	 * get a set of available units per value
	 * @return
	 *
	public Set<TemplateItem> getUnits() {
		if(units == null)
			units = new TreeSet<TemplateItem>();
		return units;
	}
	*/
	

	public TemplateItem getTemplateItem() {
		return templateItem;
	}

	public void setTemplateItem(TemplateItem templateItem) {
		this.templateItem = templateItem;
	}
	
	/**
	 * get value 
	 * @return
	 */
	public Object getValue(){
		return value;
	}
	
	public ItemInstance getFeature() {
		return feature;
	}

	public void setFeature(ItemInstance feature) {
		this.feature = feature;
	}

	public ItemInstance getUnit() {
		return unit;
	}

	public void setUnit(ItemInstance unit) {
		this.unit = unit;
	}

	public void setValue(Object value) {
		this.value = value;
	}

	/**
	 * get the question
	 * @return
	 */
	public String getQuestion(){
		if(TemplateItem.TYPE_DIAGNOSIS.equals(templateItem.getType()))
			return templateItem.getType();
		return templateItem.getName();
	}
	
	/**
	 * get the answer
	 * @return
	 */
	public String getAnswer(){
		// if we have a value, then value plus units
		if(value != null && value instanceof Double){
			return TextTools.toString((Double)value)+((unit != null)?" "+unit.getName():"");
		}
		// if we have an attribute
		if(TemplateItem.DOMAIN_SELF.equals(templateItem.getValueDomain())){
			return concept.getName();
		}
		// else return attribute if present
		if(!templateItem.getAttributeValues().isEmpty()){
			StringBuffer str = new StringBuffer();
			boolean includedAttribute = false;
			for(ItemInstance a: getAttributes()){
				for(ItemInstance v : getAttributeValues(a)){
					if(!templateItem.getName().toLowerCase().contains(v.getName().toLowerCase())){
						str.append(v.getName()+" ");
					}else{
						includedAttribute = true;
					}
				}
			}
			if(!includedAttribute && str.length() > 0)
				return str.toString().trim();
		}
			
		// return if thing is present or absent
		return isAbsent()?"absent":"present";
	}
	
	/**
	 * extract instances from the document that fit this template
	 * @param doc
	 * @return
	 */
	public void process(AnnotatedDocument doc) throws TerminologyException{
		// parse additional text to extract meaning
		List<Concept> r = getNeighbors(doc);
		List<Annotation> annotations = new ArrayList<Annotation>();
		
		// check for negation
		NegEx negex = new NegEx();
		negex.process(concept.getSearchString(),Collections.singletonList(concept));
		if(negex.getNegatedConcepts().contains(concept)){
			setAbsent(true);
			// add negation annotation
			for(Concept c: negex.getNegations())
				Collections.addAll(annotations,c.getAnnotations());
		}
		
		// parse concept for its attributes and values
		Concept c = findConcept(templateItem.getFeature());
		if(c != null){
			setFeature(new ItemInstance(templateItem.getFeature(),c));
		}

		// set attributes and modifiers
		for(TemplateItem attr: templateItem.getAttributes()){
			List<ItemInstance> inst = getMatchingInstances(templateItem.getAttributeValues().get(attr),null);
			if(inst.isEmpty())
				inst = getMatchingInstances(templateItem.getAttributeValues().get(attr),r);
			for(ItemInstance i: inst){
				addAttributeValue(new ItemInstance(attr,attr.getConcept()),i);
				annotations.addAll(i.getAnnotations());
			}
		}
		
		// set modifiers 
		List<ItemInstance> inst = getMatchingInstances(templateItem.getModifiers(),null);
		if(inst.isEmpty())
			inst = getMatchingInstances(templateItem.getModifiers(),r);
		for(ItemInstance i: inst){
			addModifier(i);
			annotations.addAll(i.getAnnotations());
		}
		// set units 
		inst = getMatchingInstances(templateItem.getUnits(),null);
		if(inst.isEmpty())
			inst = getMatchingInstances(templateItem.getUnits(),r);
		for(ItemInstance i: inst){
			setUnit(i);
			annotations.addAll(i.getAnnotations());
		}
		
		// set value 
		inst = getMatchingInstances(templateItem.getValues(),null);
		if(inst.isEmpty())
			inst = getMatchingInstances(templateItem.getValues(),r);
		for(ItemInstance i: inst){
			filterValues(i,annotations);
			for(Annotation a: i.getAnnotations()){
				setValue(TextTools.parseDecimalValue(a.getText()));
			}
			annotations.addAll(i.getAnnotations());
		}
		
		// add annotations
		if(!annotations.isEmpty()){
			String txt = getConcept().getSearchString();
			Annotation a = getAnnotations().isEmpty()?null:getAnnotations().get(0);
			int offs = 0;
			if(a != null)
				offs = a.getOffset()-txt.length();
			offs = doc.getText().indexOf(txt,offs);
			if(offs > -1){
				for(Annotation b: annotations){
					if(b.getOffset() < txt.length()) //offs
						b.updateOffset(offs);
					if(!getAnnotations().contains(b))
						getAnnotations().add(b);
				}
			}
		}
		//System.out.println(getQuestion()+" instance: "+concept.getName()+" : feature: "+feature+" attr: "+attributeValues+" units: "+unit+" value: "+value);
	}

	/**
	 * filter numeric values if they fit some criteria
	 * @param inst
	 * @param annotations2
	 * @return
	 */
	private void filterValues(ItemInstance item, List<Annotation> anat) {
		// remove annotations that happen to be part of other annotations
		// Ex: annotations: 6 and 10 where 10 is part of per 10 hpf
		for(ListIterator<Annotation> it=item.getAnnotations().listIterator();it.hasNext();){
			Annotation a = it.next();
			if(anat.contains(a))
				it.remove();
		}
	}

	/**
	 * get immediate neighbors for a concept
	 * @param doc
	 * @return
	 */
	private List<Concept> getNeighbors(AnnotatedDocument doc) {
		List<Concept> r = new ArrayList<Concept>();
		List<Annotation> annotations = Arrays.asList(getConcept().getAnnotations());
		final int WINDOW = 4;
		int st = -1, en = -1;
		for(int i=0;i<doc.getAnnotations().size();i++){
			Annotation a = doc.getAnnotations().get(i);
			if(annotations.contains(a)){
				if(st == -1)
					st = i;
			}else if(st > -1){
				en = i;
				break;
			}
		}
		// now that we have the range
		if(st > -1){
			Map<Integer,Integer> offsets = new LinkedHashMap<Integer,Integer>();
			offsets.put(st-WINDOW,st);
			if(en > -1)
				offsets.put(en,en+WINDOW);
			
			for(int off: offsets.keySet()){
				for(int i=off;i>=0 && i<offsets.get(off) && i< doc.getAnnotations().size();i++){
					Annotation a = doc.getAnnotations().get(i);
					Concept c = a.getConcept();
					if(r.contains(c)){
						for(Concept b: r){
							if(!Arrays.asList(b.getAnnotations()).contains(a)){
								r.add(c);
								break;
							}
						}
					}else{
						r.add(c);
					}
				}
			}
		}
		
		
		return r;
	}
	
	
	/**
	 * get matching instances
	 * @param items
	 * @param r - optional list of neighbors
	 * @return
	 */
	private List<ItemInstance> getMatchingInstances(Collection<TemplateItem> items, List<Concept> r){
		// make sure you don't add one item which is part of another
		List<ItemInstance> result = new ArrayList<ItemInstance>(){
			public boolean add(ItemInstance e) {
				// check if previous content subsumes or is subsumed by new entry
				for(ListIterator<ItemInstance> it = listIterator();it.hasNext();){
					ItemInstance in = it.next();
					// existing entry subsumes new entry
					if(in.getAnnotations().containsAll(e.getAnnotations())){
						return false;
					// new entry subsumes existing entry	
					}else if(e.getAnnotations().containsAll(in.getAnnotations())){
						it.remove();
					}
				}
				return super.add(e);
			}
			
		};
		for(TemplateItem mod: items){
			Concept c = (r == null)?findConcept(mod):findConcept(r,mod);
			if(c != null){
				result.add(new ItemInstance(mod, c));
			}
		}
		return result;
	}

	/**
	 * merge item instances (if one is more general/specific then other)
	 * @param o
	 */
	public void merge(ItemInstance o) {
		getAnnotations().addAll(o.getAnnotations());
	}

	
	/**
	 * does concept contain other concept
	 * @param out - 
	 * @param s
	 * @return
	 */
	private Concept findConcept(List<Concept> r, TemplateItem in){
		for(Concept c: r ){
			if(c.equals(in.getConcept()) || in.getPathHelper().hasAncestor(in.getConcept(),c))
				return c;
		}
		return null;
	}
	
	/**
	 * does concept contain other concept
	 * @param out - 
	 * @param s
	 * @return
	 */
	private Concept findConcept(TemplateItem in){
		Concept c = in.getConcept();
		try{
			IndexFinderTerminology term = new IndexFinderTerminology();
			term.setIgnoreSmallWords(false);
			term.setScoreConcepts(false);
			term.setSelectBestCandidate(false);
			term.setIgnoreUsedWords(true);
			term.setCachingEnabled(false);
			term.addConcept(c);
			
			for(Concept rc: term.search(getConcept().getSearchString())){
				rc.setTerminology(c.getTerminology());
				return rc;
			}
		}catch(TerminologyException ex){
			//ex.printStackTrace();
			
		}
		/*
		c.setSearchString(getConcept().getSearchString());
		searchRegExp(c);
		if(c.getAnnotations().length > 0){
			for(Annotation a: c.getAnnotations()){
				System.out.println(c.getSearchString()+" | "+a);
			}
			return c;
		}
		*/
		return null;
	}
	
		
	/**
	 * search through regular expressions
	 * @param text
	 * @return
	 *
	private void searchRegExp(Concept c){
		String term = c.getSearchString();
		
		// create regex map
		Set<String> regexMap = new HashSet<String>();
		for(String s: c.getSynonyms()){
			if(s != null && s.startsWith("/") && s.endsWith("/")){
				regexMap.add("\\b("+s.substring(1,s.length()-1)+")\\b");
			}
		}
		
		term = new String(term);
		List<Annotation> result = new ArrayList<Annotation>(){
			public boolean add(Annotation e) {
				for(ListIterator<Annotation> it = listIterator();it.hasNext();){
					Annotation b = it.next();
					
					// get offsets of concepts
					int st = e.getOffset();
					int en = e.getOffset()+e.getText().length();
					
					int stb = b.getOffset();
					int enb = b.getOffset()+b.getText().length();
					
					// if concept b (previous concept) is within concept c (new concept)
					if(st <=  stb && enb <= en){
						it.remove();
						return super.add(e);
					// if new concept is witing existing, dont' add
					}else if(stb <=  st && en <= enb){
						return false;
					}
				}
				return super.add(e);
			}
			
		};
		
		// iterate over expression
		for(String re: regexMap){
			// match regexp from file to
			Pattern p = Pattern.compile(re,Pattern.CASE_INSENSITIVE);
			Matcher m = p.matcher( term );
			while ( m.find() ){
				String txt = m.group(1);    // THIS BETTER BE THERE,
				//Annotation.addAnnotation(c, txt,m.start());
				Annotation a = new Annotation();
				a.setText(txt);
				a.setOffset(m.start());
				result.add(a);
			}
		}
		if(!result.isEmpty()){
			for(Annotation a: result){
				Annotation.addAnnotation(c,a.getText(),a.getOffset());
			}
		}
	}
	*/
	
	public String toString(){
		return concept.getName();
	}
	
	/**
	 * compare to other template item
	 */
	public int compareTo(Object o) {
		return getConcept().compareTo(((ItemInstance)o).getConcept());
	}

	public int hashCode() {
		return getConcept().hashCode();
	}

	public boolean equals(Object obj) {
		return getConcept().equals(((ItemInstance)obj).getConcept());
	}
	
	
}
