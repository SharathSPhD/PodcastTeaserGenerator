#!/bin/bash
# Podcast Teaser Generator Shell Script
# Usage: ./run_teaser.sh [input_file_or_directory] [duration] [visualize] [exclude_intro_outro] [create_summary]

echo "Podcast Teaser Generator"
echo "-----------------------"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    exit 1
fi

# Set default input path if not provided
INPUT_PATH="${1:-input_tracks}"
echo "Input: $INPUT_PATH"

# Set duration if provided (default: 60)
DURATION="${2:-60}"
echo "Duration: $DURATION seconds"

# Set visualization flag
VISUALIZE=""
if [ "$3" = "visualize" ]; then
    VISUALIZE="--visualize"
    echo "Visualization: Enabled"
else
    echo "Visualization: Disabled"
fi

# Set exclude intro/outro flag
INTRO_OUTRO=""
if [ "$4" = "exclude-intro-outro" ]; then
    INTRO_OUTRO="--no-intro-outro"
    echo "Exclude Intro/Outro: Enabled"
else
    echo "Exclude Intro/Outro: Disabled"
fi

# Set summary flag
SUMMARY=""
if [ "$5" = "create-summary" ]; then
    SUMMARY="--summary"
    echo "Create Summary: Enabled"
else
    echo "Create Summary: Disabled"
fi

# Check if input exists
if [ ! -e "$INPUT_PATH" ]; then
    echo "Error: Input path \"$INPUT_PATH\" does not exist"
    exit 1
fi

# Create output directory if it doesn't exist
if [ ! -d "output_teasers" ]; then
    mkdir -p output_teasers
    echo "Created output directory: output_teasers"
fi

# Run the teaser generator
echo "Running podcast teaser generator..."
echo

python3 podcast_teaser.py "$INPUT_PATH" --duration "$DURATION" $VISUALIZE $INTRO_OUTRO $SUMMARY --output-dir output_teasers --config config.json

if [ $? -ne 0 ]; then
    echo "Error occurred during processing."
else
    echo
    echo "Processing complete! Teasers saved to output_teasers directory."
fi

echo
read -p "Press Enter to continue..."
