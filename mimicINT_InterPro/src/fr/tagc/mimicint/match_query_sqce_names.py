#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os 


from fr.tagc.mimicint.util.option.OptionManager import *

# This script allows to generate a file associating each sequence 
# names as generated by SLiMProb to its original sequence name 
# (as provided in the query fasta file).


# ===========================================
# Constants
# ===========================================
# 
# Extension at the end of the IUScore files generated by IUPred
IUSCORE_FILE_EXTENSION = '.iupred.txt'

# Index of the columns of the SLiMProb occurrence file
SLIMPROB_OCC_SEQ_INDEX = 4
SLIMPROB_OCC_ACCNUM_INDEX = 5


# List of options allowed
# -----------------------
# Path to the query fasta file
QUERY_FASTA_FILE_OPTION = 'QUERY_FASTA_FILE'
# Path to the file with slimprob results (a SlimSuite tool)
SLIMPROB_RES_FILE_OPTION = 'SLIMPROB_RES_FILE'
# Path of the folder containing the IUPred scores files
IUSCORE_FOLDER_OPTION = 'IUSCORE_FOLDER'
# Path to the file associating to each sequence name used 
# by SLiMProb the original sequence name in the fasta file
SEQNAMES_FILE_OPTION = 'SEQNAMES_FILE'

OPTION_LIST = [ [ '-f', '--fastaFile', 'store', 'string', QUERY_FASTA_FILE_OPTION, None, 'The path to the query fasta file.' ],
                [ '-s', '--slimprobRes', 'store', 'string', SLIMPROB_RES_FILE_OPTION, None, 'The path to the file with slimprob results (a SlimSuite tool).' ],
                [ '-i', '--iuscoredir', 'store', 'string', IUSCORE_FOLDER_OPTION, None, 'The path of the folder containing the IUPred scores files.' ],
                [ '-n', '--seqNameFile', 'store', 'string', SEQNAMES_FILE_OPTION, None, 'The path to the file associating to each sequence name used by SLiMProb \
                                                                                      the original sequence name in the fasta file.' ] ]



# ===========================================
# Script
# ===========================================

