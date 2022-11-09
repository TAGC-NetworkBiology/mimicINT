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
echo "- MimicInt workflow started on $(date "+%d/%m/%y, at %H:%M:%S")" >> readme.txt
echo "- InterProScan version 5.52-86.0" >> readme.txt
echo "- SLiMSuite version 1.4.0" >> readme.txt
echo "- Blast+ version 2.7.1" >> readme.txt
echo "- Provided arguments: $@" >> readme.txt
echo "" >> readme.txt

# Generate the views of the pipeline's graphs
bash common/script/miscellaneous/plot_rulegraph.sh mimicINT_InterPro/workflow/mimicint_interpro_snakefile mimicINT_InterPro/docs/mimicint_snakefile_rulegraph.png

# DAG
bash common/script/miscellaneous/plot_dag.sh mimicINT_InterPro/workflow/mimicint_interpro_snakefile mimicINT_InterPro/docs/mimicint_snakefile_dag.png

echo "NB: The rules parse_elm and detect_slim_query do not appear on the rule graph and DAG\
	  as their execution depends on the rule split_query_dataset."
  


# =========================================================
# Run the workflow
# =========================================================

# Run the pipeline
# Please adapt the following lines of code depending your needs
# and the environment in which you are running the mimicINT randomization
# workflow (workstation, HPC, cloud)
snakemake --snakefile mimicINT_InterPro/workflow/mimicint_interpro_snakefile \
  --reason \
  --use-singularity \
  --singularity-args="-B $RUN_FOLDER:$RUN_FOLDER \
  					  -B $RUN_FOLDER/tools/iupred:/iupred" \
  --jobs 20 \
  --latency-wait 20 \
  --max-jobs-per-second 5 \
  --max-status-checks-per-second 5 \
  --cluster-config mimicINT_InterPro/config/config_cluster.json \
  --cluster 'sbatch -A {cluster.project} \
                  --job-name {cluster.job-name} \
                  --partition {cluster.partition} \
                  --time {cluster.time} \
              	  --mem {cluster.mem} \
          		  -c {threads} \
                  --mail-user {cluster.mail-user} \
                  --mail-type {cluster.mail-type} \
                  --error {cluster.error} \
                  --output {cluster.output}' \
  $@
  