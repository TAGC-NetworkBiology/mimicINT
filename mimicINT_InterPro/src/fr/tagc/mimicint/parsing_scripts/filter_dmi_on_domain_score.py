#!/usr/bin/python3
# -*- coding: utf-8 -*-


from fr.tagc.mimicint.util.option.OptionManager import *

# This script allows to filter the domain - motif interactions 
# based on on domain scores.


# Domain scores
# -------------

# The file of domain scores provides scores for the interactions between the domain
# of a target protein with the motifs of any query protein.
#
# The file of domain scores must be computed with an other workflow (developed by A. Zanzoni)
# and contains the following columns:
# [0] Domain_Query: String - The identifier of the target protein (fasta header) harboring the domain.
# [1] ELM_ID: String - The ELM identifier of the motif (query protein) interacting with the domain 
#                      of the target protein.
# [2] Domain_Target: String - The identifier of the gold standard protein (used for computing the score).
# [3] Domain_Score: Float - The domain score (NB: could be greater than 1).
# [4] HMM_Evalue: Float - The HMM e-value.
# [5] HMM_start: Integer - The position of the start of the Hidden Markov Motif.
# [6] HMM_end: Integer - The position of the end of the Hidden Markov Motif.
# [7] Domain_start: Integer - The position of the start of the domain on the target protein.
# [8] Domain_end: Integer - The position of the end of the domain on the target protein.
# [9] HMM_len: Integer - The length of the Hidden Markov Motif.
# [10] Percentage: Float - ?.
# [11] Annotated_Domain: Boolean - 'Yes' if the domain is annotated, i.e. if it is part of the gold standard set.
#                                  In such case, the identifier of the protein in the "Domain_Query" column must be
#                                  the same as the identifier of the protein in the "Domain_Target" protein.
#                                  'No' otherwise.


# Domain - motif interactions
# ---------------------------

# The file of domain - motif interactions generated by the rule interaction_inference.
# It is expected to contain the following columns:
# [0] Slim_Protein_acc: String - The query protein identifier.
# [1] Slim_Motif: String - The ELM identifier of the SLiM.
# [2] Slim_Start: Integer - The position of the start of the SLiM.
# [3] Slim_End: Integer - The position of the end of the SLiM.
# [4] Slim_Description: String - The description of the SLiM.
# [5] Prot_Accession: String - The accession of the target protein.
# [6] Domain_Prot_Accession: String - The identifier of the domain.
# [7] Domain_Start: Integer - The position of the start of the domain.
# [8] Domain_End: Integer - The position of the end of the domain.
# [9] Domain_Description: String - The description of the domain.



# Type of filters
# ---------------

# Two types of filters may be used:
# - A filter based on the annotation: Only interactions involving domains that are annotated are selected.
# - A filter based on the domain score: Only interactions involving domains with a score greater than a threshold are selected.

# An additional filter may be applied on the position. 
# Several instances of the same domain could exist on the same protein. If this filter is selected, the position
# of the domain will be considered in order to select only the domain for which the domain score has been computed
# as respect the filter as described above.
# Because the position of a given domain may slightly differs (notably due to difference between the InterPro version 
# used to generate the domain scores file and the one used in mimicINT), an overlap lower than 100 % may be accepted
# to select the interaction.



# ===========================================
# Constants
# ===========================================

# Indexes of columns in the domain score input file
DOMAIN_SCORE_FILE_DOMAIN_QUERY_INDEX = 0
DOMAIN_SCORE_FILE_ELM_ID_INDEX = 1
DOMAIN_SCORE_FILE_DOMAIN_SCORE_INDEX = 3
DOMAIN_SCORE_FILE_DOMAIN_START_INDEX = 7
DOMAIN_SCORE_FILE_DOMAIN_END_INDEX = 8
DOMAIN_SCORE_FILE_ANNOTATED_DOMAIN_INDEX = 11

# Values for the annotated domains
DOMAIN_SCORE_FILE_ANNOTATED_DOMAIN_YES = 'Yes'

# Indexes of columns in the domain - motif interactions file
DMI_FILE_QUERY_ELM_ID_INDEX = 1
DMI_FILE_TARGET_PROT_ID_INDEX = 5
DMI_FILE_TARGET_DOMAIN_START_POS_INDEX = 7
DMI_FILE_TARGET_DOMAIN_END_POS_INDEX = 8


# ===========================================
# Options
# ===========================================

# Options and default values
# --------------------------

