package edu.pitt.terminology.util;

import java.awt.Color;
import java.awt.event.FocusEvent;
import java.awt.event.FocusListener;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.List;

import javax.swing.DefaultListModel;
import javax.swing.JList;
import javax.swing.JTextField;
import javax.swing.SwingUtilities;
import javax.swing.event.DocumentEvent;
import javax.swing.event.DocumentListener;

public class DynamicList extends JList implements DocumentListener {
	public static final int STARTS_WITH_MATCH = 0;
	public static final int CONTAINS_MATCH = 1;
	private JTextField text;
	private Collection content;
	private boolean block,selected;
	private DefaultListModel model;
	private int matchMode;
	
	public DynamicList(JTextField text){
		this(text,Collections.EMPTY_LIST);
	}
	
		
	public DynamicList(JTextField text,Collection content){
		super(new DefaultListModel());
		this.content = content;
		this.text = text;
		this.model = (DefaultListModel) getModel();
		load(content);
		text.setText("Search");
		text.setForeground(Color.LIGHT_GRAY);
		text.addFocusListener(new FocusListener() {
			public void focusLost(FocusEvent e) {
				if("".equals(DynamicList.this.text.getText())){
					DynamicList.this.text.setForeground(Color.LIGHT_GRAY);
					DynamicList.this.text.setText("Search");
				}
			}
			public void focusGained(FocusEvent e) {
				if("Search".equals(DynamicList.this.text.getText())){
					DynamicList.this.text.setForeground(Color.BLACK);
					DynamicList.this.text.setText("");
				}
			}
		});
		text.getDocument().addDocumentListener(this);
		text.addKeyListener(new KeyAdapter() {
			public void keyTyped(KeyEvent e) {
				int c = e.getKeyCode();
				if(c == KeyEvent.VK_DOWN || c == KeyEvent.VK_TAB){
					grabFocus();
				}
				
			}
		});
	}
	
	private void load(Collection list){
		for(Object o: list){
			model.addElement(o);
		}
	}
	
	/**
	 * get text editor
	 */
	public JTextField getTextEditor(){
		return text;
	}
	
	public void clear(){
		model.removeAllElements();
		text.setText("");
	}
	
	/**
	 * set match mode
	 * STARTS_WITH_MATCH,CONTAINS_MATCH
	 * @param mode
	 */
	public void setMatchMode(int mode){
		matchMode = mode;
	}
	
	
	//sync combobox w/ what is typed in
	private void sync(String str) {
		model.removeAllElements();
		boolean show = false;
		if(str != null && str.length() > 0){
			for(Object word: getMatchingObjects(str)){
				model.addElement(word);
				show = true;
			}
		}else{
			for(Object word: content){
				model.addElement(word);
			}
		}
		revalidate();
		text.setText(str);
	}

	
	private synchronized void sync(){
		block = true;
		SwingUtilities.invokeLater(new Runnable(){
			public void run(){
				sync(text.getText());
				block = false;
			}
		});
	}
	
	/**
	 * 
	 * @param str
	 * @return
	 */
	private List getMatchingObjects(String str){
		str = str.toLowerCase();
		List list = new ArrayList();
		for(Object w: content){
			if(match(w.toString(),str)){
				list.add(w);
			}
		}
		return list;
	}
	
	
	private boolean match(String s1, String s2){
		if(text.getForeground().equals(Color.LIGHT_GRAY))
			return true;
		s1 = s1.toLowerCase();
		s2 = s2.toLowerCase();
		switch(matchMode){
			case CONTAINS_MATCH:
				return s1.contains(s2);
			default:
				return s1.startsWith(s2);
				
		}
	}
	
	
	public void changedUpdate(DocumentEvent arg0) {
		if(!block)
			sync();
	}

	public void insertUpdate(DocumentEvent arg0) {
		if(!block)
			sync();
	}

	public void removeUpdate(DocumentEvent arg0) {
		if(!block)
			sync();
	}
}