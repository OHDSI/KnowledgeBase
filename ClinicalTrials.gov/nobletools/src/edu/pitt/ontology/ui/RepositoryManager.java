package edu.pitt.ontology.ui;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.beans.PropertyChangeEvent;
import java.beans.PropertyChangeListener;
import java.io.File;
import java.io.FileOutputStream;
import java.util.Arrays;
import java.util.Comparator;

import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JComponent;
import javax.swing.JDialog;
import javax.swing.JEditorPane;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JList;
import javax.swing.JOptionPane;
import javax.swing.JProgressBar;
import javax.swing.JScrollPane;
import javax.swing.JSplitPane;
import javax.swing.JToolBar;
import javax.swing.SwingConstants;
import javax.swing.SwingUtilities;
import javax.swing.border.LineBorder;
import javax.swing.border.TitledBorder;
import javax.swing.event.ListSelectionEvent;
import javax.swing.event.ListSelectionListener;

import edu.pitt.ontology.IClass;
import edu.pitt.ontology.IOntology;
import edu.pitt.ontology.IOntologyException;
import edu.pitt.ontology.IRepository;
import edu.pitt.ontology.bioportal.BioPortalRepository;
import edu.pitt.terminology.Terminology;
import edu.pitt.terminology.util.Describable;
import edu.pitt.terminology.util.TerminologyException;

public class RepositoryManager implements ActionListener, ListSelectionListener, PropertyChangeListener{
	
	private JFrame frame;
	private IRepository repository;
	private JList ontologies, terminologies;
	private JLabel status;
	private JProgressBar progress;
	private JComponent toolbar;
	private boolean selectionSwitch;
	// bioportal import
	//private BioPortalOntologyImporter bioportal;
	private static boolean STAND_ALONE;
	public static final int ONTOLOGIES_ONLY = 1;
	public static final int TERMINOLOGIES_ONLY = 2;
	
	
	/**
	 * create GUI manager
	 */
	public RepositoryManager(){
		frame = createGUI(0);
	}
	
	public RepositoryManager(int mode){
		frame = createGUI(mode);
	}
	
