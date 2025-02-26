#!/bin/bash

cover-agent --source-file-path="src/main/java/com/davidparry/cover/SimpleMathOperations.java" --test-file-path="src/test/java/com/davidparry/cover/SimpleMathOperationsTest.java" --code-coverage-report-path="build/reports/jacoco/test/jacocoTestReport.csv" --test-command="./gradlew clean test jacocoTestReport" --test-command-dir=$(pwd) --coverage-type="jacoco" --desired-coverage=70 --max-iterations=1
