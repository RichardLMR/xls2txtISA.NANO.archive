#########################################################################################################
# test_10.py
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
#************************
import fixTxtContents
#************************
dir_of_the_current_test = delimiter().join(os.path.abspath(__file__).split(delimiter())[:-1])
print 'dir_of_the_current_test=',dir_of_the_current_test
import unittest
#************************
sys.path.append(r'%s%stests%stest_1' % (project_modules_to_test_dir,delimiter(),delimiter()))
from test_1 import test_1
#************************


class test_10_for_checking_specific_fixTxtContents_functions(test_1):
	
	def test_fixTxtContents_extractAccessionCode_function(self):
		##############################
		print 'Running unittests for this project: ', project_name
		print 'Running this unittest: ', self._testMethodName
		##############################
		
		toy_example_1 = "Characteristics[Product impurities found {MEDDRA:http://purl.bioontology.org/ontology/MDR/10069178}]"
		toy_example_2 = "http://purl.org/obo/owl/UO#UO_0000018"
		
		assert "http://purl.bioontology.org/ontology/MDR/10069178" == fixTxtContents.extractAccessionCode(toy_example_1),"extractAccessionCode(toy_example_1)=%s" % fixTxtContents.extractAccessionCode(toy_example_1)
		assert "http://purl.org/obo/owl/UO#UO_0000018" == fixTxtContents.extractAccessionCode(toy_example_2),"extractAccessionCode(toy_example_2)=%s" % fixTxtContents.extractAccessionCode(toy_example_2)
	
	def test_fixTxtContents_checkDuplicatedColumnTitlesAreAllowed_function(self):
		##############################
		print 'Running unittests for this project: ', project_name
		print 'Running this unittest: ', self._testMethodName
		##############################
		
		assert [] == fixTxtContents.findDuplicates(['x','y','z'])
		assert ['y'] == fixTxtContents.findDuplicates(['x','y','z','y'])
	
	def test_modifyColTitleOrContentItem_function(self):
		##############################
		print 'Running unittests for this project: ', project_name
		print 'Running this unittest: ', self._testMethodName
		##############################
		
		#=============================
		expectedInput2Output = {}
		
		expectedInput2Output['Factor Value[screening concentration]'] = 'Factor Value [screening concentration]'
		expectedInput2Output['Parameter Value[Instrument]'] = 'Parameter Value [Instrument]'
		expectedInput2Output['Measurement Value[z-average(hydrodynamic diameter)]'] = 'Measurement Value [z-average(hydrodynamic diameter)]'
		expectedInput2Output['Characteristics[strain {EFO:    http://www.ebi.ac.uk/efo/EFO_0005135}]'] = 'Characteristics [strain {EFO:http://www.ebi.ac.uk/efo/EFO_0005135}]'
		expectedInput2Output['Comment[Miscellaneous.1]'] = 'Comment [Miscellaneous.1]'
		
		#=============================
		
		for input in expectedInput2Output:
			assert expectedInput2Output[input] == fixTxtContents.modifyColTitleOrContentItem(input), "%s input gave %s when parsed via fixTxtContents.modifyColTitleOrContentItem???" % (input,fixTxtContents.modifyColTitleOrContentItem(input))




