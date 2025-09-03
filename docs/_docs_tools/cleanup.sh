#!/bin/bash


# the absolute paths of this script and it's directory
SCRIPT_PATH=$(realpath -s "$0")
SCRIPT_DIR=$(dirname "$SCRIPT_PATH")
cd $SCRIPT_DIR

source ${SCRIPT_DIR}/paths.sh

rm -r $BUILD_DIR >/dev/null 2>&1
rm -r $OUTPUT_DIR >/dev/null 2>&1
rm -r ../API-Reference >/dev/null 2>&1
rm -r $API_REF_TEMPLATE/*.rst >/dev/null 2>&1

exit 0
