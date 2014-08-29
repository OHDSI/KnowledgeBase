package edu.pitt.ontology;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.List;



/**
 * singleton class with lots of usefull ontology related methods
 * @author tseytlin
 */
public class OntologyUtils {
	/**
	 * get a paths to root for a given concept
	 * @param name  - name of the class in question
	 * @return list of paths (path is list of classes)
	 */
	public static List<ClassPath> getRootPaths(IClass cls){
		if(cls != null){
			// get paths to root
			List<ClassPath> paths = new ArrayList<ClassPath>();
			getPath(cls,new ClassPath(), paths);
			return paths;
		}
		return Collections.EMPTY_LIST;
	}
	
	/**
	 * get multiple paths to root
	 * @param cls
	 * @param path
	 * @param paths
	 */
	private static void getPath(IClass cls,ClassPath path, List<ClassPath> paths){
		// add to paths if path is not in paths
		if(!paths.contains(path)){
			paths.add(path);
		}
		
		// add to current path
		path.add(0,cls);
		// iterate over parents
		List<IClass> parents = new ArrayList<IClass>();
		for(IClass p: cls.getDirectSuperClasses())
			if(!p.hasSuperClass(cls))
				parents.add(p);
		
		// if only one parent, then add it to path
		if(parents.size() == 1){
			getPath(parents.get(0),path,paths);
		}else if(parents.size() > 1){
			// else clone current path and start new ones
			for(int i=1;i<parents.size();i++){
				getPath(parents.get(i),new ClassPath(path),paths);
			}
			getPath(parents.get(0),path,paths);
		}
	}
	
	/**
	 * convert object to String
	 * @param o
	 * @return
	 */
	public static String toHTML(Object o){
		if(o == null)
			return "";
		
		// do varias pretty printing things
		if(o instanceof IRestriction){
			IRestriction r = (IRestriction) o;
			StringBuffer str = new StringBuffer();
			str.append(toHTML(r.getProperty()));
			switch(r.getRestrictionType()){
			case IRestriction.ALL_VALUES_FROM:
				str.append(" <b>all</b> "); break;
			case IRestriction.SOME_VALUES_FROM:
				str.append(" <b>some</b> "); break;
			case IRestriction.HAS_VALUE:
				str.append(" <b>has</b> "); break;
			default:
				str.append(" <b> = </b> "); 
			}
			str.append(toHTML(((IRestriction) o).getParameter()));
			return str.toString();
		}else if(o instanceof IInstance){
			return "<i>"+o+"</i>";
		}else if(o instanceof IProperty){
			return "<a href=\"property:"+o+"\">"+o+"</a>";
		}else if(o instanceof IClass){
			IClass c = (IClass)o;
			return (c.isAnonymous())?"anonymous":"<a href=\"class:"+o+"\">"+o+"</a>";
		}else if(o instanceof Collection){
			String sep = ", ";
			if(o instanceof ILogicExpression){
				ILogicExpression exp = (ILogicExpression) o;
				if(exp.getExpressionType() == ILogicExpression.AND)
					sep = " and ";
				else if(exp.getExpressionType() == ILogicExpression.OR)
					sep = " or ";
			}else if(o instanceof ClassPath){
				sep = " &rArr; ";
			}
			
			StringBuffer str = new StringBuffer();
			for(Object i: (Collection) o){
				str.append(toHTML(i)+sep);
			}
			String s = (str.length() > 0)?str.substring(0,str.length()-sep.length()):"";
			return (o instanceof ILogicExpression)?"("+s+")":s;
		}else if (o instanceof Object []){
			String sep = ", ";
			StringBuffer str = new StringBuffer();
			for(Object i: (Object []) o){
				str.append(toHTML(i)+sep);
			}
			return (str.length() > 0)?str.substring(0,str.length()-sep.length()):"";
		}
		// else just convert		
		return o.toString();
	}
	
	
	/**
	 * derive valid class name from any string
	 * @param name
	 * @return
	 */
	public static String toResourceName(String name){
		return name.trim().replaceAll("\\s*\\(.+\\)\\s*","").replaceAll("[^\\w\\-]","_").replaceAll("_+","_");
	}
	
	/**
	 * Derive prettier version of a class name
	 * @param resourceName
	 * @return
	 */
	public static String toPrettyName(String resourceName){
		// if name is in fact URI, just get a thing after hash
		int i = resourceName.lastIndexOf("#");
		if(i > -1){
			resourceName = resourceName.substring(i+1);
		}
				
		// strip prefix (if available)
		i = resourceName.indexOf(":");
		if(i > -1){
			resourceName = resourceName.substring(i+1);
		}
		
		// if name is in fact a URI, but not a fragment 
		i =  resourceName.lastIndexOf("/");
		if(i > -1)
			resourceName = resourceName.substring(i+1);
	
		
		// possible lowercase values to make things look prettier
		if(!resourceName.matches("[A-Z_\\-\\'0-9]+") && !resourceName.matches("[a-z][A-Z_\\-\\'0-9]+[\\w\\-]*"))
			resourceName = resourceName.toLowerCase();
			
		// now replace all underscores with spaces
		return resourceName.replaceAll("_"," ");
	}
}
