#!/bin/bash

set -e

BUILD_TYPE="Debug"

while getopts ":t:" opt; do
  case ${opt} in
    t )
      BUILD_TYPE=$OPTARG
      ;;
    \? )
      echo "Invalid option: -$OPTARG" 1>&2
      exit 1
      ;;
    : )
      echo "Invalid option: -$OPTARG requires an argument" 1>&2
      exit 1
      ;;
  esac
done

BUILD_DIR=$(cat .cppstart/install_dir_${BUILD_TYPE})

cmake -B "$BUILD_DIR"
cmake --build "$BUILD_DIR"
