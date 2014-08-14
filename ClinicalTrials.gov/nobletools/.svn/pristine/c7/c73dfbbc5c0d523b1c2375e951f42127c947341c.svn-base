package edu.pitt.ontology.ui;

import java.awt.BorderLayout;
import java.awt.Component;
import java.awt.Dimension;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.beans.PropertyChangeEvent;
import java.beans.PropertyChangeListener;
import java.beans.PropertyChangeSupport;
import java.io.File;
import java.lang.reflect.Array;
import java.net.URI;
import java.net.URL;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.Date;
import java.util.List;

import javax.swing.DefaultListModel;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JDialog;
import javax.swing.JEditorPane;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JList;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JProgressBar;
import javax.swing.JScrollPane;
import javax.swing.JSplitPane;
import javax.swing.JToolBar;
import javax.swing.SwingUtilities;
import javax.swing.event.ListSelectionEvent;
import javax.swing.event.ListSelectionListener;

import edu.pitt.ontology.IClass;
import edu.pitt.ontology.IInstance;
import edu.pitt.ontology.ILogicExpression;
import edu.pitt.ontology.IOntology;
import edu.pitt.ontology.IOntologyException;
import edu.pitt.ontology.IProperty;
import edu.pitt.ontology.IRepository;
import edu.pitt.ontology.IResource;
import edu.pitt.ontology.IRestriction;
import edu.pitt.ontology.bioportal.BioPortalRepository;
import edu.pitt.ontology.protege.POntology;

/**
 * this class is responsible for copying one ontology into the other
 * @author tseytlin
 */

public class OntologyImporter implements 	ActionListener, PropertyChangeListener, ListSelectionListener {
	public static final String PROPERTY_PROGRESS_MSG = "ProgressMessage";
	private final URL ADD_ICON = getClass().getResource("/icons/Plus16.gif");
	private final URL REM_ICON = getClass().getResource("/icons/Minus16.gif");

	
	// GUI components
	private JOptionPane main;
	private OntologyExplorer ontologyExplorer;
	private JList ontologyList,rootList;
	private JPanel statusPanel;
	private JDialog wizard;
	private JProgressBar progress;
	private JEditorPane ontologyInfo;
	private IRepository repository;
	private PropertyChangeSupport pcs = new PropertyChangeSupport(this);
	
	private String progressMessage = "";

	private boolean disposeSource,deepCopy = true,preload = true,freshCopy;
	
	
	private Comparator<IClass> classComparator = new Comparator<IClass>() {
		public int compare(IClass o1, IClass o2) {
			return o1.getName().compareTo(o2.getName());
		}
		
	} ;

	public OntologyImporter(IRepository r){
		repository = r;
	}

	public void addPropertyChangeListener(PropertyChangeListener listener){
		pcs.addPropertyChangeListener(listener);
	}
	
	public void removePropertyChangeListener(PropertyChangeListener listener){
		pcs.removePropertyChangeListener(listener);
	}
	
	/**
	 * create an import wizzard
	 */
	public JDialog showImportWizard(Component owner){
		main = new JOptionPane(createWizardPanel(),
		JOptionPane.PLAIN_MESSAGE,JOptionPane.OK_CANCEL_OPTION);
		wizard = main.createDialog(owner,"Import Ontology");
		wizard.setModal(false);
		wizard.setResizable(true);
		wizard.setVisible(true);
		loadOntologies();
		return wizard;
	}
	
	
	/**
	 * what is the status of deep copy?
	 * @return
	 */
	public boolean isDeepCopy() {
		return deepCopy;
	}

	
	/**
	 * not only copy the hierarchy, but properties, restrictions etc..
	 * @param deepCopy
	 */
	public void setDeepCopy(boolean deepCopy) {
		this.deepCopy = deepCopy;
	}
	
	/**
	 * the ontology importer will first try to load
	 * an ontology, this can have different effects depending on implementation
	 * BioPortal ontologies can be efficiently preloaded into memory, while on Protege
	 * ontologies this option will not have any effect, since they are already preloaded
	 * @param b
	 */
	public void setPreLoad(boolean b){
		this.preload = b;
	}
	
	
	/**
	 * the ontology importer will first try to load
	 * an ontology, this can have different effects depending on implementation
	 * BioPortal ontologies can be efficiently preloaded into memory, while on Protege
	 * ontologies this option will not have any effect, since they are already preloaded
	 * @param b
	 */
	public boolean isPreLoad(){
		return preload;
	}
	
