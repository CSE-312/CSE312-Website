#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOOLS="$(cd "${ROOT}/.." && pwd)/.tools"
DEB="${TOOLS}/quarto.deb"
EXTRACT="${TOOLS}/quarto-extract"
VERSION="1.7.34"
URL="https://github.com/quarto-dev/quarto-cli/releases/download/v${VERSION}/quarto-${VERSION}-linux-amd64.deb"

mkdir -p "${TOOLS}"

if [[ -x "${EXTRACT}/opt/quarto/bin/quarto" ]]; then
  echo "Quarto already installed at ${EXTRACT}/opt/quarto/bin/quarto"
  exit 0
fi

echo "Downloading Quarto ${VERSION}..."
wget -q "${URL}" -O "${DEB}"
dpkg-deb -x "${DEB}" "${EXTRACT}"
echo "Installed Quarto to ${EXTRACT}/opt/quarto/bin/quarto"
