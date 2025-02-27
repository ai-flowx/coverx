#!/bin/bash

# Install gradle & openjdk required
# ./gradlew clean test jacocoTestReport

cover-agent \
  --api-base="https://ark.cn-beijing.volces.com/api/v3" \
  --api-key="key" \
  --model="model" \
  --source-file-path="src/main/java/com/davidparry/cover/SimpleMathOperations.java" \
  --test-file-path="src/test/java/com/davidparry/cover/SimpleMathOperationsTest.java" \
  --code-coverage-report-path="build/reports/jacoco/test/jacocoTestReport.csv" \
  --test-command="./gradlew clean test jacocoTestReport" \
  --test-command-dir="$(pwd)" \
  --coverage-type="jacoco" \
  --desired-coverage=70 \
  --max-iterations=2
