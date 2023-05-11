param(
  [string]$BuildType = "Debug",
  [string]$InstallDir = "out/build/x64"
)

# Stop the script if any command fails
$ErrorActionPreference = "Stop"

$InstallDir = Join-Path $InstallDir $BuildType

conan install . -s build_type=$BuildType --build=missing -if $InstallDir

New-Item -ItemType Directory -Path ".cppstart" -Force | Out-Null
$InstallDir | Out-File -FilePath ".cppstart/install_dir_$BuildType"
