param(
  [string]$BuildType = "Debug"
)

$BuildDir = Get-Content ".cppstart/install_dir_$BuildType"

cmake -B $BuildDir -DCMAKE_TOOLCHAIN_FILE=conan_toolchain.cmake
cmake --build $BuildDir  --config=$BuildType