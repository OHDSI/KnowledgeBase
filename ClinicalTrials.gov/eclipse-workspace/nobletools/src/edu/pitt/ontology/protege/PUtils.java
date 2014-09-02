package edu.pitt.ontology.protege;

import java.net.URI;

/**
 * set of utilities
 * @author tseytlin
 *
 */
public class PUtils {
	/**
	 * extract owl filename from path
	 * @param path
	 * @return
	 *
	public static String getName(URI path) {
		String p = path.getPath();
		return (p.lastIndexOf("/") > -1)?p.substring(p.lastIndexOf("/")+1):p;
	}
	*/
	/**
	 * extract owl filename from path
	 * @param path
	 * @return
	 */
	public static String getName(URI path) {
		String p = path.getPath();
		int i = p.lastIndexOf("/");
		String s = p;
		if(i > -1){
			// if URI ends with slash, then
			if(i == p.length()-1){
				i = p.lastIndexOf("/",i-1);
				p = p.substring(0,p.length()-1);
				if(i > -1)
					s = p.substring(i+1,p.length());
			}else
				s = p.substring(i+1);
		}
		
		// if name is composed of digits, it could be a version
		// then get the next best match
		if(s.matches("[\\d\\.]+")){
			i = p.lastIndexOf("/",i-1);
			if(i > -1)
				s = p.substring(i+1,p.length()).replaceAll("/","-");
		}
		
		return s;
	}
	
	
	/**
	 * extract owl filename from path
	 * @param path
	 * @return
	 */
	public static String getOntologyName(URI path) {
		String name = getName(path);
		int n = name.lastIndexOf(".");
		if(n > -1)
			name = name.substring(0,n);
		return name;
	}
	
	/**
	 * generate a prefix for given ontology
	 * @param path
	 * @return
	 */
	public static String createOntologyPrefix(URI path){
		String name = getOntologyName(path);
		return name.toLowerCase().replaceAll("\\W","");
	}
	
	/*
	public static void main(String [] a){
		for(String s: Arrays.asList("http://sig.biostr.washington.edu/fma3.0","http://purl.org/dc/elements/1.1/","http://www.ifomis.org/bfo/1.1","http://protege.stanford.edu/plugins/owl/dc/protege-dc.owl")){
			System.out.println(s+" | "+getName(URI.create(s)));
		}
	}
	*/
}
