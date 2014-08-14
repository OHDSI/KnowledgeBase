package edu.pitt.ontology.protege;

import java.beans.PropertyChangeListener;
import java.beans.PropertyChangeSupport;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.Iterator;
import java.util.List;

import edu.pitt.ontology.IClass;
import edu.pitt.ontology.IInstance;
import edu.pitt.ontology.IOntology;
import edu.pitt.ontology.IOntologyError;
import edu.pitt.ontology.IOntologyException;
import edu.pitt.ontology.IReasoner;
import edu.pitt.ontology.IReasoner.IResult;
import edu.pitt.ontology.IResource;
import edu.stanford.smi.protegex.owl.inference.protegeowl.ReasonerManager;
import edu.stanford.smi.protegex.owl.inference.protegeowl.task.ReasonerTaskEvent;
import edu.stanford.smi.protegex.owl.inference.protegeowl.task.ReasonerTaskListener;
import edu.stanford.smi.protegex.owl.inference.reasoner.ProtegeReasoner;
import edu.stanford.smi.protegex.owl.inference.reasoner.exception.ProtegeReasonerException;
import edu.stanford.smi.protegex.owl.model.OWLClass;
import edu.stanford.smi.protegex.owl.model.OWLIndividual;
import edu.stanford.smi.protegex.owl.model.OWLNamedClass;
import edu.stanford.smi.protegex.owl.model.RDFSNamedClass;

public class PReasoner implements IReasoner {
	private final String DEFAULT_REASONER = 
	"edu.stanford.smi.protegex.owl.inference.pellet.ProtegePelletOWLAPIReasoner";
	private ProtegeReasoner reasoner;
	private POntology ontology;
	private PropertyChangeSupport pcs = new PropertyChangeSupport(this);
	private ReasonerTaskListener taskListener;
	
	/**
	 * initialize this reasoner
	 * @param ont
	 */
	public PReasoner(POntology ont){
		this.ontology = ont;
	}
	
	
	/**
	 * initialize this reasoner
	 * @return
	 */
	public void initialize() throws IOntologyException {
		String reasonerClass = 
			System.getProperty("reasoner.class",DEFAULT_REASONER);
		try{
			ReasonerManager manager = ReasonerManager.getInstance();
			reasoner = manager.setProtegeReasonerClass(ontology.getModel(),Class.forName(reasonerClass));
			reasoner.initialize();
			//reasoner.setURL("http://localhost:8081");
			taskListener = new TaskListener();
			reasoner.setReasonerTaskListener(taskListener);
		}catch(Exception ex){
			throw new IOntologyException("Problem Initializing Reasoner ("+reasonerClass+")",ex);
		}
	}
	
	/**
	 * dispose of this reasoner instance
	 */
	public void dispose(){
		reasoner.dispose();
	}
	
	
	public void addPropertyChangeListener(PropertyChangeListener listener) {
		pcs.addPropertyChangeListener(listener);
	}

	
	/**
	 * NOTE: copy/pasted from Protege code ChangedClassesTableModel.java
	 * @param a
	 * @param b
	 */
    private void removeDuplicates(Collection a, Collection b) {
        Collection copyA = new ArrayList(a);
        a.removeAll(b);
        b.removeAll(copyA);
    }
	
	
    /**
     * NOTE: copy/pasted from Protege code ChangedClassesTableModel.java
     * compute result list for givent class
     * @param cls
     * @return
     */
    private Collection<IResult> computeResults(OWLNamedClass cls,Collection inferredClasses, int op){
    	if(inferredClasses.isEmpty())
    		return Collections.EMPTY_LIST;
    	
    	List<IResult> result = new ArrayList<IResult>();
		Collection asserted = new ArrayList(cls.getNamedSuperclasses());
        Collection inferred = new ArrayList(inferredClasses);
        removeDuplicates(asserted, inferred);
        for (Iterator ait = asserted.iterator(); ait.hasNext();) {
            RDFSNamedClass superCls = (RDFSNamedClass) ait.next();
            if (!superCls.isMetaclass()) {
            	result.add(new PResult(cls,IResult.REMOVE+op,superCls,ontology));
            }
        }
        for (Iterator ait = inferred.iterator(); ait.hasNext();) {
            RDFSNamedClass superCls = (RDFSNamedClass) ait.next();
            if (!superCls.isMetaclass()) {
                result.add(new PResult(cls,IResult.ADD+op,superCls,ontology));
            }
        }
        return result;
    }
    
    
	public IResult [] computeInferredHierarchy() {
		try{
			reasoner.classifyTaxonomy();
			List<IResult> result = new ArrayList<IResult>();
			
			// NOTE: copy/pasted from Protege code ChangedClassesTableModel.java
			for(Object o: ontology.getModel().getChangedInferredClasses()){
				OWLNamedClass c = (OWLNamedClass) o;
				result.addAll(computeResults(c,c.getInferredSuperclasses(),IResult.SUPERCLASS));
			}
			return result.toArray(new IResult[0]);
		}catch(ProtegeReasonerException ex){
			throw new IOntologyError("Reasoner Problem",ex);
		}
	}
	
	

