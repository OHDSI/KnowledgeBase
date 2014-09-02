package edu.pitt.coder;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Component;
import java.awt.Desktop;
import java.awt.Dimension;
import java.awt.FlowLayout;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.awt.Insets;
import java.awt.Point;
import java.awt.Toolkit;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.ItemEvent;
import java.awt.event.ItemListener;
import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.PrintStream;
import java.net.URL;
import java.text.NumberFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Properties;
import java.util.Set;
import java.util.TreeSet;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;

import javax.swing.AbstractButton;
import javax.swing.Box;
import javax.swing.BoxLayout;
import javax.swing.DefaultComboBoxModel;
import javax.swing.JButton;
import javax.swing.JCheckBox;
import javax.swing.JComboBox;
import javax.swing.JComponent;
import javax.swing.JEditorPane;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JProgressBar;
import javax.swing.JScrollPane;
import javax.swing.JSeparator;
import javax.swing.JTextArea;
import javax.swing.JTextField;
import javax.swing.SwingConstants;
import javax.swing.SwingUtilities;
import javax.swing.border.EmptyBorder;
import javax.swing.border.LineBorder;
import javax.swing.border.TitledBorder;

import edu.pitt.ontology.ui.QueryTool;
import edu.pitt.ontology.ui.RepositoryManager;
import edu.pitt.terminology.Terminology;
import edu.pitt.terminology.client.IndexFinderRepository;
import edu.pitt.terminology.client.IndexFinderTerminology;
import edu.pitt.terminology.lexicon.Annotation;
import edu.pitt.terminology.lexicon.Concept;
import edu.pitt.terminology.lexicon.SemanticType;
import edu.pitt.terminology.lexicon.Source;
import edu.pitt.terminology.ui.IndexFinderLoader;
import edu.pitt.terminology.ui.TerminologyExporter;
import edu.pitt.terminology.util.DeIDUtils;
import edu.pitt.terminology.util.PathHelper;
import edu.pitt.terminology.util.TerminologyException;
import edu.pitt.text.tools.NegEx;
import edu.pitt.text.tools.TextTools;

/**
 * wrapper class that wraps NobleCoderTerminology to do stand-alon concept coding
 * @author tseytlin
 *
 */
public class NobleCoder implements ActionListener{
	private static final String DEFAULT_TERMINOLOGY_DOWNLOAD = "http://slidetutor.upmc.edu/text/data/NCI_Thesaurus.term.zip";
	private final String DEFAULT_TERMINOLOGY = "TIES_Pathology";
	private final String ABBREV_TERMINOLOGY = "BiomedicalAbbreviations";
	//private final String DEFAULT_ABBREVIATION_LIST = "AbbreviationFilter.txt";
	private final String SEMANTIC_TYPES = "/resources/SemanticTypes.txt";
	private final String RESULT_CSV = "RESULT.csv";
	private final String HTML_REPORT_LOCATION = "reports";
	private final String S = "\t";
	
	private JFrame frame;
	private JTextField input,output,semanticTypes,sources,slidingWindow,abbreviationWhitelistText,pathText;
	private JTextArea console;
	private JComboBox terminologies,searchMethods;
	private JProgressBar progress;
	private JPanel buttonPanel,options,semanticPanel,sourcePanel;
	private JButton run,b1,b2,b3;
	private File file;
	private JCheckBox stripSmallWords,stripCommonWords,stripDigits,selectBestCandidates,filterBySemanticTypes;
	private JCheckBox filterBySources,useSlidingWindow,openHTML,handleAbbreviations,handleAcronymExpansion,handleNegationDetection;
	private JCheckBox subsumptionMode,overlapMode, orderedMode, contiguousMode,partialMode,ignoreUsedWords;
	private IndexFinderRepository repository;
	private IndexFinderTerminology terminology,abbreviations;
	private long searchTime,processTime;
	private long searchCount,processCount;
	private int id=0;
	private boolean skipAbbrreviationLogic,handleAcronyms = true,handleNegation = true;
	private Map<String,String> abbreviationWhitelist,acronymList;
	private BufferedWriter htmlIndexWriter,csvWriter;
	private Set<String> allSemanticTypes;
	private RepositoryManager imanager;
	private IndexFinderLoader loader;
	private TerminologyExporter exporter;
	private PathHelper pathHelper;
	
	/**
	 * @param args
	 */
	public static void main(String[] args) throws Exception {
		try{
			NobleCoder nc = new NobleCoder();
			if(args.length == 0){
				nc.printUsage(System.out);
				nc.showDialog();
			}else{
				nc.process(Arrays.asList(args));
			}
		}catch(OutOfMemoryError ex){
			JOptionPane.showMessageDialog(null,"<html>NobleCoder ran out of memory!<br>" +
					"Try to pass more memory to JVM using <font color=green>-Xmx1G</font> flag.",
					"Error",JOptionPane.ERROR_MESSAGE);
			throw ex;
		}catch(Exception ex){
			JOptionPane.showMessageDialog(null,"<html>NobleCoder ran into a problem!<br>" +
					ex.getClass().getSimpleName()+": "+ex.getMessage(),
					"Error",JOptionPane.ERROR_MESSAGE);
			throw ex;
		}
		/*
		NobleCoder coder = new NobleCoder("TIES_Pathology");
		for(Annotation a: coder.processSentence("malignant hello melanoma hiv cm, abdominal and pelvis with HPV")){
			System.out.println(a.getConcept().getCode()+" | "+a.getConcept().getName()+" | "+a.getText()+" | "+a.getOffset());
		}*/
		/*
		NobleCoder coder = new NobleCoder("UMLS");
		for(String phrase: Arrays.asList(
			"Invasive aspergillosis (IA) is the most common life-threatening opportunistic invasive mycosis in immunocompromized patients.",
			"The reference standard was composed of the criteria given by the European Organization for Research and Treatment of Cancer (EORTC) and the Mycoses Study Group (MSG).")){
			System.out.println(phrase);
			for(Concept c: coder.processPhrase(phrase)){
				System.out.println("\t"+c.getCode()+" | "+c.getName()+" | "+c.getMatchedTerm()+" | "+Arrays.toString(c.getAnnotations()));
			}
		}
			System.out.println(coder.getDocumentAcronymMap());
		*/
		
	
			
		
	}
	
	/**
	 * print usage statement
	 */
	private void printUsage(PrintStream out) {
		out.println("Usage: java -jar NobleCoder.jar -terminology <name> -input <dir> -output <dir> [options]");
		out.println("You can invoke NobleCoder using command line as well as via UI");
		out.println("\t-terminology - terminology to use. All terminolgies are located in <user.home>/.terminologies directory.");
		out.println("\t-input\t- input directory containing a set of text files with (.txt) extension");
		out.println("\t-output\t- output directory where "+RESULT_CSV+" output will be stored along with output HTML files");
		out.println("\t-search\t- search strategy: <best-match|precise-match|all-match|nonoverlap-match|partial-match|custom-match>");
		out.println("\t-stripDigits\t- don't try to match stand-alone digits");
		out.println("\t-stripSmallWords\t- don't try to match one letter words");
		out.println("\t-stripCommonWords\t- don't try to match most common English words");
		out.println("\t-selectBestCandidates\t- for each match only select the best candidate");
		out.println("\t-semanticTypes\t- <list of semantic types> only include matches from a given semantic types");
		out.println("\t-sources\t- <list of sources> only invlude matches from a given list of sources");
		out.println("\t-slidingWindow\t- <N> don't consider words that are N words apart to be part of the same concept");
		out.println("\t-abbreviations\t- <whitelist text file> a custom text file that suppresses all abbreviations except the ones in a list");
		out.println("\t-ignoreUsedWords\t- speed up search by not considering words that are already part of some concept");
		out.println("\t-subsumptionMode\t- subsume more general concepts if more specific concept is found");
		out.println("\t-overlapMode\t- overlapping concepts are allowed");
		out.println("\t-contiguousMode\t- matched terms must be contiguous in text");
		out.println("\t-orderedMode\t- matchd terms must use the same word order in text");
		out.println("\t-partialMode\t- match a term if more then 50% of its words are found in text");
		out.println("\t-acronymExpansion\t- if acronym is found in its expanded form, use its meaning to tag all other mentions of it");
		out.println("\t-negationDetection\t- invoke NegEx algorithm to detect negated concepts");
		out.println("\n\n");
	}

	/**
	 * invoke NobleCoder pointing to a terminology .term direcotry
	 * all of the relevant settings should be set in .term/search.properties
	 * @param location
	 */
	public NobleCoder(File location) throws IOException {
		IndexFinderTerminology.setPersistenceDirectory(location.getParentFile());
		terminology = new IndexFinderTerminology(location.getName());
		setupAcronyms(location);
	}
	
	/**
	 * invoke NobleCoder pointing to a terminology .term direcotry
	 * all of the relevant settings should be set in .term/search.properties
	 * @param location
	 */
	public NobleCoder(String name) throws IOException {
		terminology = new IndexFinderTerminology(name);
		setupAcronyms(new File(IndexFinderTerminology.getPersistenceDirectory(),
		name.endsWith(IndexFinderTerminology.TERM_SUFFIX)?name:name+IndexFinderTerminology.TERM_SUFFIX));
	}
	
	/**
	 * setup acronyms
	 * @param name
	 * @throws IOException
	 */
	private void setupAcronyms(File location) throws IOException{
		// load abbreviation information
		skipAbbrreviationLogic = true;
		File props = new File(location,"search.properties");
		if(props.exists()){
			Properties p = new Properties();
			p.load(new FileInputStream(props));
			if(Boolean.parseBoolean(p.getProperty("ignore.acronyms","false"))){
				File af = new File(p.getProperty("abbreviation.whitelist"));
				if(!af.exists()){
					af = new File(location,af.getName());
					if(abbreviationWhitelistText != null){
						abbreviationWhitelistText.setText(af.getAbsolutePath());
					}
				}
				abbreviationWhitelist = loadResource(af.getAbsolutePath());
				abbreviations = (IndexFinderTerminology) new IndexFinderTerminology(
						new File(location,p.getProperty("abbreviation.terminology",ABBREV_TERMINOLOGY)).getAbsolutePath());
				skipAbbrreviationLogic = false;
			}
		}
	}
	
