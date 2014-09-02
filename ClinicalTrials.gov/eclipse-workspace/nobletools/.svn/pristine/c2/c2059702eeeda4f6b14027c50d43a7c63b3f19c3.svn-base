package edu.pitt.ontology.protege;

import java.util.ArrayList;
import java.util.Collection;
import java.util.List;

import edu.pitt.ontology.IClass;
import edu.pitt.ontology.IInstance;
import edu.pitt.ontology.ILogicExpression;
import edu.pitt.ontology.IOntology;
import edu.pitt.ontology.IProperty;
import edu.pitt.ontology.IRestriction;
import edu.pitt.ontology.LogicExpression;
import edu.pitt.terminology.lexicon.Concept;
import edu.pitt.terminology.lexicon.Definition;
import edu.stanford.smi.protegex.owl.model.OWLAnonymousClass;
import edu.stanford.smi.protegex.owl.model.OWLClass;
import edu.stanford.smi.protegex.owl.model.OWLComplementClass;
import edu.stanford.smi.protegex.owl.model.OWLIndividual;
import edu.stanford.smi.protegex.owl.model.OWLIntersectionClass;
import edu.stanford.smi.protegex.owl.model.OWLLogicalClass;
import edu.stanford.smi.protegex.owl.model.OWLNAryLogicalClass;
import edu.stanford.smi.protegex.owl.model.OWLNamedClass;
import edu.stanford.smi.protegex.owl.model.OWLRestriction;
import edu.stanford.smi.protegex.owl.model.OWLUnionClass;
import edu.stanford.smi.protegex.owl.model.RDFList;
import edu.stanford.smi.protegex.owl.model.RDFProperty;
import edu.stanford.smi.protegex.owl.model.RDFSClass;

public class PClass extends PResource implements IClass {
	private Concept concept;
	private RDFSClass cls;
	
	public PClass(RDFSClass c, IOntology o){
		super(c,o);
		this.cls = c;
	}
	
	/**
	 * get appropriate resource from IClass
	 * @param a
	 * @return
	 */
	private final RDFSClass getResource(IClass a){
		return (RDFSClass)((PClass)a).getResource();
	}
	
	/**
	 * add disjoint class 
	 */
	public void addDisjointClass(IClass a) {
		if(cls instanceof OWLNamedClass)
			((OWLNamedClass)cls).addDisjointClass(getResource(a));
	}

	/**
	 * remove equivalent 
	 * @param parent
	 * @param child
	 */
	public void addEquivalentClass(IClass a){
		if(cls instanceof OWLNamedClass)
			((OWLNamedClass)cls).addEquivalentClass(getResource(a));
	}
	
	/**
	 * add direct subclass
	 */
	public void addSubClass(IClass child) {
		child.addSuperClass(this);
	}

	/**
	 * add direct superclass
	 */
	public void addSuperClass(IClass parent) {
		cls.addSuperclass(getResource(parent));
	}
	
	/**
	 * add restriction
	 */
	public void addNecessaryRestriction(IRestriction res) {
		if(cls instanceof OWLNamedClass)
			((OWLNamedClass)cls).addSuperclass(getResource(res));
	}

	/**
	 * remove restriction
	 */
	public void removeNecessaryRestriction(IRestriction res) {
		if(cls instanceof OWLNamedClass){
			RDFSClass r = getResource(res);
			// if this restriction is attached to more then one class
			// then try just to remove its parent status
			// else simply remove it
			if(r.getSubclassCount() > 1){
				RDFSClass clone = r.createClone();
				// re-add clone to subclasses
				for(Object c : r.getSubclasses(false)){
					if(c instanceof OWLNamedClass && !c.equals(cls)){
						((OWLNamedClass)c).addSuperclass(clone);
					}
				}
			}
			((OWLNamedClass)cls).removeSuperclass(r);
		}
	}
	
	
	/**
	 * get a necessary and sufficient restriction class
	 * @return
	 */
	private OWLAnonymousClass [] getEquivalentRestrictionClasses(){
		if(cls instanceof OWLNamedClass){
			List<OWLAnonymousClass> list = new ArrayList<OWLAnonymousClass>();
			for(Object obj: ((OWLNamedClass)cls).getEquivalentClasses()){
				RDFSClass cls = (RDFSClass) obj;
				if(cls instanceof OWLAnonymousClass)
					list.add((OWLAnonymousClass)cls);
			}
			return list.toArray(new OWLAnonymousClass [0]);
		}
		return null;
	}
	
