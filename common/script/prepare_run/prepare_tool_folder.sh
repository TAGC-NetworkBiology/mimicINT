#!/bin/bash

# This script allows to copy the IUPred executable files
# (compiled during the creation of the tagc-mimicint-slim-detect image)
# into the tools/iupred subfolder. This is necessary in order to 
# run the detect_slim_query rule properly. 

# Create a tools folder
if [ ! -f "tools" ]
then 
	mkdir tools
fi

# Create a iupred folder and copy the IUPred executables 
# from the tagc-mimicint-slim-detect singularity image
if [ ! -d "tools/iupred" ]
then
	singularity exec -B $(pwd)/tools:$(pwd)/tools \
	            common/Docker/slim_detect/tagc-mimicint-slim-detect.img \
	            cp -R /iupred $(pwd)/tools
fi
