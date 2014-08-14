package edu.pitt.info.extract;

import java.awt.BorderLayout;
import java.awt.Desktop;
import java.awt.Dimension;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.awt.Insets;
import java.awt.Point;
import java.awt.Toolkit;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.net.URL;
import java.util.ArrayList;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import javax.swing.Box;
import javax.swing.BoxLayout;
import javax.swing.DefaultListModel;
import javax.swing.JButton;
import javax.swing.JEditorPane;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JList;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JProgressBar;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;
import javax.swing.JTextField;
import javax.swing.SwingUtilities;
import javax.swing.border.EmptyBorder;
import javax.swing.border.TitledBorder;
import javax.swing.filechooser.FileFilter;
import javax.swing.text.html.HTMLDocument;

import edu.pitt.info.extract.model.AnnotatedDocument;
import edu.pitt.info.extract.model.DocumentFilter;
import edu.pitt.info.extract.model.ItemInstance;
import edu.pitt.info.extract.model.Template;
import edu.pitt.info.extract.model.TemplateFactory;
import edu.pitt.info.extract.model.TemplateItem;
import edu.pitt.terminology.CompositTerminology;
import edu.pitt.terminology.client.IndexFinderTerminology;
import edu.pitt.terminology.lexicon.Annotation;
import edu.pitt.terminology.lexicon.Concept;
import edu.pitt.text.tools.TextTools;


/**
 * process a set of reports and generate an HTML to get
 * @author tseytlin
 *
 */
public class InformationExtractor implements ActionListener {
	private static final String RESULT_FILE = "_RESULT_.csv";
	private final String S = "|";
	private JFrame frame;
	private JTextField input,output;
	private JList<Template> templateList;
	private JTextArea console;
	private JProgressBar progress;
	private JPanel buttonPanel;
	private JButton run;
	private File file;
	private long processTime;
	private long processCount;
	private int id=0;
	private BufferedWriter htmlIndexWriter,csvWriter;
	private TemplateFactory templateFactory;
	
	/**
	 * What 
	 * @param args
	 */
	public static void main(String[] args) throws Exception {
		InformationExtractor nc = new InformationExtractor();
		if(args.length == 0){
			nc.showDialog();
		}else{
			//nc.process(args[0],args[1],args[2]);
		}
	}

	
	/**
	 * int report processor for a given ontology
	 * @param ont
	 */
	public InformationExtractor(){
		templateFactory = TemplateFactory.getInstance();
	}
	

		
	
	/**
	 * create dialog for noble coder
	 */
	public void showDialog(){
		frame = new JFrame("Information Extractor");
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.setJMenuBar(getMenuBar());
		
		JPanel panel = new JPanel();
		panel.setLayout(new BoxLayout(panel,BoxLayout.Y_AXIS));
		GridBagConstraints c = new GridBagConstraints(0,0,1,1,1,1,GridBagConstraints.CENTER,GridBagConstraints.HORIZONTAL,new Insets(5,5,5,5),0,0);
		GridBagLayout l = new GridBagLayout();
		l.setConstraints(panel,c);
		panel.setLayout(l);
		
		input = new JTextField(30);
		templateList = new JList(new DefaultListModel<Template>());
		JButton browse = new JButton("Browse");
		browse.addActionListener(this);
		browse.setActionCommand("i_browser");
	
		
		JButton export = new JButton("Export");
		export.setActionCommand("export");
		export.addActionListener(this);
		JButton add = new JButton("Import");
		add.setActionCommand("import");
		add.addActionListener(this);
		JButton info = new JButton("Preview");
		info.setActionCommand("preview");
		info.addActionListener(this);
		JScrollPane scroll = new JScrollPane(templateList);
		scroll.setPreferredSize(new Dimension(100,100));
		
		panel.add(new JLabel("Input Template(s)"),c);c.gridx++;c.gridheight=3;
		panel.add(scroll,c);c.gridx++;c.gridheight=1;
		panel.add(add,c);c.gridy++;
		panel.add(export,c);c.gridy++;
		panel.add(info,c);c.gridy++;
		c.gridx = 0;
		panel.add(new JLabel("Input Report Directory "),c);c.gridx++;
		panel.add(input,c);c.gridx++;
		panel.add(browse,c);c.gridx=0;c.gridy++;

		output = new JTextField(30);
		browse = new JButton("Browse");
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
		run = new JButton("Run Information Extractor");
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
		
			
		// wrap up, and display
		frame.setContentPane(p);
		frame.pack();
	
		//center on screen
		Dimension d = frame.getSize();
		Dimension s = Toolkit.getDefaultToolkit().getScreenSize();
		frame.setLocation(new Point((s.width-d.width)/2,(s.height-d.height)/2));
		frame.setVisible(true);
		
		// load defaults
		loadDeafaults();
	}	
	
