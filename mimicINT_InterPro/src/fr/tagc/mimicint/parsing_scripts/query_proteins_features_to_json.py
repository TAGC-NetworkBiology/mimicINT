#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json

from fr.tagc.mimicint.util.option.OptionManager import *

# This script allows to generate a json file containing
# the features of all the query proteins necessary to
# vizualise the proteins on browsers


# ===========================================
# Constants
# ===========================================

# Index of the columns of the query domain parsed file
QUERY_DOMAIN_PARSED_PROT_NAME_INDEX = 0
QUERY_DOMAIN_PARSED_SIGNATURE_ACC_INDEX = 2
QUERY_DOMAIN_PARSED_DESCRIPTION_INDEX = 3
QUERY_DOMAIN_PARSED_START_POS_INDEX = 4
QUERY_DOMAIN_PARSED_STOP_POS_INDEX = 5
QUERY_DOMAIN_PARSED_IPS_ANNOT_INDEX = 7

# Index of the columns of the query SLIM parsed file
QUERY_SLIM_PARSED_PROT_NAME_INDEX = 0
QUERY_SLIM_PARSED_MOTIF_ID_INDEX = 1
QUERY_SLIM_PARSED_DESCRIPTION_INDEX = 2
QUERY_SLIM_PARSED_START_POS_INDEX = 3
QUERY_SLIM_PARSED_STOP_POS_INDEX = 4

# Index of the columns of the disorder propensities file
QUERY_DISORDER_PROPENSITIES_PROT_NAME_INDEX = 0
QUERY_DISORDER_PROPENSITIES_VALUES_INDEX = 3


# List of options allowed
# -----------------------
# Path to the query sequences fasta file
QUERY_FASTA_FILE_OPTION = 'QUERY_FASTA_FILE'
# Path to the query domain parsed file
QUERY_DOMAIN_PARSED_FILE_OPTION = 'QUERY_DOMAIN_PARSED_FILE'
# Path to the query SLiMProb parsed file
QUERY_SLIMPROB_PARSED_FILE_OPTION = 'QUERY_SLIMPROB_PARSED_FILE'
# Path to the disorder propensities file
DISORDER_PROPENSITIES_FILE_OPTION = 'DISORDER_PROPENSITIES_FILE'
# Path to the query features JSON file
QUERY_FEATURES_JSON_FILE_OPTION = 'QUERY_FEATURES_JSON_FILE'

OPTION_LIST = [ [ '-f', '--queryFasta', 'store', 'string', QUERY_FASTA_FILE_OPTION, None, '' ],
                [ '-d', '--queryDomain', 'store', 'string', QUERY_DOMAIN_PARSED_FILE_OPTION, None, '' ],
                [ '-m', '--querySlimprob', 'store', 'string', QUERY_SLIMPROB_PARSED_FILE_OPTION, None, '' ],
                [ '-p', '--queryPropensities', 'store', 'string', DISORDER_PROPENSITIES_FILE_OPTION, None, '' ],
                [ '-o', '--output', 'store', 'string', QUERY_FEATURES_JSON_FILE_OPTION, None, '' ] ]



# ===========================================
# Script
# ===========================================

