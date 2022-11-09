#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import json


import fr.tagc.mimicint.parsing_scripts.interaction_all_to_json as interaction_all_to_json
from fr.tagc.mimicint.util.option.OptionManager import *

# This script allows to generate short sequence names from 
# the fasta headers.

# NB: In order to work, it expects the fasta headers to be
#     provided as a three-coma-separated entry using UniProt
#     conventions.


# ===========================================
# Constants
# ===========================================

# Index of the columns of the SLiMProb matching sequence names file
SLIMPROB_MATCH_NAMES_SLIMPROB_SEQNAME_INDEX = 0
SLIMPROB_MATCH_NAMES_FASTA_SEQNAME_INDEX = 1

# Index of the columns of the InterProScan parsed files
PARSED_DOMAIN_SEQUENCE_INDEX = 0

# Index of the columns of the SLiMProb occurrence file
PARSED_SLIMRPOB_OCC_SEQUENCE_INDEX = 0

# Index of the columns of the query disorder propensities file
QUERY_DISORDER_PROP_SEQUENCE_INDEX = 0

# Index of the columns of the domain-domain interactions file
DDI_QUERY_SEQUENCE_INDEX = 0
DDI_TARGET_SEQUENCE_INDEX = 5

# Index of the columns of the domain-motif interactions file
DMI_QUERY_SEQUENCE_INDEX = 0
DMI_TARGET_SEQUENCE_INDEX = 5

# Index of the columns of the file containing all the interactions
ALL_INTER_QUERY_SEQUENCE_INDEX = 0
ALL_INTER_TARGET_SEQUENCE_INDEX = 1

# Index of the columns of the file containing the binary interactions
BINARY_INTER_QUERY_SEQUENCE_INDEX = 0
BINARY_INTER_TARGET_SEQUENCE_INDEX = 1

# Sequence identifiers used in dictionaries
FULL_FASTA_SEQNAME = 'FULL_HEADER'
SEQNAME = 'SEQNAME'
IPS_SEQNAME = 'IPS_SEQNAME'
SLIMPROB_SEQNAME = 'SLIMPROB_SEQNAME'


# List of options allowed
# -----------------------
# Path to the query fasta file
QUERY_FATA_FILE_OPTION = 'QUERY_FASTA_FILE'

# Path to the files where correspondences between query sequences 
# names provided by the fasta and used by SLiMProb are registered
QUERY_SQCE_NAMES_MATCH_FILE_OPTION = 'QUERY_SQCE_NAMES_MATCH_FILE'

# Path to the files where correspondences between sequence names are registered
SQCE_NAMES_MATCH_FILE_OPTION = 'SQCE_NAMES_MATCH_FILE'

# Path to the file containing annotated domains in target
TARGET_DOMAIN_ANNOTATIONS_FILE_OPTION = 'TARGET_DOMAIN_ANNOTATIONS_FILE'

# Path to the parsed query domain file
PARSED_QUERY_DOMAIN_FILE_OPTION = 'PARSED_QUERY_DOMAIN_FILE'

# Path to the parsed query domain file with sequences renamed
PARSED_QUERY_DOMAIN_RENAMED_SQCES_FILE_OPTION = 'PARSED_QUERY_DOMAIN_RENAMED_SQCES_FILE'

# Path to the parsed SLiMProb occurrences file
PARSED_SLIMPROB_OCC_FILE_OPTION = 'PARSED_SLIMPROB_OCC_FILE_OPTION'

# Path to the parsed SLiMProb occurrences file with sequences renamed
PARSED_SLIMPROB_OCC_RENAMED_SQCES_FILE_OPTION = 'PARSED_SLIMPROB_OCC_RENAMED_SQCES_FILE'

# Path to the file of disorder propensities
QUERY_DISORDER_PROP_FILE_OPTION = 'QUERY_DISORDER_PROP_FILE'

# Path to the file of disorder propensities with sequences renamed
QUERY_DISORDER_PROP_RENAMED_SQCES_FILE_OPTION = 'QUERY_DISORDER_PROP_RENAMED_SQCES_FILE'

# Path to the domain-domain interactions file
DDI_FILE_OPTION = 'DDI_FILE'

# Path to the domain-domain interactions file with sequences renamed
DDI_FILE_RENAMED_SQCES_FILE_OPTION = 'DDI_FILE_RENAMED_SQCES_FILE'

# Path to the domain-motif interactions file
DMI_FILE_OPTION = 'DMI_FILE'

# Path to the domain-motif interactions file with sequences renamed
DMI_FILE_RENAMED_SQCES_FILE_OPTION = 'DMI_FILE_RENAMED_SQCES_FILE'

# Path to all interactions file
ALL_INTERACTIONS_FILE_OPTION = 'ALL_INTERACTIONS_FILE'

