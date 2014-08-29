package edu.pitt.terminology.util;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Arrays;
import java.util.Collection;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TreeSet;

import edu.pitt.terminology.Terminology;
import edu.pitt.terminology.lexicon.Concept;
import edu.pitt.terminology.lexicon.Definition;
import edu.pitt.terminology.lexicon.SemanticType;
import edu.pitt.terminology.lexicon.Source;
import edu.pitt.terminology.lexicon.Term;
import edu.pitt.text.tools.TextTools;

/**
 * export a set of concept object to RRF files
 * @author tseytlin
 *
 */
public class ConceptExporter {
	private static ConceptExporter instance;
	private static final String I = "|";
	private static boolean append,compat = true;
	private Map<String,Integer> suiMap = new HashMap<String, Integer>();
	private Map<String,Integer> luiMap = new HashMap<String, Integer>();
	private Map<String,Integer> cuiMap = new HashMap<String, Integer>();
	private Map<String,Integer> tuiMap = new HashMap<String, Integer>();
	private int atomCount;
	
	/**
	 * get instance of this class
	 * @return
	 */
	public static ConceptExporter getInstances(){
		if(instance == null){
			instance = new ConceptExporter();
			append = false;
		}else{
			append = true;
		}
		return instance;
	}
	
	/**
	 * reset export, to overwrite files and reset LUE and SUI counts
	 */
	public void reset(){
		instance = null;
	}
	
