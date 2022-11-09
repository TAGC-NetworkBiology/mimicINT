#!/usr/bin/python3
# -*- coding: utf-8 -*-

import datetime

from fr.tagc.mimicint.util.option.OptionManager import *

# This script allows to generate the list of inferred interaction
# based on the domain-domain and SLiM-domain interaction templates

# NB: It uses InterPro accession to perform the inference.
#     Please see the script from the original mimicINT workflow if
#     you are willing to use Pfam accessions instead.



# Description of the input files
# ------------------------------

# The file with parsed InterProScan results for query proteins 
# is a tsv file that contains the following columns:
# - Protein_Accession: String - The accession of the protein.
# - Analysis: String - The type of analysis run with InterProScan (Pfam).
# - Signature_Accession: String - The Pfam accession of the signature.
# - Signature_Description: String - The description of the domain.
# - Start_location: Integer - The relative start location of the domain.
# - Stop_location: Integer - The relative end location of the domain.
# - Score: Float - The score attributed to the domain by InterProScan.
# - Interpro_Annotation: String - The InterPro accession of the domain.
# NB: This file contains a header.
#
#
# The file with InterPro annotated domains for target proteins 
# is a tsv file that contains the following columns:
# - UniProtKB_accession: String - The protein accession in UniProtKB.
# - name: String - The name of the protein.
# - length: Integer - The length of the protein.
# - InterPro_accession: String - The InterPro accession.
# - entry_type: String - The type of InterPro entry (homologous superfamily, protein family, 
#                        domain or repeat).
#                        See https://www.ebi.ac.uk/training/online/courses/interpro-functional-and-structural-analysis/what-is-an-interpro-entry/interpro-entry-types/ 
#                        for more information about the entry types.
# - start: Integer - The start position of the entry on the protein. 
#                    If the entry is fragmented, this position corresponds to 
#                    the lowest value of all start positions.
# - end: Integer - The end position of the entry on the protein.
#                  If the entry is fragmented, this position corresponds to 
#                  the highest value of all start positions.
# - fragmented: Boolean - Is the entry fragmented?
# 
# 
# The file with parsed SLiMProb results for query proteins
# is a tsv file that contains the following columns:
# - Seq: String - The name of the sequence.
# - Motif: String - The ELM identifier of the motif.
# - Description: String - The description of the motif.
# - Start_Pos: Integer - The relative start position of the motif on the protein.
# - End_Pos: Integer - The relative end position of the motif on the protein.
# - Prot_Len: Integer - The protein length.
# - Pattern: String - The regular expression of the motif pattern.
# - Match: String - The motif of the protein matching the pattern.
# - Comp: Float - The complexity measure calculated by slimcalc. 
#                 From SLiMProb user's manual: This value equals the number of different amino acids 
#                 observed across the length of the SLiM occurrence, divided by the maximum possible 
#                 number, which is the length of the motif or twenty, whichever is smaller. 
#                 E.g. a PxxPx[KR] motif occurrence with a sequence PASPPR 
#                      would have a complexity  of 4/6 = 0.6667
# - IUP: Float - The disorder propensity computed by IUPred.
#                From SLiMProb user's manual: IUPred calculates the mean disorder across the SLiM.
#                Each amino acid gets its own disorder score, ranging from 0 (ordered) to 1 (disordered), 
#                which is then averaged over the length of the SLiM.
#
#
# The file with the ELM - domain interactions (InterPro accessions)
# (contains the pairs of ELM - domains interactions, i.e SLiM-domain 
# interaction templates using ELM IDs and InterPro accessions)
# is a tsv file that contains the following columns:
# - ELM_id: String - The ELM identifier.
# - domain_InterPro: String - The InterPro accession.
# - domain_desc: String - The description of the domain.
# - domain_name: String - The name of the domain.
# NB: This file contains a header.
#
#
# The file containing the templates of domain-domain interactions 
# (as InterPro accessions) is a tsv file that contains the following columns:
# - InterPro_acc_1: String - The InterPro accession of the first domain.
# - InterPro_acc_2: String - The InterPro accession of the second domain.
# - InterPro_name_1: String - The InterPro name of the first domain.
# - InterPro_name_2: String - The InterPro name of the second domain.
# NB: This file contains a header.



