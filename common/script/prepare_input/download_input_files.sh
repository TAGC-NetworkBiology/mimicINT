#/bin/bash!

RUN_DIRECTORY=$(pwd)


# Constants
INPUT_DIR=${RUN_DIRECTORY}/input


# Create the input directory if necessary
mkdir -p ${INPUT_DIR}


# Download 3did file
wget -O ${INPUT_DIR}/3did_flat.gz https://3did.irbbarcelona.org/download/current/3did_flat.gz
gunzip ${INPUT_DIR}/3did_flat.gz -d ${INPUT_DIR}


# Download ELM files
# ELM classes
wget -O ${INPUT_DIR}/elm_classes.tsv http://elm.eu.org/elms/elms_index.tsv
# ELM instances
wget -O ${INPUT_DIR}/elm_instances.tsv elm.eu.org/instances.tsv?q=None&taxon=Homo%20sapiens&instance_logic=true%20positive
# ELM interaction domains
wget -O ${INPUT_DIR}/elm_interaction_domains.tsv http://elm.eu.org/infos/browse_elm_interactiondomains.tsv
