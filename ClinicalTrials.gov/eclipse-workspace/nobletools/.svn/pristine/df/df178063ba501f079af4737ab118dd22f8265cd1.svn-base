package edu.pitt.ontology.protege.concepts;

import java.util.LinkedHashMap;
import java.util.Map;

import edu.pitt.ontology.bioportal.BioPortalHelper;


/**
 * a registry map of all available concept handlers
 * @author tseytlin
 *
 */
public class ConceptRegistry {
	public static final Map<String,String> REGISTRY = new LinkedHashMap<String,String>();
	// initialize resource map
	static {
		REGISTRY.put("http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl",ThesaurusConcept.class.getName());
		REGISTRY.put("http://sig.biostr.washington.edu/fma3.0",FMAConcept.class.getName());
		REGISTRY.put("/"+BioPortalHelper.BIOPORTAL_URL.replaceAll("\\.","\\.")+".*/",BioPortalConcept.class.getName());
	}
}
