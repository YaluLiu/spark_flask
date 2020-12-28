#!/usr/bin/env bash

###############################################################################
# NAME: MONGO_FLASK_DOCKER_DEMO
# maintainer: lyl,ymh
###############################################################################

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
source "${PROJECT_DIR}/docker/spark_apollo.bashrc"


function clean_container() {
    set -x
    docker stop ${MONGO_CONTAINER} 
    docker rm ${MONGO_CONTAINER}
    set +x

    if [ $? -ne 0 ]; then
        error "Failed to delete container: ${MONGO_CONTAINER}, image: ${MONGO_IMAGE}"
        exit 1
    fi
}

function create_image() {
    set -x
    docker pull ${MONGO_IMAGE}
    set +x

    if [ $? -ne 0 ]; then
        error "Failed to pull image,please check it!"
        exit 1
    fi
    
}

function start_work() {
    set -x

    ${DOCKER_RUN} \
        -p ${MONGO_PORT}:${MONGO_PORT} \
        --name "${MONGO_CONTAINER}" \
        --restart=always \
        "${MONGO_IMAGE}"
    set +x

    if [ $? -ne 0 ]; then
        error "Failed to start docker container \"${MONGO_CONTAINER}\" based on image: ${MONGO_IMAGE}"
        exit 1
    fi
    
}


function main() {
    if [ $# != 1 ] ; then
        echo "please input cmd: create(for build/pull image) or clean(clean container) or start(for run the container)"
        exit 1;
    fi
    if [ $1 == "create" ]; then
        create_image
    fi
    if [ $1 == "clean" ]; then
        clean_container
    fi
    if [ $1 == "start" ]; then
        start_work
    fi
}

main "$@"