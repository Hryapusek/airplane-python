#!/bin/bash

# Function to process files
process_file() {
    local file="$1"
    echo "$file"
    echo "--------------------"
    cat "$file"
    echo
}

# Export the function so it's available to find
export -f process_file

# Use find to locate files, excluding __pycache__ directories, and process each file
find src -type d -name '__pycache__' -prune -o -type f -exec bash -c 'process_file "$0"' {} \;
