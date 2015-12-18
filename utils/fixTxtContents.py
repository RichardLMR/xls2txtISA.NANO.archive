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

import re,sys,csv,os
from collections import defaultdict
#########################
######Globals############
#########################
#*******************
fileType2literalFileContents2Replace = defaultdict(dict)
fileType2literalFileContents2Replace['all']['.xls'] = '.txt'
#=============================================
#see generic "xls" templates (ISA-TAB-Nano version 1.2) available from https://wiki.nci.nih.gov/x/MwGGAg (last checked 23/10/14)
fileType2literalFileContents2Replace['Investigation']['Term Source Ref'] = 'Term Source REF'
fileType2literalFileContents2Replace['Material']['Term Source Ref'] = 'Term Source REF'
# fileType2literalFileContents2Replace['Study']['Term Source REF'] = 'Term Source Ref'
# fileType2literalFileContents2Replace['Assay']['Term Source REF'] = 'Term Source Ref'
#N.B. 12/02/2015: checking of the following pages => all occurrences of 'Term Source Ref' in any file type should actually be replaced with 'Term Source REF'!
#https://wiki.nci.nih.gov/display/ICR/Investigation
#https://wiki.nci.nih.gov/display/ICR/Study
#https://wiki.nci.nih.gov/display/ICR/Assay
#https://wiki.nci.nih.gov/display/ICR/Material
fileType2literalFileContents2Replace['Study']['Term Source Ref'] = 'Term Source REF'
fileType2literalFileContents2Replace['Assay']['Term Source Ref'] = 'Term Source REF'
#=============================================
fileType2literalFileContents2Replace['Material']['QS[inherent]'] = 'QS(inherent)' #12/02/2015: quality score fields under revision within NanoPUZZLES; these columns are not included in the current,publicly released versions of the templates
fileType2literalFileContents2Replace['Investigation']['Study Assay Measurement Term'] = 'Study Assay Measurement Type Term'
#*******************
non_suspicious_duplicated_column_titles = ['Protocol REF','Term Accession Number','Term Source Ref','Term Source REF','Unit','Sample Name'] #06/12/15: actually, column titles such as Characteristics [...] and, maybe, Factors might be duplicated under certain circumstances e.g. a "Characteristics [cell type]" associated with a "Source Name" column and another "Characteristics [cell type] associated with the corresponding "Sample Name" on account of differentiation of the originally received cells => checkDuplicatedColumnTitlesAreAllowed(...) was updated and renamed
non_suspicious_duplicated_column_titles += ['"%s"' % title for title in non_suspicious_duplicated_column_titles]
del title
duplicate_marker = '_duplicate_'
#####################################
almost_ac_regex = re.compile('(http.*)') #This is designed to identify ontology term URIs as might be found in the BioPortal ID field for an ontology term e.g. see http://bioportal.bioontology.org/ontologies/NCIT?p=classes&conceptid=http%3A%2F%2Fncicb.nci.nih.gov%2Fxml%2Fowl%2FEVS%2FThesaurus.owl%23C3262 (last accessed on 10th of June 2015) #N.B. This will not remove any trailing "}" c.f. "Characteristics[...]" fields! #see BioPortal assigned "Term URIs" description in http://www.ncbi.nlm.nih.gov/pmc/articles/PMC4159173/ (last accessed on the 10th of June 2015);also see an example of the "complete URI of the term" http://www.bioontology.org/wiki/index.php/NCBO_Widgets (last accessed on the 10th of June 2015); also see http://nar.oxfordjournals.org/content/39/suppl_2/W541.full#F2 (last accessed on the 10th of June 2015) for a discussion of when BioPortal assigns its own term URIs.  #This is simpler, but less general, than the more general regex for URIs proposed here by Mikael Lepisto: http://stackoverflow.com/questions/520031/whats-the-cleanest-way-to-extract-urls-from-a-string-using-python (last accessed on the 10th of June 2015)
#########################

def findDuplicates(some_list):
	
	element2count = defaultdict(int)
	
	for element in some_list:
		element2count[element] += 1
	del element
	
	duplicates = [element for element in element2count if element2count[element] > 1]
	
	return duplicates