	/**
	 * invoke NobleCoder if you want to run it in UI mode
	 * @param location
	 */
	public NobleCoder(){}
	
	
	/**
	 * Read a list with this name and put its content into a list object
	 */	
	private Map<String,String> loadResource(String name){
		Map<String,String> list = new LinkedHashMap<String,String>();
		try{
			InputStream in = null;
			File f = new File(name);
			if(f.exists()){
				in = new FileInputStream(f);
			}else if(name.startsWith("http://")){
				in = (new URL(name)).openStream();
			}else{
				in = TextTools.class.getResourceAsStream(name);
			}
			if(in == null){
				System.err.println("ERROR: Could not load resource: "+name);
				return list;
			}	
			BufferedReader reader = new BufferedReader(new InputStreamReader(in));
			for(String line = reader.readLine();line != null;line=reader.readLine()){
				String t = line.trim();
				// skip blank lines and lines that start with #
				if(t.length() > 0 && !t.startsWith("#")){
					String [] suffixes = line.trim().split("\\t");
					if(suffixes.length >= 2)
						list.put(suffixes[0].trim(),suffixes[1].trim());
					else
						list.put(suffixes[0].trim(),null);
				}
			}
			reader.close();
			in.close();
		}catch(IOException ex){
			ex.printStackTrace();
		}
		return list;
	}
	
	/**
	 * create dialog for noble coder
	 */
	public void showDialog(){
		frame = new JFrame("NobleCoder");
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.setJMenuBar(getMenuBar());
		
		JPanel panel = new JPanel();
		panel.setLayout(new BoxLayout(panel,BoxLayout.Y_AXIS));
		GridBagConstraints c = new GridBagConstraints(0,0,1,1,1,1,GridBagConstraints.CENTER,GridBagConstraints.HORIZONTAL,new Insets(5,5,5,5),0,0);
		GridBagLayout l = new GridBagLayout();
		l.setConstraints(panel,c);
		panel.setLayout(l);
		
		terminologies = new JComboBox(getTerminologies());
		terminologies.setToolTipText("Select a terminology that will be used for coding");
		Terminology t = repository.getTerminology(DEFAULT_TERMINOLOGY);
		if(t != null)
			terminologies.setSelectedItem(t);
		
		input = new JTextField(30);
		input.setToolTipText("Select a directory with text documents (.txt) to process");
		JButton browse = new JButton("Browse");
		browse.setToolTipText("Select a directory with text documents (.txt) to process");
		browse.addActionListener(this);
		browse.setActionCommand("i_browser");
		
		JButton options = new JButton("Advanced Options");
		options.setToolTipText("Set advanced options for a given terminology");
		options.setActionCommand("options");
		options.addActionListener(this);
		
		JButton info = new JButton("Info");
		info.setToolTipText("Display information about selected terminology");
		info.setActionCommand("info");
		info.addActionListener(this);
		
		JButton query = new JButton("Query");
		query.setToolTipText("Use selected terminology to do concept search");
		query.setActionCommand("query");
		query.addActionListener(this);
		
		panel.add(new JLabel("Input Terminology"),c);c.gridx++;
		panel.add(terminologies,c);c.gridx++;
		panel.add(info,c);c.gridy++;c.gridx = 0;
		panel.add(new JLabel("Input Options"),c);c.gridx++;
		panel.add(options,c);c.gridx++;
		panel.add(query,c);c.gridy++;c.gridx=0;
		panel.add(new JLabel("Input Report Directory "),c);c.gridx++;
		panel.add(input,c);c.gridx++;
		panel.add(browse,c);c.gridx=0;c.gridy++;

		String tip = "<html>Select a directory where output will be saved<br>" +
				"Output directory will contains<ul><li><b>index.html</b> - for presenting annotated document to a human.</li>" +
				"<li><b>"+RESULT_CSV+"</b> - tabulated spreadsheet file containing all extracted concept</li></ul></html> ";
		output = new JTextField(30);
		output.setToolTipText(tip);
		browse = new JButton("Browse");
		browse.setToolTipText(tip);
		browse.addActionListener(this);
		browse.setActionCommand("o_browser");
	
		panel.add(new JLabel("Output Directory"),c);c.gridx++;
		panel.add(output,c);c.gridx++;
		panel.add(browse,c);c.gridx=0;c.gridy++;
		panel.add(Box.createRigidArea(new Dimension(10,10)),c);
		
		JPanel conp = new JPanel();
		conp.setLayout(new BorderLayout());
		conp.setBorder(new TitledBorder("Output Console"));
		console = new JTextArea(10,40);
		//console.setLineWrap(true);
		console.setEditable(false);
		conp.add(new JScrollPane(console),BorderLayout.CENTER);
		//c.gridwidth=3;		
		//panel.add(conp,c);c.gridy++;c.gridx=0;
		
		buttonPanel = new JPanel();
		buttonPanel.setLayout(new BorderLayout());
		buttonPanel.setBorder(new EmptyBorder(10,30,10,30));
		run = new JButton("Run Concept Coder");
		run.addActionListener(this);
		run.setActionCommand("run");
		buttonPanel.add(run,BorderLayout.CENTER);
		//panel.add(buttonPanel,c);
		
		progress = new JProgressBar();
		progress.setIndeterminate(true);
		progress.setString("Please Wait. It will take a while ...");
		progress.setStringPainted(true);
		
		JPanel p = new JPanel();
		p.setLayout(new BorderLayout());
		p.add(panel,BorderLayout.NORTH);
		p.add(conp,BorderLayout.CENTER);
		p.add(buttonPanel,BorderLayout.SOUTH);
		
		getOptions();
		loadDefaults();
		
		// add defaults listener
		terminologies.addItemListener(new ItemListener() {
			public void itemStateChanged(ItemEvent e) {
				loadDefaults();
			}
		});
	
		
		// wrap up, and display
		frame.setContentPane(p);
		frame.pack();
	
		//center on screen
		Dimension d = frame.getSize();
		Dimension s = Toolkit.getDefaultToolkit().getScreenSize();
		frame.setLocation(new Point((s.width-d.width)/2,(s.height-d.height)/2));
		frame.setVisible(true);
	}
	

	private JMenuBar getMenuBar() {
		JMenuBar menu = new JMenuBar();
		JMenu file = new JMenu("File");
		
		JMenuItem importer = new JMenuItem("Import ..");
		JMenuItem mmanager = new JMenuItem("Manage ..");
		JMenuItem exporter = new JMenuItem("Export ..");
		JMenuItem path = new JMenuItem("Path ..");
		importer.setToolTipText("Import Terminlogies from Different Sources");
		mmanager.setToolTipText("Query and Browse Terminlogies in Repository");
		path.setToolTipText("Change Terminology Repository Path");	
		JMenuItem exit = new JMenuItem("Exit");
		importer.addActionListener(this);
		mmanager.addActionListener(this);
		exit.addActionListener(this);
		importer.setActionCommand("importer");
		mmanager.setActionCommand("manager");
		exit.setActionCommand("exit");
		path.addActionListener(this);
		path.setActionCommand("path");
		exporter.setActionCommand("exporter");
		exporter.addActionListener(this);
		file.add(importer);
		file.add(mmanager);
		file.add(exporter);
		file.addSeparator();
		file.add(path);
		file.addSeparator();
		file.add(exit);
		menu.add(file);
		return menu;
	}

	public void actionPerformed(ActionEvent e) {
		String cmd = e.getActionCommand();
		if("run".equals(cmd)){
			doRun();
		}else if("i_browser".equals(cmd)){
			doBrowse(input);
		}else if("p_browser".equals(cmd)){
			doBrowse(pathText);
		}else if("o_browser".equals(cmd)){
			doBrowse(output);
		}else if("info".equals(cmd)){
			doInfo();
		}else if("add_source".equals(cmd)){
			doBrowse(sources);
		}else if("add_semantic_type".equals(cmd)){
			doBrowse(semanticTypes);
		}else if("add_whitelist".equals(cmd)){
			doBrowse(abbreviationWhitelistText);
		}else if("options".equals(cmd)){
			JOptionPane.showMessageDialog(frame,getOptions(),"Input Options",JOptionPane.PLAIN_MESSAGE);
		}else if(e.getSource() instanceof JCheckBox){
			syncOptions();
		}else if("importer".equals(cmd)){
			doImport();
		}else if("exporter".equals(cmd)){
			doExport();
		}else if("manager".equals(cmd)){
			doManage();
		}else if("path".equals(cmd)){
			doPath();
		}else if("exit".equals(cmd)){
			System.exit(0);
		}else if("query".equals(cmd)){
			doQuery();
		}
		
	}
	
	private void doQuery() {
		if(terminology != null){
			registerOptions();
			QueryTool tools = new QueryTool();
			tools.setTerminology(terminology);
			JOptionPane.showMessageDialog(frame,tools,"Query "+terminology.getName(),JOptionPane.PLAIN_MESSAGE);
		}else{
			JOptionPane.showMessageDialog(frame,"No Terminology Selected","Error",JOptionPane.ERROR_MESSAGE);
		}
	}

	private void doPath() {
		JPanel p = new JPanel();
		p.setLayout(new BorderLayout());
		JTextField text=  new JTextField(20);
		text.setText(IndexFinderTerminology.getPersistenceDirectory().getAbsolutePath());
		p.add(new JLabel("Repository Path  "),BorderLayout.WEST);
		p.add(text,BorderLayout.CENTER);
		JButton browse = new JButton("Browse");
		browse.addActionListener(this);
		browse.setActionCommand("p_browser");
		p.add(browse,BorderLayout.EAST);
		pathText = text;
		int r = JOptionPane.showConfirmDialog(frame,p,"Change Repository Path",JOptionPane.OK_CANCEL_OPTION,JOptionPane.PLAIN_MESSAGE);
		if(r == JOptionPane.OK_OPTION){
			IndexFinderTerminology.setPersistenceDirectory(new File(text.getText()));
			repository = null;
			SwingUtilities.invokeLater(new Runnable(){
				public void run(){
					terminologies.setModel(new DefaultComboBoxModel(getTerminologies()));
				}
			});
			
		}
	}

	private void doManage() {
		if(imanager == null){
			imanager = new RepositoryManager(RepositoryManager.TERMINOLOGIES_ONLY);
			imanager.start(repository);
			imanager.getFrame().setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
			imanager.getFrame().setLocation(frame.getLocation());
		}else{
			imanager.getFrame().setVisible(true);
		}
	}

