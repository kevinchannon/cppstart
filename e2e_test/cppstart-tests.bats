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
    rm -rf bar
}

@test "creates a directory for a new application project" {
  cppstart foo -c "some user"
  assert_exist foo
}

@test "new app project dependencies can be resolved out of the box" {
  cd foo
  ./init.sh
}

@test "new app project can be built out of the box" {
  cd foo
  ./build.sh
}

@test "creates a directory for a new library project" {
  cppstart --lib bar -c "User 2"
  assert_exist bar
}

@test "new lib project dependencies can be resolved out of the box" {
  cd bar
  ./init.sh
}

@test "new lib project can be built out of the box" {
  cd bar
  ./build.sh
}