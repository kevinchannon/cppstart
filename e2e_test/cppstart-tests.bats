#!/usr/bin/env bash

setup() {
    load 'test_helper/bats-support/load'
    load 'test_helper/bats-assert/load'
    load 'test_helper/bats-file/load'
    DIR="$( cd "$( dirname "$BATS_TEST_FILENAME" )" >/dev/null 2>&1 && pwd )"
    PATH="$DIR/../src:$PATH"
}

teardown() {
    rm -rf ../../foo
}

@test "creates a directory for the new project" {
    PYTHONPATH=../ python src/cppstart/main.py foo --lib -d ../../
    assert_exist ../../foo
}