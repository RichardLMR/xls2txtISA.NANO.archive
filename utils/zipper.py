#########################################################################################################
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

import os,re,zipfile,glob

class zipUtils():
	
	def __init__(self,delimiter_value):
		self.zip_ext_regex = re.compile('(\.zip$)')
		self.delimiter_value=delimiter_value
	
	def archive2folder(self,zip_archive,folder_name=None):
		
		#########################
		assert self.zip_ext_regex.search(zip_archive), "This zip archive does not have a valid .zip extension:\n %s" % zip_archive
		
		if folder_name is None:
			folder_name=self.zip_ext_regex.sub('',zip_archive)
		self.folder_name = folder_name
		#########################
		
		print '*'*50
		print 'Trying to extract files from:' , zip_archive
		print 'into a directory with this name:',folder_name
		
		arch_handle = zipfile.ZipFile(zip_archive,"r")
		try:
			
			cwd = os.getcwd()
			os.mkdir(folder_name)
			os.chdir(folder_name)
			
			name_count =0
			extract_count=0
			sub_folder_count = 0
			for file_name in arch_handle.namelist():
				if not re.search('(/$)',file_name): #file_name ending with dir delimiter is actually a directory name!
					name_count +=1
					data = arch_handle.read(file_name)
					try:
						if re.search('(/)',file_name): 
							dirs = file_name.split('/')[:-1]
							file_name = file_name.split('/')[-1] #We want relative file names!
						try:
							f_out = open(file_name,'wb')
							try:
								f_out.write(data)
								extract_count +=1
							finally:
								f_out.close()
								del f_out
						except IOError:
							print 'Problem creating this file: ', file_name
					finally:
						del data
				else:
					sub_folder_count += 1
			
			os.chdir(cwd)
			
		finally:
			arch_handle.close()
			del arch_handle
		print '%d files found in %d subdirectories. %d files extracted.' % (name_count,sub_folder_count,extract_count)
		print '*'*50
		
		return sub_folder_count
	
	def getRelativeFileNames(self,folder_name):
		cwd = os.getcwd()
		os.chdir(folder_name)
		all_file_names = glob.glob('*')
		os.chdir(cwd)
		return all_file_names
	
	def folder2archive(self,folder_name,zip_archive=None):
		
		#################
		if zip_archive is None:
			zip_archive = folder_name+'.zip'
		assert self.zip_ext_regex.search(zip_archive), "This zip archive does not have a valid .zip extension:\n %s" % zip_archive
		##################
		
		all_file_names = self.getRelativeFileNames(folder_name)
		
		with zipfile.ZipFile(zip_archive, 'w') as myzip:
			myzip.write(folder_name, os.path.basename(folder_name), zipfile.ZIP_DEFLATED)
			for file_name in all_file_names:
				abs_file_name = r'%s%s%s' % (folder_name,self.delimiter_value,file_name)
				myzip.write(abs_file_name,r'%s%s%s' % (os.path.basename(folder_name),self.delimiter_value,file_name), zipfile.ZIP_DEFLATED)
	
	def filesIntoFlatArchive(self,folder_name,zip_archive):
		##############
		assert self.zip_ext_regex.search(zip_archive), "This zip archive does not have a valid .zip extension:\n %s" % zip_archive
		###############
		
		all_file_names = self.getRelativeFileNames(folder_name)
		
		with zipfile.ZipFile(zip_archive, 'w') as myzip:
			for file_name in all_file_names:
				abs_file_name = r'%s%s%s' % (folder_name,self.delimiter_value,file_name)
				myzip.write(abs_file_name,file_name, zipfile.ZIP_DEFLATED)