	private void doImport() {
		if(loader == null){
			loader = new IndexFinderLoader();
			loader.showDialog();
			loader.getFrame().setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
			loader.getFrame().setLocation(frame.getLocation());
		}else{
			loader.getFrame().setVisible(true);
		}
	}

	private void doExport() {
		TerminologyExporter exporter = new TerminologyExporter(repository);
		exporter.showExportWizard(frame);
	}
	
	/**
     * Display a file in the system browser. If you want to display a file, you
     * must include the absolute path name.
     *
     * @param url
     *            the file's url (the url must start with either "http://" or
     *            "file://").
     */
     private void browseURLInSystemBrowser(String url) {
    	 Desktop desktop = Desktop.getDesktop();
    	 if( !desktop.isSupported( java.awt.Desktop.Action.BROWSE ) ) {
    		 progress("Could not open "+url+"\n");
    	 }
    	 try {
    		 java.net.URI uri = new java.net.URI( url );
    		 desktop.browse( uri );
    	 }catch ( Exception e ) {
           System.err.println( e.getMessage() );
    	 }
     }
	
	private void loadDefaults(){
		// set up defaults
		terminology = null;
		IndexFinderTerminology t = getTerminology();
		if(t != null){
			// set semantic types
			String s = "";
			for(SemanticType st: t.getFilterSemanticType()){
				s+=st.getName()+";";
			}
			if(s.length() > 0){
				filterBySemanticTypes.setSelected(true);
				semanticTypes.setEditable(true);
				semanticTypes.setText(s.substring(0,s.length()-1));
				b1.setEnabled(true);
			}else{
				filterBySemanticTypes.setSelected(false);
				semanticTypes.setText("");
			}
			// set sources
			s = "";
			for(Source st: t.getFilterSources()){
				s+=st.getName()+";";
			}
			if(s.length() > 0){
				filterBySources.setSelected(true);
				sources.setEditable(true);
				sources.setText(s.substring(0,s.length()-1));
				b2.setEnabled(true);
			}else{
				filterBySources.setSelected(false);
				sources.setText("");
			}
			
			searchMethods.setSelectedItem(t.getDefaultSearchMethod());
			stripSmallWords.setSelected(t.isIgnoreSmallWords());
			stripCommonWords.setSelected(t.isIgnoreCommonWords());
			stripDigits.setSelected(t.isIgnoreDigits());
			selectBestCandidates.setSelected(t.isSelectBestCandidate());
			useSlidingWindow.setSelected(t.getWindowSize() > 0);
			slidingWindow.setText(""+t.getWindowSize());
			handleAbbreviations.setSelected(t.isIgnoreAcronyms());
			ignoreUsedWords.setSelected(t.isIgnoreUsedWords());
			subsumptionMode.setSelected(t.isSubsumptionMode());
			overlapMode.setSelected(t.isOverlapMode());
			contiguousMode.setSelected(t.isContiguousMode());
			orderedMode.setSelected(t.isOrderedMode());
			partialMode.setSelected(t.isPartialMode());
			handleAcronymExpansion.setSelected(isAcronymExpansion());
			handleNegationDetection.setSelected(isHandleNegation());
			semanticPanel = null;
			sourcePanel = null;
			
			try {
				setupAcronyms(new File(t.getLocation()));
			} catch (IOException e) {
				e.printStackTrace();
			}
			
			syncOptions();
		}
	}
	
	private void syncOptions(){
		slidingWindow.setEditable(useSlidingWindow.isSelected());
		sources.setEditable(filterBySources.isSelected());
		semanticTypes.setEditable(filterBySemanticTypes.isSelected());
		b2.setEnabled(filterBySources.isSelected());
		b1.setEnabled(filterBySemanticTypes.isSelected());
		abbreviationWhitelistText.setEditable(handleAbbreviations.isSelected());
		b3.setEnabled(handleAbbreviations.isSelected());
		
		subsumptionMode.setEnabled(IndexFinderTerminology.CUSTOM_MATCH.equals(searchMethods.getSelectedItem()));
		overlapMode.setEnabled(IndexFinderTerminology.CUSTOM_MATCH.equals(searchMethods.getSelectedItem()));
		orderedMode.setEnabled(IndexFinderTerminology.CUSTOM_MATCH.equals(searchMethods.getSelectedItem()));
		contiguousMode.setEnabled(IndexFinderTerminology.CUSTOM_MATCH.equals(searchMethods.getSelectedItem()));
		partialMode.setEnabled(IndexFinderTerminology.CUSTOM_MATCH.equals(searchMethods.getSelectedItem()));
	}
	
	
	/**
	 * register options with selected terminology
	 */
	private void registerOptions(){
		// extrac handlers
		if(terminology != null){
			setAcronymExpansion(handleAcronymExpansion.isSelected());
			setHandleNegation(handleNegationDetection.isSelected());
		
			// initialize terminology with vaiours option
			String searchMethod = ""+searchMethods.getSelectedItem();
			terminology.setIgnoreCommonWords(stripCommonWords.isSelected());
			terminology.setIgnoreDigits(stripDigits.isSelected());
			terminology.setIgnoreSmallWords(stripSmallWords.isSelected());
			terminology.setSelectBestCandidate(selectBestCandidates.isSelected());
			terminology.setDefaultSearchMethod(searchMethod);
			terminology.setIgnoreUsedWords(ignoreUsedWords.isSelected());
			if(IndexFinderTerminology.CUSTOM_MATCH.equals(searchMethod)){
				terminology.setSubsumptionMode(subsumptionMode.isSelected());
				terminology.setOverlapMode(overlapMode.isSelected());
				terminology.setContiguousMode(contiguousMode.isSelected());
				terminology.setPartialMode(partialMode.isSelected());
				terminology.setOrderedMode(orderedMode.isSelected());
			}
			if(useSlidingWindow.isSelected()){
				int n = Integer.parseInt(slidingWindow.getText());
				terminology.setWindowSize(n);
			}
			if(filterBySemanticTypes.isSelected()){
				terminology.setFilterSemanticType(getSemanticTypes(semanticTypes.getText()));
			}else{
				terminology.setFilterSources(null);
			}
			if(filterBySources.isSelected()){
				terminology.setFilterSources(getSource(sources.getText()));
			}else{
				terminology.setFilterSources(null);
			}
				
			skipAbbrreviationLogic = true;
			terminology.setIgnoreAcronyms(false);
			if(handleAbbreviations.isSelected()){
				String path = abbreviationWhitelistText.getText();
				abbreviationWhitelist = loadResource(path);
				skipAbbrreviationLogic = false;
				terminology.setIgnoreAcronyms(true);
			}
			terminology.clearCache();
		}
	}
	
	
	private JPanel getSemanticTypePanel(){
		if(semanticPanel == null){
			semanticPanel = new JPanel();
			semanticPanel.setBackground(Color.white);
			semanticPanel.setLayout(new BoxLayout(semanticPanel,BoxLayout.Y_AXIS));
			JCheckBox all = new JCheckBox("All Semantic Types");
			all.setOpaque(false);
			all.addActionListener(new ActionListener() {
				public void actionPerformed(ActionEvent e) {
					JCheckBox all = (JCheckBox) e.getSource();
					for(int i =0; i<semanticPanel.getComponentCount();i++){
						Component c = semanticPanel.getComponent(i);
						if(c instanceof JCheckBox && c != e.getSource()){
							((JCheckBox)c).setSelected(all.isSelected());
						}
					}
				}
			});
			semanticPanel.add(all);
			semanticPanel.add(new JSeparator(SwingConstants.HORIZONTAL));
			for(String name: getAllSemanticTypes()){
				JCheckBox b = new JCheckBox(name);
				b.setOpaque(false);
				semanticPanel.add(b);
			}
		}
		return semanticPanel;
	}
	
