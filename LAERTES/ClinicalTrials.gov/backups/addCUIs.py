"""
addCUIs.py

Jeremy Jao
07.24.2014

Get the sheet names...

for sheets in book.sheet_names():
		print sheets
result:
C-ctdata3-v011

example of getColInfo(sheet, 0):
NCT
text
type
Enrollment
enrollment_type
Phases
msh_condition
msh_intervention
searchURL



"""
__author__ = 'Jeremy Jao'
__date__ = '07.24.2014'

import xlrd
import xlwt
import xlutils

###########################
inp = 'Example-CT.gov-data-v3-v011.xlsx'

text = 1
#column for the text



mp = '/media/Backup/UMLS-Triads-OHDSI-subset-Feb2014/2013AB/META/MRCONSO.RRF'
out = 'Example-CT.gov-data-v3-v011.xlsx'
###########################

def getColInfo(sheet, row):
	list = []
	for col in xrange(row, sheet.ncols):
		print sheet.cell_value(1, col)


########################################################################
def main():
	
	book = xlrd.open_workbook(filename=inp)
	
	sheet = book.sheet_by_index(0)
	
	for row in xrange(1, sheet.nrows):
		
########################################################################

if __name__ == "__main__":
	main()
