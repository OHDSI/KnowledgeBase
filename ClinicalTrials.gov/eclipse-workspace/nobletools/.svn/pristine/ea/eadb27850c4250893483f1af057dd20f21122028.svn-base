package edu.pitt.ontology.owl;

import org.semanticweb.owlapi.model.IRI;
import org.semanticweb.owlapi.model.OWLClass;
import org.semanticweb.owlapi.model.OWLDataFactory;
import org.semanticweb.owlapi.model.OWLIndividual;
import org.semanticweb.owlapi.model.OWLNamedIndividual;
import org.semanticweb.owlapi.reasoner.Node;
import org.semanticweb.owlapi.reasoner.NodeSet;

import edu.pitt.ontology.IClass;
import edu.pitt.ontology.IInstance;
import edu.pitt.ontology.ILogicExpression;
import edu.pitt.ontology.IProperty;
import edu.pitt.ontology.IRestriction;
import edu.pitt.terminology.lexicon.Concept;


public class OClass extends OResource implements IClass{
	private OWLClass cls;
	private transient Concept concept;
	
	protected OClass(OWLClass obj,OOntology ont){
		super(obj,ont);
		cls = obj;
	}

	public OWLClass getOWLClass(){
		return cls;
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
		OWLIndividual ind = dataFactory.getOWLNamedIndividual(IRI.create(getNameSpace()+name));
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
		OWLClass ch = dataFactory.getOWLClass(IRI.create(getNameSpace()+name));
		addAxiom(getOWLDataFactory().getOWLSubClassOfAxiom(ch,cls));
		return (IClass) convertOWLObject(ch);
	}

	@Override
	public void addNecessaryRestriction(IRestriction restriction) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void removeNecessaryRestriction(IRestriction restriction) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void addEquivalentRestriction(IRestriction restriction) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void removeEquivalentRestriction(IRestriction restriction) {
		// TODO Auto-generated method stub
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

	@Override
	public ILogicExpression getEquivalentRestrictions() {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public ILogicExpression getDirectNecessaryRestrictions() {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public IRestriction[] getRestrictions(IProperty p) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public ILogicExpression getNecessaryRestrictions() {
		// TODO Auto-generated method stub
		return null;
	}

	public boolean hasSuperClass(IClass parent) {
		/*OWLClass c = (OWLClass) convertOntologyObject(parent);
		OWLAxiom a = getOWLDataFactory().getOWLSubClassOfAxiom(cls,c);
		return getOWLReasoner().isEntailed(a);*/
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
