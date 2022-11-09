#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os


from fr.tagc.mimicint.util.option.OptionManager import *

# This script allows to parse a fasta file into
# several smaller files


# ===========================================
# Constants
# ===========================================

# Default maxmimum number of sequences per file
DEFAULT_MAX_SEQ_PER_FILE = 5000


# List of options allowed
# -----------------------

# Path to the input fasta file
INPUT_FASTA_FILE_OPTION = 'INPUT_FASTA_FILE'

# Path to the output directory
OUTPUT_FASTA_DIRECTORY_OPTION = 'OUTPUT_FASTA_DIRECTORY'

# Maxmimum number of sequences per file
MAX_SEQ_PER_FILE_OPTION = 'MAX_SEQ_PER_FILE'

OPTION_LIST = [ [ '-i', '--input', 'store', 'string', INPUT_FASTA_FILE_OPTION, None, 'The path to the fasta file to split.' ],
                [ '-o', '--outputDir', 'store', 'string', OUTPUT_FASTA_DIRECTORY_OPTION, None, 'The path to the output folder where to write the new fasta file.' ],
                [ '-m', '--maxSeqPerFile', 'store', 'string', MAX_SEQ_PER_FILE_OPTION, None, 'The maximum number of sequences that may be stored in a fasta file.' ] ]



# ===========================================
# Script
# ===========================================

# split_fasta_file
# ----------------
#
# This function allows to split a fasta file into several
# smaller fasta file.
#
# @param input_fasta_file: String - The path to the input fasta file.
# @param output_fasta_dir: String - The path to the directory where the new fasta files
#                                   have to be written.
# @param max_seq_per_file: Integer - The maximum number of sequences that can be stored in a file.
#
def split_fasta_file( input_fasta_file, output_fasta_dir, max_seq_per_file ):
    
    # Create the output directory if necessary
    if ( not os.path.isdir( output_fasta_dir ) ):
        os.makedirs( output_fasta_dir )
        
    # Get the name of the fasta file
    fasta_filename = '.'.join( os.path.basename( input_fasta_file ).split('.')[:-1] )
    
    # Split the input file into several fasta files
    with open( input_fasta_file, 'r' ) as input_fasta:
        
        line = input_fasta.readline()
        
        seq_stored = 0
        file_suffix = 0
        total_seq_stored = 0
        
        while ( line != '' ):
            
            # Create a new file if necessary
            if ( seq_stored == 0 ):
                output_file_path = os.path.join( output_fasta_dir, 
                                                 fasta_filename + '_' + str( file_suffix ) + '.fasta' )
                output_file = open( output_file_path, 'w' )
                file_suffix += 1
                
            # Add a new sequence to the file
            seq_stored += 1
            total_seq_stored += 1
                
            output_file.write( line )
            line = input_fasta.readline()
                
            while ( ( line != '' ) 
                    and ( not line.startswith( '>' ) ) ):
                output_file.write( line )
                line = input_fasta.readline()
            
            # If the maximum number of sequence has been stored, 
            # close the file and reset the counter for the next file
            if ( seq_stored == max_seq_per_file ):
                output_file.close()
                seq_stored = 0
                
        # Close the output file if it was left opened
        try:
            output_file.close()
        except:
            None

    print( 'INFO :: ' + str( total_seq_stored ) + ' sequences have been saved in '+ 
           str( file_suffix ) + ' files of the ' + output_fasta_dir + ' directory.' )
            


# ===========================================
# Parse command line arguments 
# and run script
# ===========================================

#### Code execution in the console ####
if __name__ == '__main__':
    
    # Parse the command-line arguments
    option_dict = parse_arguments( OPTION_LIST )
    
    # Get the path to the query fasta file
    input_fasta_file = get_option( option_dict = option_dict,
                                   option_name = INPUT_FASTA_FILE_OPTION, 
                                   not_none = True )
    
    # Get the path to the output directory
    output_fasta_dir = get_option( option_dict = option_dict,
                                   option_name = OUTPUT_FASTA_DIRECTORY_OPTION, 
                                   not_none = True )
    
    # Get the maxmimum number of sequences per file
    max_seq_per_file = get_option( option_dict = option_dict,
                                   option_name = MAX_SEQ_PER_FILE_OPTION, 
                                   not_none = False )
    
    if max_seq_per_file:
        try:
            max_seq_per_file = int( max_seq_per_file )
        except:
            raise Exception( 'The maximum number of sequences per file has to be an integer.' )
        else:
            if ( max_seq_per_file < 1 ):
                raise Exception( 'The maximum number of sequences per file has to be a positive integer.' )
    else:
        max_seq_per_file = DEFAULT_MAX_SEQ_PER_FILE
    
    # Run the script
    split_fasta_file( input_fasta_file = input_fasta_file, 
                      output_fasta_dir = output_fasta_dir, 
                      max_seq_per_file = max_seq_per_file )
    