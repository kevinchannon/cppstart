#!/bin/bash

set -e

BUILD_TYPE="Debug"
BUILD_DIR=$(<.cppstart/install_dir)

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

BUILD_DIR="$BUILD_DIR"_"$BUILD_TYPE"

cmake -B "$BUILD_DIR"
cmake --build "$BUILD_DIR"