# Type of filter
FILTER_TYPE_ANNOTATION = 'A'
FILTER_TYPE_DOMAIN_SCORE = 'D'
ALLOWED_FILTER_TYPES = [ FILTER_TYPE_ANNOTATION, FILTER_TYPE_DOMAIN_SCORE]
DEFAULT_FILTER_TYPE = FILTER_TYPE_ANNOTATION

# Domain score value
DEFAULT_DOMAIN_SCORE_VALUE = 0.4

# The minimal size of the overlap of the domain positions provided by the domain score file with
# the positions provided in the file of interactions, for the interaction to be selected
# (the coverage must be provided as a percentage)
DEFAULT_MIN_OVERLAP_POS_DSCORE_TO_DMI = 0.8

# The minimal size of the overlap of the domain positions provided by the file of interactions with
# the positions provided in the domain score file, for the interaction to be selected
# (the coverage must be provided as a percentage)
DEFAULT_MIN_OVERLAP_POS_DMI_TO_DSCORE = 0.8


# List of options allowed
# -----------------------

# Path to the domain score file (input)
INPUT_DOMAIN_SCORES_FILE_PATH_OPTION = 'INPUT_DOMAIN_SCORES_FILE_PATH_OPTION'

# Path to the domain - motif interactions (input)
INPUT_DMI_FILE_PATH_OPTION = 'INPUT_DMI_FILE_PATH_OPTION'

# Path to the filtered domain score file (output)
OUTPUT_DOMAIN_SCORES_FILE_PATH_OPTION = 'OUTPUT_DOMAIN_SCORES_FILE_PATH_OPTION'

# Path to the filtered domain - motif interactions (output)    
OUTPUT_DMI_FILE_PATH_OPTION = 'OUTPUT_DMI_FILE_PATH_OPTION'   

# Type of filter
FILTER_TYPE_OPTION = 'FILTER_TYPE_OPTION'

# Domain score value
DOMAIN_SCORE_VALUE_OPTION = 'DOMAIN_SCORE_VALUE_OPTION'

# Additional filter on position
ADDITIONAL_FILTER_POSITION_OPTION = 'ADDITIONAL_FILTER_POSITION_OPTION'

# The minimal size of the overlap of the domain positions provided by the domain score file with
# the positions provided in the file of interactions, for the interaction to be selected
# (the coverage must be provided as a percentage)
MIN_OVERLAP_POS_DSCORE_TO_DMI_OPTION = 'MIN_OVERLAP_POS_DSCORE_TO_DMI_OPTION'

# The minimal size of the overlap of the domain positions provided by the file of interactions with
# the positions provided in the domain score file, for the interaction to be selected
# (the coverage must be provided as a percentage)
MIN_OVERLAP_POS_DMI_TO_DSCORE_OPTION = 'MIN_OVERLAP_POS_DMI_TO_DSCORE_OPTION'


OPTION_LIST = [ [ '-d', '--dScore', 'store', 'string', INPUT_DOMAIN_SCORES_FILE_PATH_OPTION, None, 
                  'The path to the domain score file (input).'],
                [ '-i', '--dmi', 'store', 'string', INPUT_DMI_FILE_PATH_OPTION, None, 
                  'The path to the domain - motif interactions (input).'],
                [ '-D', '--filteredDscore', 'store', 'string', OUTPUT_DOMAIN_SCORES_FILE_PATH_OPTION, None, 
                  'The path to the filtered domain score file (output).'],
                [ '-I', '--filteredDmi', 'store', 'string', OUTPUT_DMI_FILE_PATH_OPTION, None, 
                  'The path to the filtered domain - motif interactions (output).'],
                [ '-f', '--filter', 'store', 'choice', FILTER_TYPE_OPTION, ALLOWED_FILTER_TYPES, DEFAULT_FILTER_TYPE, 
                  'The type of filter to use (must be one of ' + ', '.join( ALLOWED_FILTER_TYPES) + ') [default: %default].'],
                [ '-s', '--score', 'store', 'float', DOMAIN_SCORE_VALUE_OPTION, DEFAULT_DOMAIN_SCORE_VALUE, 
                  'The cut-off to use on the domain score (taken into account only when --filter option is set to "' + FILTER_TYPE_DOMAIN_SCORE + '") [default: %default].'],
                [ '-p', '--position', 'store_true', None, ADDITIONAL_FILTER_POSITION_OPTION, False, 
                  'Should the position of the domains be considered? [default: %default]'],
                [ '-o', '--overlap', 'store', 'float', MIN_OVERLAP_POS_DSCORE_TO_DMI_OPTION, DEFAULT_MIN_OVERLAP_POS_DSCORE_TO_DMI, 
                  'The minimal size of the overlap of the domain positions provided by the domain score file with ' +
                  ' the positions provided in the file of interactions, for the interaction to be selected' +
                  ' (the coverage must be provided as a percentage) [default: %default].'],
                [ '-O', '--Overlap', 'store', 'float', MIN_OVERLAP_POS_DMI_TO_DSCORE_OPTION, DEFAULT_MIN_OVERLAP_POS_DMI_TO_DSCORE, 
                  'The minimal size of the overlap of the domain positions provided by the file of interactions with ' +
                  ' the positions provided in the domain score file, for the interaction to be selected' +
                  ' (the coverage must be provided as a percentage) [default: %default].']]



