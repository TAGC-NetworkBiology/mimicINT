#!/usr/bin/python3
# -*- coding: utf-8 -*-
# 2018/05/15 -- AZ

########## Parser for 3did file ##########

#### Import modules ####
import sys

from fr.tagc.mimicint.util.option.OptionManager import *


# ===========================================
# Constants
# ===========================================

# List of options allowed
# -----------------------
# Path to the 3did_flat file downloaded from the 3did website
THREE_DID_FILE_OPTION = "THREE_DID_FILE"
# Path to the file containing the parsed pairs of interacting domains (i.e, domain-domain interaction templates)
PARSED_DID_FILE_OPTION = "PARSED_DID_FILE"

OPTION_LIST = [ [ "-i", "--input", "store", "string", THREE_DID_FILE_OPTION, None, "The path to the 3did_flat file downloaded from the 3did website." ],
                [ "-o", "--output", "store", "string", PARSED_DID_FILE_OPTION, None, "The path to the file containing the parsed pairs of interacting domains (i.e, domain-domain interaction templates)." ] ]



# ===========================================
# Script
# ===========================================

#### Parser definition ####
def parse_3did(did_input,did_output) :
    
    '''
    did_input : 3did_flat file downloaded from the 3did website
    
    did_output : path to the file containing the parsed pairs of interacting domains (i.e, domain-domain interaction templates).

    
    With these files, parse3did create a tsv file reporting the Pfam identifiers and labels of domain-domain interaction templates.
    '''
    
    TAG_3DID_DEFINITION = '#=ID'
    
    #### Opening files and variables definition ####
    fic3didInput = open( did_input,"r") # file with the 3did dataset
    set3did = set() # interacting domain pairs are stored here prior writing. Getting rid of potential duplicate entries
    fic3didOutput = open( did_output,"w") # results file

    #### Reading the 3did data file #### 
    line = None
    while line != '' :
        line=fic3didInput.readline() # reading file while there is not an empty line
        if line.startswith( TAG_3DID_DEFINITION) : # takes into account only lines corresponding to an interacting domain pair
            #print (line)
            line = line.split( "\t") # line became a list
            label_domain1 =line[1]
            label_domain2 = line[2]
            acc_domain1 = line[3].split('.')[0].replace('(','').strip() # remove all extra characters from domain1 accession: (PF10417.2@Pfam ==> PF10417
            acc_domain2 = line[4].split('.')[0] # remove all extra characters from domain2 accession: PF00578.14@Pfam) ==> PF00578
            
            #sort interacting domain accession strings to avoid duplicates
            if acc_domain1 < acc_domain2:
                interacting_pair = acc_domain1 + "\t" + acc_domain2 + "\t" + label_domain1 + "\t" + label_domain2
            else:
                interacting_pair = acc_domain2 + "\t" + acc_domain1 + "\t" + label_domain2 + "\t" + label_domain1
            #print (interacting_pair)
            set3did.add(interacting_pair) #add the interacting domain pair string to the set
    
    print( "Pfam_acc_1" + "\t" + "Pfam_acc_2" + "\t" + "Pfam_label_1" + "\t" + "Pfam_label_2", file=fic3didOutput)
    for domain_pair in set3did:
        print( domain_pair,file=fic3didOutput)
            
    #### Closing the files ####
    fic3didInput.close()
    fic3didOutput.close()



# ===========================================
# Parse command line arguments 
# and run script
# ===========================================

#### Code execution in the console ####
if __name__ == "__main__":
    
    # Parse the command-line arguments
    option_dict = parse_arguments( OPTION_LIST )
    
    # Get the path to the 3did_flat file downloaded from the 3did website
    did_input = get_option( option_dict = option_dict,
                            option_name = THREE_DID_FILE_OPTION,
                            not_none = True )
    
    # Get the path to the file containing the parsed pairs of interacting domains (i.e, domain-domain interaction templates)
    did_output = get_option( option_dict = option_dict,
                             option_name = PARSED_DID_FILE_OPTION,
                             not_none = True )
    
    parse_3did( did_input = did_input,
                did_output = did_output )
        