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
sudo singularity build ${SINGULARITY_IMAGE_DATAPARSE}.sif docker-daemon://${SINGULARITY_IMAGE_DATAPARSE}:latest
sudo chown $(whoami):$(whoami) ${SINGULARITY_IMAGE_DATAPARSE}.sif

  
# Domain detect
docker build -t ${SINGULARITY_IMAGE_DOMAINDETECT} ${DOMAINDETECT_DOCKERFILE_DIR}
sudo singularity build ${SINGULARITY_IMAGE_DOMAINDETECT}.sif docker-daemon://${SINGULARITY_IMAGE_DOMAINDETECT}:latest
sudo chown $(whoami):$(whoami) ${SINGULARITY_IMAGE_DOMAINDETECT}.sif

# SLiM detect
docker build -t ${SINGULARITY_IMAGE_SLIMDETECT} ${SLIMDETECT_DOCKERFILE_DIR}
sudo singularity build ${SINGULARITY_IMAGE_SLIMDETECT}.sif docker-daemon://${SINGULARITY_IMAGE_SLIMDETECT}:latest
sudo chown $(whoami):$(whoami) ${SINGULARITY_IMAGE_SLIMDETECT}.sif
  
# R
docker build -t ${SINGULARITY_IMAGE_R} ${R_DOCKERFILE_DIR}
sudo singularity build ${SINGULARITY_IMAGE_R}.sif docker-daemon://${SINGULARITY_IMAGE_R}:latest
sudo chown $(whoami):$(whoami) ${SINGULARITY_IMAGE_R}.sif

# Rstudio
docker build -t ${SINGULARITY_IMAGE_RSTUDIO} ${RSTUDIO_DOCKERFILE_DIR}
sudo singularity build ${SINGULARITY_IMAGE_RSTUDIO}.sif docker-daemon://${SINGULARITY_IMAGE_RSTUDIO}:latest
sudo chown $(whoami):$(whoami) ${SINGULARITY_IMAGE_RSTUDIO}.sif
 
  
# Miscellaneous
# Graphviz
docker build -t ${SINGULARITY_IMAGE_GRAPHVIZ} ${GRAPHVIZ_DOCKERFILE_DIR}
sudo singularity build ${SINGULARITY_IMAGE_GRAPHVIZ}.sif docker-daemon://${SINGULARITY_IMAGE_GRAPHVIZ}:latest
sudo chown $(whoami):$(whoami) ${SINGULARITY_IMAGE_GRAPHVIZ}.sif

