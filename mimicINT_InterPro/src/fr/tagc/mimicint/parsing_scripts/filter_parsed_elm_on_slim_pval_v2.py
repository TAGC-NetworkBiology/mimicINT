#!/usr/bin/python3
# -*- coding: utf-8 -*-


from fr.tagc.mimicint.util.option.OptionManager import *


# This script script allows to filter the SLiM based 
# on a cut-off on the p-value in the parsed ELM classes file.


# SLiM p-values
# -------------

# The file of SLiM p-values is expected to be computed by the mimicINT randomization 
# workflow (compute_slim_probability_v2 workflow) and to contain the following columns:
#
# [0] motif: String - The ELM identifier of the SLiM.
# [1] avg_p_value: Float - The average p-value.
# [2] fisher_p_value: Float - The average p-value.
# [3] list_of_empirical_pval: Float - The list of empirical p-values.
#
# For extensive details about the computation of the p-values, check the documentation
# of the compute_slim_probability_v2 workflow. 


# Parsed ELM classes
# ------------------

# The file of parsed ELM classes contains the following colums:
# [0] Accession
# [1] ELMIdentifier
# [2] FunctionalSiteName
# [3] Description
# [4] Regex
# [5] Probability
# [6] #Instances
# [7] #Instances_in_PDB


# ===========================================
# Constants
# ===========================================

# Indexes of columns in the SLiM p-values
SLIM_PVALUES_FILE_MOTIF_INDEX = 0
SLIM_PVALUES_FILE_FISHER_PVAL_INDEX = 2

# Indexes of columns in the parsed ELM classes file
MIMICINT_OUTPUT_PARSED_ELM_CLASSES_FILE_ELM_ID_INDEX = 1



# ===========================================
# Options
# ===========================================

# Options and default values
# --------------------------

# Cut-off to use for the SLiM p-values
DEFAULT_PVALUE_THRESHOLD = 0.05


# List of options allowed
# -----------------------

# Path to the file of SLiM p-values (input)
INPUT_SLIM_PVALUES_FILE_PATH_OPTION = 'INPUT_SLIM_PVALUES_FILE_PATH_OPTION'

# Path to the file of parsed ELM classes (input)
INPUT_PARSED_ELM_CLASSES_FILE_PATH_OPTION = 'INPUT_PARSED_ELM_CLASSES_FILE_PATH_OPTION'

# Path to the file of selected SLiMs (output)
OUTPUT_SELECTED_SLIM_FILE_PATH_OPTION = 'OUTPUT_SELECTED_SLIM_FILE_PATH_OPTION'

# Path to the file of filtered parsed ELM classes (output)
OUTPUT_PARSED_ELM_CLASSES_FILE_PATH_OPTION = 'OUTPUT_PARSED_ELM_CLASSES_FILE_PATH_OPTION'

# Cut-off to use for the SLiM p-values
PVALUE_THRESHOLD_OPTION = 'PVALUE_THRESHOLD_OPTION'


OPTION_LIST = [ [ '-p', '--slimPval', 'store', 'string', INPUT_SLIM_PVALUES_FILE_PATH_OPTION, None, 'The path to the file of SLiM p-values (input).' ],
                [ '-e', '--parsedELM', 'store', 'string', INPUT_PARSED_ELM_CLASSES_FILE_PATH_OPTION, None, 'The path to the file of parsed ELM classes (input).' ],
                [ '-s', '--selectedELM', 'store', 'string', OUTPUT_SELECTED_SLIM_FILE_PATH_OPTION, None, 'The path to the file of selected SLiMs (output).' ],
                [ '-f', '--filteredELM', 'store', 'string', OUTPUT_PARSED_ELM_CLASSES_FILE_PATH_OPTION, None, 'The path to the file of filtered parsed ELM classes (output).' ],
                [ '-c', '--cutoff', 'store', 'float', PVALUE_THRESHOLD_OPTION, DEFAULT_PVALUE_THRESHOLD, 
                  'The cut-off to use on the SLiM p-value [default: %default].']]



# ===========================================
# Methods
# ===========================================

