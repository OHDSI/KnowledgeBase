package edu.pitt.terminology.util;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TreeSet;

import edu.pitt.terminology.Terminology;
import edu.pitt.terminology.client.IndexFinderTerminology;
import edu.pitt.terminology.lexicon.Concept;
import edu.pitt.terminology.lexicon.ConceptPath;


public class PathHelper {
	private boolean readOnly = true, debug;
	private int num;
	private Map<String,List<List<String>>> pathMap;
	private Map<String,Map<String,Integer>> ancestryMap;
	private Terminology terminology;
	
	/**
	 * initialize new path helper for a given terminology
	 * @param t
	 */
	public PathHelper(Terminology t){
		this.terminology = t;
	}
	
	protected void finalize() throws Throwable {
		if(ancestryMap != null && ancestryMap instanceof JDBMMap){
			((JDBMMap) ancestryMap).dispose();
		}
		if(pathMap != null && pathMap instanceof JDBMMap){
			((JDBMMap) pathMap).dispose();
		}
	}



	/**
	 * get all paths to root for a given concept
	 * @param name  - name of the concept in question
	 * @return list of paths (path is list of concepts)
	 * WARNING: for messy terminology traversing a graph can take FOREVER!!!!
	 */
	public List<ConceptPath> getPaths(Concept concept){
		if(concept != null){
			try{
				return toPaths(terminology,getPaths(concept,new HashSet<String>()));
			}catch(Exception ex){
				ex.printStackTrace();
			}
		}
		return Collections.EMPTY_LIST;
	}
	
	/**
	 * conver to paths
	 * @param paths
	 * @return
	 */
	private List<ConceptPath> toPaths(Terminology t, List<List<String>> paths) {
		List<ConceptPath> n = new ArrayList<ConceptPath>();
		for(List<String> p: paths){
			ConceptPath np = new ConceptPath();
			for(String s: p){
				Concept c = new Concept(s);
				c.setTerminology(t);
				np.add(c);
			}
			n.add(np);
		}
		return n;
	}


	/**
	 * get appropriate map for given resource
	 * @param c
	 * @return
	 * @throws IOException 
	 */
	private Map<String,List<List<String>>> getPathMap() throws IOException{
		if(pathMap == null){
			if(terminology instanceof IndexFinderTerminology){
				File f = new File(terminology.getLocation(),"table_pathMap.d.0");
				if(!readOnly || f.exists()){
					pathMap = new JDBMMap<String, List<List<String>>>(terminology.getLocation()+File.separator+"table","pathMap",readOnly);
				}
			}
		}
		// initialize as normal map
		if(pathMap == null)
			pathMap= new HashMap<String, List<List<String>>>();
		
		return pathMap;
	}
	

	/**
	 * get appropriate map for given resource
	 * @param c
	 * @return
	 * @throws IOException 
	 */
	private Map<String,Map<String,Integer>> getAncesteryMap() throws IOException{
		if(ancestryMap == null){
			if(terminology instanceof IndexFinderTerminology){
				File f = new File(terminology.getLocation(),"table_ancestorMap.d.0");
				if(!readOnly || f.exists()){
					ancestryMap = new JDBMMap<String, Map<String,Integer>>(terminology.getLocation()+File.separator+"table","ancestorMap",readOnly);
				}
			}
		}
		// initialize as normal map
		if(ancestryMap == null)
			ancestryMap= new HashMap<String,Map<String,Integer>>();
		
		return ancestryMap;
	}
	
	
	
