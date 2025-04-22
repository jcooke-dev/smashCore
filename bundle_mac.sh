#!/bin/bash
echo "Preparing to build SmashCore for macOS install"
pyinstaller --windowed src/main.py --add-data src/assets:./assets --distpath ./dist --name smashCore_macOS --onefile
cp README.md ./dist
echo "SmashCore install build complete for macOS"
echo "SmashCore installer can be found in ./dist"
