#####################
#README.txt:Contents#
#####################
#1. Overview of this project.
#2. IMPORTANT LEGAL ISSUES
#<N.B.: Check this section ("IMPORTANT LEGAL ISSUES") to see whether - and how - you ARE ALLOWED TO use this code!>
#<N.B.: Includes contact details.>
#3. Getting started
#<N.B.: Check this section ("Getting started") to see whether you CAN use this code!>
#4. Using the code

#################################



##############################
#1. Overview of this project.#
##############################
#Project name: xls2txtISA.NANO.archive
#To convert a compressed, *flat* archive ("yyyy.zip") populated with ISA-TAB-Nano based ".xls" files, to a corresponding compressed, *flat* archive ("yyyy-txt.zip") of ISA-TAB-Nano based tab delimited text (".txt") files. 
#N.B. ISA-TAB-Nano is described here:https://wiki.nci.nih.gov/display/ICR/ISA-TAB-Nano
#DISCLAIMER: No endorsements from the original ISA-TAB-Nano developers or any other third party organisations should be inferred.

##################################
The research leading to development of this program has received funding from the European Union Seventh Framework Programme (FP7/2007-2013) under grant agreement n° 309837 (NanoPUZZLES project).

http://www.nanopuzzles.eu/
##################################

###########################
#2. IMPORTANT LEGAL ISSUES#
###########################
This file was adapted from README.txt obtained from version 0.1 of the following project:http://code.google.com/p/generic-qsar-py-utils/
Some source code files, where indicated, were also adapted from this project.
Copyright (c) 2013 Syngenta
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

####################
#3. Getting started#
####################

###############
#Prerequisites#
###############
0. To date, this code has only been tested on a machine running Windows 7. Some modifications may be required to enable it to be used on a machine running a unix-type operating system - e.g. file name manipulation and specification of path names.
1. Python interpreter. http://python.org/ Python version >= 2.5 (at least) is required. Python version 2.7.3 is recommended since all code development employed this version of Python.
2. xlrd,xlwt packages from http://www.python-excel.org/ [versions 0.9.3 and 0.7.5 of xlrd and xlwt were used respectively for development]
3. unicodecsv packages from https://pypi.python.org/pypi/unicodecsv [version 0.9.4 was used for development]

########################
#Installation guidance##
########################
The following describes a workflow one might employ to install all necessary pre-requisites to run this software on a machine running Windows 7.

1.1 Download python-2.7.3.msi [https://www.python.org/download/releases/2.7.3/]
1.2 Run the installer (right click -> "Install")
1.3 Add "C:\Python27" to your PATH variable ["Control Panel" -> "System" -> "Advanced System Settings" -> "Environment Variables..."]

N.B. For the following steps, you may need to launch a new command prompt session in between each step

2.1 Download xlrd-0.9.3.tar.gz, xlwt-0.7.5.tar.gz [from the links provided at http://www.python-excel.org/]
2.2 Extract each tar.gz -> tar -> directories via, say, the "7-Zip" program [http://www.7-zip.org/]
2.3 For both modules, enter the setup.py directory and run “python setup.py install” from the command prompt

3.1 https://pypi.python.org/pypi/setuptools
3.2 Download ez_setup.py
3.3 enter "python ez_setup.py" from the command prompt

4.1 https://pypi.python.org/pypi/unicodecsv/0.9.4
4.2 Download unicodecsv-0.9.4.tar.gz
4.3 Extract via, say, "7-Zip" program [http://www.7-zip.org/]
4.4 enter the setup.py directory and run “python setup.py install” from the command prompt

####################
#4. Using the code #
####################

Navigate to the "xls2txtISA.NANO.archive" directory, i.e. the one in which this README.txt file should be located, via the command prompt.

Type "python xls2txtISA.NANO.archive.py" at the command prompt for further documentation.



 