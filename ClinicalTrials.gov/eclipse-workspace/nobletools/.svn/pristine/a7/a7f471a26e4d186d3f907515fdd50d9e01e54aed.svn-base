package edu.pitt.ontology.owl;


import java.util.ArrayList;
import java.util.List;


import org.semanticweb.owlapi.model.IRI;
import org.semanticweb.owlapi.model.OWLClass;
import org.semanticweb.owlapi.model.OWLClassExpression;
import org.semanticweb.owlapi.model.OWLDataFactory;
import org.semanticweb.owlapi.model.OWLEquivalentClassesAxiom;
import org.semanticweb.owlapi.model.OWLIndividual;
import org.semanticweb.owlapi.model.OWLNamedIndividual;
import org.semanticweb.owlapi.model.OWLRestriction;
import org.semanticweb.owlapi.model.OWLSubClassOfAxiom;
import org.semanticweb.owlapi.reasoner.Node;
import org.semanticweb.owlapi.reasoner.NodeSet;

import edu.pitt.ontology.IClass;
import edu.pitt.ontology.IInstance;
import edu.pitt.ontology.ILogicExpression;
import edu.pitt.ontology.IProperty;
import edu.pitt.ontology.IRestriction;
import edu.pitt.ontology.LogicExpression;
import edu.pitt.terminology.lexicon.Concept;


public class OClass extends OResource implements IClass{
	private OWLClassExpression cls;
	private transient Concept concept;
	
	protected OClass(OWLClassExpression obj,OOntology ont){
		super(obj,ont);
		cls = obj;
	}

	public OWLClass getOWLClass(){
		return (OWLClass) cls;
	}
	
	public void addSubClass(IClass child) {
		OWLClass ch = (OWLClass) convertOntologyObject(child);
		addAxiom(getOWLDataFactory().getOWLSubClassOfAxiom(ch,cls));
	}

	public void addSuperClass(IClass parent) {
		OWLClass pr = (OWLClass) convertOntologyObject(parent);
		addAxiom(getOWLDataFactory().getOWLSubClassOfAxiom(cls,pr));
	}

	public void addDisjointClass(IClass a) {
		OWLClass ca = (OWLClass) convertOntologyObject(a);
		addAxiom(getOWLDataFactory().getOWLDisjointClassesAxiom(cls,ca));
	}

	public void addEquivalentClass(IClass a) {
		OWLClass ca = (OWLClass) convertOntologyObject(a);
		addAxiom(getOWLDataFactory().getOWLEquivalentClassesAxiom(cls,ca));
	}

	public IInstance createInstance(String name) {
		OWLDataFactory dataFactory = getOWLDataFactory();
		OWLIndividual ind = dataFactory.getOWLNamedIndividual(IRI.create(getOntology().getNameSpace()+name));
		addAxiom(dataFactory.getOWLClassAssertionAxiom(cls,ind));
		return (IInstance)convertOWLObject(ind);
	}

	public IInstance createInstance() {
		OWLDataFactory dataFactory = getOWLDataFactory();
		OWLIndividual ind = dataFactory.getOWLAnonymousIndividual();
		addAxiom(dataFactory.getOWLClassAssertionAxiom(cls,ind));
		return (IInstance)convertOWLObject(ind);
	}

	public IClass createSubClass(String name) {
		OWLDataFactory dataFactory = getOWLDataFactory();
		OWLClass ch = dataFactory.getOWLClass(IRI.create(getOntology().getNameSpace()+name));
		addAxiom(getOWLDataFactory().getOWLSubClassOfAxiom(ch,cls));
		return (IClass) convertOWLObject(ch);
	}

	public void addNecessaryRestriction(IRestriction restriction) {
		OWLRestriction r = ((ORestriction)restriction).getOWLRestriction();
		OWLSubClassOfAxiom ax = getOWLDataFactory().getOWLSubClassOfAxiom(getOWLClass(),r);
	    addAxiom(ax);
	}
	public void removeNecessaryRestriction(IRestriction restriction) {
		OWLRestriction r = ((ORestriction)restriction).getOWLRestriction();
		OWLSubClassOfAxiom ax = getOWLDataFactory().getOWLSubClassOfAxiom(getOWLClass(),r);
	    removeAxiom(ax);
		
	}
	public void addEquivalentRestriction(IRestriction restriction) {
		OWLRestriction r = ((ORestriction)restriction).getOWLRestriction();
		OWLEquivalentClassesAxiom ax = getOWLDataFactory().getOWLEquivalentClassesAxiom(getOWLClass(),r);
	    addAxiom(ax);
	}
	public void removeEquivalentRestriction(IRestriction restriction) {
		OWLRestriction r = ((ORestriction)restriction).getOWLRestriction();
		OWLEquivalentClassesAxiom ax = getOWLDataFactory().getOWLEquivalentClassesAxiom(getOWLClass(),r);
	    removeAxiom(ax);
	}
	
	/**
	 * get equivalent restrictions for this class
	 */
	public ILogicExpression getEquivalentRestrictions() {
		ILogicExpression exp = getOntology().createLogicExpression();
		exp.setExpressionType(ILogicExpression.AND);
		
		for(OWLEquivalentClassesAxiom ax: getDefiningOntology().getEquivalentClassesAxioms(getOWLClass())){
			for(OWLClassExpression ex: ax.getClassExpressions()){
				if(ex.isAnonymous()){
					exp.add(convertOWLObject(ex));
				}
			}
		}
		return (exp.size() == 1 && exp.get(0) instanceof ILogicExpression)?(ILogicExpression)exp.get(0):exp;
	}

