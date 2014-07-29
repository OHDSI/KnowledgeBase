package main;

import mapping.RFFMapper;

public class MeSHMapper {
	
	public static void main(String[] args) {
		
		String inputdata = "/media/Backup/UMLS-Triads-OHDSI-subset-Feb2014/2013AB/META/MRCONSO.RRF";
		String serialLocation = "../MeSHHashMap.ser";
		
		RFFMapper map = new RFFMapper();
		map.makeMapping(inputdata, 1, 13, 14);
		map.makeSerializable(serialLocation);
	}
}
