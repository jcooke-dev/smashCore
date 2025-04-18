#!/bin/bash
echo "Preparing to build SmashCore for macOS install"
pyinstaller --windowed src/__init__.py --add-data src/assets:./assets --onefile --distpath ./dist
cp README.md ./dist
echo "SmashCore install build complete for macOS"
echo "SmashCore installer can be found in ./dist"