	/**
	 * export a set of concepts to RRF files.
	 * @param concepts
	 * @param dir
	 * @throws IOException
	 */
	public void exportORF(Collection<Concept> concepts, File dir) throws IOException {
		if(!dir.exists())
			dir.mkdirs();
		
		// init buffers
		BufferedWriter mrcon = new BufferedWriter(new FileWriter(new File(dir,"MRCON"),append));
		BufferedWriter mrso = new BufferedWriter(new FileWriter(new File(dir,"MRSO"),append));
		BufferedWriter mrsty = new BufferedWriter(new FileWriter(new File(dir,"MRSTY"),append));
		BufferedWriter mrsab = new BufferedWriter(new FileWriter(new File(dir,"MRSAB"),append));
		BufferedWriter mrdef = new BufferedWriter(new FileWriter(new File(dir,"MRDEF"),append));
		BufferedWriter codes = new BufferedWriter(new FileWriter(new File(dir,"CUI2CODE"),append));

		Set<Source> sources = new TreeSet<Source>();
		Terminology term = null;
		
		// iterate over all concepts
		for(Concept c: concepts){
			String cui = getCUI(c.getCode());
			String code = c.getCode();
			
			for(Term t: c.getTerms()){
				// save term information in MRCON
				// C0002871|ENG|P|L0002871|VC|S0352787|ANEMIA|0|
				String lat = t.getLanguage() == null?"ENG":t.getLanguage();
				String ts =  t.isPreferred()?"P":"S";
				String lui = getLUI(t.getText());
				String stt = t.isPreferred()?"PF":"VO";
				String sui = getSUI(t.getText());
				String str = t.getText();
				String lrl = "0";
				
				// write out
				mrcon.write(cui+I+lat+I+ts+I+lui+I+stt+I+sui+I+str+I+lrl+I+"\n");
				mrcon.flush();
				
				// save term information in MRSO
				// C0002871|L0002871|S0013742|SNOMEDCT|OP|154786001|9|
				Source src = t.getSource();
				if(src == null && c.getSources().length > 0)
					src = c.getSources()[0];
				String sab  = src != null?src.getName():"";
				String tty = t.isPreferred()?"PT":"NP";
				//String tty = t.getForm() != null && !compat?t.getForm():"SY";
				String scode = (c.getCodes() != null && src != null && c.getCodes().containsKey(src))?""+c.getCodes().get(src):cui;
				
				mrso.write(cui+I+lui+I+sui+I+sab+I+tty+I+scode+I+lrl+I+"\n");
				mrso.flush();
			}
			
			// save MRDEF information in MRDEF
			// C0002871|CSP|subnormal levels or function of erythrocytes, resulting in symptoms of tissue hypoxia.|
			for(Definition d: c.getDefinitions()){
				Source src = d.getSource();
				if(src == null && c.getSources().length > 0)
					src = c.getSources()[0];
				String sab = src != null?src.getName():"";
				String def = d.getDefinition();
				mrdef.write(cui+I+sab+I+def+I+"\n");
				mrdef.flush();
			}
			// save MRSTY information
			// C0000005|T121|Pharmacologic Substance||
			if(compat){
				String tui = "T071";
				String sty = "Entity";
				mrsty.write(cui+I+tui+I+sty+I+"\n");
				mrsty.flush();
			}else{
				for(SemanticType st: c.getSemanticTypes()){
					String tui = getTUI(st);
					String sty = st.getName();
					mrsty.write(cui+I+tui+I+sty+I+"\n");
					mrsty.flush();
				}
			}
			// add to sources
			Collections.addAll(sources,c.getSources());	
			
			// save terminology
			if(term == null && c.getTerminology() != null)
				term = c.getTerminology();
			
			// keep track of translation
			codes.write(cui+"="+code+"\n");
			codes.flush();
		}
		
		// if possible use sources from terminology, cuase they have more data
		if(term != null && term.getSources().length > 0){
			Set<Source> tsources = new TreeSet<Source>();
			for(Source s: term.getSources()){
				if(sources.contains(s)){
					tsources.add(s);
				}
			}
			sources = tsources;
		}
		
		// write out sources
		// CL432995|C1140168|NCI2011_12E|NCI|National Cancer Institute Thesaurus, 2011_12E|NCI|2011_12E|||201112||
		// Sherri de Coronado;Center for Bioinformatics, National Cancer Institute;2115 E. Jefferson St.;6th Floor;
		// Rockville;MD;USA;20892-8335;925-377-5960;decorons@osp.nci.nih.gov|Sherri de Coronado;Center for Bioinformatics, 
		// National Cancer Institute;2115 E. Jefferson St.;6th Floor;Rockville;MD;USA;20892-8335;925-377-5960;decorons@osp.nci.nih.gov
		// |0|205092|87562|FULL-NOSIB-MULTIPLE-IGNORE-RELA|AB,AD,BN,CA2,CA3,CCN,CCS,CNU,CSN,DN,FBD,HD,OP,PT,SY|
		// Accepted_Therapeutic_Use_For,BioCarta_ID,CAS_Registry,CHEBI_ID,Chemical_Formula,Contributing_Source,Design_Note,
		// EntrezGene_ID,Essential_Amino_Acid,Essential_Fatty_Acid,Extensible_List,FDA_Table,FDA_UNII_Code,GO_Annotation,
		// GenBank_Accession_Number,Gene_Encodes_Product,Homologous_Gene,ICD-O-3_Code,INFOODS,KEGG_ID,MGI_Accession_ID,
		// Macronutrient,Micronutrient,NCBI_Taxon_ID,NSC_Code,Neoplastic_Status,Nutrient,OMIM_Number,PDQ_Closed_Trial_Search_ID,
		// PDQ_Open_Trial_Search_ID,PID_ID,PubMedID_Primary_Reference,Swiss_Prot,Tolerable_Level,USDA_ID,US_Recommended_Intake,Unit,
		// Use_For,miRBase_ID|ENG|UTF-8|Y|Y|NCI Thesaurus|National Cancer Institute, National Institutes of Health;NCI Thesaurus;
		// Sherri de Coronado, decorons@osp.nci.nih.gov;December 2011, Protege version;Rockville, MD|
		for(Source src : sources){	
			String def = src.getDescription();
			if(def != null){
				int x = def.indexOf(".");
				if(x > -1){
					def = def.substring(0,x);
				}
			}
			String vcui = "";
			String rcui = src.getCode() != null?src.getCode():"";
			String vsab = "";// versioned abbreviation
			String rsab = src.getName(); // abbreviation
			String son  = def != null?def:""; // official name
			String sf = src.getName(); // source family
			String sver = "";
			String vstart = "";
			String vend = "";
			String imeta ="";
			String rmeta = "";
			String slc = "";
			String scc = "";
			String srl = "0";
			String tfr = ""; //term frequence
			String cfr = ""; // concept frequency
			String cxty = "";
			String ttyl = "";
			String atnl = "";
			String lat = "ENG";
			String cenc = "UTF-8";
			String curver = "Y";
			String sabin = "Y";
						
			mrsab.write(vcui+I+rcui+I+vsab+I+rsab+I+son+I+sf+I+sver+I+vstart+I+vend+I+imeta+I+rmeta+I+slc+I+scc+I+srl+I+tfr+I+cfr+
						I+cxty+I+ttyl+I+atnl+I+lat+I+cenc+I+curver+I+sabin+I+"\n");
			
		}
		
		
		// create other empty files
		List<String> otherFiles = Arrays.asList("SM.DB","MRRANK","MRSAT");
		for(String file: otherFiles){
			BufferedWriter writer = new BufferedWriter(new FileWriter(new File(dir,file)));
			writer.write("");
			writer.close();
		}
		
		// close all files
		mrcon.close();
		mrso.close();
		mrsty.close();
		mrdef.close();
		mrsab.close();
		codes.close();
	}
	
