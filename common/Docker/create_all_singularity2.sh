#!/bin/bash

# This script allows to prepare all the singularity images
# necessary to run the Mimicint pipeline.

# Get the working directory / workspace
MIMICINT_WORKING_DIR=$(pwd)



# =========================================================
# Constants
# =========================================================

# Container directory
CONTAINER_DIR=${MIMICINT_WORKING_DIR}/common/Docker

# Singularity images to generate
# Data parse
DATAPARSE_DOCKERFILE_DIR=${CONTAINER_DIR}/data_parse
DATAPARSE_DOCKER_TAG=latest
SINGULARITY_IMAGE_DATAPARSE=tagc-mimicint-data-parse

# Domain detect
DOMAINDETECT_DOCKERFILE_DIR=${CONTAINER_DIR}/domain_detect
DOMAINDETECT_DOCKER_TAG=latest
SINGULARITY_IMAGE_DOMAINDETECT=tagc-mimicint-domain-detect

# SLiM detect
SLIMDETECT_DOCKERFILE_DIR=${CONTAINER_DIR}/slim_detect
SLIMDETECT_DOCKER_TAG=latest
SINGULARITY_IMAGE_SLIMDETECT=tagc-mimicint-slim-detect

# R (includes gprofiler2)
R_DOCKERFILE_DIR=${CONTAINER_DIR}/R
R_DOCKER_TAG=latest
SINGULARITY_IMAGE_R=tagc-mimicint-r

# Rstudio (necessary for compute_slim_probability)
RSTUDIO_DOCKERFILE_DIR=${CONTAINER_DIR}/Rstudio
RSTUDIO_DOCKER_TAG=latest
SINGULARITY_IMAGE_RSTUDIO=tagc-mimicint-rstudio

# Miscellaneous (not mandatory, only necessary for some optional scripts)
MISC_DOCKERFILE_DIR=${CONTAINER_DIR}/miscellaneous
# Graphviz (necessary to plot rule graphs and DAGs)
GRAPHVIZ_DOCKERFILE_DIR=${MISC_DOCKERFILE_DIR}/graphviz
GRAPHVIZ_DOCKER_TAG=latest
SINGULARITY_IMAGE_GRAPHVIZ=tagc-mimicint-misc-graphviz


# =========================================================
# Create the singularity images
# =========================================================

# Data parse
docker build -t ${SINGULARITY_IMAGE_DATAPARSE} ${DATAPARSE_DOCKERFILE_DIR}
bash ${CONTAINER_DIR}/docker_to_singularity.sh \
  ${DATAPARSE_DOCKERFILE_DIR} \
  ${SINGULARITY_IMAGE_DATAPARSE} \
  ${DATAPARSE_DOCKER_TAG} \
  ${SINGULARITY_IMAGE_DATAPARSE}
  
# Domain detect
docker build -t ${SINGULARITY_IMAGE_DOMAINDETECT} ${DOMAINDETECT_DOCKERFILE_DIR}
bash ${CONTAINER_DIR}/docker_to_singularity.sh \
  ${DOMAINDETECT_DOCKERFILE_DIR} \
  ${SINGULARITY_IMAGE_DOMAINDETECT} \
  ${DOMAINDETECT_DOCKER_TAG} \
  ${SINGULARITY_IMAGE_DOMAINDETECT}

# SLiM detect
docker build -t ${SINGULARITY_IMAGE_SLIMDETECT} ${SLIMDETECT_DOCKERFILE_DIR}
bash ${CONTAINER_DIR}/docker_to_singularity.sh \
  ${SLIMDETECT_DOCKERFILE_DIR} \
  ${SINGULARITY_IMAGE_SLIMDETECT} \
  ${SLIMDETECT_DOCKER_TAG} \
  ${SINGULARITY_IMAGE_SLIMDETECT}
  
# R
docker build -t ${SINGULARITY_IMAGE_R} ${R_DOCKERFILE_DIR}
bash ${CONTAINER_DIR}/docker_to_singularity.sh \
  ${R_DOCKERFILE_DIR} \
  ${SINGULARITY_IMAGE_R} \
  ${R_DOCKER_TAG} \
  ${SINGULARITY_IMAGE_R}

# Rstudio
docker build -t ${SINGULARITY_IMAGE_RSTUDIO} ${RSTUDIO_DOCKERFILE_DIR}
bash ${CONTAINER_DIR}/Docker/docker_to_singularity.sh \
  ${RSTUDIO_DOCKERFILE_DIR} \
  ${SINGULARITY_IMAGE_RSTUDIO} \
  ${RSTUDIO_DOCKER_TAG} \
  ${SINGULARITY_IMAGE_RSTUDIO}
  
# Miscellaneous
# Graphviz
docker build -t ${SINGULARITY_IMAGE_GRAPHVIZ} ${GRAPHVIZ_DOCKERFILE_DIR}
bash ${CONTAINER_DIR}/docker_to_singularity.sh \
  ${GRAPHVIZ_DOCKERFILE_DIR} \
  ${SINGULARITY_IMAGE_GRAPHVIZ} \
  ${GRAPHVIZ_DOCKER_TAG} \
  ${SINGULARITY_IMAGE_GRAPHVIZ}
