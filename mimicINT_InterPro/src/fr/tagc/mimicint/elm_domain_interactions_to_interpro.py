#!/usr/bin/python3
# -*- coding: utf-8 -*-

import datetime
import io


from fr.tagc.mimicint.util.option.OptionManager import *


# This script allows to convert the Pfam in the ELM - domain interactions
# file into matching InterPro accessions.



# Description of the input files
# ------------------------------

# The ELM - domain interactions file is expected to be a tsv formated 
# file containing the following columns:
# - "ELM identifier": String - The ELM identifier.
# - "Interaction Domain Id": String - The domain accession (most of the time
#                                     a Pfam accession, but could also be an
#                                     InterPro or SMART accession for instance).
# - "Interaction Domain Description": String - The description of the domain.
# - "Interaction Domain Name": String - The name of the domain.
# NB: Values are expected to be provided between quotes!
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
# - ELM_id: String - The ELM identifier.
# - domain_InterPro: String - The InterPro accession.
# - domain_desc: String - The description of the domain (as provided in the input
#                         ELM - domain interaction file).
# - domain_name: String - The name of the domain (as registered in Pfam).
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

# Index of columns in the ELM domains interactions file
ELM_DOMAIN_INTERACTIONS_COL_INDEX_ELM_ID = 0
ELM_DOMAIN_INTERACTIONS_COL_INDEX_DOMAIN_ID = 1
ELM_DOMAIN_INTERACTIONS_COL_INDEX_DOMAIN_DESC = 2
ELM_DOMAIN_INTERACTIONS_COL_INDEX_DOMAIN_NAME = 3


# List of options allowed
# -----------------------
# Path to the ELM - domain interactions file (contains the pairs 
# of ELM - domains interactions, i.e SLiM-domain interaction templates
# using ELM IDs and Pfam accessions)
ELM_DOMAIN_INTERACTIONS_PFAM_FILE_PATH_OPTION = 'ELM_DOMAIN_INTERACTIONS_PFAM_FILE_PATH'
# Path to the file containing the cross-references
CROSSREFERENCES_FILE_PATH_OPTION = 'CROSSREFERENCES_FILE_PATH'
# Path to the ELM - domain interactions file with InterPro accessions
# (contains the pairs of ELM - domains interactions, i.e SLiM-domain 
# interaction templates using ELM IDs and InterPro accessions)
ELM_DOMAIN_INTERACTIONS_INTERPRO_FILE_PATH_OPTION = 'ELM_DOMAIN_INTERACTIONS_INTERPRO_FILE_PATH'


OPTION_LIST = [ [ '-p', '--elmInteractionDomainsPfam', 'store', 'string', ELM_DOMAIN_INTERACTIONS_PFAM_FILE_PATH_OPTION, None, 
                  'The path to the ELM - domain interactions file (contains the pairs of ELM - domains interactions, i.e SLiM-domain interaction templates using ELM IDs and Pfam accessions)' ],
                [ '-c', '--crossReferences', 'store', 'string', CROSSREFERENCES_FILE_PATH_OPTION, None,
                  'The path to the file containing the cross-references (Pfam - InterPro).' ],
                [ '-i', '--elmInteractionDomainsInterPro', 'store', 'string', ELM_DOMAIN_INTERACTIONS_INTERPRO_FILE_PATH_OPTION, None, 
                  'Path to the ELM - domain interactions file with InterPro accessions (contains the pairs of ELM - domains interactions, i.e SLiM-domain interaction templates using ELM IDs and InterPro accessions)' ] ]



# ===========================================
# Script
# ===========================================

