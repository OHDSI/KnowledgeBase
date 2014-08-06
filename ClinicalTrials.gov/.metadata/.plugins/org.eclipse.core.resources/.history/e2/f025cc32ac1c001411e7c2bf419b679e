package mapping;

import mapping.RFFMapper;
/**
 * This is the file that will make a serializable hashmap for mesh terms based on the search string.
 * This HashMap<String, String> will be used when we run on 
 * 
 * Usage...
 * 
 * $ java MeSHMapper
 * 
 * input:
 * - "/media/Backup/UMLS-Triads-OHDSI-subset-Feb2014/2013AB/META/MRCONSO.RRF"
 * - has to be run on Dr. Boyce's dev server
 * output:
 * - "../MeSHHashMap.ser"
 * 
 * @author Jeremy Jao
 *
 */
public class MeSHMapper {
	
	public static void main(String[] args) {
		
		String inputdata = "/media/Backup/UMLS-Triads-OHDSI-subset-Feb2014/2013AB/META/MRCONSO.RRF";
		String serialLocation = "../MeSHHashMap.ser";
		
		RFFMapper map = new RFFMapper();
		map.makeMapping(inputdata, "MSH", 1, 13, 14);
		map.makeSerializable(serialLocation); 
	}
}

