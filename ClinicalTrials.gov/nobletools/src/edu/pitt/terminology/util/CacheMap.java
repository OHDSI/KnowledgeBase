package edu.pitt.terminology.util;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

/**
 * This class represents a hash map that can be capped at a given
 * limit, and periodically cleaned based on frequency of use or 
 * recency of use
 * @author tseytlin
 *
 * @param <K>
 * @param <V>
 */
public class CacheMap<K,V> extends HashMap<K, V> {
	public static final int FREQUENCY = 0, TIME = 1;
	private int sizeLimit,mode,totalHits;
	private long expirationTime;
	private Map<K,Integer> frequencyCount;
	private Map<K,Long> timeCount;

	
	/**
	 * create a new cache map
	 */
	public CacheMap(){
		this(FREQUENCY);
	}
	
	/**
	 * create a new cache map
	 */
	public CacheMap(int type){
		mode = type;
		if(FREQUENCY == mode){
			frequencyCount = new HashMap<K,Integer>();
		}else if(TIME == mode){
			timeCount = new HashMap<K, Long>();
		}
	}
	
	/**
	 * get the limit in size that the cache is not allowed to exceed
	 * @return
	 */
	public int getSizeLimit() {
		return sizeLimit;
	}

	/**
	 * set the limit in size that the cache is not allowed to exceed
	 * @return
	 */
	public void setSizeLimit(int sizeLimit) {
		this.sizeLimit = sizeLimit;
	}
	
	/**
	 * get the expiration time in ms
	 * @return
	 */
	public long getExpirationTime() {
		return expirationTime;
	}

	/**
	 * set the expiration time in ms
	 * @return
	 */	
	public void setExpirationTime(long expirationTime) {
		this.expirationTime = expirationTime;
	}

		
	/**
	 * touch an entry to update its counter
	 * @param key
	 */
	private synchronized void touch(K key){
		if(frequencyCount != null){
			Integer c = frequencyCount.get(key);
			frequencyCount.put(key,(c != null)?c.intValue()+1:1);
		}else if(timeCount != null){
			timeCount.put(key,System.currentTimeMillis());
		}
		totalHits++;
	}
	
	
	/**
	 * get an item and update its counter
	 */
	public synchronized V get(Object key) {
		V v = super.get(key);
		if(v != null)
			touch((K)key);
		return v;
	}
	
	/**
	 * overwrite the touch
	 */
	public synchronized V put(K key, V value) {
		// if exceed size limit, compact
		if(sizeLimit > 0 && sizeLimit <= size())
			compact();
		touch(key);
		return super.put(key, value);
	}
	
	/**
	 * remove object
	 */
	public synchronized V remove(Object key) {
		if(frequencyCount != null){
			frequencyCount.remove(key);
		}else if(timeCount != null){
			timeCount.remove(key);
		}
		return super.remove(key);
	}

	/**
	 * clear cache
	 */
	public synchronized void clear(){
		super.clear();
		if(frequencyCount != null)
			frequencyCount.clear();
		if(timeCount != null)
			timeCount.clear();
	}
	
	/**
	 * compact cache by discarding stale items
	 */
	public synchronized void compact(){
		if(frequencyCount != null){
			int ave = totalHits/size();
			for(K key : new ArrayList<K>(keySet())){
				Integer i = frequencyCount.get(key);
				if(i == null || i.intValue() < ave)
					remove(key);
			}
		}else if(timeCount != null){
			long time  = System.currentTimeMillis();
			for(K key : new ArrayList<K>(keySet())){
				Long i = timeCount.get(key);
				if(i == null || (time-i.longValue()) > expirationTime)
					remove(key);
			}
		}
	}
}