# match_query_sqce_names
# ----------------------
#
# This function allows to match all the sequence names used in 
# the outputs of SLiMProb with the ones provided in the query
# fasta file.
#
# @param query_fasta_file_path: String - The path to the fasta file containing the query sequences.
# @param slimprob_res_file_path: String - The path of the SLiMProb occurrence file.
# @param iuscore_folder_path: String - The path of the folder containing the IUPred scores
#                                      for all sequences, as generated by SLiMProb.
# @param seq_names_file_path: String - The path to the file associating to each SLiMProb
#                                      sequence its name in the original query fasta file.
#
def match_query_sqce_names( query_fasta_file_path, slimprob_res_file_path, iuscore_folder_path, seq_names_file_path) :
    
    # Get all the headers of the query fasta files
    # --------------------------------------------
    query_fasta_headers = []
    with open( query_fasta_file_path, 'r' ) as query_fasta_file:
        line = query_fasta_file.readline()
        while ( line != '' ):
            if line.startswith( '>' ):
                # Get the first part of the header
                header = line[ 1: ]
                if header.startswith( ' ' ):
                    header = header[ 1: ]
                header = header.split( ' ' )[ 0 ]
                header = header.replace( '\n', '' )
                query_fasta_headers.append( header )
            line = query_fasta_file.readline()
        
    
    # Get the sequence names used by SLiMProb
    # ---------------------------------------
    # Get the list of IUScore files contained in the iuscore folder
    iuscore_files = os.listdir( iuscore_folder_path )
    iuscore_files = [ file for file in iuscore_files if file.endswith( IUSCORE_FILE_EXTENSION ) ]
    
    # Get the full list of sequence names generated by SLiMProb
    slimprob_seq_names_list = []
    for iuscore_file in iuscore_files:
        
        with open( os.path.join( iuscore_folder_path, iuscore_file ), 'r' ) as iuscores:
            iuscores_list = iuscores.read()
            iuscores_list = iuscores_list.replace( ' ', '\t' ).replace( '\n', '' ).split( '\t' )
            # Get the name of the sequence and add it to the list
            seq = iuscores_list[ 0 ]
            slimprob_seq_names_list.append( seq )
    
    # Get the accession name of the sequence
    # As the occurrence file contains a column with the protein 
    # accession, get it as this will help resolving the associations 
    # between the sequence names and the actual name provided 
    # in the fasta headers
    slimprob_seq_acc = {}
    with open( slimprob_res_file_path, 'r' ) as slimprob_res_file:
        next( slimprob_res_file )
        line = slimprob_res_file.readline()
        while ( line != '' ):
            line = line.split( '\t' )
            slimprob_seq_name = line[ SLIMPROB_OCC_SEQ_INDEX ]
            acc_num = line[ SLIMPROB_OCC_ACCNUM_INDEX ]
            if ( not slimprob_seq_acc.get( slimprob_seq_name ) ):
                slimprob_seq_acc[ slimprob_seq_name ] = acc_num
            line = slimprob_res_file.readline()
    
    
    # Match the two sets of sequence names
    # ------------------------------------

    # Instantiate a dictionary that will associate to each unique 
    # sequence names its unique corresponding header (if existing)
    # Keys are sequence names (from SLiMProb occurrence file)
    # Values are headers from the query fasta file
    non_ambiguous_seq_names_asso_dict = {}
    
    # Instantiate a dictionary that keeps tracks of the ambiguous 
    # associations
    # Keys are sequence names (from SLiMProb occurrence file)
    # Values are lists of headers from the query fasta file
    ambiguous_seq_names_asso_dict = {}
    
    
    # First process the sequences for which the accession name is known
    for slimprob_seq_name in slimprob_seq_acc.keys():
        
        # Parse the sequence name                             
        seq = slimprob_seq_name.split( '_')
        seq = [ s for s in seq if ( s != '' and s != 'UNK' ) ]
                
        # Loop over the headers of the query fasta file to find the 
        # headers that may match the sequence name
        header_candidates = []

        for header in query_fasta_headers:
            
            all_elts_in_header = True
            
            if ( slimprob_seq_acc[ slimprob_seq_name ] not in header ):
                all_elts_in_header = False
            
            k=0
            while ( all_elts_in_header and ( k < len( seq ) ) ):
                if ( seq[ k ] not in header ):
                    all_elts_in_header = False
                k += 1
            
            # If the header has all the expected part of the sequence name
            # then add it to the candidates
            if all_elts_in_header:
                header_candidates.append( header )
            
                
        # If the search result one single candidate, then associate this 
        # sequence name to its unique header
        if ( len( header_candidates ) ==  1):
            non_ambiguous_seq_names_asso_dict[ slimprob_seq_name] = header_candidates[ 0 ]
            
        # Otherwise, if the search return several results,
        # then add this sequence to the ambiguous dictionary
        # NB: This is susceptible to happen when the name of a protein in a header
        #     is also part of the name of another protein.
        #     E.g. considering the two following headers are existing in the fasta file:
        #          sp|P0C6U8-1|NSP1_CVHSA
        #          sp|P0C6U8-10|NSP10_CVHSA
        #          Then, the search of correspondence for the sequence name
        #          NSP1_CVHSA__P0C6U8-1, will return ambiguously the two headers
        #          whilst NSP1_CVHSA__P0C6U8-10 will unambiguously associate 
        #          this sequence name to the original sp|P0C6U8-10|NSP1_CVHSA header
        elif ( len( header_candidates) > 1 ):
            ambiguous_seq_names_asso_dict[ slimprob_seq_name ] = header_candidates
            
        # Otherwise, if the search did not return any result, 
        # consider it as non processed
                    
    
    # Process the headers that have not yet been processed,
    # using information for the IUPred score files
    processed_seq_names_set = set( non_ambiguous_seq_names_asso_dict.keys() )
    processed_seq_names_ambiguous_set = set( ambiguous_seq_names_asso_dict.keys() )
    slimprob_seq_names_full_set = set( slimprob_seq_names_list )
    
    unprocessed_seq_names_set = slimprob_seq_names_full_set.difference( processed_seq_names_set )
    unprocessed_seq_names_list = list( unprocessed_seq_names_set.difference( processed_seq_names_ambiguous_set ) )
    
    for slimprob_seq_name in unprocessed_seq_names_list:
        
        # Parse the sequence name                     
        seq = slimprob_seq_name.split( '_')
        seq = [ s for s in seq if  ( s != '' and s != 'UNK' ) ]
                
        # Loop over the headers of the query fasta file to find the 
        # headers that may match the sequence name
        header_candidates = []

        for header in query_fasta_headers:
            
            all_elts_in_header = True
            
            k=0
            while ( all_elts_in_header and ( k < len( seq ) ) ):
                if ( seq[ k ] not in header ):
                    all_elts_in_header = False
                k += 1
            
            # If the header has all the expected part of the sequence name
            # then add it to the candidates
            if all_elts_in_header:
                header_candidates.append( header )
            
                
        # If the search result one single candidate, then associate this 
        # sequence name to its unique header
        if ( len( header_candidates ) ==  1):
            non_ambiguous_seq_names_asso_dict[ slimprob_seq_name] = header_candidates[ 0 ]
            
        # Otherwise, if the search return several results,
        # add this sequence to the ambiguous dictionary
        elif ( len( header_candidates) > 1 ):
            ambiguous_seq_names_asso_dict[ slimprob_seq_name ] = header_candidates
            
        # Otherwise, try to get out of the list the first element 
        # of the header and perform the same search a second time
        else:
            # When the header use the format >db|UNIQUEID|ENTRYNAME
            # where db is not 'sp' or 'tr', the sequence name in the
            # output may look like 'dbuniqueid_UNK_ENTRYNAME'. Hence,
            # removing 'dbuniqueid' might help resolving the 
            # correspondence between sequence names.
            seq = seq[1:]

            for header in query_fasta_headers:
                
                all_elts_in_header = True
                
                k=0
                while ( all_elts_in_header and ( k < len( seq ) ) ):
                    if ( seq[ k ] not in header ):
                        all_elts_in_header = False
                    k += 1
                
                # If the header has all the expected part of the sequence name
                # then add it to the candidates
                if all_elts_in_header:
                    header_candidates.append( header )
                
                    
            # If the search result one single candidate, then associate this 
            # sequence name to its unique header
            if ( len( header_candidates ) ==  1):
                non_ambiguous_seq_names_asso_dict[ slimprob_seq_name] = header_candidates[ 0 ]
                
            # Otherwise, if the search return several results,
            # add this sequence to the ambiguous dictionary
            elif ( len( header_candidates) > 1 ):
                ambiguous_seq_names_asso_dict[ slimprob_seq_name ] = header_candidates
                
            # if the search did not return any result, 
            # consider it as non processed
            else:
                non_ambiguous_seq_names_asso_dict[ slimprob_seq_name] = slimprob_seq_name
            
    
        
    # Try to resolve the eventual ambiguity that still remains
    #
    # For each of the sequence for which several headers candidates 
    # have been found, check for each candidate if it has been 
    # associated unambiguously to an other sequence.
    # This process is repeted sequentially until there is no longer 
    # any ambiguity or the remaining ambiguity cannot be solved.
    # 
    # E.g. considering the three following headers are existing in the fasta file:
    #          sp|P0C6U8-1|NSP1_CVHSA
    #          sp|P0C6U8-11|NSP11_CVHSA
    #          sp|P0C6U8-111|NSP111_CVHSA
    #          Then, 
    #            - The search of correspondence for the sequence name 
    #              NSP111_CVHSA__P0C6U8-111 will return the appropriate header 
    #              sp|P0C6U8-111|NSP111_CVHSA
    #
    #            - The other sequence names will not be associated unambiguously 
    #              to a single header
    #                - NSP1_CVHSA__P0C6U8-1  will be ambiguously associated to 
    #                  [sp|P0C6U8-1|NSP1_CVHSA, sp|P0C6U8-11|NSP11_CVHSA, sp|P0C6U8-111|NSP111_CVHSA]
    #                - NSP11_CVHSA__P0C6U8-11 will be ambiguously associated to
    #                  [sp|P0C6U8-11|NSP11_CVHSA, sp|P0C6U8-111|NSP111_CVHSA]
    #
    #          Hence, scanning the list a second time will allow 
    #              - to associate unambiguously the sequence name NSP11_CVHSA__P0C6U8-11 
    #                to sp|P0C6U8-11|NSP11_CVHSA 
    #              - the sequence name sp|P0C6U8-1|NSP1_CVHSA to the single remaining 
    #                header that has not been yet associated to a sequence name, 
    #                i.e. sp|P0C6U8-1|NSP1_CVHSA).
    #
    # NB: Scanning the sequence in the reverse alphabetical order increase the chances 
    #     of match.
    previous_ambiguous_seq_names_asso_dict = {}
    
    while ( ( len( ambiguous_seq_names_asso_dict.keys() ) != 0 )
            and( ambiguous_seq_names_asso_dict != previous_ambiguous_seq_names_asso_dict ) ):
        
        previous_ambiguous_seq_names_asso_dict = dict( ambiguous_seq_names_asso_dict )
            
        # Reverse the key-values of the non ambiguous dictionary
        reversed_non_ambiguous_seq_names_asso_dict = { val: key for (key, val) in non_ambiguous_seq_names_asso_dict.items()}
        
        # Ensure the uniqueness of the keys has been preserved
        if ( len( non_ambiguous_seq_names_asso_dict.keys()) != len( reversed_non_ambiguous_seq_names_asso_dict.keys())):
            raise Exception( 'CRITICAL :: Programming error. The dictionary non_ambiguous_seq_names_asso_dict \
                              is expected to associate unambiguously the updated sequence names with the \
                              sequence names provided in the query fasta header. \
                              Please contact the developer if you see this message.')
        
        # Process the sequences in a reverse alphabetical order
        # to maximize the chances to get a match.
        for slimprob_seq_name in sorted( ambiguous_seq_names_asso_dict.keys(), reverse = True ):
            header_candidates = ambiguous_seq_names_asso_dict.get( slimprob_seq_name )
            
            remaining_candidates = []
            for hd_candidate in header_candidates:
                if ( not reversed_non_ambiguous_seq_names_asso_dict.get( hd_candidate ) ):
                    remaining_candidates.append( hd_candidate )
            
            # If there is one single candidate that has not yet been 
            # associated to a sequence, then get it
            if ( len( remaining_candidates) == 1 ):
                non_ambiguous_seq_names_asso_dict[ slimprob_seq_name ] = remaining_candidates[0]
                
                # Remove the entry from the dictionary of ambiguous sequences
                del ambiguous_seq_names_asso_dict[ slimprob_seq_name ]
                    
    # If this is impossible to associate accurately the sequence 
    # name used by SLiMProb with the original fasta header, then
    # use the SLiMProb sequence name.
    for slimprob_seq_name in ambiguous_seq_names_asso_dict.keys():
        non_ambiguous_seq_names_asso_dict[ slimprob_seq_name ] = slimprob_seq_name
    
    
    # Write these associations in a tsv file
    # --------------------------------------
    with open( seq_names_file_path, 'w' ) as seq_names_file:
        seq_names_file.write( '\t'.join( [ 'SlimprobSeqName', 'Seq' + '\n' ] ) )
        for ( slimprob_seq_name, header_seq_name ) in non_ambiguous_seq_names_asso_dict.items():
            seq_names_file.write( '\t'.join( [ slimprob_seq_name, header_seq_name + '\n' ] ) )
            


