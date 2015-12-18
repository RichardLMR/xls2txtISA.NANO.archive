#########################################################################################################
# test_15.py
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
example_input = '%s%sTOY.test_15.zip' % (dir_of_the_current_test,delimiter())
example_output_to_compare_to = glob.glob(r'%s%s* - Copy.txt' % (dir_of_the_current_test,delimiter()))
expected_no_output_files = 8
assert expected_no_output_files == len(example_output_to_compare_to) #This line would actually be useful in earlier unit tests!
assert expected_no_output_files == len([file for file in example_output_to_compare_to if os.path.exists(file)]), "%s???" % str(example_output_to_compare_to) #This line would actually be useful in earlier unit tests!
del file #This line would actually be useful in earlier unit tests!

class test_15(test_1):
	
	def test_NanoPUZZLES_inconsistency_fix_1(self):
		##############################
		print 'Running unittests for this project: ', project_name
		print 'Running this unittest: ', self._testMethodName
		##############################
		
		##########################
		#This unit test is designed to check (an aspect of) the "-N" option for this program i.e. the conversion of potentially inconsistent fields in datasets arising from older versions of the NanoPUZZLES ISA-TAB-Nano templates
		#N.B. The "....TOY.test_11... - Copy.txt" files (which were checked to make sure they were not inconsistent with the expected changes to be made via the "-N" option) were just renamed and the "TOY.test_11.zip" Excel files were updated to make sure they contained (one of) the inconsistencies that the "-N" option is designed to fix, then all such files were renamed to give "TOY.test_15.zip".
		#[*] In addition, given the changes to the file names, the internal contents of the files (both Excel and expected text output) needed to be edited such that "TOY.test_11" was replaced with "TOY.test_15" for consistency.
		#########################
		
		##############################
		#test_15: inconsistency(ies) fix which is (are) being tested: removal of "Manufacturer supplied " prefixes for Material file "Characteristics [...]" and corresponding "Comment [...:from graph]" fields
		##############################
		
		#cmd = r'python "%s%sxls2txtISA.NANO.archive.py" -i "%s"' % (project_modules_to_test_dir,delimiter(),example_input) #[*] To check no problems with updating names from test_11 files, this test was initially run without making any changes except replacing "TOY.test_11" with "TOY.test_15" in file names and internal contents => OK [test output scrolled through to see that expected comparisons were being made]. Also, a minor error was introduced to check that self.compareOriginalAndNewFiles(orig_file,new_file) would fail as expected for one file => OK [this error was then fixed, this command was ran again with no errors and the files were further updated for the purpose of this test].
		cmd = r'python "%s%sxls2txtISA.NANO.archive.py" -i "%s" -N' % (project_modules_to_test_dir,delimiter(),example_input)
		
		assert 0 == os.system(cmd)
		
		instOfzipUtils = zipUtils(delimiter_value=delimiter())
		
		sub_folder_count = instOfzipUtils.archive2folder(re.sub('(\.zip$)','-txt_opt-N.zip',example_input))
		
		cwd = os.getcwd()
		
		os.chdir(re.sub('(\.zip$)','-txt_opt-N',example_input))
		comparisons_count = 0 #This line would actually be useful in earlier unit tests!
		for orig_file in example_output_to_compare_to:
			new_file = r'%s%s%s' % (os.getcwd(),delimiter(),re.sub('( - Copy\.txt)','.txt',orig_file.split(delimiter())[-1]))
			self.compareOriginalAndNewFiles(orig_file,new_file)
			os.remove(new_file)
			comparisons_count += 1 #This line would actually be useful in earlier unit tests!
		assert expected_no_output_files == comparisons_count, "comparisons_count=%d;expected_no_output_files=%d" % (comparisons_count,expected_no_output_files) #This line would actually be useful in earlier unit tests!
		os.chdir(cwd)
		
		os.remove(re.sub('(\.zip$)','-txt_opt-N.zip',example_input))
		os.rmdir(re.sub('(\.zip$)','-txt_opt-N',example_input))



