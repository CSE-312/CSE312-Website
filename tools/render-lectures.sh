#!/usr/bin/env bash

set -euo pipefail

TOOLS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${TOOLS_DIR}/.." && pwd)"
LECTURES_DIR="${REPO_ROOT}/content/lectures"
QUARTO_BIN="${REPO_ROOT}/.tools/quarto-extract/opt/quarto/bin/quarto"
OUTPUT_DIR="${REPO_ROOT}/static_files/lectures"

export QUARTO_DATA_DIR="${REPO_ROOT}/.quarto-data"

if [[ ! -x "${QUARTO_BIN}" ]]; then
  echo "Quarto not found at ${QUARTO_BIN}." >&2
  echo "Run: tools/install-quarto.sh" >&2
  exit 1
fi

mkdir -p "${QUARTO_DATA_DIR}"
cd "${LECTURES_DIR}"

if [[ $# -gt 0 ]]; then
  target="$1/$1.qmd"
  if [[ ! -f "${target}" ]]; then
    echo "No such lecture source: ${LECTURES_DIR}/${target}" >&2
    exit 1
  fi
  echo "Rendering ${target}..."
  "${QUARTO_BIN}" render "${target}"
else
  echo "Rendering all lectures..."
  "${QUARTO_BIN}" render
fi

rm -f "${OUTPUT_DIR}/index.html" \
      "${OUTPUT_DIR}/search.json" \
      "${OUTPUT_DIR}/listings.json" \
      "${OUTPUT_DIR}/index-listing.json"

echo
echo "Verifying rendered output..."
python3 "${TOOLS_DIR}/verify_output.py" "${OUTPUT_DIR}"

echo
echo "Published to ${OUTPUT_DIR}"
