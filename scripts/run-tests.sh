#!/usr/bin/env bash
set -e

REPORT_DIR="${REPORT_DIR:-/reports}"

mkdir -p "$REPORT_DIR"

TEST_SUITE="${TEST_SUITE:-smoke}"
BASE_URL="${BASE_URL:-http://127.0.0.1:8080}"

case "$TEST_SUITE" in
  smoke)
    pytest -m smoke \
      --base-url="$BASE_URL" \
      --junitxml="$REPORT_DIR/smoke-junit-results.xml" \
      --html="$REPORT_DIR/smoke-report.html" \
      --self-contained-html
    ;;
  api)
    pytest api_tests/tests \
      --base-url="$BASE_URL" \
      --junitxml="$REPORT_DIR/api-junit-results.xml" \
      --html="$REPORT_DIR/api-report.html" \
      --self-contained-html
    ;;
  *)
    echo "Unknown suite"
    exit 1
    ;;
esac