	/**
	 * export a set of concepts to RRF files.
	 * @param concepts
	 * @param dir
	 * @throws IOException
	 */
	public void exportRRF(Collection<Concept> concepts, File dir) throws IOException {
		if(!dir.exists())
			dir.mkdirs();
		
		// init buffers
		BufferedWriter mrconso = new BufferedWriter(new FileWriter(new File(dir,"MRCONSO.RRF"),append));
		BufferedWriter mrsty = new BufferedWriter(new FileWriter(new File(dir,"MRSTY.RRF"),append));
		BufferedWriter mrdef = new BufferedWriter(new FileWriter(new File(dir,"MRDEF.RRF"),append));
		BufferedWriter mrsab = new BufferedWriter(new FileWriter(new File(dir,"MRSAB.RRF"),append));
		BufferedWriter codes = new BufferedWriter(new FileWriter(new File(dir,"CUI2CODE"),append));

		Set<Source> sources = new TreeSet<Source>();
		Terminology term = null;
		
		// iterate over all concepts
		for(Concept c: concepts){
			String cui = getCUI(c.getCode());
			String code = c.getCode();
			
			// save term information in MRCONSO
			// C0000005|ENG|P|L0187013|PF|S2192303|Y|A4332670||M0019694|D012711|MSH|EN|D012711|(131)I-MAA|0|N||
			for(Term t: c.getTerms()){
				Source src = t.getSource();
				if(src == null && c.getSources().length > 0)
					src = c.getSources()[0];
				String lat = t.getLanguage() == null?"ENG":t.getLanguage();
				String ts =  t.isPreferred()?"P":"S";
				String lui = getLUI(t.getText());
				String stt = t.isPreferred()?"PF":"VO";
				String sui = getSUI(t.getText());
				String pref = t.isPreferred()?"Y":"N";
				String aui = String.format("A%07d",atomCount);
				String saui = "";
				String scui = "";
				String sdui = "";
				String sab  = src != null?src.getName():"";
				String tty = t.getForm() != null?t.getForm():"SY";
				String scode = (c.getCodes() != null && src != null && c.getCodes().containsKey(src))?""+c.getCodes().get(src):cui;
				String str = t.getText();
				String srl = "0";
				String sup  = "N";
				String cvf = "";
				
				// write out
				mrconso.write(cui+I+lat+I+ts+I+lui+I+stt+I+sui+I+pref+I+aui+I+saui+I+scui+I+sdui+I+sab+I+tty+I+scode+I+str+I+srl+I+sup+I+cvf+"\n");
				mrconso.flush();
				atomCount ++;
			}
			// save MRDEF information in MRDEF
			// C0000107|A3857241|AT22515555||MSH|An ANGIOTENSIN II analog which acts as a highly specific inhibitor of ANGIOTENSIN TYPE 1 RECEPTOR.|N||
			for(Definition d: c.getDefinitions()){
				Source src = d.getSource();
				if(src == null && c.getSources().length > 0)
					src = c.getSources()[0];
				String aui = "";
				String atui = "";
				String satui = "";
				String sab = src != null?src.getName():"";
				String def = d.getDefinition();
				String sup = "N";
				String cvf = "";
				mrdef.write(cui+I+aui+I+atui+I+satui+I+sab+I+def+I+sup+I+cvf+"\n");
				mrdef.flush();
			}
			// save MRSTY information
			// C0000005|T121|A1.4.1.1.1|Pharmacologic Substance|AT16627324||
			for(SemanticType st: c.getSemanticTypes()){
				String tui = getTUI(st);
				String stn = "";
				String sty = st.getName();
				String atui = "";
				String cvf = "";
				mrsty.write(cui+I+tui+I+stn+I+sty+I+atui+I+cvf+"\n");
				mrsty.flush();
			}
			// add to sources
			Collections.addAll(sources,c.getSources());	
			
			// save terminology
			if(term == null && c.getTerminology() != null)
				term = c.getTerminology();
			
			// keep track of translation
			codes.write(cui+"="+code+"\n");
			codes.flush();
		}
		
		// if possible use sources from terminology, cuase they have more data
		if(term != null && term.getSources().length > 0){
			Set<Source> tsources = new TreeSet<Source>();
			for(Source s: term.getSources()){
				if(sources.contains(s)){
					tsources.add(s);
				}
			}
			sources = tsources;
		}
		
		// write out sources
		// CL432995|C1140168|NCI2011_12E|NCI|National Cancer Institute Thesaurus, 2011_12E|NCI|2011_12E|||201112||
		// Sherri de Coronado;Center for Bioinformatics, National Cancer Institute;2115 E. Jefferson St.;6th Floor;
		// Rockville;MD;USA;20892-8335;925-377-5960;decorons@osp.nci.nih.gov|Sherri de Coronado;Center for Bioinformatics, 
		// National Cancer Institute;2115 E. Jefferson St.;6th Floor;Rockville;MD;USA;20892-8335;925-377-5960;decorons@osp.nci.nih.gov
		// |0|205092|87562|FULL-NOSIB-MULTIPLE-IGNORE-RELA|AB,AD,BN,CA2,CA3,CCN,CCS,CNU,CSN,DN,FBD,HD,OP,PT,SY|
		// Accepted_Therapeutic_Use_For,BioCarta_ID,CAS_Registry,CHEBI_ID,Chemical_Formula,Contributing_Source,Design_Note,
		// EntrezGene_ID,Essential_Amino_Acid,Essential_Fatty_Acid,Extensible_List,FDA_Table,FDA_UNII_Code,GO_Annotation,
		// GenBank_Accession_Number,Gene_Encodes_Product,Homologous_Gene,ICD-O-3_Code,INFOODS,KEGG_ID,MGI_Accession_ID,
		// Macronutrient,Micronutrient,NCBI_Taxon_ID,NSC_Code,Neoplastic_Status,Nutrient,OMIM_Number,PDQ_Closed_Trial_Search_ID,
		// PDQ_Open_Trial_Search_ID,PID_ID,PubMedID_Primary_Reference,Swiss_Prot,Tolerable_Level,USDA_ID,US_Recommended_Intake,Unit,
		// Use_For,miRBase_ID|ENG|UTF-8|Y|Y|NCI Thesaurus|National Cancer Institute, National Institutes of Health;NCI Thesaurus;
		// Sherri de Coronado, decorons@osp.nci.nih.gov;December 2011, Protege version;Rockville, MD|
		for(Source src : sources){	
			String def = src.getDescription();
			if(def != null){
				int x = def.indexOf(".");
				if(x > -1){
					def = def.substring(0,x);
				}
			}
			String vcui = "";
			String rcui = src.getCode() != null?src.getCode():"";
			String vsab = "";// versioned abbreviation
			String rsab = src.getName(); // abbreviation
			String son  = def != null?def:""; // official name
			String sf = src.getName(); // source family
			String sver = "";
			String vstart = "";
			String vend = "";
			String imeta ="";
			String rmeta = "";
			String slc = "";
			String scc = "";
			String srl = "0";
			String tfr = ""; //term frequence
			String cfr = ""; // concept frequency
			String cxty = "";
			String ttyl = "";
			String atnl = "";
			String lat = "ENG";
			String cenc = "UTF-8";
			String curver = "Y";
			String sabin = "Y";
			String ssn = son;
			String scit= src.getDescription();
						
			mrsab.write(vcui+I+rcui+I+vsab+I+rsab+I+son+I+sf+I+sver+I+vstart+I+vend+I+imeta+I+rmeta+I+slc+I+scc+I+srl+I+tfr+I+cfr+
						I+cxty+I+ttyl+I+atnl+I+lat+I+cenc+I+curver+I+sabin+I+ssn+I+scit+"\n");
			
		}
		
		// create other empty files
		List<String> otherFiles = Arrays.asList("MRAUI.RRF","MRCOC.RRF","MRCOLS.RRF","MRCUI.RRF","MRDOC.RRF","MRFILES.RRF","MRHIER.RRF","MRHIST.RRF",
				"MRMAP.RRF","MRRANK.RRF","MRREL.RRF","MRSAT.RRF","MRSMAP.RRF","MRXNS_ENG.RRF","MRXNW_ENG.RRF","MRXW_ENG.RRF","release.dat");
		for(String file: otherFiles){
			BufferedWriter writer = new BufferedWriter(new FileWriter(new File(dir,file)));
			writer.write("");
			writer.close();
		}
		
		// close all files
		mrconso.close();
		mrsty.close();
		mrdef.close();
		mrsab.close();
		codes.close();
	}
	
	private String getSUI(String text) {
		if(suiMap.containsKey(text))
			return String.format("S%07d",suiMap.get(text));
		int id = suiMap.size();
		suiMap.put(text,id);
		return String.format("S%07d",id);
	}

	private String getLUI(String text) {
		text = TextTools.normalize(text,true);
		if(luiMap.containsKey(text))
			return String.format("L%07d",luiMap.get(text));
		int id = luiMap.size();
		luiMap.put(text,id);
		return String.format("L%07d",id);
	}
	
	private String getCUI(String code) {
		if(code.matches("[A-Z]\\d{7}"))
			return code;
		if(cuiMap.containsKey(code))
			return String.format("C%07d",cuiMap.get(code));
		int id = cuiMap.size();
		cuiMap.put(code,id);
		return String.format("C%07d",id);
	}
	
	private String getTUI(SemanticType st) {
		if(st.getCode() != null && st.getCode().matches("T\\d{3}"))
			return st.getCode();
		
		String text = st.getName();
		if(tuiMap.containsKey(text))
			return String.format("T%03d",tuiMap.get(text));
		int id = tuiMap.size();
		tuiMap.put(text,id);
		return String.format("T%03d",id);
	}
}