	private JPanel getSourcePanel(){
		if(sourcePanel == null){
			sourcePanel = new JPanel();
			sourcePanel.setBackground(Color.white);
			sourcePanel.setLayout(new BoxLayout(sourcePanel,BoxLayout.Y_AXIS));
			JCheckBox all = new JCheckBox("All Sources");
			all.setOpaque(false);
			all.addActionListener(new ActionListener() {
				public void actionPerformed(ActionEvent e) {
					JCheckBox all = (JCheckBox) e.getSource();
					for(int i =0; i<sourcePanel.getComponentCount();i++){
						Component c = sourcePanel.getComponent(i);
						if(c instanceof JCheckBox && c != e.getSource()){
							((JCheckBox)c).setSelected(all.isSelected());
						}
					}
				}
			});
			sourcePanel.add(all);
			sourcePanel.add(new JSeparator(SwingConstants.HORIZONTAL));
			Terminology t = getTerminology();
			if(t != null){
				for(Source name: t.getSources()){
					JCheckBox b = new JCheckBox(name.getName());
					b.setOpaque(false);
					b.setToolTipText("<html><body><table><tr><td width=500>"+name.getDescription()+"</td></tr></table></body></html>");
					sourcePanel.add(b);
				}
			}
			sourcePanel.add(Box.createVerticalGlue());
		}
		return sourcePanel;
	}
	
	
	private JPanel getOptions() {
		if(options == null){
			options = new JPanel();
			options.setLayout(new BoxLayout(options,BoxLayout.Y_AXIS));
			
			searchMethods = new JComboBox(getSearchMethods());
			searchMethods.addItemListener(new ItemListener() {
				public void itemStateChanged(ItemEvent e) {
					syncOptions();
				}
			});
			stripSmallWords = new JCheckBox("Skip one letter words",true);
			stripCommonWords = new JCheckBox("Skip the most common English words",true);
			stripDigits = new JCheckBox("Skip digits",true);
			selectBestCandidates = new JCheckBox("Select best candidate for each matching term",true);
			useSlidingWindow = new JCheckBox("Set maximum lookup window size ");
			useSlidingWindow.addActionListener(this);
			filterBySemanticTypes = new JCheckBox("Filter by SemanticTypes");
			filterBySemanticTypes.addActionListener(this);
			filterBySources = new JCheckBox("Filter by Vocabulary Source");
			filterBySources.addActionListener(this);
			slidingWindow = new JTextField("10",3);
			semanticTypes = new JTextField(30);
			sources = new JTextField(30);
			openHTML = new JCheckBox("Open coded HTML output in the web browser",true);
			handleAbbreviations = new JCheckBox("Exclude abbreviations except the ones below",false);
			abbreviationWhitelistText = new JTextField("",30);
			handleAbbreviations.addActionListener(this);
			ignoreUsedWords = new JCheckBox("Skip already matched words in text to speed up the search");
			subsumptionMode = new JCheckBox("Subsume more general concepts if more specific concept is found");
			overlapMode = new JCheckBox("Overlapping concepts are allowed");
			contiguousMode = new JCheckBox("Matched terms must be contiguous in text");
			orderedMode = new JCheckBox("Matched terms must use the same word order in text");
			partialMode = new JCheckBox("Match a term if more then 50% of its words are found in text");
			handleAcronymExpansion = new JCheckBox("Handle acronyms found in its expanded form");
			handleNegationDetection = new JCheckBox("Handle negation detection");
			
			b1 = new JButton("+");
			b1.setActionCommand("add_semantic_type");
			b1.addActionListener(this);
		
			
			b2 = new JButton("+");
			b2.setActionCommand("add_source");
			b2.addActionListener(this);
			
			b3 = new JButton("+");
			b3.setActionCommand("add_whitelist");
			b3.addActionListener(this);
			
			JPanel p = new JPanel();
			p.setLayout(new FlowLayout(FlowLayout.LEFT));
			p.setBorder(new EmptyBorder(0,-5,0,0));
			p.add(useSlidingWindow);
			p.add(slidingWindow);
		
			JPanel p1 = new JPanel();
			p1.setLayout(new FlowLayout(FlowLayout.LEFT));
			p1.setBorder(new EmptyBorder(0,-5,0,0));
			p1.add(semanticTypes);
			p1.add(b1);
		
			JPanel p2 = new JPanel();
			p2.setLayout(new FlowLayout(FlowLayout.LEFT));
			p2.setBorder(new EmptyBorder(0,-5,0,0));
			p2.add(sources);
			p2.add(b2);
			
			JPanel p3 = new JPanel();
			p3.setLayout(new FlowLayout(FlowLayout.LEFT));
			p3.setBorder(new EmptyBorder(0,-5,0,0));
			p3.add(abbreviationWhitelistText);
			p3.add(b3);
			
			
			options.add(new JLabel("Search Method"));
			options.add(searchMethods);
			options.add(stripSmallWords);
			options.add(stripCommonWords);
			options.add(stripDigits);
			options.add(selectBestCandidates);
			options.add(p);
			options.add(ignoreUsedWords);
			options.add(subsumptionMode);
			options.add(overlapMode);
			options.add(contiguousMode);
			options.add(orderedMode);
			options.add(partialMode);
			options.add(handleAcronymExpansion);
			options.add(handleNegationDetection);
			options.add(filterBySemanticTypes);
			options.add(p1);
			options.add(filterBySources);
			options.add(p2);
			options.add(handleAbbreviations);
			options.add(p3);
			options.add(openHTML);
			
			for(Component c: options.getComponents()){
				((JComponent)c).setAlignmentX(JComponent.LEFT_ALIGNMENT);
			}
			
			syncOptions();
			
		}
		return options;
	}


	private String [] getSearchMethods() {
		Terminology t = getTerminology();
		return (t != null)?t.getSearchMethods():new String [] {""};
	}

	private void doInfo() {
		Terminology d = getTerminology();
		JEditorPane text = new JEditorPane();
		text.setContentType("text/html; charset=UTF-8");
		text.setEditable(false);
		text.setPreferredSize(new Dimension(400,400));
		text.setBorder(new LineBorder(Color.gray));
		
		String desc = "<b>"+d.getName()+"</b> "+d.getVersion()+"<br>"+d.getURI()+"<hr>"+d.getDescription();
		if(d instanceof Terminology){
			desc +="<hr>";
			Terminology t = (Terminology) d;
			desc += "Languages: "+Arrays.toString(t.getLanguages())+"<br>";
			desc += "Sources: "+Arrays.toString(t.getSources())+"<br>";

		}
		text.setText(desc);
		JOptionPane.showMessageDialog(frame,text,"",JOptionPane.PLAIN_MESSAGE);
		
	}


	private void doRun() {
		if(checkInputs())
			return;
		
		(new Thread(new Runnable(){
			public void run() {
				SwingUtilities.invokeLater(new Runnable(){
					public void run(){
						buttonPanel.removeAll();
						buttonPanel.add(progress,BorderLayout.CENTER);
						buttonPanel.validate();
						buttonPanel.repaint();
						console.setText("");
					}
				});
				
				// create a new process
				//String classpath = System.getProperty("java.class.path");
			    //String path = System.getProperty("java.home")+File.separator+"bin"+File.separator+"java";
			    
			    // build parameters
			    List<String> args = new ArrayList<String>();
			    
			    //args.add(path);
			    //args.add("-cp");
			    //args.add(classpath);
			    //args.add(NobleCoder.class.getName());
			 
			    args.add("-terminology");
			    args.add(getTerminology().getName());
			    
			    args.add("-input");
			    args.add(input.getText());
			    
			    args.add("-output");
			    args.add(output.getText());
			    
			    args.add("-search");
			    args.add(""+searchMethods.getSelectedItem());
			    
			    if(stripDigits.isSelected())
			    	args.add("-stripDigits");
			    if(stripSmallWords.isSelected())
			    	args.add("-stripSmallWords");
			    if(stripCommonWords.isSelected())
			    	args.add("-stripCommonWords");
			    if(selectBestCandidates.isSelected())
			    	args.add("-selectBestCandidates");
			    if(filterBySemanticTypes.isSelected()){
			    	args.add("-semanticTypes");
			    	args.add(semanticTypes.getText());
			    }
			    if(filterBySources.isSelected()){
			    	args.add("-sources");
			    	args.add(sources.getText());
			    }
			    if(useSlidingWindow.isSelected()){
			    	args.add("-slidingWindow");
			    	args.add(slidingWindow.getText());
			    }
			    if(handleAbbreviations.isSelected()){
			    	args.add("-abbreviations");
			    	args.add(abbreviationWhitelistText.getText());
			    }
			    if(ignoreUsedWords.isSelected())
			    	args.add("-ignoreUsedWords");
			    // customize search
			    if(IndexFinderTerminology.CUSTOM_MATCH.equals(searchMethods.getSelectedItem())){
			    	if(subsumptionMode.isSelected())
			    		args.add("-subsumptionMode");
			     	if(overlapMode.isSelected())
			    		args.add("-overlapMode");
			     	if(contiguousMode.isSelected())
			    		args.add("-contiguousMode");
			     	if(orderedMode.isSelected())
			    		args.add("-orderedMode");
			     	if(partialMode.isSelected())
			    		args.add("-partialMode");
			    }
			    // extra handlers
			    if(handleAcronymExpansion.isSelected())
			    	args.add("-acronymExpansion");
			    if(handleNegationDetection.isSelected())
			    	args.add("-negationDetection");
			    
			    // execute import
			    try{
			    	process(args);
			    }catch(Exception ex){
			    	JOptionPane.showMessageDialog(frame,ex.getMessage(),"Error",JOptionPane.ERROR_MESSAGE);
			    	ex.printStackTrace();			    	
			    }
				
				SwingUtilities.invokeLater(new Runnable(){
					public void run(){
						buttonPanel.removeAll();
						buttonPanel.add(run,BorderLayout.CENTER);
						buttonPanel.validate();
						buttonPanel.repaint();
					}
				});
				
				// open in browser
				if(openHTML != null && openHTML.isSelected()){
					browseURLInSystemBrowser(new File(output.getText()+File.separator+"index.html").toURI().toString());
				}
				
			}
		})).start();
		
	}

	protected boolean checkInputs() {
		if(input.getText().length() == 0 || output.getText().length() == 0){
			JOptionPane.showMessageDialog(frame,"Input / Output can not be blank","Error",JOptionPane.ERROR_MESSAGE);
			return true;
		}
		
		File f = new File(input.getText());
		if(!f.exists()){
			JOptionPane.showMessageDialog(frame,"Input "+f.getAbsolutePath()+" does not exist!","Error",JOptionPane.ERROR_MESSAGE);
			return true;
		}
		return false;
	}

	/**
	 * get string from check list
	 * @param p
	 * @return
	 */
	private String getCheckList(JPanel p){
		StringBuffer b = new StringBuffer();
		for(Component c: p.getComponents()){
			if(c instanceof AbstractButton && ((AbstractButton)c).isSelected()){
				b.append(((AbstractButton)c).getText()+";");
			}
		}
		return (b.length() > 0)?b.substring(0,b.length()-1):"";
	}
	
	/**
	 * get string from check list
	 * @param p
	 * @return
	 */
	private void setCheckList(JPanel p,String s){
		for(Component c: p.getComponents()){
			if(c instanceof AbstractButton){
				AbstractButton a = (AbstractButton) c;
				if(s.contains(";"+a.getText()+";") || s.startsWith(a.getText()) || s.endsWith(a.getText())){;
					a.setSelected(true);
				}else{
					a.setSelected(false);
				}
			}
		}
	}
	
	private void doBrowse(JTextField text){
		if(text == sources){
			setCheckList(getSourcePanel(),sources.getText());
			JScrollPane p = new JScrollPane(getSourcePanel());
			p.setPreferredSize(new Dimension(200,400));
			p.getVerticalScrollBar().setUnitIncrement(20);
			JOptionPane.showMessageDialog(frame,p,"Source",JOptionPane.PLAIN_MESSAGE);
			sources.setText(getCheckList(getSourcePanel()));
		}else if(text == semanticTypes) {
			setCheckList(getSemanticTypePanel(),semanticTypes.getText());
			JScrollPane p = new JScrollPane(getSemanticTypePanel());
			p.setPreferredSize(new Dimension(500,500));
			p.getVerticalScrollBar().setUnitIncrement(20);
			JOptionPane.showMessageDialog(frame,p,"Semantic Types",JOptionPane.PLAIN_MESSAGE);
			semanticTypes.setText(getCheckList(getSemanticTypePanel()));
		}else{
			JFileChooser fc = new JFileChooser(file);
			fc.setFileSelectionMode(JFileChooser.FILES_AND_DIRECTORIES);
			/*fc.setFileFilter(new FileFilter() {
				public String getDescription() {
					return "Text Documents (.txt)";
				}
				public boolean accept(File f) {
					return f.isDirectory() || f.getName().toLowerCase().endsWith(".txt");
				}
			});*/
			int r = (output == text)?fc.showSaveDialog(frame):fc.showOpenDialog(frame);
			if(r == JFileChooser.APPROVE_OPTION){
				file = fc.getSelectedFile();
				text.setText(file.getAbsolutePath());
				
				// if input, change output to default
				if(text == input){
					output.setText(new File(file.getParent()+File.separator+"Output"+File.separator+file.getName()).getAbsolutePath());
				}
			}
		}
	}
	
