package edu.pitt.info.extract.model.util;


import java.net.URI;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Properties;
import java.util.Set;

import javax.swing.tree.DefaultMutableTreeNode;
import javax.swing.tree.TreeNode;
import javax.swing.tree.TreePath;

import edu.pitt.ontology.IClass;
import edu.pitt.ontology.IInstance;
import edu.pitt.ontology.ILogicExpression;
import edu.pitt.ontology.IOntology;
import edu.pitt.ontology.LogicExpression;
import edu.pitt.text.tools.TextTools;

/**
 * varies ontology related methods
 * @author tseytlin
 */
public class SlideTutorOntologyHelper {
	// report sections
	public static final String PATIENT_HISTORY = "PATIENT HISTORY";
	public static final String GROSS_DESCRIPTION = "GROSS DESCRIPTION";
	
	
	// ontology names
	public static final String EVS_TERMINOLOGY = "Enterprise Vocabulary Service";
	public static final String ONTOLOGY_TERMINOLOGY = "Ontology Terminology";
	public static final String LUCENE_TERMINOLOGY = "Lucene Terminology";
	public static final String REMOTE_TERMINOLOGY = "Remote Terminology";
	public static final String KNOWLEDGE_BASE = "KnowledgeBase.owl";
	public static final String ANATOMY_ONTOLOGY = "AnatomicalSites.owl";
	public static final String OWL_SUFFIX = ".owl";
	public static final String CASE_SUFFIX = ".case";
	public static final String TERMS_SUFFIX = ".terms";
	public static final String CONFIG_SUFFIX = ".conf";
	public static final String INSTANCES_ONTOLOGY = "Instances"+OWL_SUFFIX;
	public static final String EXAMPLES_FOLDER = "examples";
	public static final String CASES_FOLDER = "cases";
	public static final String SPREADSHEET_FOLDER = "spreadsheets";
	public static final String DEFAULT_HOST_URL = "http://slidetutor.upmc.edu";
	public static final String DEFAULT_BASE_URI = "http://slidetutor.upmc.edu/curriculum/owl/";
	public static final String DEFAULT_TUTOR_HELP_FILE = "/resources/TutorHelp.xml";
	public static final String DEFAULT_REPORT_HELP_FILE = "/resources/ReportHelp.xml";
	public static final String CURRICULUM_ROOT = "curriculum";
	public static final String KNOWLEDGE_FOLDER = "owl";
	public static final String CONFIG_FOLDER = "config";
	public static final URI KNOWLEDGE_BASE_URI = URI.create(DEFAULT_BASE_URI+KNOWLEDGE_BASE);
	public static final URI ANATOMY_ONTOLOGY_URI = URI.create(DEFAULT_BASE_URI+ANATOMY_ONTOLOGY);
	public static final String DEFAULT_FILE_MANAGER_SERVLET = DEFAULT_HOST_URL+"/domainbuilder/servlet/FileManagerServlet";
	public static final double NO_VALUE = Double.MIN_VALUE;
	public static final String DEFAULT_JNLP_SERVLET = DEFAULT_HOST_URL+"/its/JNLPServlet";
	public static final String DEFAULT_CONFIG_URL = DEFAULT_HOST_URL+"/curriculum/config/";
	
	// class names
	public static final String CONCEPTS = "CONCEPTS";
	public static final String CASES = "CASES";
	public static final String SCHEMAS = "TEMPLATES";
	//public static final String LEXICON = "LEXICON";
	public static final String ACTIONS = "ACTIONS";
	public static final String WORKSHEET = "WORKSHEET";
	public static final String NUMERIC = "Number";
	public static final String PROCEDURE = "Procedure";
	public static final String ANATOMIC_LOCATION = "Anatomic_Location";
	public static final String INVOLVED = "involved";
	public static final String TISSUE = "Tissue";
	
	
	public static final String DIAGNOSES = "DIAGNOSES";
	public static final String RECOMMENDATIONS = "RECOMMENDATIONS";
	public static final String ANCILLARY_STUDIES = "ANCILLARY_STUDIES";
	public static final String DIAGNOSTIC_FEATURES = "DIAGNOSTIC_FINDINGS";
	public static final String PROGNOSTIC_FEATURES = "PROGNOSTIC_FINDINGS";
	public static final String CLINICAL_FEATURES = "CLINICAL_FINDINGS";
	public static final String ARCHITECTURAL_FEATURES = "ARCHITECTURAL_FEATURES";
	public static final String CYTOLOGIC_FEATURES = "CYTOLOGIC_FEATURES";
	
