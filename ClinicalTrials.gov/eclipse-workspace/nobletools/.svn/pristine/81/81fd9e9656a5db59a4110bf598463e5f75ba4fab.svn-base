package edu.pitt.info.extract.model.util;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;


public class SynopticReportDetector {
	private List<Detector> synopticDetectors,falseDetectors;
	private List<String> emptyFiles  = new ArrayList<String>();
	private int total,empty,gross,prostate;
	public static interface Detector {
		public boolean detect(String line);
	}
	
	/**
	 * get a list of synoptic line detectors
	 * @return
	 */
	private List<Detector> getSynopticDetectors(){
		if(synopticDetectors == null){
			synopticDetectors = new ArrayList<SynopticReportDetector.Detector>();
			synopticDetectors.add(new Detector(){
				public boolean detect(String line){
					// if line starts with letter and space and line, then take the latter portion
					//Matcher mt =  Pattern.compile("[a-z0A-Z0-9]{1,2}\\.?[\\s-]+(.*)").matcher(line);
					//if(mt.matches())
					//	line = mt.group(1);
					// detect white _ or . gaps >=4 between words
					Matcher mt = Pattern.compile("[^\\s]+[\\._]{4,}[^\\s]+").matcher(line);
					return mt.find();
				}
			});
			synopticDetectors.add(new Detector(){
				public boolean detect(String line){
					// detect empty click cells s.a. ( )
					Matcher mt = Pattern.compile("\\(\\s*\\)").matcher(line);
					return mt.find();
				}
			});
			synopticDetectors.add(new Detector(){
				public boolean detect(String line){
					// detect tabs 
					Matcher mt = Pattern.compile("[^\\s]+[\\t]{1,}[^\\s]+").matcher(line);
					return mt.find();
				}
			});
			synopticDetectors.add(new Detector(){
				public boolean detect(String line){
					// does the line start with a word synoptic
					Matcher mt = Pattern.compile("^\\s*synoptic\\b").matcher(line.toLowerCase());
					return mt.find();
				}
			});
			synopticDetectors.add(new Detector(){
				public boolean detect(String line){
					// do we have ___ or _X_ lines representing worksheets?
					Matcher mt = Pattern.compile("^_[xX_]_").matcher(line);
					return mt.find();
				}
			});
			synopticDetectors.add(new Detector(){
				public boolean detect(String line){
					// do we have lines that start with a single letter or number end end with digits or hash
					return line.matches("^[A-Z0-9]\\.\\s*.*:\\s*(\\d|#)$");
				}
			});
			synopticDetectors.add(new Detector(){
				public boolean detect(String line){
					// do we have a line that has a set of upper case words, followed by column and at least 4 spaces and then other characters
					if(line.matches("^[A-Z ]+:\\s{4,}.*$")){
						// skip known false positives
						return !line.matches("^(PROCEDURE|POST-OP).*");
					}
					return false;
				}
			});
			synopticDetectors.add(new Detector(){
				public boolean detect(String line){
					// if line starts with letter and space and line, then take the latter portion
					Matcher mt =  Pattern.compile("[a-z0A-Z0-9]{1,2}\\.?[\\s-]+(.*)").matcher(line);
					if(mt.matches())
						line = mt.group(1);
					// detect white space or . gaps >=4 between words
					mt = Pattern.compile("[^\\s]+[\\s]{4,}[^\\s]+").matcher(line);
					if(mt.find()){
						// if alphabetical characters are less then 60% of the total, then we are good and not a false positive
						return (double)line.replaceAll("[^A-Za-z]","").length()/line.length() < 0.6;
					}
					return false;
				}
			});
			
		}
		return synopticDetectors;
	}
	
	/**
	 * get a list of synoptic line detectors
	 * @return
	 
	private List<Detector> getFalseDetectors(){
		if(falseDetectors == null){
			falseDetectors = new ArrayList<SynopticReportDetector.Detector>();
			falseDetectors.add(new Detector(){
				public boolean detect(String line){
					//if synoptic line quit
					if(line.toLowerCase().matches("^\\s*synoptic\\b.*"))
						return false;
					if(line.matches("^[A-Z0-9]\\.\\s*.*\\s\\d$"))
						return false;
					if(line.matches("^[A-Z ]+:\\s{4,}.*$"))
						return false;
					
					int count = line.replaceAll("[^A-Za-z]","").length();

					// if alphabetical characters are greater then 60% of the total, then false positive
					if(((double)count)/line.length() > .6){
						// if true, but contains other metrics, then ignore
						Matcher mt = Pattern.compile("\\(\\s*\\)").matcher(line);
						return !mt.find();
					}
					return false;
				}
			});
		}
		return falseDetectors;
	}
	*/
	