	/**
	 * add restriction
	 */
	public void addEquivalentRestriction(IRestriction res) {
		if(cls instanceof OWLNamedClass){
			// see if there are already necessary and sufficient restrictions
			OWLAnonymousClass [] eq = getEquivalentRestrictionClasses();
			// if there aren't any add this restriction as equivalence class
			if(eq == null || eq.length == 0){
				OWLIntersectionClass ic = cls.getOWLModel().createOWLIntersectionClass();
				ic.addOperand(getResource(res));
				((OWLNamedClass)cls).addEquivalentClass(ic);
			// if there are some, make a union of them
			}else {
				// try to find intersection class and add to it
				for(int i=0;i<eq.length;i++){
					if(eq[i] instanceof OWLIntersectionClass){
						((OWLIntersectionClass)eq[i]).addOperand(getResource(res));
						return;
					}
				}
				// if we cant find intersection, lets make an intersection with
				// existing restrictions
				OWLIntersectionClass in = cls.getOWLModel().createOWLIntersectionClass();
				for(int i=0;i<eq.length;i++){
					in.addOperand(eq[i].createClone());
					((OWLNamedClass)cls).removeEquivalentClass(eq[i]);
				}
				in.addOperand(getResource(res));
				((OWLNamedClass)cls).addEquivalentClass(in);
			}
		}
	}

	/**
	 * remove restriction
	 */
	public void removeEquivalentRestriction(IRestriction res) {
		if(cls instanceof OWLNamedClass){
			// see if there are already necessary and sufficient restrictions
			OWLAnonymousClass [] eq = getEquivalentRestrictionClasses();
			if(eq != null ){
				for(int i=0;i<eq.length;i++){
					if(eq[i] instanceof OWLNAryLogicalClass){
						((OWLNAryLogicalClass)eq[i]).removeOperand(getResource(res));
						// remove empty expressions
						if(((OWLNAryLogicalClass)eq[i]).getOperands().isEmpty()){
							((OWLNamedClass)cls).removeEquivalentClass(eq[i]);
						}
					}else if (eq[i] instanceof OWLRestriction){
						((OWLNamedClass)cls).removeEquivalentClass(eq[i]);
					}
				}
			}
		}
	}
	
	/**
	 * remove subclass 
	 * @param parent
	 * @param child
	 */
	public void removeSubClass(IClass child){
		child.removeSuperClass(this);
	}
	
	/**
	 * remove subclass 
	 * @param parent
	 * @param child
	 */
	public void removeSuperClass(IClass parent){
		cls.removeSuperclass(getResource(parent));
	}
	
	
	/**
	 * remove disjoint 
	 * @param parent
	 * @param child
	 */
	public void removeDisjointClass(IClass a){
		if(cls instanceof OWLNamedClass)
			((OWLNamedClass)cls).removeDisjointClass(getResource(a));
	}
	

	/**
	 * remove equivalent 
	 * @param parent
	 * @param child
	 */
	public void removeEquivalentClass(IClass a){
		if(cls instanceof OWLNamedClass)
			((OWLNamedClass)cls).removeEquivalentClass(getResource(a));
	}
	
	
	/**
	 * create concept
	 */
	public Concept getConcept() {
		if(concept == null){
			concept = ontology.getConcept(this);
		}
		return concept;
	}

	/**
	 * get concept definitions
	 * @return
	 *
	private String [] getSynonyms(IClass [] com){
		String [] d = new String[com.length];
		for(int i=0;i<d.length;i++){
			String name = com[i].getName();
			if(name.startsWith(getPrefix()))
				name = name.substring(getPrefix().length());
			d[i] = name.replaceAll("_"," ").toLowerCase();
		}
		return d;
	}
	*/
	/**
	 * get concept definitions
	 * @return
	 */
	private Definition [] getDefinitions(){
		String [] com = getComments();
		Definition [] d = new Definition[com.length];
		for(int i=0;i<d.length;i++)
			d[i] = new Definition(com[i]);
		return d;
	}
	
	/**
	 * create instance of this class
	 * @param name
	 */
	public IInstance createInstance(String name){
		return new PInstance((OWLIndividual)cls.createInstance(name),getOntology());
	}
	
	/**
	 * create instance of this class
	 * @param name
	 */
	public IInstance createInstance(){
		return createInstance(null);
	}
	
