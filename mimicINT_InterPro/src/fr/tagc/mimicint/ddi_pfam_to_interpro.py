#!/usr/bin/python3
# -*- coding: utf-8 -*-

import datetime


from fr.tagc.mimicint.util.option.OptionManager import *


# This script allows to convert the Pfam accessions used in
# the parsed 3did file into matching InterPro accessions.



# Description of the input files
# ------------------------------

# The 3did parsed file is expected to be a tsv formated file
# containing the following columns:
# - Pfam_acc_1: String - The Pfam accession of the first domain.
# - Pfam_acc_2: String - The Pfam accession of the second domain.
# - Pfam_label_1: String - The Pfam name of the first domain.
# - Pfam_label_2: String - The Pfam name of the second domain.
# NB: This file contains a header.

# The cross-references file is expected to be a tsv formated file 
# containing the following columns:
# - Pfam_accession: String - The Pfam accession.
# - name: String - The name of the Pfam entry.
# - type: String - The type of entry.
# - InterPro_accession: String - The InterPro accession corresponding to the Pfam entry.
# NB: This file contains a header.


# Description of the output file
# ------------------------------

# The output file is a tsv file that contains the following columns:
# - InterPro_acc_1: String - The InterPro accession of the first domain.
# - InterPro_acc_2: String - The InterPro accession of the second domain.
# - InterPro_name_1: String - The name of the first domain (in Pfam).
# - InterPro_name_2: String - The name of the second domain (in Pfam).
# NB: This file contains a header.


# ===========================================
# Constants
# ===========================================

# Constants
# ---------

# Indexes of columns in the cross-references file
CROSSREF_FILE_COL_INDEX_PFAM_ACC = 0
CROSSREF_FILE_COL_INDEX_NAME = 1
CROSSREF_FILE_COL_INDEX_TYPE = 2
CROSSREF_FILE_COL_INDEX_INTERPRO_ACC = 3

# Keys used in the dictionary that register the cross-references
CROSSREF_DICT_NAME_KEY = 'name'
CROSSREF_DICT_TYPE_KEY = 'type' 
CROSSREF_DICT_INTERPRO_KEY = 'InterPro'

# Index of columns in the 3did parsed file
DDI_PFAM_COL_INDEX_PFAM_ACC_1 = 0
DDI_PFAM_COL_INDEX_PFAM_ACC_2 = 1


# List of options allowed
# -----------------------
# Path to the 3did parsed file (contains the parsed pairs of 
# interacting domains, i.e domain-domain interaction templates
# as Pfam accessions)
DDI_PFAM_FILE_PATH_OPTION = 'DDI_PFAM_FILE_PATH'
# Path to the file containing the cross-references
CROSSREFERENCES_FILE_PATH_OPTION = 'CROSSREFERENCES_FILE_PATH'
# Path to the file containing the interacting domains as InterPro
# accessions (contains the pairs of interacting domains as InterPro
# accessions instead of Pfam)
DDI_INTERPRO_FILE_PATH_OPTION = 'DDI_INTERPRO_FILE_PATH'


OPTION_LIST = [ [ '-p', '--ddiTemplatePfam', 'store', 'string', DDI_PFAM_FILE_PATH_OPTION, None, 
                  'The path to the 3did parsed file (contains the parsed pairs of interacting domains, i.e domain-domain interaction templates as Pfam accessions).' ],
                [ '-c', '--crossreferences', 'store', 'string', CROSSREFERENCES_FILE_PATH_OPTION, None,
                  'The path to the file containing the cross-references (Pfam - InterPro).' ],
                [ '-i', '--ddiTemplateInterPro', 'store', 'string', DDI_INTERPRO_FILE_PATH_OPTION, None, 
                  'The path to the file containing the interacting domains as InterPro accessions (contains the pairs of interacting domains as InterPro accessions instead of Pfam).' ] ]



# ===========================================
# Script
# ===========================================

