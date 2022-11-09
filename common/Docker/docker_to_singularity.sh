#!/bin/bash

# This script allows to convert a docker image 
# into a singularity image.


# =========================================================
# Parsing the command line
# =========================================================

# Check the number of argument provided is the one expected
if [ "$#" -ne 4 ]
then
    printf "The following command line argument is expected to be provided:\n
            - The directory of the container\n
            - The docker image name\n
            - The docker tag\n
            - The singularity image name"
    exit
fi

# Get the arguments
CONTAINER_DIR=$1
DOCKER_IMAGE_NAME=$2
DOCKER_TAG=$3
SINGULARITY_FILENAME=$4


# =========================================================
# Create the singularity image
# =========================================================

## Create the singularity file
# Display the size of the docker image
echo "$( docker image ls | grep $DOCKER_IMAGE_NAME | grep $DOCKER_TAG )"
# Ask the user the size of the singularity file
echo "Please enter the size of the Singularity image (in MB):"
read singularity_image_size
  
# Create singularity file
# Create the Singularity file
sudo singularity image.create --size ${singularity_image_size} ${SINGULARITY_FILENAME}.img
# Start the Docker container
docker run --name ${SINGULARITY_FILENAME} -d ${DOCKER_IMAGE_NAME}:${DOCKER_TAG} sleep 1800
# Convert the container to Singularity
docker export ${SINGULARITY_FILENAME} | sudo singularity image.import ${SINGULARITY_FILENAME}.img
sudo chown $(whoami):$(id -g) ${SINGULARITY_FILENAME}.img
# Stop and remove the Docker container
docker stop ${SINGULARITY_FILENAME}
docker rm ${SINGULARITY_FILENAME}

## Move the singularity file to the Run folder
if [ -f ${CONTAINER_DIR}/${SINGULARITY_FILENAME}.img ]
then
  echo "A singularity file called $(echo ${SINGULARITY_FILENAME}).img already exists in the Run folder. Do you want to overwrite it? (Y/N)"
  read overwrite_existing_singularity_file
  if [ "$overwrite_existing_singularity_file" == "Y" ]
  then
    echo "Copying the singularity file in the Run folder"
    cp ./${SINGULARITY_FILENAME}.img ${CONTAINER_DIR}
  fi
else
  echo "Copying the singularity file in the Run folder"
  cp ./${SINGULARITY_FILENAME}.img ${CONTAINER_DIR}
fi

# Remove the singularity file from the current folder
rm ./${SINGULARITY_FILENAME}.img
