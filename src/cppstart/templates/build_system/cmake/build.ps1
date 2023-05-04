param(
  [string]$BuildType = "Debug"
)

$BuildDir = Get-Content ".cppstart/install_dir_$BuildType"

cmake -B $BuildDir
cmake --build $BuildDir