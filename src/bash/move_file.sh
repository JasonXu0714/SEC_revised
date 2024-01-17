#!/bin/bash

DATA_PATH="$PWD/data"
SOURCE_FOLDER="${1:-}"
DEST_FOLDER="${2:-}"


SOURCE_DIR="$DATA_PATH/$SOURCE_FOLDER"
DEST_DIR="$DATA_PATH/$DEST_FOLDER"

echo $PWD
find "$SOURCE_DIR" -name '*.txt' -exec cp {} "$DEST_DIR" \;
exit 0 