# Path to all interactions file with sequences renamed
ALL_INTERACTIONS_FILE_RENAMED_SQCES_FILE_OPTION = 'ALL_INTERACTIONS_FILE_RENAMED_SQCES_FILE'

# Path to binary interactions file
BINARY_INTERACTIONS_FILE_OPTION = 'BINARY_INTERACTIONS_FILE'

# Path to binary interactions with sequences renamed
BINARY_INTERACTIONS_RENAMED_SQCES_FILE_OPTION = 'BINARY_INTERACTIONS_RENAMED_SQCES_FILE'

# Path to the JSON file with all interactions with sequences renamed
ALL_INTERACTIONS_JSON_RENAMED_SQCES_FILE_OPTION = 'ALL_INTERACTIONS_JSON_RENAMED_SQCES_FILE'

# Path to the JSON file with query features
QUERY_FEATURES_JSON_FILE_OPTION = 'QUERY_FEATURES_JSON_FILE'

# Path to the JSON file with query features with sequences renamed
QUERY_FEATURES_JSON_RENAMED_SQCES_FILE_OPTION = 'QUERY_FEATURES_JSON_RENAMED_SQCES_FILE'


OPTION_LIST = [ [ '-b', '--queryFasta', 'store', 'string', QUERY_FATA_FILE_OPTION, None, 'Path to the query fasta file.' ],
                [ '-c', '--queryMatch', 'store', 'string', QUERY_SQCE_NAMES_MATCH_FILE_OPTION, None, 'Path to the files where correspondences between query sequences names provided by the fasta and used by SLiMProb are registered.' ],
                [ '-d', '--targetDomain', 'store', 'string', TARGET_DOMAIN_ANNOTATIONS_FILE_OPTION, None, 'Path to the file containing all the annotated domains in the target sequences.' ],
                [ '-e', '--queryDomain', 'store', 'string', PARSED_QUERY_DOMAIN_FILE_OPTION, None, 'Path to the parsed query domain file.' ],
                [ '-f', '--querySlimprob', 'store', 'string', PARSED_SLIMPROB_OCC_FILE_OPTION, None, 'Path to the parsed SLiMProb occurrences file.' ],
                [ '-g', '--queryDisorder', 'store', 'string', QUERY_DISORDER_PROP_FILE_OPTION, None, 'Path to the file of disorder propensities.' ],
                [ '-i', '--ddi', 'store', 'string', DDI_FILE_OPTION, None, 'Path to the domain-domain interactions file.' ],
                [ '-j', '--dmi', 'store', 'string', DMI_FILE_OPTION, None, 'Path to the domain-motif interactions file.' ],
                [ '-k', '--allInteractions', 'store', 'string', ALL_INTERACTIONS_FILE_OPTION, None, 'Path to all interactions file.' ],
                [ '-x', '--binaryInteractions', 'store', 'string', BINARY_INTERACTIONS_FILE_OPTION, None, 'Path to binary interactions file.' ],
                [ '-l', '--queryFeatures', 'store', 'string', QUERY_FEATURES_JSON_FILE_OPTION, None, 'Path to the JSON file with query features.' ],
                [ '-m', '--seqNames', 'store', 'string', SQCE_NAMES_MATCH_FILE_OPTION, None, 'Path to the files where correspondences between sequence names are registered.' ],
                [ '-o', '--queryDomainOut', 'store', 'string', PARSED_QUERY_DOMAIN_RENAMED_SQCES_FILE_OPTION, None, 'Path to the parsed query domain file with sequences renamed.' ],
                [ '-p', '--querySlimprobOut', 'store', 'string', PARSED_SLIMPROB_OCC_RENAMED_SQCES_FILE_OPTION, None, 'Path to the parsed SLiMProb occurrences file with sequences renamed.' ],
                [ '-q', '--queryDisorderOut', 'store', 'string', QUERY_DISORDER_PROP_RENAMED_SQCES_FILE_OPTION, None, 'Path to the file of disorder propensities with sequences renamed.' ],
                [ '-r', '--ddiOut', 'store', 'string', DDI_FILE_RENAMED_SQCES_FILE_OPTION, None, 'Path to the domain-domain interactions file with sequences renamed.' ],
                [ '-s', '--dmiOut', 'store', 'string', DMI_FILE_RENAMED_SQCES_FILE_OPTION, None, 'Path to the domain-motif interactions file with sequences renamed.' ],
                [ '-t', '--allInteractionsOut', 'store', 'string', ALL_INTERACTIONS_FILE_RENAMED_SQCES_FILE_OPTION, None, 'Path to all interactions file with sequences renamed.' ],
                [ '-y', '--binaryInteractionsOut', 'store', 'string', BINARY_INTERACTIONS_RENAMED_SQCES_FILE_OPTION, None, 'Path to binary interactions file with sequences renamed.' ],
                [ '-u', '--allInteractionsJsonOut', 'store', 'string', ALL_INTERACTIONS_JSON_RENAMED_SQCES_FILE_OPTION, None, 'Path to the JSON file with all interactions with sequences renamed.' ],
                [ '-w', '--queryFeaturesOut', 'store', 'string', QUERY_FEATURES_JSON_RENAMED_SQCES_FILE_OPTION, None, 'Path to the JSON file with query features with sequences renamed.' ] ]



