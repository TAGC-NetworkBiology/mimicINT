#!/usr/bin/python3
# -*- coding: utf-8 -*-


from fr.tagc.mimicint.util.option.OptionManager import *


# This script allows to get the list of target proteins having
# at least one domain (i.e. with at least one InterPro entry)
# and for which interactions can be theoretically computed 
# (i.e. these InterPro have interactors in the DDI and/or DMI templates)


# Description of the input files
# ------------------------------

# The file with InterPro annotated domains for target proteins 
# is a tsv file that contains the following columns:
# - [0] UniProtKB_accession: String - The protein accession in UniProtKB.
# - [1] name: String - The name of the protein.
# - [2] length: Integer - The length of the protein.
# - [3] InterPro_accession: String - The InterPro accession.
# - [4] entry_type: String - The type of InterPro entry (homologous superfamily, protein family, 
#                            domain or repeat).
#                            See https://www.ebi.ac.uk/training/online/courses/interpro-functional-and-structural-analysis/what-is-an-interpro-entry/interpro-entry-types/ 
#                            for more information about the entry types.
# - [5] start: Integer - The start position of the entry on the protein. 
#                        If the entry is fragmented, this position corresponds to 
#                        the lowest value of all start positions.
# - [6] end: Integer - The end position of the entry on the protein.
#                      If the entry is fragmented, this position corresponds to 
#                      the highest value of all start positions.
# - [7] fragmented: Boolean - Is the entry fragmented?
# NB: This file contains a header.
#
#
# The DDI templates (InterPro accessions) file is expected to be a tsv file 
# and to contain the following columns:
# - [0] InterPro_acc_1: String - The InterPro accession of the first domain.
# - [1] InterPro_acc_2: String - The InterPro accession of the second domain.
# - [2] InterPro_name_1: String - The name of the first domain (in Pfam).
# - [3] InterPro_name_2: String - The name of the second domain (in Pfam).
# NB: This file contains a header.
#
#
# DMI templates (InterPro accessions) file file is expected to be a tsv file 
# and to contain the following columns:
# - [0] ELM_id: String - The ELM identifier.
# - [1] domain_InterPro: String - The InterPro accession.
# - [2] domain_desc: String - The description of the domain (as provided in the input
#                             ELM - domain interaction file).
# - [3] domain_name: String - The name of the domain (as registered in Pfam).
# NB: This file contains a header.


# Description of the output file
# ------------------------------

# The output file contains the list of target proteins harboring at least
# one InterPro accession and for which interactions can be theoretically 
# computed, as these InterPro can be interfaces of interactions according
# to the DDI and/or DMI templates.
# - [0] UniProtKB_accession: String - the target protein identifier.
# NB: This file does not contain any header.



# ===========================================
# Constants
# ===========================================

# Indexes of columns in the file with InterPro annotated domains for target proteins
UNIPROTKB_ACC_TARGET_PROT_DOMAINS_FILE_INDEX = 0
INTERPRO_ACC_TARGET_PROT_DOMAINS_FILE_INDEX = 3

# Indexes of columns in the file of DDI templates
INTERPRO_ACC_1_DDI_TEMPLATE_FILE_INDEX = 0
INTERPRO_ACC_2_DDI_TEMPLATE_FILE_INDEX = 1

# Indexes of columns in the file of DMI templates
INTERPRO_ACC_DMI_TEMPLATE_FILE_INDEX = 1


# ===========================================
# Options
# ===========================================

# List of options allowed
# -----------------------

# Path to the file with InterPro annotated domains for target proteins (input)
INPUT_TARGET_PROT_DOMAINS_FILE_OPTION = 'INPUT_TARGET_PROT_DOMAINS_FILE_OPTION'

# Path to the file of DDI templates (input)
INPUT_DDI_TEMPLATE_FILE_OPTION = 'INPUT_DDI_TEMPLATE_FILE_OPTION'

# Path to the file of DMI templates (input)
INPUT_DMI_TEMPLATE_FILE_OPTION = 'INPUT_DMI_TEMPLATE_FILE_OPTION'

# Path to the file of target for which interactors can be predicted (output)
OUTPUT_TARGET_PROT_LIST_FILE_OPTION = 'OUTPUT_TARGET_PROT_LIST_FILE_OPTION'

OPTION_LIST = [ [ '-t', '--targetDom', 'store', 'string', INPUT_TARGET_PROT_DOMAINS_FILE_OPTION, None, 
                  'The path to the file with InterPro annotated domains for target proteins (input).'],
                [ '-d', '--ddi', 'store', 'string', INPUT_DDI_TEMPLATE_FILE_OPTION, None, 
                  'The path to the file of DDI templates (input).'],
                [ '-m', '--dmi', 'store', 'string', INPUT_DMI_TEMPLATE_FILE_OPTION, None, 
                  'The path to the file of DMI templates (input).'],
                [ '-o', '--output', 'store', 'string', OUTPUT_TARGET_PROT_LIST_FILE_OPTION, None, 
                  'The path to the file of target for which interactors can be predicted (output).'],]



# ===========================================
# Methods
# ===========================================