def elm_domain_interactions_to_interpro( elm_domain_interactions_pfam_file_path, crossreferences_file_path, \
                                         elm_domain_interactions_interpro_file_path ):
    
    '''
    This method allows to generate a file containing the pairs of ELM - domain interactions
    using InterPro accessions instead of Pfam accessions provided by the ELM resource.
    
    @param elm_domain_interactions_pfam_file_path: String - The path to the ELM - domain interactions file 
                                                            (contains the pairs of ELM - domains interactions, 
                                                            i.e SLiM-domain interaction templates using ELM IDs 
                                                            and Pfam accessions).
    @param crossreferences_file_path: String - The path to the file containing the cross-references.
                                               (Pfam - InterPro).
    @param elm_domain_interactions_interpro_file_path: String - The path to the ELM - domain interactions file 
                                                                with InterPro accessions (contains the pairs of 
                                                                ELM - domains interactions, i.e SLiM-domain interaction 
                                                                templates using ELM IDs and InterPro accessions).
    '''
    
    # Import the cross-references
    # ---------------------------
    
    # Instantiate a dictionary that will associate to each Pfam accession
    # a dictionary containing its name, the type and the InterPro accession
    # in which it has been integrated
    crossreferences_dict = {}
    
    with open( crossreferences_file_path, 'r' ) as crossreferences_file:
        
        # Skip the header
        line = crossreferences_file.readline()
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
    
    
    
    # Convert the ELM - domain interactions
    # -------------------------------------
    
    # CAUTION: As this file uses Windows conventions instead of Unix,
    #          the carriage return is stated using '\r\n' instead of '\n'.
    #          The io package is thus use to allow splitting lines at the 
    #          right place.
    
    with open( elm_domain_interactions_interpro_file_path, 'w' ) as elm_domain_interactions_interpro_file:
         
        # Write the header in the output file
        header = [ 'ELM_id',
                   'domain_InterPro',
                   'domain_desc',
                   'domain_name' ]
        elm_domain_interactions_interpro_file.write( '\t'.join( header ) + '\n' )
        
        for line in io.open( elm_domain_interactions_pfam_file_path, mode = 'r', newline = '\r\n' ):
            
            # Parse the line and get the interacting domains
            line = line.replace( '\r', '' ).replace( '\n', '' )
            line = line.split( '"\t"' )
            line = list( map( lambda x: x.replace( '"', '' ), line ) )
            elm_id = line[ ELM_DOMAIN_INTERACTIONS_COL_INDEX_ELM_ID ]
            domain_acc = line[ ELM_DOMAIN_INTERACTIONS_COL_INDEX_DOMAIN_ID ]
            domain_desc = line[ ELM_DOMAIN_INTERACTIONS_COL_INDEX_DOMAIN_DESC ]
        
            # Most of the time, the accession provided in the file
            # is a Pfam. If this is the case, then try to get its
            # corresponding InterPro accession
            if ( domain_acc.startswith( 'PF' ) ):
            
                # Get the InterPro entry corresponding to this Pfam
                interpro_entry = crossreferences_dict.get( domain_acc )
                
                # If both the Pfam accession has a InterPro entry matching,
                # then report the interaction in the output file
                if interpro_entry:
                    
                    interpro_acc = interpro_entry[ CROSSREF_DICT_INTERPRO_KEY ]
                    pfam_name = interpro_entry[ CROSSREF_DICT_NAME_KEY ]
                    
                    interaction_pair = [ elm_id,
                                         interpro_acc,
                                         domain_desc,
                                         pfam_name ]
                    elm_domain_interactions_interpro_file.write( '\t'.join( interaction_pair ) + '\n' )
                    
                # Otherwise, if the Pfam accession has no InterPro entry matching, 
                # then log a message and skip this interaction
                else:
                    
                    print( datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S') + 
                           ' :: WARNING :: The Pfam entry ' + domain_acc + ' has no InterPro entry matching.' )
            
            # Otherwise, if the accession provided is already an InterPro, then keep it. 
            # If not (e.g. this is a SMART accession), then discard the entry.
            else:
                
                if domain_acc.startswith( 'IPR' ):  
                    
                    # Try to get the name corresponding to the domain from Pfam
                    pfam_name = crossreferences_dict.get( domain_acc )
                    # If this domain does not exist in Pfam, then get the name as 
                    # provided in the ELM - domain interaction file
                    if ( not pfam_name ):
                        pfam_name = line[ ELM_DOMAIN_INTERACTIONS_COL_INDEX_DOMAIN_NAME ]
                    
                    interaction_pair = [ elm_id,
                                         domain_acc,
                                         domain_desc,
                                         pfam_name ]
                    elm_domain_interactions_interpro_file.write( '\t'.join( interaction_pair ) + '\n' )
                    
                else:
                    
                    print( datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S') + 
                           ' :: WARNING :: The domain with accession ' + domain_acc + 
                           ' has no InterPro entry matching.' )



# ===========================================
# Parse command line arguments 
# and run script
# ===========================================

if ( __name__ == '__main__' ):
    
    # Parse the command-line arguments
    option_dict = parse_arguments( OPTION_LIST )
    
    # Get the path to the ELM - domain interactions file
    elm_domain_interactions_pfam_file_path = get_option( option_dict = option_dict,
                                                         option_name = ELM_DOMAIN_INTERACTIONS_PFAM_FILE_PATH_OPTION,
                                                         not_none = True )
    
    # Get the path to the file containing the cross-references
    crossreferences_file_path = get_option( option_dict = option_dict,
                                            option_name = CROSSREFERENCES_FILE_PATH_OPTION,
                                            not_none = True )
    
    # Get the path to the ELM - domain interactions file with InterPro accessions
    elm_domain_interactions_interpro_file_path = get_option( option_dict = option_dict,
                                                             option_name = ELM_DOMAIN_INTERACTIONS_INTERPRO_FILE_PATH_OPTION,
                                                             not_none = True )
    
    # Run the script
    print( datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S') + 
           ' :: INFO :: Starting the conversion of Pfam accessions into InterPro accessions in' +
           ' the ELM-domain interactions template file.' )
    try:
        elm_domain_interactions_to_interpro( elm_domain_interactions_pfam_file_path = elm_domain_interactions_pfam_file_path, 
                                             crossreferences_file_path = crossreferences_file_path, 
                                             elm_domain_interactions_interpro_file_path = elm_domain_interactions_interpro_file_path )
    except Exception as e:
        exit( 'An exception has been raised during the execution of the script: \n' +
              str( e ) )
    else:
        print( datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S') + 
               ' :: INFO :: The conversion of Pfam accessions into InterPro accessions in' +
               ' the ELM-domain interactions template file has finished.' )
    