# ===========================================
# Methods
# ===========================================

## filter_on_domain_score
#  ----------------------
#
# This script allows to filter (on domain scores) the domain - motif 
# interactions predicted by mimicINT.
# See documentation above for extensive information.
#
# @param input_domain_scores_file_path: String - The path to the input domain scores file.
# @param input_dmi_file_path: String - The path to the input domain - motif interactions file
#                                      (mimicINT output).
# @param output_domain_scores_file_path: String - The path to the output filtered domain scores file.
# @param output_dmi_file_path: String - The path to the output filtered domain - motif interactions file.
# @param filter_type: String - The type of filter to use. Either 'A' or 'D'.
# @param domain_score_value: Float - The domain score threshold to use.
# @param add_filter_on_pos: Boolean - Should the domain position be used to filter the interactions?
# @param min_overlap_pos_dscore_to_dmi: Float - The minimal size of the overlap of the domain positions provided by 
#                                               the domain score file with the positions provided in the file of interactions,
#                                               for the interaction to be selected (the coverage must be provided as a percentage).
# @param min_overlap_pos_dmi_to_dscore: Float - The minimal size of the overlap of the domain positions provided by the file of 
#                                               interactions with the positions provided in the domain score file, for the interaction
#                                               to be selected (the coverage must be provided as a percentage).
# 
def filter_on_domain_score( input_domain_scores_file_path, input_dmi_file_path, \
                            output_domain_scores_file_path, output_dmi_file_path, \
                            filter_type, domain_score_value, add_filter_on_pos, \
                            min_overlap_pos_dscore_to_dmi, min_overlap_pos_dmi_to_dscore):
                            
    # Parse the domain score file
    # ---------------------------
    
    # Instantiate a dictionary that will register the domain scores using the following structure:
    # {
    #   ( target_id <string>, elm_id <string>): [
    #                                               ( domain_start <int>, domain_end <int>),
    #                                               ...
    #                                           ]
    #   ...
    # }
    domain_score_dict = {}
    
    # Parse the domain score file and register only the domains that match the filter
    with open( input_domain_scores_file_path, 'r') as input_domain_scores_file:
    
        # Skip header
        line = input_domain_scores_file.readline()
        line = input_domain_scores_file.readline()
        
        while ( line != ''):
        
            line = line.replace( '\n', '')
            
            # Parse the line        
            splitted_line = line.split( '\t')
            target_id = splitted_line[ DOMAIN_SCORE_FILE_DOMAIN_QUERY_INDEX]
            elm_id = splitted_line[ DOMAIN_SCORE_FILE_ELM_ID_INDEX]
            domain_score = float( splitted_line[ DOMAIN_SCORE_FILE_DOMAIN_SCORE_INDEX])
            domain_start = int( splitted_line[ DOMAIN_SCORE_FILE_DOMAIN_START_INDEX])
            domain_end = int( splitted_line[ DOMAIN_SCORE_FILE_DOMAIN_END_INDEX])
            annotated_domain = splitted_line[ DOMAIN_SCORE_FILE_ANNOTATED_DOMAIN_INDEX]
            
            # Parse the target ID
            # The ID looks like "sp|O00213|APBB1_HUMAN" in the domain scores file
            target_id = target_id.split( '|')[1]
            
            
            # Apply the filter based on the annotation or the domain score
            register_entry = False
            
            if ( filter_type == FILTER_TYPE_ANNOTATION):
                if ( annotated_domain == DOMAIN_SCORE_FILE_ANNOTATED_DOMAIN_YES):
                    register_entry = True
            
            elif ( filter_type == FILTER_TYPE_DOMAIN_SCORE):
                if ( domain_score >= domain_score_value):
                    register_entry = True
            
            else:
                raise Exception( 'filter_on_domain_score(): The filter type provided (' + filter_type + ') is not allowed.')
                
            # Register the entry if necessary
            if register_entry:
            
                domain_score_dict_entry = domain_score_dict.get( ( target_id, elm_id))
                
                if ( not domain_score_dict_entry):
                    domain_score_dict[ ( target_id, elm_id)] = set()
                    
                domain_score_dict[ ( target_id, elm_id)].add( (domain_start, domain_end))
            
            del register_entry
            
            line = input_domain_scores_file.readline()
    
    
    # Save the filtered domain score file
    # -----------------------------------
    
    with open( output_domain_scores_file_path, 'w') as output_domain_scores_file:
    
        # Write header
        output_domain_scores_file.write( '\t'. join( [ 'target_id', 'elm_id', 'domain_start', 'domain_end']) + '\n')
        
        for ( ids, pos_set) in domain_score_dict.items():
        
            ( target_id, elm_id) = ids
            
            for positions in pos_set:
                
                ( domain_start, domain_end) = positions
            
                output_domain_scores_file.write( '\t'. join( [ target_id, elm_id, str( domain_start), str( domain_end)]) + '\n')
    
    
    # Filter the domain - motif interactions file
    # -------------------------------------------
    
    with open( input_dmi_file_path, 'r') as input_dmi_file, \
         open( output_dmi_file_path, 'w') as output_dmi_file:
         
        # Copy header
        line = input_dmi_file.readline()
        output_dmi_file.write( line)
         
        line = input_dmi_file.readline()
        
        while ( line != ''):
            
            # Parse the line
            splitted_line = line.replace( '\n', '').split( '\t')
            query_elm_id = splitted_line[ DMI_FILE_QUERY_ELM_ID_INDEX]
            target_prot_id = splitted_line[ DMI_FILE_TARGET_PROT_ID_INDEX]
            target_domain_start = int( splitted_line[ DMI_FILE_TARGET_DOMAIN_START_POS_INDEX])
            target_domain_end = int( splitted_line[ DMI_FILE_TARGET_DOMAIN_END_POS_INDEX])
            
            # If the target protein - ELM couple has been selected,
            # then eventually register the interactions (depending on other filters)
            domain_positions_set = domain_score_dict.get( (target_prot_id, query_elm_id))
    
            register_interaction = False
            
            if domain_positions_set:
                
                # If required, apply the filter based on the domain position
                if add_filter_on_pos:
                
                    # Check if the domain position is close to one of the positions
                    # from the domain scores file
                    k = 0
                    domain_positions_list = list( domain_positions_set)
                    while ( ( not register_interaction) and ( k < len( domain_positions_list))):
                       
                        domain_positions = domain_positions_list[ k]
                    
                        ( domain_start, domain_end) = domain_positions
                                                
                        # Check the overlap between the domain position 
                        # and the positions provided by the domain scores file
                        
                        # Get the length of the domains (according to the positions)
                        domain_len = domain_end - domain_start + 1
                        target_domain_len = target_domain_end - target_domain_start + 1
                        
                        # Get the value of the overlap in residues
                        # First case:
                        # domain:        -------[==========]---------------------------
                        # target_domain: -------------------------[==========]---------
                        if ( domain_end <= target_domain_start):
                            overlap = 0
                            
                        # Second case:
                        # domain:        -------------------------[==========]---------
                        # target_domain: -------[==========]---------------------------
                        elif ( domain_start >= target_domain_end):
                            overlap = 0
                            
                        # Third case:
                        # domain:        -------[========================]-------------
                        # target_domain: -------------[==========]---------------------
                        elif ( ( domain_start <= target_domain_start)
                               and ( domain_end >= target_domain_end)):
                            overlap = domain_len
                        
                        # Fourth case:
                        # domain:        -------------[==========]---------------------
                        # target_domain: -------[========================]-------------
                        elif ( ( domain_start >= target_domain_start) 
                               and ( domain_end <= target_domain_end)):
                            overlap = target_domain_len
                        
                        # Fifth case:
                        # domain:        -------------[==========]---------------------
                        # target_domain: -------------------[==============]-----------
                        elif ( ( domain_start <= target_domain_start)
                               and ( domain_end <= target_domain_end)):
                            overlap = domain_end - target_domain_start + 1
                        
                        # Sixth case:
                        # domain:        -------------------[==============]-----------
                        # target_domain: -------------[==========]---------------------
                        elif ( ( domain_start >= target_domain_start )
                               and ( domain_end >= target_domain_end)):
                            overlap = target_domain_end - domain_start + 1
                        
                        # Any other case encountered would mean there is a bug!
                        else:
                            raise Exception( 'Critical error: A case has been omitted for the computation of the overlap!' +
                                             ' (domain positions: ' + str( domain_start) + ':' + str( domain_end) + 
                                             ', domain target positions: ' + str( target_domain_start) + ':' + str( target_domain_end) + ').')
                        
                        # Compute the overlap as percentages
                        domain_overlap_percent = overlap / domain_len
                        target_domain_overlap_percent = overlap / target_domain_len
                        
                        # If the overlap is greater or equal to the one provided, 
                        # then the interaction is selected
                        if ( ( domain_overlap_percent >= min_overlap_pos_dscore_to_dmi)
                             and ( target_domain_overlap_percent >= min_overlap_pos_dmi_to_dscore)):
                            register_interaction = True
                       
                        k += 1
                
                # Otherwise register the interaction
                else:
                    register_interaction = True
        
            # Write the line in the output file if necessary
            if register_interaction:
                output_dmi_file.write( line) 
                
            line = input_dmi_file.readline()
        
                