#def checkDuplicatedColumnTitlesAreAllowed(column_titles,allowed_dup_cts=non_suspicious_duplicated_column_titles):
#06/12/15: actually, column titles such as Characteristics [...] and, maybe, Factors might be duplicated under certain circumstances e.g. a "Characteristics [cell type]" associated with a "Source Name" column and another "Characteristics [cell type] associated with the corresponding "Sample Name" on account of differentiation of the originally received cells => checkDuplicatedColumnTitlesAreAllowed(...) was updated and renamed
def checkDuplicatedColumnTitlesAreNotSuspicious(column_titles,ok_dup_cts=non_suspicious_duplicated_column_titles):
	duplicated_column_titles = findDuplicates(column_titles)
	
	ret_val = ''
	
	if not 0 == len(duplicated_column_titles):
		suspicious_duplicates = [ct for ct in duplicated_column_titles if not ct in ok_dup_cts]
		del ct
		if not 0 == len(suspicious_duplicates):
			ret_val =  "WARNING: suspicious duplicates:%s" % str(suspicious_duplicates)
		del suspicious_duplicates
		
	return ret_val

def makeNanoPUZZLESspecificChanges_dueToTemplateUpdates(col_title_or_content_item,current_file_type):
	
	#############################
	#The following changes may be required due to iterative updating of the NanoPUZZLES ISA-TAB-Nano templates:
	##############################
	col_title_or_content_item = col_title_or_content_item.replace("Manufacturer supplied ",'')
	
	col_title_or_content_item = col_title_or_content_item.replace("nanoparticle sample","nanomaterial")
	col_title_or_content_item = col_title_or_content_item.replace("http://purl.bioontology.org/ontology/npo#NPO_1404","http://purl.bioontology.org/ontology/npo#NPO_199")
	
	if 'UNKNOWN' == col_title_or_content_item:
		col_title_or_content_item = ''
	
	if "Characteristics[shape]" == col_title_or_content_item:
		col_title_or_content_item = "Characteristics [shape {NPO:http://purl.bioontology.org/ontology/npo#NPO_274}]"
		assert 'Material' == current_file_type,"Characteristics[shape] in file of this type:%s" % current_file_type
	
	if "Measurement Value[zeta potential]" == col_title_or_content_item: 
		col_title_or_content_item = "Measurement Value[mean(zeta potential)]"
		assert 'Assay' == current_file_type,"Measurement Value[zeta potential] in file of this type:%s" % current_file_type
	
	return col_title_or_content_item

def fixCommentsWithDots(col_title_or_content_item):#,current_file_type):
	##################
	#The following changes were specifically required for some NanoPUZZLES datasets because they were observed to throw errors upon trying to import into the nanoDMS system [http://biocenitc-deq.urv.cat/nanodms/, last accessed on 4th of June 2015] due to the restriction on "." characters in the headers of the Material, Study or Assay files being violated by comments columns such as "Comment[miscellaneous.5]" and "Comment[Miscellaneous.1]"
	##################
	
	comments_with_dots_regex = re.compile('(Comment\s*\[miscellaneous\.)',re.IGNORECASE)
	
	col_title_or_content_item = comments_with_dots_regex.sub("Comment [miscellaneous_",col_title_or_content_item)
	
	return col_title_or_content_item

def makeNanoPUZZLESspecificChanges(col_title_or_content_item,current_file_type):
	
	col_title_or_content_item = makeNanoPUZZLESspecificChanges_dueToTemplateUpdates(col_title_or_content_item,current_file_type)
	
	return col_title_or_content_item

