#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import datetime
import time
import shutil
from optparse import OptionParser

import subprocess

from multiprocessing import Pool


# This script allows to run SLiMProb on all randomized sequences
# of a particular strain on one particular background.

# NB: In order to work properly, this script expects the appropriate number
#     of randomized sequences files to have been generated properly.


# ===========================================
# Constants
# ===========================================

# Default option values
DEFAULT_SLIMPROB_EXTRAS = '0'
DEFAULT_SLIMPROB_PICKLE = 'F'
DEFAULT_SLIMPROB_SAVESPACE = '2'

# List of options allowed
# -----------------------

# Path to the ELM motifs
ELM_MOTIFS_PARSED_FILE_OPTION = 'ELM_MOTIFS_PARSED_FILE'
# Pattern of the path to the randomized sequences
RANDOMIZED_FASTA_FILE_PATTERN_OPTION = 'RANDOMIZED_FASTA_FILE_PATTERN'
# Pattern of the path to the randomized sequence SLiMProb folder
RANDOMIZED_SQCE_SLIMPROB_FOLDER_PATTERN_OPTION = 'RANDOMIZED_SQCE_SLIMPROB_FOLDER_PATTERN'
# Pattern of the path to the occurence file
OCCURENCE_FILE_PATTERN_OPTION = 'OCCURENCE_FILE_PATTERN'
# Pattern of the path to the log file
LOG_FILE_PATTERN_OPTION = 'LOG_FILE_PATTERN'
# Number of randomizations
RANDOM_ITERATIONS_OPTION = 'RANDOM_ITERATIONS'
# Number of threads available
THREAD_NB_COUNT_OPTION = 'THREAD_NB_COUNT'
# SLiMProb options
# - maxsize
SLIMPROB_MAXSIZE_OPTION = 'SLIMPROB_MAXSIZE'
# - maxseq
SLIMPROB_MAXSEQ_OPTION = 'SLIMPROB_MAXSEQ'
# - minregion
SLIMPROB_MINREGION_OPTION = 'SLIMPROB_MINREGION'
# - iumethod
SLIMPROB_IUMETHOD_OPTION = 'SLIMPROB_IUMETHOD'
# - iucut
SLIMPROB_IUCUT_OPTION = 'SLIMPROB_IUCUT'
# - extras
SLIMPROB_EXTRAS_OPTION = 'SLIMPROB_EXTRAS'
# - pickle
SLIMPROB_PICKLE_OPTION = 'SLIMPROB_PICKLE'
# - savespace 
SLIMPROB_SAVESPACE_OPTION = 'SLIMPROB_SAVESPACE'

OPTION_LIST = [ [ '-m', '--motifs', 'store', 'string', ELM_MOTIFS_PARSED_FILE_OPTION, None, 'The path to the ELM motifs parsed file.' ],
                [ '-s', '--seqinPattern', 'store', 'string', RANDOMIZED_FASTA_FILE_PATTERN_OPTION, None, 'The pattern of the paths to the randomized sequences fasta files.' ], 
                [ '-r', '--resdirPattern', 'store', 'string', RANDOMIZED_SQCE_SLIMPROB_FOLDER_PATTERN_OPTION, None, 'The pattern of the paths to the SLiMProb (temporary) folders.' ],
                [ '-o', '--resfilePattern', 'store', 'string', OCCURENCE_FILE_PATTERN_OPTION, None, 'The pattern of the paths to the occurrence files.' ],
                [ '-l', '--logPattern', 'store', 'string', LOG_FILE_PATTERN_OPTION, None, 'The pattern of the paths to the log files.' ],
                [ '-S', '--shufflingNumber', 'store', 'string', RANDOM_ITERATIONS_OPTION, None, 'The number of randomizations.' ],
                [ '-t', '--threads', 'store', 'string', THREAD_NB_COUNT_OPTION, None, 'The number of threads allocated to the SLiMProb processes.' ],
                [ '-M', '--maxsize', 'store', 'string', SLIMPROB_MAXSIZE_OPTION, None, 'The maxsize SLiMProb argument.' ],
                [ '-q', '--maxseq', 'store', 'string', SLIMPROB_MAXSEQ_OPTION, None, 'The maxseq SLiMProb argument.' ],
                [ '-g', '--minregion', 'store', 'string', SLIMPROB_MINREGION_OPTION, None, 'The minregion SLiMProb argument.' ],
                [ '-e', '--iumethod', 'store', 'string', SLIMPROB_IUMETHOD_OPTION, None, 'The iumethod SLiMProb argument.' ],
                [ '-u', '--iucut', 'store', 'string', SLIMPROB_IUCUT_OPTION, None, 'The iucut SLiMProb argument.' ],
                [ '-x', '--extras', 'store', 'string', SLIMPROB_EXTRAS_OPTION, None, 'The extras SLiMProb argument.' ],
                [ '-p', '--pickle', 'store', 'string', SLIMPROB_PICKLE_OPTION, None, 'The pickle SLiMProb argument.' ],
                [ '-d', '--savespace', 'store', 'string', SLIMPROB_SAVESPACE_OPTION, None, 'The savespace SLiMProb argument.' ] ]



