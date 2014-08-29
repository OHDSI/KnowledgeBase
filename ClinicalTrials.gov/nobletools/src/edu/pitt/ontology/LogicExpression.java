package edu.pitt.ontology;

import java.util.*;

/**
 * list of resources that could be conjunction or disjunction
 * @author tseytlin
 */
public class LogicExpression extends ArrayList implements ILogicExpression {
	private int type;

	
	/**
	 * create logic expression of a type
	 * @param type
	 */
	public LogicExpression(Object obj){
		this(0,obj);
	}
	
	/**
	 * create logic expression of a type
	 * @param type
	 */
	public LogicExpression(int type){
		super();
		this.type = type;
	}
	
	/**
	 * create logic expression of a type
	 * @param type
	 */
	public LogicExpression(int type, Collection c){
		super(c);
		this.type = type;
	}
	
	/**
	 * create logic expression of a type
	 * @param type
	 */
	public LogicExpression(int type, Object obj){
		super();
		this.type = type;
		add(obj);
	}
	
	
	/**
	 * create logic expression of a type
	 * @param type
	 */
	public LogicExpression(int type, Object [] obj){
		super();
		this.type = type;
		Collections.addAll(this,obj);
	}
	/**
	 * get single operand, usefull when singleton expression
	 * @return
	 */
	public Object getOperand(){
		return (size() > 0)?get(0):null;
	}
	
	/**
	 * get all operands
	 * @return
	 */
	public List getOperands(){
		return this;
	}
	
	/**
	 * get expression type
	 * AND, OR, NOT
	 * if 0 is returned then expression is just a container 
	 * for a single value ex: (A)  
	 * @return
	 */
	public int getExpressionType(){
		return type;
	}
	
	/**
	 * set expression type
	 * AND, OR, NOT
	 * if 0 is returned then expression is just a container 
	 * for a single value ex: (A)  
	 * @return
	 */
	public void setExpressionType(int type){
		this.type = type;
	}
	
	/**
	 * true if expression has only one parameter
	 * Ex: NOT or empty expression
	 * @return
	 */
	public boolean isSingleton(){
		//return size() == 1;
		return type == NOT || type == EMPTY;
	}
	
	
	/**
	 * add object enforce singleton
	 */
	public boolean add(Object obj){
		if(type <= NOT && !isEmpty()){
			return false;
		}
		return super.add(obj);
	}
	
	/**
	 * evaluate single parameter
	 * @param obj
	 * @return
	 */
	private boolean evaluateParameter(Object obj, Object param){
		if(obj instanceof ILogicExpression){
			return ((ILogicExpression) obj).evaluate(param);
		}else if(obj instanceof IClass){
			return ((IClass) obj).evaluate(param);
		}
		return obj.equals(param);
	}
	
	/**
	 * evaluate this expression against given object
	 * @param object
	 * @return true if object passes this expression, false otherwise
	 */
	public boolean evaluate(Object obj){
		switch(type){
			case EMPTY: 
				return evaluateParameter(getOperand(),obj);
			case NOT:   
				//	TODO: maybe incorrect
				return !evaluateParameter(getOperand(),obj);  
			case AND: 
				//	iterate over expression
				boolean b = true;
				for(Object e : this){
					b &= evaluateParameter(e,obj);
				}
				return b;	
			case OR:
				// iterate over expression
				b = false;
				for(Object e : this){
					b |= evaluateParameter(e,obj);
				}
				return b;
		}
		return false;
	}
	
	
	/**
	 * create pretty printed expressions
	 */
	public String toString(){
		if(type == AND)
			return super.toString().replaceAll(","," and");
		else if(type == OR)
			return super.toString().replaceAll(","," or");
		else if(type == NOT)
			return "[!"+super.toString().substring(1);
		return super.toString();
	}
	
	
	/**
	 * are two expressions equal?
	 */
	public boolean equals(Object obj){
		if(obj instanceof ILogicExpression){
			ILogicExpression exp = (ILogicExpression) obj;
			if(exp.size() == size() && getExpressionType() == exp.getExpressionType()){
				for(int i=0;i<size();i++){
					if(!get(i).equals(exp.get(i)))
						return false;
				}
				return true;
			}
		}
		return false;
	}
}
