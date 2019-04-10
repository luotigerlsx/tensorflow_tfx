#!/usr/bin/env bash

# Copyright 2018 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

cd "$( dirname "${BASH_SOURCE[0]}" )"
DIR="$( pwd )"
PROJECT_DIR=${DIR}

export PYTHONPATH=${PYTHONPATH}:${PROJECT_DIR}

python ${PROJECT_DIR}/tf_data_validation_example.py \
    --project=woven-rush-197905 \
    --runner=DataflowRunner \
    --temp_location=gs://tfx_job/tmp \
    --staging_location=gs://tfx_job/tmp \
    --setup_file=${PROJECT_DIR}/setup.py \
    --input_path "gs://tfx_job/census_train.csv" \
    --output_path "gs://tfx_job/output"