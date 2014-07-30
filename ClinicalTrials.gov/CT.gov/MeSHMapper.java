
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.util.HashMap;

import mapping.RFFMapper;

public class MeSHMapper {
	
	public static void main(String[] args) {
		
		String inputdata = "/media/Backup/UMLS-Triads-OHDSI-subset-Feb2014/2013AB/META/MRCONSO.RRF";
		String serialLocation = "../MeSHHashMap.ser";
		
		RFFMapper map = new RFFMapper();
		map.makeMapping(inputdata, 1, 13, 14);
		map.makeSerializable(serialLocation);
		try {
			ObjectInputStream mappu = new ObjectInputStream(new FileInputStream(serialLocation));
			@SuppressWarnings("unchecked")
			HashMap<String, String> hey = (HashMap<String, String>)mappu.readObject();
			mappu.close();
			
			System.out.println(hey);
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (ClassNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
}

