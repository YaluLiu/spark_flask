#!/usr/bin/env bash

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
source "${PROJECT_DIR}/docker/spark_apollo.bashrc"

docker exec \
    -it "${SPARK_CONTAINER}" \
    /bin/bash
