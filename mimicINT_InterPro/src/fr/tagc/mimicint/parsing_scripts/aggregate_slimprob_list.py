#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import datetime


from fr.tagc.mimicint.util.option.OptionManager import *

# This script allows to aggregare several SLiMProb 
# occurrence files into one single file.


# ===========================================
# Constants
# ===========================================

# List of options allowed
# -----------------------

# List of paths to the input occurrence files
INPUT_OCC_FILES_LIST_OPTION = 'INPUT_OCC_FILES_LIST'

# Path to the output occurrence file
OUTPUT_OCC_FILE_OPTION = 'OUTPUT_OCC_FILE'

OPTION_LIST = [ [ '-i', '--input', 'store', 'string', INPUT_OCC_FILES_LIST_OPTION, None, 'The list of paths to the input occurrence files.' ],
                [ '-o', '--output', 'store', 'string', OUTPUT_OCC_FILE_OPTION, None, 'The path to the output occurrence file.' ] ]



# ===========================================
# Script
# ===========================================

# aggregate_slimprob_list
# -----------------------
#
# This function allows to aggregate several SLiMProb 
# occurrence files into one single file.
#
# @param input_occ_files_list: List - The list of paths to the input occurrence files.
# @param output_occ_file: String - The path to the output occurrence file.
#
def aggregate_slimprob_list( input_occ_files_list, output_occ_file ):

    print( 'INFO :: results from ' + str( len( input_occ_files_list ) ) + 
           ' SLiMProb occurrence files will be aggregated together.' )
    
    with open( output_occ_file, 'w' ) as output_occ:
        # Write the header from the first file
        with open( input_occ_files_list[ 0 ], 'r' ) as input_occ:
            line = input_occ.readline()
            output_occ.write( line )
            
        # For all files, copy all lines except the first one
        for input_occ_file in input_occ_files_list:
            with open( input_occ_file, 'r' ) as input_occ:
                # Skip header
                line = input_occ.readline()
                line = input_occ.readline()
                while ( line != '' ):
                    output_occ.write( line )
                    line = input_occ.readline()
            


# ===========================================
# Parse command line arguments 
# and run script
# ===========================================

#### Code execution in the console ####
if __name__ == '__main__':
    
    # Parse the command-line arguments
    option_dict = parse_arguments( OPTION_LIST )
    
    # Get the list of paths to the input occurrence files
    input_occ_files_list = get_option( option_dict = option_dict,
                                       option_name = INPUT_OCC_FILES_LIST_OPTION, 
                                       not_none = True )
    try:
        input_occ_files_list = input_occ_files_list.split( ',' )
    except:
        raise Exception( 'An error occurred during the conversion of paths of' +
                         ' the input occurrence files into a list.' )
    
    # Get the path to the output occurrence file
    output_occ_file = get_option( option_dict = option_dict,
                                  option_name = OUTPUT_OCC_FILE_OPTION, 
                                  not_none = True )
    
    print( datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S') +
           ':: INFO :: Starting the aggregation of SLiMProb occurrence files.' )
    
    # Run the script    
    aggregate_slimprob_list( input_occ_files_list = input_occ_files_list, 
                             output_occ_file = output_occ_file )
    
    print( datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S') +
           ':: INFO :: The aggregation of SLiMProb occurrence files has finished.' )
    