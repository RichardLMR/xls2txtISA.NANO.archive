#########################################################################################################
# test_1.py
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


class test_1(unittest.TestCase):
	
	def clean_up_if_all_checks_passed(self,specific_files_not_to_delete):
		all_files_to_delete = [file_name for file_name in glob.glob(r'%s%s*' % (delimiter().join(os.path.abspath(__file__).split(delimiter())[:-1]),delimiter())) if not re.search('(.\py$)',file_name) and not file_name in specific_files_not_to_delete]
		
		for FILE_TO_DELETE in all_files_to_delete:
			os.remove(FILE_TO_DELETE)
			assert not os.path.exists(FILE_TO_DELETE), " This still exists: \n %s" % FILE_TO_DELETE
			print 'Removed this temporary file: ', FILE_TO_DELETE
	
	def compareOriginalAndNewFiles(self,orig_file,new_file):
		
		print '-'*50
		print 'Comparing: '
		print orig_file
		print 'to:'
		print new_file
		print '-'*50
		
		file2Contents = {}
		
		for file_name in [orig_file,new_file]:
			f_in = open(file_name)
			try:
				file2Contents[file_name] = ''.join([re.sub(r'\r|\n','<EOL>',LINE) for LINE in f_in.readlines()])
				del LINE
			finally:
				f_in.close()
				del f_in
		del file_name
		
		
		assert file2Contents[orig_file] == file2Contents[new_file], " These files do not match: \n %s \n %s \n" % (orig_file,new_file)
	
	def checkStillWorks(self,all_input_files,all_new_files):
		all_orig_output_files_to_be_compared_as_required_for_unittesting = []
		for new_file in all_new_files:
			file_ext = new_file.split('.')[-1]
			orig_file = re.sub('(\.%s$)' % file_ext,' - Copy.%s' % file_ext,new_file)
			all_orig_output_files_to_be_compared_as_required_for_unittesting.append(orig_file)
			self.compareOriginalAndNewFiles(orig_file,new_file)
		
		files_not_to_delete = all_input_files+all_orig_output_files_to_be_compared_as_required_for_unittesting
		self.clean_up_if_all_checks_passed(specific_files_not_to_delete=files_not_to_delete)
	
	def test_changeXls2txt(self):
		##############################
		print 'Running unittests for this project: ', project_name
		print 'Running this unittest: ', self._testMethodName
		##############################
		
		import itertools
		from xls2txt import changeXls2txt
		
		input_file_extensions = ['xls']
		
		all_input_files = []
		
		for extension in input_file_extensions:
			extension_regex = re.compile('(\.%s$)' % extension)
			for input_file in glob.glob(r'%s%s*.%s' % (dir_of_the_current_test,delimiter(),extension)):
				no_nonblank_sheets = changeXls2txt(input_file,extension_regex)
				#assert 1 == no_nonblank_sheets, "%d non-blank sheets in %s!" % (no_nonblank_sheets,input_file)
				all_input_files.append(input_file)
		del input_file
		del extension
		
		assert 1 == len(all_input_files)
		
		all_new_files = list(itertools.chain(*[[re.sub('(\.%s)' % extension,'.txt',input_file) for input_file in glob.glob(r'%s%s*.%s' % (dir_of_the_current_test,delimiter(),extension))] for extension in input_file_extensions]))
		
		self.checkStillWorks(all_input_files,all_new_files)
