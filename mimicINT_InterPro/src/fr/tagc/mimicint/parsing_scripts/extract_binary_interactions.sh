#!/bin/bash

# This script allows to extract the binary interactions from
# the files of DDIs and DMIs

# Input files
# -----------
#
# The following files are expected to be provided:
# - File of DMIs
# - File of DDIs
#
# The file registering the SLiM-domain interactions is a tsv file
# that is expected to contain the following columns:
# [0] Slim_Protein_acc: String - The accession, name or ID of the query protein.
# [1] Slim_Motif: String - The ELM identifier of the motif.
# [2] Slim_Start: Integer - The relative start position of the motif.
# [3] Slim_End: Integer - The relative end position of the motif.
# [4] Slim_Description: String - The description of the motif.
# [5] Prot_Accession: String - The accession, name or ID of the target protein.
# [6] Domain_Prot_Accession: String - The InterPro accession of the domain.
# [7] Domain_Start: Integer - The relative start position of the domain.
# [8] Domain_End: Integer - The relative end position of the domain.
# [9] Domain_Fragmented: Boolean - Is the domain fragmented?
# [10] Domain_Name: String - The name of the domain.
# NB: This file contains a header.
#
# The file registering the domain-domain interactions is a tsv file
# that is expected to contain the following columns:
# [0] Prot_Accession1: String - The accession, name or ID of the query protein.
# [1] Domain_Prot_Accession1: String - The InterPro accession of the domain (on the query protein).
# [2] Domain_Start1: Integer - The relative start location of the domain (on the query protein).
# [3] Domain_End1: Integer - The relative end location of the domain (on the query protein).
# [4] Domain_Name1: String - The name of the domain (on the query protein).
# [5] Prot_Accession2: String - The accession, name or ID of the target protein.
# [6] Domain_Prot_Accession2: String - The InterPro accession of the domain (on the target protein).
# [7] Domain_Start2: Integer - The relative start location of the domain (on the target protein).
# [8] Domain_End2: Integer - The relative end location of the domain (on the target protein).
# [9] Domain_Fragmented2: Boolean - Is the domain fragmented (on the target protein)?
# [10] Domain_Name2: String - The name of the domain (on the target protein).
# NB: This file contains a header.


# Output files
# ------------
#
# The following files are generated
# - File of all unique DD and DM interactions
# - File of binary DMIs and DDIs
#
# The file containing the list of all inferred unique SLiM-domain
# and domain-domain interactions is a tsv file that contains 
# the following columns:
# [0] Query_Accession: String - The name, accession or ID of the query protein.
# [1] Target_Accession: String - The name, accession or ID of the target protein.
# [2] Interaction_Type: String - The type of interaction (either domain-domain or slim-domain).
# NB: This file contains a header.
#
# The file containing the list of binary inferred protein interactions
# is a ncol file that contains the following columns:
# [] Query_Accession: String - The name, accession or ID of the query protein.
# [1] Target_Accession: String - The name, accession or ID of the target protein.
# NB: This file does not contain any header (conform with the .ncol file format).


# ===============================================================================
# Parsing the command line arguments
# ===============================================================================

echo "DEBUG :: Arguments provided $@"

OPTIONS_LIST=(
  "dmi"
  "ddi"
  "all"
  "binary"
)

# Parse the options
opts=$(getopt \
    --longoptions "$(printf "%s:," "${OPTIONS_LIST[@]}")" \
    --name "$(basename "$0")" \
    --options "" \
    -- "$@"
)
eval set --$opts

while [[ $# -gt 0 ]]; do
    case "$1" in
        --dmi)
            dmi_file=$2
            shift 2
            ;;
            
        --ddi)
            ddi_file=$2
            shift 2
            ;;
            
        --all)
        	all_file=$2
            shift 2
            ;;
            
        --binary)
        	binary_file=$2
            shift 2
            ;;

        *)
            break
            ;;
    esac
done

printf "DEBUG :: Arguments parsed: \n\
        - dmi: $dmi_file \n\
        - ddi: $ddi_file \n\
        - all: $all_file \n\
        - binary: $binary_file \n"



# ===============================================================================
# Extract binary interactions
# ===============================================================================

cat \
  <( printf "Query_Accession\tTarget_Accession\tInteraction_Type\n" ) \
  <( awk 'BEGIN { FS = "\t"; OFS = "\t" }{ print $1,$6,"slim-domain" }' $dmi_file | tail -n+2 | sort -u) \
  <( awk 'BEGIN { FS = "\t"; OFS = "\t" }{ print $1,$6,"domain-domain" }' $ddi_file | tail -n+2 | sort -u) \
  > $all_file
  
cat \
  <( awk 'BEGIN { FS = "\t"; OFS = "\t" }{ print $1,$6 }' $dmi_file | tail -n+2 ) \
  <( awk 'BEGIN { FS = "\t"; OFS = "\t" }{ print $1,$6 }' $ddi_file | tail -n+2 ) \
  | sort -u \
  > $binary_file
