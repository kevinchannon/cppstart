cmake_minimum_required(VERSION 3.15)

enable_testing()

add_executable(proj_nameTest
  "proj_name.tests.cpp"
)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

set_property(TARGET proj_nameTest PROPERTY CXX_STANDARD 20)

target_compile_options(proj_nameTest PRIVATE
	$<$<CXX_COMPILER_ID:MSVC>:/W4 /WX>
	$<$<NOT:$<CXX_COMPILER_ID:MSVC>>:-Wall -Wextra -Wpedantic -Werror>
)

target_include_directories(proj_nameTest PRIVATE
	${CMAKE_SOURCE_DIR}
)

target_link_libraries(proj_nameTest
  PRIVATE
    CONAN_PKG::catch2
    proj_nameLib::proj_nameLib
)

list(APPEND CMAKE_MODULE_PATH ${catch2_SOURCE_DIR}/extras)
include(CTest)
include(Catch)

catch_discover_tests(proj_nameTest)

add_test(NAME proj_nameTest COMMAND proj_nameTest)