	public IResult [] computeInferredTypes() {
		try{
			reasoner.computeInferredIndividualTypes();
			// NOTE: copy/pasted from Protege code ChangedClassesTableModel.java
			for(Object o: ontology.getModel().getChangedInferredClasses()){
				OWLNamedClass cls = (OWLNamedClass) o;
				System.out.println("inferred types: "+cls);
			}
		}catch(ProtegeReasonerException ex){
			throw new IOntologyError("Reasoner Problem",ex);
		}
		return new IResult [0];
	}
	
	
	/**
	 * classify the entire ontology, For each named class in the ontology, 
	 * this method queries the reasoner for the consistency of the class, 
	 * its inferred super classes and its inferred equivalent classes.
	 * Assert the result
	 */
	public IResult [] computeInferredHierarchy(IClass cls){
		try{
			OWLNamedClass  c = (OWLNamedClass)ontology.convertSetValue(cls);
			List<IResult> result = new ArrayList<IResult>();
			result.addAll(computeResults(c,reasoner.getSuperclasses(c),IResult.SUPERCLASS));
			//result.addAll(computeResults(c,reasoner.getSubclasses(c),IResult.SUBCLASS));
			return result.toArray(new IResult[0]);
		}catch(Exception ex){
			throw new IOntologyError("Reasoner Problem",ex);
		}
	}
	
	/**
	 * infer types for all individuals in ontology. Assert the result
	 */
	public IResult [] computeInferredTypes(IInstance inst){
		//TODO:
		return new IResult [0];
	}
	
	

	public IClass[] getDirectSubClasses(IClass cls) {
		try{
			Object [] o = ontology.convertGetValues(
					reasoner.getSubclasses((OWLClass)ontology.convertSetValue(cls)));
			return (o.length > 0)?(IClass [])o:new IClass[0];
		}catch(ProtegeReasonerException ex){
			throw new IOntologyError("Reasoner Problem",ex);
		}
		//return new IClass[0];
	}

	public IClass[] getDirectSuperClasses(IClass cls) {
		try{
			Object [] o = ontology.convertGetValues(
					reasoner.getSuperclasses((OWLClass)ontology.convertSetValue(cls)));
			return (o.length > 0)?(IClass [])o:new IClass[0];
		}catch(ProtegeReasonerException ex){
			throw new IOntologyError("Reasoner Problem",ex);
		}
		//return new IClass[0];
	}

	public IClass[] getEquivalentClasses(IClass cls) {
		try{
			Object [] o = ontology.convertGetValues(
					reasoner.getEquivalentClasses((OWLClass)ontology.convertSetValue(cls)));
			return (o.length > 0)?(IClass [])o:new IClass[0];
		}catch(ProtegeReasonerException ex){
			throw new IOntologyError("Reasoner Problem",ex);
		}
		//return new IClass[0];
	}

	public IInstance[] getInstances(IClass cls) {
		try{
			Object [] o = ontology.convertGetValues(
					reasoner.getIndividualsBelongingToClass((OWLClass)ontology.convertSetValue(cls)));
			return (o.length > 0)?(IInstance [])o:new IInstance[0];
		}catch(ProtegeReasonerException ex){
			throw new IOntologyError("Reasoner Problem",ex);
		}
		//return new IInstance[0];
	}

	public IClass[] getSubClasses(IClass cls) {
		try{
			Object [] o = ontology.convertGetValues(
					reasoner.getDescendantClasses((OWLClass)ontology.convertSetValue(cls)));
			return (o.length > 0)?(IClass [])o:new IClass[0];
		}catch(ProtegeReasonerException ex){
			throw new IOntologyError("Reasoner Problem",ex);
		}
		//return new IClass[0];
	}