	/**
	 * 
	 * @return
	 */
	private void loadDeafaults(){
		(new Thread(new Runnable(){
			public void run(){
				setBusy(true);
				try {
					List<URL> urls = new ArrayList<URL>();
					urls.add(new URL("http://slidetutor.upmc.edu/curriculum/templates/InvasiveMelanoma.template"));
					urls.add(new URL("http://slidetutor.upmc.edu/curriculum/templates/GeneMutations.template"));
					
					for(URL u: urls){
						templateFactory.importTemplate(u.openStream());
					}
					//templateFactory.importTemplates("http://slidetutor.upmc.edu/curriculum/owl/skin/PITT/Melanocytic.owl");
					/*
					File f = new File(NobleCoderTerminology.getPersistenceDirectory(),"GeneMutations.term");
					if(f.exists())
						templateFactory.importTemplates("GeneMutations");
					*/
					
				} catch (Exception e) {
					e.printStackTrace();
				}
				refreshTemplateList();
				//input.setText("/home/tseytlin/Data/Reports/ReportProcessorInput/");
				//output.setText("/home/tseytlin/Data/Reports/Output/ReportProcessorInput/");
				setBusy(false);
			}
		})).start();
	}
	
	private void refreshTemplateList(){
		SwingUtilities.invokeLater(new Runnable(){
			public void run(){
				((DefaultListModel<Template>)templateList.getModel()).removeAllElements();
				for(Template t: templateFactory.getTemplates()){
					((DefaultListModel<Template>)templateList.getModel()).addElement(t);
				}
				templateList.validate();
			}
		});
	}
	
	
	/**
	 * set busy 
	 * @param b
	 */
	private void setBusy(boolean b){
		final boolean busy = b;
		SwingUtilities.invokeLater(new Runnable(){
			public void run(){
				buttonPanel.removeAll();
				if(busy){
					progress.setIndeterminate(true);
					progress.setString("Please Wait. It may take a while ...");
					progress.setStringPainted(true);
					buttonPanel.add(progress,BorderLayout.CENTER);
					console.setText("");
				}else{
					buttonPanel.add(run,BorderLayout.CENTER);
				}
				buttonPanel.validate();
				buttonPanel.repaint();
				
			}
		});
	}
	

