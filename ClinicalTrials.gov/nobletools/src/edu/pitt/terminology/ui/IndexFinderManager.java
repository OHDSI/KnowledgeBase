package edu.pitt.terminology.ui;
import javax.swing.JFrame;

import edu.pitt.ontology.ui.RepositoryManager;
import edu.pitt.terminology.client.IndexFinderRepository;


public class IndexFinderManager {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		RepositoryManager manager = new RepositoryManager();
		manager.getFrame().setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		//NobleCoderTerminology.setPersistenceDirectory(new File("/home/tseytlin/Data/Terminologies/IndexFinder"));
		//NobleCoderTerminology.setCachingEnabled(false);
		manager.start(new IndexFinderRepository());

	}

}
