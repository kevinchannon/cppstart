param(
  [string]$BuildType = "Debug",
  [string]$InstallDir = "out/build/x64"
)

# Stop the script if any command fails
$ErrorActionPreference = "Stop"

$InstallDir = Join-Path $InstallDir $BuildType

##> APP ONLY :conan install . -s build_type=$BuildType --build=missing -if $InstallDir -pr:b=default
##> LIB ONLY :conan install .\conanfile.py -s build_type=$BuildType --build=missing -if $InstallDir -pr:b=default
##> LIB ONLY :conan install .\test\conanfile.py -s build_type=$BuildType --build=missing -if $InstallDir -pr:b=default

New-Item -ItemType Directory -Path ".cppstart" -Force | Out-Null
$InstallDir | Out-File -FilePath ".cppstart/install_dir_$BuildType"