# ===========================================
# Parse arguments and run script
# ===========================================

if ( __name__ == '__main__'):
    
    # Parse the command-line arguments
    option_dict = parse_arguments( OPTION_LIST)
    
    
    # Get the path to the domain score file (input)
    input_domain_scores_file_path = get_option( option_dict = option_dict, 
                                                option_name = INPUT_DOMAIN_SCORES_FILE_PATH_OPTION, 
                                                not_none = True)
    
    # Get the path to the domain - motif interactions (input)
    input_dmi_file_path = get_option( option_dict = option_dict, 
                                      option_name = INPUT_DMI_FILE_PATH_OPTION, 
                                      not_none = True)
    
    # Get the path to the filtered domain score file (output)
    output_domain_scores_file_path = get_option( option_dict = option_dict, 
                                                 option_name = OUTPUT_DOMAIN_SCORES_FILE_PATH_OPTION, 
                                                 not_none = True)
    
    # Get the path to the filtered domain - motif interactions (output)
    output_dmi_file_path = get_option( option_dict = option_dict,
                                       option_name = OUTPUT_DMI_FILE_PATH_OPTION, 
                                       not_none = True)


    # Get the option values
    # ---------------------
        
    # Type of filter
    filter_type = option_dict.get( FILTER_TYPE_OPTION)
                  
    # Domain score value
    domain_score_value = option_dict.get( DOMAIN_SCORE_VALUE_OPTION)
                  
    # Additional filter on position
    add_filter_on_pos = option_dict.get( ADDITIONAL_FILTER_POSITION_OPTION)
    
    # The minimal size of the overlap of the domain positions provided by the domain score file with
    # the positions provided in the file of interactions, for the interaction to be selected
    # (the coverage must be provided as a percentage)
    min_overlap_pos_dscore_to_dmi = option_dict.get( MIN_OVERLAP_POS_DSCORE_TO_DMI_OPTION)

    if ( ( min_overlap_pos_dscore_to_dmi < 0) 
         or ( min_overlap_pos_dscore_to_dmi > 1)):
        raise Exception( 'The overlap size must be provided as a percentage between 0 and 1.')
    

    # The minimal size of the overlap of the domain positions provided by the file of interactions with
    # the positions provided in the domain score file, for the interaction to be selected
    # (the coverage must be provided as a percentage)
    min_overlap_pos_dmi_to_dscore = option_dict.get( MIN_OVERLAP_POS_DMI_TO_DSCORE_OPTION)

    if ( ( min_overlap_pos_dmi_to_dscore < 0) 
         or ( min_overlap_pos_dmi_to_dscore > 1)):
        raise Exception( 'The overlap size must be provided as a percentage between 0 and 1.')
    
    # Run the script
    filter_on_domain_score( input_domain_scores_file_path = input_domain_scores_file_path,
                            input_dmi_file_path = input_dmi_file_path,
                            output_domain_scores_file_path = output_domain_scores_file_path,
                            output_dmi_file_path = output_dmi_file_path,
                            filter_type = filter_type,
                            domain_score_value = domain_score_value,
                            add_filter_on_pos = add_filter_on_pos,
                            min_overlap_pos_dscore_to_dmi = min_overlap_pos_dscore_to_dmi,
                            min_overlap_pos_dmi_to_dscore = min_overlap_pos_dmi_to_dscore)
                            