#!/bin/bash
set -e

# Build the backup module decks. The command line and the LaTeX run are the
# same as in build.sh. The default output directory is Lectures/modules, so a
# module deck is not mixed with the decks of the core days in Lectures.

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Default output directory for the module decks
OUTPUT_DIR="Lectures/modules"
TEX_FILE=""
FILE_PREFIX=""

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --output)
      OUTPUT_DIR="$2"
      shift 2
      ;;
    --file)
      TEX_FILE="$2"
      shift 2
      ;;
    --prefix)
      FILE_PREFIX="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1"
      echo "Usage: $0 [--file Module_TH-3.tex] [--output Lectures/modules] [--prefix Module_]"
      exit 1
      ;;
  esac
done

# Without --file, build the module decks and nothing else
if [ -z "$TEX_FILE" ] && [ -z "$FILE_PREFIX" ]; then
  FILE_PREFIX="Module_"
fi

# A module deck has the name Module_<ID>.tex. Say so early, so the reader does
# not have to find out later that a core day deck went to Lectures/modules.
if [ -n "$TEX_FILE" ] && [[ ! "$(basename "$TEX_FILE")" == Module_*.tex ]]; then
  echo "Warning: '$TEX_FILE' is not named Module_<ID>.tex. Its PDF still goes to $OUTPUT_DIR/."
fi

# Ensure the output directory exists
mkdir -p "$OUTPUT_DIR"

# Navigate to the source directory
cd "$SCRIPT_DIR/LaTeX" || { echo "Error: Could not find template directory"; exit 1; }

# Collect the list of files to build
BUILD_FILES=""
if [ -n "$TEX_FILE" ]; then
  if [ ! -f "$TEX_FILE" ]; then
    echo "Error: Specified file '$TEX_FILE' not found."
    exit 1
  fi
  BUILD_FILES="$TEX_FILE"
else
  for f in $FILE_PREFIX*.tex; do
    if [ -f "$f" ]; then
      BUILD_FILES="$BUILD_FILES $f"
    fi
  done
  if [ -z "$BUILD_FILES" ]; then
    echo "Error: No LaTeX file matches '${FILE_PREFIX}*.tex'."
    exit 1
  fi
fi

# Build the PDFs. The first run writes the aux files that the second run needs.
echo "Building PDF..."
for f in $BUILD_FILES; do
  latexmk -pdf -shell-escape -interaction=nonstopmode -file-line-error -bibtex -use-make "$f" || echo "Warning: PDF build had issues but continuing..."
  latexmk -pdf -shell-escape -interaction=nonstopmode -file-line-error -bibtex -use-make "$f" || echo "Warning: PDF build had issues but continuing..."
done

# Move the PDFs to the specified output directory
echo "Moving PDFs to $OUTPUT_DIR/"
for f in $BUILD_FILES; do
  PDF_NAME="${f%.tex}.pdf"
  if [ ! -f "$PDF_NAME" ]; then
    echo "Error: LaTeX did not write $PDF_NAME"
    exit 1
  fi
  mv "$PDF_NAME" "../$OUTPUT_DIR/" || { echo "Error: Could not move PDF"; exit 1; }
done

# Clean up auxiliary files. The list holds names that may not exist, so the
# removal uses -f and does not stop the script.
echo "Cleaning up auxiliary files..."
latexmk -C
rm -f *.nav *.snm *.out *.toc *.aux *.bbl *.log *.fdb_latexmk *.fls *.vrb *.bcf *.run.xml *.synctex.gz

echo "Build completed successfully!"