	public static final String FEATURES = "FINDINGS";
	public static final String ATTRIBUTES = "ATTRIBUTES";
	public static final String MODIFIERS = "MODIFIERS";
	public static final String LOCATIONS = "LOCATION";
	public static final String VALUES = "VALUES";
	
	public static final String ACTION_OBSERVE_ALL = "Observe_all";
	public static final String ACTION_OBSERVE_SOME = "Observe_some";
	public static final String ACTION_OBSERVE_SLIDE = "Observe_slide";
	public static final String ACTION_MEASURE_MM2   = "Measure_with_mm2";
	public static final String ACTION_MEASURE_RULER = "Measure_with_ruler";
	public static final String ACTION_MEASURE_HPF   = "Measure_with_HPF";
	public static final String ACTION_MEASURE_10HPF   = "Measure_with_10HPF";
	
	
	public static final String HAS_CLINICAL = "hasClinicalFinding";
	public static final String HAS_ANCILLARY = "hasAncillaryStudies";
	public static final String HAS_FINDING = "hasFinding";
	public static final String HAS_NO_FINDING = "hasAbsentFinding";
	public static final String HAS_PROGNOSTIC = "hasPrognostic";
	public static final String HAS_TRIGGER    = "hasTrigger";
	public static final String HAS_ACTION 	  = "hasAction";
	
	public static final String HAS_CONCEPT_CODE = "code";
	public static final String HAS_EXAMPLE = "example";
	public static final String HAS_REPORT = "hasReport";
	public static final String HAS_SLIDE = "hasImage";
	public static final String HAS_POWER = "power";
	public static final String HAS_NUMERIC_VALUE = "hasNumericValue";
	public static final String IS_ABSENT = "isAbsent";
	public static final String HAS_ORDER = "order";
	
	public static final String POWER_LOW = "low";
	public static final String POWER_MEDIUM = "medium";
	public static final String POWER_HIGH = "high";
	
	
	private static Map<IClass,IClass> featureMap;
	
	
	/**
	 * reset static resources s.a feature map
	 */
	public static void reset(){
		featureMap = null;
	}
	
	/**
	 * Get instance with given name, if it doesn't exist
	 * create it
	 * @param name
	 * @return
	 */
	public static IInstance getInstance(IClass cls, String name){
		IInstance inst = cls.getOntology().getInstance(name);
		if(inst == null)
			inst = cls.createInstance(name);
		return inst;
	}
	
	/**
	 * Get instance with given name, if it doesn't exist
	 * create it
	 * @param name
	 * @return
	 */
	public static IInstance getInstance(IClass cls){
		return getInstance(cls,cls.getName().toLowerCase());
	}
	
	/**
	 * get case base ontology from knowledge base
	 * @param ont
	 * @return
	 */
	public static String getCaseBase(String u){
		if(u.endsWith(".owl"))
			u = u.substring(0,u.length()-4);
		return u + INSTANCES_ONTOLOGY;
	}
	
	/**
	 * get concept categories
	 * @return
	 */
	public static String [] getConceptCategories(){
		return new String [] {DIAGNOSTIC_FEATURES,PROGNOSTIC_FEATURES,
						CLINICAL_FEATURES,ANCILLARY_STUDIES,DIAGNOSES,RECOMMENDATIONS};
	}
	
	
	/**
	 * get matching property for category
	 * @param category
	 * @param absent
	 * @return
	 */
	public static String getPropertyForCategory(String category,boolean absent){
		if(DIAGNOSTIC_FEATURES.equals(category)){
			return (absent)?HAS_NO_FINDING:HAS_FINDING;
		}else if(PROGNOSTIC_FEATURES.equals(category)){
			return HAS_PROGNOSTIC;
		}else if(CLINICAL_FEATURES.equals(category)){
			return (absent)?HAS_NO_FINDING:HAS_CLINICAL;
		}else if(ANCILLARY_STUDIES.equals(category)){
			return HAS_ANCILLARY;
		}	
		return null;
	}

	
	/**
	 * find a subtree in the root node and return it, based on exact match
	 * @param root
	 * @param name
	 * @return
	 */
	public static TreeNode getSubTree(TreeNode root, String name){
		// if root is what we are looking for, get it
		if((""+root).equals(name))
			return root;
		// else go into children (depth-first)
		TreeNode node = null;
		for(int i=0; i< root.getChildCount(); i++){
			node = getSubTree(root.getChildAt(i), name);
			if(node != null)
				break; 
		}
		return node;
	}
	
