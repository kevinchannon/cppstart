#!/bin/bash

set -e

BUILD_TYPE="Debug"
INSTALL_DIR="out/build/x64"

while getopts ":t:o:" opt; do
  case $opt in
    t)
      BUILD_TYPE="$OPTARG"
      ;;
    o)
      INSTALL_DIR="$OPTARG"
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac
done

conan install . --build=missing -s build_type=$BUILD_TYPE -if $INSTALL_DIR

mkdir -p .cppstart
echo "$INSTALL_DIR" > ".cppstart/install_dir_$BUILD_TYPE"