# ===========================================
# Methods
# ===========================================

## run_slimprob_multithread
#  ------------------------
#
# This method allows to run SLiMProb for all the randomized fasta files of 
# one particular strain for one provided background as concurrent processes.
#
# @param elm_motifs_parsed_file: String - The path to the ELM parsed file.
# @param randomized_fasta_file_pattern: String - The pattern of the randomized fasta file.
#                                                This path must contain the {sqce_nb} string.
# @param randomized_sqces_slimprob_folder_pattern: String - The pattern of the path to the SLiMProb output directory.
#                                                           This path must contain the {sqce_nb} string.
# @param randomized_sqces_res_file_pattern: String - The pattern of the path to the occurrence file generated
#                                                    by SLiMProb. This path must contain the {sqce_nb} string.
# @param randomized_sqces_log_file_pattern: String - The pattern of the path to the log file. 
#                                                    This path must contain the {sqce_nb} string.
# @param randomization_count: Integer (>0) - The number of randomization that have been performed.
# @param maxsize: Integer (>0) - The maxsize parameter for SliMProb (see SLiMProb documentation).
# @param maxseq: Integer (>0) - The maxseq parameter for SliMProb (see SLiMProb documentation).
# @param minregion: Integer (>0) - The minregion parameter for SliMProb (see SLiMProb documentation).
# @param iumethod: String - The iumethod (long / short) parameter for SliMProb (see SLiMProb documentation).
# @param iucut: Float - The iucut parameter for SliMProb (see SLiMProb documentation).
# @param extras: Integer - Should SLiMProb generate additional output files (alignments etc.)? 0 by default.
#                          - 0 = No output beyond main results file
#                          - 1 = Saved masked input sequences [*.masked.fas]
#                          - 2 = Generate additional outputs (alignments etc.)
#                          - 3 = Additional distance matrices for input sequences
# @param pickle: String - Should SLiMProb save pickles (T/F)? F by default.
# @param savespace: Integer - Shoud SLiMProb delete the "unneccessary" files following run. 2 by default.
#                          - 0 = Delete no files
#                          - 1 = Delete all bar *.upc and *.pickle files
#                          - 2 = Delete all dataset-specific files including *.upc and *.pickle (not *.tar.gz)
#
def run_slimprob_multithread( elm_motifs_parsed_file, randomized_fasta_file_pattern, randomized_sqces_slimprob_folder_pattern, \
                              randomized_sqces_res_file_pattern, randomized_sqces_log_file_pattern, randomization_count, \
                              thread_nb, maxsize, maxseq, minregion, iumethod, iucut, extras, pickle, savespace ):
        
    # Instantiate the list of arguments
    run_slimprob_args = []
    
    # Define the SLiMProb arguments common to all processes
    slimprob_common_args = { '--motifs': elm_motifs_parsed_file,
                             '--maxsize': str( maxsize ),
                             '--maxseq': str( maxseq ),
                             '--minregion': str( minregion ),
                             '--iumethod': iumethod,
                             '--iucut': str( iucut ),
                             '--extras': str( extras ),
                             '--pickle': pickle,
                             '--savespace': str( savespace ) }
    
    # For each fasta file, start a new SLiMProb process with
    # the appropriate arguments
    for random_nb in range( randomization_count ):
        
        # Get the path of the files and folders
        seqin = randomized_fasta_file_pattern.format( sqce_nb = str( random_nb ) )
        resdir = randomized_sqces_slimprob_folder_pattern.format( sqce_nb = str( random_nb ) )
        resfile = randomized_sqces_res_file_pattern.format( sqce_nb = str( random_nb ) )
        log = randomized_sqces_log_file_pattern.format( sqce_nb = str( random_nb ) )
                
        # If the ouput file has already been created, then skip this file
        # This allows to restart the current script if something when wrong during 
        # the execution but a part of the files have been correctly generated
        if ( not os.path.exists( resfile ) ):
            
            # Complete the dictionnary of arguments to provide to SLiMProb
            slimprob_args = { '--seqin': seqin,
                              '--resdir': resdir,
                              '--resfile': resfile,
                              '--log': log }
            slimprob_args.update( slimprob_common_args )
            
            run_slimprob_args.append( slimprob_args )
            
    # Instantiate the pool 
    p = Pool( thread_nb )
    messages = p.map( run_slimprob, run_slimprob_args )
    p.close()
    
    # Wait for all processes to be completed
    p.join()
    
    for message in messages:
        if ( len( message ) != 0 ):
            print( '\n'.join( message ) )
    




