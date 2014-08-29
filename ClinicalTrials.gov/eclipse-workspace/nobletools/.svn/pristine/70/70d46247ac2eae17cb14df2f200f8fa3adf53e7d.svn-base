package edu.pitt.terminology.ui;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Component;
import java.awt.Dimension;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.net.URI;
import java.net.URL;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Comparator;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Set;

import javax.swing.Box;
import javax.swing.BoxLayout;
import javax.swing.DefaultListModel;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JComboBox;
import javax.swing.JComponent;
import javax.swing.JDialog;
import javax.swing.JFileChooser;
import javax.swing.JLabel;
import javax.swing.JList;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JProgressBar;
import javax.swing.JScrollPane;
import javax.swing.JSplitPane;
import javax.swing.JTabbedPane;
import javax.swing.JTextArea;
import javax.swing.JTextField;
import javax.swing.JToolBar;
import javax.swing.SwingUtilities;
import javax.swing.border.BevelBorder;
import javax.swing.border.CompoundBorder;
import javax.swing.border.EmptyBorder;
import javax.swing.filechooser.FileFilter;

import edu.pitt.ontology.IClass;
import edu.pitt.ontology.IOntology;
import edu.pitt.ontology.IProperty;
import edu.pitt.ontology.IRepository;
import edu.pitt.ontology.protege.POntology;
import edu.pitt.ontology.ui.OntologyExplorer;
import edu.pitt.ontology.ui.QueryTool;
import edu.pitt.ontology.ui.ResourceCellRenderer;
import edu.pitt.terminology.Terminology;
import edu.pitt.terminology.client.IndexFinderRepository;
import edu.pitt.terminology.lexicon.Concept;
import edu.pitt.terminology.lexicon.Definition;
import edu.pitt.terminology.lexicon.SemanticType;
import edu.pitt.terminology.util.DynamicList;
import edu.pitt.terminology.util.TerminologyException;
import edu.pitt.text.tools.TextTools;

/**
 * this class is responsible for copying one ontology into the other
 * @author tseytlin
 */

public class TerminologyExporter implements ActionListener {
	public static final String PROPERTY_PROGRESS_MSG = "ProgressMessage";
	private final URL ADD_ICON = getClass().getResource("/icons/Plus16.gif");
	private final URL REM_ICON = getClass().getResource("/icons/Minus16.gif");
	private final String SEMANTIC_TYPES = "/resources/SemanticTypes.txt";

	
	// GUI components
	private JPanel main;
	private OntologyExplorer ontologyExplorer;
	private QueryTool query;
	private JList rootList,semTypeList;
	private DynamicList semanticTypeList;
	private JComboBox<Terminology> terminologyList;
	private JTextField outputFile;
	private JTextArea console;
	private JPanel statusPanel,semanticTypePanel;
	private JDialog wizard;
	private JProgressBar progress;
	private IRepository repository;
	private String defaultURI = "http://www.ontologies.com/";

	

	public TerminologyExporter(IRepository r){
		repository = r;
	}


	/**
	 * create an import wizzard
	 */
	public JDialog showExportWizard(Component owner){
		//main = new JOptionPane(createWizardPanel(),
		//JOptionPane.PLAIN_MESSAGE,JOptionPane.CLOSED_OPTION);
		//wizard = main.createDialog(owner,"Export Terminology as OWL Ontology");
		main = createWizardPanel();
		main.setBorder(new CompoundBorder(new EmptyBorder(10,10,10,10),new BevelBorder(BevelBorder.RAISED)));
		wizard = new JDialog(JOptionPane.getFrameForComponent(owner));
		wizard.setTitle("Export Terminology as OWL Ontology");
		wizard.getContentPane().add(main);
		wizard.setModal(false);
		wizard.setResizable(true);
		wizard.pack();
		wizard.setLocationRelativeTo(owner);
		wizard.setVisible(true);
		loadTerminologies();
		return wizard;
	}
	


	
	/**
	 * load ontologies
	 */
	public void loadTerminologies(){
		(new Thread(new Runnable(){
			public void run(){
				setBusy(true);
				Terminology [] ont = repository.getTerminologies();
				Arrays.sort(ont, new Comparator<Terminology>() {
					public int compare(Terminology o1, Terminology o2) {
						return o1.getName().compareTo(o2.getName());
					}
				});
				for(int i=0;i<ont.length;i++){
					terminologyList.addItem(ont[i]);
				}
				SwingUtilities.invokeLater(new Runnable(){
					public void run(){
						terminologyList.repaint();
						setBusy(false);
					}
				});
			}
		})).start();
	}
	
