package edu.pitt.ontology.owl;

import java.io.File;
import java.util.Arrays;

import edu.pitt.ontology.IClass;
import edu.pitt.ontology.IOntology;
import edu.pitt.ontology.IProperty;

public class OOntologyTests {
	
	public static void main(String [] args) throws Exception {
		//IOntology ont = OOntology.loadOntology(new URL("http://slidetutor.upmc.edu/curriculum/owl/KnowledgeBase.owl"));
		IOntology ont = OOntology.loadOntology(new File("/home/tseytlin/test.owl"));
		//IOntology ont = OOntology.loadOntology(new URL("http://slidetutor.upmc.edu/curriculum/owl/skin/PITT/MelanocyticInstances.owl"));
		System.out.println("name:\t"+ont.getName());
		System.out.println("desc:\t"+ont.getDescription());
		System.out.println("ver:\t"+ont.getVersion());
		System.out.println("format:\t"+ont.getFormat());
		System.out.println("prefix:\t"+ont.getPrefix());
		System.out.println("uri:\t"+ont.getURI());
		System.out.println("loc:\t"+ont.getLocation());
		System.out.println("root:\t"+ont.getRoot());
		System.out.println("import:\t"+Arrays.toString(ont.getImportedOntologies())+"\n");
		//String cls_url = "http://slidetutor.upmc.edu/curriculum/owl/KnowledgeBase.owl#DIAGNOSES";
		//String cls_url = "knowledgebase:DIAGNOSES";
		String cls_url = "DIAGNOSES";
		
		IClass cls = ont.getClass(cls_url);
		
		IClass mel = ont.getClass("MALIGNANT_MELANOMA_IN-SITU_NOS");
		printClassInfo(mel);
		printClassInfo(ont.getClass("MALIGNANT_MELANOMA"));
		
		if(mel != null){
			System.out.println("has dx as super? "+mel.hasSuperClass(cls));
			System.out.println("has mm as direct super? "+mel.hasDirectSuperClass(ont.getClass("MALIGNANT_MELANOMA")));
			System.out.println("has mml as direct super? "+mel.hasDirectSuperClass(ont.getClass("MALIGNANT_MELANOCYTIC_LESION")));
			System.out.println("\n\n");
		}
		IProperty prop = ont.getProperty("rdfs:label");
		printPropertyInfo(prop);
		
		printPropertyInfo(ont.getProperty("abrLabel"));
	}
	
	private static void printClassInfo(IClass cls){
		if(cls == null){
			System.err.println("Class is NULL");
		}else{
			System.out.println("class:\t"+cls);
			System.out.println("uri:\t"+cls.getURI());
			System.out.println("namespace:\t"+cls.getNameSpace());
			System.out.println("labels:\t"+Arrays.toString(cls.getLabels()));
			System.out.println("comments:\t"+Arrays.toString(cls.getComments()));
			System.out.println("prefix:\t"+cls.getPrefix());
			
			System.out.println("direct subclass:\t"+Arrays.toString(cls.getDirectSubClasses()));
			System.out.println("direct superclass:\t"+Arrays.toString(cls.getDirectSuperClasses()));
			System.out.println("subclass:\t"+Arrays.toString(cls.getSubClasses()));
			System.out.println("superclass:\t"+Arrays.toString(cls.getSuperClasses()));
			System.out.println("equivalent:\t"+Arrays.toString(cls.getEquivalentClasses()));
			System.out.println("disjoint:\t"+Arrays.toString(cls.getDisjointClasses()));
			System.out.println("instances:\t"+Arrays.toString(cls.getInstances()));
			
			System.out.println("concept:");
			cls.getConcept().printInfo(System.out);
			
			System.out.println("\n\n");
		}
	}
	
	private static void printPropertyInfo(IProperty cls){
		if(cls == null){
			System.err.println("Property is NULL");
		}else{
			System.out.println("prop:\t"+cls);
			System.out.println("uri:\t"+cls.getURI());
			System.out.println("namespace:\t"+cls.getNameSpace());
			System.out.println("labels:\t"+Arrays.toString(cls.getLabels()));
			System.out.println("comments:\t"+Arrays.toString(cls.getComments()));
			System.out.println("prefix:\t"+cls.getPrefix());
			
			System.out.println("annotaiton:\t"+cls.isAnnotationProperty());
			System.out.println("object prop:\t"+cls.isObjectProperty());
			System.out.println("data prop:\t"+cls.isDatatypeProperty());
			System.out.println("functional:\t"+cls.isFunctional());
			
			
			System.out.println("direct subproperties:\t"+Arrays.toString(cls.getDirectSubProperties()));
			System.out.println("direct superproperties:\t"+Arrays.toString(cls.getDirectSuperProperties()));
			System.out.println("subproperties:\t"+Arrays.toString(cls.getSubProperties()));
			System.out.println("superproperties:\t"+Arrays.toString(cls.getSuperProperties()));
			
			
			System.out.println("\n\n");
		}
	}
	
}