	/**
	 * does line belong to synoptic report?
	 * @param line
	 * @return
	 */
	private boolean detect(String line){
		// if synoptic detector fired
		if(detect(line,getSynopticDetectors())){
			// check known false positives
			//return (detect(line,getFalseDetectors()))?false:true;
			return true;
		}
		return false;
	}
	
	/**
	 * does line belong to synoptic report?
	 * @param line
	 * @return
	 */
	private boolean detect(String line,List<Detector> list){
		for(Detector d: list){
			if(d.detect(line))
				return true;
		}
		return false;
	}
	
	
	/**
	 * process document
	 * @param dir
	 */
	public void process(File f) throws Exception {
		if(f.isDirectory()){
			for(File c: f.listFiles()){
				process(c);
			}
		}else if(f.getName().endsWith(".txt")){
			System.out.println(f.getName()+"\n---------------------------");
			String tx = getText(f);
			String rp = getSynopticReport(tx);
			total++;
			if(rp.length()== 0){
				empty++;
				if(tx.contains("SYNOPTIC-  PRIMARY PROSTATE TUMORS")){
					prostate++;
				}
				emptyFiles.add(f.getName());
			}
			if(rp.contains("[Gross Description]"))
				gross++;
			System.out.println(rp);
		}
	}
	
	public String getText(File f) throws Exception {
		BufferedReader r = new BufferedReader(new FileReader(f));
		StringBuffer b = new StringBuffer();
		for(String l=r.readLine();l != null; l=r.readLine()){
			b.append(l+"\n");
		}
		return b.toString();
	}
	
	public int[] getSynopticReportRange(String text) {
		int st = -1, en = -1, offs = 0;
		int dcount = 0;
		for(String l: text.split("\n")){
			if(detect(l)){
				// if detected line, put starte offset
				if(st < 0)
					st = offs;
				//carry on with end offset
				en = offs+l.length()+1;
				// inclrement line count
				dcount ++;
			}else if(l.trim().length() > 0){
				//if not empty line
				
				// if we have a start, but there are less then 2 lines
				// reset count
				if(st > -1 && dcount < 2){
					st = -1;
					dcount = 0;
				}
				
				// if we get into another section heading
				// we overshot it, so quit
				if(st > -1 && (l.matches("^\\[[\\w ]+\\]$") || l.matches("^[A-Z\\- ]{4,20}:$"))){
					break;
				}
				
			}
			offs += l.length()+1;
		}
		int[] offsets = new int[2];
		if (st > 0 && dcount > 1) {
			offsets[0] = st;
			offsets[1] = en;
		}
		else {
			offsets[0] = -1;
			offsets[1] = -1;
		}
		return offsets;
	}
	
	
	/**
	 * process document
	 * @param dir
	 */
	public String getSynopticReport(String text){
		int[] offsets = getSynopticReportRange(text);
		int st = offsets[0];
		int en = offsets[1];
		return (st > 0 && en > 0) ? text.substring(st,en) : "";
	}
	
	
	/**
	 * @param args
	 */
	public static void main(String[] args) throws Exception {
		//args = new String [] {"/home/tseytlin/Data/Reports/SynopticReportsMany"};
		args = new String [] {"/home/tseytlin/Data/Reports/ODIE50"};
		//args = new String [] {"/home/tseytlin/Data/Reports/SynopticReports"};
		//args = new String [] {"/home/tseytlin/Data/Reports/SynopticReports","/home/tseytlin/Data/Reports/TIES Reports","/home/tseytlin/Data/Reports/SynopticReportsMany"};
		//args = new String [] {"/home/tseytlin/Data/Reports/TIES Reports"};
		SynopticReportDetector srd = new SynopticReportDetector();
		for(String a: args){
			srd.process(new File(a));
		}
		
		System.out.println("\n\nTotal: "+srd.total+"\nEmpty: "+srd.empty+"\nGross: "+srd.gross+"\nProstate: "+srd.prostate);
		System.out.println(srd.emptyFiles);
	}

}
