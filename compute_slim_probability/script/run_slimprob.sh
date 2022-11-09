#!/bin/bash

# This script allows to run SLiMProb, using the appropriate
# command line depending on the options provided

# ===============================================================================
# Information about the SLiMProb options
# ===============================================================================

# Extensive information about the options may be found at:
# - https://github.com/slimsuite/SLiMSuite/blob/master/docs/manuals/SLiMProb%20Manual.pdf
# - https://github.com/slimsuite/SLiMSuite/blob/master/libraries/rje.py
# 
#
# Common options
# --------------
#
# - Input and output files
#   - motifs: Path to the input ELM motifs file.
#   - seqin: Path to the sequences (.fasta) file.
#   - batch: List of files (.fasta) containing the sequences (over-rules by seqin).
#   - resdir: Path to individual output directory (and intermediates directory).
#   - buildpath: Path to intermediates directory.
#   - resfile: SLiMProb result file.
# 	- log: SLiMProb log file.
# 
# - Paths to binaries and executables
#   - blastpath and blast+path: Path to BLAST files.
#   - iupath: Path to IUPred executable.
#
# - General options
#   - walltime=0: Disable abortion of the program after a pre-defined time.
#   - i=-1: Run the program in full-auto mode (not interactive mode).
#   - maxsize: Maximum dataset size to process in amino acids.
#   - maxseq: Maximum number of sequences to process. If batch option used, the maxseq 
#             option can be used to limit which files are actually searched.
#   - newlog=T: Create new log file.
#
# - Disorder masking
#   - masking=T: Turn on all masking.
#   - dismask=T: Mask ordered regions.
#   - minregion: Minimum number of consecutive residues that must 
#				 have the same disorder state.
#
# - Blast
#	- efilter=F: Disable the use of evolutionary filter.
#
# - IUPred
#	- iumethod: IUPred method to use (long/short).
#   - iucut: Cut-off for IUPred results.
#
# - Additional SLiM calculations
#   - slimcalc: List of additional statistics to calculate for occurrences, 
# 				(Cons,SA,Hyd,Fold,IUP,Chg,Comp).
#



# ===============================================================================
# Parsing the command line arguments
# ===============================================================================

echo "DEBUG :: Arguments provided $@"

# Allowed options
# - motifs: String - Path to the motifs file (motifs).
# - seqin: String - Path to shuffled sequences fasta file (seqin).
# - resdir: Path to individual output directory (and intermediates directory).
# - resfile: String - Path to SLiMProb result file (resfile).
# - log: String - Path to the SLiMProb log file (log).
# - maxsize: Integer - Maximum dataset size to process in aa (maxsize).
# - maxseq: Integer - Maximum number of sequences to process (maxseq).
# - minregion: Integer - Minimum number of consecutive residues that
# 						 must have the same disorder state (minregion).
# - iumethod: IUPred method to use (long/short).
# - iucut: Float - Cut-off for IUPred results (iucut).
OPTIONS_LIST=(
  "motifs"
  "seqin"
  "resdir"
  "resfile"
  "log"
  "maxsize"
  "maxseq"
  "minregion"
  "iumethod"
  "iucut"
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
        --motifs)
            elm_motifs_parsed_file=$2
            shift 2
            ;;
            
        --seqin)
            sqce_fasta_file=$2
            shift 2
            ;;
            
        --resdir)
            slim_slimprob_out_dir=$2
            shift 2
            ;;
            
        --resfile)
            slim_slimprob_res=$2
            shift 2
            ;;
            
        --log)
            slimprob_log_file=$2
            shift 2
            ;;    
            
        --maxsize)
            maxsize=$2
            shift 2
            ;;
            
        --maxseq)
            maxseq=$2
            shift 2
            ;;
            
        --minregion)
            minregion=$2
            shift 2
            ;;
            
        --iumethod)
        	iumethod=$2
        	shift 2
        	;;
            
        --iucut)
            iucut=$2
            shift 2
            ;;

        *)
            break
            ;;
    esac
done



# ===============================================================================
# Running SLiMProb using the appropriate options
# ===============================================================================

# Define environment variables
# ----------------------------
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
export IUPred_PATH=/iupred
export BLAST_PATH=/usr/ncbi-blast-2.7.1+/bin


# Run SLiMProb
# ------------

printf "SLiMProb will be run using the following options: \n\
             - motifs: $elm_motifs_parsed_file \n\
             - seqin: $sqce_fasta_file \n\
             - resdir: $slim_slimprob_out_dir \n\
             - resfile: $slim_slimprob_res \n\
             - logile: $slimprob_log_file \n\
             - maxsize: $maxsize \n\
             - maxseq: $maxseq \n\
             - minregion: $minregion \n\
             - iumethod: $iumethod \n\
             - iucut: $iucut \n"

python2.7 /SLiMSuite/slimsuite/tools/slimprob.py \
  motifs=$elm_motifs_parsed_file \
  seqin=$sqce_fasta_file \
  resdir=$slim_slimprob_out_dir \
  buildpath=$slim_slimprob_out_dir \
  resfile=$slim_slimprob_res \
  log=$slimprob_log_file \
  newlog=T \
  blastpath=$BLAST_PATH \
  blast+path=$BLAST_PATH \
  iuchdir=T \
  iupath=/$IUPred_PATH/iupred \
  walltime=0 \
  i=-1 \
  maxsize=$maxsize \
  maxseq=$maxseq \
  masking=T \
  dismask=T \
  minregion=$minregion \
  iumethod=$iumethod \
  efilter=F \
  iucut=$iucut \
  slimcalc=IUP,Comp
