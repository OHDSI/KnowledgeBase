package edu.pitt.info.extract.model.util;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.ArrayList;
import java.util.List;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.transform.OutputKeys;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerException;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;

import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;

public class XMLUtils {
	
	/**
	 * format XML into human readable form
	 * @param document
	 * @param root
	 * @param tab
	 *
	private static void formatXML(Document document, Element root, String tab) {
		NodeList children = root.getChildNodes();
		// save the nodes in the array first
		Node[] nodes = new Node[children.getLength()];
		for (int i = 0; i < children.getLength(); i++)
			nodes[i] = children.item(i);
		// insert identations
		for (int i = 0; i < nodes.length; i++) {
			root.insertBefore(document.createTextNode("\n" + tab), nodes[i]);
			if (nodes[i] instanceof Element)
				formatXML(document, (Element) nodes[i], "  " + tab);
		}
		root.appendChild(document.createTextNode("\n"
				+ tab.substring(0, tab.length() - 2)));
	}
	*/
	
	/**
	 * write out an XML file
	 * 
	 * @param doc
	 * @param os
	 * @throws TransformerException 
	 * @throws IOException 
	 */
	public static void writeXML(Document doc, OutputStream os) 
		throws TransformerException, IOException{
		// write out xml file
		TransformerFactory tFactory = TransformerFactory.newInstance();
        Transformer transformer = tFactory.newTransformer();
        transformer.setOutputProperty(OutputKeys.INDENT, "yes");
        transformer.setOutputProperty("{http://xml.apache.org/xslt}indent-amount", "2");
        
        //indent XML properly
        //formatXML(doc,doc.getDocumentElement(),"  ");

        //normalize document
        doc.getDocumentElement().normalize();

		 //write XML to file
        DOMSource source = new DOMSource(doc);
        StreamResult result = new StreamResult(os);
    
        transformer.transform(source, result);
        os.close();
	}
	
	/**
	 * parse XML document
	 * @param in
	 * @return
	 * @throws IOException
	 */
	public static Document parseXML(InputStream in) throws IOException {
		Document document = null;
		DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
		//factory.setValidating(true);
		//factory.setNamespaceAware(true);

		try {
			DocumentBuilder builder = factory.newDocumentBuilder();
			//builder.setErrorHandler(new XmlErrorHandler());
			//builder.setEntityResolver(new XmlEntityResolver());
			document = builder.parse(in);
			
			// close input stream
			in.close();
		}catch(Exception ex){
			throw new IOException(ex.getMessage());
		}
		return document;
	}
	
	/**
	 * get single element by tag name
	 * @param element
	 * @param tag
	 * @return
	 */
	public static Element getElementByTagName(Element element, String tag){
		NodeList list = element.getChildNodes();
		for(int i=0;i<list.getLength();i++){
			Node node = list.item(i);
			if(node instanceof Element && ((Element)node).getTagName().equals(tag)){
				return (Element) node;
			}
		}
		return null;
	}
	
	/**
	 * get single element by tag name
	 * @param element
	 * @param tag
	 * @return
	 */
	public static List<Element> getElementsByTagName(Element element, String tag){
		List<Element> elems = new ArrayList<Element>();
		NodeList list = element.getChildNodes();
		for(int i=0;i<list.getLength();i++){
			Node node = list.item(i);
			if(node instanceof Element){
				Element e = (Element) node;
				if(e.getTagName().equals(tag)){
					elems.add(e);
				}
			}
		}
		return elems;
	}
	
	/**
	 * get single element by tag name
	 * @param element
	 * @param tag
	 * @return
	 */
	public static List<Element> getChildElements(Element element){
		List<Element> elems = new ArrayList<Element>();
		NodeList list = element.getChildNodes();
		for(int i=0;i<list.getLength();i++){
			Node node = list.item(i);
			if(node instanceof Element){
				Element e = (Element) node;
				elems.add(e);
			}
		}
		return elems;
	}
}