	private Terminology [] getTerminologies() {
		if(repository == null)
			repository =  new IndexFinderRepository();
		Terminology [] terms =  repository.getTerminologies();
		Arrays.sort(terms,new Comparator<Terminology>() {
			public int compare(Terminology o1, Terminology o2) {
				return o1.getName().compareTo(o2.getName());
			}
		});
		
		if(terms.length == 0){
			int r = JOptionPane.showConfirmDialog(frame, "<html>It appears you do not have any terminologies loaded.<br>" +
					"Would you like to download NCI Thesaurus termonology for use with NobleCoder?","Download?",JOptionPane.YES_NO_CANCEL_OPTION);
			if(JOptionPane.CANCEL_OPTION == r){
				System.exit(1);
			}else if(JOptionPane.YES_OPTION == r){
				downloadTerminology();
			}
		}
		
		return terms;
	}
	
	private void downloadTerminology(){
		(new Thread(){
			public void run(){
				try{
					URL url = new URL(DEFAULT_TERMINOLOGY_DOWNLOAD);
					InputStream is = url.openStream();
					unzip(is,IndexFinderTerminology.getPersistenceDirectory());
					repository =  new IndexFinderRepository();
					SwingUtilities.invokeLater(new Runnable() {
						public void run() {
							DefaultComboBoxModel<Terminology> model = new DefaultComboBoxModel<Terminology>();
							for(Terminology t: repository.getTerminologies()){
								model.addElement(t);
							}
							terminologies.setModel(model);
							terminologies.validate();
							terminologies.repaint();
							terminologies.setSelectedIndex(0);
							options = null;
							getOptions();
						}
					});
					
				}catch(Exception ex){
					JOptionPane.showMessageDialog(frame,"<html>Failed to download Terminology!<br>"+ex.getMessage(),"Error",JOptionPane.ERROR_MESSAGE);
					ex.printStackTrace();
				}
			}
		}).start();
	}
	
	/**
	 * unzip file to directory
	 * copy/pasted from http://javadevtips.blogspot.com/2011/10/unzip-files.html
	 * http://www.thecoderscorner.com/team-blog/java-and-jvm/12-reading-a-zip-file-from-java-using-zipinputstream
	 * and modified
	 * @param srcZipFileName
	 * @param destDirectoryName
	 * @return
	 */
	 public void unzip(InputStream is, File destDirectory) throws Exception {
		 // create the destination directory structure (if needed)
		 if(!destDirectory.exists())
			 destDirectory.mkdirs();
			 
		 // create a buffer to improve copy performance later.
	     byte[] buffer = new byte[2048];

	     // open the zip file stream
	     ZipInputStream stream = new ZipInputStream(new BufferedInputStream(is));
	     try {

	    	 // now iterate through each item in the stream. The get next
	         // entry call will return a ZipEntry for each file in the
	         // stream
	         ZipEntry entry;
	         while((entry = stream.getNextEntry())!=null) {
	        	 // Once we get the entry from the stream, the stream is
	             // positioned read to read the raw data, and we keep
	             // reading until read returns 0 or less.
	        	 File outpath =  new File(destDirectory,entry.getName());
		         if(entry.isDirectory()){
		        	 outpath.mkdirs();
	        	 }else{
		        	 if(!outpath.getParentFile().exists())
		            	 outpath.getParentFile().mkdirs();
		             FileOutputStream output = null;
		             try{
		            	 output = new FileOutputStream(outpath);
		                 int len = 0;
		                 while ((len = stream.read(buffer)) > 0){
		                	 output.write(buffer, 0, len);
		                 }
		             }finally {
		                 // we must always close the output file
		                 if(output !=null) 
		                	 output.close();
		            }
	        	}
	        }
	     }finally{
	         // we must always close the zip file.
	         stream.close();
	     }
	 }
	
	
	public IndexFinderTerminology getTerminology(){
		if(terminology == null && terminologies != null)
			terminology = (IndexFinderTerminology) terminologies.getSelectedItem();
		return terminology;
	}
	
	private IndexFinderTerminology getAbbreviations(){
		if(abbreviations == null && repository != null){
			abbreviations = (IndexFinderTerminology) repository.getTerminology(ABBREV_TERMINOLOGY);
		}
		return abbreviations;
	}
	
	public PathHelper getPathHelper(){
		if(pathHelper == null)
			pathHelper = new PathHelper(getTerminology());
		return pathHelper;
	}
	

	private SemanticType [] getSemanticTypes(String str){
		String [] p = str.split(";");
		SemanticType [] src = new SemanticType [p.length];
		for(int i=0;i<p.length;i++)
			src[i] = SemanticType.getSemanticType(p[i].trim());
		return src;
	}
	
	private Source [] getSource(String str ){
		String [] p = str.split(";");
		Source [] src = new Source [p.length];
		for(int i=0;i<p.length;i++)
			src[i] = Source.getSource(p[i].trim());
		return src;
	}
	
	/**
	 * process  documents
	 * @param args
	 */
	public void process(List<String> args) throws Exception{
		String term = args.get(args.indexOf("-terminology")+1);
		String in = args.get(args.indexOf("-input")+1);
		String out = args.get(args.indexOf("-output")+1);
		
		// set properties object
		Properties p = new Properties();
		String searchMethod = args.get(args.indexOf("-search")+1);
		p.setProperty("default.search.method",searchMethod);
		p.setProperty("ignore.small.words",""+args.contains("-stripCommonWords"));
		p.setProperty("ignore.common.words",""+args.contains("-stripCommonWords"));
		p.setProperty("ignore.digits",""+args.contains("-stripDigits"));
		p.setProperty("select.best.candidate",""+args.contains("-selectBestCandidates"));
		p.setProperty("sliding.window","0");
		p.setProperty("source.filter","");
		p.setProperty("semantic.type.filter","");
		
		p.setProperty("ignore.used.words",""+args.contains("-ignoreUsedWords"));
		p.setProperty("subsumption.mode",""+args.contains("-subsumptionMode"));
		p.setProperty("overlap.mode",""+args.contains("-overlapMode"));
		p.setProperty("contiguous.mode",""+args.contains("-contiguousMode"));
		p.setProperty("ordered.mode",""+args.contains("-orderedMode"));
		p.setProperty("partial.mode",""+args.contains("-partialMode"));
		
		// extrac handlers
		setAcronymExpansion(args.contains("-acronymExpansion"));
		setHandleNegation(args.contains("-negationDetection"));
		
		// initialize terminology with vaiours option
		terminology =  (IndexFinderTerminology) repository.getTerminology(term);
		terminology.setIgnoreCommonWords(args.contains("-stripCommonWords"));
		terminology.setIgnoreDigits(args.contains("-stripDigits"));
		terminology.setIgnoreSmallWords(args.contains("-stripSmallWords"));
		terminology.setSelectBestCandidate(args.contains("-selectBestCandidates"));
		terminology.setDefaultSearchMethod(searchMethod);
		terminology.setIgnoreUsedWords(args.contains("-ignoreUsedWords"));
		if(IndexFinderTerminology.CUSTOM_MATCH.equals(searchMethod)){
			terminology.setSubsumptionMode(Boolean.parseBoolean(p.getProperty("subsumption.mode")));
			terminology.setOverlapMode(Boolean.parseBoolean(p.getProperty("overlap.mode")));
			terminology.setContiguousMode(Boolean.parseBoolean(p.getProperty("contiguous.mode")));
			terminology.setPartialMode(Boolean.parseBoolean(p.getProperty("partial.mode")));
			terminology.setOrderedMode(Boolean.parseBoolean(p.getProperty("ordered.mode")));
		}
		
		terminology.setIgnoreAcronyms(false);
		p.setProperty("terminology.name",terminology.getName());
		
		// clear flash
		terminology.clearCache();
		
		
		int x = args.indexOf("-slidingWindow");
		if(x > -1){
			int n = Integer.parseInt(args.get(x+1));
			terminology.setWindowSize(n);
			p.setProperty("sliding.window",""+n);
		}
		x = args.indexOf("-semanticTypes");
		if(x > -1){
			terminology.setFilterSemanticType(getSemanticTypes(args.get(x+1)));
			p.setProperty("semantic.type.filter",args.get(x+1));
		}else{
			terminology.setFilterSemanticType(null);
		}
		x = args.indexOf("-sources");
		if(x > -1){
			terminology.setFilterSources(getSource(args.get(x+1)));
			p.setProperty("source.filter",args.get(x+1));
		}else{
			terminology.setFilterSources(null);
		}
		skipAbbrreviationLogic = true;
		x = args.indexOf("-abbreviations");
		if(x > -1){
			String path = args.get(x+1);
			abbreviationWhitelist = loadResource(path);
			skipAbbrreviationLogic = false;
			terminology.setIgnoreAcronyms(true);
			p.setProperty("ignore.acronyms","true");
			p.setProperty("abbreviation.whitelist",path);
			p.setProperty("abbreviation.terminology",ABBREV_TERMINOLOGY);
			
		}
		
		// process file
		List<File> files = getFiles(new File(in),new ArrayList<File>());
		if(files.isEmpty()){
			JOptionPane.showMessageDialog(frame,"No input files found","Error",JOptionPane.ERROR_MESSAGE);
			return;
		}
		
		
		
		if(progress != null){
			final int n = files.size();
			SwingUtilities.invokeLater(new Runnable(){
				public void run(){
					progress.setIndeterminate(false);
					progress.setMaximum(n);
				}
			});
		}
		Collections.sort(files);
		
		// process report
		File outputDir = new File(out);
		if(!outputDir.exists())
			outputDir.mkdirs();
		
		// reset stat counters
		processCount = 0;
		processTime = 0;
		searchTime = 0;
		
		for(int i=0;i<files.size();i++){
			processReport(files.get(i), outputDir);
			if(progress != null){
				final int n = i+1;
				SwingUtilities.invokeLater(new Runnable(){
					public void run(){
						progress.setValue(n);
					}
				});
			}
		}
		
		// save search properties
		FileOutputStream os = new FileOutputStream(new File(outputDir,"search.properties"));
		p.store(os,"NobleCoder parameters for a given run");
		os.close();
		
		// wrap up
		flush();
		
		// summary
		double ave = (processCount > 0)?processTime/processCount:0;
		progress("\nTotal process time for all reports:\t"+processTime+" ms\n");
		progress("Average process time per report:\t"+ave+" ms\n");
		progress("Average search time per phrase:\t"+(searchTime/searchCount)+" ms\n");
	}

