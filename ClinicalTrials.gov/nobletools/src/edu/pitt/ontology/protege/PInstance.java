package edu.pitt.ontology.protege;

import edu.pitt.ontology.IClass;
import edu.pitt.ontology.IInstance;
import edu.pitt.ontology.IOntology;
import edu.stanford.smi.protegex.owl.model.OWLIndividual;
import edu.stanford.smi.protegex.owl.model.RDFSClass;

public class PInstance extends PResource implements IInstance {
	private OWLIndividual inst;
	public PInstance(OWLIndividual r, IOntology o){
		super(r,o);
		this.inst = r;
	}
	
	/**
	 * add a direct type to this instance
	 * @param cls
	 */
	public void addType(IClass cls){
		//inst.addRDFType((RDFSClass)convertSetValue(cls));
		inst.addDirectType((RDFSClass)convertSetValue(cls));
	}
	
	/**
	 * remove a type from this instance
	 * @param cls
	 */
	public void removeType(IClass cls){
		//inst.removeRDFType((RDFSClass)convertSetValue(cls));
		inst.removeDirectType((RDFSClass)convertSetValue(cls));
	}
	
	
	public IClass[] getDirectTypes() {
		return getClasses(inst.getDirectTypes());
	}

	public IClass[] getTypes() {
		return getClasses(inst.getRDFTypes());
	}

	public boolean hasType(IClass cls) {
		//return inst.hasRDFType((RDFSClass)((PClass)cls).getResource());
		return inst.hasType((RDFSClass)convertSetValue(cls));
	}
}