	/**
	 * constract tree from list of paths
	 * @param paths
	 * @return
	 */
	public static TreeNode getTree(List<TreePath> paths){
		return getTree(paths,null);
	}
	/**
	 * constract tree from list of paths
	 * @param paths
	 * @return
	 */
	public static TreeNode getTree(List<TreePath> paths, String root){
		// check for empty list
		if(paths == null || paths.isEmpty())
			return null; //new DefaultMutableTreeNode("EMPTY");
		
		// iterate over paths
		Map<String,DefaultMutableTreeNode> map = new LinkedHashMap<String,DefaultMutableTreeNode>();
		for(TreePath path: paths){
			DefaultMutableTreeNode parent = null;
			for(Object n: path.getPath()){
				DefaultMutableTreeNode node = map.get(""+n);
				if(node == null){
					node = new DefaultMutableTreeNode(""+n);
					map.put(""+n,node);
				}
				// add as child to parent
				if(parent != null)
					parent.add(node);
				parent = node;
			}
		}
		// the root should be the very first entry in linked table
		return (map.containsKey(root))?map.get(root):map.get(map.keySet().iterator().next());
	}
	
	
	/**
	 * get default image folder for domain builder
	 * @return
	 */
	public static String getDomainFromCase(String problem){
		String domain = problem;
		domain = domain.replaceAll("/"+CASES_FOLDER+"/","/"+KNOWLEDGE_FOLDER+"/");
		int i = domain.lastIndexOf("/");
		if(i > -1){
			domain = domain.substring(0,i);
		}
		return domain+OWL_SUFFIX;
	}
	
	
	/**
	 * get default image folder for domain builder
	 * @return
	 */
	public static String getCasePath(URI uri){
		String path = uri.getPath();
		// strip the owl suffix
		if(path.endsWith(OWL_SUFFIX))
			path = path.substring(0,path.length()-OWL_SUFFIX.length());
		
		// replace /owl/ with /CASE/
		path = path.replaceAll("/"+KNOWLEDGE_FOLDER+"/","/"+CASES_FOLDER+"/");
		
		// replace /domainbuilder/ with /curriculum/
		// for backword compatibility
		//path = path.replaceAll("/domainbuilder/","/curriculum/");
		
		return path;
	}
	
	
	/**
	 * get default image folder for domain builder
	 * @return
	 */
	public static String getCasePath(IOntology ont){
		return getCasePath(ont.getURI());
	}
	
	/**
	 * get default image folder for domain builder
	 * @return
	 */
	public static String getSpreadsheetPath(IOntology ont){
		String path = ont.getURI().getPath();
		// strip the owl suffix
		if(path.endsWith(ont.getName()))
			path = path.substring(0,path.length()-ont.getName().length());
		
		// replace /owl/ with /CASE/
		path = path.replaceAll("/"+KNOWLEDGE_FOLDER+"/","/"+SPREADSHEET_FOLDER+"/");
		
		// replace /domainbuilder/ with /curriculum/
		// for backword compatibility
		//path = path.replaceAll("/domainbuilder/","/curriculum/");
		
		return path;
	}
	