## query_proteins_features_to_json
#  -------------------------------
#
# This function allows to generate a JSON file resuming
# the most important features of the query sequences.
#
# @param query_fasta_file: String - The path to the query sequences fasta file.
# @param query_domain_parsed_file: String - The path to the query domain parsed file.
# @param query_slim_parsed_file: String - The path to the query SLiMProb parsed file.
# @param disorder_propensities_file: String - The path to the disorder propensities file.
# @param query_features_json_file: String - The path to the query features JSON file (the output).
#
def query_proteins_features_to_json( query_fasta_file, query_domain_parsed_file, query_slim_parsed_file, \
                                     disorder_propensities_file, query_features_json_file ):
    
    # Get all the query sequence names
    # Ideally, the match_query_sqce_names rule succeed to associate 
    # to each sequence name of SLiMProb output its actual sequence 
    # name as provided in the query fasta file. Nevertheless, this
    # can sometimes fail, resulting in key errors in the current 
    # script when trying to access the dictionary with SLiMProb 
    # sequence names. In order to avoid this, the sequences for which
    # no match may be found are registered twice under both of their 
    # name (meaning the information belonging to the smae protein will 
    # unfortunatelly be registered in two "objects" of the json file).
    sequences_dict = {}
    
    # Get all the query sequence names and sequences from the fasta file
    with open( query_fasta_file, 'r' ) as query_fasta:
        line = query_fasta.readline().replace( '\n', '' )
        while ( line != '' ):
            if line.startswith( '>' ):
                # Parse the header to get the name of the protein and 
                # instantiate a string for this protein in the dictionary
                line = line[1:]
                protein_name = line.split( ' ' )[0]
                sequences_dict[ protein_name ] = ''
            else:
                # Add the line to the sequence
                sequences_dict[ protein_name ] += line
            line = query_fasta.readline().replace( '\n', '' )
    
    # Complete the dictionary of sequence nmaes
    with open( disorder_propensities_file, 'r' ) as disorder_propensities:
        # Skip headers
        next( disorder_propensities )
        line = disorder_propensities.readline().replace( '\n', '' )
        while ( line != '' ):
            # Parse the line to get information about the motif
            line = line.split( '\t' )
            protein_name = line[ QUERY_DISORDER_PROPENSITIES_PROT_NAME_INDEX ]
            # If the protein name is not registered in the dictionary, add it
            existing_protein_name = sequences_dict.get( protein_name )
            if ( not existing_protein_name ): 
                sequences_dict[ protein_name ] = ''
    
            line = disorder_propensities.readline().replace( '\n', '' )
    
    
    # Get all the domains detected on the query proteins
    # Instantiate a dictionary that associate to each query
    # protein its list of domains
    domains_dict = { protein_name: [] for protein_name in sequences_dict.keys() }
    with open( query_domain_parsed_file, 'r' ) as query_domain_parsed:
        # Skip headers
        next( query_domain_parsed )
        line = query_domain_parsed.readline().replace( '\n', '' )
        while ( line != '' ):
            # Parse the line to get information about the domain
            line = line.split( '\t' )
            protein_name = line[ QUERY_DOMAIN_PARSED_PROT_NAME_INDEX ]
            start_pos = line[ QUERY_DOMAIN_PARSED_START_POS_INDEX ]
            stop_pos = line[ QUERY_DOMAIN_PARSED_STOP_POS_INDEX ]
            description = line[ QUERY_DOMAIN_PARSED_DESCRIPTION_INDEX ]
            signature_acc = line[ QUERY_DOMAIN_PARSED_SIGNATURE_ACC_INDEX ]
            interpro_annot = line[ QUERY_DOMAIN_PARSED_IPS_ANNOT_INDEX ]
            domain = { 'x': start_pos,
                       'y': stop_pos,
                       'description': description + '\n InterPro annotation:' + interpro_annot, 
                       'id': signature_acc }
            
            # Append the entry to the list of domain for the protein
            domains_dict[ protein_name ].append( domain )
            
            line = query_domain_parsed.readline().replace( '\n', '' )
    
    
    # Get all the motifs detected on the query proteins
    # Instantiate a dictionary that associate to each query
    # protein its list of SLiMs
    motifs_dict = { protein_name: [] for protein_name in sequences_dict.keys() }
    with open( query_slim_parsed_file, 'r' ) as query_slim_parsed:
        # Skip headers
        next( query_slim_parsed )
        line = query_slim_parsed.readline().replace( '\n', '' )
        while ( line != '' ):
            # Parse the line to get information about the motif
            line = line.split( '\t' )
            protein_name = line[ QUERY_SLIM_PARSED_PROT_NAME_INDEX ]
            start_pos = line[ QUERY_SLIM_PARSED_START_POS_INDEX ]
            stop_pos = line[ QUERY_SLIM_PARSED_STOP_POS_INDEX ]
            description = line[ QUERY_SLIM_PARSED_DESCRIPTION_INDEX ]
            motif_id = line[ QUERY_SLIM_PARSED_MOTIF_ID_INDEX ]
            motif = { 'x': start_pos,
                      'y': stop_pos,
                      'description': description, 
                      'id': motif_id }
            
            # Append the entry to the list of domain for the protein
            motifs_dict[ protein_name ].append( motif )
    
            line = query_slim_parsed.readline().replace( '\n', '' )
    
    
    # Get the disorder propensities of the amino acids 
    # for each query protein sequence
    # Instantiate a dictionary that associate to each query
    # protein its list of IUPred scores
    iuscore_dict = { protein_name: [] for protein_name in sequences_dict.keys() }
    with open( disorder_propensities_file, 'r' ) as disorder_propensities:
        # Skip headers
        next( disorder_propensities )
        line = disorder_propensities.readline().replace( '\n', '' )
        while ( line != '' ):
            # Parse the line to get information about the motif
            line = line.split( '\t' )
            protein_name = line[ QUERY_DISORDER_PROPENSITIES_PROT_NAME_INDEX ]
            iuscores = line[ QUERY_DISORDER_PROPENSITIES_VALUES_INDEX ].split( ',' )
            aa_pos = 0
            for iuscore in iuscores:
                aa_pos += 1
                iuscore_dict[ protein_name ].append( { 'x': aa_pos,
                                                       'y': float( iuscore ) } )
    
            line = disorder_propensities.readline().replace( '\n', '' )

          
    # Build the dictionary that will be written in the JSON file
    json_dict = {}
    for prot_name in sequences_dict.keys():
        json_dict[ prot_name ]  = { 'sequence': sequences_dict.get( prot_name ),
                                    'domains': domains_dict.get( prot_name ),
                                    'motifs': motifs_dict.get( prot_name ),
                                    'IUPRED': iuscore_dict.get( prot_name ) }
    
    with open( query_features_json_file, 'w' ) as query_features_json:
        json.dump( json_dict, query_features_json, indent=4 )