	private List<File> getFiles(File in,List<File> list) {
		if(in.isDirectory()){
			for(File f: in.listFiles()){
				getFiles(f,list);
			}
		}else if(in.isFile()){ // && in.getName().endsWith(".txt")
			list.add(in);
			
		/*	try{
				// add text files
				String type = Files.probeContentType(in.toPath());
				if (type.equals("text/plain")) {
					list.add(in); 
				}
			}catch(NoClassDefFoundError ex){
				// if Files not there then we have Java < 1.7, then add anyway
				list.add(in);
			} catch (IOException e) {
				e.printStackTrace();
			}*/
		}
		return list;
	}


	/**
	 * parse text into sentence chunks
	 * @param text
	 * @return
	 */
	private String [] getSentences(String text){
		return text.split("\n");
	}
	
	/**
	 * get phrases
	 * @param line
	 * @return
	 */
	private String [] getPhrases(String line){
		return line.split("[\\.\\?\\!:;]");
	}
	
	private Map<String,String> getAbbreviationWhitelist(){
		if(abbreviationWhitelist == null){
			if(abbreviationWhitelistText != null){
				String d = abbreviationWhitelistText.getText();
				skipAbbrreviationLogic = true;
				if(d.length() > 0){
					abbreviationWhitelist = loadResource(d);
					if(!abbreviationWhitelist.isEmpty()){
						skipAbbrreviationLogic = false;
					}
				}
			}
			
		}
		return abbreviationWhitelist;
	}
	
	/**
	 * get a list of all emantic types
	 * @return
	 */
	private Set<String> getAllSemanticTypes(){
		if(allSemanticTypes == null){
			allSemanticTypes = new TreeSet<String>(loadResource(SEMANTIC_TYPES).keySet());
		}
		return allSemanticTypes;
	}
	
	
	/**
	 * concept code a given phrase
	 * @param phrase
	 * @return
	 */
	public Concept [] processPhrase(String phrase) throws TerminologyException {
		// concept code the phrase
		Concept [] r = getTerminology().search(phrase);
		
		// process abbreviations in expanded form
		return processAcronyms(phrase,r);
	}
	
	
	/**
	 * get a map of acronyms that were identified during parsing
	 * @return
	 */
	public Map<String,String> getAcronyms(){
		if(acronymList == null){
			acronymList = new HashMap<String, String>();
		}
		return acronymList;
	}
	
	/**
	 * clear a list of acronyms that was gathered so far.
	 */
	public void clearAcronyms(){
		acronymList = null;
	}
	
	
	/**
	 * process negation
	 * @param phrase
	 * @param foundConcepts
	 * @return
	 */
	public List<Concept> processNegation(String phrase, Concept [] foundConcepts){
		NegEx negex = new NegEx();
		negex.process(phrase,Arrays.asList(foundConcepts));
		return negex.getNegatedConcepts();
	}
	
	
	/**
	 * process abbreviations and acronyms
	 * @param phrase
	 * @param foundConcepts
	 * @return
	 * @throws TerminologyException
	 */
	private Concept [] processAcronyms(String phrase, Concept [] foundConcepts) throws TerminologyException {
		Concept [] r = foundConcepts;
		
		// handle acronyms that are mentioned in a document
		if(handleAcronyms){
			List<Concept> concepts = new ArrayList<Concept>(Arrays.asList(r));
			
			// check for acronyms in expanded form
			Matcher m = Pattern.compile("(([A-Z]?[a-z-0-9]+ )+)\\(([A-Z-0-9]+s?)\\)").matcher(TextTools.stripDiacritics(phrase));
			if(m.find()){
				String expanded = m.group(1);
				String acronym  = m.group(m.groupCount());
				expanded = getAcronymExapndedForm(expanded,acronym);
				// don't match to single words acronyms and don't match digits
				if(expanded != null && acronym.length() > 1 && !acronym.matches("\\d+")){
					Concept exp = null;
					List<Concept> acr = new ArrayList<Concept>();
					// find annotations assigned to expanded part of the acronym
					for(Concept c: r){
						if(matches(c,expanded))
							exp = c;
						else if(matches(c,acronym))
							acr.add(c);
					}
					// if expanded form was matched as a single concept
					if(exp != null){
						// fix annotations
						exp.addMatchedTerm(acronym);
						exp.setAnnotations(null);
						exp.setText(null);
						// save acronym with expanded form code
						getAcronyms().put(acronym,exp.getCode());
						// if there was a different acronym selected, then remove them
						for(Concept a: acr){
							if(!a.getCode().equals(exp.getCode()))
								concepts.remove(a);
						}
					}
				}
			}else{
				// check if acronyms exist
				for(String acronym: getAcronyms().keySet()){
					m = Pattern.compile("\\b"+acronym+"\\b").matcher(phrase);
					while(m.find()){
						// remove an already matched one
						for(Concept c: concepts){
							if(c.getMatchedTerm().equals(acronym)){
								concepts.remove(c);
								break;
							}
						}
						
						// add new concept for this acronym
						Concept c = new Concept(getAcronyms().get(acronym),acronym);
						c.setTerminology(terminology);
						c.setSearchString(phrase);
						c.setMatchedTerm(acronym);
						concepts.add(c);
					}
				}
			}
			r = concepts.toArray(new Concept [0]);
		}
		
		if(skipAbbrreviationLogic)
			return r;
		
		// look at abbreviations
		Set<String> acronyms = new HashSet<String>();
		for(Concept a: getAbbreviations().search(phrase)){
			acronyms.add(a.getName());
		}
	
		// don't do anything if nothing found
		if(acronyms.isEmpty())
			return r;
		
		// if abbreviations found
		Set<Concept> list = new LinkedHashSet<Concept>();
		for(Concept c: r){
			// add only what is not in the list
			if(!acronyms.contains(c.getMatchedTerm().toLowerCase())){
				list.add(c);
			}
		}
		// add abbreviations that are in whitelist
		for(String txt: acronyms){
			if(getAbbreviationWhitelist().containsKey(txt)){
				String cui = getAbbreviationWhitelist().get(txt);
				Concept c1 = getTerminology().lookupConcept(cui);
				if(c1 == null)
					c1 = getAbbreviations().lookupConcept(cui);
				if(c1 != null){
					c1.setSearchString(phrase);
					c1.setMatchedTerm(txt);
					list.add(c1);
				}
			}
		}
		
		return list.toArray(new Concept [0]);
	}
	
	/**
	 * is matched concept matches a string
	 * @param c
	 * @param expanded
	 * @return
	 */
	private boolean matches(Concept c, String expanded) {
		List<String> a = new ArrayList<String>(); 
		for(String s: expanded.trim().split("[^A-Za-z]+")){
			if(!TextTools.isStopWord(s))
				a.add(s);
		}
		List<String> b = new ArrayList<String>();
		for(Annotation an : c.getAnnotations()){
			b.add(an.getText());
		}
		return b.containsAll(a);
	}

	
	/**
	 * get expanded form acronym from 
	 * @param a proposed expanded form of the acronym
	 * @param a proposed acronym for the expanded form
	 * @return expanded form or null, if false matched
	 */
	private String getAcronymExapndedForm(String expanded, String acronym) {
		List<String> words = Arrays.asList(expanded.trim().split("[^A-Za-z]+"));
		
		//if(acronym.endsWith("s"))
		//	acronym = acronym.substring(0,acronym.length()-1);
		// remove non capital letters from acronym
		acronym = acronym.replaceAll("[^A-Z]", "");
		int k = 0, s =0;;
		for(int i=acronym.length()-1;i>=0;i--){
			String c = ""+acronym.charAt(i);
			int j = (words.size()-acronym.length())+i-s;
			
			// if less words then in acronym, die
			if(j >= words.size() || j < 0)
				return null;
			
			// skip stop words or empty word
			if(words.get(j).length() == 0 || TextTools.isStopWord(words.get(j))){
				j--;
				s++;
			}
			// if run out of words, quit
			if(j < 0)
				return null;
			
			// if first char of the word doesn't equal to letter of acronym, die
			if(words.get(j).length() > 0 && !c.equalsIgnoreCase(""+words.get(j).charAt(0))){
				// we might have an acronym that has several letters from each word
				if(words.get(j).toLowerCase().contains(c.toLowerCase())){
					s--;
				}else{
					return null;
				}
			}
			// increment offset
			k = expanded.lastIndexOf(words.get(j));
		}
		return expanded.substring(k);
	}