# ===========================================
# Get the matchs between sequence names
# ===========================================

# simplify_sqce_names
# -------------------
#
# This function allows to compute a "short" sequence name
# for all the sequences provided by the user.
# In order to work properly, it expects the headers to follow UniProt
# nomenclature, i.e. to be formatted such as:
# db|UniqueIdentifier|EntryName Supplementary Information
# With the three first element necessary.
# 
# @param query_fasta_file_path: String - The path to the fasta file containing the query sequences.
# @param query_sqce_names_match_file_path: String - The path to the file containing the association
#                                                   between the sequence names used by SLiMProb and the 
#                                                   "short" fasta headers.
# @param sqce_names_match_file_path: String - The path to the file containing all the association between
#                                             the provided fasta headers and the various sequence names 
#                                             computed.
#
# @return query_sqces: Dictionary - A dictionary that associates the "short" fasta headers
#                                   to the sequence names for the query sequences.
#
# @throw Exception - When the header cannot be parsed properly.
# @throw Exception - When the "short" header is not unique.
# 
def simplify_sqce_names( query_fasta_file_path, query_sqce_names_match_file_path, sqce_names_match_file_path ):
    
    # Parse the query fasta file
    # --------------------------
    # Instantiate a dictionary that associate to each "short" 
    # header (e.g.db|UniqueIdentifier|EntryName)
    # - The "full" header (as provided, e.g. db|UniqueIdentifier|EntryName Supplementary Information)
    # - The "sequence name" (e.g. UniqueIdentifier)
    # - The IPS sequence name (expected to be the same as the "short" header)
    # - The SLiMProb sequence name (it is set to an empty string at this stage and will be completed later, 
    #   so that sequences for which no SLiM has been detected have no SLiMProb sequence name registered)
    query_sqces = {}
    
    with open( query_fasta_file_path, 'r' ) as query_fasta_file:
        
        line = query_fasta_file.readline()
        
        while ( line != '' ):
            if line.startswith( '>' ):
                line = line.replace( '>', '' ).replace( '\n', '' )
                
                # Get the header as it is provided
                # e.g. db|UniqueIdentifier|EntryName Supplementary Information
                full_header = line
                
                # Get the first part of the header
                # e.g. db|UniqueIdentifier|EntryName
                short_header = line.split( ' ' )[0]
                
                # Try to get the unique identifier from the header
                # e.g. UniqueIdentifier
                short_header_elts = short_header.split( '|' )
                try:
                    seq_name = short_header_elts[1]
                except IndexError as e:
                    if ( len( short_header_elts ) == 1 ):
                        seq_name = short_header_elts[0]
                    else:
                        raise Exception( 'The format of the header is unexcepted (' + short_header +
                                         ', query fasta file). Fasta header must contains either a single' +
                                         ' sequence identifier, or a pipe (|)-separated header where the' +
                                         ' second element is the sequence identifier to allow sequence' +
                                         ' names simplification in output files.' )
                
                # Add this header to the dictionary 
                if not query_sqces.get( short_header ):
                    query_sqces[ short_header ] = { FULL_FASTA_SEQNAME: full_header,
                                                    SEQNAME: seq_name,
                                                    IPS_SEQNAME: short_header,
                                                    SLIMPROB_SEQNAME: '' }
                else:
                    raise Exception( 'The header "' + short_header + '" has been found twice in the' +
                                     ' query fasta file. Please, make sure to provide a fasta with' +
                                     ' unique sequence identifiers.' )
            
            line = query_fasta_file.readline()
    
    
    # Get the SLiMProb sequence names
    # -------------------------------
    # As SLiMProb uses different sequence names than the one provided,
    # and as the recovering of the actual fasta sequence names
    # is expected to have been performed (see match_query_sqce_names rule),
    # add to the query_sqces entry, the identifier used by SLiMProb,
    # getting the information in the file query_seqnames_match.tsv
    with open( query_sqce_names_match_file_path, 'r' ) as query_sqce_names_match_file:
        # Skip headers
        next( query_sqce_names_match_file )
        line = query_sqce_names_match_file.readline()
        while ( line != '' ):
            line = line.replace( '\n', '' ).split( '\t' )
            slimprob_seq_name = line[ SLIMPROB_MATCH_NAMES_SLIMPROB_SEQNAME_INDEX ]
            short_header = line[ SLIMPROB_MATCH_NAMES_FASTA_SEQNAME_INDEX ]
            query_sqces_entry = query_sqces.get( short_header )
            if query_sqces_entry:
                query_sqces_entry.update( { SLIMPROB_SEQNAME: slimprob_seq_name } )
            else:
                print( 'An unmatched sequence name has been found in the SLiMProb outputs:' +
                       slimprob_seq_name + '.' )
                query_sqces_entry.update( { SLIMPROB_SEQNAME: '' } )
            query_sqces[ short_header ] = query_sqces_entry
            line = query_sqce_names_match_file.readline()
    
    
    # Save the sequence names in a file
    # ---------------------------------
    with open( sqce_names_match_file_path, 'w' ) as sqce_names_match_file:
        # Add headers
        sqce_names_match_file.write( '\t'.join( [ 'Set', 'ShortHeader', 'FullHeader', 'SeqName', 
                                                  'IPS_SeqName', 'SLiMProb_SeqName' ] ) + '\n' )
        # Add the query sequences (in the alphabetical order)
        for short_header in sorted( query_sqces.keys() ):
            query_sqces_entry = query_sqces.get( short_header )
            sqce_names_match_file.write( '\t'.join( [ 'query', 
                                                      short_header,
                                                      query_sqces_entry.get( FULL_FASTA_SEQNAME ),
                                                      query_sqces_entry.get( SEQNAME ),
                                                      query_sqces_entry.get( IPS_SEQNAME ),
                                                      query_sqces_entry.get( SLIMPROB_SEQNAME ) ] ) + '\n' )
            
    return query_sqces
    

