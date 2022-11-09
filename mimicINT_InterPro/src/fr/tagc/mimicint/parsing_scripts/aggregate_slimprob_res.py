#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import datetime


from fr.tagc.mimicint.util.option.OptionManager import *

# This script allows to aggregare several SLiMProb 
# result files into one single file.


# ===========================================
# Constants
# ===========================================

# List of options allowed
# -----------------------

# List of paths to the input result files
INPUT_RESULT_FILES_LIST_OPTION = 'INPUT_RESULT_FILES_LIST'

# Path to the output result file
OUTPUT_RESULT_FILE_OPTION = 'OUTPUT_RESULT_FILE'

OPTION_LIST = [ [ '-i', '--input', 'store', 'string', INPUT_RESULT_FILES_LIST_OPTION, None, 'The list of paths to the input result files.' ],
                [ '-o', '--output', 'store', 'string', OUTPUT_RESULT_FILE_OPTION, None, 'The path to the output result file.' ] ]



# ===========================================
# Script
# ===========================================

# aggregate_slimprob_res
# ----------------------
#
# This function allows to aggregate several SLiMProb 
# result files into one single file.
#
# @param input_res_files_list: List - The list of paths to the input result files.
# @param output_res_file: String - The path to the output result file.
#
def aggregate_slimprob_res( input_res_files_list, output_res_file ):

    print( 'INFO :: results from ' + str( len( input_res_files_list ) ) + 
           ' SLiMProb result files will be aggregated together.' )
    
    with open( output_res_file, 'w' ) as output_res:
        # Write the header from the first file
        with open( input_res_files_list[ 0 ], 'r' ) as input_res:
            line = input_res.readline()
            output_res.write( line )      
            
        # For all files, copy all lines except the first one
        for input_res_file in input_res_files_list:
            with open( input_res_file, 'r' ) as input_res:
                # Skip header
                line = input_res.readline()
                line = input_res.readline()
                while ( line != '' ):
                    output_res.write( line )
                    line = input_res.readline()
            


# ===========================================
# Parse command line arguments 
# and run script
# ===========================================

#### Code execution in the console ####
if __name__ == '__main__':
    
    # Parse the command-line arguments
    option_dict = parse_arguments( OPTION_LIST )
    
    # Get the list of paths to the input result files
    input_res_files_list = get_option( option_dict = option_dict,
                                       option_name = INPUT_RESULT_FILES_LIST_OPTION, 
                                       not_none = True )
    try:
        input_res_files_list = input_res_files_list.split( ',' )
    except:
        raise Exception( 'An error occurred during the conversion of paths of' +
                         ' the input result files into a list.' )
    
    # Get the path to the output result file
    output_res_file = get_option( option_dict = option_dict,
                                  option_name = OUTPUT_RESULT_FILE_OPTION, 
                                  not_none = True )
    
    print( datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S') +
           ':: INFO :: Starting the aggregation of SLiMProb result files.' )
    
    # Run the script    
    aggregate_slimprob_res( input_res_files_list = input_res_files_list, 
                            output_res_file = output_res_file )
    
    print( datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S') +
           ':: INFO :: The aggregation of SLiMProb result files has finished.' )
    