	/**
	 * get all parents of the node
	 * @param c
	 * @return
	 */
	private List<List<String>> getPaths(Concept c,Set<String> used) throws Exception {
		// if visited return values
		if(getPathMap().containsKey(c.getCode()))
			return getPathMap().get(c.getCode());
		
		
		// if root, return empty map
		for(Concept r: terminology.getRootConcepts()){
			if(r.equals(c))
				return Collections.EMPTY_LIST;
		}
		
		// new map
		List<List<String>> paths = new ArrayList();
		for(Concept p: c.getParentConcepts()){
			if(used.contains(p.getCode()))
				return Collections.EMPTY_LIST;
			
			// skip stuff from different category as irrelevant
			//if(!p.getSemanticTypes()[0].equals(c.getSemanticTypes()[0]))
			//	return Collections.EMPTY_LIST;
		
			// keep track of used branches
			Set<String> u = new HashSet<String>();
			u.add(p.getCode());
			u.addAll(used);
			List<List<String>> ppaths = getPaths(p,u);
			if(ppaths.isEmpty()){
				paths.add(Collections.singletonList(p.getCode()));
			}else{
				for(List<String> ppath: ppaths){
					List<String> path = new ArrayList<String>();
					path.add(p.getCode());
					path.addAll(ppath);
					paths.add(path);
				}
			}
		}
		if(debug)
			System.out.println("("+num+++") "+c.getName()+" ["+c.getCode()+"] : "+paths.size()+" paths found");
		getPathMap().put(c.getCode(),paths);
		return paths;
	}
	
	
	/**
	 * given a list of concept paths, it returns a map of parent concepts and their minimum levels
	 * @param list
	 * @return
	 */
	public Map<Concept,Integer> toAncestors(List<ConceptPath> list){
		Map<Concept,Integer> map = new LinkedHashMap<Concept, Integer>();
		for(ConceptPath l: list){
			for(int i=0;i<l.size();i++){
				if(!map.containsKey(l.get(i)) || i+1 < map.get(l.get(i))){
					map.put(l.get(i),i+1);
				}
			}
		}
		return map;
	}
	
	
	/**
	 * convert a map of ancestors to a string representation
	 * @param map
	 * @return
	 */
	public String toString(Map<Concept,Integer> map){
		if(map == null)
			return "";
		
		Set<String> cuis = new TreeSet<String>(new Comparator<String>() {
			public int compare(String o1, String o2) {
				String [] c1 = o1.split(":");
				String [] c2 = o2.split(":");
				if(c1.length == 2 && c2.length == 2){
					int x = Integer.parseInt(c1[1]) - Integer.parseInt(c2[1]);
					if(x == 0)
						return c1[0].compareTo(c2[0]);
					return x;
				}
				return o1.compareTo(o2);
			}
		});
		for(Concept c: map.keySet()){
			cuis.add(c.getCode()+":"+map.get(c));
		}
		
		String s = cuis.toString();
		return s.substring(1,s.length()-1).replaceAll(" ","");
	}
	

