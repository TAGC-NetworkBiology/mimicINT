#!/bin/bash

# This script needs to be started from the 
# appropriate run directory

# It may eventually be necessary to add lines to activate
# the appropriate Python environment and/or to load modules
# on the HPC.

# =========================================================
# Parsing the command line
# =========================================================

# Parse the command line arguments
if [ "$#" -ge 1 ]
then
	printf "The following command line arguments will be used as snakemake arguments: \n \
		    $@\n"
fi



# =========================================================
# Prepare the Run
# =========================================================

# Get the Run folder path
RUN_FOLDER=$(pwd)

# Create the tools folder if necessary
bash common/script/prepare_run/prepare_tool_folder.sh

# Add informations about the run to the readme
echo "# ==================================================" >> readme.txt
echo "- MimicInt SLiM likelihood computation workflow started on $(date "+%d/%m/%y, at %H:%M:%S")" >> readme.txt
echo "- SLiMSuite version 1.4.0" >> readme.txt
echo "- Blast+ version 2.7.1" >> readme.txt
echo "- Provided arguments: $@" >> readme.txt
echo "" >> readme.txt

# Generate the views of the pipeline's graphs
echo "The Snakemake rulegraph and DAG will not be generated as this could take a long time..."
echo "If you need them, then you can generate them running the following commands:\n\
	  bash common/script/miscellaneous/plot_rulegraph.sh compute_slim_probability/workflow/comp_slim_proba_snakefile compute_slim_probability/docs/comp_slim_proba_snakefile_rulegraph.png \n\
	  bash common/script/miscellaneous/plot_dag.sh compute_slim_probability/workflow/comp_slim_proba_snakefile compute_slim_probability/docs/comp_slim_proba_snakefile_dag.png \n"


  
# =========================================================
# Run the workflow
# =========================================================

# Run the pipeline
# Please adapt the following lines of code depending your needs
# and the environment in which you are running the mimicINT randomization
# workflow (workstation, HPC, cloud)
snakemake --snakefile compute_slim_probability/workflow/comp_slim_proba_snakefile \
  --reason \
  --use-singularity \
  --singularity-args="-B $RUN_FOLDER:$RUN_FOLDER \
  					  -B $RUN_FOLDER/tools/iupred:/iupred" \
  --jobs 14 \
  --latency-wait 20 \
  --max-jobs-per-second 5 \
  --max-status-checks-per-second 5 \
  --cluster-config compute_slim_probability/config/config_cluster.json \
  --cluster 'sbatch -A {cluster.project} \
                  --job-name {cluster.job-name} \
                  --partition {cluster.partition} \
                  --time {cluster.time} \
                  --mincpus {cluster.mincpus} \
                  -N {cluster.nodes-number} \
                  --ntasks-per-core {cluster.ntasks-per-core} \
                  --hint {cluster.hint} \
                  --mem-per-cpu {cluster.mem-per-cpu} \
                  --output {cluster.output} \
                  --error {cluster.error} \
                  --mail-user {cluster.mail-user} \
                  --mail-type {cluster.mail-type}' \
  $@