# ===========================================
# Parse command line arguments 
# and run script
# ===========================================

#### Code execution in the console ####
if __name__ == '__main__':
    
    # Parse the command-line arguments
    option_dict = parse_arguments( OPTION_LIST )
    
    # Get the path to the query fasta file
    query_fasta_file_path = get_option( option_dict = option_dict,
                                        option_name = QUERY_FASTA_FILE_OPTION, 
                                        not_none = True )
    
    # Get the path to the occurrence file
    slimprob_res_file_path = get_option( option_dict = option_dict, 
                                         option_name = SLIMPROB_RES_FILE_OPTION, 
                                         not_none = True )
    
    # Get the path to the iuscore folder
    iuscore_folder_path = get_option( option_dict = option_dict,
                                      option_name = IUSCORE_FOLDER_OPTION, 
                                      not_none = True )
    
    # Get the path to the output file
    seq_names_file_path = get_option( option_dict = option_dict,
                                      option_name = SEQNAMES_FILE_OPTION, 
                                      not_none = True )
    
    # Run the script
    match_query_sqce_names( query_fasta_file_path = query_fasta_file_path,
                            slimprob_res_file_path = slimprob_res_file_path,
                            iuscore_folder_path = iuscore_folder_path, 
                            seq_names_file_path = seq_names_file_path )
    