	/**
	 * get default image folder for domain builder
	 * @return
	 */
	public static String getExamplePath(IOntology ont){
		String path = ont.getURI().getPath();
		// strip the owl suffix
		if(path.endsWith(OWL_SUFFIX))
			path = path.substring(0,path.length()-OWL_SUFFIX.length());
		
		// replace /owl/ with /CASE/
		path = path.replaceAll("/"+KNOWLEDGE_FOLDER+"/","/"+EXAMPLES_FOLDER+"/");
		
		// replace /domainbuilder/ with /curriculum/
		// for backword compatibility
		//path = path.replaceAll("/domainbuilder/","/curriculum/");
		
		return path;
	}
	
	
	/**
	 * get relational distance between two classes
	 * if c1 is a direct parent of c2 then distance is 1
	 * if c1 == c2 distance is 0
	 * if c1 is not related to c2, then answer is max int
	 * @param c1
	 * @param c2
	 * @return
	 */
	public static int getDistance(IClass c1, IClass c2){
		if(c1.equals(c2))
			return 0;
		
		// check if c2 is a child of c1
		if(c1.hasSubClass(c2)){
			for(IClass c: c2.getDirectSuperClasses())
				if(c1.equals(c) || c1.hasSubClass(c))
					return 1 + getDistance(c1, c);
		}
		
		// check if c2 is a parent of c1
		if(c1.hasSuperClass(c2)){
			for(IClass c: c1.getDirectSuperClasses())
				if(c2.equals(c) || c2.hasSubClass(c))
					return 1 + getDistance(c,c2);
		}
		
		return Integer.MAX_VALUE;
	}
	
	
	/**
	 * convert power to integer
	 * @param pow
	 * @return
	 */
	public static int powerToInteger(String pow){
		if(POWER_LOW.equalsIgnoreCase(pow)){
			return 1;
		}else if(POWER_MEDIUM.equalsIgnoreCase(pow)){
			return 2;
		}else if(POWER_HIGH.equalsIgnoreCase(pow)){
			return 3;
		}
		return 0;
	}
	
	
	
	/**
	 * is something a knowledge base class
	 * @param cls
	 * @return
	 */
	public static boolean isSystemClass(IClass cls){
		return cls != null && cls.getNameSpace().contains(KNOWLEDGE_BASE);
	}
	
	
	/**
	 * is something an attribute?
	 * @param c
	 * @return
	 */
	public static boolean isAttribute(IClass c){
		return isOfParent(c,ATTRIBUTES);
	}
	
	
	
	
	/**
	 * is something an attribute?
	 * @param c
	 * @return
	 */
	public static boolean isModifier(IClass c){
		return isOfParent(c,MODIFIERS);
	}
	
	/**
	 * is something an attribute?
	 * @param c
	 * @return
	 */
	public static boolean isValue(IClass c){
		return (isOfParent(c,VALUES) && !NUMERIC.equals(c.getName())) && !isFeature(c);
	}
	
	/**
	 * is something an attribute?
	 * @param c
	 * @return
	 */
	public static boolean isNumber(IClass c){
		return (NUMERIC.equals(c.getName()) || isOfParent(c,NUMERIC)) && !isFeature(c);
	}
	

	/**
	 * is something an attribute?
	 * @param c
	 * @return
	 */
	public static boolean isAnatomicLocation(IClass c){
		return ANATOMIC_LOCATION.equals(c.getName()) || isOfParent(c,ANATOMIC_LOCATION);
	}
	
	/**
	 * is something an attribute?
	 * @param c
	 * @return
	 */
	public static boolean isWorksheet(IClass c){
		return isOfParent(c,WORKSHEET);
	}
	
	/**
	 * is something an attribute?
	 * @param c
	 * @return
	 */
	public static boolean isHeader(IClass c){
		return c != null && c.hasDirectSuperClass(c.getOntology().getClass(PROGNOSTIC_FEATURES)) && isSystemClass(c);
	}
	
	/**
	 * is something a location
	 * @param c
	 * @return
	 */
	public static boolean isLocation(IClass c){
		return isOfParent(c,LOCATIONS);
	}
	
	/**
	 * is something a location
	 * @param c
	 * @return
	 */
	public static boolean isDirectLocation(IClass c){
		return c.hasDirectSuperClass(c.getOntology().getClass(LOCATIONS));
	}
	
	
	/**
	 * check if this entry is a feature NOTE that FAVs are also features
	 * @return
	 */
	public static boolean isFeature(IClass c){
		return isOfParent(c,FEATURES);
	}
	
	
	
	/**
	 * check if this entry is a feature
	 * @return
	 */
	public static boolean isDisease(IClass c){
		return isOfParent(c,DIAGNOSES);
	}
	
