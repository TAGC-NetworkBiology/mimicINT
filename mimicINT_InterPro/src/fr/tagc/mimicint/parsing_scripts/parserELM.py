#!/usr/bin/python3

########## Parser for ELM files ##########

#### Import modules ####
import sys

from fr.tagc.mimicint.util.option.OptionManager import *


# ===========================================
# Constants
# ===========================================
	
TAG_ELM_DEFINITION = '"ELM'

DEFAULT_PVAL_THRESHOLD = 0.01

# List of options allowed
# -----------------------
# Path to the file with a list of SLiMs
CLASSES_FILE_OPTION = "CLASSES_FILE"
# Path to the file with a list of SLiMs actually found in H. sapiens
INSTANCES_FILE_OPTION = "INSTANCES_FILE"
# Path to the result file
RESULT_FILE_OPTION = "RESULT_FILE"
# Path to the motifs file
MOTIF_FILE_OPTION = "MOTIF_FILE"
# Cut-off to use to filter the ELM classes based 
# on their probability of occurrence
PVALUE_THRESHOLD_OPTION = "PVALUE_THRESHOLD"

OPTION_LIST = [ [ "-c", "--classes", "store", "string", CLASSES_FILE_OPTION, None, "The path to the file with a list of SLiMs." ],
                [ "-i", "--instances", "store", "string", INSTANCES_FILE_OPTION, None, "The path to the file with a list of SLiMs actually found in H. sapiens." ],
                [ "-r", "--results", "store", "string", RESULT_FILE_OPTION, None, "The path to the result file." ],
                [ "-m", "--motifs", "store", "string", MOTIF_FILE_OPTION, None, "The path to the motifs file." ],
                [ "-p", "--pvalThreshold", "store", "string", PVALUE_THRESHOLD_OPTION, None, "The cut-off to use to filter the ELM classes on their probability of occurrence." ] ]



# ===========================================
# Script
# ===========================================

#### Parser definition ####
def parse_elm(classes, instances, results, motifs, pval_threshold=DEFAULT_PVAL_THRESHOLD) :
	
	'''
	classes : file with a list of SLiMs
	
	instances : file with a list of SLiMs actually found in H. sapiens
	
	results and motifs : path to the results files + their names
	
	pval_threshold: Cut-off to use to filter the ELM classes based on their 
	                probability of occurrence (0.01 by default)
	
	With these files, parseELM create a tsv with the SLiMs actually
	found in H. sapiens and whose regex are found in "classes"
	'''
	
	#### Opening files and variables definition ####
	ficClasses = open( classes,"r") # file with a list of SLiMs
	ficPositives = open( instances,"r") # file with a list of SLiMs actually found in H. sapiens
	listELMI = [] # empty list where the ELM identifiers will be stored
	ficResParse = open( results,"w") # results file
	ficResMotifs = open( motifs,"w") # file with motifs (used with SlimSuite)
	
	#### Reading the file with a list of SLiMs actually found in H. sapiens and collection on ELM identifiers #### 
	line = None
	while line != '' :
		line=ficPositives.readline() # reading file while there is not an empty line
		if line.startswith( TAG_ELM_DEFINITION) : # takes in count only lines corresponding of SLiM
			line = line.split( "\t") # line became a list
			if line[2] not in listELMI :
				listELMI.append( line[2]) # if the id doesn't exist, add it to the list
	print( '"ELMIdentifier"' + "\t" + '"Regex"'+ "\t" + '"Description"',file=ficResMotifs) # collection of columns useful for SlimSuite
	
	#### Reading the file with a list of SLiMs and collection of those which match with listELMI ####
	line2 = None
	while line2 != '' :
		line2=ficClasses.readline()
		if line2.startswith( '"Acc') :
			line2 = line2.rstrip( '\n')
			print( line2,file=ficResParse) # writing the column names in the new files names
		if line2.startswith( TAG_ELM_DEFINITION) :
			line2 = line2.rstrip( '\n') # delete the '\n' at the end
			line2 = line2.split( "\t")
	#### Writing the new file ####
			if line2[1] in listELMI and float(line2[5][1:-1])<float(pval_threshold): # remove promiscuous ELM definitions and keep those found among true positive instances 
				print( line2[0] + "\t" + line2[1] + "\t" + line2[2] + "\t" + line2[3]+"\t"+line2[4]+"\t"+line2[5]+"\t"+line2[6]+"\t"+line2[7],file=ficResParse)
				print( line2[1] + "\t" + line2[4] + "\t" + line2[3],file=ficResMotifs)
			
	#### Closing the files ####
	ficClasses.close()
	ficPositives.close()
	ficResParse.close()
	ficResMotifs.close()



# ===========================================
# Parse command line arguments 
# and run script
# ===========================================

#### Code execution in the console ####
if __name__ == "__main__":
    
    # Parse the command-line arguments
    option_dict = parse_arguments( OPTION_LIST )
    
    # Get the path to the file with a list of SLiMs
    classes = get_option( option_dict = option_dict, 
						  option_name = CLASSES_FILE_OPTION, 
                          not_none = True )
    
    # Get the path to the file with a list of SLiMs actually found in H. sapiens
    instances = get_option( option_dict = option_dict,
						    option_name = INSTANCES_FILE_OPTION,
						    not_none = True )
    
    # Get the path to the result file
    results = get_option( option_dict = option_dict,
						  option_name = RESULT_FILE_OPTION,
						  not_none = True )
    
    # Get the path to the motifs file
    motifs = get_option( option_dict = option_dict,
						 option_name = MOTIF_FILE_OPTION,
						 not_none = True )
    
    # Get the cut-off to use to filter the ELM classes on their probability of occurrence
    pval_threshold = get_option( option_dict = option_dict,
						 option_name = PVALUE_THRESHOLD_OPTION,
						 not_none = False )
    if pval_threshold:
	    try:
	    	pval_threshold = float( pval_threshold )
	    except:
	        raise Exception( 'The p-value cut-off provided has to be an float.' )
	    else:
	        if ( ( pval_threshold < 0 )
	             or ( pval_threshold > 1 ) ):
	            raise Exception( 'The p-value cut-off provided has to be an float between 0 and 1.' )
    else:
    	pval_threshold = DEFAULT_PVAL_THRESHOLD
    	
    # Run the script
    parse_elm( classes = classes,
			   instances = instances,
			   results = results,
			   motifs = motifs,
			   pval_threshold = pval_threshold )
	