#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json

from fr.tagc.mimicint.util.option.OptionManager import *

# This script allows to generate a json file of all 
# inferred interactions compatible with Cytoscape


# ===========================================
# Constants
# ===========================================
 
# Index of the column containing the sequence ID
# in the domain parsed files
DOMAIN_FILE_PROT_INDEX = 0
 
# Index of the columns in the inferred_all_interactions_file file
  # Protein 1
ALL_INTER_FILE_PROT1_INDEX = 0
  # Protein 2
ALL_INTER_FILE_PROT2_INDEX = 1
  # Type of interaction
ALL_INTER_FILE_INTER_TYPE_INDEX = 2
 
# Types of interactions registered in the inferred_all_interactions_file file
  # SLiM-domain
SLIM_DOMAIN_INTERACTION = 'slim-domain'
  # domain-domain
DOMAIN_DOMAIN_INTERACTION = 'domain-domain'
 
# Types of interactions to register in the JSON file
  # Domain-domain
DOMAIN_DOMAIN_INTERACTION_JSON_TYPE_1 = '1'
  # SLiM-domain
SLIM_DOMAIN_INTERACTION_JSON_TYPE_2 = '2'
  # Both domain-domain SLiM-domain interactions
BOTH_INTERACTIONS_JSON_TYPE_3 = '3'


# List of options allowed
# -----------------------
# Path to the file containing all the inferred interactions
INFERRED_ALL_INTERACTIONS_FILE_OPTION = 'INFERRED_ALL_INTERACTIONS_FILE'
# Path to the file containing all the domains annotated in the target sequences
TARGET_DOMAIN_ANNOTATIONS_FILE_OPTION = 'TARGET_DOMAIN_ANNOTATIONS_FILE'
# Path to the JSON file generated
JSON_OUTPUT_FILE_OPTION = 'JSON_OUTPUT_FILE'

OPTION_LIST = [ [ '-i', '--inferredInteractions', 'store', 'string', INFERRED_ALL_INTERACTIONS_FILE_OPTION, None, 'The path to the file containing all the inferred interactions.' ],
                [ '-t', '--targetDomain', 'store', 'string', TARGET_DOMAIN_ANNOTATIONS_FILE_OPTION, None, 'The path to the file containing all the domains annotated in the target sequences.' ],
                [ '-o', '--output', 'store', 'string', JSON_OUTPUT_FILE_OPTION, None, 'The path to the JSON file generated.' ] ]



# ===========================================
# Script
# ===========================================