	private JMenuBar getMenuBar() {
		JMenuBar menu = new JMenuBar();
		JMenu file = new JMenu("File");
		JMenuItem exit = new JMenuItem("Exit");
		exit.addActionListener(this);
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
		}else if("d_browser".equals(cmd)){
			
		}else if("o_browser".equals(cmd)){
			doBrowse(output);
		}else if("exit".equals(cmd)){
			System.exit(0);
		}else if("export".equals(cmd)){
			doExport();
		}else if("import".equals(cmd)){
			doImport();
		}else if("preview".equals(cmd)){
			doPreview();
		}
	}
	
	/**
	 * do preview
	 */
	private void doPreview() {
		Template t = templateList.getSelectedValue();
		if(t == null)
			return;
		
		StringBuffer b = new StringBuffer();
		b.append("<h2>"+t.getName()+"</h2>");
		b.append(t.getDescription()+"<hr>");
		b.append("<ul>");
		for(TemplateItem i: t.getTemplateItems()){
			b.append("<li><b>"+i.getName()+"</b>"); 
		}
		b.append("</ul>");
		
		JEditorPane text = new JEditorPane();
		text.setContentType("text/html; charset=UTF-8");
		HTMLDocument doc = (HTMLDocument) text.getDocument();
		doc.getStyleSheet().addRule("body { font-family: sans-serif;");
		text.setText(b.toString());
		JPanel msg = new JPanel();
		msg.setLayout(new BorderLayout());
		msg.setPreferredSize(new Dimension(500,500));
		msg.add(new JScrollPane(text),BorderLayout.CENTER);
		JOptionPane.showMessageDialog(frame,msg,"Preview",JOptionPane.PLAIN_MESSAGE);
	}


	/**
	 * do export of highlighted template
	 */
	private void doExport() {
		Template template = templateList.getSelectedValue();
		if(template != null){
			JFileChooser chooser = new JFileChooser();
			chooser.setFileFilter(new FileFilter(){
				public boolean accept(File f) {
					return f.isDirectory() || f.getName().endsWith(".template");
				}
				public String getDescription() {
					return "Template XML File";
				}
				
			});
			chooser.setSelectedFile(new File(template.getName()+".template"));
			int r = chooser.showSaveDialog(frame);
			if(r == JFileChooser.APPROVE_OPTION){
				try{
					File f = chooser.getSelectedFile();
					FileOutputStream out = new FileOutputStream(f);
					templateFactory.exportTemplate(template, out);
					out.close();
				}catch(Exception ex){
					JOptionPane.showMessageDialog(frame,ex.getMessage(),"Error",JOptionPane.ERROR_MESSAGE);
					ex.printStackTrace();
				}
			}
		}
	}
	
	/**
	 * do export of highlighted template
	 */
	private void doImport() {
		JFileChooser chooser = new JFileChooser();
		chooser.setFileFilter(new FileFilter(){
			public boolean accept(File f) {
				return f.isDirectory() || f.getName().endsWith(".template");
			}
			public String getDescription() {
				return "Template XML File";
			}
			
		});
		int r = chooser.showOpenDialog(frame);
		if(r == JFileChooser.APPROVE_OPTION){
			try{
				File f = chooser.getSelectedFile();
				FileInputStream in  = new FileInputStream(f);
				templateFactory.importTemplate(in);
				in.close();
				refreshTemplateList();
			}catch(Exception ex){
				JOptionPane.showMessageDialog(frame,ex.getMessage(),"Error",JOptionPane.ERROR_MESSAGE);
				ex.printStackTrace();
			}
		}
		
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
	
	
     /**
      * check UI inputs
      * @return
      */
    private boolean checkInputs(){
 		if(templateList.getSelectedValuesList().isEmpty()){
			JOptionPane.showMessageDialog(frame,"Please Select Templates");
			return false;
		}
		if(!new File(input.getText()).exists()){
			JOptionPane.showMessageDialog(frame,"Please Select Input Report Directory");
			return false;
		}
		return true;
    }
     
    /**
     * run the damn thing
     */
	private void doRun() {
		(new Thread(new Runnable(){
			public void run() {
				if(!checkInputs()){
					return;
				}
				setBusy(true);
				
				
				try {
					process(getSelectedValuesList(),input.getText(),output.getText());
				} catch (Exception e) {
					e.printStackTrace();
				}
				
				setBusy(false);
				
				// open in browser
				browseURLInSystemBrowser(new File(output.getText()+File.separator+"index.html").toURI().toString());
				
			}
		})).start();
	}

	private List<Template> getSelectedValuesList(){
		List<Template> list = new ArrayList<Template>();
		for(Object o: templateList.getSelectedValues()){
			list.add((Template) o);
		}
		return list;
	}
	
	
	private void doBrowse(JTextField text){
		//if(text == domain){
		//	
		//}else{
			JFileChooser fc = new JFileChooser(file);
			fc.setFileSelectionMode(JFileChooser.FILES_AND_DIRECTORIES);
			int r = (output == text)?fc.showSaveDialog(frame):fc.showOpenDialog(frame);
			if(r == JFileChooser.APPROVE_OPTION){
				file = fc.getSelectedFile();
				text.setText(file.getAbsolutePath());
				
				// if input, change output to default
				if(text == input){
					output.setText(new File(file.getParent()+File.separator+"Output"+File.separator+file.getName()).getAbsolutePath());
				}
			}
		//}
	}

	/**
	 * process  documents
	 * @param args
	 */
	public void process(List<Template> templates,String in, String out) throws Exception{	
		// process file
		List<File> files = getFiles(new File(in),new ArrayList<File>());
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
		
		for(int i=0;i<files.size();i++){
			processReport(templates,files.get(i), outputDir);
			if(progress != null){
				final int n = i+1;
				SwingUtilities.invokeLater(new Runnable(){
					public void run(){
						progress.setValue(n);
					}
				});
			}
		}
		
		
		// wrap up
		flush();
		
		// summary
		progress("\nTotal process time for all reports:\t"+processTime+" ms\n");
		progress("Average process time per report:\t"+(processTime/processCount)+" ms\n");
		//progress("Average search time per phrase:\t"+(searchTime/searchCount)+" ms\n");
	}

	private List<File> getFiles(File in,List<File> list) {
		if(in.isDirectory()){
			for(File f: in.listFiles()){
				getFiles(f,list);
			}
		}else if(in.isFile() && in.getName().endsWith(".txt")){
			list.add(in);
		}
		return list;
	}


	/**
	 * parse text into sentence chunks
	 * @param text
	 * @return
	 */
	private String [] getLines(String text){
		return text.split("\n");
	}
	/**
	 * parse text into sentence chunks
	 * @param text
	 * @return
	 */
	private String [] getSentences(String line){
		//return text.split("\n");
		List<String> sentences = new ArrayList<String>();
		line = line.replaceAll("\\.([0-9]+)","\\$$1");
		for(String s: line.split("[\\.?!]")){
			sentences.add(s.replaceAll("\\$([0-9]+)",".$1"));
		}
		return sentences.toArray(new String [0]);
	}
	
	/**
	 * get phrases
	 * @param line
	 * @return
	 */
	private String [] getPhrases(String line){
		//return line.split("[\\.\\?\\!:;]");
		return line.split("[,\\:;]");
		//return new String [] {line};
	}
	
	
	/**
	 * process report
	 * @param text
	 * @param out
	 */
	private void processReport(List<Template> templates, File reportFile,File outputDir) throws Exception {
		progress("processing report ("+(processCount+1)+") "+reportFile.getName()+" ... ");
		
		// read in the report
		String text = TextTools.getText(new FileInputStream(reportFile));
		AnnotatedDocument doc = new AnnotatedDocument();
		doc.setName(reportFile.getName());
		doc.setText(text);
		doc.getFilters().addAll(DocumentFilter.getDeIDFilters());
		
		// combine terminologies into a single instance and add filters
		CompositTerminology terminology = new CompositTerminology();
		for(Template t: templates){
			doc.getFilters().addAll(t.getFilters());
			terminology.addTerminology(t.getTerminology());
		}
		
		
		// do a simple parsing of this document
		long time = System.currentTimeMillis();
		int offset = 0;
		for(String line: getLines(doc.getFilteredDocument())){
			// skip synoptic sections
			if(doc.isSynopticSection(offset))
				continue;
		
			for(String sentence: getSentences(line)){
				for(String phrase: getPhrases(sentence) ){
					int offs = line.indexOf(phrase);
					for(Concept c: terminology.search(phrase,IndexFinderTerminology.BEST_MATCH)){
						for(Annotation a: c.getAnnotations()){	
							if(a.getOffset() < (offset+offs))
								a.updateOffset(offset+offs);
							doc.addAnnotation(a);
						}
						doc.addConcept(c);
					}
				}
			}
			offset += (line.length()+1);
		}
		doc.sort();
		
	/*	System.out.println("--------------");
		for(Annotation a: doc.getAnnotations()){
			System.out.println(a.getText()+" ... ("+a.getStartPosition()+","+a.getEndPosition()+ ") \t\t"+a.getConcept().getName()+" ... "+a.getConcept().getCode());
		}
		System.out.println("\n----------------( "+time+" )-------------------\n");*/
		
		
		// get a list of processed concepts
		Map<Template,List<ItemInstance>> resultMap = new LinkedHashMap<Template, List<ItemInstance>>();
		
		// now lets do information extraction
		for(Template template: templates){
			if(template.isAppropriate(doc)){
				List<ItemInstance> items = template.process(doc);
				resultMap.put(template,items);
				
				// re-add annotation
				for(ItemInstance i: items){
					for(Annotation a: i.getAnnotations()){
						if(!doc.getAnnotations().contains(a))
							doc.getAnnotations().add(a);
					}
				}
			}
		}
		doc.sort();
		
		long total = System.currentTimeMillis()-time;
		processCount ++;
		processTime += total;
			
		// now output HTML for this report
		String name = reportFile.getName();
		if(name.endsWith(".txt"))
			name = name.substring(0,name.length()-".txt".length());
		
		// save HTML
		createCodedHTMLReport(new File(outputDir,name+".html"),doc,resultMap,total);
		
		// update HTML index
		getHTMLIndex(outputDir).write("<a href=\""+name+".html\" target=\"frame\">"+reportFile.getName()+"</a><br>");
		
		// save CSV
		createCodedCSVReport(new File(outputDir,RESULT_FILE),name,resultMap);
		
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
			htmlIndexWriter.write("<head><title>Information Extractor</title>\n");
			htmlIndexWriter.write("<script type=\"text/javascript\">function l(){var h=800;if(!window.innerWidth){\n");
			htmlIndexWriter.write("if(!(document.documentElement.clientWidth == 0)){\n h = document.documentElement.clientHeight;\n");
			htmlIndexWriter.write("}else{h = document.body.clientHeight;}}else{ h = window.innerHeight;} var hd = (h-100)+\"px\";\n");
			htmlIndexWriter.write("document.getElementById(\"d1\").style.maxHeight=hd;}</script>\n");
			htmlIndexWriter.write("</head><body style=\"overflow: hidden;\" bgcolor=\"#EEEEFF\" onload=\"l();\" onresize=\"l();\"><center><h3>Information Extractor Output [");
			htmlIndexWriter.write("<a href=\""+RESULT_FILE+"\" title=\"Download the entire result in CSV format\">CSV</a>]</h3></center>\n");
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
	
	
	private BufferedWriter getCSVWriter(File out,Set<Template> templates) throws Exception {
		if(csvWriter == null){
			csvWriter = new BufferedWriter(new FileWriter(out));
			csvWriter.write("Report");
			for(Template template: templates){
				for(TemplateItem temp: template.getTemplateItems()){
					csvWriter.write(S+getQuestion(temp));
					if(!temp.getUnits().isEmpty())
						csvWriter.write(S+getQuestion(temp)+" (units)");
				}
			}
			csvWriter.write("\n");
		}
		return csvWriter;
	}
	
	/**
	 * get the question
	 * @return
	 */
	private String getQuestion(TemplateItem templateItem){
		if(TemplateItem.TYPE_DIAGNOSIS.equals(templateItem.getType()))
			return templateItem.getType();
		return templateItem.getName();
	}

	/**
	 * create codes csv report
	 * @param file
	 * @param name
	 * @param resultMap
	 * @throws Exception
	 */
	private void createCodedCSVReport(File file, String name, Map<Template,List<ItemInstance>> resultMap)  throws Exception{
		BufferedWriter writer = getCSVWriter(file,resultMap.keySet());
		writer.write(name);
		for(Template template: resultMap.keySet()){
			for(TemplateItem temp: template.getTemplateItems()){
				boolean hasUnits = !temp.getUnits().isEmpty();
				List<ItemInstance> instances = getInstances(temp,resultMap.get(template));
				StringBuffer b = new StringBuffer();
				for(ItemInstance inst :instances){
					b.append(((hasUnits && inst.getValue() != null)?TextTools.toString((Double)inst.getValue()):inst.getAnswer())+" ");
				}
				writer.write(S+b.toString().trim());
				if(hasUnits){
					b = new StringBuffer();
					for(ItemInstance inst :instances){
						String nm = (inst.getUnit() != null)?inst.getUnit().getName():"";
						b.append(nm+" ");
					}
					writer.write(S+b.toString().trim());
				}
			}
		}
		writer.write("\n");
		writer.flush();
	}


	/**
	 * code label
	 * @param l
	 * @return
	 */
	private String codeLabel(Annotation l){
		String lid = ""+l.getOffset();
		String word = l.getText();
		String codes = "";
		String tip = ""+l.getConcept();
		return "<label id=\""+lid+"\" style=\"color:green;\" onmouseover=\"h("+codes+");\" onmouseout=\"u("+codes+");\" title=\""+tip+"\">"+word+"</label>";
	}
	
	

	/**
	 * create pretty CAP template
	 * @param concepts
	 * @return
	 */
	private String createTemplate(Map<Template,List<ItemInstance>> map){
		StringBuffer cap = new StringBuffer();
		
		for(Template template: map.keySet()){
			int num = 1;
			cap.append("<h3>"+template.getName()+"</h3>");
			cap.append("<table border=0 cellspacing=0 cellpadding=2>");
			for(TemplateItem temp: template.getTemplateItems()){
				List<ItemInstance> items = getInstances(temp,map.get(template));
				String name = (items.isEmpty())?temp.getName():codeTemplateItem(items.get(0));
				cap.append("<tr><td> <font color=\"#E0E0E0 \">"+(num++)+"</font> </td><th align=left> "+name+" </th><td align=left style=\"padding-left:20px;\">");
				String br = "";
				for(ItemInstance item: items){
					cap.append(br+codeConcept(item));
					br="<br>";
				}
				cap.append("</td></tr>");
			}
			cap.append("</table>");
		}
		return cap.toString();
	}

	/**
	 * get matching instances
	 * @param temp
	 * @param all
	 * @return
	 */
	private List<ItemInstance> getInstances(TemplateItem temp,List<ItemInstance> all){
		List<ItemInstance> inst = new ArrayList<ItemInstance>();
		for(ItemInstance item: all){
			if(item.getTemplateItem().equals(temp))
				inst.add(item);
		}
		return inst;
	}
	
	

	/**
	 * code label
	 * @param l
	 * @return
	 */
	private String codeConcept(ItemInstance e){
		String lid = e.getName();
		String text = e.getAnswer();
		String tip = e.getDescription();
		List<String> codes = new ArrayList<String>();
		try{
			for(Annotation l: e.getAnnotations()){
				codes.add("'"+l.getOffset()+"'");
			}
		}catch(Exception ex){}
		return "<label id=\""+lid+"\" style=\"color:blue;\" onmouseover=\"h("+codes+");\" onmouseout=\"u("+codes+");\" onclick=\"j("+codes+")\" title=\""+tip+"\">"+text+"</label>";
	}

	/**
	 * code label
	 * @param l
	 * @return
	 */
	private String codeTemplateItem(ItemInstance e){
		String lid = e.getName();
		String text = e.getQuestion();
		String tip = e.getTemplateItem().getDescription();
		List<String> codes = new ArrayList<String>();
		try{
			for(Annotation l: e.getAnnotations()){
				codes.add("'"+l.getOffset()+"'");
			}
		}catch(Exception ex){}
		return "<label id=\""+lid+"\" style=\"color:blue;\" onmouseover=\"h("+codes+");\" onmouseout=\"u("+codes+");\" onclick=\"j("+codes+")\" title=\""+tip+"\">"+text+"</label>";
	}
	

	/**
	 * create a coded html report
	 */
	private void createCodedHTMLReport(File out, AnnotatedDocument doc, Map<Template,List<ItemInstance>> map, long total) throws Exception {
		// create cap protocol
		String cap    =  createTemplate(map);
		
		// build report
		String content = doc.getText();
		StringBuffer text = new StringBuffer();
		int offs = 0;
		List<Annotation> last = new ArrayList<Annotation>();
		for(Annotation l: doc.getAnnotations()){
			if(checkAnnotation(last,l,map)){
				try{
					int o = l.getOffset();
					text.append(content.substring(offs,o));
					text.append(codeLabel(l));
					offs = o+l.getLength();
				}catch(Exception ex){
					System.err.println(l+" offset: "+offs);
					ex.printStackTrace();
					
				}
				last.add(l);
			}
		}
		text.append(content.substring(offs));
		
		int n = 0;
		for(Template t: map.keySet()){
			n += map.get(t).size();
		}
		
		// get report representation and cap protocol
		String report = convertToHTML(text.toString());
		
		StringBuffer info = new StringBuffer();
		info.append("report process time: <b>"+total+"</b> ms , ");
		info.append("found items: <b>"+n+"</b>");
		
		// write out results
		String name = doc.getName();
		BufferedWriter htmlWriter = new BufferedWriter(new FileWriter(out));
		
		
		htmlWriter.write("<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">");
		htmlWriter.write("<html xmlns=\"http://www.w3.org/1999/xhtml\">");
		htmlWriter.write("<head><title>Report Processor Output</title><script type=\"text/javascript\">");
		htmlWriter.write("function h(id){for(i=0;i<id.length;i++){document.getElementById(id[i]).style.backgroundColor=\"yellow\";}}");
		htmlWriter.write("function u(id){for(i=0;i<id.length;i++){document.getElementById(id[i]).style.backgroundColor=\"white\";}}"); //</script>
		htmlWriter.write("function j(id){for(i=0;i<id.length;i++){location.href=\"#\";location.href=\"#\"+id[i];}}");
		htmlWriter.write("function l(){var h=800;if(!window.innerWidth){\n");
		htmlWriter.write("if(!(document.documentElement.clientWidth == 0)){\n h = document.documentElement.clientHeight;\n");
		htmlWriter.write("}else{h = document.body.clientHeight;}}else{ h = window.innerHeight;} var hd = (h-100)+\"px\";\n");
		htmlWriter.write("document.getElementById(\"d1\").style.maxHeight=hd;document.getElementById(\"d2\").style.maxHeight=hd;}</script>\n");
		
		htmlWriter.write("</head><body onload=\"l();\" onresize=\"l();\"><table width=\"100%\" style=\"table-layout:fixed; \" cellspacing=\"5\">\n"); //word-wrap:break-word;
		htmlWriter.write("<tr><td colspan=2 align=center><h3>"+name+"</h3></td></tr>\n");
		htmlWriter.write("<tr><td width=\"50%\" valign=middle><div id=\"d1\" style=\"overflow: auto; max-height: 800px; \">"+report+"</div></td>");
		htmlWriter.write("<td width=\"50%\" valign=top><div id=\"d2\" style=\"overflow: auto; max-height: 800px;\">"+cap+"</div></td></tr>\n");
		htmlWriter.write("<tr><td colspan=2 align=center>"+info+"</td></tr>\n");
		htmlWriter.write("<tr><td colspan=2 align=center></td></tr>\n");
		htmlWriter.flush();
		
		// finish up
		htmlWriter.write("<tr><td colspan=2></td></tr>\n");
		htmlWriter.write("</table></body></html>\n");
		htmlWriter.flush();
		htmlWriter.close();
	
	}
	
	
	/**
	 * is this a valid annotation belonging to found items.
	 * @param l
	 * @param map
	 * @return
	 */
	private boolean checkAnnotation(List<Annotation> previous, Annotation l, Map<Template, List<ItemInstance>> map) {
		// if span is with previous one, don't include
		int fromIndex = (previous.size()>5)?previous.size()-5:0; 
		for(Annotation last: previous.subList(fromIndex, previous.size())){
			if(((last.getStartPosition() <= l.getStartPosition() && l.getEndPosition() <= last.getEndPosition()) ||
				(l.getStartPosition() <= last.getStartPosition() && last.getEndPosition() <= l.getEndPosition())))
				return false;
		}
		// check if it was mentioned
		boolean include = false;
		for(Template t: map.keySet()){
			for(ItemInstance i: map.get(t)){
				if(i.getAnnotations().contains(l)){
					include = true;
					break;
				}
			}
		}
		
		return include;
	}


	/**
	 * convert regular text report to HTML
	 * 
	 * @param txt
	 * @return
	 */
	public static String convertToHTML(String txt) {
		return (txt + "\n").replaceAll("\n", "<br>").replaceAll("(^|<br>)([A-Z ]+:)<br>", "$1<b>$2</b><br>").
							replaceAll("(^|<br>)(\\[[A-Za-z ]+\\])<br>", "$1<b>$2</b><br>");
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
		}else{
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
}