	/**
	 * display busy
	 * @param b
	 */
	public void setBusy(boolean busy){
		if(busy){
			statusPanel.removeAll();
			statusPanel.add(progress,BorderLayout.SOUTH);
		}else{
			JLabel lbl = new JLabel("");
			statusPanel.removeAll();
			statusPanel.add(lbl,BorderLayout.SOUTH);
		}
		statusPanel.revalidate();
		statusPanel.repaint();
	}
	
	
	/**
	 * create filter panel
	 * @param label
	 * @param command
	 * @param list
	 * @return
	 */
	private JPanel createFilterPanel(String label, String command, JList list){
		list.setCellRenderer(new ResourceCellRenderer());
		JToolBar toolbar = new JToolBar();
		JButton add = new JButton(new ImageIcon(ADD_ICON));
		add.setToolTipText("Add "+command);
		add.setActionCommand("add-"+command);
		add.addActionListener(this);
		
		JButton rem = new JButton(new ImageIcon(REM_ICON));
		rem.setToolTipText("Remove "+command);
		rem.setActionCommand("rem-"+command);
		rem.addActionListener(this);
		toolbar.add(add);
		toolbar.add(rem);
		toolbar.addSeparator();
		toolbar.add(new JLabel(label));
		
		JPanel selectPanel = new JPanel();
		selectPanel.setLayout(new BorderLayout());
		selectPanel.add(toolbar,BorderLayout.NORTH);
		selectPanel.add(new JScrollPane(list),BorderLayout.CENTER);
		
		return selectPanel;
	}
	
	
	/**
	 * create ontology selector panel
	 * @return
	 */
	private JPanel createWizardPanel(){
		JPanel panel = new JPanel();
		panel.setLayout(new BorderLayout());
		panel.setPreferredSize(new Dimension(600,500));
		
		
		
		JPanel leftPanel = new JPanel();
		leftPanel.setLayout(new BoxLayout(leftPanel,BoxLayout.Y_AXIS));
		
		terminologyList = new JComboBox<Terminology>();
		leftPanel.add(new JLabel("Terminology to Export"));
		leftPanel.add(terminologyList);
		
		
		rootList = new JList(new DefaultListModel());
		leftPanel.add(createFilterPanel("Root Concept Filter","Branch",rootList));
		
		
		semTypeList = new JList(new DefaultListModel());
		leftPanel.add(createFilterPanel("Semantic Type Filter","SemType",semTypeList));
		//leftPanel.add(Box.createRigidArea(new Dimension(50,50)));
	
		leftPanel.add(new JLabel("Output OWL Ontology"));
		outputFile = new JTextField();
		JButton browse = new JButton("Browse");
		browse.addActionListener(this);
		browse.setActionCommand("browse");
		JPanel p = new JPanel();
		p.setLayout(new BorderLayout());
		p.add(outputFile,BorderLayout.CENTER);
		p.add(browse,BorderLayout.EAST);
		leftPanel.add(p);
		
		leftPanel.add(Box.createVerticalStrut(100));
		JButton export =new JButton("Export Terminology");
		export.addActionListener(this);
		export.setActionCommand("export");
		leftPanel.add(export);
		
		for(int i=0;i<leftPanel.getComponentCount();i++){
			if(leftPanel.getComponent(i) instanceof JComponent){
				JComponent c = ((JComponent)leftPanel.getComponent(i));
				c.setBorder(new CompoundBorder(c.getBorder(),new EmptyBorder(5,5,5,5)));
				c.setAlignmentX(Component.CENTER_ALIGNMENT);
			}
		}
		
		
		JPanel rightPanel = new JPanel();
		rightPanel.setLayout(new BorderLayout());
		console = new JTextArea();
		rightPanel.add(new JScrollPane(console),BorderLayout.CENTER);
	
		// setup main split
		JSplitPane split = new JSplitPane(JSplitPane.HORIZONTAL_SPLIT);
		//split.setLeftComponent(new JScrollPane(ontologyList));
		split.setLeftComponent(leftPanel);
		split.setRightComponent(rightPanel);
		split.setResizeWeight(0.5);
		split.setDividerLocation(300);
		panel.add(split,BorderLayout.CENTER);
		
		statusPanel = new JPanel();
		statusPanel.setLayout(new BorderLayout());
		progress = new JProgressBar();
		progress.setIndeterminate(true);
		progress.setStringPainted(true);
		statusPanel.add(new JLabel(""),BorderLayout.CENTER);
		panel.add(statusPanel,BorderLayout.SOUTH);
		
		return panel;
	}

