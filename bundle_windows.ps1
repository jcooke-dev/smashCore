$pyinstaller_cmd = "pyinstaller --windowed src/main.py --add-data src/assets:./assets --onefile --distpath ./dist --name SmashCore_win"
Write-Output "Preparing to build SmashCore for Windows install"

Invoke-Expression $pyinstaller_cmd
Copy-Item "README.md" -Destination "./dist/README.md"
Write-Output "SmashCore install build complete for Windows"
Write-Output "SmashCore installer can be found in ./dist"