	/**
	 * check if this entry is a feature
	 * @return
	 */
	public static boolean isDiagnosticFeature(IClass cls){
		return isOfParent(cls,DIAGNOSTIC_FEATURES);
	}
	
	/**
	 * check if this entry is a feature
	 * @return
	 */
	public static boolean isArchitecturalFeature(IClass cls){
		return isOfParent(cls,ARCHITECTURAL_FEATURES);
	}
	
	/**
	 * check if this entry is a feature
	 * @return
	 */
	public static boolean isCytologicFeature(IClass cls){
		return isOfParent(cls,CYTOLOGIC_FEATURES);
	}
	
	/**
	 * check if this entry is a feature
	 * @return
	 */
	public static boolean isPrognosticFeature(IClass cls){
		return isOfParent(cls,PROGNOSTIC_FEATURES);
	}
	
	/**
	 * check if this entry is a feature
	 * @return
	 */
	public static boolean isClinicalFeature(IClass cls){
		return isOfParent(cls,CLINICAL_FEATURES);
	}
	
	
	/**
	 * check if this entry is a feature
	 * @return
	 */
	public static boolean isAncillaryStudy(IClass cls){
		return isOfParent(cls,ANCILLARY_STUDIES);
	}
	
	
	
	/**
	 * is this class an attribute category
	 * @param cls
	 * @return
	 */
	public static boolean isAttributeCategory(IClass cls){
		return isAttribute(cls) && !isDisease(cls) && cls.getName().matches("[A-Z_]+");
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
	 * is given class a feature or diagnoses, but not an attribute
	 * @param c
	 * @return
	 */
	public static boolean isNamedFeature(IClass c){
		return (isFeature(c) || isDisease(c)) && !isSystemClass(c) && (!isAttribute(c) || isLocation(c));
	}
	
	/**
	 * is given class a attribute, but not finding
	 * @param c
	 * @return
	 */
	public static boolean isNamedAttribute(IClass parent){
		return (isAttribute(parent) && (!isSystemClass(parent) || isValue(parent)) && !isAttributeCategory(parent) &&
				  (!(isFeature(parent) || isDisease(parent)) || isDirectLocation(parent)));
	}
	
	
		
	/**
	 * find a feature/disease inside a potential finding
	 * @param cls
	 * @return
	 */
	public static IClass getFeature(IClass cls){
		if(cls == null)
			return null;
		
		// init table
		if(featureMap == null)
			featureMap = new HashMap<IClass, IClass>();
		
		// short cut for a feature
		if(featureMap.containsKey(cls))
			return featureMap.get(cls);
		
		
		// feature is the class itself by default
		IClass parent = cls;
		for(IClass p: cls.getDirectSuperClasses()){
			if(SlideTutorOntologyHelper.isSystemClass(p))
				continue;
			
			// if direct super class is more general, then lets look further
			// once in a blue moon, we have a direct superclass not being in general form, but its parent is
			// Ex:  Infectious_Cause -> Bacterial_Infectious_Cause -> Actinomycotic_Infectious_Cause
			if(isFeature(p) && (isGeneralForm(p,cls,false) || isGeneralForm(getFeature(p),cls,false))){
				// reset feature if it is equal to class or it is NOT preposition
				if(parent.equals(cls) || isGeneralForm(p,cls,true))
					parent = getFeature(p);
				//break;
			}
		}
		
		// at this point we know the parent, lets save this
		featureMap.put(cls,parent);
		
		return parent;
	}
	
	/**
	 * get a list of attributes/modifiers belong to this finding
	 * @param cls
	 * @return
	 */
	public static List<IClass> getAttributes(IClass cls){
		List<IClass> list = new ArrayList<IClass>();
		
		// if feature is itself, don't bother
		IClass feature = getFeature(cls);
		if(feature.equals(cls))
			return list;
		
		for(IClass p: cls.getSuperClasses()){
			if(isNamedAttribute(p) || isNumber(p)){
				// make sure that list contains only the most specific attributes
				// we don't want four AND number appearing here
				IClass torem = null;
				for(IClass c: list){
					if(p.hasSubClass(c)){
						// do not insert a more general class
						torem = p;
					}else if(p.hasSuperClass(c)){
						// remove more general class
						torem = c;
					}
				}
				// add new item, remove old item (or itself)
				list.add(p);
				list.remove(torem);
			}
		}
		// if feature is itself an attribute, we want to exclude it
		list.remove(feature);
		
		return list;
	}

	
	/**
	 * get a list of available attributes/modifiers for a given finding
	 * @param cls
	 * @return
	 */
	public static List<IClass> getPotentialAttributes(IClass cls){
		Set<IClass> list = new LinkedHashSet<IClass>();
		IClass feature = getFeature(cls);
		for(IClass p: feature.getSubClasses()){
			if(feature.equals(getFeature(p)))
				list.addAll(getAttributes(p));
		}
		return new ArrayList<IClass>(list);
	}
	
	/**
	 * get a list of available attributes/modifiers for a given finding
	 * @param cls
	 * @return
	 */
	public static List<IClass> getPotentialTemplateAttributes(IClass cls){
		Set<IClass> list = new LinkedHashSet<IClass>();
		IClass feature = getFeature(cls);
		if(!feature.equals(cls)){
			list.addAll(getAttributes(cls));
		}
		for(IClass p: cls.getSubClasses()){
			if(feature.equals(getFeature(p)))
				list.addAll(getAttributes(p));
		}
		return new ArrayList<IClass>(list);
	}
	
	
	/**
	 * is parent a more general version of child?
	 * @param parent
	 * @param child
	 * @return
	 */
	public static boolean isGeneralForm(IClass parent, IClass child){
		return isGeneralForm(parent, child,true);
	}
	
	/**
	 * get character count from string
	 * 
	 * @param str
	 * @return
	 */
	public static int getSequenceCount(String text, String str) {
		int count = 0;
		for (int i = text.indexOf(str); i > -1; i = text.indexOf(str, i + 1)) {
			count++;
		}
		return count;
	}
	
	/**
	 * Derive prettier version of a class name
	 * 
	 * @param name
	 * @return
	 */
	public static String getTextFromName(String name) {
		// strip prefix (if available)
		int i = name.indexOf(":");
		if (i > -1) {
			name = name.substring(i + 1);
		}

		// strip suffix
		// if(name.endsWith(OntologyHelper.WORD))
		// name = name.substring(0,name.length()-OntologyHelper.WORD.length());

		// possible lowercase values to make things look prettier
		if (!name.matches("[A-Z_\\-\\'0-9]+")
				&& !name.matches("[a-z][A-Z_\\-\\'0-9]+[a-z]*"))
			name = name.toLowerCase();

		// now replace all underscores with spaces
		return name.replaceAll("_", " ");
	}
	
	/**
	 * is parent a more general version of child?
	 * @param parent
	 * @param child
	 * @return
	 */
	public static boolean isGeneralForm(IClass parent, IClass child, boolean filterPrepositionalFeature){
		// shortcut to save time
		if(child.getName().contains(parent.getName()) && !filterPrepositionalFeature){
			// number of words in child should exceed the number of words in parent
			if(getSequenceCount(child.getName(),"_") > getSequenceCount(parent.getName(),"_"))
				return true;
		}
		
		// get words from parents and children
		String [] pnames = TextTools.getWords(getTextFromName(parent.getName()));
		String [] cnames = TextTools.getWords(getTextFromName(child.getName()));
		
		// normalize words
		List<String> plist = new ArrayList<String>();
		for(String s: pnames){
			plist.add(TextTools.stem(s));
		}
		// this is a map, to make lookup constant
		Map<String,String> clist = new LinkedHashMap<String,String>();
		for(String s: cnames){
			clist.put(TextTools.stem(s),"");
		}
		
		// now check for general form
		boolean general = true;
		for(String s: plist){
			general &= clist.containsKey(s);
		}
		
		// now check for prepositions in features
		// if we have a positive match
		if(general && filterPrepositionalFeature){
			// if in front of first parent word there is a preposition
			// then this maybe a false positive
			boolean preposition = false;
			for(String c: clist.keySet()){
				if(TextTools.isPrepositionWord(c)){
					preposition = true;
				}
				
				// as soon as we have a feature (contained in parent list)
				// check preposition, if preposition is true, then false positive
				if(plist.contains(c)){
					general = !preposition;
					break;
				}
			}
		}
		
		
		return general;
	}
	
	
	/**
	 * is class described (aka has glossary description, examples, etc
	 * @param cls
	 * @return
	 */
	public static boolean isDescribed(IClass cls){
		if(cls == null)
			return false;
		
		return cls.getComments().length > 0;
	}
	
			
	/**
	 * find out which pattern does this case match
	 * @param evidence
	 * @param dpatterns
	 * @return
	 */
	public static ILogicExpression getMatchingPatterns(IClass dx, IInstance inst){
		// check for multi-pattern
		ILogicExpression result = new LogicExpression(ILogicExpression.OR);
		ILogicExpression exp = dx.getEquivalentRestrictions();
		if(exp.getExpressionType() == ILogicExpression.OR){
			for(int i=0;i<exp.size();i++){
				if(exp.get(i) instanceof ILogicExpression){
					ILogicExpression e = (ILogicExpression) exp.get(i);
					// if this pattern matches
					if(e.evaluate(inst)){
						result.add(exp.get(i));
					}
				}
			}
		}
		return result;
	}
	
	
	/**
	 * get direct parent
	 * @param c
	 * @return
	 */
	private static IClass getDirectParent(IClass c){
		// check if direct parent is already part of the rule
		IClass parent = null;
		for(IClass p: c.getDirectSuperClasses()){
			if(isDiagnosticFeature(p)){
				parent = p;
				break;
			}
		}
		return parent;
	}
	
	
	/**
	 * process a list of simple concepts and attempts to merge
	 * them into a meaningful compunt concepts
	 */
	public static List<IClass> getCommonConcepts(List<IClass> concepts){
		// compact concept list until it stops changing size
		int previousSize = 0;
		while(concepts.size() != previousSize){
			previousSize = concepts.size();
			IClass previous = null;
			for(IClass entry: new ArrayList<IClass>(concepts)){
				// check if you can merge concepts
				if(previous != null){
					//check if there is a common higher level concept
					IClass common = mergeConcepts(previous, entry,concepts);
					if(common == null){
						//if not,check if there is another higher level concept that can be 
						//constructed with components of current concept
					}else{
						entry = common;
					}
				}
				previous = entry;
			}
		}
		
		// sort that most specific concept first
		Collections.sort(concepts,new Comparator<IClass>() {
			public int compare(IClass a, IClass b) {
				return b.getName().compareTo(a.getName());
			}
		});
		return concepts;
	}
	
		
	
	/**
	 * attempt to merge two concepts
	 * @param previous
	 * @param entry
	 * @return
	 */
	private static IClass mergeConcepts(IClass pc, IClass ec, Collection<IClass> concepts){
		IClass common = getDirectCommonChild(pc,ec);
		if(common != null){
			// update list
			concepts.remove(ec);
			concepts.remove(pc);
			concepts.add(common);
			return common;
		}
		return null;
	}
	
	
	/**
	 * get common parent of two classes
	 * @param c1
	 * @param c2
	 * @return
	 */
	public static IClass getDirectCommonChild(IClass c1, IClass c2){
		// take care of base conditions
		if(c1.equals(c2))
			return c1;
		if(c1.hasDirectSubClass(c2))
			return c2;
		if(c2.hasDirectSubClass(c1))
			return c1;
		
		// check direct children
		List<IClass> c1c = Arrays.asList(c1.getDirectSubClasses());
		List<IClass> c2c = Arrays.asList(c2.getDirectSubClasses());
		for(IClass c: c1c){
			if(c2c.contains(c))
				return c;
		}
		return null;
	}
	
	/**
	 * get common parent of two classes
	 * @param c1
	 * @param c2
	 * @return
	 */
	public static List<IClass> getDirectCommonChildren(IClass c1, IClass c2){
		// take care of base conditions
		if(c1.equals(c2))
			return Collections.singletonList(c1);
		if(c1.hasDirectSubClass(c2))
			return Collections.singletonList(c2);
		if(c2.hasDirectSubClass(c1))
			return Collections.singletonList(c1);
		
		// check direct children
		List<IClass> c1c = Arrays.asList(c1.getDirectSubClasses());
		List<IClass> c2c = Arrays.asList(c2.getDirectSubClasses());
		List<IClass> result = new ArrayList<IClass>();
		for(IClass c: c1c){
			if(c2c.contains(c))
				result.add(c);
		}
		return result;
	}
	
	
	/**
	 * get direct common parent class
	 * @param c1
	 * @param c2
	 * @return
	 */
	public static IClass getDirectCommonParent(IClass c1, IClass c2){
		for(IClass p: c1.getDirectSuperClasses()){
			if(c2.hasDirectSuperClass(p))
				return p;
		}
		return null;
	}
	
	/**
	 * get common child of two classes
	 * @param c1
	 * @param c2
	 * @return
	 */
	public static IClass getCommonChild(IClass c1, IClass c2){
		// take care of base conditions
		if(c1 == null)
			return c2;
		if(c2 == null)
			return c1;
		if(c1.equals(c2))
			return c1;
		if(c1.hasSubClass(c2))
			return c2;
		if(c2.hasSubClass(c1))
			return c1;
		
		// check direct children
		List<IClass> c1c = Arrays.asList(c1.getSubClasses());
		List<IClass> c2c = Arrays.asList(c2.getSubClasses());
		
		// pick the most specific class
		List<IClass> cc = new ArrayList<IClass>();
		for(IClass c: c1c){
			if(c2c.contains(c)){
				//return c;
				cc.add(c);
			}
		}
		if(cc.size() == 1)
			return cc.get(0);
		else if(cc.size() > 1){
			IClass g = null;
			for(IClass c: cc){
				if(g == null || c.hasSubClass(g))
					g = c;
			}
			return g;
		}
		return null;
	}
	/**
	 * get the most specific common parent of two classes
	 * @param c1
	 * @param c2
	 * @return
	 */
	public static IClass getCommonParent(IClass c1, IClass c2){
		return getCommonParent(c1, c2,null);
	}
	
	/**
	 * get the most specific common parent of two classes
	 * @param c1
	 * @param c2
	 * @return
	 */
	public static IClass getCommonParent(IClass c1, IClass c2,IClass branch){
		// take care of base conditions
		if(c1.equals(c2))
			return c1;
		if(c1.hasSubClass(c2))
			return c1;
		if(c2.hasSubClass(c1))
			return c2;
		
		// if direct parents were not found, recurse further
		IClass parent = null;
		for(IClass c : c1.getDirectSuperClasses()){
			IClass p = getCommonParent(c,c2);
			// keep the most specific parent
			if(parent == null || parent.hasSubClass(p) || (branch != null && branch.hasSubClass(p)))
				parent = p;
		}
		
		return parent;
		
	}
	
	
	/**
	 * get case name query component
	 * @param name
	 * @return
	 */
	public static Properties getURLQuery(String name){
		Properties p = new Properties();
		int i = name.lastIndexOf("?");
		if(i > -1){
			String query  = name.substring(i+1);
			String [] q = query.split("&");
			for(String str: q){
				String [] s = str.split("=");
				if(s.length == 2){
					p.setProperty(s[0].trim(),s[1].trim());
				}
			}
		}
		return p;
	}
	
	/**
	 * strip the query part if available
	 * @param name
	 * @return
	 */
	public static String stripURLQuery(String name){
		if(name != null){
			// strip the query part of the name
			int i = name.lastIndexOf("?");
			if(i > -1)
				name = name.substring(0,i);
		}
		return name;
	}
			
		
	/**
	 * get ancesstors of a class
	 * @return
	 */
	public static List<IClass> getFindingAncesstors(IClass cls, List<IClass> list){
		if(isFeature(cls)){
			list.add(cls);
			if(!cls.equals(getFeature(cls))){
				List<IClass> dp = new ArrayList<IClass>();
				for(IClass p: cls.getDirectSuperClasses()){
					if(isFeature(p))
						dp.add(p);
				}
				if(dp.size() == 1)
					return getFindingAncesstors(dp.get(0),list);
				else if(dp.size() > 1){
					// best match is the one has definition
					for(IClass p: dp){
						if(p.getComments().length > 0)
							return getFindingAncesstors(p,list);
					}
					// else just return the first one
					return getFindingAncesstors(dp.get(0),list);
				}
			}
		}
		return list;
	}
}
