package edu.pitt.terminology.util;

import java.lang.management.ManagementFactory;
import java.lang.management.MemoryMXBean;
import java.lang.management.MemoryNotificationInfo;
import java.lang.management.MemoryPoolMXBean;
import java.lang.management.MemoryType;
import java.util.ArrayList;
import java.util.List;

import javax.management.ListenerNotFoundException;
import javax.management.Notification;
import javax.management.NotificationEmitter;
import javax.management.NotificationListener;

/**
 * this class attempts to notify user before available memory is about to run
 * out Most of the code was shamelessly copied from this link
 * http://techblug.wordpress.com/2011/07/21/detecting-low-memory-in-java-part-2/
 * 
 * @author Eugene Tseytlin (University of Pittsburgh)
 */
public class MemoryManager {
	private static MemoryPoolMXBean tenuredGenPool = null;
	private static List<NotificationListener> listeners = new ArrayList<NotificationListener>();
	
	static {
		for (MemoryPoolMXBean pool : ManagementFactory.getMemoryPoolMXBeans()) {
			// see http://www.javaspecialists.eu/archive/Issue092.html
			if (pool.getType() == MemoryType.HEAP && pool.isUsageThresholdSupported()) {
				tenuredGenPool = pool;
			}
		}
	}

	/**
	 * When memory reaches a given threshold say 90% of available
	 * execute a given action right away
	 * @param run
	 */
	public static void setMemoryThreshold(Runnable run, double threshold) {
		// setting the threshold to 80% usage of the memory
		tenuredGenPool.setCollectionUsageThreshold((int) Math.floor(tenuredGenPool.getUsage().getMax() * threshold));
		tenuredGenPool.setUsageThreshold((int) Math.floor(tenuredGenPool.getUsage().getMax() * threshold));

		final Runnable r = run;
		MemoryMXBean mbean = ManagementFactory.getMemoryMXBean();
		NotificationEmitter emitter = (NotificationEmitter) mbean;
		NotificationListener l = new NotificationListener() {
			public void handleNotification(Notification n, Object hb) {
				if (n.getType().equals(MemoryNotificationInfo.MEMORY_COLLECTION_THRESHOLD_EXCEEDED)) {
					// this is th warning we want
					r.run();
				} else if (n.getType().equals(MemoryNotificationInfo.MEMORY_THRESHOLD_EXCEEDED)) {
					// just FYI
					// System.out.println("memory threshold exceeded !!! : \n "+memString());
				}
			}
		};
		emitter.addNotificationListener(l,null,null);
		
		// remove previous listeners
		for(NotificationListener n : listeners){
			try {
				emitter.removeNotificationListener(n);
			} catch (ListenerNotFoundException e) {
				e.printStackTrace();
			}
		}
		listeners.clear();
		listeners.add(l);
	}

}