	// actions
	public void actionPerformed(ActionEvent e) {
		String cmd = e.getActionCommand().toLowerCase();
		if(cmd.equals("add-branch")){
			doAddRoot();
		}else if(cmd.equals("rem-branch")){
			doRemove(rootList);
		}else if(cmd.equals("add-semtype")){
			doAddSemType();
		}else if(cmd.equals("rem-semtype")){
			doRemove(semTypeList);
		}else if(cmd.equals("browse")){
			doBrowse();
		}else if(cmd.equals("export")){
			doExport();
		}
	}
	

	private void doBrowse() {
		JFileChooser fc = new JFileChooser(outputFile.getText());
		fc.setFileFilter(new FileFilter() {
			public String getDescription() {
				return "OWL Ontology File (.owl)";
			}
			public boolean accept(File f) {
				return f.isDirectory() || f.getName().endsWith(".owl");
			}
		});
		int n = fc.showSaveDialog(main);
		if(n == JFileChooser.APPROVE_OPTION){
			File f = fc.getSelectedFile();
			if(!f.getName().endsWith(".owl")){
				f = new File(f.getParentFile(),f.getName()+".owl");
			}
			outputFile.setText(f.getAbsolutePath());
		}
	}

	private void doAddSemType() {
		if(semanticTypePanel == null){
			semanticTypePanel = createSemanticTypeSelector();
		}
		int r = JOptionPane.showConfirmDialog(main,semanticTypePanel,"Add SemanticType",
				JOptionPane.OK_CANCEL_OPTION,JOptionPane.PLAIN_MESSAGE);		
		if(r == JOptionPane.OK_OPTION){
			for(Object obj: semanticTypeList.getSelectedValuesList())
				addObject(semTypeList,obj);
		}
		
	}

	private JPanel createSemanticTypeSelector() {
		JPanel panel = new JPanel();
		panel.setPreferredSize(new Dimension(350,300));
		panel.setLayout(new BorderLayout());
		JTextField search = new JTextField();
		search.setForeground(Color.lightGray);
		semanticTypeList = new DynamicList(search,getAllSemanticTypes());
		semanticTypeList.setMatchMode(DynamicList.CONTAINS_MATCH);
		panel.add(search,BorderLayout.NORTH);
		panel.add(new JScrollPane(semanticTypeList),BorderLayout.CENTER);
		return panel;
	}

	/**
	 * get a list of all emantic types
	 * @return
	 */
	private List<String> getAllSemanticTypes(){
		InputStream in = TextTools.class.getResourceAsStream(SEMANTIC_TYPES);
		try {
			List list = new ArrayList(Arrays.asList(TextTools.getText(in).split("\n")));
			Collections.sort(list);
			return list;
		} catch (IOException e) {
			e.printStackTrace();
		}
		return Collections.EMPTY_LIST;
	}
	
	
	private void doRemove(JList list){
		int [] sel = list.getSelectedIndices();
		for(int i: sel){
			((DefaultListModel)list.getModel()).remove(i);
		}
	}
	
	
	