# Description of the output file
# ------------------------------

# The file registering the SLiM-domain interactions is a tsv file
# that contains the following columns:
# - Slim_Protein_acc: String - The accession, name or ID of the query protein.
# - Slim_Motif: String - The ELM identifier of the motif.
# - Slim_Start: Integer - The relative start position of the motif.
# - Slim_End: Integer - The relative end position of the motif.
# - Slim_Description: String - The description of the motif.
# - Prot_Accession: String - The accession, name or ID of the target protein.
# - Domain_Prot_Accession: String - The InterPro accession of the domain.
# - Domain_Start: Integer - The relative start position of the domain.
# - Domain_End: Integer - The relative end position of the domain.
# - Domain_Fragmented: Boolean - Is the domain fragmented?
# - Domain_Name: String - The name of the domain.
# NB: This file contains a header.
#
#
# The file registering the domain-domain interactions is a tsv file
# that contains the following columns:
# - Prot_Accession1: String - The accession, name or ID of the query protein.
# - Domain_Prot_Accession1: String - The InterPro accession of the domain (on the query protein).
# - Domain_Start1: Integer - The relative start location of the domain (on the query protein).
# - Domain_End1: Integer - The relative end location of the domain (on the query protein).
# - Domain_Name1: String - The name of the domain (on the query protein).
# - Prot_Accession2: String - The accession, name or ID of the target protein.
# - Domain_Prot_Accession2: String - The InterPro accession of the domain (on the target protein).
# - Domain_Start2: Integer - The relative start location of the domain (on the target protein).
# - Domain_End2: Integer - The relative end location of the domain (on the target protein).
# - Domain_Fragmented2: Boolean - Is the domain fragmented (on the target protein)?
# - Domain_Name2: String - The name of the domain (on the target protein).
# NB: This file contains a header.



# ===========================================
# Constants
# ===========================================

# Constants
# ---------

# Index of columns in the ELM domains interactions file
ELM_DOMAIN_INTERACTIONS_COL_INDEX_ELM_ID = 0
ELM_DOMAIN_INTERACTIONS_COL_INDEX_DOMAIN_ID = 1
ELM_DOMAIN_INTERACTIONS_COL_INDEX_DOMAIN_DESC = 2
ELM_DOMAIN_INTERACTIONS_COL_INDEX_DOMAIN_NAME = 3

# Index of columns in the 3did file using InterProScan accessions
DDI_INTERPRO_COL_INDEX_INTERPRO_ACC_1 = 0
DDI_INTERPRO_COL_INDEX_INTERPRO_ACC_2 = 1
DDI_INTERPRO_COL_INDEX_INTERPRO_NAME_1 = 2
DDI_INTERPRO_COL_INDEX_INTERPRO_NAME_2 = 3

# Headers of the file with InterPro annotated domains for target proteins
TARGET_DOMAIN_ANNOTATION_FILE_HEADER_UNIPROTKB_ACC = 'UniProtKB_accession'
TARGET_DOMAIN_ANNOTATION_FILE_HEADER_PROTEIN_NAME = 'name'
TARGET_DOMAIN_ANNOTATION_FILE_HEADER_PROTEIN_LENGTH = 'length'
TARGET_DOMAIN_ANNOTATION_FILE_HEADER_INTERPRO_ACC = 'InterPro_accession'
TARGET_DOMAIN_ANNOTATION_FILE_HEADER_ENTRY_TYPE = 'entry_type'
TARGET_DOMAIN_ANNOTATION_FILE_HEADER_START = 'start'
TARGET_DOMAIN_ANNOTATION_FILE_HEADER_END = 'end'
TARGET_DOMAIN_ANNOTATION_FILE_HEADER_FRAGMENTED = 'fragmented'