## run_slimprob
#  ------------
#
# This function allows to start SLiMProb using the arguments provided.
# 
# @param run_slimprob_args: Dictionary - The arguments to use to run SLiMProb.
#
def run_slimprob( slimprob_args ):
    
    # Instantiate a list that aims to store the messages to log
    messages = []
            
    # Convert the dictionary into a list
    slimprob_args_list = []
    for ( opt, val ) in slimprob_args.items():
        slimprob_args_list += [ opt, val ]
    
    # Run SLiMProb with the arguments provided and check the program
    # did not return a non zero exit code
    slimprob_command = [ 'bash', 'compute_slim_probability/script/run_slimprob.sh' ] + slimprob_args_list
    
    # Run the process
    # If the process returns an error message, then log it and remove
    # the occurrence file and the SLiMProb folder created.
    run_slimprob = subprocess.Popen( slimprob_command, 
                                     stdout = subprocess.PIPE,
                                     stderr = subprocess.PIPE )
    ( stdout, stderr ) = run_slimprob.communicate()
    
    if ( stderr != '' ):
        slimprob_param = []
        for ( param, value ) in slimprob_args.items():
            slimprob_param.append( param + ' ' + value )
        messages.append( 'ERROR :: The execution of SLiMProb with the following parameters:\n' +
               '\n'.join( slimprob_param ) + '\nreturned the error message:\n' +
               str( stderr ) + 'The files already created by SLiMProb will be removed.' )
        # Remove the occurrence file created
        if os.path.exists( slimprob_args.get( '--resdir' ) ):
            shutil.rmtree( slimprob_args.get( '--resdir' ) )
            
    return messages
                



# ===========================================
# Parse options and run script
# ===========================================