# ===========================================
# Simplify InterProScan outputs
# ===========================================

# simplify_parsed_domain_interpro
# -------------------------------
#
# This function allows to "simplify" the sequence names of the files
# parsed_target_domain_interpro.tsv and parsed_query_domain_interpro.tsv.
# 
# @param parsed_domain_file_path: String - The path to the parsed domain InterProScan file.
# @param parsed_domain_renamed_sqces_file_path: String - The path to the parsed domain InterProScan file
#                                                        where sequences have been renamed.
# @param sqce_dict: Dictionary - The dictionary that associates the "short" fasta headers
#                                to the sequence names.
# 
def simplify_parsed_domain_interpro( parsed_domain_file_path, parsed_domain_renamed_sqces_file_path, sqce_dict ):
    
    with open( parsed_domain_file_path, 'r' ) as parsed_domain_file, \
         open( parsed_domain_renamed_sqces_file_path, 'w' ) as parsed_domain_renamed_sqces_file:
        
        # Copy headers
        line = parsed_domain_file.readline()
        parsed_domain_renamed_sqces_file.write( line )
        line = parsed_domain_file.readline()
        
        while ( line != '' ):
            line = line.split( '\t' )
            # Get the sequence name to use
            parsed_seq_name = line[ PARSED_DOMAIN_SEQUENCE_INDEX ]
            seq_name = sqce_dict.get( parsed_seq_name ).get( SEQNAME )
            # Copy the line
            parsed_domain_renamed_sqces_file.write( '\t'.join( line[ :PARSED_DOMAIN_SEQUENCE_INDEX ] +
                                                               [ seq_name ] + 
                                                               line[ PARSED_DOMAIN_SEQUENCE_INDEX+1: ] ) )
            line = parsed_domain_file.readline()
            

# ===========================================
# Simplify SLiMProb outputs
# ===========================================

# simplify_parsed_slimprob_occ
# ----------------------------
#
# This function allows to "simplify" the sequence names of the parsed
# occurrence file (output of SLiMProb).
# 
# @param parsed_slimprob_occ_file_path: String - The path to the parsed SLiMProb occurrence file.
# @param parsed_slimprob_occ_renamed_sqces_file_path: String - The path to the parsed SLiMProb occurrence 
#                                                              file where sequences have been renamed.
# @param sqce_dict: Dictionary - The dictionary that associates the "short" fasta headers
#                                to the sequence names.
# 
def simplify_parsed_slimprob_occ( parsed_slimprob_occ_file_path, parsed_slimprob_occ_renamed_sqces_file_path, sqce_dict ):
    
    with open( parsed_slimprob_occ_file_path, 'r' ) as parsed_slimprob_occ_file, \
         open( parsed_slimprob_occ_renamed_sqces_file_path, 'w' ) as parsed_slimprob_occ_renamed_sqces_file:
        
        # Copy headers
        line = parsed_slimprob_occ_file.readline()
        parsed_slimprob_occ_renamed_sqces_file.write( line )
        line = parsed_slimprob_occ_file.readline()
        
        while ( line != '' ):
            line = line.split( '\t' )
            # Get the sequence name to use
            parsed_seq_name = line[ PARSED_SLIMRPOB_OCC_SEQUENCE_INDEX ]
            seq_name = sqce_dict.get( parsed_seq_name ).get( SEQNAME )
            # Copy the line
            if ( seq_name != '' ):
                parsed_slimprob_occ_renamed_sqces_file.write( '\t'.join( line[ :PARSED_SLIMRPOB_OCC_SEQUENCE_INDEX ] +
                                                                         [ seq_name ] + 
                                                                         line[ PARSED_SLIMRPOB_OCC_SEQUENCE_INDEX+1: ] ) )
            else:
                parsed_slimprob_occ_renamed_sqces_file.write( '\t'.join( line ) )
            line = parsed_slimprob_occ_file.readline()
            