	/**
	 * process sentence
	 * @param text
	 * @return
	 * @throws TerminologyException
	 */
	public List<Annotation> processSentence(String text) throws TerminologyException {
		List<Annotation> a = new ArrayList<Annotation>();
		for(Concept c: processPhrase(text)){
			a.addAll(getAnnotations(c));
		}
		Collections.sort(a,new Comparator<Annotation>() {
			public int compare(Annotation o1, Annotation o2) {
				return o1.getOffset()-o2.getOffset();
			}
		});
		return a;
	}
	
	
	/**
	 * Get a list of contiguous concept annotations from a given concept
	 * Essentially converts a single concepts that annotates multiple related words to text
	 * to potentially multiple instances of a concept in text
	 * @param c
	 * @return
	 */
	public static List<Annotation> getAnnotations(Concept c){
		String text = c.getSearchString();
		List<Annotation> list = new ArrayList<Annotation>();
		try{
			int st = -1,en = -1,lastWordOffset = -1;
			String [] words = TextTools.getWords(text);
			//Set<String> usedWords = new HashSet<String>();
			for(Annotation a: c.getAnnotations()){
				int offs = indexOf(words,a.getText(),lastWordOffset+1);
				
				//String w = TextTools.normalize(a.getText(),true);
				// this word was encountered before, saved previous annoation
				// if the gap between last word and next word is more then 2 words,
				// it must be a seperate mention and deserves a seperate annotation
				if(lastWordOffset > -1 && (offs-lastWordOffset) > 2){
					Annotation an = new Annotation();
					an.setSearchString(text);
					an.setConcept(c);
					an.setOffset(st);
					an.setText(text.substring(st,en));
					list.add(an);
					//usedWords.clear();
					st = -1;
				}
				
				// start w/ first annotation
				if(st < 0)
					st = a.getStartPosition();
				// remember end position
				en = a.getEndPosition();
				
				//usedWords.add(w);
				lastWordOffset = offs;
			}
			// finish last annotation
			if(st >= 0 && en >= 0){
				Annotation an = new Annotation();
				an.setSearchString(text);
				an.setConcept(c);
				an.setOffset(st);
				an.setText(text.substring(st,en));
				list.add(an);
			}
		}catch(Exception ex){
			System.err.println("match: "+c.getMatchedTerm()+" | name: "+c.getName()+" | code: "+c.getCode());
			System.err.println("annotations: "+Arrays.toString(c.getAnnotations()));
			System.err.println("search: "+c.getSearchString()+"\n");
			System.err.println("error: "+ex.getMessage()+"\n");
	
		}
		return list;
	}
	
	
	private static int indexOf(String[] words, String text, int lastWordOffset) {
		for(int i=Math.max(0,lastWordOffset);i<words.length;i++){
			if(words[i].equals(text))
				return i;
		}
		return -1;
	}


	private class ResultContainer{
		public Concept [] result;
		public List<Concept> negated;
		public String text;
		public long time;
		public int offset;
	}
	
	
	
	
	public boolean isAbbrreviationFiltering() {
		return !skipAbbrreviationLogic;
	}
	
	/**
	 * set abbreviation filtering against the abbreviation terminology and white list if available.
	 * @param filter
	 */
	public void setAbbrreviationFiltering(boolean filter) {
		this.skipAbbrreviationLogic = !filter;
	}

	
	/**
	 * is acronym expansion enabled
	 * @return
	 */
	public boolean isAcronymExpansion() {
		return handleAcronyms;
	}

	/**
	 * handle acronym expansion
	 * @param handleAcronyms
	 */
	public void setAcronymExpansion(boolean handleAcronyms) {
		this.handleAcronyms = handleAcronyms;
	}

	
	
	public boolean isHandleNegation() {
		return handleNegation;
	}

	public void setHandleNegation(boolean handleNegation) {
		this.handleNegation = handleNegation;
	}

	/**
	 * process document 
	 * @param text
	 * @return
	 */
	public List<Concept> processDocument(String text) throws TerminologyException{
		clearAcronyms();
		List<Concept> result = new ArrayList<Concept>();
		for(String line: getSentences(text)){
			if(filterSentence(line)){
				continue;
			}
			// split each line into 'phrases' very stupid shallow parse
			for(String phrase: getPhrases(line)){
				phrase = phrase.trim();
				// process phrase
				if(phrase.length() > 3){
					Collections.addAll(result,processPhrase(phrase));
				}
			}
		}
		return result;
	}
	
	
	/**
	 * return true if sentence should not be parsed
	 * Ex: blank, section heading, de-id string etc..
	 * @param line
	 * @return
	 */
	private boolean filterSentence(String line){
		// skip blank lines
		if(line.length() == 0){
			return true;
		}
		// don't process section headings
		if(TextTools.isReportSection(line)){
			return true;
		}
		
		if(DeIDUtils.isDeIDHeader(line)){
			return true;
		}
		
		return false;
	}
	
	
	/**
	 * filter junk out
	 * @param line
	 * @return
	 */
	private String filterPhrase(String line){
		return DeIDUtils.filterDeIDTags(line);
	}
	
	
	/**
	 * process report
	 * @param text
	 * @param out
	 */
	private void processReport(File reportFile,File outputDir) throws Exception {
		progress("processing report ("+(processCount+1)+") "+reportFile.getName()+" ... ");
		
		// read in the report
		StringBuffer content = new StringBuffer();
		BufferedReader reader = new BufferedReader(new FileReader(reportFile));
		for(String line = reader.readLine();line != null;line = reader.readLine()){
			content.append(line.trim()+"\n");
		}
		reader.close();
		String text = content.toString();
		
		// process report (very simple shallow parse)
		Map<String,ResultContainer> resultTable = new LinkedHashMap<String,ResultContainer>();
		
		//Pattern pt = Pattern.compile("^[0-9]+,(.*)\\s+OP\\s(.*)");
		
		// go over report
		long time = System.currentTimeMillis();
		int offset = 0;
		for(String line: getSentences(text)){
			offset = text.indexOf(line.length()>3?line.substring(0,3):line,offset);
			
			// skip blank lines
			if(filterSentence(line)){
				continue;
			}
		
			// split each line into 'phrases' very stupid shallow parse
			int po = 0;
			for(String phrase: getPhrases(line)){
				phrase = phrase.trim();
				// process phrase
				if(phrase.length() > 3){
					long t1 = System.currentTimeMillis();
					ResultContainer r = new ResultContainer();
					String fphrase = filterPhrase(phrase);
					r.result = processPhrase(fphrase);
					if(!fphrase.equals(phrase)){
						for(Concept c:r.result){
							c.setSearchString(phrase);
						}
					}
					if(handleNegation)
						r.negated = processNegation(phrase,r.result);
					r.text = phrase;
					r.time = System.currentTimeMillis()-t1;
					r.offset = offset+line.indexOf(phrase.length()>3?phrase.substring(0,3):phrase,po)+1;
					searchTime += r.time;
					po+=phrase.length();
					searchCount++;
					resultTable.put(phrase,r);
				}
			}
			
			offset += line.length();
		}
		long total = System.currentTimeMillis()-time;
		processCount ++;
		processTime += total;
		
		// now output HTML for this report
		String name = reportFile.getName();
		if(name.endsWith(".txt"))
			name = name.substring(0,name.length()-".txt".length());
		
		// save HTML
		File reportDir = new File(outputDir,HTML_REPORT_LOCATION);
		if(!reportDir.exists())
			reportDir.mkdirs();
		createCodedHTMLReport(new File(reportDir,name+".html"), content.toString(), resultTable, total);
		
		// update HTML index
		getHTMLIndex(outputDir).write("<a href=\""+HTML_REPORT_LOCATION+"/"+name+".html\" target=\"frame\">"+reportFile.getName()+"</a><br>");
		
		// save CSV
		createCodedCSVReport(new File(outputDir,RESULT_CSV),name,resultTable);
		
		// do progress
		progress(total+" ms\n");
	}
	
	private void progress(String str){
		System.out.print(str);
		if(console != null){
			final String s = str;
			SwingUtilities.invokeLater(new Runnable(){
				public void run(){
					console.append(s);
				}
			});
			
		}
	}
	
	
	private BufferedWriter getHTMLIndex(File outputDirectory) throws Exception {
		if(htmlIndexWriter == null){
			// write header 
			htmlIndexWriter = new BufferedWriter(new FileWriter(new File(outputDirectory,"index.html")));
			htmlIndexWriter.write("<html xmlns=\"http://www.w3.org/1999/xhtml\">");
			htmlIndexWriter.write("<head><title>NobleCoder Annoted Output</title>\n");
			htmlIndexWriter.write("<script type=\"text/javascript\">function l(){var h=800;if(!window.innerWidth){\n");
			htmlIndexWriter.write("if(!(document.documentElement.clientWidth == 0)){\n h = document.documentElement.clientHeight;\n");
			htmlIndexWriter.write("}else{h = document.body.clientHeight;}}else{ h = window.innerHeight;} var hd = (h-100)+\"px\";\n");
			htmlIndexWriter.write("document.getElementById(\"d1\").style.maxHeight=hd;}</script>\n");
			htmlIndexWriter.write("</head><body style=\"overflow: hidden;\" bgcolor=\"#EEEEFF\" onload=\"l();\" onresize=\"l();\"><center><h3>NobleCoder Annotated Output [");
			htmlIndexWriter.write("<a href=\""+RESULT_CSV+"\" title=\"Download the entire result in CSV format\">CSV</a>]</h3></center>\n");
			htmlIndexWriter.write("<center><table bgcolor=\"#FFFFF\" width=\"100%\" height=\"95%\" border=0>\n");
			htmlIndexWriter.write("<tr><td align=\"left\" valign=\"top\" width=\"200px\" style=\"white-space: nowrap\">\n");
			htmlIndexWriter.write("<div id=\"d1\" style=\"overflow: auto; max-height: 800px;\"><div style=\"border-style:solid; border-color: #EEEEFF; padding:10px 10px;\">");
		}
		return htmlIndexWriter;
	}
	
	/**
	 * flush all writers
	 */
	private void flush() throws Exception {
		if(htmlIndexWriter != null){
			htmlIndexWriter.write("</div></div></td><td valign=top><iframe bgcolor=white frameborder=\"0\" scrolling=\"auto\" name=\"frame\" width=\"100%\" height=\"100%\"></iframe>\n");
			htmlIndexWriter.write("</td></tr></table></center></body></html>\n");
			htmlIndexWriter.flush();
			htmlIndexWriter.close();
		}
		if(csvWriter != null){
			csvWriter.close();
		}
		htmlIndexWriter = null;
		csvWriter = null;
	}
	
	
	private BufferedWriter getCSVWriter(File out) throws Exception {
		if(csvWriter == null){
			csvWriter = new BufferedWriter(new FileWriter(out));
			//csvWriter.write("Report"+S+"Matched Term"+S+"Code"+S+"Name"+S+"Semantic Type"+S+"Score"+S+"Annotations"+S+"Acronym"+S+"Search Time"+S+"Phrase\n");
			csvWriter.write("Report"+S+"Matched Term"+S+"Code"+S+"Name"+S+"Semantic Type"+S+"Annotations");
			if(handleAcronyms)
				csvWriter.write(S+"Acronym");
			if(handleNegation)
				csvWriter.write(S+"Negated");
			csvWriter.write("\n");
		}
		return csvWriter;
	}
	