	private void doAddRoot(){
		final Terminology ont = getSelectedTerminology();
		if(ont == null)
			return;
		if(query == null){
			query = new QueryTool();
			query.setPreferredSize(new Dimension(600,400));
		}
		if(ontologyExplorer == null){
			ontologyExplorer = new OntologyExplorer();
			ontologyExplorer.setPreferredSize(new Dimension(600,400));
		}
		
		query.setTerminology(ont);
		try {
			ontologyExplorer.setRoot(ont.getRootConcepts());
		} catch (TerminologyException e) {
			e.printStackTrace();
		}
		
		JTabbedPane tabs = new JTabbedPane();
		tabs.addTab("Search", query);
		tabs.addTab("Browse", ontologyExplorer);
		
		
		int r = JOptionPane.showConfirmDialog(main,tabs,"Add Concept",JOptionPane.OK_CANCEL_OPTION,JOptionPane.PLAIN_MESSAGE);		
		if(r == JOptionPane.OK_OPTION){
			if(tabs.getSelectedIndex() != 0){
				addObject(rootList,ontologyExplorer.getSelectedEntry());
			}else{
				for(Object c: query.getSelectedConcepts()){
					addObject(rootList,c);
				}
			}
		}
	}
	
	/**
	 * add root class
	 * @param obj
	 */
	private void addObject(JList list, Object obj){
		final JList llist = list;
		DefaultListModel model = (DefaultListModel) list.getModel();
		if(!model.contains(obj))
			model.addElement(obj);
		SwingUtilities.invokeLater(new Runnable(){
			public void run(){
				llist.repaint();
			}
		});
	}
	
	/**
	 * get selected ontology
	 * @return
	 */
	public Terminology getSelectedTerminology(){
		Object obj = terminologyList.getSelectedItem();
		return (obj != null && obj instanceof Terminology)?(Terminology)obj:null;
	}
	
	/**
	 * get selected classes
	 * @return
	 */
	public Concept [] getSelectedConcepts(){
		Terminology ont = getSelectedTerminology();
		if(ont == null)
			return new Concept [0];
		Concept [] cls = new Concept [rootList.getModel().getSize()];
		for(int i=0;i<cls.length;i++)
			cls[i] = (Concept) rootList.getModel().getElementAt(i);
		try {
			return (cls.length > 0)?cls:ont.getRootConcepts();
		} catch (TerminologyException e) {
			e.printStackTrace();
		}
		return new Concept [0];
	}
	
	
	/**
	 * do export
	 */

	private void doExport() {
		setBusy(true);
		(new Thread(new Runnable(){
			public void run(){
				File ontologyFile = new File(outputFile.getText());
				if(ontologyFile == null || ontologyFile.isDirectory() || !ontologyFile.getParentFile().exists()){
					String msg = "Not valid ontology file "+ontologyFile.getAbsolutePath();
					console.append("Error: "+msg+"\n");
					JOptionPane.showMessageDialog(main,msg,"Error",JOptionPane.ERROR_MESSAGE);
					return;
				}
				Terminology term = (Terminology) terminologyList.getSelectedItem();
				List<Concept> rootFilter = new ArrayList<Concept>();
				List<SemanticType> semanticTypeFilter = new ArrayList<SemanticType>();
				for(int i=0;i<rootList.getModel().getSize();i++){
					rootFilter.add((Concept)rootList.getModel().getElementAt(i));
				}
				for(int i=0;i<semTypeList.getModel().getSize();i++){
					semanticTypeFilter.add(SemanticType.getSemanticType(""+semTypeList.getModel().getElementAt(i)));
				}
				try {
					IOntology ont = POntology.createOntology(URI.create(defaultURI+ontologyFile.getName()),ontologyFile.getParentFile());
					export(term,rootFilter,semanticTypeFilter,ont);
					ont.save();
				} catch (Exception e) {
					console.append("Error: "+e.getMessage()+"\n");
					JOptionPane.showMessageDialog(main,"Problems encounted during export","Error",JOptionPane.ERROR_MESSAGE);
					e.printStackTrace();
				}
				
				setBusy(false);
			}

		
		})).start();
		
	}
	
	
	/**
	 * export terminology to ontology
	 * @param term
	 * @param rootFilter
	 * @param semanticTypeFilter
	 * @param ont
	 * @throws Exception 
	 */
	public void export(Terminology term, List<Concept> rootFilter, List<SemanticType> semanticTypeFilter,IOntology ont) throws Exception {
		List<Concept> roots = (rootFilter.isEmpty())?Arrays.asList(term.getRootConcepts()):rootFilter;
		for(Concept c: roots){
			exportConcept(c,semanticTypeFilter,"",ont.getRoot());
		}
	}
	
