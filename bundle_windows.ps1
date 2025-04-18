$pyinstaller_cmd = "pyinstaller --windowed src/__init__.py --add-data src/assets:./assets --onefile --distpath ./dist"
Write-Output "Preparing to build SmashCore for macOS install"
# Check if the Python script exists
if (Test-Path $pythonScriptPath) {
    Invoke-Expression $pyinstallerCommand
    Copy-Item "README.md" -Destination "./dist/README.md"
    Write-Output "SmashCore install build complete for macOS"
    Write-Output "SmashCore installer can be found in ./dist"
} else {
    Write-Error "Python script not found at '$pythonScriptPath'."
}