# Headers of the file with parsed InterProScan results for query proteins
QUERY_INTERPROSCAN_FILE_HEADER_PROT_ACC = 'Protein_Accession'
QUERY_INTERPROSCAN_FILE_HEADER_ANALYSIS = 'Analysis'
QUERY_INTERPROSCAN_FILE_HEADER_SIGNATURE_ACC = 'Signature_Accession'
QUERY_INTERPROSCAN_FILE_HEADER_SIGNATURE_DESC = 'Signature_Description'
QUERY_INTERPROSCAN_FILE_HEADER_START_POS = 'Start_location'
QUERY_INTERPROSCAN_FILE_HEADER_STOP_POS = 'Stop_location'
QUERY_INTERPROSCAN_FILE_HEADER_SCORE = 'Score'
QUERY_INTERPROSCAN_FILE_HEADER_INTERPRO_ACC = 'Interpro_Annotation'

# Headers of the file with parsed SLiMProb results for query proteins
QUERY_SLIMPROB_FILE_HEADER_SEQ_ID = 'Seq'
QUERY_SLIMPROB_FILE_HEADER_MOTIF_ID = 'Motif'
QUERY_SLIMPROB_FILE_HEADER_MOTIF_DESC = 'Description'
QUERY_SLIMPROB_FILE_HEADER_MOTIF_START_POS = 'Start_Pos'
QUERY_SLIMPROB_FILE_HEADER_MOTIF_END_POS = 'End_Pos'
QUERY_SLIMPROB_FILE_HEADER_PROT_LENGTH = 'Prot_Len'
QUERY_SLIMPROB_FILE_HEADER_MOTIF_PATTERN = 'Pattern'
QUERY_SLIMPROB_FILE_HEADER_MOTIF_MATCH = 'Match'
QUERY_SLIMPROB_FILE_HEADER_MOTIF_COMP = 'Comp'
QUERY_SLIMPROB_FILE_HEADER_MOTIF_IUP = 'IUP'



# List of options allowed
# -----------------------
# Path to the file with parsed InterProScan results for query proteins
QUERY_INTERPROSCAN_FILE_PATH_OPTION = 'QUERY_IPS_FILE_PATH'
# Path to the file with InterPro annotated domains for target proteins
TARGET_DOMAIN_ANNOTATION_FILE_PATH_OPTION = 'TARGET_DOMAIN_ANNOTATION_FILE_PATH'
# Path to file with parsed SLiMProb results for query proteins
QUERY_SLIMPROB_FILE_PATH_OPTION = 'QUERY_SP_FILE_PATH'

# Path to the ELM - domain interactions file with InterPro accessions
# (contains the pairs of ELM - domains interactions, i.e SLiM-domain 
# interaction templates using ELM IDs and InterPro accessions)
ELM_DOMAIN_INTERACTIONS_INTERPRO_FILE_PATH_OPTION = 'ELM_DOMAIN_INTERACTIONS_INTERPRO_FILE_PATH'
# Path to the file containing the interacting domains as InterPro
# accessions (contains the pairs of interacting domains as InterPro
# accessions)
DDI_INTERPRO_FILE_PATH_OPTION = 'DDI_INTERPRO_FILE_PATH'

# Path to output file registering the SLiM-domain interactions
OUTPUT_SLIM_DOMAIN_INTERACTIONS_FILE_PATH_OPTION = 'OUTPUT_SLIM_DOMAIN_INTERACTIONS_FILE_PATH'
# Path to output file registering the domain-domain interactions
OUTPUT_DOMAIN_DOMAIN_INTERACTIONS_FILE_PATH_OPTION = 'OUTPUT_DOMAIN_DOMAIN_INTERACTIONS_FILE_PATH'