	/**
	 * get fresh copy flag, when set to true this means that the target ontology is assumed to be blank.
	 * So if during the copy process we encounter that the class already exists, that means
	 * that we have already encountered this branch previously and other then adding a superclass
	 * we don't need to revisit it.
	 * On the other hand, this performance saving might not be desireable whent the target ontology
	 * may have classes w/ the same names, but different set of children.
	 * 
	 * @param freshCopy
	 */
	public boolean isFreshCopy() {
		return freshCopy;
	}

	/**
	 * set fresh copy flag, this means that the target ontology is assumed to be blank.
	 * So if during the copy process we encounter that the class already exists, that means
	 * that we have already encountered this branch previously and other then adding a superclass
	 * we don't need to revisit it.
	 * On the other hand, this performance saving might not be desireable whent the target ontology
	 * may have classes w/ the same names, but different set of children.
	 * 
	 * @param freshCopy
	 */
	public void setFreshCopy(boolean freshCopy) {
		this.freshCopy = freshCopy;
	}

	
	/**
	 * load ontologies
	 */
	public void loadOntologies(){
		(new Thread(new Runnable(){
			public void run(){
				setBusy(true);
				final IOntology [] ont = repository.getOntologies();
				Arrays.sort(ont);
				SwingUtilities.invokeLater(new Runnable(){
					public void run(){
						ontologyList.setListData(ont);
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
			JLabel lbl = new JLabel(
			ontologyList.getModel().getSize()+" ontologies in "+
			repository.getName());
			statusPanel.removeAll();
			statusPanel.add(lbl,BorderLayout.SOUTH);
		}
		statusPanel.revalidate();
		statusPanel.repaint();
	}
	
	/**
	 * create ontology selector panel
	 * @return
	 */
	private JPanel createWizardPanel(){
		JPanel panel = new JPanel();
		panel.setLayout(new BorderLayout());
		panel.setPreferredSize(new Dimension(600,500));
		
		// list
		ontologyList = new JList(new DefaultListModel());
		ontologyList.addListSelectionListener(this);
		ontologyList.setMinimumSize(new Dimension(1,1));
		ontologyList.setCellRenderer(new ResourceCellRenderer());
		//panel.add(scroll1,BorderLayout.CENTER);
		
		// info
		ontologyInfo = new JEditorPane();
		ontologyInfo.setContentType("text/html; charset=UTF-8");
		ontologyInfo.setEditable(false);
		ontologyInfo.setMinimumSize(new Dimension(1,1));
	
		
		// root selector
		rootList = new JList(new DefaultListModel());
		rootList.setCellRenderer(new ResourceCellRenderer());
		JToolBar toolbar = new JToolBar();
		JButton add = new JButton(new ImageIcon(ADD_ICON));
		add.setToolTipText("Add Class Tree");
		add.setActionCommand("add");
		add.addActionListener(this);
		
		JButton rem = new JButton(new ImageIcon(REM_ICON));
		rem.setToolTipText("Remove Class Tree");
		rem.setActionCommand("rem");
		rem.addActionListener(this);
		toolbar.add(add);
		toolbar.add(rem);
		toolbar.addSeparator();
		toolbar.add(new JLabel("Import Classes"));
		
		JPanel selectPanel = new JPanel();
		selectPanel.setLayout(new BorderLayout());
		selectPanel.add(toolbar,BorderLayout.NORTH);
		selectPanel.add(new JScrollPane(rootList),BorderLayout.CENTER);
		
		JSplitPane rightPanel = new JSplitPane(JSplitPane.VERTICAL_SPLIT);
		rightPanel.setTopComponent(ontologyInfo);
		rightPanel.setBottomComponent(selectPanel);
		rightPanel.setResizeWeight(0.5);
		rightPanel.setDividerLocation(250);
		
		// setup main split
		JSplitPane split = new JSplitPane(JSplitPane.HORIZONTAL_SPLIT);
		split.setLeftComponent(new JScrollPane(ontologyList));
		split.setRightComponent(rightPanel);
		split.setResizeWeight(0.5);
		split.setDividerLocation(300);
		panel.add(split,BorderLayout.CENTER);
		
		statusPanel = new JPanel();
		statusPanel.setLayout(new BorderLayout());
		progress = new JProgressBar();
		progress.setIndeterminate(true);
		progress.setString("loading ontologies from "+repository.getName()+"..");
		progress.setStringPainted(true);
		statusPanel.add(new JLabel("|"),BorderLayout.CENTER);
		panel.add(statusPanel,BorderLayout.SOUTH);
		
		return panel;
	}

	// actions
	public void actionPerformed(ActionEvent e) {
		String cmd = e.getActionCommand();
		if(cmd.equals("add")){
			doAdd();
		}else if(cmd.equals("rem")){
			int [] sel = rootList.getSelectedIndices();
			for(int i: sel){
				((DefaultListModel)rootList.getModel()).remove(i);
			}
		}
	}
	
	/**
	 * add classes to a list
	 */
	public void propertyChange(PropertyChangeEvent evt) {
		String cmd = evt.getPropertyName();
		if(OntologyExplorer.VALUE_SELECTED_EVENT.equals(cmd)){
			addRootClass(evt.getNewValue());
		}else if(IOntology.ONTOLOGY_LOADING_EVENT.equals(cmd)){
			pcs.firePropertyChange(PROPERTY_PROGRESS_MSG,progressMessage,evt.getNewValue());
			progressMessage = ""+evt.getNewValue();
		}else if(IOntology.ONTOLOGY_LOADED_EVENT.equals(cmd)){
			// after it is loaded stop listening to the ontology
			IOntology ont = (IOntology) evt.getSource();
			ont.removePropertyChangeListener(this);
		}
	}

	public boolean isDisposeSource() {
		return disposeSource;
	}

	public void setDisposeSource(boolean disposeSource) {
		this.disposeSource = disposeSource;
	}


	
	private void doAdd(){
		final IOntology ont = getSelectedOntology();
		if(ont == null)
			return;
		
		if(ontologyExplorer != null){
			ontologyExplorer.removePropertyChangeListener(this);
		}
		ontologyExplorer = new OntologyExplorer();
		ontologyExplorer.addPropertyChangeListener(this);
		
		JOptionPane explorer = new JOptionPane(ontologyExplorer,
		JOptionPane.PLAIN_MESSAGE,JOptionPane.OK_CANCEL_OPTION);
		JDialog d = explorer.createDialog(wizard,"Ontology Explorer ["+getSelectedOntology()+"]");
		d.setModal(true);
		d.setResizable(true);
		ontologyExplorer.setBusy(true);
		(new Thread(new Runnable(){
			public void run(){
				/*
				try{
					Thread.sleep(500);
				}catch(Exception ex){}
				*/
				ontologyExplorer.setRoot(ont.getRoot());
				ontologyExplorer.setBusy(false);
			}
		})).start();
		d.setVisible(true);
		
		// if ok add
		Integer ok = JOptionPane.OK_OPTION;
		if(ok.equals(explorer.getValue())){
			addRootClass(ontologyExplorer.getSelectedEntry());
		}
	}
	
	
	/**
	 * add root class
	 * @param obj
	 */
	private void addRootClass(Object obj){
		DefaultListModel model = (DefaultListModel) rootList.getModel();
		if(!model.contains(obj))
			model.addElement(obj);
	}
	
	/**
	 * get selected ontology
	 * @return
	 */
	public IOntology getSelectedOntology(){
		Object obj = ontologyList.getSelectedValue();
		return (obj != null && obj instanceof IOntology)?(IOntology)obj:null;
	}
	
	/**
	 * get selected classes
	 * @return
	 */
	public IClass [] getSelectedClasses(){
		IOntology ont = getSelectedOntology();
		if(ont == null)
			return new IClass [0];
		IClass [] cls = new IClass [rootList.getModel().getSize()];
		for(int i=0;i<cls.length;i++)
			cls[i] = (IClass) rootList.getModel().getElementAt(i);
		return (cls.length > 0)?cls:ont.getRootClasses();
	}
	

	public void valueChanged(ListSelectionEvent e) {
		if(e.getSource() == ontologyList && !e.getValueIsAdjusting()){
			Object obj = ontologyList.getSelectedValue();
			if(obj != null && obj instanceof IOntology){
				IOntology ont = (IOntology) obj;
				String name = ont.getName();
				String [] labels = ont.getLabels();
				if(labels.length > 0)
					name = labels[0];
				ontologyInfo.setText(
						"<b>"+name+"</b> "+ont.getVersion()+"<br><a>"+ont.getURI()+"</a><br>"+
						"<hr>"+ont.getDescription());
			}
		}
	}

	/**
	 * has selection been made
	 * @return
	 */
	public boolean isSelected(){
		Integer i = JOptionPane.OK_OPTION;
		return i.equals(main.getValue()) && getSelectedOntology() != null;
	}
	
	/**
	 * import source ontology into destination ontology
	 * @param source
	 * @param roots
	 * @param destination
	 * @param root
	 
	public void copy(IClass [] sourceRoots,IClass targetRoot){
		copy(sourceRoots,targetRoot,null);
	}
	*/
	
	/**
	 * import source ontology into destination ontology avoid cycles
	 * @param source
	 * @param roots
	 * @param destination
	 * @param root
	 *
	public void copyNoCycle(IClass [] sourceRoots,IClass targetRoot){
		copyNoCycle(sourceRoots,targetRoot,null);
	}
	*/
	
	/**
	 * import source ontology into destination ontology
	 * @param source
	 * @param roots
	 * @param destination
	 * @param root
	 *
	public void copyClasses(IClass [] sourceRoots,IClass targetRoot,JProgressBar bar){
		copy(sourceRoots,targetRoot,bar);
	}
	*/
	/**
	 * import source ontology into destination ontology
	 * @param source
	 * @param roots
	 * @param destination
	 * @param root
	 */
	public void copyClasses(IClass [] sourceRoots,IClass targetRoot){
		copy(sourceRoots,targetRoot);
	}
	
	
	/**
	 * import source ontology into destination ontology avoiding cycles
	 * @param source
	 * @param roots
	 * @param destination
	 * @param root
	 *
	public void copyClassesNoCycle(IClass [] sourceRoots,IClass targetRoot){
		copyNoCycle(sourceRoots,targetRoot);
	}
	*/
	
	/**
	 * import source ontology into destination ontology
	 * @param source
	 * @param roots
	 * @param destination
	 * @param root
	 */
	public void copy(IClass [] sourceRoots, IClass targetRoot){
		// preload ontology
		if(isPreLoad() && sourceRoots.length > 0){
			IOntology ont = sourceRoots[0].getOntology();
			try{
				ont.addPropertyChangeListener(this);
				ont.load();
			}catch(IOntologyException ex){
				System.out.println("Error: Could not load ontology "+ont);
				ex.printStackTrace();
			}
		}
		
		// copy all classes
		for(IClass c: sourceRoots){
			try{
				copyClass(targetRoot, c);
			}catch(Exception ex){
				System.out.println("Error: Could not copy class "+c);
				ex.printStackTrace();
			}
		}
		
		// copy metadata for ontologies
		if(sourceRoots.length > 0){
			IOntology src = sourceRoots[0].getOntology();
			IOntology dst = targetRoot.getOntology();
			copyResourceInfo(src, dst);			
		}
		
		// do deep copy
		/*
		if(deepCopy){
			// copy all properties
			if(sourceRoots.length > 0)
				copyProperties(sourceRoots[0].getOntology(), targetRoot.getOntology(),bar);
			
			
			// now copy all class content
			for(IClass c: sourceRoots){
				try{
					copyClassContent(targetRoot.getOntology(),c,bar);
				}catch(Exception ex){
					System.out.println("Error: Could not copy class content"+c);
					ex.printStackTrace();
				}
			}
		}
		*/
	}
	
	/**
	 * import source ontology into destination ontology avoiding cycles
	 * @param source
	 * @param roots
	 * @param destination
	 * @param root
	 *
	public void copyNoCycle(IClass [] sourceRoots, IClass targetRoot, JProgressBar bar){
		// copy all classes
		for(IClass c: sourceRoots){
			try{
				copyClassNoCycle(targetRoot, c, new TreeSet<IClass>(classComparator), bar);
			}catch(Exception ex){
				System.out.println("Error: Could not copy class "+c);
				ex.printStackTrace();
			}
		}
		// copy metadata for ontologies
		if(sourceRoots.length > 0){
			IOntology src = sourceRoots[0].getOntology();
			IOntology dst = targetRoot.getOntology();
			copyResourceInfo(src, dst);			
		}
	}
	*/
	/**
	 * import source ontology into destination ontology
	 * @param source
	 * @param roots
	 * @param destination
	 * @param root
	 *
	public void copyValues(IOntology source, IOntology target){
		copyValues(source,target,null);
	}
	*/
	
	/**
	 * import source ontology into destination ontology
	 * @param source
	 * @param roots
	 * @param destination
	 * @param root
	 */
	public void copyValues(IOntology source, IOntology target){
		// copy all properties
		copyProperties(source, target);
				
		// now copy all class content
		for(IClass src: source.getRootClasses())
			copyClassContent(target,src);
	}
	
	/**
	 * import source ontology into destination ontology
	 * @param source
	 * @param roots
	 * @param destination
	 * @param root
	 */
	public void copyValues(IClass [] source, IClass target){
		if(source.length == 0 || target == null)
			return;
		
		// copy all properties
		copyProperties(source[0].getOntology(), target.getOntology());
				
		// now copy all class content
		for(IClass src: source)
			copyClassContent(target.getOntology(),src);
	}
	
	
	/**
	 * copy resource info
	 * @param src
	 * @param dst
	 */
	private void copyResourceInfo(IResource src, IResource dst){
		// copy superficial stuff
		for(String lbl: src.getLabels())
			dst.addLabel(lbl);
		for(String com: src.getComments())
			dst.addComment(com);
		if(src.getVersion() != null)
			dst.addVersion(src.getVersion());
	}
	
	/**
	 * import source ontology into destination ontology
	 * @param source
	 * @param roots
	 * @param destination
	 * @param root
	 */
	public void copy(IOntology source,IOntology target){
		copyClasses(source.getRootClasses(),target.getRoot());
		if(deepCopy)
			copyValues(source, target);
	}
	

	/**
	 * import source ontology into destination ontology avoiding cycles
	 * @param source
	 * @param roots
	 * @param destination
	 * @param root
	 *
	public void copyNoCycle(IOntology source,IOntology target){
		
		// Delegate some of progress reporting to the paging ontology
		if (source instanceof edu.pitt.dbmi.ontology.bioportal.BOntology) {
			((edu.pitt.dbmi.ontology.bioportal.paged.BOntology)source).setPropertyChangeSupport(this.pcs) ;
			((edu.pitt.dbmi.ontology.bioportal.paged.BOntology)source).setProgressMessage(this.progressMessage) ;	
		}
		
		copyClassesNoCycle(source.getRootClasses(),target.getRoot());
		if(deepCopy)
			copyValues(source, target);
	}
	*/
	
	/**
	 * create class from 
	 * @return
	 */
	private void copyClass(IClass parent, IClass source){
		// figure out the name
		String name = source.getName();
		
		// notify of progress
		String msg = "Copying class "+name+" ...";
		pcs.firePropertyChange(PROPERTY_PROGRESS_MSG, progressMessage, msg);
		progressMessage = msg;
		
		
		//check if name exits
		IOntology ont = parent.getOntology();
		IClass cls = ont.getClass(name);
		///IClass [] children = source.getDirectSubClasses();
		
		if(cls == null){
			cls = parent.createSubClass(name);
			copyResourceInfo(source,cls);
		}else if(!cls.hasSuperClass(parent)){
			cls.addSuperClass(parent);
			// don't visit this branch, since we've probably been there
			if(freshCopy)
				return;
		}
		
		//a might be slow, be somehow show equivalent classes
		List<IClass> children =  new ArrayList<IClass>(Arrays.asList(source.getDirectSubClasses()));
		List<IClass> parents = Arrays.asList(source.getSuperClasses());
		// avoid having infinite loops
		children.removeAll(parents);
		children.remove(source);
		
		// go into children
		for(IClass child: children){
			copyClass(cls,child);
		}
		if(disposeSource)
			source.dispose();
	}
	
	
	
	
	/**
	 * create class from 
	 * @return
	 *
	private void copyClassNoCycle(IClass parent, IClass source, TreeSet<IClass> traversalPath, JProgressBar bar){
		// figure out the name
		//String [] l = source.getLabels();
		//String name = getClassName((l.length > 0)?l[0]:source.getName());
		String name = source.getName();
		String msg = "Copying class "+name+" ...";
		
		// notify of progress
		if(bar != null){
			bar.setString(msg);
		}else{
			pcs.firePropertyChange(PROPERTY_PROGRESS_MSG, progressMessage, msg);
			progressMessage = msg;
		}
		
		//check if name exits
		IOntology ont = parent.getOntology();
		IClass cls = ont.getClass(name);
		IClass [] children = source.getDirectSubClasses();
		
		if(cls == null){
			cls = parent.createSubClass(name);
			copyResourceInfo(source,cls);
		}else if(!cls.hasSuperClass(parent)){
			cls.addSuperClass(parent);
		}
		
		TreeSet<IClass> newTraversalPath = new TreeSet<IClass>(classComparator) ;
		newTraversalPath.add(source) ;
		newTraversalPath.addAll(traversalPath) ;
		
		// go into children
		for(IClass child: children){
			if (!newTraversalPath.contains(child)) {  // Avoid self describing class (BIRNLex, BioTOP)
				copyClassNoCycle(cls,child,newTraversalPath,bar);
			}
		}
		
		if(disposeSource)
			source.dispose();
	}
	*/
	
	/**
	 * copy all properties
	 * @param src
	 * @param target
	 */
	private void copyProperties(IOntology src, IOntology target){
		// create all properties
		for(IProperty sp : src.getProperties()){
			String name = sp.getName();
			// skip properties that are incorrectly named
			if(!name.matches("\\w+"))
				continue;
			IProperty tp = target.getProperty(name);
			if(tp == null && !target.hasResource(name)){
				tp = target.createProperty(name,sp.getPropertyType());
				
				// notify of progress
				String msg = "Copying property "+name+" ...";
				pcs.firePropertyChange(PROPERTY_PROGRESS_MSG, progressMessage, msg);
				progressMessage = msg;
				
				
				
				// copy stuff
				copyResourceInfo(sp,tp);
				
				// copy booleans
				tp.setFunctional(sp.isFunctional());
				tp.setTransitive(sp.isTransitive());
				tp.setSymmetric(sp.isSymmetric());
				
				// copy domain and ranges
				tp.setDomain((IResource []) convertResources(target,sp.getDomain(),IResource.class));
				tp.setRange(convertResources(target,sp.getRange()));
			}
		}
		
		// set rest of properties properties
		for(IProperty sp : src.getProperties()){
			String name = sp.getName();
			// skip properties that are incorrectly named
			if(!name.matches("\\w+"))
				continue;
			
			IProperty tp = target.getProperty(name);
			if(tp != null){
				tp.setInverseProperty((IProperty)convertResource(target,sp.getInverseProperty()));
				IProperty [] sub = sp.getSubProperties();
				if(sub != null && sub.length > 0){
					for(IProperty p: (IProperty []) convertResources(target,sub,IProperty.class)){
						tp.addSubProperty(p);
					}
				}
				IProperty [] sup = sp.getSuperProperties();
				if(sup != null && sup.length > 0){
					for(IProperty p: (IProperty []) convertResources(target,sup,IProperty.class)){
						tp.addSuperProperty(p);
					}
				}
				
			}
		}
	}
	
	/**
	 * convert an array of resources to different onology
	 * @param ont
	 * @param values
	 * @return
	 */
	private Object [] convertResources(IOntology ont, Object [] values){
		return convertResources(ont, values,null);
	}
	
	/**
	 * convert an array of resources to different onology
	 * @param ont
	 * @param values
	 * @return
	 */
	private Object [] convertResources(IOntology ont, Object [] values, Class type){
		ArrayList list = new ArrayList();
		Class ltype = type;
		for(int i = 0; i< values.length; i++){
			Object obj = convertResource(ont, values[i]);
			if(obj != null){
				ltype = obj.getClass();
				if(obj instanceof ILogicExpression){
					for(Object o : (ILogicExpression) obj){
						ltype = o.getClass();
						list.add(o);
					}
				}else	
					list.add(obj);
			}else{
				System.err.println("null for "+values[i]);
			}
		}
		return (ltype != null)?list.toArray((Object [])Array.newInstance(ltype,0)):list.toArray();
	}
	
	/**
	 * convert an array of resources to different onology
	 * @param ont
	 * @param values
	 * @return
	 */
	private Object  convertResource(IOntology ont, Object value){
		if(value == null)
			return null;
		
		if(value instanceof IRestriction){
			IRestriction r = (IRestriction) value;
			IRestriction t = ont.createRestriction(r.getRestrictionType());
			t.setProperty((IProperty)convertResource(ont,r.getProperty()));
			t.setParameter((ILogicExpression)convertResource(ont,r.getParameter()));
			return t;
		}else if(value instanceof ILogicExpression){
			ILogicExpression e = (ILogicExpression) value;
			ILogicExpression t = ont.createLogicExpression();
			t.setExpressionType(e.getExpressionType());
			for(Object o: e){
				t.add(convertResource(ont,o));
			}
			return t;
		}else if(value instanceof IProperty){
			return ont.getProperty(((IProperty) value).getName());
		}else if(value instanceof IClass){
			IClass c = (IClass) value;
			if(c.isAnonymous())
				return convertResource(ont,c.getLogicExpression());
			return ont.getClass(c.getName());
		}else if(value instanceof IInstance){
			return ont.getInstance(((IInstance) value).getName());
		}else if(value instanceof IResource){
			return ont.getResource(((IResource) value).getName());
		}
		return value;
	}
	
	
	
	/**
	 * recursively copy class content when all classes were created already
	 * @param source
	 * @param destination
	 */
	private void copyClassContent(IOntology ont, IClass source){
		String name = source.getName();
		
		
		// notify of progress
		String msg = "Copying class content "+name+" ...";
		pcs.firePropertyChange(PROPERTY_PROGRESS_MSG, progressMessage, msg);
		progressMessage = msg;
		
		
		//check if name exits
		IClass cls = ont.getClass(name);
		// if exists, then do the magic
		if(cls != null){
			// copy property values 
			for(IProperty sp: source.getProperties()){
				IProperty tp = (IProperty) convertResource(ont,sp);
				if(tp != null){
					// set property values
					if(tp.isFunctional())
						cls.setPropertyValue(tp,convertResource(ont,source.getPropertyValue(sp)));
					else
						cls.setPropertyValues(tp,convertResources(ont,source.getPropertyValues(sp)));
					
				}	
			}
			
			// copy disjoints
			for(IClass c: source.getDisjointClasses()){
				cls.addDisjointClass((IClass)convertResource(ont,c));
			}
			
			// copy necessary restrictions
			ILogicExpression exp = source.getNecessaryRestrictions();
			if(exp.getExpressionType() == ILogicExpression.OR){
				cls.addSuperClass(ont.createClass((ILogicExpression) convertResource(ont,exp)));
			}else{
				for(Object c: exp){
					if(c instanceof IRestriction)
						cls.addNecessaryRestriction((IRestriction)convertResource(ont,c));
					else if(c instanceof IClass)
						cls.addSuperClass((IClass) convertResource(ont,c));
					else if(c instanceof ILogicExpression)
						cls.addSuperClass(ont.createClass((ILogicExpression) convertResource(ont,exp)));		
				}
			}
			
			// copy equivalent restrictions
			exp = source.getEquivalentRestrictions();
			if(exp.getExpressionType() == ILogicExpression.OR){
				cls.addEquivalentClass(ont.createClass((ILogicExpression) convertResource(ont,exp)));
			}else{
				for(Object c: exp){
					if(c instanceof IRestriction)
						cls.addEquivalentRestriction((IRestriction)convertResource(ont,c));
					else if(c instanceof IClass)
						cls.addEquivalentClass((IClass) convertResource(ont,c));
					else if(c instanceof ILogicExpression)
						cls.addEquivalentClass(ont.createClass((ILogicExpression) convertResource(ont,exp)));
					
				}
			}
						
			// copy instances
			for(IInstance inst: source.getDirectInstances()){
				IInstance i = ont.getInstance(inst.getName());
				if(i == null){
					i = cls.createInstance(inst.getName());
					// copy property values
					for(IProperty sp : inst.getProperties()){
						IProperty tp = (IProperty) convertResource(ont,sp);
						if(tp != null){
							if(tp.isFunctional())
								i.setPropertyValue(tp,convertResource(ont,inst.getPropertyValue(sp)));
							else
								i.setPropertyValues(tp,convertResources(ont,inst.getPropertyValues(sp)));
						}
					}
				}
			}
			
			
			//a might be slow, be somehow show equivalent classes
			List<IClass> children =  new ArrayList<IClass>(Arrays.asList(source.getDirectSubClasses()));
			List<IClass> parents = Arrays.asList(source.getSuperClasses());
			// avoid having infinite loops
			children.removeAll(parents);
			children.remove(source);
			
			// go into children
			for(IClass child: children){
				copyClassContent(ont,child);
			}
		}
		
	
		// dispose if necessary		
		if(disposeSource)
			source.dispose();
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
	static long time2;
	public static void main(String[] args) throws Exception {
		/*
		String driver = "com.mysql.jdbc.Driver";
		String url = "jdbc:mysql://localhost/repository";
		String user = "user";
		String pass = "resu";
		String table = "repository";
		String dir   = System.getProperty("user.home")+File.separator+".protegeRepository";
		IRepository r = new ProtegeRepository(driver,url,user,pass,table,dir);
		*/
		
		//new BioPortalRepository()
		OntologyImporter importer = new OntologyImporter(new BioPortalRepository());
		importer.setDeepCopy(true);
		importer.setPreLoad(true);
		importer.setFreshCopy(true);
		importer.addPropertyChangeListener(new PropertyChangeListener(){
			int i = 0;
			public void propertyChange(PropertyChangeEvent p) {
				String msg = ""+p.getNewValue();
				if(!msg.startsWith("Copy") || i++ %1000 == 0)
					System.out.println(msg);
			}
		});
		
		
		/*
		File dir = new File(System.getProperty("user.home")+File.separator+"Output");
		IOntology src = POntology.loadOntology(new File(dir,"Animals.owl"));
		IOntology dst = POntology.createOntology(URI.create("http://www.test.org/Frogs.owl"), dir);
		dst.createClass("CONCEPTS").createSubClass("DIAGNOSES");
		*/
		
		
		
		JDialog d = importer.showImportWizard(null);
		while(d.isShowing()){
			try{
				Thread.sleep(500);
			}catch(Exception ex){}
		}
		if(importer.isSelected()){
			//IOntology source = POntology.loadOntology(new File("/home/tseytlin/Work/curriculum/owl/skin/UPMC/Alopecia.owl"));
			IOntology source = importer.getSelectedOntology();
			source.addPropertyChangeListener(new PropertyChangeListener() {
				public void propertyChange(PropertyChangeEvent e) {
					if(IOntology.ONTOLOGY_LOADED_EVENT.equals(e.getPropertyName())){
						System.out.println("preload time "+((System.currentTimeMillis()-time2)/1000)+" s");
					}	
				}
			});
			IClass [] scls = importer.getSelectedClasses();
			
			IOntology ont = POntology.createOntology(URI.create("http://www.ontologies.com/Test.owl"),new File(System.getProperty("user.home")));
			System.out.println("start time "+new Date());
			long time = System.currentTimeMillis();
			time2 = System.currentTimeMillis();
			importer.copyClasses(scls,ont.getRoot());
			importer.copyValues(scls,ont.getRoot());
			System.out.println("total import time "+((System.currentTimeMillis()-time)/1000)+" s");
			System.out.println("end time "+new Date());
			ont.save();
			showOntology(ont);
			
		}else
			System.exit(0);
			
	}

	private static void showOntology(IOntology ont){
		OntologyExplorer e = new OntologyExplorer();
		JFrame frame = new JFrame("Ontology Explorer");
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.getContentPane().add(e);
		frame.pack();
		frame.setVisible(true);
		e.setRoot(ont.getRoot());
	}
}
