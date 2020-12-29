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
    docker logs -ft ${SPARK_CONTAINER}
    # docker exec -it "${SPARK_CONTAINER}" bash
}

function clean_container() {
    docker stop ${SPARK_CONTAINER} 
    docker rm ${SPARK_CONTAINER}
}


function create_image() {
    cd docker
    if [[ "$(docker images -q ${SPARK_ENV_IMAGE} 2> /dev/null)" == "" ]]; 
    then
        set -x
        docker pull ${DOCKER_HUB_USER}/${SPARK_ENV_IMAGE}
        docker tag ${DOCKER_HUB_USER}/${SPARK_ENV_IMAGE} ${SPARK_ENV_IMAGE}
        set +x
    else
        log "alreay found ENV_IMAGE:${SPARK_ENV_IMAGE}."
    fi

    if [[ "$(docker images -q ${SPARK_IMAGE} 2> /dev/null)" == "" ]]; 
    then
        set -x
        docker build -t ${SPARK_IMAGE} .
        set +x
    else
        log "alreay found WORK_IMAGE:${SPARK_IMAGE},delete it and rebuild."
        set -x
        docker rmi ${SPARK_IMAGE}
        docker build -t ${SPARK_IMAGE} .
        set +x
    fi

    
    cd ..
    
    if [ $? -ne 0 ]; then
        error "Failed to build ${SPARK_IMAGE}!"
        exit 1
    fi
    
}

function check_clean_container(){
    state_run=`docker ps | grep ${SPARK_CONTAINER} | grep Up`
    state_stop=`docker ps -a| grep ${SPARK_CONTAINER} | grep Exist`
    # echo $state_run  ${#state_run}
    # echo $state_stop ${#state_stop}

    if [[ -n $state_run ]]; then # state is run
        clean_container
    elif [[ -n $state_stop ]]; then # state is stop
        docker rm ${SPARK_CONTAINER}
    fi
}

function start_work() {
    check_clean_container
    set -x
    ${DOCKER_RUN} \
        -p ${SPARK_PORT}:${SPARK_PORT} \
        -v ${PROJECT_DIR}:${DOCKER_ROOT_DIR} \
        --name "${SPARK_CONTAINER}" \
        --restart=always \
        "${SPARK_IMAGE}"
    set +x

    if [ $? -ne 0 ]; then
        error "Failed to start docker container \"${SPARK_CONTAINER}\" based on image: ${SPARK_IMAGE}"
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
        create_image
        start_work
    fi
    if [ $1 == "test" ]; then
        echo "test"
    fi
}

main "$@"