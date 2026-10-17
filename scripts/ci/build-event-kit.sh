#!/usr/bin/env bash
set -euo pipefail
mkdir -p dist
echo "Generating event handout bundle and packaging static assets"
tar -czf dist/event-kit.tar.gz race-day-merchandising-guide.md
