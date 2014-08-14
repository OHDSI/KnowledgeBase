package edu.pitt.ontology.protege;

import java.util.Map;

import edu.pitt.ontology.IQueryResults;
import edu.stanford.smi.protegex.owl.model.query.QueryResults;

public class PQueryResults implements IQueryResults {
	private QueryResults results;
	
	public PQueryResults(QueryResults r){
		results = r;
	}
	
	public String[] getVariables() {
		return (String []) results.getVariables().toArray(new String [0]);
	}

	public Map next() {
		return results.next();
	}

	public boolean hasNext() {
		return results.hasNext();
	}

	public void remove() {
	}

}
