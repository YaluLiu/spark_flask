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
SPARK_ENV_IMAGE="spark_env"
CONTAINER_NAME="spark"
IMAGE_NAME="spark"
DOCKER_ROOT_DIR="/home"
PORT="7010"

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

function ok() {
  (echo >&2 -e "[${GREEN}${BOLD} OK ${NO_COLOR}] $*")
}