# simplify_query_disorder_prop
# ----------------------------
#
# This function allows to "simplify" the sequence names of the parsed
# occurrence file (output of SLiMProb).
# 
# @param query_disorder_prop_file_path: String - The path to the file containing the query disorder scores.
# @param query_disorder_prop_renamed_sqces_file_path: String - The path to the file containing the query disorder 
#                                                              scores where sequences have been renamed.
# @param sqce_dict: Dictionary - The dictionary that associates the "short" fasta headers
#                                to the sequence names.
# 
def simplify_query_disorder_prop( query_disorder_prop_file_path, query_disorder_prop_renamed_sqces_file_path, sqce_dict ):
    
    with open( query_disorder_prop_file_path, 'r' ) as query_disorder_prop_file, \
         open( query_disorder_prop_renamed_sqces_file_path, 'w' ) as query_disorder_prop_renamed_sqces_file:
        
        # Copy headers
        line = query_disorder_prop_file.readline()
        query_disorder_prop_renamed_sqces_file.write( line )
        line = query_disorder_prop_file.readline()
        
        while (line != '' ):
            line = line.split( '\t' )
            # Get the sequence name to use
            file_seq_name = line[ QUERY_DISORDER_PROP_SEQUENCE_INDEX ]
            seq_name = sqce_dict.get( file_seq_name ).get( SEQNAME )
            # Copy the line
            if ( seq_name != '' ):
                query_disorder_prop_renamed_sqces_file.write( '\t'.join( line[ :QUERY_DISORDER_PROP_SEQUENCE_INDEX ] +
                                                                         [ seq_name ] +
                                                                         line[ QUERY_DISORDER_PROP_SEQUENCE_INDEX+1: ] ) )
            else:
                query_disorder_prop_renamed_sqces_file.write( '\t'.join( line ) )
            line = query_disorder_prop_file.readline()
    

            
# ===========================================
# Simplify interaction inference outputs
# ===========================================

# simplify_inferred_ddi
# ---------------------
#
# This function allows to "simplify" the sequence names of the 
# domain-domain interactions file.
# 
# @param ddi_file_path: String - The path to the file containing the domain-domain interactions.
# @param ddi_renamed_sqces_file_path: String - The path to the file containing the domain-domain interactions
#                                              where sequences have been renamed.
# @param query_sqces: Dictionary - The dictionary that associates the "short" fasta headers
#                                  to the sequence names for the query sequences.
# 
def simplify_inferred_ddi( ddi_file_path, ddi_renamed_sqces_file_path, query_sqces ):
    
    with open( ddi_file_path, 'r' ) as ddi_file, \
         open( ddi_renamed_sqces_file_path, 'w' ) as ddi_renamed_sqces_file:
        
        # Copy headers
        line = ddi_file.readline()
        ddi_renamed_sqces_file.write( line )
        line = ddi_file.readline()
        
        while (line != '' ):
            line = line.split( '\t' )
            # Get the query sequence name to use
            file_query_seq_name = line[ DDI_QUERY_SEQUENCE_INDEX ]
            query_seq_name = query_sqces.get( file_query_seq_name ).get( SEQNAME )
            if ( query_seq_name == '' ):
                query_seq_name = file_query_seq_name
            
            # Get the target sequence name to use
            file_target_seq_name = line[ DDI_TARGET_SEQUENCE_INDEX ]
            
            # Copy the line
            ddi_renamed_sqces_file.write( '\t'.join( line[ : DDI_QUERY_SEQUENCE_INDEX ] +
                                                     [ query_seq_name ] +
                                                     line[ DDI_QUERY_SEQUENCE_INDEX+1 : DDI_TARGET_SEQUENCE_INDEX ] +
                                                     [ file_target_seq_name ] +
                                                     line[ DDI_TARGET_SEQUENCE_INDEX+1 : ] ) )
            line = ddi_file.readline()



