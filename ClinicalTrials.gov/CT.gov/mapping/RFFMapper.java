package mapping;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.ObjectOutputStream;
import java.io.Serializable;
import java.util.HashMap;

/**
 * 
 * Takes RFF files from the UMLS Metathesaurus then adds them to a hashmap.
 * Right now, it only considers a case to find and then a match... such as...
 * finding the word 'Hello' and get a CUI match of '12315'.
 * 
 * This file was originally made to find MeSH CUIs for ENG strings in
 * MRCONSO.RFF so when finding mappings, you have to know the file before running it.
 * 
 * @author epicstar
 *
 */
public class RFFMapper implements Serializable {
	
	/**
	 * Serial ID (Eclipse likes this a lot)
	 */
	private static final long serialVersionUID = -8572398461651470175L;
	
	/**
	 * The mapper to find the MeSH CUI:
	 * String: CUI
	 * 
	 * I reckon this isn't the most space efficient way but it's the fastest way to program this.
	 */
	private HashMap<String, String> find;
	
	/**
	 * Initializes the Mapper from the RFF files
	 */
	public RFFMapper() {	
		find = new HashMap<String, String>();
	}
	
	/**
	 * Adds the string literal of a certain CUI to the map.
	 * @param cui
	 * @param string
	 */
	private void addToMap(String cui, String string) {
		if(find.containsKey(string)) {
			System.out.println(string + " is already contained...");

			if(find.get(string).equals(cui)) {
				System.out.println("However, the CUIs are equal...");
			}
			else {
				System.out.println("The CUIs are different...| " + "old: " + find.get(string) + " | new: " + cui);
				return;
			}
		}
		find.put(string, cui);
	}
	
	/**
	 * Builds up the mapper object.
	 * @param fileInputLocation input location of the file.
	 * @param language In some files, many string finders have many different languages for one CUI
	 * @param cui This is the common universal identifier for a string
	 * @param string The string to find the common universal identifier
	 */
	public void makeMapping(String fileInputLocation, int language, int cui, int string) {
		BufferedReader buf;
		String[] currentRow;
		try {
			System.out.println("Processing file...");
			buf = new BufferedReader(new FileReader(fileInputLocation));
			System.out.println("Finished processing! Now parsing and creating.");
			while (buf.ready()) {
				currentRow = buf.readLine().split("\\|");
				if((currentRow.length >= Math.max(cui, string)) && (language == -1 || (currentRow[language].equals("PT") ||currentRow[language].equals("ENG")))) {
					addToMap(currentRow[cui], currentRow[string]);
				}
			}
			buf.close();
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
	/**
	 * 
	 * @param fileInputLocation
	 * @param cui
	 * @param string
	 */
	public final void makeMapping(String fileInputLocation, int cui, int string) {
		makeMapping(fileInputLocation, -1, cui, string);
	}
	
	/**
	 * Getter method for the mapper
	 * @return the map object (as a final)
	 */
	public final HashMap<String, String> getMapping() {
		return find;
	}
	
	/**
	 * This takes the map object (HashMap<String, String>) and serializes it.
	 * This was so if there was a long big RFF file, we could run this first and save the HashMap object
	 * to disk.
	 * 
	 * @param output location of the file you want to save the serialized object by string...
	 */
	public void makeSerializable(String output) {
		
		try {
			ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream(output));
			out.writeObject(find);
			out.close();
			System.out.println("Hashmap written to " + output);
			
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
	}
	
}