OPTION_LIST = [ [ '-q', '--queryDomains', 'store', 'string', QUERY_INTERPROSCAN_FILE_PATH_OPTION, None, 'The path to the file with parsed InterProScan results for query proteins.' ],
                [ '-t', '--targetDomains', 'store', 'string', TARGET_DOMAIN_ANNOTATION_FILE_PATH_OPTION, None, 'The path to the file with InterPro annotated domains for target proteins.' ],
                [ '-s', '--querySlim', 'store', 'string', QUERY_SLIMPROB_FILE_PATH_OPTION, None, 'The path to file with parsed SLiMProb results for query proteins.' ],
                [ '-e', '--elmDomainInt', 'store', 'string', ELM_DOMAIN_INTERACTIONS_INTERPRO_FILE_PATH_OPTION, None, ( 'The path to the ELM - domain interactions file with InterPro accessions' +
                                                                                                                        ' (contains the pairs of ELM - domains interactions, i.e SLiM-domain interaction' +
                                                                                                                        ' templates using ELM IDs and InterPro accessions).' ) ],
                [ '-d', '--domainDomainInt', 'store', 'string', DDI_INTERPRO_FILE_PATH_OPTION, None, ( 'The path to the file containing the interacting domains as InterPro accessions (contains the pairs' +
                                                                                                       ' of interacting domains as InterPro accessions).' ) ],
                [ '-l', '--outputSlimDomainInt', 'store', 'string', OUTPUT_SLIM_DOMAIN_INTERACTIONS_FILE_PATH_OPTION, None, 'The path to output file registering the SLiM-domain interactions.' ],
                [ '-o', '--outputDomainDomainInt', 'store', 'string', OUTPUT_DOMAIN_DOMAIN_INTERACTIONS_FILE_PATH_OPTION, None, 'The path to output file registering the domain-domain interactions.' ] ]



# ===========================================
# Script
# ===========================================