	/**
	 * export single concept as class
	 * @param c
	 * @param hashSet
	 * @param semanticTypeFilter
	 * @param root
	 */
	private void exportConcept(Concept c, List<SemanticType> semanticTypeFilter,String prefix, IClass parent) throws Exception {
		// first make sure that it fits the filter
		if(isFilteredOut(c, semanticTypeFilter)){
			return;
		}
		IOntology ont = parent.getOntology();
		String clsName = getClassName(c.getName());
		IClass cls = ont.getClass(clsName);
		// if class exists, then we have a cycle, just add a parent and quit
		if(cls != null){
			if(!(cls.equals(parent) || cls.hasSuperClass(parent) || cls.hasSubClass(parent)))
				cls.addSuperClass(parent);
			return;
		}
		
		// create class
		cls = parent.createSubClass(clsName);
		
		Set<String> labels = new LinkedHashSet<String>();
		labels.add(c.getName());
		Collections.addAll(labels,c.getSynonyms());
		
		// add synonyms
		for(String s: labels){
			cls.addLabel(s);
		}
		// add definitions
		for(Definition d: c.getDefinitions()){
			cls.addComment(d.getDefinition());
		}
		
		// get concept code 
		IProperty code = getProperty(ont,"code");
		cls.setPropertyValue(code,c.getCode());
		
		// get semantic types
		IProperty stype = getProperty(ont,"SemanticType");
		for(SemanticType st: c.getSemanticTypes())
			cls.addPropertyValue(stype,st.getName());
		
		// output
		console.append(prefix+c.getName()+"\n");
		SwingUtilities.invokeLater(new Runnable(){
			public void run(){
				console.repaint();
			}
		});
		
		// now go into children
		for(Concept child: c.getChildrenConcepts()){
			exportConcept(child,semanticTypeFilter,"  "+prefix,cls);
		}
	}
	
	/**
	 * get or create property
	 * @param ont
	 * @param name
	 * @return
	 */
	private IProperty getProperty(IOntology ont, String name){
		IProperty code = ont.getProperty(name);
		if(code == null){
			code = ont.createProperty(name,IProperty.ANNOTATION_DATATYPE);
			code.setRange(new String [0]);
		}
		return code;
	}
	
	
	/**
	 * is concept filtered out by sem
	 * @param c
	 * @param semanticTypeFilter
	 * @return
	 */
	private boolean isFilteredOut(Concept c, List<SemanticType> semanticTypeFilter){
		if(semanticTypeFilter.isEmpty())
			return false;
		for(SemanticType st: c.getSemanticTypes()){
			if(semanticTypeFilter.contains(st))
				return false;
		}
		return true;
	}
	
	
	/**
	 * create ontology friendly class name
	 * @param name
	 * @return
	 */
	private String getClassName(String name){
		return name.trim().replaceAll("\\s*\\(.+\\)\\s*","").replaceAll("\\W","_").replaceAll("_+","_");
	}
	
	/**
	 * @param args
	 */
	public static void main(String[] args) throws Exception {
		TerminologyExporter importer = new TerminologyExporter(new IndexFinderRepository());
		JDialog d = importer.showExportWizard(null);
		
	}

}