# generate_json
# -------------
#
# This function allows to generate a JSON file compatible with 
# Cytoscape and that contains all the interactions inferred by
# the pipeline.
# NB: Three types of edges are registered in this file:
#     1 - The domain-domain interactions
#     2 - The SLiM-domain interactions
#     3 - The proteins that interact through both domain-domain and
#         SLiM-domain interactions
#
# @param inferred_all_interactions_file: String - The path to the file containing all the 
#                                                 inferred interactions.
# @param target_domain_annotations_file: String - The path to the file containing all the domains 
#                                                 annotated in the target sequences.
# @param all_interactions_json_file: String - The path to the JSON file generated.
#
def generate_json( inferred_all_interactions_file, target_domain_annotations_file, all_interactions_json_file ):
    
    # Get the list of target protein names from 
    # the query_domain_parsed_file file
    all_target_proteins_list = []
    with open( target_domain_annotations_file, 'r' ) as target_domain_annot_file:
        # Skip headers
        next( target_domain_annot_file )
        line = target_domain_annot_file.readline()
        while ( line != '' ):
            all_target_proteins_list.append( line.split( '\t' )[ DOMAIN_FILE_PROT_INDEX ] )
            line = target_domain_annot_file.readline()
    
    
    # NB: All proteins which are not part of the all_target_proteins_list 
    #     are then considered as query protein.
    # NB: If necessary, SLiM sequence names could be imported from the
    #     query_domain_parsed_file and query_slim_slimprob_parsed_file
    #     files.
    
    
    # Get the protein names interacting together and the nature of the 
    # interactions between target and query proteins.
    # Define a dictionary to register all the target proteins and their 
    # degrees and a dictionary to register all the query proteins and 
    # their degrees.
    target_protein_degrees = {}
    query_protein_degress = {}

    # Defines a list that will register all the SLiM-domain interactions 
    # and a list that will register all the domain-domain interactions.
    # NB: An interaction is registered as (target protein, query protein) 
    #     in this list.
    slim_domain_interactions = []    
    domain_domain_interactions = []
    
    with open( inferred_all_interactions_file, 'r' ) as all_interactions_file:
        # Skip headers
        next( all_interactions_file )
        line = all_interactions_file.readline()
        while ( line != '' ):
            line = line.split( '\t' )
            
            # Get the name of the proteins
            protein_1 = line[ ALL_INTER_FILE_PROT1_INDEX ]
            protein_2 = line[ ALL_INTER_FILE_PROT2_INDEX ]
            # Check which of the protein comes from the target
            # and which comes from the query
            if ( protein_1 in all_target_proteins_list ):
                target_protein = protein_1
                query_protein = protein_2
            else:
                target_protein = protein_2
                query_protein = protein_1
                
            # Add the target proteins to the dictionaries containing 
            # the target nodes
            if ( target_protein in target_protein_degrees.keys() ):
                target_protein_degrees[ target_protein ] += 1
            else:
                target_protein_degrees[ target_protein ] = 1
                
            # Add the query proteins to the dictionaries containing 
            # the query nodes
            if ( query_protein in query_protein_degress.keys() ):
                query_protein_degress[ query_protein ] += 1
            else:
                query_protein_degress[ query_protein ] = 1
             
             
            # Get the type of interaction
            interaction_type = line[ ALL_INTER_FILE_INTER_TYPE_INDEX ]
            # Add the interaction to the appropriate list
            if ( interaction_type == SLIM_DOMAIN_INTERACTION + '\n' ):
                slim_domain_interactions.append( ( target_protein, query_protein ) )
            elif ( interaction_type == DOMAIN_DOMAIN_INTERACTION + '\n' ):
                domain_domain_interactions.append( ( target_protein, query_protein ) )
            
            # Get the next line
            line = all_interactions_file.readline()
    
    # Get the couple of (target, query) proteins that interact together 
    # through both SLiM-domain and domain-domain interactions
    domain_domain_interactions_set = set( domain_domain_interactions )
    slim_domain_interactions_set = set( slim_domain_interactions )
    both_interactions = list( domain_domain_interactions_set.intersection( slim_domain_interactions_set ) )
        
    
    # Prepare the lists of proteins and interactions to be exported as JSON file        
    # Build the list of nodes
    nodes_list = []
    
    # Add the target proteins to the list of nodes
    for ( target_protein, degree ) in target_protein_degrees.items():
        nodes_list.append( { "data": { "id": target_protein,
                                       "type": "target",
                                       "target_degree": str( degree ) } } )
        
    # Add the query proteins to the list of nodes
    for ( query_protein, degree ) in query_protein_degress.items():
        nodes_list.append( { "data": { "id": query_protein,
                                       "type": "query",
                                       "query_degree": str( degree ) } } )
        
    # Build the list of edges
    edges_list = []
    autoincrement_id = 1
    
    # Add the domain-domain interactions to the list of edges
    for ( target_protein, query_protein ) in domain_domain_interactions:
        edges_list.append( { "data": { "id": str( autoincrement_id ),
                                       "source": target_protein,
                                       "target": query_protein,
                                       "type": DOMAIN_DOMAIN_INTERACTION_JSON_TYPE_1 } } )
        autoincrement_id += 1
        
    # Add the slim-domain interactions to the list of edges
    for ( target_protein, query_protein ) in slim_domain_interactions:
        edges_list.append( { "data": { "id": str( autoincrement_id ),
                                       "source": target_protein,
                                       "target": query_protein,
                                       "type": SLIM_DOMAIN_INTERACTION_JSON_TYPE_2 } } )
        autoincrement_id += 1
        
    # Add the proteins that interact together through both domain-domain
    # and SLiM-domain interactions to the list of edges
    for ( target_protein, query_protein ) in both_interactions:
        edges_list.append( { "data": { "id": str( autoincrement_id ),
                                       "source": target_protein,
                                       "target": query_protein,
                                       "type": BOTH_INTERACTIONS_JSON_TYPE_3 } } )
        autoincrement_id += 1
        
        
    # Build the dictionary that will be written in the JSON file
    json_dict = { "nodes": nodes_list,
                  "edges": edges_list }
    
    with open( all_interactions_json_file, 'w' ) as output_file:
        json.dump( json_dict, output_file, indent=4 )



# ===========================================
# Parse command line arguments 
# and run script
# ===========================================
     
if __name__=='__main__':
    
    # Parse the command-line arguments
    option_dict = parse_arguments( OPTION_LIST )
    
    # Get the path to the file containing all interactions
    inferred_all_interactions_file = get_option( option_dict = option_dict, 
                                                 option_name = INFERRED_ALL_INTERACTIONS_FILE_OPTION, 
                                                 not_none = True )
    
    # Get the path to the file containing the annotated domains
    target_domain_annotations_file = get_option( option_dict = option_dict,
                                                 option_name = TARGET_DOMAIN_ANNOTATIONS_FILE_OPTION,
                                                 not_none = True )
    
    # Get the path to the output file
    all_interactions_json_file = get_option( option_dict = option_dict, 
                                             option_name = JSON_OUTPUT_FILE_OPTION, 
                                             not_none = True )
    
    # Run the script    
    generate_json( inferred_all_interactions_file = inferred_all_interactions_file, 
                   target_domain_annotations_file = target_domain_annotations_file, 
                   all_interactions_json_file = all_interactions_json_file )
    