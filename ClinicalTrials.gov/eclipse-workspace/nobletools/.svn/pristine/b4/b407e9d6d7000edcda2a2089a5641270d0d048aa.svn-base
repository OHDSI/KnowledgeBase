package edu.pitt.ontology.protege;

import edu.pitt.ontology.IClass;
import edu.pitt.ontology.IInstance;
import edu.pitt.ontology.ILogicExpression;
import edu.pitt.ontology.IOntology;
import edu.pitt.ontology.IProperty;
import edu.pitt.ontology.IRestriction;
import edu.pitt.ontology.LogicExpression;
import edu.stanford.smi.protegex.owl.model.OWLAllValuesFrom;
import edu.stanford.smi.protegex.owl.model.OWLCardinality;
import edu.stanford.smi.protegex.owl.model.OWLCardinalityBase;
import edu.stanford.smi.protegex.owl.model.OWLHasValue;
import edu.stanford.smi.protegex.owl.model.OWLMaxCardinality;
import edu.stanford.smi.protegex.owl.model.OWLMinCardinality;
import edu.stanford.smi.protegex.owl.model.OWLRestriction;
import edu.stanford.smi.protegex.owl.model.OWLSomeValuesFrom;
import edu.stanford.smi.protegex.owl.model.RDFProperty;
import edu.stanford.smi.protegex.owl.model.RDFResource;
import edu.stanford.smi.protegex.owl.model.RDFSLiteral;

public class PRestriction extends PClass implements IRestriction {
	private OWLRestriction rest;
	
	public PRestriction(OWLRestriction r, IOntology o){
		super(r,o);
		this.rest = r;
		
		// print info
		/*
		System.out.println(rest.getClass().getName()+" defined: "+rest.isDefined());
		System.out.println("filler prop: "+rest.getFillerProperty().getBrowserText());
		System.out.println("on property: "+rest.getOnProperty().getBrowserText());
		if(r instanceof OWLQuantifierRestriction){
			System.out.println("filler: "+((OWLQuantifierRestriction)r).getFiller().getBrowserText());
		}
		
		if(r instanceof OWLSomeValuesFrom){
			OWLSomeValuesFrom s = (OWLSomeValuesFrom) r;
			System.out.println("resource: "+s.getSomeValuesFrom().getBrowserText());
		}else if(r instanceof OWLHasValue){
			OWLHasValue s = (OWLHasValue) r;
			System.out.println("value: "+s.getHasValue());
		}
		*/
	}
	
	/**
	 * get restriction type
	 * @return a type that can be either one of:
	 * ALL_VALUES_FROM,SOME_VALUES_FROM,HAS_VALUE,CARDINALITY,MAX_CARDINALITY,MIN_CARDINALITY
	 */
	public int getRestrictionType(){
		if(rest instanceof OWLAllValuesFrom)
			return IRestriction.ALL_VALUES_FROM;
		else if(rest instanceof OWLSomeValuesFrom)
			return IRestriction.SOME_VALUES_FROM;
		else if(rest instanceof OWLHasValue)
			return IRestriction.HAS_VALUE;
		else if(rest instanceof OWLCardinality)
			return IRestriction.CARDINALITY;
		else if(rest instanceof OWLMaxCardinality)
			return IRestriction.MAX_CARDINALITY;
		else if(rest instanceof OWLMinCardinality)
			return IRestriction.MIN_CARDINALITY;
		return 0;
	}
	
	
	/**
	 * Gets the property that is restricted by this restriction
	 * @return
	 */
	public IProperty getProperty(){
		return new PProperty(rest.getOnProperty(),getOntology());
	}
	
