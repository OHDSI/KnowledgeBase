package map.addcuis;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;

import edu.pitt.terminology.client.IndexFinderTerminology;
import edu.pitt.terminology.lexicon.Concept;
import edu.pitt.terminology.lexicon.SemanticType;
import edu.pitt.terminology.lexicon.Source;
import edu.pitt.terminology.util.TerminologyException;

/**
 * Adds CUIs to the file in the Git "Example-CT.gov-data-v3-v011.csv"
 * 
 * Adds the MeSH CUIs to the MeSH Condition and MeSH Interventions in a pipe delimited format
 * from the triads MeSH exact string mapper which does with amazing accuracy.
 * 
 * Will Add MedDRA, SNOMED_CT, and RxNorm CUIs from Nobletools jar NLP program from the text column
 * Using the IndexFinderTerminology class.
 * 
 * @author epicstar
 *
 */

public class AddCuis {
	
	private HashMap<String, String> meshMap;
	private IndexFinderTerminology term;
	private PrintWriter pseudolog;
	private static final Source[] nobleCoderVocabs = {new Source("MDR"), new Source("SNOMEDCT_US"), new Source("MSH")};
	
	public AddCuis() throws FileNotFoundException {
		meshMap = null;
		term = null;
		pseudolog = new PrintWriter("../missingCUIs.txt");
	}
	
	@SuppressWarnings("unchecked")
	public boolean addCuis(String input, String output) {
		
		
		
		try {
			
			BufferedReader in = new BufferedReader(new FileReader(input));
			PrintWriter out = new PrintWriter(output);
			List<String> line = new LinkedList<String>(Arrays.asList(in.readLine().split("\t")));
			
			System.out.println("Starting the CUI adder");
			insert(line, 8, "msh_intervention_CUI");
			insert(line, 7, "msh_condition_CUI");
			
			insert(line, 2, "text_MedDRA_CUI");
			insert(line, 2, "text_SNOMED_CT_CUI");
			insert(line, 2, "text_MeSH_CUI");
			
//			System.out.println(line);
			out.write(outputString(line, "\t") + "\n");			
			
			ObjectInputStream meshMapfile = new ObjectInputStream(new FileInputStream("../MeSHHashMap.ser"));
			meshMap = (HashMap<String, String>)meshMapfile.readObject();
			setupNobleCoder();
			meshMapfile.close();
			
			System.out.println("Adding CUIs. This may take take a while.");
			
			while(in.ready()) {
				
				line = new ArrayList<String>(Arrays.asList(in.readLine().split("\t")));
				addMesh(line, 8);
				addMesh(line, 7);
				addFromNobleCoder(line);
				out.write(outputString(line, "\t") + "\n");
				
//				insert(line, 2, "MedDRA_CUI");
//				insert(line, 2, "SNOMED_CUI");
//				insert(line, 2, "RxNorm_CUI");
				
			}
			System.out.println("Finished!");
			in.close();
			out.close();
			pseudolog.close();
			
		
		} catch(IOException e) {
			System.out.println(e.getMessage());
			return false;
		} catch(ClassNotFoundException e) {
			System.out.println(e.getMessage());
			return false;
		}
			
		return true;
		
	}
	
	private void addFromNobleCoder(List<String> line) {
		String find = line.get(1);
		try {
			
			Concept[] results = term.search(find);
			if(results.length > 0) {
				@SuppressWarnings("rawtypes")
				Map nobleCodes = results[0].getCodes();

				LinkedList<String> missingCUIs = new LinkedList<String>();
				for(Source vocab : nobleCoderVocabs) {
					if(nobleCodes.containsKey(vocab))
						insert(line, 2, (String)nobleCodes.get(vocab));
					else {
						insert(line, 2, "");
						missingCUIs.add(vocab.toString());
					}
				}
				if(missingCUIs.size()>0) {
					StringBuffer log = new StringBuffer();
					log.append(find + " missing NobleCoder CUIs: ");
					int index = 0;
					for(String voc : missingCUIs) {
						log.append(voc);
						if(++index < missingCUIs.size())
							log.append(", ");
					}
					pseudolog.write(log.toString() + "\n");
				}
			}
			else {
				for(int i=0;i<3;++i) {
					insert(line, 2, "");
				}
				pseudolog.write(find + " not found in NobleCoder." + "\n");
			}
		} catch (TerminologyException e) {
			System.out.println(e.getMessage());
			e.printStackTrace();
		}
	}
	
	private void setupNobleCoder() throws IOException {

			term = new IndexFinderTerminology();
			term.load("triads-test-Feb2014");
			term.setIgnoreAcronyms(false);
			term.setOverlapMode(false);
			term.setSelectBestCandidate(false);
			term.setDefaultSearchMethod("best-match");
			term.setSubsumptionMode(false);
			term.setFilterSources(term.getSources("MDR,MSH,SNOMEDCT_US"));
			term.
				setFilterSemanticType(SemanticType
								.getSemanticTypes(new String []{
										"Event",
										"Pathologic Function",
										"Body Substance",
										"Functional Concept",
										"Mental or Behavioral Concept",
										"Mental or Behavioral Dysfunction",
										"Finding",
										"Sign or Symptom",
										"Individual Behavior",
										"Disease or Syndrome",
										"Mental Process",
										"Body Part, Organ, or Organ Component",
										"Therapeutic or Preventive Procedure",
															   }
												)
									  );
			pseudolog.write(term.getSearchProperties().toString() + "\n");
	}
	
	private void addMesh(List<String> line, int index) {
		String queryThis = line.get(index  - 1);
		List<String> cuis = new LinkedList<String>();
		for(String word : queryThis.split("\\|")) {
			if(meshMap.containsKey(word))
				cuis.add(meshMap.get(word));
			else {
				cuis.add("");
				pseudolog.write("MESH: No exact match for \"" + word + "\"" + "\n");
			}
		}
		line.add(index, outputString(cuis, "|"));
	}
	
	private void insert(List<String> line, int index, String add) {
		line.add(index, add);
	}
	
	private String outputString(List<String> string, String delim) {
		
		StringBuffer buf = new StringBuffer();
		int lastIndex = string.size() - 1;
		
		for(int i=0;i<string.size();++i) {
			buf.append(string.get(i));
			if(i < lastIndex)
				buf.append(delim);
			else
				return buf.toString();
		}
		
		return "";
	}
	
	/**
	 * Main to run to add CUIs to the main module
	 * @param args not used
	 */
	public static void main(String[] args) {
		
		final String inputfile = "../Example-CT.gov-data-v3-v011.csv";
		final String outputfile = "../Example-CT.gov-data-v3-v011_CUIs_v2.csv";
		
		AddCuis add;
		try {
			add = new AddCuis();
			add.addCuis(inputfile, outputfile);
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		
	}

}