# simplify_inferred_dmi
# ---------------------
#
# This function allows to "simplify" the sequence names of the 
# domain-motif interactions file.
# 
# @param dmi_file_path: String - The path to the file containing the domain-motif interactions.
# @param dmi_renamed_sqces_file_path: String - The path to the file containing the domain-motif interactions
#                                              where sequences have been renamed.
# @param query_sqces: Dictionary - The dictionary that associates the "short" fasta headers
#                                  to the sequence names for the query sequences.
# 
def simplify_inferred_dmi( dmi_file_path, dmi_renamed_sqces_file_path, query_sqces ):
    
    with open( dmi_file_path, 'r' ) as dmi_file, \
         open( dmi_renamed_sqces_file_path, 'w' ) as dmi_renamed_sqces_file:
        
        # Copy headers
        line = dmi_file.readline()
        dmi_renamed_sqces_file.write( line )
        line = dmi_file.readline()
        
        while (line != '' ):
            line = line.split( '\t' )
            # Get the query sequence name to use
            file_query_seq_name = line[ DMI_QUERY_SEQUENCE_INDEX ]
            query_seq_name = query_sqces.get( file_query_seq_name ).get( SEQNAME )
            if ( query_seq_name == '' ):
                query_seq_name = file_query_seq_name
            
            # Get the target sequence name to use
            file_target_seq_name = line[ DMI_TARGET_SEQUENCE_INDEX ]
            
            # Copy the line
            dmi_renamed_sqces_file.write( '\t'.join( line[ : DMI_QUERY_SEQUENCE_INDEX ] +
                                                     [ query_seq_name ] +
                                                     line[ DMI_QUERY_SEQUENCE_INDEX+1 : DMI_TARGET_SEQUENCE_INDEX ] +
                                                     [ file_target_seq_name ] +
                                                     line[ DMI_TARGET_SEQUENCE_INDEX+1 : ] ) )
            line = dmi_file.readline()



# simplify_inferred_all
# ---------------------
#
# This function allows to "simplify" the sequence names of the 
# file containing all inferred interactions.
# 
# @param all_inter_file_path: String - The path to the file containing all the inferred interactions.
# @param all_inter_renamed_sqces_file_path: String - The path to the file containing all the inferred interactions
#                                                    where sequences have been renamed.
# @param query_sqces: Dictionary - The dictionary that associates the "short" fasta headers
#                                  to the sequence names for the query sequences.
# 
def simplify_inferred_all( all_inter_file_path, all_inter_renamed_sqces_file_path, query_sqces ):
    
    with open( all_inter_file_path, 'r' ) as all_inter_file, \
         open( all_inter_renamed_sqces_file_path, 'w' ) as all_inter_renamed_sqces_file:
        
        # Copy headers
        line = all_inter_file.readline()
        all_inter_renamed_sqces_file.write( line )
        line = all_inter_file.readline()
        
        while (line != '' ):
            line = line.split( '\t' )
            # Get the query sequence name to use
            file_query_seq_name = line[ ALL_INTER_QUERY_SEQUENCE_INDEX ]
            query_seq_name = query_sqces.get( file_query_seq_name ).get( SEQNAME )
            if ( query_seq_name == '' ):
                query_seq_name = file_query_seq_name
            
            # Get the target sequence name to use
            file_target_seq_name = line[ ALL_INTER_TARGET_SEQUENCE_INDEX ]
            
            # Copy the line
            all_inter_renamed_sqces_file.write( '\t'.join( line[ : ALL_INTER_QUERY_SEQUENCE_INDEX ] +
                                                           [ query_seq_name ] +
                                                           line[ ALL_INTER_QUERY_SEQUENCE_INDEX+1 : ALL_INTER_TARGET_SEQUENCE_INDEX ] +
                                                           [ file_target_seq_name ] +
                                                           line[ ALL_INTER_TARGET_SEQUENCE_INDEX+1 : ] ) )
            line = all_inter_file.readline()



