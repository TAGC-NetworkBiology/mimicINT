#!/usr/bin/python3
# -*- coding: utf-8 -*-

########## Parser for the InterProScan results file ##########

#### Import modules ####
from fr.tagc.mimicint.util.option.OptionManager import *


# ===========================================
# Constants
# ===========================================

# List of options allowed
# -----------------------
# Path to the file with InterProScan results
IPS_RES_FILE_OPTION = "IPS_RES_FILE"
# Path to the results file + its name
PARSED_FILE_OPTION = "PARSED_FILE"
# Maximum e-value for the occurrence to be kept
SCORE_THRESHOLD_OPTION = "SCORE_THRESHOLD"

OPTION_LIST = [ [ "-i", "--ipsRes", "store", "string", IPS_RES_FILE_OPTION, None, "The path to the file with InterProScan results." ],
                [ "-o", "--output", "store", "string", PARSED_FILE_OPTION, None, "The path to the results file + its name." ],
                [ "-s", "--scoreThreshold", "store", "string", SCORE_THRESHOLD_OPTION, None, "The maximum e-value for the occurrence to be kept." ] ]



# ===========================================
# Script
# ===========================================

#### Parser definition ####
def parse_interproscan(ips_res, parsed_file, score_threshold=0.00001) :
	
	'''
	ips_res : file with InterProScan results
	
	parsed_file : path to the results file + its name
	
	score_threshold: maximum e-value for the occurrence to be kept
	
	This parser allows to collect the useful columns in the InterProScan
	results file :
	Protein_Accession, Analysis, Signature_Accession, Signature_Description, Start_location, Stop_location, Score et Interpro_Annotation
	and to add names for these columns (which is not already done by InterProScan)
	'''
	
	#### Opening files ####
	fileResIps = open(ips_res,"r") #  file with InterProScan results
	fileResParser = open(parsed_file,"w") # results file
	
	#### Writing the columns names in the results file ####
	print("Protein_Accession" + "\t" + "Analysis" + "\t" + "Signature_Accession" + "\t" + "Signature_Description" + "\t" + "Start_location" + "\t" + "Stop_location" + "\t" + "Score" + "\t" + "Interpro_Annotation",file=fileResParser)
	
	#### Reading the InterProScan results file ####
	line = None
	while line != '' :
		line = fileResIps.readline() # reading file while there is not an empty line
		if line != '' :
			line = line.split("\t")
			# The column Interpro_Annotation is optional
			# so, writing in the results file depends on its presence or absence
			# to avoid any error message
			
			if ( float(line[8]) < float( score_threshold ) ):
				if len(line)>11 :
					print(line[0] + "\t" + line[3] + "\t" + line[4] + "\t" + line[5] + "\t" + line[6] + "\t" + line[7] + "\t" + line[8] + "\t" + line[11],file=fileResParser)
				else :
					print(line[0] + "\t" + line[3] + "\t" + line[4] + "\t" + line[5] + "\t" + line[6] + "\t" + line[7] + "\t" + line[8] + "\t",file=fileResParser)				
	
	#### Closing the files ####
	fileResIps.close()
	fileResParser.close()



# ===========================================
# Parse command line arguments 
# and run script
# ===========================================

#### Code execution in the console ####
if __name__ == "__main__":
    
    # Parse the command-line arguments
    option_dict = parse_arguments( OPTION_LIST )
    
    # Get the path to the file with InterProScan results
    ips_res = get_option( option_dict = option_dict, 
						  option_name = IPS_RES_FILE_OPTION, 
                          not_none = True )
    
    # Get the path to the results file + its name
    parsed_file = get_option( option_dict = option_dict, 
							  option_name = PARSED_FILE_OPTION, 
							  not_none = True )
    
    # Get the maximum e-value for the occurrence to be kept
    score_threshold = get_option( option_dict = option_dict,
								  option_name = SCORE_THRESHOLD_OPTION,
								  not_none = True )
    try:
    	score_threshold = float( score_threshold )
    except:
        raise Exception( 'The e-value cut-off provided has to be an float.' )
    else:
        if ( ( score_threshold < 0 )
             or ( score_threshold > 1 ) ):
            raise Exception( 'The e-value cut-off provided has to be an float between 0 and 1.' )
    
    # Run the script
    parse_interproscan( ips_res = ips_res,
					    parsed_file = parsed_file,
					    score_threshold = score_threshold )
