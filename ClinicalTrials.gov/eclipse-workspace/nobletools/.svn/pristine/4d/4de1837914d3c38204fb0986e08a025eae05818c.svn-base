package edu.pitt.terminology.ui;
import java.awt.BorderLayout;
import java.awt.Dimension;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.awt.Insets;
import java.awt.Point;
import java.awt.Toolkit;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.ItemEvent;
import java.awt.event.ItemListener;
import java.beans.PropertyChangeEvent;
import java.beans.PropertyChangeListener;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.URI;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Vector;

import javax.swing.BoxLayout;
import javax.swing.JButton;
import javax.swing.JCheckBox;
import javax.swing.JComboBox;
import javax.swing.JDialog;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JProgressBar;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;
import javax.swing.JTextField;
import javax.swing.SwingUtilities;
import javax.swing.border.EmptyBorder;
import javax.swing.border.TitledBorder;

import edu.pitt.ontology.IOntology;
import edu.pitt.ontology.bioportal.BioPortalRepository;
import edu.pitt.ontology.protege.POntology;
import edu.pitt.ontology.ui.OntologyImporter;
import edu.pitt.terminology.Terminology;
import edu.pitt.terminology.client.IndexFinderTerminology;
import edu.pitt.terminology.lexicon.Concept;
import edu.pitt.terminology.util.ConceptImporter;
import edu.pitt.terminology.util.PathHelper;





/**
 * loads IndexFinder loaders
 * @author tseytlin
 *
 */
public class IndexFinderLoader implements ItemListener, ActionListener, PropertyChangeListener {
	private final String [] FORMAT_NAMES = new String [] 
	{"UMLS/Metathesaurus RRF Directory","OWL Ontology","BioPortal Ontology","Terminology Text File","OBO Taxonomy"};
	private final String [] FORMAT_ARGS = new String [] {"-rrf","-owl","-bioportal","-txt","-obo"};
	private JFrame frame;
	private JComboBox inputFormats;
	private JTextField inputLocation,outputLocation,semanticTypeList,sourceList,languageList,memSize;
	private JTextArea console;
	private JCheckBox useStemmer,stripDigits;
	private JPanel rrfOptions,buttonPanel,commonOptions;
	private JDialog bioportalDialog;
	private OntologyImporter importer;
	private JButton run,options;
	private JLabel inputLabel;
	private JProgressBar progress;
	private File file;
	private JCheckBox createAncestors;
	private JTextField hierarchySourceList;

	/**
	 * create UI
	 */
	public void showDialog() {
		Vector<String> formats = new Vector<String>();
		Collections.addAll(formats,FORMAT_NAMES);
		frame = new JFrame("NobleCoder Terminology Loader");
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		JPanel panel = new JPanel();
		panel.setLayout(new BoxLayout(panel,BoxLayout.Y_AXIS));
		GridBagConstraints c = new GridBagConstraints(0,0,1,1,1,1,GridBagConstraints.CENTER,GridBagConstraints.HORIZONTAL,new Insets(5,5,5,5),0,0);
		GridBagLayout l = new GridBagLayout();
		l.setConstraints(panel,c);
		panel.setLayout(l);
		
		
		inputFormats = new JComboBox(formats);
		inputFormats.addItemListener(this);
		inputLabel = new JLabel("Input RRF Directory");
		inputLocation = new JTextField(30);
		JButton browse = new JButton("Browse");
		browse.addActionListener(this);
		browse.setActionCommand("i_browser");
		options = new JButton("Advanced Options");	
		options.setActionCommand("options");
		options.addActionListener(this);
		
		panel.add(new JLabel("Input Format"),c);c.gridx++;
		panel.add(inputFormats,c);c.gridy++;c.gridx = 0;
		panel.add(inputLabel,c);c.gridx++;
		panel.add(inputLocation,c);c.gridx++;
		panel.add(browse,c);c.gridx=0;c.gridy++;
		panel.add(new JLabel("Input Options"),c);c.gridx++;
		panel.add(options,c);c.gridy++;c.gridx=0;
		
		
		memSize = new JTextField(30);
		
		panel.add(new JLabel("Memory Size"),c);c.gridx++;
		panel.add(memSize,c);c.gridx=0;c.gridy++;

		
		
		outputLocation = new JTextField(30);
		browse = new JButton("Browse");
		browse.addActionListener(this);
		browse.setActionCommand("o_browser");
	
		panel.add(new JLabel("Output Location"),c);c.gridx++;
		panel.add(outputLocation,c);c.gridx++;
		panel.add(browse,c);c.gridx=0;c.gridy++;
		
		
		JPanel conp = new JPanel();
		conp.setLayout(new BorderLayout());
		conp.setBorder(new TitledBorder("Console"));
		console = new JTextArea(10,40);
		//console.setLineWrap(true);
		console.setEditable(false);
		conp.add(new JScrollPane(console),BorderLayout.CENTER);
		//c.gridwidth=3;		
		//panel.add(conp,c);c.gridy++;c.gridx=0;
		
		buttonPanel = new JPanel();
		buttonPanel.setLayout(new BorderLayout());
		buttonPanel.setBorder(new EmptyBorder(10,30,10,30));
		run = new JButton("Load IndexFinder Tables");
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
		
		
		frame.setContentPane(p);
		frame.pack();
		frame.setVisible(true);
		
		Dimension d =Toolkit.getDefaultToolkit().getScreenSize();
		Dimension s = frame.getSize();
		frame.setLocation(new Point((d.width-s.width)/2,(d.height-s.height)/2));
	}
	
