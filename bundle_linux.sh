#!/bin/bash
echo "Preparing to build SmashCore for Linux install"
pyinstaller --windowed src/__init__.py --paths=src/ --add-data src/assets:./assets --distpath ./dist --name smashCore_linux -F
cp README.md ./dist
echo "SmashCore install build complete for Linux"
echo "SmashCore installer can be found in ./dist"
