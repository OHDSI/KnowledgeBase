package edu.pitt.ontology;

import java.util.List;

/**
 * a list of resources that could be either
 * conjunction or disjunction
 * @author tseytlin
 */
public interface ILogicExpression extends List {
	public static int OR = 3;
	public static int AND = 2;
	public static int NOT = 1;
	public static int EMPTY = 0;
	
	/**
	 * get expression type
	 * AND, OR, NOT
	 * if 0 is returned then expression is just a container 
	 * for a single value ex: (A)  
	 * @return
	 */
	public int getExpressionType();
	
	
	/**
	 * set expression type
	 * AND, OR, NOT
	 * if 0 is returned then expression is just a container 
	 * for a single value ex: (A)  
	 * @return
	 */
	public void setExpressionType(int type);
	
	/**
	 * true if expression has only one parameter
	 * Ex: NOT or empty expression
	 * @return
	 */
	public boolean isSingleton();
	
	/**
	 * get single operand, usefull when singleton expression
	 * @return
	 */
	public Object getOperand();
	
	/**
	 * get all operands
	 * @return
	 */
	public List getOperands();
	
	
	/**
	 * evaluate this expression against given object
	 * @param object
	 * @return true if object passes this expression, false otherwise
	 */
	public boolean evaluate(Object obj);
}
