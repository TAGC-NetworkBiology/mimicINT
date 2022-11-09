#!/bin/bash

# Parse the command line arguments
if [ "$#" -ne 2 ]
then
  printf "The following arguments needs to be provided: \n \
		  - The path to the snakefile\n\
	      - The path of the output png file\n"
  exit
fi

SNAKEFILE=$1
PNGFILE=$2

# Plot the DAG
snakemake --dag --snakefile $SNAKEFILE | \
  singularity exec -B $(pwd):$(pwd) common/Docker/miscellaneous/graphviz/tagc-mimicint-misc-graphviz.img dot -Tpng \
  > $PNGFILE
  