	/**
	 * create GUI component
	 * @return
	 */
	private JFrame createGUI(int mode){
		JFrame f = new JFrame("RepositoryManager");
		if(STAND_ALONE)
			f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		f.getContentPane().setLayout(new BorderLayout());
		ontologies = new JList();
		ontologies.setCellRenderer(new ResourceCellRenderer());
		terminologies = new JList();
		terminologies.setCellRenderer(new ResourceCellRenderer());
		ontologies.addListSelectionListener(this);
		terminologies.addListSelectionListener(this);
		JScrollPane s1 = new JScrollPane(ontologies);
		JScrollPane s2 = new JScrollPane(terminologies);
		s1.setPreferredSize(new Dimension(300,200));
		s2.setPreferredSize(new Dimension(300,200));
		s1.setBorder(new TitledBorder("Ontologies"));
		s2.setBorder(new TitledBorder("Terminologies"));
		JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT);
		split.setTopComponent(s1);
		split.setBottomComponent(s2);
		split.setResizeWeight(.5);
		status = new JLabel(" ");
		progress = new JProgressBar();
		progress.setString("Please Wait ...");
		progress.setStringPainted(true);
		progress.setIndeterminate(true);
		toolbar = createToolBar();
		JComponent c = split;
		if(ONTOLOGIES_ONLY == mode)
			c = s1;
		else if(TERMINOLOGIES_ONLY == mode)
			c = s2;
		f.getContentPane().add(c,BorderLayout.CENTER);
		f.getContentPane().add(toolbar,BorderLayout.EAST);
		f.getContentPane().add(status,BorderLayout.SOUTH);
		f.pack();
		return f;
	}
	
	/**
	 * display busy
	 * @param b
	 */
	public void setBusy(boolean busy){
		if(busy){
			frame.getContentPane().remove(status);
			frame.getContentPane().add(progress,BorderLayout.SOUTH);
		}else{
			frame.getContentPane().remove(progress);
			frame.getContentPane().add(status,BorderLayout.SOUTH);
		}
		frame.getContentPane().validate();
		frame.getContentPane().repaint();
	}
	
	/**
	 * start application
	 * @param config
	 *
	public void start(String config){
		try{
			start(new ProtegeRepository(config));
		}catch(IOntologyException ex){
			ex.printStackTrace();
		}
	}
	*/
	
	/**
	 * start application
	 * @param config
	 */
	public void start(IRepository r){
		frame.setVisible(true);
		repository = r;
		repository.addPropertyChangeListener(this);
		setBusy(true);
		
		(new Thread(new Runnable(){
			public void run() {
				final IOntology [] ont = repository.getOntologies();
				final Terminology [] term = repository.getTerminologies();
				Arrays.sort(ont,new Comparator<IOntology>(){
					public int compare(IOntology o1, IOntology o2) {
						if(o1 instanceof IOntology && o2 instanceof IOntology)
							return ((IOntology)o1).getName().compareTo(((IOntology)o2).getName());
						return o1.toString().compareTo(o2.toString());
					}
					
				});
				Arrays.sort(term,new Comparator<Terminology>(){
					public int compare(Terminology o1, Terminology o2) {
						return o1.getName().compareTo(o2.getName());
					}
				});
				
				SwingUtilities.invokeLater(new Runnable(){
					public void run(){
						ontologies.setListData(ont);
						terminologies.setListData(term);
						setBusy(false);
					}
				});
				
			}
		})).start();
		
	}
	
	
	/**
	 * handle reloads
	 */
	public void propertyChange(PropertyChangeEvent evt){
		if(OntologyImporter.PROPERTY_PROGRESS_MSG.equals(evt.getPropertyName())){
			progress.setString(""+evt.getNewValue());
		}else{
			ontologies.setListData(repository.getOntologies());
			terminologies.setListData(repository.getTerminologies());
			ontologies.revalidate();
			terminologies.revalidate();
		}
	}
	
	/**
	 * create button
	 * @param text
	 * @return
	 */
	private JButton createButton(String text, String icon){
		JButton bt = new JButton(text);
		bt.addActionListener(this);
		bt.setActionCommand(text);
		bt.setHorizontalAlignment(SwingConstants.LEFT);
		bt.setMaximumSize(new Dimension(175,30));
		if(icon != null)
			bt.setIcon(new ImageIcon(getClass().getResource(icon)));
		return bt;
	}
	
	/**
	 * create toolbar with buttons
	 * @return
	 */
	private JComponent createToolBar(){
		JToolBar toolbar = new JToolBar(JToolBar.VERTICAL);
		toolbar.add(createButton("NEW","/icons/New24.gif"));
		toolbar.add(createButton("PORTAL","/icons/WebComponentAdd24.gif"));
		toolbar.add(createButton("IMPORT","/icons/Import24.gif"));
		toolbar.add(createButton("EXPORT","/icons/Export24.gif"));
		toolbar.add(createButton("REMOVE","/icons/Delete24.gif"));
		toolbar.addSeparator();
		toolbar.add(createButton("INFO","/icons/Information24.gif"));
		toolbar.add(createButton("BROWSE","/icons/Search24.gif"));
		toolbar.add(createButton("QUERY","/icons/Find24.gif"));
		return toolbar;
	}
	
	
	/**
	 * get selected value
	 * @return
	 */
	private Describable getSelectedValue(){
		Describable d = (Describable) ontologies.getSelectedValue();
		if(d == null)
			d = (Describable) terminologies.getSelectedValue();
		return d;
	}
	
	
	/**
	 * actions on buttons
	 * @param e
	 */
	public void actionPerformed(ActionEvent e){
		String cmd = e.getActionCommand();
		if(cmd.equalsIgnoreCase("NEW")){
			JOptionPane.showMessageDialog(frame,"Not Implemented!");
		}else if(cmd.equalsIgnoreCase("PORTAL")){
			doPortal();
		}else if(cmd.equalsIgnoreCase("IMPORT")){
			doImport();
		}else if(cmd.equalsIgnoreCase("EXPORT")){
			doExport();
		}else if(cmd.equalsIgnoreCase("INFO")){
			doInfo();
		}else if(cmd.equalsIgnoreCase("BROWSE")){
			doBrowser();
		}else if(cmd.equalsIgnoreCase("QUERY")){
			doQuery();
		}else if(cmd.equalsIgnoreCase("REMOVE")){
			doRemove();
		}
	}

	/**
	 * remove ontology
	 */
	private void doRemove(){
		int r = JOptionPane.showConfirmDialog(frame,"Are you sure you want to delete selected ontologies?","Confirm",JOptionPane.YES_NO_OPTION);
		// if not canceled, remove entry
		if(r == JOptionPane.YES_OPTION){
			for(Object o : ontologies.getSelectedValues()){
				IOntology ont = (IOntology) o;
				// remove entry
				repository.removeOntology(ont);
				// remove data
				ont.delete();
				
			}
		}
	}

	/**
	 * import ontology
	 */
	private void doPortal(){
		
		(new Thread(new Runnable(){
			public void run(){
				try{
					OntologyImporter importer = new OntologyImporter(new BioPortalRepository());
					importer.addPropertyChangeListener(RepositoryManager.this);
					JDialog d = importer.showImportWizard(frame);
					
					
					// wait for selection
					while(d.isShowing()){
						try{
							Thread.sleep(500);
						}catch(Exception ex){}
					}
					//selected
					if(importer.isSelected()){
						setBusy(true);
					
						IOntology source = importer.getSelectedOntology();
						IClass [] scls = importer.getSelectedClasses();
						
						// create new ontology
						IOntology ont = repository.createOntology(source.getURI());
						
						//copy content
						importer.copy(scls,ont.getRoot());
						
						// import ontology
						repository.importOntology(ont);
					}
					importer.removePropertyChangeListener(RepositoryManager.this);
				}catch(Exception ex){
					ex.printStackTrace();
					JOptionPane.showMessageDialog(frame,ex.getMessage(),
								"Error",JOptionPane.ERROR_MESSAGE);
				}
				setBusy(false);
			}
		})).start();

		
	}
	
	/**
	 * import ontology from file
	 */
	private void doImport(){
		JFileChooser chooser = new JFileChooser();
		if(chooser.showOpenDialog(frame) == JFileChooser.APPROVE_OPTION){
			final File f = chooser.getSelectedFile();
			if(f != null && f.canRead()){
				setBusy(true);
				(new Thread(new Runnable(){
					public void run(){
						try{
							repository.importOntology(f.toURI());
						}catch(Exception ex){
							ex.printStackTrace();
							JOptionPane.showMessageDialog(frame,ex.getMessage(),"Error",JOptionPane.ERROR_MESSAGE);
						}
						setBusy(false);
					}
				})).start();
			}
		}
	}
	
	
	
	
	/**
	 * export ontology
	 */
	private void doExport(){
		final Object value = getSelectedValue();
		if(value instanceof IOntology){
			JFileChooser chooser = new JFileChooser();
			if(chooser.showSaveDialog(frame) == JFileChooser.APPROVE_OPTION){
				final File f = chooser.getSelectedFile();
				setBusy(true);
				(new Thread(new Runnable(){
					public void run(){
						IOntology ont = (IOntology) value;
						try{
							ont.load();
							ont.write(new FileOutputStream(f),IOntology.OWL_FORMAT);
							JOptionPane.showMessageDialog(frame,ont.getName()+" saved as "+f.getAbsolutePath());
						}catch(Exception ex){
							ex.printStackTrace();
							JOptionPane.showMessageDialog(frame,ex.getMessage(),"Error",JOptionPane.ERROR_MESSAGE);							
						}
						setBusy(false);
					}
				})).start();
			}
			
		}else
			JOptionPane.showMessageDialog(frame,"Not Implemented!");
	}
	
	
	/**
	 * open ontology expolorer
	 *
	 */
	private void doInfo(){
		Describable d = getSelectedValue();
		if(d == null)
			return;
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
	
	/**
	 * open ontology expolorer
	 *
	 */
	private void doBrowser(){
		final OntologyExplorer explorer = new OntologyExplorer();
		JFrame f = new JFrame("Ontology Explorer");
		f.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
		f.getContentPane().add(explorer);
		f.pack();
		f.setVisible(true);
		// set root
		Object value = getSelectedValue();
		if(value instanceof IOntology){
			final IOntology ont = (IOntology) value;
			explorer.setBusy(true);
			(new Thread(new Runnable(){
				public void run(){
					/*
					try{
						ont.load();
					}catch(IOntologyException ex){
						ex.printStackTrace();
					}*/
					explorer.setRoot(ont.getRootClasses());
					explorer.setBusy(false);
				}
			})).start();
		}else if(value instanceof Terminology){
			final Terminology term = (Terminology) value;
			explorer.setBusy(true);
			(new Thread(new Runnable(){
				public void run(){
					try{
						explorer.setRoot(term.getRootConcepts());
					}catch(TerminologyException ex){
						ex.printStackTrace();
					}
					explorer.setBusy(false);
				}
			})).start();
		}
	}
	
	/**
	 * open ontology expolorer
	 *
	 */
	private void doQuery(){
		final QueryTool explorer = new QueryTool();
		JFrame f = new JFrame("Terminology Query");
		f.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
		f.getContentPane().add(explorer);
		f.pack();
		f.setVisible(true);
		// set root
		Object value = getSelectedValue();
		if(value instanceof IOntology){
			final IOntology ont = (IOntology) value;
			explorer.setBusy(true);
			(new Thread(new Runnable(){
				public void run(){
					try{
						ont.load();
					}catch(IOntologyException ex){
						ex.printStackTrace();
					}
					explorer.setOntology(ont);
					explorer.setBusy(false);
				}
			})).start();
		}else if(value instanceof Terminology){
			explorer.setTerminology((Terminology)value);
		}
	}
	
	
	/**
	 * follow lists
	 */
	public void valueChanged(ListSelectionEvent e){
		if(!e.getValueIsAdjusting() && !selectionSwitch){
			selectionSwitch = true;
			if(e.getSource() == ontologies){
				terminologies.clearSelection();
				setOntologyButtonsEnabled(true);
			}else if(e.getSource() == terminologies){
				ontologies.clearSelection();
				setOntologyButtonsEnabled(false);
			}
			selectionSwitch = false;
		}
	}
	
	/**
	 * enable/disable ontology buttons
	 * @param b
	 */
	private void setOntologyButtonsEnabled(boolean b){
		if(toolbar != null){
			for(int i=0;i<4;i++){
				toolbar.getComponent(i).setEnabled(b);
			}
		}
	}
	
	/**
	 * @return the frame
	 */
	public JFrame getFrame() {
		return frame;
	}
	

	/**
	 * @return the repository
	 */
	public IRepository getRepository() {
		return repository;
	}

	/**
	 * @param args
	 *
	public static void main(String[] args) throws Exception {
		STAND_ALONE = true;
	
		//setup string
		File f = null;
		if(args.length > 0){
			f = new File(args[0]);
			if(!f.exists()){
				System.err.println("Error: cannot find config file "+f.getAbsolutePath());
			}
		}else{
			System.err.println("Usage: java RepositoryManager <config file>");
		}
		
		
		// load properties
		
		//if(f != null)
		//	p.load(new FileInputStream(f));
		
		Properties p = new Properties();
		String driver = p.getProperty("repository.driver","com.mysql.jdbc.Driver");
		String url   =  p.getProperty("repository.url","jdbc:mysql://cds-its01.acct.upmchs.net/ontologies");
		String user  =  p.getProperty("repository.username","user");
		String pass  =  p.getProperty("repository.password","resu");
		String table =  p.getProperty("repository.table","repository");
		String dir   =  System.getProperty("user.home")+File.separator+p.getProperty("repository.folder",".protegeRepository");
		 
		RepositoryManager manager = new RepositoryManager();
		manager.start(new ProtegeRepository(driver,url,user,pass,table,dir));
		//manager.start(new BioPortalRepository());
	}
	*/
}