# simplify_inferred_binary
# ------------------------
#
# This function allows to "simplify" the sequence names of the 
# file containing binary inferred interactions.
# 
# @param binary_inter_file_path: String - The path to the file containing the binary inferred interactions.
# @param binary_inter_renamed_sqces_file_path: String - The path to the file containing the binary inferred 
#                                                       interactions where sequences have been renamed.
# @param query_sqces: Dictionary - The dictionary that associates the "short" fasta headers
#                                  to the sequence names for the query sequences.
# 
def simplify_inferred_binary( binary_inter_file_path, binary_inter_renamed_sqces_file_path, query_sqces ):
    
    with open( binary_inter_file_path, 'r' ) as binary_inter_file, \
         open( binary_inter_renamed_sqces_file_path, 'w' ) as binary_inter_renamed_sqces_file:
        
        line = binary_inter_file.readline()
        
        while (line != '' ):
            line = line.split( '\t' )
            # Get the query sequence name to use
            file_query_seq_name = line[ BINARY_INTER_QUERY_SEQUENCE_INDEX ]
            query_seq_name = query_sqces.get( file_query_seq_name ).get( SEQNAME )
            if ( query_seq_name == '' ):
                query_seq_name = file_query_seq_name
            
            # Get the target sequence name to use
            file_target_seq_name = line[ BINARY_INTER_TARGET_SEQUENCE_INDEX ]
            
            # Copy the line
            binary_inter_renamed_sqces_file.write( '\t'.join( line[ : BINARY_INTER_QUERY_SEQUENCE_INDEX ] +
                                                              [ query_seq_name ] +
                                                              line[ BINARY_INTER_QUERY_SEQUENCE_INDEX+1 : BINARY_INTER_TARGET_SEQUENCE_INDEX ] +
                                                              [ file_target_seq_name ] +
                                                              line[ BINARY_INTER_TARGET_SEQUENCE_INDEX+1 : ] ) )
            line = binary_inter_file.readline()
    

            
# ===========================================
# Simplify summary files
# ===========================================

# simplify_query_features_json
# ----------------------------
#
# This function allows to "simplify" the sequence names of the 
# query features JSON file.
# 
# @param query_features_json_file_path: String - The path to the file containing the domain-domain interactions.
# @param query_features_json_renamed_sqces_file_path: String - The path to the file containing the domain-domain interactions
#                                              where sequences have been renamed.
# @param query_sqces: Dictionary - The dictionary that associates the "short" fasta headers
#                                  to the sequence names for the query sequences.
# 
def simplify_query_features_json( query_features_json_file_path, query_features_json_renamed_sqces_file_path, query_sqces ):
    
    with open( query_features_json_file_path, 'r' ) as query_features_json_file:
        json_content = json.load( query_features_json_file )
    
    # Update the content of the file
    json_content_renamed_seq = {}
    for file_seq_name in json_content.keys():
        # Get the sequence name to use
        seq_name = query_sqces.get( file_seq_name ).get( SEQNAME )
        if ( seq_name == '' ):
            seq_name = file_seq_name
        # Update the sequence name
        json_content_renamed_seq[ seq_name ] = json_content.get( file_seq_name )
            
    with open( query_features_json_renamed_sqces_file_path, 'w' ) as query_features_json_renamed_sqces_file:
        json.dump( json_content_renamed_seq, query_features_json_renamed_sqces_file, indent=4 )
    
            


# ===========================================
# Parse command line arguments 
# and run script
# ===========================================
     
