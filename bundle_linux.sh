#!/bin/bash
echo "Preparing to build SmashCore for Linux install"
pyinstaller --windowed --add-data src/assets:./assets --distpath ./dist --name smashCore_linux -F src/main.py
cp README.md ./dist
echo "SmashCore install build complete for Linux"
echo "SmashCore installer can be found in ./dist"