	public ILogicExpression getDirectNecessaryRestrictions() {
		ILogicExpression exp = getOntology().createLogicExpression();
		exp.setExpressionType(ILogicExpression.AND);
	    for (OWLSubClassOfAxiom ax : getDefiningOntology().getSubClassAxiomsForSubClass(getOWLClass())) {
	    	OWLClassExpression ex = ax.getSuperClass();
			if(ex.isAnonymous()){
				exp.add(convertOWLObject(ex));
			}
			
		}
		return (exp.size() == 1 && exp.get(0) instanceof ILogicExpression)?(ILogicExpression)exp.get(0):exp;
	}

	public IRestriction[] getRestrictions(IProperty p) {
		List<IRestriction> list = new ArrayList<IRestriction>();
		for(List l: new List [] {getEquivalentRestrictions(),getNecessaryRestrictions()}){
			for(Object o: l){
				if(o instanceof IRestriction){
					IRestriction r = (IRestriction)o;
					if(r.getProperty().equals(p))
						list.add(r);
				}
			}
		}
		return list.toArray(new IRestriction [0]);
	}

	/**
	 * get necessary restrictions
	 */
	public ILogicExpression getNecessaryRestrictions() {
		ILogicExpression exp = new LogicExpression(ILogicExpression.AND);
		for(Object o: getDirectNecessaryRestrictions())
			exp.add(o);
		for(IClass parent: getSuperClasses()){
			for(Object o: parent.getDirectNecessaryRestrictions())
				exp.add(o);
		}
		return exp;
	}

	public void removeSubClass(IClass child) {
		OWLClass ch = (OWLClass) convertOntologyObject(child);
		removeAxiom(getOWLDataFactory().getOWLSubClassOfAxiom(ch,cls));
	}

	public void removeSuperClass(IClass parent) {
		OWLClass pr = (OWLClass) convertOntologyObject(parent);
		removeAxiom(getOWLDataFactory().getOWLSubClassOfAxiom(cls,pr));
	}

	public void removeDisjointClass(IClass a) {
		OWLClass ca = (OWLClass) convertOntologyObject(a);
		removeAxiom(getOWLDataFactory().getOWLDisjointClassesAxiom(cls,ca));
	}

	public void removeEquivalentClass(IClass a) {
		OWLClass ca = (OWLClass) convertOntologyObject(a);
		removeAxiom(getOWLDataFactory().getOWLEquivalentClassesAxiom(cls,ca));
	}

	public IClass[] getSuperClasses() {
		NodeSet<OWLClass> sub = getOWLReasoner().getSuperClasses(cls, false);
		return getClasses(sub.getFlattened());
	}

	public IClass[] getSubClasses() {
		NodeSet<OWLClass> sub = getOWLReasoner().getSubClasses(cls, false);
		return getClasses(sub.getFlattened());
	}

	public IClass[] getDirectSuperClasses() {
		NodeSet<OWLClass> sub = getOWLReasoner().getSuperClasses(cls, true);
		return getClasses(sub.getFlattened());
	}

	public IClass[] getDirectSubClasses() {
		NodeSet<OWLClass> sub = getOWLReasoner().getSubClasses(cls, true);
		return getClasses(sub.getFlattened());
	}

	
	public IInstance[] getInstances() {
		NodeSet<OWLNamedIndividual> sub = getOWLReasoner().getInstances(cls,false);
		return getInstances(sub.getFlattened());
	}

	public IInstance[] getDirectInstances() {
		NodeSet<OWLNamedIndividual> sub = getOWLReasoner().getInstances(cls,true);
		return getInstances(sub.getFlattened());
	}

	public boolean hasSuperClass(IClass parent) {
		return getOWLReasoner().getSuperClasses(cls,false).containsEntity((OWLClass)convertOntologyObject(parent));
	}

	public boolean hasSubClass(IClass child) {
		return getOWLReasoner().getSubClasses(cls,false).containsEntity((OWLClass)convertOntologyObject(child));
	}

	public boolean hasEquivalentClass(IClass child) {
		return getOWLReasoner().getEquivalentClasses(cls).contains((OWLClass)convertOntologyObject(child));
	}

	public boolean hasDirectSuperClass(IClass parent) {
		return getOWLReasoner().getSuperClasses(cls, true).containsEntity((OWLClass)convertOntologyObject(parent));
		//return hasClass(sub.getFlattened(),parent);
	}
	
	public boolean hasDirectSubClass(IClass child) {
		return getOWLReasoner().getSubClasses(cls, true).containsEntity((OWLClass)convertOntologyObject(child));
	}

	public IClass[] getDisjointClasses() {
		NodeSet<OWLClass> sub = getOWLReasoner().getDisjointClasses(cls);
		return getClasses(sub.getFlattened());
	}

	public IClass[] getEquivalentClasses() {
		Node<OWLClass> sub = getOWLReasoner().getEquivalentClasses(cls);
		return getClasses(sub.getEntities());
	}

	public boolean hasDisjointClass(IClass a) {
		return getOWLReasoner().getDisjointClasses(cls).containsEntity((OWLClass)convertOntologyObject(a));
	}
	
	public boolean isAnonymous() {
		return cls.isAnonymous();
	}

	public Concept getConcept() {
		if(concept == null){
			concept = getOntology().getConcept(this);
		}
		return concept;
	}

	public boolean evaluate(Object obj) {
		if(obj instanceof IInstance)
			return ((IInstance)obj).hasType(this);
		else if(obj instanceof IClass)
			return equals(obj) || hasSubClass((IClass)obj);
		return false;
	}
	
}
