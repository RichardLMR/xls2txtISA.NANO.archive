'''
xls2txtISA.NANO.archive.py

***********************
The research leading to the development of this program has received funding from the European Union Seventh Framework Programme (FP7/2007-2013) under grant agreement number 309837 (NanoPUZZLES project).

http://wwww.nanopuzzles.eu
************************

######################
#License information##
######################
Copyright (c) 2015 Liverpool John Moores University
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or (at
your option) any later version.

THIS PROGRAM IS MADE AVAILABLE FOR DISTRIBUTION WITHOUT ANY FORM OF WARRANTY TO THE 
EXTENT PERMITTED BY APPLICABLE LAW.  THE COPYRIGHT HOLDER PROVIDES THE PROGRAM \"AS IS\" 
WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT  
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR 
PURPOSE. THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM LIES
WITH THE USER.  SHOULD THE PROGRAM PROVE DEFECTIVE IN ANY WAY, THE USER ASSUMES THE
COST OF ALL NECESSARY SERVICING, REPAIR OR CORRECTION. THE COPYRIGHT HOLDER IS NOT 
RESPONSIBLE FOR ANY AMENDMENT, MODIFICATION OR OTHER ENHANCEMENT MADE TO THE PROGRAM 
BY ANY USER WHO REDISTRIBUTES THE PROGRAM SO AMENDED, MODIFIED OR ENHANCED.

IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING WILL THE 
COPYRIGHT HOLDER BE LIABLE TO ANY USER FOR DAMAGES, INCLUDING ANY GENERAL, SPECIAL,
INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OR INABILITY TO USE THE
PROGRAM (INCLUDING BUT NOT LIMITED TO LOSS OF DATA OR DATA BEING RENDERED INACCURATE
OR LOSSES SUSTAINED BY THE USER OR THIRD PARTIES OR A FAILURE OF THE PROGRAM TO 
OPERATE WITH ANY OTHER PROGRAMS), EVEN IF SUCH HOLDER HAS BEEN ADVISED OF THE 
POSSIBILITY OF SUCH DAMAGES.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

####################
See also: http://www.gnu.org/licenses/ (last accessed 14/01/2013)

Contact: 
1. R.L.MarcheseRobinson@ljmu.ac.uk
or if this fails
2. rmarcheserobinson@gmail.com
#####################

########
Purpose# 
########
To convert a compressed, *flat* archive ("yyyy.zip") populated with ISA-TAB-Nano based ".xls" files, to a corresponding compressed, *flat* archive ("yyyy-txt.zip") of ISA-TAB-Nano based tab delimited text (".txt") files.  
N.B. ISA-TAB-Nano is described here:https://wiki.nci.nih.gov/display/ICR/ISA-TAB-Nano
DISCLAIMER: No endorsements from the original ISA-TAB-Nano developers or any other third party organisations should be inferred.

########
Usage  # 
########

python xls2txtISA.NANO.archive.py -i <absolute name of zip file containing ISA-TAB-Nano files in ".xls" format>

e.g.

python xls2txtISA.NANO.archive.py -i "C:\Work\Investigation.ID.zip"

Options:

-a : modify "Term Accession Numbers" = TRUE (default:FALSE). N.B. If this is set to TRUE, http://purl.bioontology.org/ontology/npo#NPO_1915 would be converted to NPO_1915 etc. This may be required by some ISA-TAB-Nano software programs.

-c : remove all "Comment" rows from the Investigation file. Some ISA-TAB-Nano software programs may not accept these rows.

-N: edit certain fields (or field entries) to be consistent with the latest version of the NanoPUZZLES ISA-TAB-Nano Excel templates

'''
###########################
#######Imports#############
import sys,re,glob,getopt,shutil,os
dir_of_this_file = re.sub('(xls2txtISA\.NANO\.archive\.py)','',os.path.abspath(__file__))
sys.path.append(r'%sutils' % dir_of_this_file)
from zipper import zipUtils
from os_ind_delimiter import delimiter
from xls2txt import changeXls2txt
from fixTxtContents import fixContents
###########################

##########################
########Globals###########
#*************************************
#Fixed
#*************************************
fileNameRegexesDict = {}
fileNameRegexesDict['input_extension'] = re.compile('(\.xls$)')
fileNameRegexesDict['Investigation'] = re.compile('(i_)')
fileNameRegexesDict['Study'] = re.compile('(s_)')
fileNameRegexesDict['Material'] = re.compile('(m_)')
fileNameRegexesDict['Assay'] = re.compile('(a_)')
all_file_types = [key for key in fileNameRegexesDict.keys() if not 'input_extension' == key]
del key
##########################

def extractXlsFolder(xls_archive):
	
	instOfzipUtils = zipUtils(delimiter())
	
	sub_folder_count = instOfzipUtils.archive2folder(xls_archive)
	
	assert 0 == sub_folder_count
	
	return instOfzipUtils.folder_name

