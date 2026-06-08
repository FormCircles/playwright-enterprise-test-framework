#!/usr/bin/env bash
set -e

TEST_SUITE="${TEST_SUITE:-smoke}"
BASE_URL="${BASE_URL:-http://127.0.0.1:8080}"

echo "Running test suite: $TEST_SUITE"
echo "Using BASE_URL: $BASE_URL"

case "$TEST_SUITE" in
  smoke)
    pytest -m smoke --base-url="$BASE_URL"
    ;;
  api)
    pytest api_tests/tests -m api --base-url="$BASE_URL"
    ;;
  ui)
    pytest ui_tests/tests -m ui --base-url="$BASE_URL"
    ;;
  regression)
    pytest -m regression --base-url="$BASE_URL"
    ;;
  all)
    pytest --base-url="$BASE_URL"
    ;;
  *)
    echo "Unknown TEST_SUITE: $TEST_SUITE"
    echo "Supported values: smoke, api, ui, regression, all"
    exit 1
    ;;
esac