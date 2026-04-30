#!/bin/bash
# Inject the Zenodo DOI into the manuscript and README once it has been
# minted. Run this from the repo root after you obtain the version-
# specific DOI from Zenodo (e.g., 10.5281/zenodo.1234567).
#
# Usage:
#   ./inject_zenodo_doi.sh 10.5281/zenodo.1234567
#
# This script edits paper/FINAL_PAPER.md and README.md, replacing every
# instance of [ZENODO-DOI-PENDING] with the supplied DOI. It does not
# commit; review the diff with `git diff` before committing.

set -euo pipefail

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <ZENODO_DOI>"
    echo "Example: $0 10.5281/zenodo.1234567"
    exit 1
fi

DOI="$1"

# Sanity check: must look like a DOI
if ! echo "$DOI" | grep -qE '^10\.[0-9]+/'; then
    echo "ERROR: '$DOI' does not look like a DOI (expected format: 10.NNNN/...)"
    exit 1
fi

echo "Injecting DOI: $DOI"
echo ""

# Replace placeholder in manuscript
sed -i.bak "s|\[ZENODO-DOI-PENDING\]|$DOI|g" paper/FINAL_PAPER.md
echo "  Updated paper/FINAL_PAPER.md"

# Replace pending badge and prose in README
sed -i.bak \
    -e "s|\[!\[DOI\](https://img.shields.io/badge/Zenodo-pending-lightgrey.svg)\](https://zenodo.org)|[![DOI](https://zenodo.org/badge/DOI/$DOI.svg)](https://doi.org/$DOI)|" \
    -e "s|will be permanently archived in Zenodo (DOI: \*\*pending\*\*) once the GitHub Release is published|has been permanently archived in Zenodo with DOI **$DOI**|" \
    README.md
echo "  Updated README.md"

# Cleanup .bak files
rm -f paper/FINAL_PAPER.md.bak README.md.bak

echo ""
echo "Done. Review the diff with:"
echo "  git diff paper/FINAL_PAPER.md README.md"
echo ""
echo "Then commit and push:"
echo "  git add paper/FINAL_PAPER.md README.md"
echo "  git commit -m 'Inject Zenodo DOI $DOI'"
echo "  git push origin main"
