package edu.pitt.terminology.util;

import java.io.File;
import java.io.IOException;
import java.util.Collection;
import java.util.Map;
import java.util.Set;

import org.apache.jdbm.DB;
import org.apache.jdbm.DBMaker;

/**
 * This class wraps JDBM http://jdbm.sourceforge.net/ HTree
 * To create a persistent hashtable on disk
 * @author tseytlin
 * @param <K>
 * @param <V>
 */

public class JDBMMap<K extends Comparable, V> implements Map<K, V> {
	private Map<K,V> map;
	private String name,filename;
	private DB db;
	private boolean readonly;
	private final String JDBM_SUFFIX = ".d.0";
	
	
	/**
	 * create an instance of persistent hash map
	 */
	public JDBMMap(String filename, String tablename) throws IOException{
		this(filename,tablename,false);
	}
			
	/**
	 * create an instance of persistent hash map
	 */
	public JDBMMap(String filename, String tablename, boolean readonly) throws IOException{
		this.name = tablename;
		this.filename = filename;
		this.readonly = readonly;
		String f = filename+"_"+tablename;
		
		// check parent directory
		if(!new File(f).getParentFile().exists())
			throw new IOException("Location "+new File(f).getParentFile().getAbsolutePath()+" does not exist!");
		
		// if file doesn't exist, make it read-only
		if(readonly && !new File(f+JDBM_SUFFIX ).exists())
			readonly = false;
		
		// init record manager
		DBMaker d = DBMaker.openFile(f);
		// set options
		d.disableTransactions();
		d.closeOnExit();
		d.enableMRUCache();
		d.useRandomAccessFile();
		//d.enableHardCache();
		//d.disableCache();
		if(readonly){
			d.disableLocking();
			d.readonly();
		}
		db = d.make();
		
	    // create or load hashtable from given file
		map = db.getHashMap(tablename);
		if(map == null)
			map = db.createHashMap(tablename);
	}
	public boolean isReadOnly(){
		return readonly;
	}
	
	public String getTableName(){
		return name;
	}
	
	public String getFileName(){
		return filename;
	}
	
	protected void finalize() throws Throwable {
		dispose();
	}
	

	public void dispose(){
		db.close();
	}
	
	/**
	 * commit transaction
	 */
	public void commit(){
		db.commit();
	}
	
	public void compact(){
		db.defrag(true);
	}
	
	/**
	 * remove all records at once
	 */
	public void clear() {
		map.clear();
	}

	
	/**
	 * contains key
	 */
	public boolean containsKey(Object key) {
		return map.containsKey(key);
	}

	/**
	 * this is very expensive call to check for values
	 */
	public boolean containsValue(Object e) {
		return map.containsValue(e);
	}

	
	/**
	 * this is a very expensive call to get all of the entry set
	 */
	public Set<Map.Entry<K, V>> entrySet() {
		return map.entrySet();
	}

	
	/**
	 * get value for given key
	 */
	public V get(Object key) {
		return map.get(key);
	}

	public boolean isEmpty() {
		return map.isEmpty();
	}

	
	/**
	 * this is an expensive call to get all of the keys
	 */
	public Set<K> keySet() {
		return map.keySet();
	}

	/**
	 * put values into the table
	 */
	public V put(K key, V value) {
		return map.put(key,value);
	}

	/**
	 * put all values
	 */
	public void putAll(Map<? extends K, ? extends V> m) {
		map.putAll(m);
	}

	
	/**
	 * remove entry from hashtable
	 */
	public V remove(Object key) {
		return map.remove(key);
	}

	public int size() {
		return map.size();
	}

	/**
	 * this is an expensive call to get all of the values
	 */
	public Collection<V> values() {
		return map.values();
	}
	public String toString(){
		return map.toString();
	}
}
