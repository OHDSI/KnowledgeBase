package edu.pitt.terminology.util;
import java.io.EOFException;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.net.URL;
import java.net.URLConnection;

public class Sender {
	private URL servletURL;
	
	/**
	 * set servlet URL
	 */
	public Sender(URL s){
		servletURL = s;	 
	}
	
	public URL getServletURL(){
		return servletURL;
	}
	
	/**
	 * Send object to the servlet and get a reply
	 */
	public Object sendObject(Object obj) {
		URLConnection conn = null;
		Object reply = null;	
		
		
		// send object
		try {
			// open URL connection
			conn = servletURL.openConnection();
			conn.setDoInput(true);
			conn.setDoOutput(true);
			conn.setUseCaches( false );
		
			// send object
			ObjectOutputStream objOut = new ObjectOutputStream( conn.getOutputStream() );
			objOut.writeObject( obj );
			objOut.flush();
			objOut.close();
		} catch ( IOException ex ) {
			ex.printStackTrace();
			return null;
		}
		
		// recieve reply
		try{
			ObjectInputStream objIn = new ObjectInputStream( conn.getInputStream() );
			reply = objIn.readObject();
			objIn.close();
		} catch ( Exception ex ) {
			// it is ok if we get an exception here
			// that means that there is no object being returned
			if( !(ex instanceof EOFException))
				ex.printStackTrace();
			//System.err.println("*");
			//ex.printStackTrace();
		}	
		return reply;
	}
}