	/**
	 * create subclass of this class
	 */
	public IClass createSubClass(String name){
		if(cls instanceof OWLNamedClass){
			return new PClass((RDFSClass)cls.getOWLModel().
					createOWLNamedSubclass(name,(OWLNamedClass)cls),getOntology());
		}
		return null;
	}
	
	
	/**
	 * get direct instances
	 */
	private IInstance[] getInstances(boolean b) {
		Object [] o = convertGetValues(cls.getInstances(b));
		if(o.length > 0 && o instanceof IInstance [])
			return (IInstance [])o;
		return new IInstance [0];
	}


		
	/**
	 * get all instances including subclasses
	 */
	public IInstance[] getInstances() {
		return getInstances(true);
	}
	
	/**
	 * get direct instances of this class
	 */
	public IInstance[] getDirectInstances(){
		return getInstances(false);
	}
	

	/**
	 * get direct non anynous subclasses
	 */
	public IClass[] getDirectSubClasses() {
		return getClasses(cls.getNamedSubclasses(false));
	}

	public IClass[] getDirectSuperClasses() {
		return getClasses(cls.getNamedSuperclasses(false));
	}

	public IClass[] getSubClasses() {
		return getClasses(cls.getNamedSubclasses(true));
	}

	public IClass[] getSuperClasses() {
		return getClasses(cls.getNamedSuperclasses(true));
	}

	public boolean hasSubClass(IClass child) {
		//return ((OWLClass)((PClass)child).getResource()).hasSuperclass(cls);
		return child.hasSuperClass(this);
	}

	public boolean hasSuperClass(IClass parent) {
		return cls.hasSuperclass((OWLClass)((PClass)parent).getResource());
	}
	
	/**
	 * is child a sub class of parent
	 * @param child
	 * @return
	 */
	public boolean hasEquivalentClass(IClass child){
		//return cls.hasEquivalentClass((OWLClass)((PClass)child).getResource());
		return cls.hasEquivalentClass(getResource(child));
	}
	
	
	public boolean hasDirectSuperClass(IClass parent){
		return cls.isSubclassOf((OWLClass) convertSetValue(parent));
	}
	
	public boolean hasDirectSubClass(IClass child){
		return ((OWLClass)convertSetValue(child)).isSubclassOf(cls);
	}
	
	
	public boolean isAnonymous() {
		return cls.isAnonymous();
	}

		
	public boolean hasDisjointClass(IClass a) {
		return ((OWLNamedClass)cls).getDisjointClasses().contains(((PClass)a).getResource());
	}

	
	public IClass[] getDisjointClasses() {
		if(cls instanceof OWLNamedClass)
			return getClasses(((OWLNamedClass)cls).getDisjointClasses());
		return null;
	}
	
	/**
	 * get equivalent classes of a given class
	 * @param a
	 * @return
	 */
	public IClass [] getEquivalentClasses(){
		if(cls instanceof OWLNamedClass){
			return getClasses(((OWLNamedClass)cls).getEquivalentClasses());
		}
		return null;
	}
	
	/**
	 * get all restrictions associated with a given class
	 * @return
	 *
	public IRestriction[] getRestrictions() {
		if(cls instanceof OWLNamedClass){
			
			System.out.println("RESTRICTIONS OF "+this);
			for(Object o: ((OWLNamedClass) cls).getRestrictions(true)){
				RDFSClass c = (RDFSClass) o;
				System.out.println(c.getBrowserText()+" "+c.getClass().getName());
			}
			System.out.println("SUPERCLASSES OF "+this);
			for(Object o: ((OWLNamedClass) cls).getSuperclasses(true)){
				RDFSClass c = (RDFSClass) o;
				System.out.println(c.getBrowserText()+" "+c.isSystem());
			}
			System.out.println("EQUIVALENT OF "+this);
			for(Object o: ((OWLNamedClass) cls).getEquivalentClasses()){
				RDFSClass c = (RDFSClass) o;
				System.out.println(c.getBrowserText()+" "+c.getClass().getName());
			}
			System.out.println("");
			return getRestriction(((OWLNamedClass)cls).getRestrictions(true));
		}
		return null;
	}
	*/
	/**
	 * get direct restrictions associated with a given class
	 * @return
	 */
	public ILogicExpression getNecessaryRestrictions(){
		ILogicExpression exp = new LogicExpression(ILogicExpression.AND);
		if(cls instanceof OWLNamedClass){
			Collection list = cls.getEquivalentClasses();
			for(Object o: ((OWLNamedClass) cls).getSuperclasses(true)){
				RDFSClass c = (RDFSClass) o;
				if(c.isAnonymous() && !list.contains(c)){
					exp.add(convertParameter(c));
				}
			}
		}
		return exp;
	}