def modifyColTitleOrContentItem(col_title_or_content_item,current_file_type=None,includingNanoPUZZLESspecificChanges=False):
	
	if includingNanoPUZZLESspecificChanges:
		col_title_or_content_item = makeNanoPUZZLESspecificChanges(col_title_or_content_item,current_file_type)
	
	col_title_or_content_item = fixCommentsWithDots(col_title_or_content_item)#,current_file_type)
	
	col_title_or_content_item = re.sub('(\r|\n)','',col_title_or_content_item)
	
	col_title_or_content_item = re.sub('(\s*;\s*)',';',col_title_or_content_item)
	
	col_title_or_content_item = re.sub('(\s*:\s*)',':',col_title_or_content_item)
	
	col_title_or_content_item = re.sub('(\[\s*)','[',col_title_or_content_item) #06/02/2015:updated
	
	col_title_or_content_item = re.sub('(Value\s*\[)','Value [',col_title_or_content_item) #06/02/2015:updated
	col_title_or_content_item = re.sub('(Characteristics\s*\[)','Characteristics [',col_title_or_content_item) #06/02/2015:updated
	col_title_or_content_item = re.sub('(Comment\s*\[)','Comment [',col_title_or_content_item) #06/02/2015:updated
	
	col_title_or_content_item = col_title_or_content_item.strip()
	
	return col_title_or_content_item


def fixContents_step1(input_file,file_type):
	
	#################
	assert re.search('(\.txt$)',input_file)
	intermediate_1 = re.sub('(\.txt$)','_1.txt',input_file)
	#################
	
	f_in = open(input_file)
	try:
		data = f_in.read()
	finally:
		f_in.close()
		del f_in
	
	tmp_dict = {}
	tmp_dict.update(fileType2literalFileContents2Replace['all'])
	tmp_dict.update(fileType2literalFileContents2Replace[file_type])
	
	for src,target in tmp_dict.iteritems():
		data = data.replace(src,target)
	del src,target,tmp_dict
	
	data = re.sub('(\r\n)','\n',data)
	
	f_out = open(intermediate_1,'wb')
	try:
		f_out.write(data)
	finally:
		f_out.close()
		del f_out
	del data
	
	return intermediate_1

def getRows(tab_delimited_text_file):
	##################
	#Since some text files created directly from Excel-based ISA-TAB-Nano files can contain line endings in the middle of (quoted) column titles/data row cells, extracting the column titles/data rows needs to make use of the csv module.
	##################
	
	f_in = open(tab_delimited_text_file)
	try:
		try:
			reader = csv.reader(f_in,delimiter='\t',quotechar='"')
			rows = [ROW for ROW in reader] #first ROW is a list of column titles, including internal line endings if applicable
		finally:
			del reader
	finally:
		f_in.close()
		del f_in
	
	return rows

def rowHasBlankFirstEntry(row):
	#No valid Investigation, Study, Assay, Material file has a blank entry in the first column
	#This enables blank rows to be deleted
	##############
	assert type([]) == type(row)
	##############
	if "" == row[0]:
		return True
	else:
		return False

def fixContents_step2(intermediate_1,out_name,file_type,shouldMakeNanoPUZZLESspecificChanges):
	
	f_out = open(out_name,'wb')
	try:
		row_count = 0
		for row in getRows(intermediate_1):
			row_count += 1
			#================
			if rowHasBlankFirstEntry(row):
				assert not 1 == row_count, "Blank column title in %s (file type:%s)!" % (out_name,file_type)
				continue
			#================
			#================
			if 1 == row_count and not 'Investigation'==file_type:
				print checkDuplicatedColumnTitlesAreNotSuspicious(column_titles=row)
			#================
			f_out.write('\t'.join([modifyColTitleOrContentItem(part,current_file_type=file_type,includingNanoPUZZLESspecificChanges=shouldMakeNanoPUZZLESspecificChanges) for part in row])+'\n')
	finally:
		f_out.close()
		del f_out


def extractAccessionCode(text_with_at_most_one_accession_code):
	
	if almost_ac_regex.search(text_with_at_most_one_accession_code):
		
		############
		#Debug:
		############
		#print "DEBUGGING:text_with_at_most_one_accession_code=%s;almost_ac_regex.split(text_with_at_most_one_accession_code)=" % text_with_at_most_one_accession_code,almost_ac_regex.split(text_with_at_most_one_accession_code)
		############
		
		
		almost_ac_candidates = [p for p in almost_ac_regex.split(text_with_at_most_one_accession_code) if not p is None and almost_ac_regex.match(p)]
		del p
		assert 1 == len(almost_ac_candidates),"text_with_at_most_one_accession_code=%s;almost_ac_candidates=%s" % (text_with_at_most_one_accession_code,str(almost_ac_candidates))
		
		return almost_ac_candidates[0].split('}')[0]
	else:
		return None

