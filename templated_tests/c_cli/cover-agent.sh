#!/bin/bash

# sudo apt-get update
# sudo apt-get install -y gcc ruby lcov
# pip install lcov_cobertura
# git clone https://github.com/ThrowTheSwitch/Unity.git

cover-agent \
  --api-base="https://ark.cn-beijing.volces.com/api/v3" \
  --api-key="key" \
  --model="model" \
  --source-file-path="calc.c" \
  --test-file-path="test_calc.c" \
  --code-coverage-report-path="coverage_filtered.info" \
  --test-command="./build_and_test_with_coverage.sh" \
  --test-command-dir="$(pwd)" \
  --coverage-type="lcov" \
  --desired-coverage=70 \
  --max-iterations=3