def idInputFiles(xls_folder):
	
	instOfzipUtils = zipUtils(delimiter())
	
	input_files = instOfzipUtils.getRelativeFileNames(xls_folder)
	input_files = [r'%s%s%s' % (xls_folder,delimiter(),file) for file in input_files if fileNameRegexesDict['input_extension'].search(file)]
	del file
	
	del instOfzipUtils
	
	#non_xls_files = [file_name for file_name in input_files if not fileNameRegexesDict['input_extension'].search(file_name)]
	#del file_name
	
	#assert 0 == len(non_xls_files),"There are %d non-xls files in the folder %s created from the input archive." % (len(non_xls_files),xls_folder)
	#del non_xls_files
	
	fileType2No = {}
	for fileType in all_file_types:
		fileType2No[fileType] = len([file_name for file_name in input_files if fileNameRegexesDict[fileType].match(file_name.split(delimiter())[-1])])
		assert not 0 == fileType2No[fileType], "Zero %s input files in the folder created from the input archive!" % fileType
		print "%d %s input files in the folder created from the input archive!" % (fileType2No[fileType],fileType)
	del fileType2No
	
	return input_files#,non_xls_files  #non_xls_files should just be copied across to the final zip archive without modification -see "def createFlatTxtArchive(xls_folder):"




def createAllTxt(xls_folder,mustEditAccessionCodes,mustRemoveComments,mustMakeNanoPUZZLESspecificChanges):
	
	abs_name_input_files = idInputFiles(xls_folder)
	
	for xls_file in abs_name_input_files:
		txt_file = changeXls2txt(xls_file,fileNameRegexesDict['input_extension'])
		
		applicable_standard_file_types = [ft for ft in all_file_types if fileNameRegexesDict[ft].match(txt_file.split(delimiter())[-1])]
		del ft
		assert 1 >= len(applicable_standard_file_types),"txt_file=%s,applicable_standard_file_types=%s" % (txt_file,str(applicable_standard_file_types))
		
		if 1 == len(applicable_standard_file_types):
			current_file_type = applicable_standard_file_types[0]
		else:
			assert 0 == len(applicable_standard_file_types),"txt_file=%s,applicable_standard_file_types=%s" % (txt_file,str(applicable_standard_file_types))
			current_file_type = 'NonStandard'
		del applicable_standard_file_types
		
		fixContents(input_file=txt_file,out_name=None,del_intermediates=True,file_type=current_file_type,shouldEditAccessionCodes=mustEditAccessionCodes,shouldRemoveComments=mustRemoveComments,shouldMakeNanoPUZZLESspecificChanges=mustMakeNanoPUZZLESspecificChanges)
		

def createFlatTxtArchive(xls_folder,mustEditAccessionCodes,mustRemoveComments,mustMakeNanoPUZZLESspecificChanges):
	
	flat_txt_archive = xls_folder+"-txt.zip"
	
	###########
	#Rename the output file if non-default options are used
	if mustEditAccessionCodes:
		flat_txt_archive = re.sub('(\.zip$)','_opt-a.zip',flat_txt_archive)
	if mustRemoveComments:
		flat_txt_archive = re.sub('(\.zip$)','_opt-c.zip',flat_txt_archive)
	if mustMakeNanoPUZZLESspecificChanges:
		flat_txt_archive = re.sub('(\.zip$)','_opt-N.zip',flat_txt_archive)
	###########
	
	cwd = os.getcwd()
	os.chdir(xls_folder)
	for xls_file in glob.glob('*.xls'):
		os.remove(xls_file)
	os.chdir(cwd)
	del cwd,xls_file
	
	instOfzipUtils = zipUtils(delimiter_value=delimiter())
	
	instOfzipUtils.filesIntoFlatArchive(folder_name=xls_folder,zip_archive=flat_txt_archive)
	
	del instOfzipUtils

def cleanUp(folder_list):
	
	for folder in folder_list:
		cwd = os.getcwd()
		os.chdir(folder)
		for file in glob.glob('*'):
			os.remove(file)
		os.chdir(cwd)
		os.rmdir(folder)



def main():
	
	#######################
	#**********************
	#These Boolean variables can be changed from their default values using command line switches
	#**********************
	mustEditAccessionCodes = False
	mustRemoveComments = False
	mustMakeNanoPUZZLESspecificChanges = False
	#######################
	
	print '-'*50
	
	try:
		#############
		opts,args = getopt.getopt(sys.argv[1:],'Ncai:',['mustMakeNanoPUZZLESspecificChanges=True','mustRemoveComments=True','mustEditAccessionCodes=True','input='])
		for o,v in opts:
			if '-i' == o:
				xls_archive = r'%s' % re.sub('"','',v)
			if '-a' == o:
				mustEditAccessionCodes = True
			if '-c' == o:
				mustRemoveComments = True
			if '-N' == o:
				mustMakeNanoPUZZLESspecificChanges = True
		del o,v,opts,args
		#############
	except Exception:
		print __doc__
		sys.exit(1)
	
	print 'Converting:', xls_archive
	
	xls_folder = extractXlsFolder(xls_archive)
	
	createAllTxt(xls_folder,mustEditAccessionCodes,mustRemoveComments,mustMakeNanoPUZZLESspecificChanges)
	
	createFlatTxtArchive(xls_folder,mustEditAccessionCodes,mustRemoveComments,mustMakeNanoPUZZLESspecificChanges)
	
	cleanUp([xls_folder])
	
	print xls_archive, " CONVERTED SUCCESSFULLY"
	print '-'*50
	
	return 0

if __name__ == '__main__':
	sys.exit(main())
