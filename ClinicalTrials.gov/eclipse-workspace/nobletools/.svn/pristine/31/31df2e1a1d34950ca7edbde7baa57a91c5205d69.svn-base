package edu.pitt.ontology.owl;

import java.beans.PropertyChangeListener;
import java.beans.PropertyChangeSupport;

import edu.pitt.ontology.IClass;
import edu.pitt.ontology.IInstance;
import edu.pitt.ontology.IOntology;
import edu.pitt.ontology.IOntologyException;
import edu.pitt.ontology.IReasoner;

/**
 * wraps reasoner for this ontolgoy
 * @author tseytlin
 *
 */
public class OReasoner implements IReasoner {
	private OOntology ontology;
	private PropertyChangeSupport pcs = new PropertyChangeSupport(this);
	
	public OReasoner(OOntology ont){
		this.ontology = ont;
	}
	
	@Override
	public void initialize() throws IOntologyException {
		// TODO Auto-generated method stub

	}

	@Override
	public void dispose() {
		// TODO Auto-generated method stub

	}

	public void addPropertyChangeListener(PropertyChangeListener listener) {
		pcs.addPropertyChangeListener(listener);
	}

	public void removePropertyChangeListener(PropertyChangeListener listener) {
		pcs.removePropertyChangeListener(listener);

	}
	public IOntology getOntology() {
		return ontology;
	}

	@Override
	public IResult[] computeInferredHierarchy() {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public IResult[] computeInferredTypes() {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public IResult[] computeInferredHierarchy(IClass cls) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public IResult[] computeInferredTypes(IInstance inst) {
		// TODO Auto-generated method stub
		return null;
	}
	public IClass[] getSuperClasses(IClass cls) {
		return cls.getSuperClasses();
	}
	public IClass[] getDirectSubClasses(IClass cls) {
		return cls.getDirectSubClasses();
	}

	public IClass[] getDirectSuperClasses(IClass cls) {
		return cls.getDirectSuperClasses();
	}
	public IClass[] getSubClasses(IClass cls) {
		return cls.getSubClasses();
	}

	public IClass[] getEquivalentClasses(IClass cls) {
		return cls.getEquivalentClasses();
	}
	public IInstance[] getInstances(IClass cls) {
		return cls.getInstances();
	}

	public IClass[] getTypes(IInstance inst) {
		return inst.getTypes();
	}
	public IClass[] getDirectTypes(IInstance inst) {
		return inst.getDirectTypes();
	}

}
