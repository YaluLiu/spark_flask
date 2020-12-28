#!/usr/bin/env bash

###############################################################################
# Copyright 2020 The Apollo Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###############################################################################


# CMD 
DOCKER_RUN="docker run -dt"
DOCKER_ROOT_DIR="/home"

DOCKER_HUB_USER="353942829"
SPARK_ENV_IMAGE="spark_env"

# main server
SPARK_CONTAINER="spark"
SPARK_IMAGE="spark"
SPARK_PORT="7010"

# mongodb docker
MONGO_CONTAINER="mongo"
MONGO_IMAGE="mongo:4.4.2"
MONGO_PORT="27017"

#  color 
BOLD='\033[1m'
RED='\033[0;31m'
BLUE='\033[0;34m'
GREEN='\033[32m'
WHITE='\033[34m'
YELLOW='\033[33m'
NO_COLOR='\033[0m'

function env() {
  (echo >&2 -e "[${YELLOW} ENV ${NO_COLOR}] $*")
}

function log() {
  (echo >&2 -e "[${GREEN} LOG ${GREEN}${NO_COLOR}]${GREEN} $* ${NO_COLOR}")
}

function ok() {
  (echo >&2 -e "[${GREEN}${BOLD} OK ${NO_COLOR}] $*")
}
