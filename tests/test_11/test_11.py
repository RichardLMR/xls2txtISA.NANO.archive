#########################################################################################################
# test_11.py
# Implements unit tests This file was adapted from test_1.py obtained from version 0.1 of the following project:http://code.google.com/p/generic-qsar-py-utils/
# Copyright (c) 2013 Syngenta
# Copyright (c) 2015 Liverpool John Moores University
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or (at
# your option) any later version.

# THIS PROGRAM IS MADE AVAILABLE FOR DISTRIBUTION WITHOUT ANY FORM OF WARRANTY TO THE 
# EXTENT PERMITTED BY APPLICABLE LAW.  THE COPYRIGHT HOLDER PROVIDES THE PROGRAM \"AS IS\" 
# WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT  
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR 
# PURPOSE. THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM LIES
# WITH THE USER.  SHOULD THE PROGRAM PROVE DEFECTIVE IN ANY WAY, THE USER ASSUMES THE
# COST OF ALL NECESSARY SERVICING, REPAIR OR CORRECTION. THE COPYRIGHT HOLDER IS NOT 
# RESPONSIBLE FOR ANY AMENDMENT, MODIFICATION OR OTHER ENHANCEMENT MADE TO THE PROGRAM 
# BY ANY USER WHO REDISTRIBUTES THE PROGRAM SO AMENDED, MODIFIED OR ENHANCED.

# IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING WILL THE 
# COPYRIGHT HOLDER BE LIABLE TO ANY USER FOR DAMAGES, INCLUDING ANY GENERAL, SPECIAL,
# INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OR INABILITY TO USE THE
# PROGRAM (INCLUDING BUT NOT LIMITED TO LOSS OF DATA OR DATA BEING RENDERED INACCURATE
# OR LOSSES SUSTAINED BY THE USER OR THIRD PARTIES OR A FAILURE OF THE PROGRAM TO 
# OPERATE WITH ANY OTHER PROGRAMS), EVEN IF SUCH HOLDER HAS BEEN ADVISED OF THE 
# POSSIBILITY OF SUCH DAMAGES.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#########################################################################################################

#########################
project_name = 'xls2txtISA.NANO.archive'
run_tests_levels_below_top_dir = 1
this_test_levels_below_top_dir = 2
#########################
#************************
import sys,re,os,glob
cwd = os.getcwd()
for level in range(1,(run_tests_levels_below_top_dir+1)):
	os.chdir('..')
	#print os.getcwd()
del level
sys.path.append('utils')
from os_ind_delimiter import delimiter
from zipper import zipUtils
os.chdir(cwd)
del cwd
project_modules_to_test_dir = delimiter().join(os.path.abspath(__file__).split(delimiter())[:-(this_test_levels_below_top_dir+1)])
print 'project_modules_to_test_dir=',project_modules_to_test_dir
sys.path.append(project_modules_to_test_dir)
sys.path.append(r'%s%sutils' %(project_modules_to_test_dir,delimiter()))
dir_of_the_current_test = delimiter().join(os.path.abspath(__file__).split(delimiter())[:-1])
print 'dir_of_the_current_test=',dir_of_the_current_test
import unittest
#************************
sys.path.append(r'%s%stests%stest_1' % (project_modules_to_test_dir,delimiter(),delimiter()))
from test_1 import test_1
example_input = '%s%sTOY.test_11.zip' % (dir_of_the_current_test,delimiter())
example_output_to_compare_to = glob.glob(r'%s%s* - Copy.txt' % (dir_of_the_current_test,delimiter()))
#assert not 0 == len(example_output_to_compare_to)
#assert not 0 == len([file for file in example_output_to_compare_to if not os.path.exists(file)]), "%s???" % str(example_output_to_compare_to) #Curiously, this fails as does os.path.isfile(...), even though file names look valid!
#del file 

class test_11(test_1):
	
	def test_parseTOYtest11_defaultOptions(self):
		##############################
		print 'Running unittests for this project: ', project_name
		print 'Running this unittest: ', self._testMethodName
		##############################
		
		##########################
		#Observations regarding TOY.test_11.zip files which are relevant to testing capabilities of the code to fix xls errors:
		#s_TOY.test_11_InVitro.CB.xls => "Factor Value[culture medium]" : should be converted to "Factor Value [culture medium]" in txt version
		#a_TOY.test_11_PC_size_TEM.xls => "Parameter Value[Instrument Version]" : ditto "Parameter Value [Instrument Version]"
		#ditto => "Measurement Value[maximum(diameter)]" ditto "Measurement Value [maximum(diameter)]"
		#m_TiO2_TOY.test_11.xls -> Excel 2010 saved as tab delimited text => "Characteristics [Product impurities found {MEDDRA:\nhttp://purl.bioontology.org/ontology/MDR/10069178}]" i.e. this field contained a line ending inside a field - which should be removed in code created version!
		#ditto =>  Characteristics[purity {NPO: http://purl.bioontology.org/ontology/npo#NPO_1345}] : should be converted to "Characteristics [purity {NPO: http://purl.bioontology.org/ontology/npo#NPO_1345}]"
		#########################
		
		
		
		cmd = r'python "%s%sxls2txtISA.NANO.archive.py" -i "%s"' % (project_modules_to_test_dir,delimiter(),example_input)
		
		assert 0 == os.system(cmd)
		
		instOfzipUtils = zipUtils(delimiter_value=delimiter())
		
		sub_folder_count = instOfzipUtils.archive2folder(re.sub('(\.zip$)','-txt.zip',example_input))
		
		cwd = os.getcwd()
		
		os.chdir(re.sub('(\.zip$)','-txt',example_input))
		
		for orig_file in example_output_to_compare_to:
			new_file = r'%s%s%s' % (os.getcwd(),delimiter(),re.sub('( - Copy\.txt)','.txt',orig_file.split(delimiter())[-1]))
			self.compareOriginalAndNewFiles(orig_file,new_file)
			os.remove(new_file)
		
		os.chdir(cwd)
		
		os.remove(re.sub('(\.zip$)','-txt.zip',example_input))
		os.rmdir(re.sub('(\.zip$)','-txt',example_input))