## filter_parsed_elm_on_slim_pval
#  ------------------------------
#
# This script script allows to filter the SLiM based 
# on a cut-off on the p-value in the parsed ELM classes file.
#
# @param input_slim_pvalues_file_path: String - The path to the file containing the SLiM p-values.
# @param input_parsed_elm_classes_file_path: String - The path to the file containing the parsed ELM classes.
# @param output_selected_slim_file_path: String - The path to the file containing the list of selected SLiMs.
# @param output_parsed_elm_classes_file_path: String - The path to the file containing the filtered parsed ELM classes.
# @param pval_threshold: Float - The p-value cut-off.
# 
def filter_parsed_elm_on_slim_pval( input_slim_pvalues_file_path, input_parsed_elm_classes_file_path, \
                                    output_selected_slim_file_path, output_parsed_elm_classes_file_path,
                                    pval_threshold):
        
    # Parse the SLiM p-values file
    # ----------------------------
    
    # Instantiate a list that will register the SLiM with a p-value 
    # lower than the threshold
    selected_slims_set = set()
    
    # Parse the SLiM p-values file and register only the p-values under the cut-off
    with open( input_slim_pvalues_file_path, 'r') as input_slim_pvalues_file:
    
        # Skip header
        line = input_slim_pvalues_file.readline()
        line = input_slim_pvalues_file.readline()    
        
        while ( line != ''):
        
            line = line.replace( '\n', '')
            
            # Parse the line    
            splitted_line = line.split( '\t')
            motif_id = splitted_line[ SLIM_PVALUES_FILE_MOTIF_INDEX]
            motif_pval = float( splitted_line[ SLIM_PVALUES_FILE_FISHER_PVAL_INDEX])
            
            # Select only the motif with a p-value under the cut-off
            if ( motif_pval <= pval_threshold):
                selected_slims_set.add( motif_id)
            
            line = input_slim_pvalues_file.readline()
    
    
    # Save the filtered SLiMs
    # -----------------------
    
    with open( output_selected_slim_file_path, 'w') as output_slim_pvalues_file:
                
        for selected_slim in selected_slims_set:
        
            output_slim_pvalues_file.write( selected_slim + '\n')
                            
    
    # Filter the parsed ELM classes file
    # ----------------------------------
    
    with open( input_parsed_elm_classes_file_path, 'r') as input_parsed_elm_classes_file, \
         open( output_parsed_elm_classes_file_path, 'w') as output_parsed_elm_classes_file:
         
        # Copy header
        line = input_parsed_elm_classes_file.readline()
        output_parsed_elm_classes_file.write( line)
         
        line = input_parsed_elm_classes_file.readline()
        
        while ( line != ''):
            
            # Parse the line
            splitted_line = line.replace( '\n', '').split( '\t')
            elm_id = splitted_line[ MIMICINT_OUTPUT_PARSED_ELM_CLASSES_FILE_ELM_ID_INDEX].replace( '"', '')
            
            # If the SLiM has been selected, then register the interaction
            # and write the line in the output file if necessary
            if ( elm_id in selected_slims_set):
                output_parsed_elm_classes_file.write( line) 
                
            line = input_parsed_elm_classes_file.readline()
        
                

# ===========================================
# Parse arguments and run script
# ===========================================

if ( __name__ == '__main__'):
    
    # Parse the command-line arguments
    option_dict = parse_arguments( OPTION_LIST )
    
    
    # Get the path to the file of SLiM p-values (input)
    input_slim_pvalues_file_path = get_option( option_dict = option_dict, 
                                               option_name = INPUT_SLIM_PVALUES_FILE_PATH_OPTION, 
                                               not_none = True )
    
    # Get the path to the file of parsed ELM classes (input)
    input_parsed_elm_classes_file_path = get_option( option_dict = option_dict, 
                                                     option_name = INPUT_PARSED_ELM_CLASSES_FILE_PATH_OPTION, 
                                                     not_none = True )
    
    # Get the path to the file of selected SLiMs (output)
    output_selected_slim_file_path = get_option( option_dict = option_dict, 
                                                 option_name = OUTPUT_SELECTED_SLIM_FILE_PATH_OPTION, 
                                                 not_none = True )
    
    # Get the path to the file of filtered parsed ELM classes (output)
    output_parsed_elm_classes_file_path = get_option( option_dict = option_dict, 
                                                 option_name = OUTPUT_PARSED_ELM_CLASSES_FILE_PATH_OPTION, 
                                                 not_none = True )
    
    
    # Get the option values
    # ---------------------
        
    # Get the p-value threshold
    pval_threshold = option_dict.get( PVALUE_THRESHOLD_OPTION)
    
    if ( pval_threshold < 0):
        raise Exception( 'The p-value threshold must be a positive float.')
    
    # Run the script
    filter_parsed_elm_on_slim_pval( input_slim_pvalues_file_path = input_slim_pvalues_file_path,
                                    input_parsed_elm_classes_file_path = input_parsed_elm_classes_file_path,
                                    output_selected_slim_file_path = output_selected_slim_file_path,
                                    output_parsed_elm_classes_file_path = output_parsed_elm_classes_file_path,
                                    pval_threshold = pval_threshold)
    