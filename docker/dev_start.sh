#!/usr/bin/env bash

###############################################################################
# NAME: SPARK_FLASK_DOCKER_DEMO
# maintainer: lyl,ymh
###############################################################################

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
source "${PROJECT_DIR}/docker/spark_apollo.bashrc"

function print_debug {
    env "FILE_NAME:" ${BASH_SOURCE[0]}
    env "PROJECT_DIR:" ${PROJECT_DIR}
    env "USER:" ${USER}
}

function post_run_setup() {
    set -x
    docker exec -it "${CONTAINER_NAME}" bash
    set +x

    if [ $? -ne 0 ]; then
        error "Failed to get into docker container \"${CONTAINER_NAME}\" based on image: ${IMAGE_NAME}"
        exit 1
    fi
}

function clean_container() {
    set -x
    docker stop ${CONTAINER_NAME} 
    docker rm ${CONTAINER_NAME}
    docker rmi ${IMAGE_NAME}
    set +x

    if [ $? -ne 0 ]; then
        error "Failed to start docker container \"${CONTAINER_NAME}\" based on image: ${IMAGE_NAME}"
        exit 1
    fi
}

function create_image() {
    set -x
    cd docker
    docker build -t ${IMAGE_NAME} .
    docker build -t ${IMAGE_NAME} .
    cd ..
    set +x

    if [ $? -ne 0 ]; then
        error "Failed to start docker container \"${APOLLO_DEV}\" based on image: ${APOLLO_DEV_IMAGE}"
        exit 1
    fi
    
}

function start_work() {
    set -x

    ${DOCKER_RUN} \
        -p ${PORT}:${PORT} \
        -v ${PROJECT_DIR}:${DOCKER_ROOT_DIR} \
        --name "${CONTAINER_NAME}" \
        --restart=always \
        "${IMAGE_NAME}"
    set +x

    if [ $? -ne 0 ]; then
        error "Failed to start docker container \"${APOLLO_DEV}\" based on image: ${APOLLO_DEV_IMAGE}"
        exit 1
    fi
    
}


function main() {
    if [ $# != 1 ] ; then
        echo "please input cmd: create or clean or start"
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
        post_run_setup
    fi
}

main "$@"