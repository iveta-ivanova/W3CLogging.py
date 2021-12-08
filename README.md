# LogAnalysis

This documentation is for a console app which analyses log files. Currently it accepts .log files of W3C format and outputs a list of unique client-server URI targets (URI stem) ranked by the number of "hits" each has received. The basic assumptions regarding the format are outlined below.

**Pre-requisites** 

The program was tested in python 3.8.

No additional libraries are required to run the program.

Once unpacked, the path to the project folder should be added to the environmental variable `PYTHONPATH`. 

Running tests requires the installation of pytest: 

`pip install pytest
`

**Arguments**: 

Currently two parameters are required: the file paths and the URI field name. 

1) The first argument or set of arguments is the relative paths to the .log files wished to be analysed. These can either be a directory or subdirectory (relative to the current project directory), in which case all .log files in the given directory are processed, or a direct path to a .log file itself. The number of arguments that can be passed for this parameter is uncapped. The individual log entries are accumulated and statistics is performed. 


2) The second argument is passed to the keyword parameter "url_field" and corresponds to the column name of the client-server URI target. For most Microsoft logs this is typically "cs-uri-stem".

Example arguments for a file named _loganalysis.py_: 
   
`loganalysis.py logfile.log folder folder/subfolder/logfile2.log --url_field cs-uri-stem`

**Assumptions**

1) The log files must have a .log extension - paths to any other files will be ignored, including those in the selected directories.
   

2) Each file's metadata must contain a "#Fields" line containing the column names - otherwise the URI can not be identified and an empty list will be returned. 


3) Any log entries occurring prior to the first Fields metadata will be ignored.  