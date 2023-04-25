#!/usr/bin/env bash

setup() {
    load 'test_helper/bats-support/load'
    load 'test_helper/bats-assert/load'
    load 'test_helper/bats-file/load'
    DIR="$( cd "$( dirname "$BATS_TEST_FILENAME" )" >/dev/null 2>&1 && pwd )"
    PATH="$DIR/../src:$PATH"
}

teardown_file() {
    rm -rf foo
}

@test "creates a directory for the new project" {
  cppstart foo -c "some user"
  assert_exist foo
}

@test "new project dependencies can be resolved out of the box" {
  cd foo
  ./init.sh
}

@test "new project can be built out of the box" {
  cd foo
  ./build.sh
}