def interaction_inference( query_interproscan_file_path, target_domain_annotation_file_path, query_slimprob_file_path, \
                           elm_domain_interactions_interpro_file_path, ddi_interpro_file_path, \
                           output_slim_domain_interactions_file_path, output_domain_domain_interactions_file_path ):
    
    '''
    @param query_interproscan_file_path: String - The path to the file with parsed InterProScan results 
                                                  for query proteins.
    @param target_domain_annotation_file_path: String - The path to the file with InterPro annotated domains
                                                        for target proteins.
    @param query_slimprob_file_path: String - The path to file with parsed SLiMProb results for query proteins.
    @param elm_domain_interactions_interpro_file_path: String - The path to the ELM - domain interactions file 
                                                                with InterPro accessions (contains the pairs of 
                                                                ELM - domains interactions, i.e SLiM-domain 
                                                                interaction templates using ELM IDs and InterPro 
                                                                accessions).
    @param ddi_interpro_file_path: String - The path to the file containing the interacting domains as InterPro 
                                            accessions (contains the pairs of interacting domains as InterPro 
                                            accessions).
    @param output_slim_domain_interactions_file_path: String - The path to output file registering the 
                                                               SLiM-domain interactions.
    @param output_domain_domain_interactions_file_path: String - The path to output file registering the 
                                                                 domain-domain interactions.
    
    This script infers protein-protein interactions based on interaction templates (from ELM and 3did) 
    by taking into account ELM occurrences (query) and domain occurrences (query and target).
    Three outputs (tsv files) are generated:
    - A file with all domain-domain interactions along with some of their characteristics (domain location etc.)
    - A file with all SLiM-domain interactions along with some of their characteristics (SLiM and domain location etc.)
    
    See the documentation of the script for more information about the outputs.
    '''
    
    # Get the SLiM and domain occurrences
    # -----------------------------------
    
    # Import the domains detected on query proteins 
    # (results from InterProScan) as a list of dictionaries
    query_domain_dict = import_tsv_as_list( tsv_file_path = query_interproscan_file_path ) 
    
    # Import the domains annotated on target proteins
    # (as InterPro accessions)
    target_domain_dict = import_tsv_as_list( tsv_file_path = target_domain_annotation_file_path )
    
    # Import the SLiM occurrences detected on query proteins 
    # (results from SLiMProb) as a list of dictionaries
    query_slim_occ_dict = import_tsv_as_list( tsv_file_path = query_slimprob_file_path ) 
    
    
    # Get the domain names
    # --------------------
    
    # Instantiate a dictionary that will associate to each InterPro accession (key) 
    # its domain name (value) from Pfam
    # This dictionary will be filled while parsing the 3did and ELM-domain interaction
    # templates
    # NB: The Pfam-InterPro cross-references file could also have been parsed to recover this information
    #     but InterPro entries from the ELM-domain interaction file that have no corresponding Pfam entries
    #     would have been missed.
    domain_names_dict = {}
    
    
    # Get the interaction templates
    # -----------------------------
    
    # Instantiate a set that will register all the SLiM-domain templates (from ELM)
    # Elements of the set are tuples (ELM ID, InterPro accession).
    slim_domain_int_templates_set = set()
    
    with open( elm_domain_interactions_interpro_file_path, 'r' ) as elm_domain_interactions_interpro_file:
        
        line = elm_domain_interactions_interpro_file.readline()
        
        while ( line != '' ):
            
            # Parse the line
            line = line.replace( '\n', '' )
            line = line.split( '\t' )
            elm_id = line[ ELM_DOMAIN_INTERACTIONS_COL_INDEX_ELM_ID ]
            domain_accession = line[ ELM_DOMAIN_INTERACTIONS_COL_INDEX_DOMAIN_ID ]
            domain_name = line[ ELM_DOMAIN_INTERACTIONS_COL_INDEX_DOMAIN_NAME ]
            
            # Add the SLiM - domain interaction to the set
            slim_domain_int_templates_set.add( ( elm_id, domain_accession ) )
            
            # Add the domain name to the dictionary that associates
            # to each InterPro accession its name
            existing_domain_name = domain_names_dict.get( domain_accession )
            if ( not existing_domain_name ):
                domain_names_dict[ domain_accession ] = domain_name
            
            # Read next line
            line = elm_domain_interactions_interpro_file.readline()
    
    
    # Instantiate a set that will register all the domain-domain templates (from 3did)
    # Elements of the set are tuples (InterPro accession, InterPro accession).
    domain_domain_int_templates_set = set()
    
    with open( ddi_interpro_file_path, 'r' ) as ddi_interpro_file:
        
        line = ddi_interpro_file.readline()
        
        while ( line != '' ):
            
            # Parse the line
            line = line.replace( '\n', '' )
            line = line.split( '\t' )
            first_domain_accession = line[ DDI_INTERPRO_COL_INDEX_INTERPRO_ACC_1 ]
            second_domain_accession = line[ DDI_INTERPRO_COL_INDEX_INTERPRO_ACC_2 ]
            
            # Add the SLiM - domain interaction to the set
            # NB: The graph generated is undirected, so both interactions domain1 -> domain2 
            #     and domain2 -> domain1 must be considered
            domain_domain_int_templates_set.add( ( first_domain_accession, second_domain_accession ) )
            domain_domain_int_templates_set.add( ( second_domain_accession, first_domain_accession ) )
            
            # Add the domain name to the dictionary that associates
            # to each InterPro accession its name
            first_domain_name = line[ DDI_INTERPRO_COL_INDEX_INTERPRO_NAME_1 ]
            existing_domain_name = domain_names_dict.get( first_domain_accession )
            if ( not existing_domain_name ):
                domain_names_dict[ domain_accession ] = first_domain_name
                
            second_domain_name = line[ DDI_INTERPRO_COL_INDEX_INTERPRO_NAME_2 ]
            existing_domain_name = domain_names_dict.get( second_domain_accession )
            if ( not existing_domain_name ):
                domain_names_dict[ domain_accession ] = second_domain_name

            # Read next line
            line = ddi_interpro_file.readline()
    
    
    # Interactions inference
    # ----------------------
    
    # Infer the SLiM (query) - domain (target) and 
    # domain (query) - domain (target) interactions
    with open( output_slim_domain_interactions_file_path, 'w' ) as output_slim_domain_interactions_file, \
         open( output_domain_domain_interactions_file_path, 'w' ) as output_domain_domain_interactions_file:
        
        # Write the header of the file registering SLiM-domain interactions
        slim_domain_header = [ 'Slim_Protein_acc', 'Slim_Motif', 'Slim_Start', 'Slim_End', 'Slim_Description',
                               'Prot_Accession', 'Domain_Prot_Accession', 'Domain_Start', 'Domain_End',
                               'Domain_Fragmented', 'Domain_Name' ]
        output_slim_domain_interactions_file.write( '\t'.join( slim_domain_header ) + '\n' )
        
        # Write the header of the file registering domain-domain interactions
        domain_domain_header =  [ 'Prot_Accession1', 'Domain_Prot_Accession1', 'Domain_Start1', 
                                  'Domain_End1', 'Domain_Name1',
                                  'Prot_Accession2', 'Domain_Prot_Accession2', 'Domain_Start2',
                                  'Domain_End2', 'Domain_Fragmented2', 'Domain_Name2' ]
        output_domain_domain_interactions_file.write( '\t'.join( domain_domain_header ) + '\n' )
        
        
        # For each domain annotated in each sequence of the target, 
        # look for the interactions it may mediate
        for row_inter_target in target_domain_dict:
            
            # Get the InterPro accession of the target entry
            target_interpro_acc = row_inter_target[ TARGET_DOMAIN_ANNOTATION_FILE_HEADER_INTERPRO_ACC ]
            
            
            # Infer SLiM-domain interactions
            # For each SLiM detected in each sequence of the query,
            # look for the interactions it may mediate
            for row_slim_query in query_slim_occ_dict:
                
                # Get the ELM identifier of the query entry
                query_motif_id = row_slim_query[ QUERY_SLIMPROB_FILE_HEADER_MOTIF_ID ]
                
                # Check if the domain of the target may interact with the motif of the query,
                # i.e. check if the domain and the motif are registered in the templates of
                # domain-motif interactions.
                # If this is the case, then record a new domain-SLiM interaction between
                # the two proteins. Otherwise, skip this query protein and process the 
                # next one.
                if ( ( query_motif_id, target_interpro_acc ) in slim_domain_int_templates_set ):
                    
                    # Get information about the query sequence
                    query_seq_id = row_slim_query[ QUERY_SLIMPROB_FILE_HEADER_SEQ_ID ]
                    query_slim_description = row_slim_query[ QUERY_SLIMPROB_FILE_HEADER_MOTIF_DESC ]
                    query_slim_start_pos = row_slim_query[ QUERY_SLIMPROB_FILE_HEADER_MOTIF_START_POS ]
                    query_slim_end_pos = row_slim_query[ QUERY_SLIMPROB_FILE_HEADER_MOTIF_END_POS ]
                    
                    # Get information about the target sequence
                    target_prot_acc = row_inter_target[ TARGET_DOMAIN_ANNOTATION_FILE_HEADER_UNIPROTKB_ACC ]
                    target_domain_start_pos = row_inter_target[ TARGET_DOMAIN_ANNOTATION_FILE_HEADER_START ]
                    target_domain_end_pos = row_inter_target[ TARGET_DOMAIN_ANNOTATION_FILE_HEADER_END ]
                    target_domain_fragmented = row_inter_target[ TARGET_DOMAIN_ANNOTATION_FILE_HEADER_FRAGMENTED ]
                    # Get the name of the target domain
                    target_domain_name = domain_names_dict.get( target_interpro_acc, '' )
        
                    # Add the interaction to the output file    
                    new_line = [ query_seq_id, 
                                 query_motif_id, 
                                 query_slim_start_pos, 
                                 query_slim_end_pos, 
                                 query_slim_description,
                                 target_prot_acc, 
                                 target_interpro_acc, 
                                 target_domain_start_pos, 
                                 target_domain_end_pos, 
                                 target_domain_fragmented,
                                 target_domain_name ]
                    output_slim_domain_interactions_file.write( '\t'.join( new_line ) + '\n' )
        
            
            # Infer domain-domain interactions
            # For each domain detected in each sequence of the query,
            # look for the interactions it may mediate
            for row_inter_query in query_domain_dict:
                
                # Get the InterPro accession of the query domain
                query_interpro_acc = row_inter_query[ QUERY_INTERPROSCAN_FILE_HEADER_INTERPRO_ACC ]
                
                # Check if the domain of the target may interact with the domain of the query,
                # i.e. check if the two domains are registered in the templates of domain-domain
                # interactions.
                # If this is the case, then record a new domain-domain interaction between
                # the two proteins. Otherwise, skip this query protein and process the 
                # next one.
                if ( query_interpro_acc, target_interpro_acc ) in domain_domain_int_templates_set:
                
                    # Get information about the query sequence
                    query_prot_acc = row_inter_query[ QUERY_INTERPROSCAN_FILE_HEADER_PROT_ACC ]
                    query_domain_desc = row_inter_query[ QUERY_INTERPROSCAN_FILE_HEADER_SIGNATURE_DESC ]
                    query_domain_start_pos = row_inter_query[ QUERY_INTERPROSCAN_FILE_HEADER_START_POS ]
                    query_domain_end_pos = row_inter_query[ QUERY_INTERPROSCAN_FILE_HEADER_STOP_POS ]
                    # Get the name of the query domain
                    query_domain_name = domain_names_dict.get( query_interpro_acc, '' )
                    
                    # Get information about the target sequence
                    target_prot_acc = row_inter_target[ TARGET_DOMAIN_ANNOTATION_FILE_HEADER_UNIPROTKB_ACC ]
                    target_domain_start_pos = row_inter_target[ TARGET_DOMAIN_ANNOTATION_FILE_HEADER_START ]
                    target_domain_end_pos = row_inter_target[ TARGET_DOMAIN_ANNOTATION_FILE_HEADER_END ]
                    target_domain_fragmented = row_inter_target[ TARGET_DOMAIN_ANNOTATION_FILE_HEADER_FRAGMENTED ]
                    # Get the name of the target domain
                    target_domain_name = domain_names_dict.get( target_interpro_acc, '' )
        
                    # Add the interaction to the output file    
                    new_line = [ query_prot_acc,
                                 query_interpro_acc,
                                 query_domain_start_pos,
                                 query_domain_end_pos,
                                 query_domain_name,
                                 target_prot_acc, 
                                 target_interpro_acc, 
                                 target_domain_start_pos, 
                                 target_domain_end_pos, 
                                 target_domain_fragmented,
                                 target_domain_name ]
                    output_domain_domain_interactions_file.write( '\t'.join( new_line ) + '\n' )
        
        
        
