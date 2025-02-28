#!/bin/bash

# sudo apt-get update
# sudo apt-get install g++ cmake make lcov libgtest-dev
# pip install lcov_cobertura

# cd /usr/src/gtest
# sudo cmake CMakeLists.txt
# sudo make
# sudo find . -type f -name "*.a" -exec cp {} /usr/lib \;

cover-agent \
  --api-base="https://ark.cn-beijing.volces.com/api/v3" \
  --api-key="key" \
  --model="model" \
  --source-file-path="calculator.cpp" \
  --test-file-path="test_calculator.cpp" \
  --code-coverage-report-path="coverage_filtered.info" \
  --test-command="./build_and_test_with_coverage.sh" \
  --test-command-dir="$(pwd)" \
  --coverage-type="lcov" \
  --desired-coverage=70 \
  --max-iterations=3
