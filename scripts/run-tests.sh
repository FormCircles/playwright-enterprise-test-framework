#!/usr/bin/env bash
set -e

REPORT_DIR="${REPORT_DIR:-/reports}"

mkdir -p "$REPORT_DIR"

TEST_SUITE="${TEST_SUITE:-smoke}"
PETF_ENV="${PETF_ENV:-docker}"

case "$TEST_SUITE" in
  smoke)
    pytest -m smoke \
      --env="$PETF_ENV" \
      --junitxml="$REPORT_DIR/smoke-junit-results.xml" \
      --html="$REPORT_DIR/smoke-report.html" \
      --self-contained-html
    ;;
  api)
    pytest api_tests/tests \
      --env="$PETF_ENV" \
      --junitxml="$REPORT_DIR/api-junit-results.xml" \
      --html="$REPORT_DIR/api-report.html" \
      --self-contained-html
    ;;
  *)
    echo "Unknown suite"
    exit 1
    ;;
esac