	public JFrame getFrame(){
		return frame;
	}
	
	
	private void doBrowse(JTextField text){
		// if input location and BioPortal selected
		if(text == inputLocation && inputFormats.getSelectedIndex() == 2){
			final JTextField textField = text;
			(new Thread(new Runnable(){
				public void run(){
					if(bioportalDialog == null){
						importer = new OntologyImporter(new BioPortalRepository());
						bioportalDialog = importer.showImportWizard(frame);
					}else{
						bioportalDialog.setVisible(true);
					}
					while(bioportalDialog.isShowing()){
						try {
							Thread.sleep(500);
						} catch (InterruptedException e) {
							e.printStackTrace();
						}
					}
					if(importer.isSelected()){
						textField.setText(""+importer.getSelectedOntology().getURI());
					}
				}
			})).start();
		}else{
			JFileChooser fc = new JFileChooser(file);
			fc.setFileSelectionMode(JFileChooser.FILES_AND_DIRECTORIES);
			int r = (outputLocation == text)?fc.showSaveDialog(frame):fc.showOpenDialog(frame);
			if(r == JFileChooser.APPROVE_OPTION){
				file = fc.getSelectedFile();
				text.setText(file.getAbsolutePath());
			}
		}
	}
	
	private void doRun(){
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
				String classpath = System.getProperty("java.class.path");
			    String path = System.getProperty("java.home")+File.separator+"bin"+File.separator+"java";
			    
			    // check memmory parameter
			    String mem = memSize.getText();
			    
			    // build parameters
			    List<String> args = new ArrayList<String>();
			    args.add(path);
			    if(mem.length() > 0)
			    	args.add("-Xmx"+mem);
			    args.add("-cp");
			    args.add(classpath);
			    args.add(IndexFinderLoader.class.getName());
			    args.add(FORMAT_ARGS[inputFormats.getSelectedIndex()]);
			    args.add(inputLocation.getText());
			    
			    if(outputLocation.getText().length() > 0){
			    	args.add("-output");
			    	args.add(outputLocation.getText());
			    }
			    
			    if(sourceList != null && sourceList.getText().length() > 0){
			    	args.add("-sources");
			    	args.add(sourceList.getText());
			    }
			    
			    if(hierarchySourceList != null && hierarchySourceList.getText().length() > 0){
			    	args.add("-hierarchySources");
			    	args.add(hierarchySourceList.getText());
			    }
			    
			    if(semanticTypeList != null && semanticTypeList.getText().length() > 0){
			    	args.add("-semanticTypes");
			    	args.add(semanticTypeList.getText());
			    }
			    
			    if(languageList != null && languageList.getText().length() > 0){
			    	args.add("-languages");
			    	args.add(languageList.getText());
			    }
			    
			    if(useStemmer != null && useStemmer.isSelected())
			    	args.add("-stemWords");
			  
			    if(stripDigits != null && stripDigits.isSelected())
			    	args.add("-stripDigits");
			    
			    if(createAncestors != null && createAncestors.isSelected())
			    	args.add("-createAncestry");
			    
			    
			    
			    // execute import
			    execute(args);
				
				SwingUtilities.invokeLater(new Runnable(){
					public void run(){
						buttonPanel.removeAll();
						buttonPanel.add(run,BorderLayout.CENTER);
						buttonPanel.validate();
						buttonPanel.repaint();
					}
				});
				
			}
		})).start();
	}
	
	
	private void execute(List<String> args){
		try {
				load(args.toArray(new String [0]));
			} catch (Exception e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			}
		 
		/*ProcessBuilder processBuilder = new ProcessBuilder(args.toArray(new String [0]));
	    processBuilder.redirectErrorStream(true);
	    Process process;
		try {
			int r = 0;
			do{
				process = processBuilder.start();
				StreamGobbler sg = new StreamGobbler(process.getInputStream());
				sg.start();
				process.waitFor();
				r = process.exitValue();
			}while(r != 0);
		} catch (Exception e) {
			e.printStackTrace();
		}*/
	}
	
	private class StreamGobbler extends Thread {
	    private InputStream is;
	    public StreamGobbler(InputStream is){
	        this.is = is;
	    }
	    
	    public void run(){
	        try {
	            InputStreamReader isr = new InputStreamReader(is);
	            BufferedReader br = new BufferedReader(isr);
	            String line=null;
	            while ((line = br.readLine()) != null){
	            	console.append(line+"\n");
	            	/*SwingUtilities.invokeLater(new Runnable(){
	            	   public void run(){
	            		   console.repaint();
	            	   }
	            	});*/
	            }
            } catch (IOException ioe){
                ioe.printStackTrace();  
            }
	    }
	}
	
	
	private JPanel getCommonOptions(){
		if(commonOptions == null){
			commonOptions = new JPanel();
			commonOptions.setLayout(new BoxLayout(commonOptions, BoxLayout.Y_AXIS));
			commonOptions.setBorder(new TitledBorder("Common Options"));
			
			useStemmer = new JCheckBox("Stem words with a Porter Stemmer when saving term information",true);
			stripDigits = new JCheckBox("Strip digits when saving term information",false);
			createAncestors = new JCheckBox("Create ancestry cache for terminology",false);
			commonOptions.add(useStemmer);
			commonOptions.add(stripDigits);
			commonOptions.add(createAncestors);
			
		}
		return commonOptions;
	}
	
	private JPanel getRRFDialog(){
		if(rrfOptions == null){
			JPanel panel = new JPanel();
			panel.setLayout(new BoxLayout(panel,BoxLayout.Y_AXIS));
			GridBagConstraints c = new GridBagConstraints(0,0,1,1,1,1,GridBagConstraints.CENTER,GridBagConstraints.HORIZONTAL,new Insets(5,5,5,5),0,0);
			GridBagLayout l = new GridBagLayout();
			l.setConstraints(panel,c);
			panel.setLayout(l);
			
			sourceList = new JTextField(30);
			JButton browse = new JButton("Browse");
			browse.addActionListener(this);
			browse.setActionCommand("src_browser");
				
			panel.add(new JLabel("Filter by Source"),c);c.gridx++;
			panel.add(sourceList,c);c.gridx++;
			panel.add(browse,c);c.gridx=0;c.gridy++;
			
			hierarchySourceList = new JTextField(30);
			browse = new JButton("Browse");
			browse.addActionListener(this);
			browse.setActionCommand("src_browser2");
			
			panel.add(new JLabel("Filter Hierarchy by Source"),c);c.gridx++;
			panel.add(hierarchySourceList,c);c.gridx++;
			panel.add(browse,c);c.gridx=0;c.gridy++;
			
			
			semanticTypeList = new JTextField(30);
			browse = new JButton("Browse");
			browse.addActionListener(this);
			browse.setActionCommand("st_browser");
		
			panel.add(new JLabel("Filter by Semantic Type"),c);c.gridx++;
			panel.add(semanticTypeList,c);c.gridx++;
			panel.add(browse,c);c.gridx=0;c.gridy++;
			
			languageList = new JTextField("ENG",30);
			panel.add(new JLabel("Filter by Language"),c);c.gridx++;
			panel.add(languageList,c);c.gridy++;c.gridx=0;
			c.gridwidth=3;
			c.gridheight=1;
			panel.add(getCommonOptions(),c);
			
			rrfOptions = panel;
		}
		return rrfOptions;
	}
	
	
	
	
	private void doOptions(){
		JOptionPane.showMessageDialog(frame,getRRFDialog(),"RRF Options",JOptionPane.PLAIN_MESSAGE);
	}
	
	public void actionPerformed(ActionEvent e) {
		String cmd = e.getActionCommand();
		if("run".equals(cmd)){
			doRun();
		}else if("i_browser".equals(cmd)){
			doBrowse(inputLocation);
		}else if("o_browser".equals(cmd)){
			doBrowse(outputLocation);
		}else if("src_browser".equals(cmd)){
			doBrowse(sourceList);
		}else if("src_browser2".equals(cmd)){
			doBrowse(hierarchySourceList);
		}else if("st_browser".equals(cmd)){
			doBrowse(semanticTypeList);
		}else if("options".equals(cmd)){
			doOptions();
		}	
	}

	public void itemStateChanged(ItemEvent e) {
		if(e.getStateChange() == ItemEvent.SELECTED){
			options.setEnabled(false);
			switch(inputFormats.getSelectedIndex()){
			case 0: inputLabel.setText("Input RRF Directory");options.setEnabled(true);break;
			case 1: inputLabel.setText("Input OWL File");break;
			case 2: inputLabel.setText("Input URL");break;
			case 3: inputLabel.setText("Input Text File");break;
			case 4: inputLabel.setText("Input OBO File");break;
			}
		}
		
	}
	
	public void propertyChange(PropertyChangeEvent e) {
		log(e.getPropertyName()+": "+e.getNewValue());
	}
	
	/**
	 * get option from parameter list, null if not passed
	 * @param params
	 * @param option
	 * @return
	 */
	private String getOption(List<String> params, String option){
		int i = params.indexOf(option);
		if(i > -1 && i+1 < params.size()){
			return params.get(i+1);
		}
		return null;
	}
	
	/**
	 * actually load
	 */
	public void load(String [] args) throws Exception{
		List<String> params = Arrays.asList(args);
		String output = getOption(params,"-output");
		String rrf = getOption(params,"-rrf");
		String owl = getOption(params,"-owl");
		String obo = getOption(params,"-obo");
		String bioportal = getOption(params,"-bioportal");
		String txt = getOption(params,"-txt");
		String lng = getOption(params,"-languages");
		String sr = getOption(params,"-sources");
		String hsr = getOption(params,"-hierarchySources");
		String se = getOption(params,"-semanticTypes");
		boolean stemWords = params.contains("-stemWords");
		boolean stripDigits = params.contains("-stripDigits");
		boolean createAncestry = params.contains("-createAncestry");
		
		// start index finder terminology
		IndexFinderTerminology terminology = new IndexFinderTerminology();
		terminology.addPropertyChangeListener(this);
		terminology.setStemWords(stemWords);
		terminology.setIgnoreDigits(stripDigits);
		
		// setup persistance directory
		String name = null;
		if(output != null){
			File f = new File(output);
			if(f.getParentFile().exists()){
				if(f.isDirectory()){
					IndexFinderTerminology.setPersistenceDirectory(f);
				}else{
					IndexFinderTerminology.setPersistenceDirectory(f.getParentFile());
					name = f.getName();
				}
			}
		}
		
		// load approprate ontology		
		if(rrf != null){
			File f = new File(rrf);
			List<String> lang = (lng != null)?readList(lng):null;
			List<String> src =  (sr  != null)?readList(sr):null;
			List<String> hsrc =  (hsr  != null)?readList(hsr):null;
			List<String> sem =  (se  != null)?readList(se):null;
			
			// load ontology
			log("Loading RRF terminology from "+f.getAbsolutePath()+"...");
			log("Languages: "+lang);
			log("Sources: "+src);
			log("Hierarchy Sources: "+hsrc);
			log("SemanticTypes: "+sem);
			
			Map<String,List<String>> pmap = new HashMap<String,List<String>>();
			pmap.put("name",Arrays.asList(name));
			pmap.put("languages",lang);
			pmap.put("sources",src);
			pmap.put("semanticTypes",sem);
			pmap.put("hierarchySources",hsrc);
			terminology.loadRRF(f,pmap);
			name = (name == null)?f.getName():name;
		}else if(owl != null){
			log("Loading OWL terminology from "+owl+"...");
			IOntology ont = POntology.loadOntology(owl);
			if(ont != null){
				terminology.loadOntology(ont,name);
			}
			name = (name == null)?ont.getName():name;
		}else if(obo != null){
			log("Loading OBO terminology from "+obo+"...");
			if(name == null){
				name = (new File(obo)).getName();
				if(name.endsWith(".obo"))
					name = name.substring(0,name.length()-4);
			}
			terminology.load(name);
			ConceptImporter.getInstance().addPropertyChangeListener(this);
			ConceptImporter.getInstance().loadOBO(terminology,new File(obo));
			ConceptImporter.getInstance().removePropertyChangeListener(this);
			terminology.save();
		}else if(bioportal != null){
			log("Loading BioPortal terminology from "+bioportal+"...");
			BioPortalRepository r = new BioPortalRepository();
			IOntology ont = r.getOntology(URI.create(bioportal));
			if(ont != null){
				ont.addPropertyChangeListener(this);
				terminology.loadOntology(ont,name);
			}
			name = (name == null)?ont.getName():name;
		}else if(txt != null){
			log("Loading Text terminology from "+txt+"...");
			File f = new File(txt);
			terminology.loadText(f,name);
			name = (name == null)?f.getName():name;
		}
		
		//print info
		log("Testing Terminology "+name+" ...");
		
		// reopen it
		printInfo(terminology);
		
		// doing ancestry index
		if(createAncestry){
			log("Creating Ancestry Cache for "+name+" ..,");
			PathHelper ph = new PathHelper(terminology);
			ph.createAncestryCache();
		}
		
		
		log("\n\nAll Done!");
	}
	
	
	private void log(Object obj){
		System.out.println(obj);
		if(console != null){
			console.append(obj+"\n");
		}
	}
	
	
	public void printInfo(Terminology terminology) throws Exception {
		log("\n[INFO]");
		log("name:\t\t"+terminology.getName());
		log("version:\t"+terminology.getVersion());
		log("description:\t"+terminology.getDescription());
		log("location:\t"+terminology.getLocation());
		log("uri:\t\t"+terminology.getURI());
		log("languages:\t"+Arrays.toString(terminology.getLanguages()));
		log("relations:\t"+Arrays.toString(terminology.getRelations()));
		log("sources:\t"+Arrays.toString(terminology.getSources()));
		System.out.print("roots:\t");
		for(Concept c: terminology.getRootConcepts()){
			System.out.print(c.getName()+", "); 
		}
		log("\n");
	}
	
	
	private List<String> readList(String text) throws Exception {
		List<String> list = null;
		File file = new File(text);
		if(file.exists()){
			list = new ArrayList<String>();
			BufferedReader reader = new BufferedReader(new FileReader(file));
			for(String line=reader.readLine();line != null;line = reader.readLine()){
				line = line.trim();
				if(line.length() > 0)
					list.add(line);
			}
			reader.close();
		}else{
			list = Arrays.asList(text.split("[,; ]"));
		}
		return list;
	}

	/**
	 * @param args
	 */
	public static void main(String[] args){
		//args = new String [] {"-bioportal","http://bioportal.bioontology.org/ontologies/African_Traditional_Medicine"};
		//args = new String [] {"-rrf","/home/tseytlin/Data/Terminologies/NCI_Metathesaurus-201203D","-output","/home/tseytlin/Test"};
		
		IndexFinderLoader loader = new IndexFinderLoader();
		if(args.length == 0){
			loader.showDialog();
		}else{
			try{
				loader.load(args);
			}catch(Exception ex){
				ex.printStackTrace();
			}
		}
	}

	
}