## get_target_prot_with_potential_interactions
#  -------------------------------------------
#
# This method allows to get the list of target proteins having
# at least one domain (i.e. with at least one InterPro entry)
# and for which interactions can be theoretically computed 
# (i.e. these InterPro have interactors in the DDI and/or DMI templates)
#
# @param input_target_prot_domains_file_path: String - The path to the file with InterPro annotated domains 
#                                                      for target proteins (input).
# @param input_ddi_templates_file_path: String - The path to the file of DDI templates (input).
# @param input_dmi_template_file_path: String - The path to the the file of DMI templates (input).
# @param output_target_prot_list_file_path: String - The path to the file of target for which interactors 
#                                                    can be predicted (output).
# 
def get_target_prot_with_potential_interactions( input_target_prot_domains_file_path, input_ddi_templates_file_path,\
                                                 input_dmi_template_file_path, output_target_prot_list_file_path):
    
    # Instantiate a set that will register all domains involved in 
    # at least one template of interactions (either DDI or DMI)
    domains_with_interactions_set = set()
            
                            
    # Parse the file of DDI templates
    # -------------------------------
    with open( input_ddi_templates_file_path, 'r') as input_ddi_templates_file:
        
        # Skip headers
        line = input_ddi_templates_file.readline()
        line = input_ddi_templates_file.readline()
        
        while ( line != ''):
            
            splitted_line = line.split( '\t')
            
            interpro_acc_1 = splitted_line[ INTERPRO_ACC_1_DDI_TEMPLATE_FILE_INDEX]
            interpro_acc_2 = splitted_line[ INTERPRO_ACC_2_DDI_TEMPLATE_FILE_INDEX]
            
            domains_with_interactions_set.add( interpro_acc_1)
            domains_with_interactions_set.add( interpro_acc_2)
            
            line = input_ddi_templates_file.readline()
            
                            
    # Parse the file of DMI templates
    # -------------------------------
    with open( input_dmi_template_file_path, 'r') as input_dmi_template_file:
        
        # Skip headers
        line = input_dmi_template_file.readline()
        line = input_dmi_template_file.readline()
        
        while ( line != ''):
            
            splitted_line = line.split( '\t')
            
            interpro_acc = splitted_line[ INTERPRO_ACC_DMI_TEMPLATE_FILE_INDEX]
            
            domains_with_interactions_set.add( interpro_acc)
            
            line = input_dmi_template_file.readline()
    
                            
    # Parse the file of target domains
    # --------------------------------
    
    # Instantiate a set that will register all target proteins harboring a domain
    # able to mediate at least one interaction
    target_with_dom_able_to_interact_set = set()

    with open( input_target_prot_domains_file_path, 'r') as input_target_prot_domains_file:
        
        # Skip header
        line = input_target_prot_domains_file.readline()
        line = input_target_prot_domains_file.readline()
        
        while ( line != ''):
            
            splitted_line = line.split( '\t')
            uniprot_acc = splitted_line[ UNIPROTKB_ACC_TARGET_PROT_DOMAINS_FILE_INDEX]
            interpro_acc = splitted_line[ INTERPRO_ACC_TARGET_PROT_DOMAINS_FILE_INDEX]
            
            if ( interpro_acc in domains_with_interactions_set):
                target_with_dom_able_to_interact_set.add( uniprot_acc)
            
            line = input_target_prot_domains_file.readline()
    
                            
    # Register the list of target proteins with potential interactions
    # ----------------------------------------------------------------
    
    with open( output_target_prot_list_file_path, 'w') as output_target_prot_list_file:
        
        for target_prot in target_with_dom_able_to_interact_set:
            
            output_target_prot_list_file.write( target_prot + '\n')

                

# ===========================================
# Parse arguments and run script
# ===========================================

if ( __name__ == '__main__'):
    
    # Parse the command-line arguments
    option_dict = parse_arguments( OPTION_LIST)
    
    
    # Get the path to the file with InterPro annotated domains for target proteins (input)
    input_target_prot_domains_file_path = get_option( option_dict = option_dict, 
                                                      option_name = INPUT_TARGET_PROT_DOMAINS_FILE_OPTION, 
                                                      not_none = True)

    # Get the path to the file of DDI templates (input)
    input_ddi_templates_file_path = get_option( option_dict = option_dict, 
                                                option_name = INPUT_DDI_TEMPLATE_FILE_OPTION, 
                                                not_none = True)

    # Get the path to the file of DMI templates (input)
    input_dmi_template_file_path = get_option( option_dict = option_dict, 
                                               option_name = INPUT_DMI_TEMPLATE_FILE_OPTION, 
                                               not_none = True)

    # Get the path to the file of target for which interactors can be predicted (output)
    output_target_prot_list_file_path = get_option( option_dict = option_dict, 
                                                    option_name = OUTPUT_TARGET_PROT_LIST_FILE_OPTION, 
                                                    not_none = True)
    
    # Run the script
    get_target_prot_with_potential_interactions( input_target_prot_domains_file_path = input_target_prot_domains_file_path,
                                                 input_ddi_templates_file_path = input_ddi_templates_file_path,
                                                 input_dmi_template_file_path = input_dmi_template_file_path,
                                                 output_target_prot_list_file_path = output_target_prot_list_file_path)
    