	/**
	 * get direct restrictions associated with a given class
	 * @return
	 */
	public ILogicExpression getEquivalentRestrictions(){
		ILogicExpression exp = ontology.createLogicExpression();
		exp.setExpressionType(ILogicExpression.AND);
		if(cls instanceof OWLNamedClass){
			ArrayList<PClass> list = new ArrayList<PClass>();
			// get list of anonymous classes
			for(IClass cls : getEquivalentClasses()){
				if(cls.isAnonymous())
					list.add((PClass)cls);
			}
			// if we have just one anonymous class that is an expression
			// return it, else build our own expression from what we've got
			if(list.size() == 1 && list.get(0).getResource() instanceof OWLLogicalClass){
				return list.get(0).getLogicExpression();
			}else{
				// else we've got several equivalent expressions that should be ANDed
				for(PClass pc : list){
					if(pc.isAnonymous()){
						if(pc.getResource() instanceof OWLRestriction){
							exp.add((pc instanceof IRestriction)?pc:new PRestriction((OWLRestriction)pc.getResource(),getOntology()));
						}else if(pc.getResource() instanceof OWLIntersectionClass){
							exp.addAll(pc.getLogicExpression());
						}else if(pc.getResource() instanceof OWLLogicalClass){
							exp.add(pc.getLogicExpression());
						}
					}
				}
			}
		}
		return exp;
	}
	
	/**
	 * get direct restrictions associated with a given class
	 * @return
	 */
	public ILogicExpression getDirectNecessaryRestrictions(){
		ILogicExpression exp = new LogicExpression(ILogicExpression.AND);
		if(cls instanceof OWLNamedClass){
			Collection list = cls.getEquivalentClasses();
			for(Object o: ((OWLNamedClass) cls).getSuperclasses(false)){
				RDFSClass c = (RDFSClass) o;
				if(c.isAnonymous() && !list.contains(c)){
					exp.add(convertParameter(c));
				}
			}
		}
		return exp;
	}	
	
	/**
	 * get restrictions for given property
	 */
	public IRestriction [] getRestrictions(IProperty p){
		if(cls instanceof OWLNamedClass){
			Collection c =((OWLNamedClass)cls).getRestrictions((RDFProperty)convertSetValue(p),true);
			Object [] o  = convertGetValues(c);
			return (o.length > 0)?(IRestriction [])o:new IRestriction [0];
		}
		return new IRestriction [0];
	}
	
	/**
	 * return RDFSClass as a IRestriction, IClass or ILogicExpression
	 * @param c
	 * @return
	 */
	private Object convertParameter(RDFSClass c){
		if(c instanceof OWLRestriction){
			return new PRestriction((OWLRestriction)c,getOntology());
		}else if(c instanceof OWLLogicalClass){
			return (new PClass(c,getOntology())).getLogicExpression();
		}else
			return new PClass(c,getOntology());
	}
	
	/**
	 * get this class that is encompasses as a logic expression
	 * @return
	 */
	public ILogicExpression getLogicExpression(){
		
		// if we have a union or intersection class
		if(resource instanceof OWLNAryLogicalClass){
			ILogicExpression exp = new LogicExpression(
					(resource instanceof OWLUnionClass)?ILogicExpression.OR:ILogicExpression.AND);
			for(Object c: (Collection) ((OWLNAryLogicalClass) resource).getOperands() ){
				if(c instanceof RDFSClass){
					exp.add(convertParameter((RDFSClass)c));
				}else if(c instanceof RDFList){
					RDFList l = (RDFList) c;
					System.err.println("WARNING: unexpected list "+l.getBrowserText()+" in logic expression for "+getName());
				}
			}
			return exp;
		// we might have a complement
		}else if(resource instanceof OWLComplementClass){
			RDFSClass c = ((OWLComplementClass)resource).getComplement();
			return new LogicExpression(ILogicExpression.NOT,convertParameter(c));
		}
		// default just container that contains this
		return super.getLogicExpression();
	}
	
	

	/**
	 * is this restriction satisfied for the owner of this restriction
	 * @param this could be a IClass, IInstance, IReousrceList or java object
	 */
	public boolean evaluate(Object obj){
		if(obj instanceof IInstance)
			return ((IInstance)obj).hasType(this);
		else if(obj instanceof IClass)
			return equals(obj) || hasSubClass((IClass)obj);
		return false;
	}
	
}