def ddi_pfam_to_interpro( ddi_pfam_file_path, crossreferences_file_path, ddi_interpro_file_path ):
    
    '''
    This method allows to generate a file containing the pairs of interacting domains
    using InterPro accessions instead of Pfam accessions provided by the 3did resource.
    
    @param ddi_pfam_file_path: String - The path to the 3did parsed file (contains the parsed 
                                        pairs of interacting domains, i.e domain-domain interaction 
                                        templates as Pfam accessions).
    @param crossreferences_file_path: String - The path to the file containing the cross-references 
                                               (Pfam - InterPro).
    @param ddi_interpro_file_path: String - The path to the file containing the interacting domains 
                                            as InterPro accessions (contains the pairs of interacting
                                            domains as InterPro accessions instead of Pfam).
    '''
    
    # Import the cross-references
    # ---------------------------
    
    # Instantiate a dictionary that will associate to each Pfam accession
    # a dictionary containing its name, the type and the InterPro accession
    # in which it has been integrated
    crossreferences_dict = {}
    
    with open( crossreferences_file_path, 'r' ) as crossreferences_file:
        
        line = crossreferences_file.readline()
        
        while ( line != '' ):
            
            # Parse the line
            line = line.replace( '\n', '' )
            line = line.split( '\t' )
            pfam_acc = line[ CROSSREF_FILE_COL_INDEX_PFAM_ACC ]
            pfam_name = line[ CROSSREF_FILE_COL_INDEX_NAME ]
            pfam_type = line[ CROSSREF_FILE_COL_INDEX_TYPE ]
            interpro_acc = line[ CROSSREF_FILE_COL_INDEX_INTERPRO_ACC ]
            
            # Add the entry to the dictionary
            crossreferences_dict[ pfam_acc ] = {
                                                    CROSSREF_DICT_NAME_KEY : pfam_name,
                                                    CROSSREF_DICT_TYPE_KEY : pfam_type,
                                                    CROSSREF_DICT_INTERPRO_KEY : interpro_acc }
            
            line = crossreferences_file.readline()
    
    
    
    # Convert the pairs of interacting domains
    # ----------------------------------------
    
    with open( ddi_pfam_file_path, 'r' ) as ddi_pfam_file, \
         open( ddi_interpro_file_path, 'w' ) as ddi_interpro_file:
        
        # Write the header in the output file
        header = [ 'InterPro_acc_1',
                   'InterPro_acc_2',
                   'InterPro_name_1',
                   'InterPro_name_2' ]
        ddi_interpro_file.write( '\t'.join( header ) + '\n' )
        
        line = ddi_pfam_file.readline()
        
        while ( line != '' ):
            
            # Parse the line and get the interacting domains
            line = line.replace( '\n', '' )
            line = line.split( '\t' )
            pfam_acc_1 = line[ DDI_PFAM_COL_INDEX_PFAM_ACC_1 ]
            pfam_acc_2 = line[ DDI_PFAM_COL_INDEX_PFAM_ACC_2 ]
            
            # Get the InterPro entries corresponding to these Pfam
            interpro_entry_1 = crossreferences_dict.get( pfam_acc_1 )
            interpro_entry_2 = crossreferences_dict.get( pfam_acc_2 )
            
            # If both Pfam accessions have InterPro entries matching,
            # then report the interaction in the output file
            if ( interpro_entry_1 and interpro_entry_2 ):
                
                interpro_acc_1 = interpro_entry_1[ CROSSREF_DICT_INTERPRO_KEY ]
                pfam_name_1 = interpro_entry_1[ CROSSREF_DICT_NAME_KEY ]
                
                interpro_acc_2 = interpro_entry_2[ CROSSREF_DICT_INTERPRO_KEY ]
                pfam_name_2 = interpro_entry_2[ CROSSREF_DICT_NAME_KEY ]
                
                interaction_pair = [ interpro_acc_1,
                                     interpro_acc_2,
                                     pfam_name_1,
                                     pfam_name_2 ]
                ddi_interpro_file.write( '\t'.join( interaction_pair ) + '\n' )
            
            # Otherwise, if one of the Pfam accession has no InterPro 
            # entry matching, then log a message and skip this interaction
            else:
                message_to_print = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S') + ' :: WARNING :: '
                
                if ( ( not interpro_entry_1 ) and ( not interpro_entry_2 ) ):
                    message_to_print = ( message_to_print + 
                                         'The Pfam entries ' + pfam_acc_1 + ' and ' + pfam_acc_2 + 
                                         ' have no InterPro entries matching.' )
                else:
                    if ( not interpro_entry_1 ):
                        message_to_print = ( message_to_print + 
                                             'The Pfam entry ' + pfam_acc_1 + ' has no InterPro entry matching.' )
                    if ( not interpro_entry_2 ):
                        message_to_print = ( message_to_print + 
                                             'The Pfam entry ' + pfam_acc_2 + ' has no InterPro entry matching.' )
                        
                print( message_to_print )
                
            # Read next line
            line = ddi_pfam_file.readline()



# ===========================================
# Parse command line arguments 
# and run script
# ===========================================

if ( __name__ == '__main__' ):
    
    # Parse the command-line arguments
    option_dict = parse_arguments( OPTION_LIST )
    
    # Get the path to the 3did parsed file
    ddi_pfam_file_path = get_option( option_dict = option_dict,
                                     option_name = DDI_PFAM_FILE_PATH_OPTION,
                                     not_none = True )
    
    # Get the path to the file containing the cross-references
    crossreferences_file_path = get_option( option_dict = option_dict,
                                            option_name = CROSSREFERENCES_FILE_PATH_OPTION,
                                            not_none = True )
    
    # Get the path to the output file containing the interacting
    # domains as InterPro accessions 
    ddi_interpro_file_path = get_option( option_dict = option_dict,
                                         option_name = DDI_INTERPRO_FILE_PATH_OPTION,
                                         not_none = True )
    
    # Run the script
    print( datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S') + 
           ' :: INFO :: Starting the conversion of Pfam accessions into InterPro accessions in' +
           ' the domain-domain interactions template file.' )
    try:
        ddi_pfam_to_interpro( ddi_pfam_file_path = ddi_pfam_file_path, 
                              crossreferences_file_path = crossreferences_file_path, 
                              ddi_interpro_file_path = ddi_interpro_file_path )
    except Exception as e:
        exit( 'An exception has been raised during the execution of the script: \n' +
              str( e ) )
    else:
        print( datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S') + 
               ' :: INFO :: The conversion of Pfam accessions into InterPro accessions in' +
               ' the domain-domain interactions template file has finished.' )
    