	private void createCodedCSVReport(File file, String name, Map<String,ResultContainer> resultTable)  throws Exception{
		NumberFormat nf = NumberFormat.getInstance();
		nf.setMaximumFractionDigits(3);
		BufferedWriter writer = getCSVWriter(file);
		for(String text: resultTable.keySet()){
			ResultContainer r = resultTable.get(text);
			for(Concept c: r.result){
				String s = Arrays.toString(c.getSemanticTypes());
				StringBuffer a = new StringBuffer();
				for(Annotation an : c.getAnnotations()){
					a.append(an.getText()+"/"+(r.offset+an.getOffset())+", ");
				}
				if(a.length()> 0){
					a = new StringBuffer(a.substring(0,a.length()-2));
				}
				String acr = "";
				String neg = "";
				for(String ac: getAcronyms().keySet()){
					if(c.getCode().equals(getAcronyms().get(ac))){
						acr = ac;
					}
				}
				if(r.negated != null && r.negated.contains(c)){
					neg = "True";
				}
				//StringBuffer oc = new StringBuffer();
				//for(Object o: c.getCodes().values()){
				//	oc.append(o+" ");
				//}
				//csvWriter.write(name+S+c.getMatchedTerm()+S+getCode(c)+S+getName(c)+S+s.substring(1,s.length()-1)+S+
				//nf.format(c.getScore())+S+a.substring(1,a.length()-1)+S+acr+S+r.time+S+text+"\n");
				csvWriter.write(name+S+c.getMatchedTerm()+S+getCode(c)+S+getName(c)+S+s.substring(1,s.length()-1)+S+a);
				if(handleAcronyms)
					csvWriter.write(S+acr);
				if(handleNegation)
					csvWriter.write(S+neg);
				csvWriter.write("\n");
			}
		}
		writer.flush();
	}

	
	
	/**
	 * create a coded html report
	 */
	
	private void createCodedHTMLReport(File out, String content,Map<String,ResultContainer> resultTable, long total) throws Exception {
		Map<Concept,Set<Integer>> conceptReferences = new HashMap<Concept, Set<Integer>>();
		Set<Concept> result = new TreeSet<Concept>(new Comparator<Concept>() {
			public int compare(Concept o1, Concept o2) {
				return o1.getName().compareToIgnoreCase(o2.getName());
			}
		});
		for(ResultContainer r: resultTable.values()){
			Collections.addAll(result,r.result);
		}
		
		StringBuffer report = new StringBuffer();
		// go over report again to build a pretty html
		for(String line: getSentences(content)){
			// skip blank lines
			if(line.length() == 0){
				report.append("<br>");
				continue;
			}
			// don't process section headings
			if(TextTools.isReportSection(line)){
				report.append("<h4>"+line+"</h4>");
				continue;
			}
			
			// split each line into 'phrases' very stupid shallow parse
			int end = 0;
			for(String phrase: getPhrases(line)){
				phrase = phrase.trim();
				// if not form beginint
				if(end == 0){
					int st = line.indexOf(phrase);
					if(st > 0)
						report.append(line.substring(0,st-1));
				}
				
				// process phrase
				if(phrase.length() > 3){
					Concept [] r = new Concept [0];
					if(resultTable.containsKey(phrase))
						r = resultTable.get(phrase).result;
						
					// global results
					for(Concept c: r ){
						result.add(c);
					}
					
					// process phrase
					int st = line.indexOf(phrase,end);
					String s = (end > 0 && end < st)?line.substring(end,st):"";
					report.append(s+codePhrase(phrase,r, conceptReferences));
					end = st+phrase.length();
					
				}else{
					int st = line.indexOf(phrase,end);
					String s = (end > 0 && end < st)?line.substring(end,st):"";
					report.append(s+phrase);
					end = st+phrase.length();
				}
			}
			report.append("<br>");
		}
		
		StringBuffer output = new StringBuffer();
		boolean alt = true;
		for(Concept c: result){
			if(conceptReferences.containsKey(c)){
				String ids = conceptReferences.get(c).toString();
				String color = (alt)?"blue":"black";
				alt ^= true;
				output.append(codeConcept(c, color, ids));
			}
		}
		StringBuffer info = new StringBuffer();
		info.append("report process time: <b>"+total+"</b> ms , ");
		info.append("average search time: <b>"+(searchTime/searchCount)+"</b> ms , ");
		info.append("found concepts: <b>"+result.size()+"</b>");
		
		// write out results
		String name = out.getName();
		if(name.endsWith(".html"))
			name = name.substring(0,name.length()-".html".length());
		BufferedWriter htmlWriter = new BufferedWriter(new FileWriter(out));
		htmlWriter.write("<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">");
		htmlWriter.write("<html xmlns=\"http://www.w3.org/1999/xhtml\">");
		htmlWriter.write("<head><title>"+name+"</title><script type=\"text/javascript\">");
		htmlWriter.write("function h(id){for(i=0;i<id.length;i++){document.getElementById(id[i]).style.backgroundColor=\"yellow\";}}");
		htmlWriter.write("function u(id){for(i=0;i<id.length;i++){document.getElementById(id[i]).style.backgroundColor=\"white\";}}"); //</script>
		htmlWriter.write("function j(id){for(i=0;i<id.length;i++){location.href=\"#\";location.href=\"#\"+id[i];}}");
		htmlWriter.write("function l(){var h=800;if(!window.innerWidth){\n");
		htmlWriter.write("if(!(document.documentElement.clientWidth == 0)){\n h = document.documentElement.clientHeight;\n");
		htmlWriter.write("}else{h = document.body.clientHeight;}}else{ h = window.innerHeight;} var hd = (h-100)+\"px\";\n");
		htmlWriter.write("document.getElementById(\"d1\").style.maxHeight=hd;document.getElementById(\"d2\").style.maxHeight=hd;}</script>\n");
		htmlWriter.write("</head><body onload=\"l();\" onresize=\"l();\"><table width=\"100%\" style=\"table-layout:fixed;\" cellspacing=\"5\">\n"); //word-wrap:break-word;
		
		htmlWriter.write("<tr><td colspan=2 align=center><big><b>"+name+"</b></big></td></tr>\n");
		htmlWriter.write("<tr><td width=\"50%\" valign=middle><div id=\"d1\" style=\"overflow: auto; max-height: 800px; \">"+report+"</div></td>");
		htmlWriter.write("<td width=\"50%\" valign=middle><div id=\"d2\" style=\"overflow: auto; max-height: 800px;\">"+output+"</div></td></tr>\n");
		htmlWriter.write("<tr><td colspan=2 align=center>"+info+"</td></tr>\n");
		htmlWriter.flush();
		
		// finish up
		htmlWriter.write("</table></body></html>\n");
		htmlWriter.flush();
		htmlWriter.close();
	
	}
	
	/**
	 * code individual concept
	 * @param c
	 * @param color
	 * @param ids
	 * @return
	 */
	private String codeConcept(Concept c, String color, String ids){
		String code = getCode(c);
		String tip = getCode(c)+" "+Arrays.toString(c.getSemanticTypes())+"\n"+c.getDefinition();
		StringBuffer out = new StringBuffer();
		out.append("<a style=\"color:"+color+";\" onmouseover=\"h("+ids+");t=setTimeout(function(){j("+ids+");},2000);\" onmouseout=\"u("+ids+"); clearTimeout(t);\" id=\""+processCount+code+"\"");
		out.append(" href=\"http://slidetutor.upmc.edu/term/servlet/TerminologyServlet?action=lookup_concept&term=indexfinder.metathesaurus&code="+code);
		out.append("\" target=\"_blank\" title=\""+TextTools.escapeHTML(tip)+"\">"+TextTools.escapeHTML(getName(c))+"</a> &nbsp; ");
		return out.toString();
	}
	
	
	/**
	 * get UMLS code
	 * @param c
	 * @return
	 */
	private String getCode(Concept c){
		String code = c.getCode();
		if(c.getCode().matches("C\\w\\d{6}")){
			code = c.getCode();
		}else if(c.getCodes() != null){
			for(Object obj: c.getCodes().values()){
				if(obj.toString().matches("C\\w\\d{6}")){
					code = obj.toString();
					break;
				}
			}
		}
		// fix metamap hack
		Pattern pt = Pattern.compile("C9(\\d{6})");
		Matcher mt = pt.matcher(code);
		if(mt.matches())
			code = "CL"+mt.group(1);
		return code;
	}
	private String getName(Concept c){
		return c.getName();
	}
	
	
	/**
	 * format line of text
	 * @param line
	 * @param result
	 * @return
	 */
	private String codePhrase(String phrase, Concept [] result, Map<Concept,Set<Integer>> conceptReferences){
		// break phrase into 
		String [] words = TextTools.getWords(phrase);
		Map<String,List<Concept>> wordConceptMap = new HashMap<String, List<Concept>>();
		for(String word : words){
			wordConceptMap.put(word,new ArrayList<Concept>());
		}
		
		// go over the result		
		for(Concept c: result ){
			c.getText();
			int [] cWordMap = c.getWordMap();
			String [] cWords = words; //TextTools.getWords(c.getSearchString());
			for(int i=0;i<cWords.length;i++){
				if(i<cWordMap.length && cWordMap[i] > 0){
					wordConceptMap.get(cWords[i]).add(c);
				}
			}
			
		}
		
		// go over words
		StringBuffer line = new StringBuffer();
		int end = 0;
		for(String word: words){
			List<Concept> r = wordConceptMap.get(word);
			List<String> codes = new ArrayList<String>();
			String tip = "";
			// assign ids
			for(Concept c: r){
				if(!conceptReferences.containsKey(c)){
					conceptReferences.put(c,new HashSet<Integer>());
				}
				conceptReferences.get(c).add(id);
				codes.add("'"+processCount+getCode(c)+"'");
				tip += getName(c)+" ("+getCode(c)+") "+Arrays.toString(c.getSemanticTypes())+"\n";
			}
			// substitute words
			int st = phrase.indexOf(word,end);
			String s = (end > 0 && end < st)?phrase.substring(end,st):"";
			if(r.isEmpty()){
				line.append(s+word);
			}else{
				//tip = tip.substring(0,tip.length()-2);
				line.append(s+"<label id=\""+id+"\" style=\"color:green;\" onmouseover=\"h("+codes+");\" onmouseout=\"u("+codes+");\" title=\""+tip+"\">"+word+"</label>");
			}
			end = st+word.length();
			
			id++;
		}
		line.append(end > 0 && end <= phrase.length()?phrase.substring(end):"");
		return line.toString();
	}
	
}