	/**
	 * Sets the property that is restricted by this restriction
	 * @return
	 */
	public void setProperty(IProperty prop){
		rest.setOnProperty((RDFProperty)convertSetValue(prop));
	}
	
	
	/**
	 * get restriction parameter. Filler. 
	 * Parameter could be a Integer, String, Boolean, Float for CARDINALITY and HAS_VALUE restrictions
	 * It could be IResource for ALL_VALUES_FROM, SOME_VALUES_FROM and HAS_VALUE
	 * It could also be IResourceList that is a conjunction or disjunction of parameters
	 * @return
	 */
	public ILogicExpression getParameter(){
		Object obj = null;
		if(rest instanceof OWLAllValuesFrom){
			RDFResource r = ((OWLAllValuesFrom) rest).getAllValuesFrom();
			obj = convertGetValue(r);
		}else if(rest instanceof OWLSomeValuesFrom){
			RDFResource r = ((OWLSomeValuesFrom) rest).getSomeValuesFrom();
			obj = convertGetValue(r);
		}else if(rest instanceof OWLHasValue){
			Object r = ((OWLHasValue) rest).getHasValue();
			obj = convertGetValue(r);
		}else if(rest instanceof OWLCardinalityBase){
			int  r = ((OWLCardinalityBase) rest).getCardinality();
			obj = new Integer(r);
		}
		if(obj instanceof ILogicExpression)
			return (ILogicExpression) obj;
		return new LogicExpression(obj);
	}
	
	/**
	 * set restriction parameter. Filler. 
	 * Parameter could be a Integer, String, Boolean, Float for CARDINALITY and HAS_VALUE restrictions
	 * It could be IResource for ALL_VALUES_FROM, SOME_VALUES_FROM and HAS_VALUE
	 * It could also be IResourceList that is a conjunction or disjunction of parameters
	 * @return
	 */
	public void setParameter(ILogicExpression exp){
		if(exp == null || exp.isEmpty())
			return;
		// convert to Protege way
		Object obj = convertSetValue(exp);
		
		// set parameter
		if(rest instanceof OWLAllValuesFrom && obj instanceof RDFResource){
			((OWLAllValuesFrom) rest).setAllValuesFrom((RDFResource) obj);
		}else if(rest instanceof OWLSomeValuesFrom && obj instanceof RDFResource){
			((OWLSomeValuesFrom) rest).setSomeValuesFrom((RDFResource) obj);
		}else if(rest instanceof OWLHasValue){
			((OWLHasValue) rest).setHasValue(obj);
		}else if(rest instanceof OWLCardinalityBase){
			int i = -1;
			if(obj instanceof Integer)
				i = ((Integer) obj).intValue();
			else if(obj instanceof RDFSLiteral)
				i = ((RDFSLiteral) obj).getInt();
			if(i > -1)
				((OWLCardinalityBase) rest).setCardinality(i);
		}
	}
	
	
	/**
	 * get owner of this restriction
	 * @return
	 */
	public IClass getOwner(){
		return new PClass(rest.getOwner(),getOntology());
	}

	
	
	/**
	 * check if property is satisfied
	 * @param prop
	 * @param inst
	 * @return
	 */
	private boolean isPropertySatisfied(IProperty prop, IInstance inst){
		// if property is null, then not satisfied
		if(prop == null)
			return false;
		
		// if either parameter is null, then condition is sutisfied :)
		if(inst == null)
			return true;
		
		Object [] values = inst.getPropertyValues(prop);
		if(values == null || values.length == 0)
			return false;
		
		// if any of values fits, that we are good
		ILogicExpression exp = getParameter();
		for(int i=0;i<values.length;i++){
			if(exp.evaluate(values[i])){
				return true;
			}
		}
		return false;
	}
	
	
	/**
	 * is this restriction satisfied for the owner of this restriction
	 * @param this could be a IClass, IInstance, IReousrceList or java object
	 */
	public boolean evaluate(Object obj){
		if(obj instanceof IInstance){
			IInstance inst = (IInstance) obj;
			// see if this instance has a value that fits this restriction
			IProperty prop = getProperty();
			
			// is property satisfied
			boolean satisfied = isPropertySatisfied(prop, inst);
			
			// check if there is evidence to contradict inverse property
			// then the instance becomes inconsistent again
			if(satisfied && isPropertySatisfied(prop.getInverseProperty(), inst)){
				satisfied = false;
			}
			return satisfied;
		}else{
			return super.evaluate(obj);
		}
	}
	
	
	
	
	/**
	 * how does this thing appear
	 */
	public String getName(){
		return rest.getOperator()+" "+rest.getBrowserText();
	}
}