def import_tsv_as_list( tsv_file_path ):
    
    '''
    This method allows to import the content from a tsv file as a list of dictionaries.
    
    Each line is represented by an element of the list. Each element of the list is a
    dictionary that associate to each header (key) its value for the line (value).
    
    @param tsv_file_path: String - The path to the tsv file.
    
    @return tsv_content: List of dict - The list of dictionary corresponding to the tsv
                                        file content.
    '''
    
    tsv_content = []
    
    with open( tsv_file_path, 'r' ) as tsv_file:
                
        # Parse the header
        header = tsv_file.readline()
        header = header.replace( '\n', '' )
        header = header.split( '\t' )
        
        columns_count = len( header )
        
        # For each line of the file, convert it as a dictionary
        # and append the dictionary to the list
        line = tsv_file.readline()
        
        while ( line != '' ):
            
            line = line.replace( '\n', '' )
            line = line.split( '\t' )
            
            line_dict = {}
            for k in range( columns_count ):
                line_dict[ header[ k ] ] = line[ k ]
                
            line = tsv_file.readline()
            
            # Add the dictionary to the list
            tsv_content.append( line_dict )
            
    return tsv_content



# ===========================================
# Parse command line arguments 
# and run script
# ===========================================

if ( __name__ == '__main__' ):
    
    # Parse the command-line arguments
    option_dict = parse_arguments( OPTION_LIST )
    
    # Get the path to the file with parsed InterProScan results for query proteins
    query_interproscan_file_path = get_option( option_dict = option_dict,
                                               option_name = QUERY_INTERPROSCAN_FILE_PATH_OPTION,
                                               not_none = True )
    
    # Get the path to the file with InterPro annotated domains for target proteins
    target_domain_annotation_file_path = get_option( option_dict = option_dict,
                                                     option_name = TARGET_DOMAIN_ANNOTATION_FILE_PATH_OPTION,
                                                     not_none = True )
    
    # Get the path to file with parsed SLiMProb results for query proteins
    query_slimprob_file_path = get_option( option_dict = option_dict,
                                           option_name = QUERY_SLIMPROB_FILE_PATH_OPTION,
                                           not_none = True )
    
    # Get the path to the ELM - domain interactions file with InterPro accessions
    # (contains the pairs of ELM - domains interactions, i.e SLiM-domain 
    # interaction templates using ELM IDs and InterPro accessions)
    elm_domain_interactions_interpro_file_path = get_option( option_dict = option_dict,
                                                             option_name = ELM_DOMAIN_INTERACTIONS_INTERPRO_FILE_PATH_OPTION,
                                                             not_none = True )
    
    # Get the path to the file containing the interacting domains as InterPro
    # accessions (contains the pairs of interacting domains as InterPro
    # accessions)
    ddi_interpro_file_path = get_option( option_dict = option_dict,
                                         option_name = DDI_INTERPRO_FILE_PATH_OPTION,
                                         not_none = True )
    
    # Get the path to output file registering the SLiM-domain interactions
    output_slim_domain_interactions_file_path = get_option( option_dict = option_dict,
                                                            option_name = OUTPUT_SLIM_DOMAIN_INTERACTIONS_FILE_PATH_OPTION,
                                                            not_none = True )
     
    # Get the path to output file registering the domain-domain interactions
    output_domain_domain_interactions_file_path = get_option( option_dict = option_dict,
                                                              option_name = OUTPUT_DOMAIN_DOMAIN_INTERACTIONS_FILE_PATH_OPTION,
                                                              not_none = True )
    
    # Run the script
    print( datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S') + 
           ' :: INFO :: Starting the inference of the SLiM-domain and domain-domain interactions.' )
    try:
        interaction_inference( query_interproscan_file_path = query_interproscan_file_path,
                               target_domain_annotation_file_path = target_domain_annotation_file_path,
                               query_slimprob_file_path = query_slimprob_file_path,
                               elm_domain_interactions_interpro_file_path = elm_domain_interactions_interpro_file_path,
                               ddi_interpro_file_path = ddi_interpro_file_path,
                               output_slim_domain_interactions_file_path = output_slim_domain_interactions_file_path,
                               output_domain_domain_interactions_file_path = output_domain_domain_interactions_file_path )
    except Exception as e:
        exit( 'An exception has been raised during the execution of the script: \n' +
              str( e ) )
    else:
        print( datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S') + 
           ' :: INFO :: The inference of the SLiM-domain and domain-domain interactions has finished.' )
    