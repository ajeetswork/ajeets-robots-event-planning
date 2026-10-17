#!/usr/bin/env bash
set -euo pipefail
echo "Preparing hosted event asset bundle"
mkdir -p dist
cp race-day-merchandising-guide.md dist/guide.md
echo "Uploading hosted event assets"
