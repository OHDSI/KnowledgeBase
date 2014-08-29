package edu.pitt.terminology.util;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class DeIDUtils {
	/**
	 * parse date produced by DeID software in format **DATE[Oct 15 2007] 1453 
	 * @param d
	 * @return
	 */
	public static Date parseDate(String d){
		SimpleDateFormat sd1 = new SimpleDateFormat("MMM d yyyy HH:mm");
		SimpleDateFormat sd2 = new SimpleDateFormat("MMM d yyyy");
		Pattern pt = Pattern.compile("\\*\\*DATE\\[([A-Za-z]+ \\d{1,2} \\d{4})\\](?:\\s(\\d{2})\\:?(\\d{2}))?");
		Matcher mt = pt.matcher(d);
		if(mt.matches()){
			String date = mt.group(1);
			String h = mt.group(2);
			String m = mt.group(3);
			try{
				if(h != null){
					return sd1.parse(date+" "+h+":"+m);
				}else{
					return sd2.parse(date);
				}
			}catch(ParseException ex){}
		}
		return null;
	}
	
	/**
	 * is this line a predefine De-ID header that should be ignored?
	 * @param line
	 * @return
	 */
	public static boolean isDeIDHeader(String line){
		return line != null && (line.matches("\\[.* de\\-identified.*De\\-ID.*\\]") || line.matches("[SE]_O_[HR]"));
	}
	
	
	
	/**
	 * blank out DeID tags from text
	 * @param line
	 * @return
	 */
	public static String filterDeIDTags(String line){
		if(line == null || line.length() == 0)
			return line;
		// find and replace all tags
		Pattern pt = Pattern.compile("\\*?\\*\\*[A-Z\\-]+(\\[.*\\])?");
		Matcher mt = pt.matcher(line);
		StringBuffer buffer = new StringBuffer(line);
		while(mt.find()){
			buffer.replace(mt.start(),mt.end(),fill(mt.group().length()));
		}
		return buffer.toString();
	}

	private static String fill(int length) {
		StringBuffer b = new StringBuffer();
		for(int i=0;i<length;i++)
			b.append(" ");
		return b.toString();
	}
}