if __name__ == '__main__':
    
    ## Command-line arguments are parsed.
    # Store the various option values into a dictionary
    optionParser = OptionParser()    
    for current_opt in OPTION_LIST:
        optionParser.add_option( current_opt[0],
                                 current_opt[1],
                                 action = current_opt[2],
                                 type = current_opt[3],
                                 dest = current_opt[4],
                                 default = current_opt[5],
                                 help = current_opt[6] )
    (opts, args) = optionParser.parse_args()
    option_dict = vars(opts)
    
    # Get the path to the ELM motifs parsed file
    elm_motifs_parsed_file = option_dict.get( ELM_MOTIFS_PARSED_FILE_OPTION )
    if not elm_motifs_parsed_file:
        raise Exception( 'The path to the ELM parsed file has to be provided.' )

    # Get the pattern of the path to the randomized sequences
    randomized_fasta_file_pattern = option_dict.get( RANDOMIZED_FASTA_FILE_PATTERN_OPTION )
    if randomized_fasta_file_pattern:
        randomized_fasta_file_pattern = randomized_fasta_file_pattern.replace( '[', '{' ).replace( ']', '}' )
        if ( '{sqce_nb}' not in randomized_fasta_file_pattern ):
            raise Exception( 'The "schema" of the path to the randomized sequences fasta files' +
                             ' has to contain "{sqce_nb}".' )
    else:
        raise Exception( 'The "schema" of the path to the randomized sequences fasta files' +
                         ' has to be provided.' )

    # Get the pattern of the path to the randomized sequence SLiMProb folder
    randomized_sqces_slimprob_folder_pattern = option_dict.get( RANDOMIZED_SQCE_SLIMPROB_FOLDER_PATTERN_OPTION )
    if randomized_sqces_slimprob_folder_pattern:
        randomized_sqces_slimprob_folder_pattern = randomized_sqces_slimprob_folder_pattern.replace( '[', '{' ).replace( ']', '}' )
        if ( '{sqce_nb}' not in randomized_sqces_slimprob_folder_pattern ):
            raise Exception( 'The "schema" of the path to the randomized sequences SLiMProb folder' +
                             ' has to contain "{sqce_nb}".' )
    else:
        raise Exception( 'The "schema" of the path to the randomized sequences SLiMProb folder' +
                         ' has to be provided.' )

    # Get the pattern of the path to the occurrence file
    randomized_sqces_res_file_pattern = option_dict.get( OCCURENCE_FILE_PATTERN_OPTION )
    if randomized_sqces_res_file_pattern:
        randomized_sqces_res_file_pattern = randomized_sqces_res_file_pattern.replace( '[', '{' ).replace( ']', '}' )
        if ( '{sqce_nb}' not in randomized_sqces_res_file_pattern ):
            raise Exception( 'The "schema" of the path to the randomized occurrence file' +
                             ' has to contain "{sqce_nb}".' )
    else:
        raise Exception( 'The "schema" of the path to the randomized occurrence file has to be provided.' )

    # Get the pattern of the path to the occurrence file
    randomized_sqces_log_file_pattern = option_dict.get( LOG_FILE_PATTERN_OPTION )
    if randomized_sqces_log_file_pattern:
        randomized_sqces_log_file_pattern = randomized_sqces_log_file_pattern.replace( '[', '{' ).replace( ']', '}' )
        if ( '{sqce_nb}' not in randomized_sqces_res_file_pattern ):
            raise Exception( 'The "schema" of the path to the randomized SLiMProb log file' +
                             ' has to contain "{sqce_nb}".' )
    else:
        raise Exception( 'The "schema" of the path to the randomized SLiMProb log file has to be provided.' )

    # Get the number of randomization
    randomization_count = option_dict.get( RANDOM_ITERATIONS_OPTION )
    if randomization_count:
        try:
            randomization_count = int( randomization_count )
        except:
            raise Exception( 'The randomization count has to be an integer.' )
        else:
            if ( randomization_count <= 0 ):
                raise Exception( 'The randomization count has to be a positive integer.' )
    else:
        raise Exception( 'The randomization count has to be provided.' )

    # Get the number of threads
    thread_nb = option_dict.get( THREAD_NB_COUNT_OPTION )
    if thread_nb:
        try:
            thread_nb = int( thread_nb )
        except:
            raise Exception( 'The number of threads has to be an integer.' )
        else:
            if ( thread_nb <= 0 ):
                raise Exception( 'The number of threads has to be a positive integer.' )
    else:
        thread_nb = 1

    # Get the SLiMProb options
    maxsize = option_dict.get( SLIMPROB_MAXSIZE_OPTION )
    if maxsize:
        try:
            maxsize = int( maxsize )
        except:
            raise Exception( 'The maxsize has to be an integer.' )
        else:
            if ( maxsize <= 0 ):
                raise Exception( 'The maxsize has to be a positive integer.' )
    else:
        raise Exception( 'The maxsize has to be provided.' )
    
    maxseq = option_dict.get( SLIMPROB_MAXSEQ_OPTION )
    if maxseq:
        try:
            maxseq = int( maxseq )
        except:
            raise Exception( 'The maxseq has to be an integer.' )
        else:
            if ( maxseq <= 0 ):
                raise Exception( 'The maxseq has to be a positive integer.' )
    else:
        raise Exception( 'The maxseq has to be provided.' )
    
    minregion = option_dict.get( SLIMPROB_MINREGION_OPTION )
    if minregion:
        try:
            minregion = int( minregion )
        except:
            raise Exception( 'The minregion has to be an integer.' )
        else:
            if ( minregion <= 0 ):
                raise Exception( 'The minregion has to be a positive integer.' )
    else:
        raise Exception( 'The minregion has to be provided.' )
    
    iumethod = option_dict.get( SLIMPROB_IUMETHOD_OPTION )
    if not iumethod:
        raise Exception( 'The iumethod has to be provided.' )
    
    iucut = option_dict.get( SLIMPROB_IUCUT_OPTION )
    if iucut:
        try:
            iucut = float( iucut )
        except:
            raise Exception( 'The iucut has to be a float.' )
        else:
            if ( ( iucut < 0 ) or ( iucut > 1 ) ):
                raise Exception( 'The iucut has to be a float between 0 and 1.' )
    else:
        raise Exception( 'The iucut has to be provided.' )
        
    extras = option_dict.get( SLIMPROB_EXTRAS_OPTION )
    if extras:
        if ( str( extras ) not in [ '0', '1', '2', '3' ] ):
            raise Exception( 'The extras parameter has to be an integer between 0 and 3.' )
    else:
        extras = DEFAULT_SLIMPROB_EXTRAS
    
    pickle = option_dict.get( SLIMPROB_PICKLE_OPTION )
    if pickle:
        if ( pickle not in [ 'T', 'F' ] ):
            raise Exception( 'The pickle parameter has to be a boolean equal to "T" or "F".' )
    else:
        pickle = DEFAULT_SLIMPROB_PICKLE
    
    savespace = option_dict.get( SLIMPROB_SAVESPACE_OPTION )
    if savespace:
        if ( str( savespace ) not in [ '0', '1', '2' ] ):
            raise Exception( 'The savespace parameter has to be an integer between 0 and 2.' )
    else:
        pickle = DEFAULT_SLIMPROB_SAVESPACE   
    
    # Compute the SLiM likelihoods
    print( datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S') +
           ':: INFO :: Starting the SLiMProb subprocesses' )
    print( 'DEBUG :: Number of threads available: ' + str( thread_nb ) )
    start_time = time.time()
    run_slimprob_multithread( elm_motifs_parsed_file = elm_motifs_parsed_file, 
                              randomized_fasta_file_pattern = randomized_fasta_file_pattern, 
                              randomized_sqces_slimprob_folder_pattern = randomized_sqces_slimprob_folder_pattern,
                              randomized_sqces_res_file_pattern = randomized_sqces_res_file_pattern,
                              randomized_sqces_log_file_pattern = randomized_sqces_log_file_pattern, 
                              randomization_count = randomization_count, 
                              thread_nb = thread_nb,
                              maxsize = maxsize, 
                              maxseq = maxseq, 
                              minregion = minregion, 
                              iumethod = iumethod, 
                              iucut = iucut,
                              extras = extras,
                              pickle = pickle,
                              savespace = savespace )
    print( datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S') +
           ':: INFO :: The SLiMProb subprocesses has finished (' + 
           str( round( time.time() - start_time, 2 ) ) + ' seconds)\n'  )
    