def editAccessionCodesForOneSingleCellEntry(the_entry):
	
	
	all_accession_codes = []
	
	for text_with_at_most_one_accession_code in the_entry.split(";"):
		all_accession_codes.append(extractAccessionCode(text_with_at_most_one_accession_code))
	
	
	
	for accession_code in all_accession_codes:
		if not accession_code is None:
			edited = accession_code.split('/')[-1]
			edited = edited.split('#')[-1]
			
			the_entry = the_entry.replace(accession_code,edited)
		else:
			pass
	
	return the_entry

def findAndEditAccessionCodesForOneSingleCellEntry(the_entry,the_file_type,the_col_title,the_row_title):
	
	potentialAccessionCodes = False
	
	if 'Investigation' == the_file_type:
		if re.search('(Term Accession Number)',the_row_title) and not '' == the_entry:
			potentialAccessionCodes = True
	else:
		if re.search('(Characteristic|Term Accession Number)',the_col_title) and not '' == the_entry:
			potentialAccessionCodes = True
	
	if potentialAccessionCodes:
		return editAccessionCodesForOneSingleCellEntry(the_entry)
	else:
		return the_entry


def editAccessionCodes(out_name,file_type):
	original_rows =  getRows(out_name)
	
	f_out = open(out_name,'wb')
	try:
		for row in original_rows:
			f_out.write('\t'.join([findAndEditAccessionCodesForOneSingleCellEntry(the_entry=row[part_index],the_file_type=file_type,the_col_title=original_rows[0][part_index],the_row_title=row[0]) for part_index in range(0,len(row))])+'\n')
	finally:
		f_out.close()
		del f_out

def removeComments(out_name,file_type):
	original_rows = getRows(out_name)
	
	f_out = open(out_name,'wb')
	try:
		for row in original_rows:
			if 'Investigation' == file_type:
				if re.match('(Comment)',row[0]):
					continue
				else:
					new_row = row[:]
			else:
				new_row = [row[part_index] for part_index in range(0,len(row)) if not re.match('(Comment)',original_rows[0][part_index])]
			
			f_out.write('\t'.join(new_row)+'\n')
			
	finally:
		f_out.close()
		del f_out

def fixContents(input_file,out_name=None,del_intermediates=True,file_type='Assay',shouldEditAccessionCodes=False,shouldRemoveComments=False,shouldMakeNanoPUZZLESspecificChanges=False):
	
	print '-'*50
	print 'Applying fixContents(...) to:',input_file
	print 'Current file type:',file_type
	print 'shouldEditAccessionCodes=%s' % str(shouldEditAccessionCodes)
	print 'shouldRemoveComments=%s' % str(shouldRemoveComments)
	print 'shouldMakeNanoPUZZLESspecificChanges=%s' % str(shouldMakeNanoPUZZLESspecificChanges)
	print '-'*50
	
	#################
	if out_name is None:
		out_name = input_file
	##################
	
	all_intermediates = []
	
	intermediate_1 = fixContents_step1(input_file,file_type)
	
	all_intermediates.append(intermediate_1)
		
	fixContents_step2(intermediate_1,out_name,file_type,shouldMakeNanoPUZZLESspecificChanges)
	
		
	if del_intermediates: #DEBUG:commented
		for intermediate in all_intermediates:
			os.remove(intermediate)
	
	if shouldEditAccessionCodes:
		editAccessionCodes(out_name,file_type)
	
	if shouldRemoveComments:
		if 'Investigation' == file_type:
			removeComments(out_name,file_type)

def main():
	import getopt
	
	opts,args = getopt.getopt(sys.argv[1:],'i:',['input='])
	
	for o,v in opts:
		if '-i' == o:
			input = re.sub('"','',v)
	
	print 'Converting: ', input
	
	fixContents(input_file=input,out_name='output.txt')
	
	return 0

if __name__ == '__main__':
	sys.exit(main())