	/**
	 * given a list of concept paths, it returns a map of parent concepts and their minimum levels
	 * @param list
	 * @return
	 */
	public Map<Concept,Integer> getAncestors(Concept c){
		//return getAncestors(getPaths(c));
		Map<Concept,Integer> result = new LinkedHashMap<Concept, Integer>();
		try {
			Map<String, Integer> map = getAncestors(c,new HashSet<Concept>());
			for(String nm: map.keySet()){
				Concept cn = new Concept(nm);
				cn.setTerminology(terminology);
				result.put(cn,map.get(nm));
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
		return result;
	}
	
	
	/**
	 * get all parents of the node
	 * @param c
	 * @return
	 */
	private Map<String,Integer> getAncestors(Concept c,Set<Concept> path) throws Exception {
		// if visited return values
		if(getAncesteryMap().containsKey(c.getCode()))
			return getAncesteryMap().get(c.getCode());
		
		// if root, return empty map
		for(Concept r: terminology.getRootConcepts()){
			if(r.equals(c))
				return Collections.EMPTY_MAP;
		}
		
		// new map
		Map<String,Integer> map = new LinkedHashMap<String,Integer>();
		for(Concept p: c.getParentConcepts()){
			// skip loops
			if(path.contains(p))
				return Collections.EMPTY_MAP;
			
			map.put(p.getCode(),1);
			
			Set<Concept> ppath = new HashSet<Concept>(path);
			ppath.add(p);
			Map<String,Integer> other = getAncestors(p,ppath);
			for(String cui: other.keySet()){
				int n = other.get(cui)+1;
				// if the other cui is in ancestors
				// then add it if it has a smaller offset
				if(map.containsKey(cui)){
					if(n < map.get(cui)){
						map.put(cui,n);
					}
				// else just add it	
				}else{
					map.put(cui,n);
				}
			}
		}
		if(debug)
			System.out.println("("+num+++") "+c.getName()+" ["+c.getCode()+"] : "+map.size()+" ancestors found");
		if (!readOnly) {
			getAncesteryMap().put(c.getCode(),map);
		}
		
		return map;
	}
	
	
	
	/**
	 * pre-build ancestory cache for a given terminology for faster ancestory access 
	 * @param t
	 */
	public void createPathCache() throws Exception {
		if(terminology instanceof IndexFinderTerminology){
			readOnly = false;
			debug = true;
			num = 0;
			if(pathMap != null && pathMap instanceof JDBMMap){
				((JDBMMap) pathMap).dispose();
			}
			JDBMMap map = (JDBMMap) getPathMap();
			for(String cui: ((IndexFinderTerminology)terminology).getAllConcepts()){
				getPaths(terminology.lookupConcept(cui),new HashSet<String>());
				if(num % 1000 == 0)
					map.commit();
			}
			map.commit();
			map.compact();
			map.dispose();
			readOnly = true;
			debug = false;
			ancestryMap = null;
		}
	}
	
	/**
	 * pre-build ancestory cache for a given terminology for faster ancestory access 
	 * @param t
	 */
	public void createAncestryCache() throws Exception {
		if(terminology instanceof IndexFinderTerminology){
			readOnly = false;
			debug = true;
			num = 0;
			if(ancestryMap != null && ancestryMap instanceof JDBMMap){
				((JDBMMap) ancestryMap).dispose();
			}
			JDBMMap map = (JDBMMap) getAncesteryMap();
			for(String cui: ((IndexFinderTerminology)terminology).getAllConcepts()){
				getAncestors(terminology.lookupConcept(cui),new HashSet<Concept>());
				if(num % 1000 == 0)
					map.commit();
			}
			map.commit();
			map.compact();
			map.dispose();
			readOnly = true;
			debug = false;
			ancestryMap = null;
		}
	}

	/**
	 * Does A have an ancestor B
	 * @param a
	 * @param b
	 * @return
	 */
	public boolean hasAncestor(Concept a, Concept b){
		try {
			return a.equals(b) || getAncestors(a,new HashSet<Concept>()).containsKey(b.getCode());
		} catch (Exception e) {
			e.printStackTrace();
		}
		return false;
	}
	
	
	/**
	 * @param args
	 */
	public static void main(String[] args) throws Exception {
		IndexFinderTerminology.setPersistenceDirectory(new File("/home/tseytlin/Data/Terminologies/IndexFinder"));
		Terminology terminology = new IndexFinderTerminology("TIES_Pathology");
		//Terminology terminology = new IndexFinderTerminology("NCI_Thesaurus");
		PathHelper ph = new PathHelper(terminology);
		//ph.createAncestryCache();
		for(String text: Arrays.asList("melanoma","nevus","skin","margin")){
			for(Concept c: terminology.search(text)){
				long t = System.currentTimeMillis();
				// lookup paths
				
				List<ConceptPath> path = ph.getPaths(c);
				t = System.currentTimeMillis()-t;
				System.out.println(c.getName()+" ["+c+"] ("+t+" ms)  number of paths: "+path.size());
				for(ConceptPath p: path)
					System.out.println("\t"+p);
				
				// lookup ancestors
				t = System.currentTimeMillis();
				Map<Concept,Integer> ancestors = ph.getAncestors(c);
				t = System.currentTimeMillis()-t;
				System.out.println(c.getName()+" ["+c+"] ("+t+" ms) number of ancestors: "+ancestors.size());
				System.out.println("\t"+ph.toString(ancestors));
				
			}
		}

	}
}