if __name__=='__main__':
    
    # Parse the command-line arguments
    option_dict = parse_arguments( OPTION_LIST )
    
    # Get all the paths necessary to run the current script
    # Inputs
    query_fasta_file_path = get_option( option_dict = option_dict, option_name = QUERY_FATA_FILE_OPTION, not_none = True )
    
    target_domain_annotations_file_path = get_option( option_dict = option_dict, option_name = TARGET_DOMAIN_ANNOTATIONS_FILE_OPTION, not_none = True )
    
    parsed_query_domain_file_path = get_option( option_dict = option_dict, option_name = PARSED_QUERY_DOMAIN_FILE_OPTION, not_none = True )
    
    query_sqce_names_match_file_path = get_option( option_dict = option_dict, option_name = QUERY_SQCE_NAMES_MATCH_FILE_OPTION, not_none = True )
    parsed_slimprob_occ_file_path = get_option( option_dict = option_dict, option_name = PARSED_SLIMPROB_OCC_FILE_OPTION, not_none = True )
    query_disorder_prop_file_path = get_option( option_dict = option_dict, option_name = QUERY_DISORDER_PROP_FILE_OPTION, not_none = True )
    
    ddi_file_path = get_option( option_dict = option_dict, option_name = DDI_FILE_OPTION, not_none = True )
    dmi_file_path = get_option( option_dict = option_dict, option_name = DMI_FILE_OPTION, not_none = True )
    all_inter_file_path = get_option( option_dict = option_dict, option_name = ALL_INTERACTIONS_FILE_OPTION, not_none = True )
    binary_inter_file_path = get_option( option_dict = option_dict, option_name = BINARY_INTERACTIONS_FILE_OPTION, not_none = True )
    
    query_features_json_file_path = get_option( option_dict = option_dict, option_name = QUERY_FEATURES_JSON_FILE_OPTION, not_none = True )
    
    
    # Outputs
    sqce_names_match_file_path = get_option( option_dict = option_dict, option_name = SQCE_NAMES_MATCH_FILE_OPTION, not_none = True )
    
    parsed_query_domain_renamed_sqces_file_path = get_option( option_dict = option_dict, option_name = PARSED_QUERY_DOMAIN_RENAMED_SQCES_FILE_OPTION, not_none = True )
    
    parsed_slimprob_occ_renamed_sqces_file_path = get_option( option_dict = option_dict, option_name = PARSED_SLIMPROB_OCC_RENAMED_SQCES_FILE_OPTION, not_none = True )
    query_disorder_prop_renamed_sqces_file_path = get_option( option_dict = option_dict, option_name = QUERY_DISORDER_PROP_RENAMED_SQCES_FILE_OPTION, not_none = True )
    
    ddi_renamed_sqces_file_path = get_option( option_dict = option_dict, option_name = DDI_FILE_RENAMED_SQCES_FILE_OPTION, not_none = True )
    dmi_renamed_sqces_file_path = get_option( option_dict = option_dict, option_name = DMI_FILE_RENAMED_SQCES_FILE_OPTION, not_none = True )
    all_inter_renamed_sqces_file_path = get_option( option_dict = option_dict, option_name = ALL_INTERACTIONS_FILE_RENAMED_SQCES_FILE_OPTION, not_none = True )
    binary_inter_renamed_sqces_file_path = get_option( option_dict = option_dict, option_name = BINARY_INTERACTIONS_RENAMED_SQCES_FILE_OPTION, not_none = True )
    all_interactions_renamed_sqces_json_file_path = get_option( option_dict = option_dict, option_name = ALL_INTERACTIONS_JSON_RENAMED_SQCES_FILE_OPTION, not_none = True )
    
    query_features_json_renamed_sqces_file_path = get_option( option_dict = option_dict, option_name = QUERY_FEATURES_JSON_RENAMED_SQCES_FILE_OPTION, not_none = True )
        
    
    # Run the scripts
    # --------------- 
    
    # Compute the "short" query sequence names
    query_sqces = simplify_sqce_names( query_fasta_file_path = query_fasta_file_path,
                                       query_sqce_names_match_file_path = query_sqce_names_match_file_path,
                                       sqce_names_match_file_path = sqce_names_match_file_path )
        
    # "Simplify" the outputs of InterProScan
      # Query sequences
    simplify_parsed_domain_interpro( parsed_domain_file_path = parsed_query_domain_file_path, 
                                     parsed_domain_renamed_sqces_file_path = parsed_query_domain_renamed_sqces_file_path, 
                                     sqce_dict = query_sqces )
    
    # "Simplify" the outputs of SLiMProb
      # Occurrences file
    simplify_parsed_slimprob_occ( parsed_slimprob_occ_file_path = parsed_slimprob_occ_file_path, 
                                  parsed_slimprob_occ_renamed_sqces_file_path = parsed_slimprob_occ_renamed_sqces_file_path, 
                                  sqce_dict = query_sqces )
      # Disorder propensities file
    simplify_query_disorder_prop( query_disorder_prop_file_path = query_disorder_prop_file_path,
                                  query_disorder_prop_renamed_sqces_file_path = query_disorder_prop_renamed_sqces_file_path, 
                                  sqce_dict = query_sqces )
    
    # Inferred interactions files
      # Domain-domain interactions file
    simplify_inferred_ddi( ddi_file_path = ddi_file_path, 
                           ddi_renamed_sqces_file_path = ddi_renamed_sqces_file_path, 
                           query_sqces = query_sqces )
    
      # Domain-motif interactions file
    simplify_inferred_dmi( dmi_file_path = dmi_file_path,
                           dmi_renamed_sqces_file_path = dmi_renamed_sqces_file_path,
                           query_sqces = query_sqces )
         
      # All interactions file
    simplify_inferred_all( all_inter_file_path = all_inter_file_path,
                           all_inter_renamed_sqces_file_path = all_inter_renamed_sqces_file_path,
                           query_sqces = query_sqces )
    
      # Binary interactions file
    simplify_inferred_binary( binary_inter_file_path = binary_inter_file_path,
                              binary_inter_renamed_sqces_file_path = binary_inter_renamed_sqces_file_path,
                              query_sqces = query_sqces )
    
      # Re-built the Json file containing all the interactions
      # NB: This is quicker than parsing the file and changing the name
      #     and would make maintenance of the current script easier.
    interaction_all_to_json.generate_json( inferred_all_interactions_file = all_inter_renamed_sqces_file_path, 
                                           target_domain_annotations_file = target_domain_annotations_file_path,
                                           all_interactions_json_file = all_interactions_renamed_sqces_json_file_path )
    
    # "Simplify" the summary files
    simplify_query_features_json( query_features_json_file_path = query_features_json_file_path,
                                  query_features_json_renamed_sqces_file_path = query_features_json_renamed_sqces_file_path, 
                                  query_sqces = query_sqces )
    