	public IClass[] getSuperClasses(IClass cls) {
		try{
			Object [] o = ontology.convertGetValues(
					reasoner.getAncestorClasses((OWLClass)ontology.convertSetValue(cls)));
			return (o.length > 0)?(IClass [])o:new IClass[0];
		}catch(ProtegeReasonerException ex){
			throw new IOntologyError("Reasoner Problem",ex);
		}
		//return new IClass[0];
	}

	public IClass[] getTypes(IInstance inst) {
		try{
			Object [] o = ontology.convertGetValues(
					reasoner.getIndividualTypes((OWLIndividual)ontology.convertSetValue(inst)));
			return (o.length > 0)?(IClass [])o:new IClass[0];
		}catch(ProtegeReasonerException ex){
			throw new IOntologyError("Reasoner Problem",ex);
		}
		//return new IClass[0];
	}

	public IClass[] getDirectTypes(IInstance inst) {
		//TODO:
		try{
			Object [] o = ontology.convertGetValues(
					reasoner.getIndividualTypes((OWLIndividual)ontology.convertSetValue(inst)));
			return (o.length > 0)?(IClass [])o:new IClass[0];
		}catch(ProtegeReasonerException ex){
			throw new IOntologyError("Reasoner Problem",ex);
		}
		//return new IClass[0];
	}
	
	public void removePropertyChangeListener(PropertyChangeListener listener) {
		pcs.removePropertyChangeListener(listener);
	}

	public IOntology getOntology() {
		return ontology;
	}

	public String toString(){
		return reasoner.getClass().getSimpleName()+" ("+ontology.getURI()+")";
	}
	
	
	/**
	 * result class
	 * @author tseytlin
	 */
	public static class PResult implements IResult {
		private OWLNamedClass operand;
		private RDFSNamedClass param;
		private int operation;
		private POntology ontology;
		
		/**
		 * create new result
		 * @param op
		 * @param oper
		 * @param param
		 */
		public PResult(OWLNamedClass op, int oper, RDFSNamedClass param, POntology ont){
			this.operand = op;
			this.param = param;
			this.operation = oper;
			this.ontology = ont;
		}
		
		public void assertResult() {
			switch(operation){
			case (ADD_SUPERCLASS):
				operand.addSuperclass(param);
				break;
			case (REMOVE_SUPERCLASS):
				operand.removeSuperclass(param);
				break;
			case (ADD_SUBCLASS):
				param.addSuperclass(operand);
				break;
			case (REMOVE_SUBCLASS):
				param.removeSuperclass(operand);
				break;
			}
			ontology.flush();
		}

		public IResource getOperand() {
			return (IResource) ontology.convertGetValue(operand);
		}

		public int getOperation() {
			return operation;
		}

		public IResource getParameter() {
			return (IResource) ontology.convertGetValue(param);
		}
		
		private String getOperationString(){
			switch(operation){
			case (ADD_SUPERCLASS):
				return "add superclass";
			case (REMOVE_SUPERCLASS):
				return "remove superclass";
			case (ADD_SUBCLASS):
				return "remove superclass";
			case (REMOVE_SUBCLASS):
				return "remove superclass";
			}
			return "noop";
		}
		
		public String toString(){
			return operand.getBrowserText()+" "+
				   getOperationString()+" "+getParameter();
		}
	}
	
	
	/**
	 * task reasoner
	 * @author tseytlin
	 */
	private class TaskListener implements ReasonerTaskListener {
		public void addedToTask(ReasonerTaskEvent e) {
			// TODO Auto-generated method stub
			//System.out.println("task "+e);
			
		}
	
		public void descriptionChanged(ReasonerTaskEvent arg0) {
			// TODO Auto-generated method stub
		}
	
	
		public void messageChanged(ReasonerTaskEvent arg0) {
			// TODO Auto-generated method stub
			
		}
	
	
		public void progressChanged(ReasonerTaskEvent arg0) {
			// TODO Auto-generated method stub
			
		}
	
	
		public void progressIndeterminateChanged(ReasonerTaskEvent arg0) {
			// TODO Auto-generated method stub
			
		}
	
	
		public void taskCompleted(ReasonerTaskEvent e) {
			// TODO Auto-generated method stub
			//System.out.println("completed "+e.getSource()+" "+e.getSource().getMessage());
						
		}
	
	
		public void taskFailed(ReasonerTaskEvent arg0) {
			// TODO Auto-generated method stub
			
		}

	}
}
