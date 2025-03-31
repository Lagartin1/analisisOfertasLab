#!/bin/bash

# Name of the .env file
env_file=".env"

# Check if the .env file already exists
if [ -f "$env_file" ]; then
    echo "The $env_file file already exists. Do you want to overwrite it? (y/n)"
    read response
    if [ "$response" != "y" ]; then
        echo "The file has not been overwritten."
        exit 1
    fi
fi

# Create the .env file with basic variables
echo "Creating the .env file..."

cat <<EOL > "$env_file"
# Config file

LINK_FILE_1=
CSV_CHILETRABAJOS=
CSV_COMPUTRABAJO=

EOL

echo "The .env file has been created successfully."