# ===========================================
# Parse command line arguments 
# and run script
# ===========================================
     
if __name__=='__main__':
    
    # Parse the command-line arguments
    option_dict = parse_arguments( OPTION_LIST )
    
    # Get the query sequences fasta file path
    query_fasta_file = get_option( option_dict = option_dict, 
                                   option_name = QUERY_FASTA_FILE_OPTION, 
                                   not_none = True )
    
    # Get the query domain parsed file path
    query_domain_parsed_file = get_option( option_dict = option_dict, 
                                           option_name = QUERY_DOMAIN_PARSED_FILE_OPTION, 
                                           not_none = True )
    
    # Get the query SLiMProb parsed file path
    query_slim_parsed_file = get_option( option_dict = option_dict, 
                                           option_name = QUERY_SLIMPROB_PARSED_FILE_OPTION, 
                                           not_none = True )
    
    # Get the disorder propensities file path
    disorder_propensities_file = get_option( option_dict = option_dict, 
                                             option_name = DISORDER_PROPENSITIES_FILE_OPTION, 
                                             not_none = True )
    
    # Get the query features JSON file path
    query_features_json_file = get_option( option_dict = option_dict, 
                                             option_name = QUERY_FEATURES_JSON_FILE_OPTION, 
                                             not_none = True )
    
    # Run the script
    query_proteins_features_to_json( query_fasta_file = query_fasta_file, 
                                     query_domain_parsed_file = query_domain_parsed_file, 
                                     query_slim_parsed_file = query_slim_parsed_file,
                                     disorder_propensities_file = disorder_propensities_file, 
                                     query_features_json_file = query_features_json_file )
    