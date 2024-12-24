#!/bin/bash

# Configuration
BINARY="../cfiles/DES"
GDB_SCRIPT="./scr.gdb"
HOST="localhost"
PORT="1234"
OUTPUT_FILE="/home/sal/HDModel/assemblyfiles/DES_dynamic.txt"

# Ensure the binary exists
if [ ! -f "$BINARY" ]; then
    echo "Error: Binary file does not exist at $BINARY"
    exit 1
fi

# Start gdb-multiarch with the script for remote debugging
gdb-multiarch -x $GDB_SCRIPT -ex "target remote $HOST:$PORT" $BINARY 2>&1 | tee $OUTPUT_FILE


# Check if GDB exited successfully
if [ $? -eq 0 ]; then
    echo "Dynamic disassembly complete. Output saved to $OUTPUT_FILE"
    # Echo the content of the output file
    echo "Displaying output:"
    cat $OUTPUT_FILE
else
    echo "Dynamic disassembly failed."
fi
