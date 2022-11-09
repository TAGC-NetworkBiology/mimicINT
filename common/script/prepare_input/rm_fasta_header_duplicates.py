#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
from optparse import OptionParser

# This is a script allowing to ensure there are no duplicates 
# in the headers of a fasta file. It generates a new fasta 
# containing unique IDs if the same ID is found several times.
# NB: SLiMProb uses the AC as an "primary key". Hence, if the 
#     same AC is found associated with several sequences, the
#     detection of SLiMs will raises errors and only the last
#     sequence scanned will be registered.

# Format of the expected header:
# >sp|P0C6U8|NSP1_CVHSA

def rm_fasta_header_dup( input_fasta, output_fasta ):
    '''
    @param input_fasta: String - The path to the fasta file where duplicate 
                                 headers have to been searched for.
    @param output_fasta: String - The path to the fasta file where duplicate
                                  headers have been removed.
    '''
    
    # Constants
    FASTA_HEADER_SEP = '|'
    
    # Create the output folder if it does not yet exist 
    # (and its parent folders if necessary)
    output_folder = os.path.dirname( output_fasta )
    if not os.path.isdir( output_folder ):
        os.makedirs( output_folder )
    
    with open( input_fasta, 'r' ) as input_fasta_file, open( output_fasta, 'w' ) as output_fasta_file:
        
        line = None
        previous_AC = None
        while line != '':
            # Get a new line from the input file
            line = input_fasta_file.readline()
                        
            # If this line is a header
            if line.startswith( '>' ):
                # The header is expected to be at the following format:
                # >sp|P0C6U8|NSP1_CVHSA
                
                print( 'DEBUG :: Treating header ' + line[ :-2 ] )
                
                # Get the AC ID
                new_line = line.split( FASTA_HEADER_SEP )
                
                # Any AC is rename by using the AC and adding an unique 
                # integer at its end
                if ( new_line[ 1 ] != previous_AC ):
                    ac_duplicate_count = 1
                    previous_AC = new_line[ 1 ]
                else:
                    ac_duplicate_count += 1
                
                new_line[ 1 ] = new_line[ 1 ] + '-' + str( ac_duplicate_count )
                
                # Recreate a string to be used as header and 
                # write it in the output file
                new_line = FASTA_HEADER_SEP.join( new_line )
                
                output_fasta_file.write( new_line )
                
            # Otherwise, copy it in the output file as is
            else:
                output_fasta_file.write( line )
                
                
if __name__ == '__main__':
    
    # Parse arguments
    INPUT_FASTA_OPT = 'INPUT_FASTA'
    OUTPUT_FASTA_OPT = 'OUTPUT_FASTA'
    OPTION_LIST = [ [ '-i', '--input', 'store', 'string', INPUT_FASTA_OPT, None, 'The path of the input fasta file.' ],
                    [ '-o', '--output', 'store', 'string', OUTPUT_FASTA_OPT, None, 'The path of the output fasta file.' ] ]
    
    optionParser = OptionParser()    
    for current_opt in OPTION_LIST:
        optionParser.add_option( current_opt[ 0 ],
                                 current_opt[ 1 ],
                                 action = current_opt[ 2 ],
                                 type = current_opt[ 3 ],
                                 dest = current_opt[ 4 ],
                                 default = current_opt[ 5 ],
                                 help = current_opt[ 6 ] )
    
    # Get the various option values into a dictionary
    ( opts, args ) = optionParser.parse_args()
    option_dict = vars( opts )
    
    # Run the script
    rm_fasta_header_dup( input_fasta = option_dict[ INPUT_FASTA_OPT ],
                         output_fasta = option_dict[ OUTPUT_FASTA_OPT ] )
        